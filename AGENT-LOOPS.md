# Agent Loops

This file turns the broad mission into bounded, verifiable loops.

## Loop design rules

Inspired by Eric's X bookmark signal around loop engineering, subagents, scoping, and verification:

1. Every loop has a named deliverable.
2. Every loop has gates and stop conditions.
3. Every loop writes/updates docs before moving on.
4. Every subagent result is parent-verified with files, source links, tests, or git state.
5. A loop can continue overnight if it is bounded, reversible, or covered by the standing public-build approval.
6. Public actions are allowed for this project when accurate, non-spammy, prototype-labeled, and not dependent on paid infrastructure or production/private keys.

## Loop 1: Research corpus and protocol matrix

**Goal:** Build the source-grounded knowledge base.

**Tasks:**

- Research Radicle current architecture and collaboration model.
- Research ForgeFed/ActivityPub forge federation status.
- Research Nostr NIP-34/NIP-35 and tools like n34/ngit.
- Research IPFS/IPLD/Filecoin/Arweave for repo snapshots and artifacts.
- Research Sigstore/cosign/in-toto/SLSA for signed CI/release trust.
- Research AT Protocol/PDS, Hypercore, and SSB as optional inspiration.
- Fill `PROTOCOL-MATRIX.md`.
- Write recommendation in `ARCHITECTURE.md`.

**Stop conditions:**

- Source access fails for a critical protocol.
- Findings show the core thesis is infeasible.
- Tool/time cap reached.

## Loop 2: MVP registry object and static repo page prototype

**Goal:** Prove a decentralized project identity can be represented and rendered.

**Tasks:**

- Create `schemas/project-registry.schema.json`.
- Create `fixtures/example-project.registry.json`.
- Create a local renderer script or static page.
- Validate the schema with a local test.

**Stop conditions:**

- No schema validator available and dependency install fails.
- Loop 1 recommends a different canonical object model.

## Loop 3: NIP-34 read/write spike

**Goal:** Test decentralized repo announcement mechanics locally/safely.

**Tasks:**

- Use test keys only.
- Use local/dev relay if available, otherwise prepare a dry-run payload.
- Create repo announcement event shape.
- Read/parse announcement back if local relay exists.

**Gate:**

Public relay publishing is now approved for this project only with disposable/project-scoped keys, documented storage locations, and prototype labeling. Use only test keys for local/dev relay or dry-run fixtures; never use production/private personal keys.

## Loop 4: Radicle local integration spike

**Goal:** Map Radicle's repository identity, delegates, issues, and patches into the local registry model without publishing.

**Tasks:**

- Install or locate Radicle tooling only through an approved safe path; do not run curl-pipe-shell installers.
- If the CLI is unavailable, inspect official source/manpage/examples and mark outputs as source-inspected rather than live-tested.
- Write `docs/radicle-mapping.md` mapping Radicle fields to `project-registry.schema.json`.
- Add a synthetic Radicle-backed registry fixture with fake public IDs only.
- Validate fixture JSON and run unit tests.

**Gate:**

No public seed publishing unless it is an accurate prototype-labeled project update covered by the public-build approval. No production/private keys, unsafe installs, contacting specific people outside public channels, or spending without explicit approval.

**Current result:**

Completed as a source-inspected local spike because `rad` was unavailable and the documented `curl https://radicle.dev/install | sh` path was not approved. Outputs are `docs/radicle-mapping.md`, `fixtures/radicle-backed-project.registry.json`, and expanded registry tests.

## Loop 5: Nostr local/dev relay or stronger dry-run collaboration fixtures

**Goal:** Demonstrate repository issue/patch announcement mechanics without using public relays.

**Tasks:**

- Prefer a free/safe local relay if available; publish only synthetic test-key events and read them back locally.
- If no local relay is feasible, expand NIP-34/NIP-35 dry-run fixtures for issue and patch collaboration events.
- Add parser/validation tests that prove the local registry can ingest or preserve the event shapes.
- Update `STATUS.md`, `.hermes/context.md`, and docs with verification evidence.

