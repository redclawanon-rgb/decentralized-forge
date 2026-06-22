# Decentralized Forge Project Context

## Mission

Build a GitHub-class decentralized forge that feels accessible to normal developers while avoiding dependence on any single platform, host, account provider, or censorship chokepoint.

## Eric's intent

Eric wants more than a Nostr experiment. He wants serious research into combining the best available decentralized protocols to recreate GitHub-like functionality in a fully decentralized or censorship-resistant way.

## Operating principles from Eric's X bookmark signal

Recent bookmarks point to these execution patterns:

1. **Scope before build** — turn the big idea into bounded loops and artifacts.
2. **Canonical project brain** — keep markdown docs as the durable source of truth.
3. **Loop engineering** — define repeatable agent loops; do not babysit each step.
4. **Subagents/background threads** — use independent agents for research/build/review work.
5. **Verification stack** — assume agent summaries can be wrong; verify with source links, tests, files, and git state.
6. **Search → Extract → Interact** — search broad, extract known sources, use browser/interactive fallback only when needed.
7. **Harness over prompts** — create the system that runs loops, not one giant prompt.

## Current product thesis

The winning design is likely a protocol-aggregating decentralized forge:

- Git remains the canonical code object model.
- Decentralized/federated protocols handle identity, discovery, issues, PRs, reviews, releases, and replication.
- Multiple substrates are supported behind a normal GitHub-like UX.

## Candidate protocol layers

- Code/versioning: Git
- P2P repo replication: Radicle, libp2p-like approaches
- Federation: ForgeFed / ActivityPub
- Open event layer: Nostr NIP-34/NIP-35
- Durable immutable blobs: IPFS/IPLD/Filecoin/Arweave
- Build/release trust: Sigstore, cosign, in-toto, SLSA
- Optional user data portability: AT Protocol / PDS
- Offline append-only inspiration: Hypercore, Secure Scuttlebutt

## Hard boundaries / gates for the current autonomous loop

Eric's current standing approval for this all-night controller run includes building in public for this project: public GitHub publishing/pushes, public project updates, public accounts/projects, and Nostr/X/GitHub posts are allowed when accurate, non-spammy, and clearly labeled as research/prototype work.

Allowed without additional approval:

- Local files/docs/specs/prototypes in this repo
- Read-only web/X/API research
- Local code prototypes
- Local tests
- Local git commits
- Public GitHub repo pushes for this project after tests/preflight pass
- Public collaboration surfaces and project updates for this project when accurate and prototype-labeled
- Public Nostr relay publishing only with disposable/project-scoped keys and documented storage locations

Requires Eric approval or a separate explicit target:

- Spending money or provisioning paid infrastructure
- Using production/private personal keys for protocol actions
- Contacting specific people outside public project channels
- Making unsupported security/compliance/privacy claims
- Claiming production readiness, censorship-proof guarantees, or live protocol verification that has not actually been tested
## Current loop state

Loops 1–9 are complete. Loop 4 (Radicle local integration spike) is complete as a **source-inspected local artifact**, not a live Radicle CLI run. Loop 5 is complete as **dry-run Nostr collaboration fixtures**, not a live Nostr relay run. Loop 6 is complete as **local/free artifact metadata with a stdlib-verified CIDv1 raw/base32-compatible fixture**, not live IPFS pinning or durable storage. Loop 7 is complete as **synthetic local CI/provenance fixtures**, not real CI execution, signing, Sigstore/cosign/in-toto verification, Rekor upload, or SLSA compliance. Loop 8 is complete as a **local static renderer/UI improvement**, not public CI/status publication or new infrastructure. Loop 9 is complete as a **public GitHub collaboration surface**, with roadmap/docs and bounded public issues.

Public GitHub repo is live at `https://github.com/redclawanon-rgb/decentralized-forge`. Verified public settings: default branch `main`, Issues enabled, Discussions enabled, Wiki disabled. Public building is approved; keep project updates accurate and labeled as research/prototype work.

