# Spec2PR: Why We Replaced Prompt Engineering with the RTCFR Framework

Audience: Engineering leaders, senior engineers, and platform teams building AI workflows
Tone: Reflective and analytical — lessons learned from real adoption at scale

When we gave engineers access to GitHub Copilot, prompt quality became the bottleneck.
The engineers who wrote the best prompts got the best code. Everyone else got drift.
This article explains why we stopped training engineers to write better prompts and
instead embedded the RTCFR framework — Role, Task, Context, Format, Report — directly
into the DevEx AI Assistant extension, making principal-engineer-level context the
default for every interaction.

Key points:
- Why prompt engineering at scale creates inconsistency, not consistency
- What RTCFR means: Role, Task, Context, Format, Report — and why each element matters
- How RTCFR is embedded into the DevEx extension so engineers never write a raw prompt
- Before and after: what LLD-based RTCFR-structured generation produces vs ad-hoc prompts
- Why encoding engineering frameworks into AI workflows is more durable than training individuals