**Gate:**

Public relay publishing is allowed only with disposable/project-scoped keys and documented storage; otherwise keep dry-run fixtures and use GitHub issues/discussions as the public collaboration surface first. No production/private keys, unsupported public claims, paid services, or contacting specific people outside public channels.

## Loop 6: release/artifact metadata and local CID-compatible fixture

**Current result:**

Completed as local/free artifact metadata. Outputs include `fixtures/local-release-artifact.txt`, strengthened artifact metadata in the schema/fixtures, `docs/artifact-metadata.md`, and tests for SHA-256/CIDv1-compatible local fixture metadata. No live IPFS add/fetch/pin, paid storage, wallet, Filecoin/Arweave spend, or durability claim was performed.

## Loop 7: CI/provenance model docs and local fake attestation fixtures

**Current result:**

Completed as synthetic local CI/provenance fixtures. Outputs include `docs/ci-provenance-model.md`, optional `ci_checks[]` and artifact `provenance` schema fields, fake local CI records, fake artifact attestation/provenance metadata, and tests for no real signatures/keys/SLSA claims. No hosted CI, public status, signing, Sigstore/cosign/in-toto verification, Rekor upload, or SLSA compliance claim was performed.

## Loop 8: static UI/renderer improvements

**Current result:**

Completed as local static renderer/UI work. `scripts/render_project_page.py` now displays a prototype boundary notice plus clear sections for artifact availability, content addresses, provenance/attestation metadata, CI checks, and protocol substrate details. `output/demo-project.html` was regenerated and renderer tests assert the new non-claim labels. No public status publication, hosted service, paid infrastructure, production key, or unsupported security/SLSA claim was introduced.

## Loop 9: public collaboration surface

**Goal:** Make the already-public GitHub project easier to collaborate on without overstating protocol maturity.

**Tasks:**

- Tighten README roadmap/current status for external readers.
- Prepare GitHub Issues/Discussions templates or seed issues only if accurate and prototype-labeled.
- Draft a concise public update/post that clearly states what is local/synthetic versus verified.
- Run preflight/tests before any public push or post.

**Gate:**

Public collaboration surfaces and updates are approved for this project when accurate, non-spammy, and clearly labeled research/prototype. Do not contact specific people directly. Do not spend money, use production/private keys, or claim production readiness, censorship-proof guarantees, live IPFS availability, real signing/Sigstore/in-toto verification, SLSA compliance, or live protocol verification unless actually verified.

**Current result:**

Completed as a public GitHub collaboration surface. Roadmap/docs were updated and public issues #1–#5 were verified for renderer UX, Nostr parser/conformance, Radicle safe local verification, artifact state modeling, and provenance evolution. GitHub remains temporary coordination scaffolding while decentralized collaboration is fixture-backed.

## Loop 10: final architecture/roadmap/decision matrix cleanup

**Goal:** Consolidate public-facing architecture, roadmap, status, and protocol decision docs after Loop 9.

**Tasks:**

- Update README/architecture/protocol matrix/roadmap/status docs so they consistently distinguish local fixtures, dry-run protocol shapes, source-inspected mappings, synthetic provenance, and live-verified support.
- Add or tighten a next-step decision matrix for the next implementation loops.
- Keep edits documentation-bounded and secret-free.
- Run stdlib tests and JSON validation for touched/related fixtures.

**Gate:**

Do not add new live protocol claims, public posts, spending, production/private keys, or infrastructure. If JSON fixtures/schemas are touched, validate them with `python3 -m json.tool` and run `python3 -m unittest discover -s tests`.

**Current result:**

Completed as documentation consolidation. `README.md`, `ARCHITECTURE.md`, `PROTOCOL-MATRIX.md`, `ROADMAP.md`, `STATUS.md`, `AGENT-LOOPS.md`, and `docs/public-collaboration.md` now align on fixture-vs-live boundaries and recommend Loop 11 as a local NIP-34 parser/conformance adapter.

