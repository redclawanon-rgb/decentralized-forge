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

This repository is a **local registry/static renderer prototype** with protocol-mapping fixtures. It is public for collaboration, but the decentralized protocol integrations are not live-verified yet.

| Area | Current state | Not claimed |
|---|---|---|
| Registry/UI | Local JSON schema, fixtures, stdlib renderer, generated demo HTML | Production forge, hosted service, signed authority |
| Nostr NIP-34 | Dry-run repository/issue/patch/state fixtures plus local stdlib parser round-trip tests, NIP-01 shape/conformance reports, and rendered fixture-adapter/conformance summary sections | Relay publishing/readback, real keys, valid signatures, fixture ID replacement, live relay verification, public CI/status events |
| Radicle | Source-inspected mapping and synthetic fixture | Live `rad` CLI verification, real RID, public seed publish |
| Artifacts | Local SHA-256 and CIDv1 raw/base32-compatible metadata | IPFS availability, pinning, Filecoin/Arweave durability |
| CI/provenance | Synthetic local CI/provenance display fields | Hosted CI, real signing, Sigstore/in-toto verification, Rekor upload, SLSA compliance |
| Verification labels | Top-level `verification_states[]` records identify local fixtures, source-inspected mappings, synthetic fixtures, live-unverified scopes, and future live-verified evidence | Implicit live verification, production trust, censorship-proof/durability/security guarantees |
| Public collaboration | GitHub issues/discussions for temporary coordination | Decentralized issue/patch federation running in production |

## Docs

- `.hermes/context.md` — durable project brain for agents
- `STATUS.md` — current loop, gates, and next actions
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
- `ROADMAP.md` — public prototype roadmap, verification-state labels, and collaboration tracks
- `schemas/project-registry.schema.json` — MVP project registry schema
- `fixtures/example-project.registry.json` — local-only demo project registry fixture
- `fixtures/local-release-artifact.txt` — local-only release artifact fixture with stdlib-tested SHA-256/CIDv1 metadata
- `fixtures/nostr-repo-state-status.json` — local-only `kind: 30618` repository state fixture generated from the recorded local Git HEAD at fixture creation time plus fixture-only synthetic status/check projections
- `fixtures/radicle-backed-project.registry.json` — synthetic local-only Radicle-backed registry fixture
- `scripts/nip34_adapter.py` — stdlib parser/export helper that round-trips dry-run NIP-34 repository, issue, patch, repository state, fixture-only status/check data, and local NIP-01 conformance metadata back to registry-shaped concepts without relay publishing
- `scripts/render_project_page.py` — stdlib renderer for static project pages, including verification-state labels, artifact availability, content-address, CI/provenance, substrate detail sections, and optional local NIP-34 fixture adapter import/display
- `output/demo-project.html` — generated demo project page
- `tests/test_registry_fixture.py` — stdlib verification tests for the registry fixture and renderer

## Local prototype verification

```sh
python3 scripts/render_project_page.py fixtures/example-project.registry.json output/demo-project.html \
  --nip34-repo-fixture fixtures/nostr-repo-announcement.json \
  --nip34-collaboration-fixture fixtures/nostr-collaboration-events.json \
  --nip34-state-status-fixture fixtures/nostr-repo-state-status.json
python3 -m unittest discover -s tests
```

The prototype is local-only: it does not publish to relays, run a public federation actor, spend money, or use private/production keys. Top-level `verification_states[]` records now make each scope's evidence and claim boundary explicit; current protocol scopes are local fixtures, source-inspected mappings, synthetic fixtures, or live-unverified, not live-verified. The NIP-34 adapter only parses local dry-run fixtures and preserves placeholder IDs/signatures plus `published: false` non-claim fields; its conformance reports compute possible NIP-01 reference event IDs only as local metadata and do not replace fixture IDs, sign, or publish. The renderer displays verification labels plus a concise Loop 15 conformance summary (report counts, known NIP-34 kind counts, placeholder flags, signed/published false, and possible-event-ID local references) without dumping full serialized event payloads by default. The renderer can display imported fixture output, including the `kind: 30618` repository state fixture generated from recorded local Git commit `32f88a7a42498328a515e4763e28d84216420a98` at fixture creation time and fixture-only status/check projections. Later commits may make that recorded fixture commit an ancestor of current `HEAD`; tests account for that. The renderer does not sign, connect to relays, fetch relay state, publish events, create public CI/status events, or verify relay read/write compatibility. Release artifact metadata can carry local hashes and CID-compatible identifiers, but Loop 6 did not pin, upload, fetch from IPFS, use wallets, spend on Filecoin/Arweave, or make durability claims. CI/provenance fields and renderer sections are synthetic/local fixture displays only; they do not claim real hosted CI, public commit status, artifact signing, Sigstore/cosign/in-toto verification, Rekor upload, SLSA compliance, or production supply-chain trust.

Loop 4's Radicle artifact is also local-only. It was mapped from the official Radicle source tree available at `/tmp/radicle-heartwood` in this run; no Radicle CLI install, `rad init`, network node, public seed, or publish action was performed.
