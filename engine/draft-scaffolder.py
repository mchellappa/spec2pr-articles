"""draft-scaffolder.py

Reads a spec JSON file and writes a Markdown draft skeleton to the drafts/ folder.
The skeleton contains all section headings from the spec so the author can fill in content.

Usage:
    python engine/draft-scaffolder.py --spec specs/my-article.json --output drafts/my-article.md
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


LOGO_URL = "https://raw.githubusercontent.com/mchellappa/devex-workspace/main/images/icon.png"

DRAFT_HEADER = """\
<!--
  Draft generated from spec: {spec_id}
  Title: {title}
  Audience: {audience}
  Tone: {tone}
  Tags: {tags}

  Instructions:
  - Fill in each section below.
  - Keep tone and audience in mind (see above).
  - When ready to publish, set "publish": true in the spec JSON.
-->

![Spec2PR — DevEx AI Assistant]({logo_url})

# {title}

> **Key thesis:** {key_thesis}

"""

SECTION_TEMPLATE = """\
## {heading}

<!-- Intent: {intent} -->

"""

DRAFT_FOOTER = """\
---

*This article is part of the **Spec2PR** series on Intelligent Software Delivery.*
*[DevEx AI Assistant](https://github.com/mchellappa/devex-workspace) — AI-powered SDLC acceleration for engineering teams.*
"""


def scaffold_draft(spec: dict) -> str:
    header = DRAFT_HEADER.format(
        spec_id=spec.get("id", ""),
        title=spec.get("title", "Untitled"),
        audience=spec.get("audience", ""),
        tone=spec.get("tone", ""),
        tags=", ".join(spec.get("tags", [])),
        key_thesis=spec.get("key_thesis", ""),
        logo_url=LOGO_URL,
    )

    sections = "\n".join(
        SECTION_TEMPLATE.format(
            heading=s.get("heading", "Section"),
            intent=s.get("intent", ""),
        )
        for s in spec.get("sections", [])
    )

    return header + sections + DRAFT_FOOTER


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a Markdown draft from a spec JSON.")
    parser.add_argument("--spec", required=True, type=Path, help="Path to spec JSON file")
    parser.add_argument("--output", required=True, type=Path, help="Path to write draft Markdown")
    args = parser.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    draft = scaffold_draft(spec)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(draft, encoding="utf-8")
    print(f"Draft scaffold written to {args.output}")


if __name__ == "__main__":
    main()
