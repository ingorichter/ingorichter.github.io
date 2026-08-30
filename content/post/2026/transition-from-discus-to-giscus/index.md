+++
categories = ["TIL"]
date = "2026-08-29T20:48:48-07:00"
description = "Moving my blog's comments from Disqus to giscus: enabling GitHub Discussions, exporting old comments, and importing them with a small script."
draft = false
id = "94f2a349236206ce9e8564684bf1c580e3bb48cd"
link = ""
tags = ["TIL"]
title = "Transition From Disqus to giscus"
[params]
  [[headerimage]]
    src = "header.svg"
    alt = "The word Disqus struck through, an arrow pointing to a green giscus speech bubble labelled 'powered by GitHub Discussions'"
    stretch = "horizontal"
+++

<!--more-->

For a long time I've wanted to move away from [Disqus](https://disqus.com) to [giscus](https://giscus.app), for a few reasons. Back when I started this blog, Disqus was a convenient way to add comments. But there are plenty of reports about how invasive Disqus is: how much tracking it injects into a page, and how much the platform is disliked in general.

The post that finally pushed me over the edge was Rob J. Hyndman's [Moving from Disqus to giscus](https://robjhyndman.com/hyndsight/disqus2giscus.html). I found it a while ago and it stuck with me.

So here I am, staring at a pile of work to enable giscus for my blog. Let's go.

## This is a multi-step process

Here's the rough shape of it:

1. Enable Discussions in my GitHub repo
2. Generate the giscus config values
3. Export the Disqus comments
4. Fix the URLs in the export
5. Import the comments into GitHub Discussions
6. Update the Hugo config
7. Replace the comments template
8. Verify comments show up on the blog

## Enable Discussions in my GitHub repo

1. Repo Settings → General → Features → check "Discussions".
2. Install the giscus GitHub App: <https://github.com/apps/giscus> → Configure → grant it to `ingorichter/ingorichter.github.io` only. Grant `Read access to metadata` and `Read and write access to discussions`. This step requires authentication.
3. The `ingorichter/ingorichter.github.io` repo must be public. Check!
4. Create a Discussions category for comments:
    - Repo Discussions → Categories (pencil icon) → New category.
    - Name: `Comments`. Type: `Announcements` (only maintainers open threads — giscus opens them via the app, visitors only reply). Format: `Open-ended discussion`, but this can't be selected — it's the default for this type.

## Generate the giscus config values

Go to <https://giscus.app> and fill in the form:

- Repository: `ingorichter/ingorichter.github.io`
- Page ↔ Discussions mapping: `pathname`
- Enable "Use strict title matching"
- Category: `Comments`
- Enable "Only search for discussions in this category"
- Enable "Load the comments lazily"
- Use the "Preferred color scheme" theme

Copy the generated script. It's used later in the Hugo `comments.html`:

```html
<script src="https://giscus.app/client.js"
        data-repo="ingorichter/ingorichter.github.io"
        data-repo-id="MDEwOlJlcG9zaXRvcnkxMDgwNjQ0Mw=="
        data-category="Comments"
        data-category-id="DIC_kwDOAKTkq84DEfQE"
        data-mapping="pathname"
        data-strict="1"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="preferred_color_scheme"
        data-lang="en"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>
```

## Export the Disqus comments

I wanted to keep as many of the Disqus comments as possible. There are only a few, but they matter to me.

1. Disqus admin → your site → Community → Export (or `https://<shortname>.disqus.com/admin/discussions/export/`). Shortname: `ingorichterio`.
2. Wait for the email → download `<shortname>-<date>.xml.gz` → `gunzip` it to `.xml`.

The email arrived fast.

## Fix the URLs in the Disqus export

I asked Claude to help me identify which comments are still live and worth saving. After some back and forth, I had a cleaned-up, minimal XML file to use in the next step.

## Import into GitHub Discussions

I used Claude to help me write an importer [script](https://github.com/ingorichter/ingorichter.github.io/blob/master/scripts/import-to-giscus.py) that consumes the Disqus export file.

It talks to GitHub through the `gh` CLI, so it needs the `read:discussion` and `write:discussion` scopes on my `gh` login. I had to run `gh auth refresh -s write:discussion,read:discussion` before running the script:

```bash
# dry run — already ran, output looked good
python3 import-to-giscus.py --repo ingorichter/ingorichter.github.io --category Comments --dry-run

# real run
python3 import-to-giscus.py --repo ingorichter/ingorichter.github.io --category Comments
```

The script creates one Discussion per thread (title = pathname) and posts each Disqus comment on it, preserving the author name and date in the body. Replies stay threaded under their parent comment.

I improved the import script until it was idempotent and added an option to wipe all previously imported comments. That helps a lot while testing, right up until everything goes live.

> GitHub's Discussion search index lags a minute or two behind. If you re-run the script right away, it might not see the Discussions it just created. Wait a bit between runs.

## Update the Hugo config

Remove the Disqus config from `config.toml`:

```toml
[services.disqus]
shortname = 'ingorichterio'
```

Add this block instead. The `repoID` and `categoryID` are part of the `<script>` generated on the giscus site (see above):

```toml
[params.giscus]
repo = "ingorichter/ingorichter.github.io"
repoID = "MDEwOlJlcG9zaXRvcnkxMDgwNjQ0Mw=="
category = "Comments"
categoryID = "DIC_kwDOAKTkq84DEfQE"
mapping = "pathname"
strict = "1"
reactionsEnabled = "1"
inputPosition = "top"
theme = "preferred_color_scheme"
```

## Replace the comments template

I needed a new template for Hugo to render the giscus comment section on each post, so I added a new file at `layouts/_default/comments.html`:

```go
{{- $g := .Site.Params.giscus -}}
{{- if and $g $g.repo $g.repoID (ne .Params.comments false) (not .Params.menu) -}}
  <section class="comments">
    <h2>Comments</h2>
    <script src="https://giscus.app/client.js"
      data-repo="{{ $g.repo }}"
      data-repo-id="{{ $g.repoID }}"
      data-category="{{ $g.category }}"
      data-category-id="{{ $g.categoryID }}"
      data-mapping="{{ default "pathname" $g.mapping }}"
      data-strict="{{ default "1" $g.strict }}"
      data-reactions-enabled="{{ default "1" $g.reactionsEnabled }}"
      data-emit-metadata="0"
      data-input-position="{{ default "top" $g.inputPosition }}"
      data-theme="{{ default "preferred_color_scheme" $g.theme }}"
      data-lang="en"
      data-loading="lazy"
      crossorigin="anonymous"
      async>
    </script>
    <noscript>Enable JavaScript to view comments.</noscript>
  </section>
{{- end -}}
```

Now `.Render "comments"` in `single.html` picks it up unchanged. Opt out per post with `comments: false` in the front matter.

## Verify comments show up on the blog

Run `make preview` to launch the local Hugo server.

- Open a post whose thread you test-imported → the giscus box loads and the old comments show.
- Check the browser console for a giscus "discussion not found" error — that means a pathname mismatch (see step 4).
- Run `make build`, then `grep -r disqus public/` to confirm it's gone.

One comment came through mapped to the wrong thread. I fixed the script, wiped the imported comments (the reset option earned its keep here), and re-ran the import with the corrected Disqus export XML. That sorted it out.

## Done

After about an hour of work, I cut ties with Disqus. giscus works just fine, and I'm happy to run something less invasive.

Thanks to the maintainers for a great piece of open source software.

Mahalo 🌸
