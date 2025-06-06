import os
import feedparser
import requests
from atproto import Client as AtprotoClient  # For Bluesky
from urllib.parse import urljoin

# 1. Parse RSS feed
feed = feedparser.parse("public/index.xml")
if not feed.entries:
    print("Error: No entries found in the RSS feed. Please check the feed path and content.")
    exit(1)
latest = feed.entries[0]  # newest first

title = latest.title
link = latest.link

site_url = "https://ingo-richter.io"  # blog URL

# Ensure link starts with https://
if not link.startswith('http'):
    link = urljoin(site_url, link)

# 2. Announce to Mastodon
mastodon_token = os.environ["MASTODON_TOKEN"]
mastodon_instance = os.environ.get("MASTODON_INSTANCE", "https://mastodon.social")
mastodon_status = f'New blog post: "{title}" {link}'

resp = requests.post(
    f"{mastodon_instance}/api/v1/statuses",
    headers={"Authorization": f"Bearer {mastodon_token}"},
    data={"status": mastodon_status}
)
resp.raise_for_status()

# 3. Announce to Bluesky (using atproto)
bsky_handle = os.environ.get("BLUESKY_HANDLE")
bsky_app_password = os.environ.get("BLUESKY_APP_PASSWORD")
if bsky_handle and bsky_app_password:
    bsky = AtprotoClient()
    bsky.login(bsky_handle, bsky_app_password)
    bsky.send_post(f'New blog post: "{title}" {link}')
    print("Announcement posted to Bluesky!")
else:
    print("Bluesky credentials not set. Skipping Bluesky announcement.")

print("Announcement posted to Mastodon and Bluesky!")