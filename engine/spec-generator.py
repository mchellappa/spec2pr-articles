from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

REQUIRED_KEYS = {
    "id",
    "title",
    "audience",
    "tone",
    "key_thesis",
    "sections",
    "tags",
    "publish",
}
MIN_TAG_LENGTH = 4
MAX_TAG_COUNT = 5
STOP_WORDS = {
    "about",
    "from",
    "that",
    "this",
    "with",
    "into",
    "when",
    "where",
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "untitled-idea"


def generate_spec(idea_markdown: str, source_id: str = "") -> dict[str, Any]:
    lines = [line.strip() for line in idea_markdown.splitlines() if line.strip()]

    title = next((line.lstrip("# ").strip() for line in lines if line.startswith("#")), "Untitled Idea")
    audience = _extract_prefixed_value(lines, "Audience:")
    tone = _extract_prefixed_value(lines, "Tone:")

    body_lines = [
        line
        for line in lines
        if not line.startswith("#")
        and not line.startswith("Audience:")
        and not line.startswith("Tone:")
        and not line.startswith("Key points:")
        and not line.startswith("-")
    ]
    key_thesis = " ".join(body_lines).strip() or f"{title} in a practical format for {audience}."

    bullets = [line.lstrip("- ").strip() for line in lines if line.startswith("-")]
    sections = [
        {
            "heading": heading,
            "intent": f"Explain {heading.lower()} with practical examples.",
        }
        for heading in bullets
    ]
    if not sections:
        sections = [{"heading": "Main Idea", "intent": "Explain the core thesis clearly."}]

    raw_tags = _extract_tags(title, key_thesis)

    spec = {
        "id": slugify(source_id or title),
        "title": title,
        "audience": audience,
        "tone": tone,
        "key_thesis": key_thesis,
        "sections": sections,
        "tags": raw_tags,
        "publish": False,
    }
    validate_spec_schema(spec)
    return spec


def validate_spec_schema(spec: dict[str, Any]) -> None:
    missing = REQUIRED_KEYS - set(spec.keys())
    if missing:
        raise ValueError(f"Missing required keys: {sorted(missing)}")

    if not isinstance(spec["id"], str) or not spec["id"]:
        raise ValueError("'id' must be a non-empty string")
    if not isinstance(spec["title"], str) or not spec["title"]:
        raise ValueError("'title' must be a non-empty string")
    if not isinstance(spec["audience"], str) or not spec["audience"]:
        raise ValueError("'audience' must be a non-empty string")
    if not isinstance(spec["tone"], str) or not spec["tone"]:
        raise ValueError("'tone' must be a non-empty string")
    if not isinstance(spec["key_thesis"], str) or not spec["key_thesis"]:
        raise ValueError("'key_thesis' must be a non-empty string")
    if not isinstance(spec["publish"], bool):
        raise ValueError("'publish' must be a boolean")

    sections = spec["sections"]
    if not isinstance(sections, list) or not sections:
        raise ValueError("'sections' must be a non-empty list")
    for idx, section in enumerate(sections):
        if not isinstance(section, dict):
            raise ValueError(f"section at index {idx} must be an object")
        if not section.get("heading") or not section.get("intent"):
            raise ValueError(f"section at index {idx} must include non-empty heading and intent")

    tags = spec["tags"]
    if not isinstance(tags, list) or not all(isinstance(tag, str) and tag for tag in tags):
        raise ValueError("'tags' must be a list of non-empty strings")


def _extract_prefixed_value(lines: list[str], prefix: str) -> str:
    value = next((line[len(prefix) :].strip() for line in lines if line.startswith(prefix)), "")
    if value:
        return value
    if prefix == "Audience:":
        return "Software engineers"
    if prefix == "Tone:":
        return "Practical"
    return ""


def _extract_tags(title: str, thesis: str) -> list[str]:
    candidates = re.findall(rf"[a-zA-Z]{{{MIN_TAG_LENGTH},}}", f"{title} {thesis}".lower())
    deduped: list[str] = []
    for token in candidates:
        if token not in STOP_WORDS and token not in deduped:
            deduped.append(token)
        if len(deduped) == MAX_TAG_COUNT:
            break
    return deduped or ["writing", "engineering"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a content spec JSON from a markdown idea.")
    parser.add_argument("--input", required=True, type=Path, help="Path to markdown idea file")
    parser.add_argument("--output", required=True, type=Path, help="Path to write generated spec JSON")
    args = parser.parse_args()

    markdown = args.input.read_text(encoding="utf-8")
    spec = generate_spec(markdown, source_id=args.input.stem)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
