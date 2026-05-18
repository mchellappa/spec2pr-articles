# Spec2PR: Building a VS Code Extension Powered by GitHub Copilot

Audience: Developers and platform engineers interested in building AI-powered developer tools
Tone: Technical and hands-on — architecture decisions, patterns, and lessons learned

Most teams use GitHub Copilot as a coding assistant. We built an entire engineering
delivery platform on top of it. This article covers the technical architecture of the
DevEx AI Assistant VS Code extension — how it uses the VS Code Language Model API,
why we chose GitHub Copilot (Claude) as the underlying model, how the RTCFR-structured
prompts are constructed programmatically, and the lessons learned building a production
extension used daily by engineering teams.

Key points:
- VS Code Extension API and Language Model API — what is available and what is not
- How to call GitHub Copilot programmatically from a VS Code extension (no extra API keys)
- Constructing RTCFR-structured prompts in TypeScript for consistent, high-quality output
- Template-driven code generation with Handlebars — why templates beat pure LLM output
- Lessons learned: streaming responses, error handling, and building reliable AI workflows in production
