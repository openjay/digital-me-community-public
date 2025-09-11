# Enhanced Development Plan

## Phase A — Community SDK Maturation (2–4 weeks)
- AgentBuilder + Lifecycle hooks (pre_start/post_stop)
- Provider adapters (OpenAI, local, Anthropic) behind common interface
- Typed plugin config models (pydantic v2)

## Phase B — Examples & Documentation (2–3 weeks)
- hello_world (done), text_tools, finance_tools (calculator), web_tools
- Sphinx docs + mkdocs for site publishing
- Tutorials: build, test, secure, containerize

## Phase C — Security & Ops (continuous)
- CodeQL, Trivy, Gitleaks (enforced in PR)
- Coverage ≥ 90% gate on `main`
- Reproducible builds, SBOM export

## Phase D — Community Launch (1–2 weeks)
- PyPI pre-release
- Issues labeled `good first issue`
- Biweekly community call notes + roadmap board

## Success Metrics
- ≥ 15 example PRs merged from external contributors
- CI green > 99% over rolling 30 days
- ≥ 90% test coverage; zero critical vulns