## Loop 11: NIP-34 parser/conformance adapter and fixture round-trip tests

**Goal:** Turn existing NIP-34 dry-run fixtures into a reusable local adapter seam without publishing to relays.

**Tasks:**

- Add a small stdlib parser/export helper for `fixtures/nostr-repo-announcement.json` and `fixtures/nostr-collaboration-events.json`.
- Round-trip repository id/name/clone URLs/maintainers plus issue and patch title/status/content mappings back to registry concepts.
- Add unit tests proving fixture conformance and preserving dry-run non-claim fields.
- Update `docs/nip34-event-shapes.md`, `STATUS.md`, and README if behavior or verification states change.

**Current result:**

Completed as a local stdlib parser/conformance adapter. `scripts/nip34_adapter.py` parses the existing NIP-34 repository announcement and issue/patch fixtures back into registry-shaped concepts, including repository id/name/description/web URL, clone URLs, Nostr maintainers, issue/patch title/status/summary/content, NIP-34 substrate fields, and dry-run non-claim metadata. Unit tests round-trip the fixture mappings and assert placeholder IDs/signatures, relay fallback, synthetic key policy, NIP-35 boundary, and `published: false`. No relay publishing, key use, event signing, event-id computation, or live relay verification was performed.

**Gate:**

Keep relay publishing out of scope unless disposable/project-scoped keys, relay selection, storage location, and public protocol gates are explicitly satisfied. No production/private keys, paid services, unsupported live-verification claims, or direct outreach.

## Loop 12: NIP-34 renderer/import follow-up

**Goal:** Wire the completed local NIP-34 adapter into the static renderer without external services.

**Current result:**

Completed as a local renderer/import surface. `scripts/render_project_page.py` now accepts paired `--nip34-repo-fixture` and `--nip34-collaboration-fixture` arguments plus optional `--nip34-state-status-fixture`, imports them through `scripts/nip34_adapter.py`, and renders a **NIP-34 fixture adapter** section in `output/demo-project.html`. The section displays local parser/conformance output including repository id/name/kind, relay hints, dry-run publish status, imported issue/patch counts/titles/statuses/summaries/source kinds, repository state HEAD ref/commit/refs, fixture-only status/check projections, and relay/key/NIP-35/state-status dry-run non-claim fields. Tests assert the rendered section, boundary language, placeholder IDs/signatures, current Git HEAD mapping, and required paired arguments. No relay publishing/readback, relay fetching, key use, signing, event-id computation, live protocol verification, spending, public post, commit, or push was performed.

**Gate:**

Keep this as local fixture import/display only. Do not claim Nostr relay compatibility until a disposable-key relay publish/readback path is explicitly approved and verified.

## Loop 13: Local NIP-34 repository state/status fixture follow-up

**Goal:** Extend local NIP-34 fixture coverage to repository state and fixture-only status/check display without publishing or signing.

**Current result:**

Completed as a local fixture follow-up because `rad` was unavailable for a safe CLI replay path. Added `fixtures/nostr-repo-state-status.json` with a dry-run `kind: 30618` repository state event generated from the local `git rev-parse HEAD` recorded at fixture creation time (`32f88a7a42498328a515e4763e28d84216420a98`) plus fixture-only status/check projections tied to that state and existing synthetic CI names. Later commits may make this recorded SHA an ancestor rather than current `HEAD`. `scripts/nip34_adapter.py` parses the state refs/HEAD commit and preserves placeholder id/signature/pubkey plus `published: false`; `scripts/render_project_page.py` displays the repository state, status/check projections, and explicit state/status non-claims. Tests validate the recorded Git SHA mapping and no relay/signing/public-status claims.

**Gate:**

Keep repository state/status evidence local until a future loop explicitly approves disposable/project-scoped keys, relay selection, signing, publish/readback verification, and public status semantics. No production/private keys, paid services, unsupported live-verification claims, or direct outreach.
