"""Announce new blog posts on Mastodon and Bluesky.

Reads the built RSS feed (public/index.xml), compares every entry against a
small state file of already-announced entry IDs, and posts one announcement
per genuinely new entry. This means several posts published on the same day
each get their own toot/skeet, in chronological order.

State handling
--------------
- State file: scripts/.announce-state.json  ({"announced": [ids...]})
  In CI it is persisted between runs via actions/cache.
- First run (no state file): every current entry is recorded as "already
  announced" and nothing is posted. This avoids spamming the back catalog.
- The newest N entries are considered each run (OLDEST_FIRST) so the timeline
  order matches publish order.

Environment
-----------
MASTODON_TOKEN         required for Mastodon
MASTODON_INSTANCE      default https://mastodon.social
BLUESKY_HANDLE         optional
BLUESKY_APP_PASSWORD   optional
ANNOUNCE_SECTIONS      comma-separated URL path segments to include,
                       default "post" (set to "" to announce every entry)
ANNOUNCE_STATE_FILE    default scripts/.announce-state.json
ANNOUNCE_MAX_ENTRIES   how many recent entries to inspect, default 15
ANNOUNCE_DRY_RUN       if set, print instead of posting
"""

import json
import os
import sys
from urllib.parse import urljoin, urlparse

import feedparser
import requests

SITE_URL = "https://ingo-richter.io"
FEED_PATH = "public/index.xml"

STATE_FILE = os.environ.get("ANNOUNCE_STATE_FILE", "scripts/.announce-state.json")
MAX_ENTRIES = int(os.environ.get("ANNOUNCE_MAX_ENTRIES", "15"))
DRY_RUN = bool(os.environ.get("ANNOUNCE_DRY_RUN"))
SECTIONS = [s.strip() for s in os.environ.get("ANNOUNCE_SECTIONS", "post").split(",") if s.strip()]


def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return set(data.get("announced", [])), True
    except (FileNotFoundError, json.JSONDecodeError):
        return set(), False


def save_state(announced):
    os.makedirs(os.path.dirname(STATE_FILE) or ".", exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as fh:
        # keep it bounded so the file does not grow forever
        json.dump({"announced": sorted(announced)[-500:]}, fh, indent=2)
        fh.write("\n")


def entry_id(entry):
    return entry.get("id") or entry.get("link")


def normalize_link(link):
    if not link:
        return link
    parsed = urlparse(link)
    # local builds use http://localhost:1313 - rewrite onto the real host
    if parsed.scheme in ("http", "https") and parsed.hostname not in (None, "ingo-richter.io"):
        return urljoin(SITE_URL, parsed.path)
    if not link.startswith("http"):
        return urljoin(SITE_URL, link)
    return link


def wanted(entry):
    if not SECTIONS:
        return True
    path = urlparse(entry.get("link") or "").path
    return any(f"/{seg}/" in path for seg in SECTIONS)


def announce_mastodon(title, link):
    token = os.environ.get("MASTODON_TOKEN")
    if not token:
        print("MASTODON_TOKEN not set. Skipping Mastodon.")
        return
    instance = os.environ.get("MASTODON_INSTANCE", "https://mastodon.social")
    status = f'New blog post: "{title}" {link}'
    if DRY_RUN:
        print(f"[dry-run] Mastodon: {status}")
        return
    resp = requests.post(
        f"{instance}/api/v1/statuses",
        headers={"Authorization": f"Bearer {token}"},
        data={"status": status},
        timeout=30,
    )
    resp.raise_for_status()
    print(f"Mastodon: announced {title!r}")


def announce_bluesky(title, link):
    handle = os.environ.get("BLUESKY_HANDLE")
    app_password = os.environ.get("BLUESKY_APP_PASSWORD")
    if not (handle and app_password):
        print("Bluesky credentials not set. Skipping Bluesky.")
        return
    from atproto import Client as AtprotoClient
    from atproto import client_utils

    text = (
        client_utils.TextBuilder()
        .text(f'New blog post: "{title}" ')
        .link(link, link)
    )
    if DRY_RUN:
        print(f"[dry-run] Bluesky: New blog post: {title!r} {link}")
        return
    client = AtprotoClient()
    client.login(handle, app_password)
    client.send_post(text)
    print(f"Bluesky: announced {title!r}")


def main():
    feed = feedparser.parse(FEED_PATH)
    if not feed.entries:
        print(f"Error: no entries in {FEED_PATH}.")
        sys.exit(1)

    announced, had_state = load_state()

    # feed is newest-first; inspect a bounded window, then post oldest-first
    window = [e for e in feed.entries[:MAX_ENTRIES] if wanted(e)]

    if not had_state:
        for e in window:
            announced.add(entry_id(e))
        save_state(announced)
        print(f"Seeded state with {len(announced)} entries. No announcements on first run.")
        return

    new_entries = [e for e in reversed(window) if entry_id(e) not in announced]
    if not new_entries:
        print("No new posts to announce.")
        return

    failures = 0
    for entry in new_entries:
        title = entry.title
        link = normalize_link(entry.get("link"))
        print(f"Announcing: {title!r} -> {link}")
        try:
            announce_mastodon(title, link)
            announce_bluesky(title, link)
        except Exception as exc:  # keep going, retry next run
            failures += 1
            print(f"  failed: {exc}")
            continue
        announced.add(entry_id(entry))

    save_state(announced)
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
