"""publisher.py

Reads a spec JSON and its corresponding draft Markdown, then publishes the article
to either Dev.to or Medium (legacy) via their respective APIs.

After a successful publish, updates published/tracking.json with the post URL and ID.

Usage:
    # Publish to Dev.to (default, recommended — free API, no token restrictions)
    python engine/publisher.py --spec specs/my-article.json --draft drafts/my-article.md

    # Publish to Medium (only if you already have a legacy integration token)
    python engine/publisher.py --spec specs/my-article.json --draft drafts/my-article.md --target medium

Environment variables:

  Dev.to (default):
    DEVTO_API_KEY   - Your Dev.to API key (Settings → Extensions → DEV Community API Keys)

  Medium (legacy — new tokens no longer issued as of 2025):
    MEDIUM_TOKEN    - Your Medium integration token
    MEDIUM_USER_ID  - Your Medium user ID (GET https://api.medium.com/v1/me)

The spec must have "publish": true to post as a public article.
If "publish" is false the article is created as a draft for preview.
"""

from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


DEVTO_API_BASE = "https://dev.to/api"
MEDIUM_API_BASE = "https://api.medium.com/v1"
TRACKING_FILE = Path(__file__).resolve().parents[1] / "published" / "tracking.json"
ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


def _load_env_file() -> None:
    """Load key=value pairs from .env into os.environ (if the file exists)."""
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


# ---------------------------------------------------------------------------
# Tracking helpers
# ---------------------------------------------------------------------------

def load_tracking() -> dict:
    if TRACKING_FILE.exists():
        return json.loads(TRACKING_FILE.read_text(encoding="utf-8"))
    return {"articles": []}


def save_tracking(data: dict) -> None:
    TRACKING_FILE.parent.mkdir(parents=True, exist_ok=True)
    TRACKING_FILE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def already_published(tracking: dict, spec_id: str) -> bool:
    return any(a.get("id") == spec_id for a in tracking.get("articles", []))


def _ssl_context(verify: bool) -> ssl.SSLContext:
    """Return an SSL context. Set verify=False in corporate proxy environments."""
    if verify:
        return ssl.create_default_context()
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


# ---------------------------------------------------------------------------
# Dev.to publisher
# ---------------------------------------------------------------------------

def publish_to_devto(api_key: str, spec: dict, draft_content: str, verify_ssl: bool = True) -> dict:
    """POST an article to Dev.to. Returns the API response dict."""
    published = bool(spec.get("publish"))

    body = {
        "article": {
            "title": spec["title"],
            "body_markdown": draft_content,
            "published": published,
            "tags": spec.get("tags", [])[:4],  # Dev.to allows up to 4 tags
        }
    }

    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        f"{DEVTO_API_BASE}/articles",
        data=data,
        headers={
            "api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "spec2pr-publisher/1.0 (https://github.com/mchellappa/spec2pr-articles)",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, context=_ssl_context(verify_ssl)) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8")
        print(f"Dev.to API error {exc.code}: {error_body}", file=sys.stderr)
        raise


# ---------------------------------------------------------------------------
# Medium publisher (legacy)
# ---------------------------------------------------------------------------

def publish_to_medium(token: str, user_id: str, spec: dict, draft_content: str, verify_ssl: bool = True) -> dict:
    """POST an article to Medium. Returns the API response dict.

    NOTE: Medium stopped issuing new integration tokens in 2025.
    This function only works if you already have a legacy token.
    """
    publish_status = "public" if spec.get("publish") else "draft"

    body = {
        "title": spec["title"],
        "contentFormat": "markdown",
        "content": draft_content,
        "tags": spec.get("tags", [])[:5],
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
        with urllib.request.urlopen(req, context=_ssl_context(verify_ssl)) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8")
        print(f"Medium API error {exc.code}: {error_body}", file=sys.stderr)
        raise


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Publish a draft article via Dev.to or Medium API.")
    parser.add_argument("--spec", required=True, type=Path, help="Path to spec JSON file")
    parser.add_argument("--draft", required=True, type=Path, help="Path to draft Markdown file")
    parser.add_argument(
        "--target",
        choices=["devto", "medium"],
        default="devto",
        help="Publish target: 'devto' (default, recommended) or 'medium' (requires legacy token)",
    )
    parser.add_argument(
        "--no-verify-ssl",
        action="store_true",
        default=False,
        help="Disable SSL certificate verification (use on corporate networks with proxy inspection)",
    )
    args = parser.parse_args()

    _load_env_file()

    verify_ssl = not args.no_verify_ssl
    if not verify_ssl:
        print("Warning: SSL verification disabled (corporate proxy mode).", file=sys.stderr)

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    draft_content = args.draft.read_text(encoding="utf-8")
    tracking = load_tracking()

    if already_published(tracking, spec["id"]):
        print(f"Article '{spec['id']}' is already in tracking.json — skipping.")
        sys.exit(0)

    publish_label = "public" if spec.get("publish") else "draft"

    if args.target == "devto":
        api_key = os.environ.get("DEVTO_API_KEY", "").strip()
        if not api_key:
            print("Error: DEVTO_API_KEY environment variable must be set.", file=sys.stderr)
            print("Get your key at: https://dev.to/settings/extensions", file=sys.stderr)
            sys.exit(1)

        print(f"Publishing '{spec['title']}' to Dev.to ({publish_label})...")
        result = publish_to_devto(api_key, spec, draft_content, verify_ssl=verify_ssl)

        entry = {
            "id": spec["id"],
            "title": spec["title"],
            "target": "devto",
            "post_id": str(result.get("id", "")),
            "url": result.get("url", ""),
            "publish_status": publish_label,
            "published_at": datetime.now(timezone.utc).isoformat(),
            "spec_file": str(args.spec),
            "draft_file": str(args.draft),
        }

    else:  # medium
        token = os.environ.get("MEDIUM_TOKEN", "").strip()
        user_id = os.environ.get("MEDIUM_USER_ID", "").strip()
        if not token or not user_id:
            print("Error: MEDIUM_TOKEN and MEDIUM_USER_ID must be set.", file=sys.stderr)
            print("Note: Medium stopped issuing new tokens in 2025.", file=sys.stderr)
            sys.exit(1)

        print(f"Publishing '{spec['title']}' to Medium ({publish_label})...")
        result = publish_to_medium(token, user_id, spec, draft_content, verify_ssl=verify_ssl)
        post_data = result.get("data", {})

        entry = {
            "id": spec["id"],
            "title": spec["title"],
            "target": "medium",
            "post_id": post_data.get("id", ""),
            "url": post_data.get("url", ""),
            "publish_status": publish_label,
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
