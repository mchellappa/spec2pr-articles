<!--
  Draft generated from spec: spec2pr-building-vscode-extension
  Title: Spec2PR: Building a VS Code Extension Powered by GitHub Copilot
  Audience: Developers and platform engineers interested in building AI-powered developer tools
  Tone: Technical and hands-on — architecture decisions, patterns, and lessons learned
  Tags: spec, building, code, extension, powered

  Instructions:
  - Fill in each section below.
  - Keep tone and audience in mind (see above).
  - When ready to publish, set "publish": true in the spec JSON.
-->

![Spec2PR — DevEx AI Assistant](https://raw.githubusercontent.com/mchellappa/devex-workspace/main/images/icon.png)

# Spec2PR: Building a VS Code Extension Powered by GitHub Copilot

> **Key thesis:** Most teams use GitHub Copilot as a coding assistant. We built an entire engineering delivery platform on top of it. This article covers the technical architecture of the DevEx AI Assistant VS Code extension — how it uses the VS Code Language Model API, why we chose GitHub Copilot (Claude) as the underlying model, how the RTCFR-structured prompts are constructed programmatically, and the lessons learned building a production extension used daily by engineering teams.

## VS Code Extension API and Language Model API — what is available and what is not

<!-- Intent: Explain vs code extension api and language model api — what is available and what is not with practical examples. -->


## How to call GitHub Copilot programmatically from a VS Code extension (no extra API keys)

<!-- Intent: Explain how to call github copilot programmatically from a vs code extension (no extra api keys) with practical examples. -->


## Constructing RTCFR-structured prompts in TypeScript for consistent, high-quality output

<!-- Intent: Explain constructing rtcfr-structured prompts in typescript for consistent, high-quality output with practical examples. -->


## Template-driven code generation with Handlebars — why templates beat pure LLM output

<!-- Intent: Explain template-driven code generation with handlebars — why templates beat pure llm output with practical examples. -->


## Lessons learned: streaming responses, error handling, and building reliable AI workflows in production

<!-- Intent: Explain lessons learned: streaming responses, error handling, and building reliable ai workflows in production with practical examples. -->

---

*This article is part of the **Spec2PR** series on Intelligent Software Delivery.*
*[DevEx AI Assistant](https://github.com/mchellappa/devex-workspace) — AI-powered SDLC acceleration for engineering teams.*
