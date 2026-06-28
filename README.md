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
- released with structured metadata, artifact hashes, and eventual signed attestations once verified.

## Current status

This repository is a **local registry/static renderer prototype** with protocol-mapping fixtures and narrow, evidence-backed live checks. It is public for collaboration, but it is not a production forge and does not claim durable storage, broad protocol availability, censorship resistance, security guarantees, or production readiness.

As of Loop 35, the project has local CAR/CID fixture verification, one selected-relay Nostr repository-announcement readback import, one disposable Radicle local/private replay, and one disposable public Radicle seed/remote-clone smoke. Those checks are deliberately scoped to the exact evidence files in this repo.

| Area | Current state | Not claimed |
|---|---|---|
| Registry/UI | Local JSON schema, fixtures, stdlib renderer, generated demo HTML | Production forge, hosted service, signed authority |
| Nostr NIP-34 | Dry-run repository/issue/patch/state fixtures, local stdlib parser/conformance checks, and one imported Loop 25 selected-relay repository-announcement readback event using a disposable project key | Durability, global propagation, identity trust, issue/patch readback, full NIP-34/forge compatibility |
| Radicle | Source-inspected mapping, disposable local/private CLI replay evidence, and one disposable public seed/remote-clone smoke for exact RID `rad:z2WtozFrCRhygh9CGzyUN57CN7Nwa` | Persistent seed operation, broad Radicle network availability, durability, identity trust, production readiness |
| Artifacts | Local SHA-256, CIDv1 raw/base32-compatible metadata, and lockfile-backed local CAR/CID readback evidence | IPFS daemon add/fetch, public gateway availability, pinning, Filecoin/Arweave durability |
| CI/provenance | Synthetic local CI/provenance display fields | Hosted CI, real signing, Sigstore/in-toto verification, Rekor upload, SLSA compliance |
| Verification labels | Top-level and NIP-34 adapter `verification_states[]` records identify local fixtures, source-inspected mappings, synthetic fixtures, live-unverified scopes, and narrow live-verified evidence, with rendered counts and claim-boundary summaries | Implicit trust, unsupported scope expansion, censorship-proof/durability/security guarantees |
| Live replay gates | Safe replay checklist advanced through Loop 35; further live storage, broader Radicle checks, public updates, or stronger claims require a new explicit target/approval | Unbounded live testing, paid services, production/private personal keys |
| Public collaboration | GitHub issues/discussions for temporary coordination | Decentralized issue/patch federation running in production |

## Docs

- `.hermes/context.md` — durable project brain for agents
- `STATUS.md` — current loop, gates, and next actions
- `COMPLETION-CRITERIA.md` — Milestone 1 definition of done, verification commands, and gated completion lanes
- `RESEARCH.md` — source-grounded protocol research
- `PROTOCOL-MATRIX.md` — protocol fit/maturity comparison plus next-step decision matrix
- `SPEC-FIRST.md` — MVP product/specification
- `ARCHITECTURE.md` — proposed architecture, verification-state boundaries, and implementation decision matrix
- `AGENT-LOOPS.md` — autonomous loop definitions for overnight work
- `docs/nip34-event-shapes.md` — NIP-34 dry-run event shape notes
- `docs/radicle-mapping.md` — source-inspected Radicle-to-registry mapping, clearly marked not live-CLI verified
- `docs/artifact-metadata.md` — Loop 6 release artifact metadata, local CID fixture, and no-pinning/no-durability boundaries
- `docs/ci-provenance-model.md` — Loop 7 synthetic local CI/provenance model and no-Sigstore/no-SLSA-claim boundaries
- `docs/public-collaboration.md` — Loop 9 public collaboration stance, first issue set, and public update draft
- `docs/live-adapter-replay-plan.md` — Loop 20 safe live-gated Radicle/Nostr replay prerequisites, evidence checklist, rollback, and non-claim gates
- `docs/live-completion-gates.md` — optional post-Milestone-1 live IPFS, Nostr, Radicle, and signing gates
- `ROADMAP.md` — public prototype roadmap, verification-state labels, and collaboration tracks
- `schemas/project-registry.schema.json` — MVP project registry schema
- `fixtures/example-project.registry.json` — local-only demo project registry fixture
- `fixtures/portable-lab.registry.json` — second local-only registry fixture for non-demo CLI/export coverage
- `fixtures/live-adapter-replay-checklist.json` — secret-free replay gate/checklist state advanced through Loop 35
- `fixtures/live-evidence-index.json` — secret-free index of Radicle local CLI replay evidence, Nostr selected-relay readback evidence, and explicit non-claims
- `fixtures/local-release-artifact.txt` — local-only release artifact fixture with stdlib-tested SHA-256/CIDv1 metadata
- `fixtures/nostr-repo-state-status.json` — local-only `kind: 30618` repository state fixture generated from the recorded local Git HEAD at fixture creation time plus fixture-only synthetic status/check projections
- `fixtures/radicle-backed-project.registry.json` — synthetic local-only Radicle-backed registry fixture
- `scripts/nip34_adapter.py` — stdlib parser/export helper that round-trips dry-run NIP-34 repository, issue, patch, repository state, fixture-only status/check data, and local NIP-01 conformance metadata back to registry-shaped concepts without relay publishing
- `scripts/render_project_page.py` — stdlib renderer for static project pages, including verification-state labels, artifact availability, content-address, CI/provenance, substrate detail sections, optional local NIP-34 fixture adapter import/display, and optional live-evidence index display
- `scripts/preflight_static_artifact.py` — stdlib preflight for generated static artifact freshness, expected local/synthetic boundary sections, optional NIP-34 fixture sections, optional live evidence index, and selected unsupported claim phrases
- `output/demo-project.html` — generated demo project page
- `output/portable-lab.html` — generated second-fixture project page
- `output/*.summary.json` — deterministic machine-readable registry summaries
- `tests/test_registry_fixture.py` — stdlib verification tests for the registry fixture and renderer

