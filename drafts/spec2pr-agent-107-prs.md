<!--
  Draft generated from spec: spec2pr-agent-107-prs
  Title: The Agent That Created 107 PRs (And Why That Was the Problem)
  Audience: Engineering leaders, DevSecOps practitioners, and senior engineers evaluating AI agents in CI/CD pipelines
  Tone: Honest and reflective — a real story told without spin, inviting debate and shared experience
  Tags: ai, devsecops, softwareengineering, github

  Instructions:
  - Fill in each section below.
  - Keep tone and audience in mind (see above).
  - When ready to publish, set "publish": true in the spec JSON.
  - Cover image (logo) is set automatically by publisher.py via the cover_image API field.
-->

# The Agent That Created 107 PRs (And Why That Was the Problem)

At my organisation, our leadership classifies AI initiatives into three buckets.

**Vibe Coding** — developers using AI to move faster, autocomplete code, explore ideas. Low structure, high energy, individual productivity gains.

**Professional AI Assistant** — AI embedded into structured workflows. Thinks before it acts. Works alongside an engineer who stays in the loop.

**Autonomous Agents** — AI that takes a task end-to-end with minimal human involvement. Acts, decides, commits, raises PRs. Leadership loves this one.

The push lately has been toward that third bucket. And I get it. The metrics are compelling. Story points closed. Alerts resolved. PRs raised. Numbers that look excellent on a CIO dashboard.

This is a story about what those numbers don't show.

---

## 107 Pull Requests, One Monday Morning

We had a backlog of code scanning alerts. The kind that accumulates quietly over months because no sprint ever prioritises it and no single engineer owns it. Security debt, sitting in a dashboard.

Someone — reasonably — decided to assign an autonomous agent to clear the backlog.

By Monday morning, the agent had done exactly what it was asked. It had reviewed every alert. Produced a code change for every one. Opened 107 pull requests and assigned them to engineers for review.

On a leadership slide, this looks like a win. Backlog cleared overnight. Agent productivity: 107 story points. Engineers can just click approve.

The team's reaction was a little different.

---

## What the Metrics Miss

Here is the thing about 107 PRs: someone still has to read them.

Not just skim them. Actually understand them. Because each PR needed an engineer to:

- Understand the original alert
- Read what the agent changed and why
- Decide whether the fix was actually correct — not just syntactically valid, but semantically right for *this* codebase
- Check whether the fix introduced new risk
- Catch the ones responding to misconfigured rules that should have been suppressed, not patched

Some of the fixes were fine. Straightforward, safe, clearly right. But others patched symptoms rather than causes. A few changed behaviour in subtle ways that only someone familiar with the codebase would notice. And several were technically valid but not the *right* approach for our context.

The agent didn't know any of this. It wasn't asked to reason. It was asked to act.

The story points looked great. The review queue told a different story.

---

## The Gap Between the Dashboard and the Codebase

This is the tension I keep coming back to.

A CIO looking at AI adoption metrics sees: 107 security issues resolved by an autonomous agent. That is a real number. The agent really did produce 107 changes. That is genuinely impressive.

A Principal Engineer looking at the team sees: 107 changes that need to be validated before we can trust any of them, arriving all at once, on top of everything else the team is already carrying.

Neither view is wrong. They are measuring different things.

The CIO is measuring output. The Principal Engineer is measuring trust. And the cost of establishing trust in an agent's work — at scale, without prior context — is not zero. It does not show up in the story points.

I am not saying autonomous agents are a mistake. I am saying the metrics we are using to evaluate them might be incomplete. And when leadership optimises for the metric without understanding what it measures, the gap gets wider.

---

## What I Actually Want to Know

I don't have a clean answer here. I am not sure anyone does yet.

But I am genuinely curious whether others have seen this same dynamic play out — the enthusiasm at the top, the quiet friction at the bottom, and the metrics that don't quite capture what is really happening.

A few questions I would love to hear your honest perspective on:

**Have your AI agent metrics told a different story than your engineers' actual experience?**

**How do you measure the review burden an agent creates, not just the output it produces?**

**Is your organisation in the same rush toward autonomous agents — and if so, what guardrails, if any, are in place?**

**Where do you think the right boundary is between an agent that acts and a human who decides?**

Drop your experience in the comments. The honest stories — the ones that didn't make it onto the leadership slide — are the ones I want to read.
