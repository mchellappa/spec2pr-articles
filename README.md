# Spec2PR — Medium Articles Pipeline

A GitHub-native workflow for writing and publishing Medium articles. GitHub is the source of truth; publishing is automated via the Medium API.

**Idea → Spec → Draft → Review → Publish**

---

## How it works

```
ideas/my-article.md   ← you write the idea (title, audience, tone, key points)
        ↓
  merge to main
        ↓
intake.yml            ← auto-generates specs/my-article.json + drafts/my-article.md skeleton
        ↓
drafts/my-article.md  ← you write the article content in the scaffold
        ↓
  set "publish": true in specs/my-article.json
        ↓
  push to main
        ↓
publish.yml           ← posts to Medium, updates published/tracking.json
```

---

## Quick start

### 1. Add your API key as a GitHub Actions secret

> **Note:** Medium stopped issuing new API integration tokens in 2025.  
> **Dev.to is recommended** — it has a free, open API and a large engineering audience.

Go to **Settings → Secrets and variables → Actions → New repository secret** and add:

**For Dev.to (recommended):**

| Secret | Value |
|---|---|
| `DEVTO_API_KEY` | Your Dev.to API key — get it at [dev.to/settings/extensions](https://dev.to/settings/extensions) under **DEV Community API Keys** |

**For Medium (only if you already have a legacy integration token from before 2025):**

| Secret | Value |
|---|---|
| `MEDIUM_TOKEN` | Your Medium integration token |
| `MEDIUM_USER_ID` | Your Medium user ID — run the command below |

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.medium.com/v1/me
```

### 2. Write an idea

Create a Markdown file in `ideas/`:

```md
# Your Article Title

Audience: Who this is for
Tone: Practical

One paragraph describing the key thesis.

Key points:
- First section topic
- Second section topic
- Third section topic
```

### 3. Open and merge a PR

Push to a branch and open a PR. When merged to `main`:
- `intake.yml` runs automatically
- Generates `specs/your-article.json` (structured spec)
- Generates `drafts/your-article.md` (section skeleton for you to fill in)

### 4. Write your article

Pull the generated draft and fill in each section:

```bash
git pull
# Edit drafts/your-article.md
```

### 5. Publish

When your draft is ready, open `specs/your-article.json` and set:

```json
"publish": true
```

Push to `main`. `publish.yml` will:
- Find specs with `publish: true` not already in `tracking.json`
- POST the draft to Medium (public post)
- Update `published/tracking.json` with the URL

**To create a Medium draft for preview instead of publishing live**, leave `"publish": false` — the workflow will create a draft in your Medium account.

---

## Directory layout

| Path | Purpose |
|---|---|
| `ideas/` | Raw article ideas in Markdown |
| `specs/` | Generated spec JSON (auto-generated from ideas) |
| `drafts/` | Article drafts in Markdown (skeleton auto-generated; you fill in) |
| `published/tracking.json` | Record of published articles with Medium URLs |
| `engine/spec-generator.py` | Converts idea markdown → spec JSON |
| `engine/draft-scaffolder.py` | Converts spec JSON → draft skeleton |
| `engine/publisher.py` | Posts draft to Medium API, updates tracking |
| `templates/` | Editorial style guide and Medium format reference |
| `.github/workflows/intake.yml` | Triggered on idea changes: generates spec + draft |
| `.github/workflows/publish.yml` | Triggered on spec changes: publishes to Medium |

---

## Local usage

Run any engine step locally:

```bash
# Generate spec from idea
python engine/spec-generator.py --input ideas/my-article.md --output specs/my-article.json

# Scaffold draft from spec
python engine/draft-scaffolder.py --spec specs/my-article.json --output drafts/my-article.md

# Publish to Dev.to (recommended)
DEVTO_API_KEY=xxx \
  python engine/publisher.py --spec specs/my-article.json --draft drafts/my-article.md

# Publish to Medium (legacy token holders only)
MEDIUM_TOKEN=xxx MEDIUM_USER_ID=yyy \
  python engine/publisher.py --spec specs/my-article.json --draft drafts/my-article.md --target medium
```

## Manually trigger publish

You can manually trigger the publish workflow from **Actions → Publish to Medium → Run workflow** and optionally specify a single spec file to publish.

---

## Spec schema

```json
{
  "id": "unique-slug",
  "title": "Article title",
  "audience": "Who this is for",
  "tone": "Practical",
  "key_thesis": "One-sentence summary",
  "sections": [
    { "heading": "Section title", "intent": "What to explain" }
  ],
  "tags": ["tag1", "tag2"],
  "publish": false
}
```

Set `"publish": true` when the draft is ready to go live on Medium.

