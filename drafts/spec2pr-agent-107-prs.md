<!--
  Draft generated from spec: spec2pr-agent-107-prs
  Title: The Agent That Created 107 PRs (And Why That Was the Problem)
  Tags: ai, devsecops, softwareengineering, github
-->

# The Agent That Created 107 PRs (And Why That Was the Problem)

One of our leaders has a way of framing AI initiatives that I find genuinely useful. Three buckets: Vibe Coding, Professional AI Assistant, and Autonomous Agents. I won't unpack it further, but if you work in a large engineering org right now, you probably recognise all three.

The push has been toward that third one. And the metrics look good. Story points closed. Alerts resolved. PRs raised. Numbers that are easy to put on a slide for the CIO.

This is a story about what those numbers don't show.

---

## 107 Pull Requests on a Monday Morning

We had a backlog of code scanning alerts. The kind that quietly builds up over months because no sprint ever picks it up and no one owns it. Security debt, sitting in a dashboard.

Someone decided to assign an autonomous agent to clear it.

By Monday morning, the agent had reviewed every alert, produced a fix for every one, and opened 107 pull requests for engineers to review and approve.

On a leadership slide, this is a win. Backlog cleared overnight.

The team saw it differently.

---

## What the Metrics Don't Capture

Someone still had to read those 107 PRs. Not skim them. Actually understand them.

Each one required an engineer to figure out what the original alert was, read what the agent changed, decide whether the fix was correct for this specific codebase, and check whether it introduced new risk.

The agent didn't know the context. It was not asked to reason about it. It was asked to act.

The story points looked great. The review queue told a different story.

---

## The Fix That Wasn't Really a Fix

Here is the part I keep thinking about.

One of the alerts was a Java trust boundary violation in an old codebase. Code from the 1990s that, during build time, pulls in source from another project. The agent saw the violation, could not change the original source, and wrote a Python script to handle it at build time.

Technically, the alert was resolved. The scanner was happy.

But any engineer who has worked on legacy systems knows what that means. You now have a silent dependency. If anyone changes the original code, for any reason, the Python script breaks. There is no warning. There is no test. The fix works until it doesn't, and when it stops working, the person debugging it has no idea why.

Was that the only way to address it? Maybe. This is old code and the constraints were real.

But that is exactly the conversation that should have happened before anyone wrote a single line. Not "here is the fix." Instead, "here is what I found, here is why it's complicated, here is one option and here is what it risks."

The agent skipped that conversation entirely.

---

## Two Different Dashboards

A CIO sees 107 security issues resolved by an autonomous agent overnight. That is a real number and genuinely impressive work.

A Principal Engineer sees 107 changes that need to be validated before trusting any of them, plus at least one fix that trades a known vulnerability for an invisible fragility.

Neither view is wrong. They are measuring different things.

The CIO is measuring output. The Principal Engineer is measuring trust. The cost of validating an agent's work at scale does not show up in story points. And when leadership optimises for the number without understanding what the number measures, the gap between those two dashboards gets wider.

---

## What I Actually Want to Know

I don't have a tidy answer here. I am not sure anyone does yet.

But I am curious whether others have seen this same dynamic, where the metrics say one thing and the engineers feel something different.

A few honest questions:

Have your AI agent metrics told a different story than what your engineers experienced on the ground?

How do you measure the review burden an agent creates, not just the output it produces?

Is your organisation pushing toward autonomous agents right now, and if so, what does human oversight look like in practice?

And when an agent finds something genuinely complex, something with history and context and tradeoffs, what should it do? Act, and let a human review it? Or stop and ask first?

I want to hear the real stories in the comments. The ones that didn't make it onto the slide.
