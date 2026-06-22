# Decentralized Forge

A research and prototype project for a GitHub-class decentralized forge.

## One-line thesis

Build a normal-feeling GitHub alternative whose authority is decentralized across Git, cryptographic identity, P2P/federated collaboration protocols, durable artifact storage, and signed build/release attestations.

## Starting question

Can modern decentralized protocols be combined to recreate GitHub's core features without central platform censorship?

## Initial scope

This repo starts as a research/spec/prototype workspace. The first milestone is not a production forge; it is a proof that a project can be:

- announced without GitHub,
- discovered without GitHub,
- cloned from one or more mirrors,
- discussed through decentralized issues,
- proposed against through decentralized patches/PRs,
- released with verifiable signed metadata and optional content-addressed artifacts.

## Docs

- `.hermes/context.md` — durable project brain for agents
- `STATUS.md` — current loop, gates, and next actions
- `RESEARCH.md` — source-grounded protocol research
- `PROTOCOL-MATRIX.md` — protocol fit/maturity comparison
- `SPEC-FIRST.md` — MVP product/specification
- `ARCHITECTURE.md` — proposed architecture
- `AGENT-LOOPS.md` — autonomous loop definitions for overnight work
- `docs/nip34-event-shapes.md` — NIP-34 dry-run event shape notes
- `docs/radicle-mapping.md` — source-inspected Radicle-to-registry mapping, clearly marked not live-CLI verified
- `schemas/project-registry.schema.json` — MVP project registry schema
- `fixtures/example-project.registry.json` — local-only demo project registry fixture
- `fixtures/radicle-backed-project.registry.json` — synthetic local-only Radicle-backed registry fixture
- `scripts/render_project_page.py` — stdlib renderer for static project pages
- `output/demo-project.html` — generated demo project page
- `tests/test_registry_fixture.py` — stdlib verification tests for the registry fixture and renderer

## Local prototype verification

```sh
python3 scripts/render_project_page.py fixtures/example-project.registry.json output/demo-project.html
python3 -m unittest discover -s tests
```

The prototype is local-only: it does not publish to relays, run a public federation actor, spend money, or use private/production keys.

Loop 4's Radicle artifact is also local-only. It was mapped from the official Radicle source tree available at `/tmp/radicle-heartwood` in this run; no Radicle CLI install, `rad init`, network node, public seed, or publish action was performed.
