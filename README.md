# Spec2PR Content Pipeline

Spec2PR Content Pipeline is a GitHub-native content orchestration system that treats content delivery like software delivery:

**Idea -> Spec -> Draft -> Validation -> PR -> Publish**

This repository is currently in the first incremental implementation step.

## Current Scope

- Repository skeleton for pipeline stages and artifacts
- Initial `engine/spec-generator.py` module
- Example idea input in `/ideas`
- Intake workflow at `.github/workflows/intake.yml`

## Directory Layout

- `/ideas` - Raw content ideas in Markdown
- `/specs` - Generated content specification JSON files
- `/drafts` - Generated article drafts
- `/published` - Publishing state and metadata (`tracking.json`)
- `/engine` - Pipeline stage modules
- `/templates` - Editorial and Medium formatting templates
- `/.github/workflows` - GitHub Actions orchestration

## Spec Generator

Generate a content spec from an idea markdown file:

```bash
python engine/spec-generator.py --input ideas/example-idea.md --output specs/example-idea.json
```

The generated spec follows this schema:

```json
{
  "id": "unique-slug",
  "title": "",
  "audience": "",
  "tone": "",
  "key_thesis": "",
  "sections": [
    {
      "heading": "",
      "intent": ""
    }
  ],
  "tags": [],
  "publish": false
}
```

## Environment

Copy `.env.example` and set values for later publishing stages.