Loop 4 outputs:

- `docs/radicle-mapping.md`
- `fixtures/radicle-backed-project.registry.json`
- expanded `tests/test_registry_fixture.py`

Loop 5 outputs:

- `fixtures/nostr-collaboration-events.json`
- expanded `docs/nip34-event-shapes.md`
- parser/shape checks in `tests/test_registry_fixture.py`

Loop 6 outputs:

- `fixtures/local-release-artifact.txt`
- `docs/artifact-metadata.md`
- strengthened release artifact metadata in `schemas/project-registry.schema.json`
- updated registry fixtures and stdlib tests for local SHA-256/CID shape plus explicit no-pinning/no-durability flags

Loop 6 caveat: the CID-compatible value is computed locally from fixture bytes and validated by tests, but no IPFS add/fetch/pin, gateway verification, paid storage, wallet, Filecoin/Arweave spend, or durability verification occurred. Do not claim pinned, durable, censorship-proof, replicated, gateway-reachable, or production-ready artifact storage.

Loop 7 outputs:

- `docs/ci-provenance-model.md`
- optional `ci_checks[]` and artifact `provenance` schema fields
- fake local CI check records and fake artifact attestation/provenance metadata in `fixtures/example-project.registry.json`
- explicit Sigstore/SLSA non-claim flags in registry fixtures
- stdlib tests for synthetic-only CI states, coherent artifact hash/commit/repo references, and no real signatures/keys/SLSA claims

Loop 8 outputs:

- improved `scripts/render_project_page.py` static UI with a prototype boundary notice
- clearer rendered sections for release artifact availability, content addresses, provenance/attestation metadata, CI checks, and protocol substrate details
- regenerated `output/demo-project.html`
- renderer tests that assert new non-claim labels and preserve existing basics

Loop 7 caveat: CI/provenance data is synthetic and local-only. No hosted CI job, public commit status, CI secret/token, real signing key, Sigstore/cosign/in-toto verification, Rekor upload, SLSA level/compliance claim, paid CI, or public infrastructure was used. Do not claim signed artifacts, real provenance verification, or production supply-chain trust.

Loop 8 caveat: renderer improvements are static/local and only display fixture fields. They do not create or publish public CI status, verify live IPFS availability, sign artifacts, verify Sigstore/in-toto statements, upload to Rekor, or establish SLSA compliance.

Nostr caveat: no local relay/client tool (`nak`, `nostril`, `strfry`, or `nostr-rs-relay`) was installed or immediately usable, so Loop 5 used dry-run fixtures only. No public relay post, private key, production key, or unsafe installer was used. The synthetic issue (`kind: 1621`) and patch (`kind: 1617`) events have placeholder IDs/signatures and repeated-hex pubkeys.

Radicle caveat: `rad` was unavailable in the environment, and the documented `curl https://radicle.dev/install | sh` installer was not used. The mapping was derived from official source/manpage/examples in `/tmp/radicle-heartwood` at commit `90aaec1c9eee77a0beebece48f460c1424c1c8bd`. Do not claim live Radicle verification until an approved binary/install path is available and a temporary local `RAD_HOME` replay has been run.

Loop 9 outputs:

- `ROADMAP.md`
- `docs/public-collaboration.md`
- bounded public GitHub issues for renderer UX, Nostr fixtures, Radicle verification, artifact state model, and provenance evolution (#1–#5): https://github.com/redclawanon-rgb/decentralized-forge/issues

Loop 9 caveat: public GitHub issues are temporary coordination scaffolding while decentralized collaboration remains fixture-backed. No direct contact with specific people, paid services, production/private keys, live protocol verification claims, or unsupported security/SLSA/production/censorship-proof claims were used.

## Current next recommended loop

**Loop 10: final architecture/roadmap/decision matrix cleanup.** Consolidate architecture, protocol matrix, roadmap, and status docs after the public collaboration setup; ensure all public-facing docs consistently distinguish local fixtures from live-verified protocol support.
