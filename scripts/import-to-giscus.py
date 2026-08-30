#!/usr/bin/env python3
"""Import a cleaned Disqus export into GitHub Discussions for giscus.

Prereqs:
  gh auth login
  gh auth refresh -s write:discussion,read:discussion

Usage:
  python3 import-to-giscus.py --repo ingorichter/ingorichter.github.io \
      --category Comments --xml discusexport-clean.xml [--dry-run]
  python3 import-to-giscus.py --repo ... --category Comments --reset   # delete all
      discussions in the category, then exit

The run is IDEMPOTENT - safe to run again:
  * a Discussion is matched by the giscus hash <!-- sha1: <sha1(term)> --> in its
    body (term = pathname without leading slash, per giscus client.ts); reused if
    it already exists, created otherwise.
  * every imported comment carries a hidden marker <!-- dsq:<disqus-post-id> -->;
    on re-run, comments already carrying their marker are skipped, so a partial
    or repeated run only fills in what is missing - no duplicates.

Replies are nested one level (GitHub's max) via replyToId.
"""
import argparse, hashlib, html, json, re, subprocess, sys, datetime

def gql(query, variables=None):
    variables = variables or {}
    p = subprocess.run(
        # -f sends every var as a raw string; GitHub coerces string -> ID/String.
        ["gh", "api", "graphql", "-f", f"query={query}"]
        + sum(([f"-f", f"{k}={v}"] for k, v in variables.items()), []),
        capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit(f"gh api error:\n{p.stderr}\n{p.stdout}")
    out = json.loads(p.stdout)
    if out.get("errors"):
        sys.exit("graphql errors:\n" + json.dumps(out["errors"], indent=2))
    return out["data"]

def term_for(path):
    return "index" if len(path) < 2 else re.sub(r"\.\w+$", "", path[1:])

def sha1_hex(s):
    return hashlib.sha1(s.encode()).hexdigest()

def disqus_html_to_md(s):
    s = re.sub(r"^<!\[CDATA\[|\]\]>$", "", s.strip())
    s = re.sub(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', r"[\2](\1)", s, flags=re.S)
    s = s.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    s = re.sub(r"</p>\s*<p>", "\n\n", s)
    s = re.sub(r"</?p>", "", s)
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).strip()

def parse_xml(path):
    x = open(path, encoding="utf-8").read()
    threads = {}
    for m in re.finditer(r'<thread dsq:id="(\d+)">(.*?)</thread>', x, re.S):
        tid, b = m.groups()
        link = re.search(r"<link>(.*?)</link>", b).group(1).strip()
        title = re.search(r"<title>(.*?)</title>", b)
        threads[tid] = {
            "link": link,
            "title": html.unescape(title.group(1)) if title else link,
            "path": re.sub(r"^https?://[^/]+", "", link) or "/",
            "posts": [],
        }
    for m in re.finditer(r'<post dsq:id="(\d+)">(.*?)</post>', x, re.S):
        pid, b = m.groups()
        tref = re.search(r'<thread dsq:id="(\d+)"', b).group(1)
        par = re.search(r'<parent dsq:id="(\d+)"', b)
        threads[tref]["posts"].append({
            "id": pid,
            "parent": par.group(1) if par else None,
            "name": html.unescape(re.search(r"<author>.*?<name>(.*?)</name>", b, re.S).group(1).strip()),
            "created": re.search(r"<createdAt>(.*?)</createdAt>", b).group(1),
            "body": disqus_html_to_md(re.search(r"<message>(.*?)</message>", b, re.S).group(1)),
        })
    for t in threads.values():
        t["posts"].sort(key=lambda p: p["created"])
    return threads

def resolve_repo_category(owner, name, category):
    d = gql("query($o:String!,$n:String!){repository(owner:$o,name:$n){id "
            "discussionCategories(first:20){nodes{id name}}}}",
            {"o": owner, "n": name})["repository"]
    cats = {c["name"]: c["id"] for c in d["discussionCategories"]["nodes"]}
    if category not in cats:
        sys.exit(f"category {category!r} not found. have: {list(cats)}")
    return d["id"], cats[category]

def find_discussion(repo, category, h):
    q = f'repo:{repo} category:"{category}" in:body "{h}"'
    nodes = gql(
        "query($q:String!){search(query:$q,type:DISCUSSION,first:1){nodes{"
        "... on Discussion{id url comments(first:100){nodes{id body "
        "replies(first:100){nodes{id body}}}}}}}}", {"q": q})["search"]["nodes"]
    if not nodes:
        return None
    disc = nodes[0]
    seen = {}  # disqus post id -> comment node id
    for c in disc["comments"]["nodes"]:
        for node in [c] + c["replies"]["nodes"]:
            m = re.search(r"<!--\s*dsq:(\d+)\s*-->", node["body"] or "")
            if m:
                seen[m.group(1)] = c["id"]  # map replies to their top-level comment
    disc["seen"] = seen
    return disc

def reset(repo, owner, name, cat_id, category):
    nodes = gql("query($o:String!,$n:String!,$c:ID!){repository(owner:$o,name:$n){"
                "discussions(first:100,categoryId:$c){nodes{id title}}}}",
                {"o": owner, "n": name, "c": cat_id})["repository"]["discussions"]["nodes"]
    if not nodes:
        print("no discussions in category", category)
        return
    print(f"about to DELETE {len(nodes)} discussion(s) in {repo} / {category}:")
    for x in nodes:
        print("  -", x["title"])
    if input("type 'delete' to confirm: ").strip() != "delete":
        sys.exit("aborted")
    for x in nodes:
        gql("mutation($i:ID!){deleteDiscussion(input:{id:$i}){clientMutationId}}",
            {"i": x["id"]})
        print("deleted", x["title"])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--category", required=True)
    ap.add_argument("--xml", default="discusexport-clean.xml")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--reset", action="store_true")
    args = ap.parse_args()
    owner, name = args.repo.split("/")

    if args.dry_run:
        for t in parse_xml(args.xml).values():
            print(f"\n=== {t['path']}  ({len(t['posts'])} comments)  "
                  f"sha1={sha1_hex(term_for(t['path']))}")
            for p in t["posts"]:
                tag = " [reply]" if p["parent"] else ""
                print(f"  - {p['name']} ({p['created'][:10]}){tag}: {p['body'][:70]}")
        return

    repo_id, cat_id = resolve_repo_category(owner, name, args.category)

    if args.reset:
        reset(args.repo, owner, name, cat_id, args.category)
        return

    for t in parse_xml(args.xml).values():
        term = term_for(t["path"])
        h = sha1_hex(term)
        print(f"\n=== {t['path']}  ({len(t['posts'])} comments)  sha1={h}")

        disc = find_discussion(args.repo, args.category, h)
        if disc:
            print(f"  reuse {disc['url']}  ({len(disc['seen'])} comments already imported)")
        else:
            body = (f"Comment thread for <{t['link']}>\n\nImported from Disqus.\n\n"
                    f"<!-- sha1: {h} -->")
            disc = gql("mutation($r:ID!,$c:ID!,$t:String!,$b:String!){createDiscussion("
                       "input:{repositoryId:$r,categoryId:$c,title:$t,body:$b})"
                       "{discussion{id url}}}",
                       {"r": repo_id, "c": cat_id, "t": term, "b": body})["createDiscussion"]["discussion"]
            disc["seen"] = {}
            print(f"  created {disc['url']}")

        made = dict(disc["seen"])  # disqus post id -> top-level comment node id
        for p in t["posts"]:
            if p["id"] in disc["seen"]:
                print(f"    = {p['name']} (already imported)")
                continue
            when = datetime.date.fromisoformat(p["created"][:10]).strftime("%B %-d, %Y")
            cbody = (f"> **{p['name']}** · {when} · imported from Disqus\n\n"
                     f"{p['body']}\n\n<!-- dsq:{p['id']} -->")
            variables = {"d": disc["id"], "b": cbody}
            mut = ("mutation($d:ID!,$b:String!{extra}){{addDiscussionComment(input:{{"
                   "discussionId:$d,body:$b{arg}}}){{comment{{id}}}}}}")
            if p["parent"] and p["parent"] in made:
                q = mut.format(extra=",$p:ID!", arg=",replyToId:$p")
                variables["p"] = made[p["parent"]]
            else:
                q = mut.format(extra="", arg="")
            cid = gql(q, variables)["addDiscussionComment"]["comment"]["id"]
            made[p["id"]] = cid
            print(f"    + {p['name']}")

if __name__ == "__main__":
    main()