## Local prototype usage and verification

Regenerate the public demo artifact with every local fixture section enabled:

```sh
python3 scripts/render_project_page.py fixtures/example-project.registry.json output/demo-project.html \
  --nip34-repo-fixture fixtures/nostr-repo-announcement.json \
  --nip34-collaboration-fixture fixtures/nostr-collaboration-events.json \
  --nip34-state-status-fixture fixtures/nostr-repo-state-status.json \
  --live-evidence-index fixtures/live-evidence-index.json
```

Open the generated artifact locally in a browser:

```sh
python3 -m webbrowser output/demo-project.html
```

Run the static artifact preflight before release-oriented edits, screenshots, pushes, or public updates:

```sh
python3 scripts/preflight_static_artifact.py
```

The preflight is stdlib-only. It checks that `output/demo-project.html` exists, is byte-for-byte current with the renderer plus all optional NIP-34 fixtures and the Loop 26 live evidence index, includes expected local/synthetic/non-claim sections, includes the optional NIP-34 fixture adapter/state/status/conformance sections, includes the live evidence index section, and omits selected unsupported live-protocol/security/durability claim phrases.

Run the full local verification suite:

```sh
python3 -m json.tool schemas/project-registry.schema.json
python3 -m json.tool fixtures/example-project.registry.json
python3 -m json.tool fixtures/portable-lab.registry.json
python3 -m json.tool fixtures/radicle-backed-project.registry.json
python3 -m json.tool fixtures/nostr-repo-announcement.json
python3 -m json.tool fixtures/nostr-collaboration-events.json
python3 -m json.tool fixtures/nostr-repo-state-status.json
python3 -m json.tool fixtures/live-adapter-replay-checklist.json
python3 -m json.tool fixtures/live-evidence-index.json
python3 scripts/nip34_adapter.py fixtures/nostr-repo-announcement.json fixtures/nostr-collaboration-events.json fixtures/nostr-repo-state-status.json
python3 scripts/preflight_static_artifact.py
python3 scripts/forge_registry.py validate fixtures/example-project.registry.json fixtures/portable-lab.registry.json
python3 scripts/forge_registry.py render fixtures/portable-lab.registry.json output/portable-lab.html
python3 scripts/forge_registry.py export-summary fixtures/example-project.registry.json output/demo-project.summary.json
python3 scripts/forge_registry.py export-summary fixtures/portable-lab.registry.json output/portable-lab.summary.json
python3 scripts/live_gate_inventory.py
python3 -m unittest discover -s tests
npm run verify:car-cid
```

The prototype is evidence-scoped: it does not run a public federation actor, spend money, use production/private personal keys, or claim production readiness. Top-level `verification_states[]` records make each scope's evidence and claim boundary explicit. CI/provenance fields and renderer sections remain synthetic/local display data unless separately verified. The NIP-34 adapter parses local dry-run fixtures and separately imports the already-recorded selected-relay readback event; it does not publish new relay events during rendering or tests. Release artifact metadata includes local hashes, CID-compatible identifiers, and a local CAR/CID readback fixture, but it is not pinned, uploaded, fetched from IPFS, wallet-backed, paid-storage-backed, or durable-storage verified.

The renderer summarizes both registry-level and adapter-level verification rows: total row counts, live-verified false/true counts, synthetic false/true counts, state chips, grouped rows by state, and claim-boundary summaries. It also displays a concise conformance summary without dumping full serialized event payloads by default. Further live storage, broader/repeated Radicle public-network testing, public updates about Loop 33/34 results, or stronger durability/censorship/security/production claims require a new explicit approval/target.
