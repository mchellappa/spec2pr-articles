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

## Kick off a new article

1. Create a new markdown idea file in `/ideas` (for example: `ideas/spec-first-content-pipeline.md`).
2. Use this minimal structure:

```md
# Your article title

Audience: Who this is for
Tone: Practical

One short paragraph describing the key thesis.

- Section topic one
- Section topic two
```

3. Push the change to a feature branch and open a PR.
4. Merge the PR to `main` to trigger the intake workflow automatically (`.github/workflows/intake.yml`).
5. Optional: run the intake workflow manually from the Actions tab using **Run workflow**.
6. Optional local step: generate a spec before pushing:

```bash
python engine/spec-generator.py --input ideas/spec-first-content-pipeline.md --output specs/spec-first-content-pipeline.json
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
