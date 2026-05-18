# Idea: Spec2PR — The Agent That Created 107 PRs (And Why That Was the Problem)

## What I want to write about

A real story. We had code scanning alerts in our repo. We assigned an AI agent to fix them. It worked — technically. It created 107 pull requests for engineers to review and approve.

But it missed one critical step: **analyzing whether the fix was actually the right fix.**

The agent was efficient but not intelligent. It treated every alert as a mechanical patch rather than understanding the root cause. The result was a flood of PRs that overwhelmed engineers and created more review burden than the original problem.

## The core insight

Speed without reasoning is not acceleration — it is noise.

An AI agent that acts without analyzing is just a faster way to make mistakes at scale. The missing ingredient is the deliberate step between "detect" and "fix": **understand**.

## Conversation angles (why this invites discussion)

- Have others seen agents create too many PRs / too many changes without enough context?
- How do you validate that an AI agent's fix is actually correct, not just syntactically valid?
- Should agents always require human approval of the _approach_ before executing?
- What is the right human-AI handoff model for security fixes?

## Target audience

Engineering leaders, DevSecOps practitioners, senior engineers who are evaluating or using AI agents in their CI/CD pipelines.

## Tone

Honest and reflective. Not anti-AI — the goal is to share what we learned so others can do it better. Invite debate and shared experiences.

## Connection to Spec2PR

The Spec2PR philosophy is exactly the antidote: require the agent to produce a **spec** (a reasoned plan with context, analysis, and proposed approach) before it writes any code. The spec IS the "analyze before you act" step that was missing.
