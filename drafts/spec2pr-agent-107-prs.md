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

> **Key thesis:** An AI agent that acts without analyzing is just a faster way to make mistakes at scale. The missing step between detect and fix is: understand.

## The Setup: 107 Pull Requests Waiting for You on Monday Morning

It started as a reasonable idea.

Our repository had accumulated a backlog of code scanning alerts — the kind that sit in a dashboard for weeks because no single engineer owns them and no sprint ever prioritises them. Security debt. The slow kind.

So we did what teams are starting to do: we assigned an AI agent to fix them.

By the next morning, the agent had done exactly what we asked. It had reviewed every open alert. It had produced a code change for every one. It had opened pull requests — 107 of them — and assigned them to engineers for review and approval.

On paper, this looked like a productivity breakthrough. In practice, it was Monday morning and the team had 107 PRs staring at them before their first coffee.

This is not a story about AI failing. The agent worked. This is a story about what "working" means when an agent acts without reasoning — and what we learned from it.

---

## What the Agent Did Right

Let's be fair, because the agent genuinely did remarkable things.

It processed the entire alert backlog in one session. It correctly identified the vulnerable code patterns flagged by the scanner. It produced syntactically valid fixes for all of them. It created well-structured PRs with descriptions, linked the originating alert, and assigned reviewers.

No human would have done that overnight. No human *could* have done that overnight.

If the goal was "turn alerts into PRs as fast as possible," the agent achieved it perfectly. The throughput was real. The automation was real. The time saved in mechanical triage was real.

That matters. I don't want to dismiss it.

---

## What the Agent Missed: The Analysis Step

Here is what the agent never did: it never asked *why*.

- Why does this alert exist?
- Is this alert a true positive or a false positive?
- What is the intent of the code it is changing?
- Is the proposed fix actually safe in this specific context?
- Are there 20 alerts that share the same root cause — and could be resolved with one change instead of twenty?

The agent treated each alert as an independent mechanical task: alert exists → apply pattern fix → open PR. It was optimising for closure, not for correctness.

In security work, those are very different things.

Some of the fixes were straightforward and clearly right. But others were patches applied to symptoms rather than causes. A few changed behaviour in subtle ways that only someone familiar with the codebase would catch. And a handful were responding to alerts that, on closer inspection, were misconfigured rules that should have been suppressed — not fixed.

The agent had no way to know this. It had not been asked to reason. It had been asked to act.

---

## The Real Cost: Review Burden at Scale

Here is the uncomfortable truth about 107 PRs: they did not eliminate the human work. They redistributed it.

Before the agent, we had a backlog of alerts that engineers occasionally glanced at. After the agent, we had 107 PRs that engineers were *obligated* to review — each one requiring them to:

1. Understand the original alert
2. Read the agent's proposed fix
3. Evaluate whether the fix was correct and safe
4. Approve, reject, or request changes

In many cases this took longer than simply fixing the alert would have. The agent had optimised its own throughput at the cost of the team's review capacity.

This is the hidden math of autonomous agents: **the cost of reviewing an AI's work is not zero**. When an agent acts at scale without reasoning, it can move the bottleneck rather than remove it — and sometimes make it worse by generating volume the team cannot absorb.

107 PRs reviewed over a week by a team that had other priorities is not a productivity win. It is a different kind of backlog.

---

## Let's Talk: Have You Seen This?

This experience made us rethink something we thought we understood: that automation is always an improvement over manual work.

Maybe it is. Maybe the answer is better tooling, better prompts, better pipelines. Maybe this is just a growing pain and we will figure it out.

But I am not sure — and I think that uncertainty is worth sitting with for a moment before we rush to the next solution.

I am genuinely curious whether others have run into this pattern. A few questions I would love to hear your perspective on:

**1. Have you had an AI agent generate more work than it saved?**
Not because it was wrong, but because the volume of its output overwhelmed your review capacity?

**2. How do you validate that an agent's fix is actually correct — not just syntactically valid?**
Do you rely on tests? Code review? A separate validation agent? Something else?

**3. What is your human-AI handoff model for security fixes?**
Should agents always get human sign-off on the approach before they act? Or is that friction that defeats the purpose?

**4. Where is the right boundary between autonomous action and human approval?**
One PR per alert? A summary per batch? A reasoning doc before any code? Nothing at all?

There is no single right answer here. It depends on team size, risk tolerance, codebase complexity, and how much you trust your scanner's signal quality. But I think this conversation is worth having publicly, because most teams are figuring it out in isolation.

Drop your experience in the comments. I want to hear the honest stories — the ones where it worked, and the ones where it didn't.
