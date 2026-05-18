"""publisher.py

Reads a spec JSON and its corresponding draft Markdown, then publishes (or creates a draft)
on Medium via the Medium API v1.

After a successful publish, updates published/tracking.json with the post's URL and ID.

Usage:
    python engine/publisher.py --spec specs/my-article.json --draft drafts/my-article.md

Environment variables required:
    MEDIUM_TOKEN    - Your Medium integration token
    MEDIUM_USER_ID  - Your Medium user ID (obtain via GET /v1/me)

The spec must have "publish": true to post as a public article.
If "publish" is false the post will be created as a Medium draft so you can preview it.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


MEDIUM_API_BASE = "https://api.medium.com/v1"
TRACKING_FILE = Path(__file__).resolve().parents[1] / "published" / "tracking.json"


def load_tracking() -> dict:
    if TRACKING_FILE.exists():
        return json.loads(TRACKING_FILE.read_text(encoding="utf-8"))
    return {"articles": []}


def save_tracking(data: dict) -> None:
    TRACKING_FILE.parent.mkdir(parents=True, exist_ok=True)
    TRACKING_FILE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def already_published(tracking: dict, spec_id: str) -> bool:
    return any(a.get("id") == spec_id for a in tracking.get("articles", []))


def publish_to_medium(token: str, user_id: str, spec: dict, draft_content: str) -> dict:
    publish_status = "public" if spec.get("publish") else "draft"

    # Medium API accepts Markdown content
    body = {
        "title": spec["title"],
        "contentFormat": "markdown",
        "content": draft_content,
        "tags": spec.get("tags", [])[:5],  # Medium allows up to 5 tags
        "publishStatus": publish_status,
    }

    url = f"{MEDIUM_API_BASE}/users/{user_id}/posts"
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8")
        print(f"Medium API error {exc.code}: {error_body}", file=sys.stderr)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish a draft to Medium via the API.")
    parser.add_argument("--spec", required=True, type=Path, help="Path to spec JSON file")
    parser.add_argument("--draft", required=True, type=Path, help="Path to draft Markdown file")
    args = parser.parse_args()

    token = os.environ.get("MEDIUM_TOKEN", "").strip()
    user_id = os.environ.get("MEDIUM_USER_ID", "").strip()

    if not token or not user_id:
        print("Error: MEDIUM_TOKEN and MEDIUM_USER_ID environment variables must be set.", file=sys.stderr)
        sys.exit(1)

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    draft_content = args.draft.read_text(encoding="utf-8")

    tracking = load_tracking()

    if already_published(tracking, spec["id"]):
        print(f"Article '{spec['id']}' is already in tracking.json — skipping.")
        sys.exit(0)

    print(f"Publishing '{spec['title']}' to Medium (status: {'public' if spec.get('publish') else 'draft'})...")
    result = publish_to_medium(token, user_id, spec, draft_content)

    post_data = result.get("data", {})
    entry = {
        "id": spec["id"],
        "title": spec["title"],
        "medium_post_id": post_data.get("id", ""),
        "url": post_data.get("url", ""),
        "publish_status": post_data.get("publishStatus", ""),
        "published_at": datetime.now(timezone.utc).isoformat(),
        "spec_file": str(args.spec),
        "draft_file": str(args.draft),
    }

    tracking["articles"].append(entry)
    save_tracking(tracking)

    print(f"Done. URL: {entry['url']}")
    print(f"Tracking updated: {TRACKING_FILE}")


if __name__ == "__main__":
    main()
