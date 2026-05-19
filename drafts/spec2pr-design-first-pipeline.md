<!--
  Draft: spec2pr-design-first-pipeline
  Title: Spec2PR: The Design-First Pipeline
  Tags: springboot, ai, softwareengineering, architecture
-->

# Spec2PR: The Design-First Pipeline

I joined this project last year. The teams I had worked with before were more agile, so this process-driven environment was actually refreshing. Development does not begin until the LLD is approved. I liked that.

But the more LARB reviews I attended, the more I noticed a pattern. The documents kept coming in incomplete. I would have to challenge the presenter on basic error handling questions every single time. The same security architect kept asking the same security questions in every review. And the architects presenting the next LLD had still not incorporated those comments.

I don't fully blame the presenters. Business teams often don't share the unhappy path. But as an architect, my job is to build a fool-proof design and that means those gaps have to be caught somewhere.

---

## Adding AI to the Review Process

Around the same time, I was already building a VS Code extension to explore how AI could improve developer productivity. I had added a command for code reviews and thought, why not add LLD review too?

The idea was simple. The tool reads the LLD document and checks it against a checklist: error handling scenarios, security requirements, data classification, alerting and notifications. These were exactly the questions that kept coming up in every LARB session. It gives the document a percentage score for development readiness and lists what is missing.

The architecture team's reaction was positive. They acknowledged the gaps the tool surfaced and appreciated how thorough it was. But more importantly, those conversations could now happen before the formal review, not during it.

---

## Giving Architects a Head Start

As the project grew, leadership had limited visibility into what was happening across squads. With multiple teams running in parallel, the handshake points between business, architecture, and engineering were hard to track. Jira was already the source of truth for the project, so I had to build Jira integration anyway for the code development workflow.

Once that pipeline was in place, I added two more commands. Summarize Jira reads the story and gives the architect a concise picture of what the business is asking for. Generate LLD takes that further. It prompts the architect with specific questions, builds a full document across 10 sections, and covers all the NFRs including error handling, security, data classification, and alerting. The architect still has to review it and fill in company-specific details and standards. But the structure is there, the questions are answered, and the document is ready to take into a review.

---

## From Approved LLD to Closed Story

Once the LLD is approved, the next command is Generate Jira Story from LLD. It reads the approved design, asks clarifying questions, generates an OpenAPI spec for any RESTful API stories, and creates the development stories in Jira. Not just one story. It breaks the work down into a development story, a database migration story, and any other stories needed. Each one has enough detail for an engineer to actually start work.

From there the developer takes over. They run Implement Jira Story and pick the story they are working on. The tool asks a few clarifying questions: which programming language, which LLD, which OpenAPI spec to use. These choices are already available from the earlier steps in the pipeline, so it is not starting from scratch. Once confirmed, it generates the code, creates the GitHub branch named after the Jira story, commits the changes with full context, and updates the Jira story with the right comments automatically.

When the developer is satisfied the code is working, one more command submits the PR and closes the Jira story. The whole thread from approved LLD to closed story is traceable.

---

## Guardrails: Making AI Consistent

Early on I ran into a problem with code generation. One run would produce a Maven project. The next run would produce a Gradle project. Spring Boot versions were inconsistent across generated services. The AI was making its own choices every time, and there was no guarantee two developers on the same project were getting the same foundation.

The fix was a templates folder. It contains sample Spring Boot and .NET projects with the correct version dependencies, the database frameworks the project uses, and the security principles to follow. When the extension builds the prompt for code generation, it pulls from these templates. The AI is no longer making those choices. They are already made. Every generated service comes out on the same stack, with the same versions, following the same standards.

For a principal engineer who is accountable for what goes into production, that consistency matters. You are not reviewing each PR wondering what decisions the AI made this time. You already know.

---

## What This Makes Possible

I did not build this to replace engineers or architects. I built it because the gap between a business requirement and a production-ready service is full of manual steps that slow everyone down and introduce inconsistency at every handoff.

What I want people to take away from this is not the tool itself. It is the idea that AI can do more than generate code. When you set the right guardrails, give it the right context, and connect it to the right systems, it can carry the thread across the entire delivery lifecycle. And the principal engineer who is accountable for the output can feel confident because the standards were baked in from the start, not reviewed in at the end.

---

*This article is part of the **Spec2PR** series on Intelligent Software Delivery.*
*[DevEx AI Assistant](https://github.com/mchellappa/devex-workspace) — AI-powered SDLC acceleration for engineering teams.*
