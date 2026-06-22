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

## Loop 14: Local NIP-01/NIP-34 conformance metadata for dry-run fixtures

**Goal:** Strengthen the local NIP-34 adapter with NIP-01 event-shape metadata without signing or publishing.

**Current result:**

Completed as local-only conformance reporting. `scripts/nip34_adapter.py` now validates required NIP-01 event fields, tag/content shapes, exact non-bool integer `kind`/`created_at`, and fixture pubkey shape for repository announcement (`30617`), issue (`1621`), patch (`1617`), and repository state (`30618`) fixtures. The adapter exports `dry_run.conformance.reports[]` with placeholder id/signature flags, `event_id_computed: false`, `signed: false`, `published: false`, and local-only `serialized_event_payload`/`possible_event_id` references where shape permits; those references are not fixture ID replacements or signed/relay-accepted event ID claims. Tests cover valid reports and invalid bool integer/tag/content/pubkey rejection.

**Gate:**

Keep these reports as local metadata only. Do not replace dry-run fixture IDs/signatures or claim live Nostr compatibility until disposable/project-scoped keys, relay selection, signing, publish/readback, and verification are explicitly approved and completed.

## Loop 15: Render local NIP-34 conformance metadata in static HTML

**Goal:** Display the Loop 14 local conformance reports in the static renderer without increasing protocol claims.

**Current result:**

Completed as a local renderer follow-up. `scripts/render_project_page.py` now displays `dry_run.conformance.reports[]` as a concise **Local NIP-34 conformance summary** with report count, known NIP-34 kind count, scope/source, per-event label/kind/local-validity, placeholder id/signature flags, signed/published false fields, and `possible_event_id` labeled as local reference only. Full serialized payloads are intentionally omitted by default. `output/demo-project.html` was regenerated with all optional NIP-34 fixtures, and tests assert the rendered summary, possible-event-ID labels/values, placeholder metadata, boundary wording, and low-noise payload omission.

**Gate:**

Keep the summary as local fixture metadata only. Do not replace dry-run fixture IDs/signatures or claim live Nostr compatibility until disposable/project-scoped keys, relay selection, signing, publish/readback, and verification are explicitly approved and completed.

## Loop 16: Further schema/fixture cleanup around verification-state labels

**Goal:** Tighten schema/fixture/status consistency now that Loop 15 has been parent-verified and pushed.

**Candidate tasks:**

- Further schema/fixture cleanup around fixture-vs-live verification labels.
- Make local-only/live-unverified status fields easier to consume consistently across registry, renderer, and docs.
- Safe Radicle local CLI replay only if an approved `rad` binary/install path appears.

**Gate:**

Keep all live protocol claims gated by actual command/network verification. No relay publishing, spending, production/private keys, unsupported security/durability/censorship-proof claims, or direct outreach without the existing project gates being satisfied.

**Current result:**

Completed as local schema/fixture/renderer cleanup. `schemas/project-registry.schema.json` now allows top-level `verification_states[]`; both registry fixtures include explicit rows for local fixture, source-inspected mapping, synthetic fixture, and live-unverified scopes as applicable; `scripts/render_project_page.py` renders a **Verification states** section; tests assert the schema enum, explicit fixture rows, no live-verified claims for unverified protocol scopes, renderer output, and absence of unsupported claim phrases. No relay publishing, live protocol verification, spending, production/private keys, or unsupported security/durability/censorship-proof claims were introduced.

## Loop 17: Verification-state vocabulary follow-up or safe live-gated replay

**Goal:** Reuse the new verification-state labels in adapter outputs/docs, or run a safe local live-verification replay only if prerequisites are explicitly satisfied.

**Candidate tasks:**

- Make `scripts/nip34_adapter.py` exports consume or emit `verification_states[]`-compatible records for imported fixture evidence.
- Align any remaining docs/status tables on the same state vocabulary.
- Attempt a Radicle local CLI replay only if an approved `rad` binary/install path is available; use temporary local state and avoid public seed publishing by default.

**Current result:**

Completed as local adapter/renderer vocabulary alignment. `scripts/nip34_adapter.py` now exports adapter-local `verification_states[]` records using the same vocabulary as top-level registry fixtures for repository announcement import, collaboration events, conformance reports, repository state, and synthetic fixture-only status/check projections. `scripts/render_project_page.py` renders those adapter rows inside the optional NIP-34 fixture adapter section, separate from the registry-level verification states. Tests assert non-live/synthetic/local adapter values, renderer display, and absence of unsupported live/security/durability/censorship-proof claim phrases in adapter rows. `output/demo-project.html` was regenerated with all optional NIP-34 fixtures. No relay publishing, signing, fixture ID replacement, live protocol verification, spending, or key use occurred.

**Gate:**

No relay publishing, spending, production/private keys, unsupported live protocol/security/durability/censorship-proof claims, or direct outreach. Any live-verified row must be backed by actual command/network evidence recorded in docs/tests.

## Loop 18: Static UX/status filtering or safe live-gated replay

**Goal:** Make verification-state rows easier to consume in the static UI, or run a live-gated replay only if prerequisites are explicitly satisfied.

**Candidate tasks:**

- Add static renderer grouping/filtering/summaries for registry and adapter verification-state rows.
- Keep local/synthetic/live-unverified labels visible without implying live protocol support.
- Attempt a Radicle local CLI replay only if an approved `rad` binary/install path is available; use temporary local state and avoid public seed publishing by default.

**Gate:**

No relay publishing, spending, production/private keys, unsupported live protocol/security/durability/censorship-proof claims, or direct outreach. Any live-verified row must be backed by actual command/network evidence recorded in docs/tests.

**Current result:**

Completed as local static renderer UX/status work. `scripts/render_project_page.py` now summarizes registry-level and adapter-level `verification_states[]` rows with total counts, live-verified counts, live-unverified/local counts, synthetic/non-synthetic counts, state chips, grouped rows by state, and claim-boundary summaries. CSS classes make local fixture, source-inspected mapping, synthetic fixture, live-unverified, and live-verified labels visible without JavaScript. `output/demo-project.html` was regenerated with all optional NIP-34 fixtures, and tests assert registry/adapter summary counts with current live-verified counts remaining zero. No relay publishing, signing, fixture ID replacement, live protocol verification, spending, or key use occurred.

## Loop 19: Release/preflight polish for generated static artifact

**Goal:** Make the generated static HTML artifact and public usage instructions easier to verify and consume without adding live protocol claims.

**Current result:**

Completed as local static artifact release/preflight polish. Added `scripts/preflight_static_artifact.py`, a stdlib-only check that verifies `output/demo-project.html` exists, is byte-for-byte current with a regenerated renderer output using all optional NIP-34 fixtures, includes required local/synthetic/non-claim and adapter/state/status/conformance sections, and omits selected unsupported live-protocol/security/durability claim phrases. README now documents regeneration, local browser opening, preflight, and full local verification commands. Tests cover preflight pass/fail behavior and the CLI command. `output/demo-project.html` was regenerated with all optional NIP-34 fixtures. No hosting, paid screenshot tooling, relay publishing, signing, fixture ID replacement, live protocol verification, spending, or key use occurred.

**Gate:**

No relay publishing, spending, production/private keys, unsupported live protocol/security/durability/censorship-proof claims, or direct outreach. Any live-verified row must be backed by actual command/network evidence recorded in docs/tests.

## Loop 20: Safe live-gated adapter replay planning

**Goal:** Prepare the next live-verification seam without accidentally performing public protocol actions or overclaiming support.

**Candidate tasks:**

- Discover whether an approved `rad` binary/install path is available; if yes, design a temporary `RAD_HOME` local replay with no public seed publish by default.
- Alternatively, draft a Nostr disposable/project-scoped key and relay publish/readback checklist, including storage location, relay choice, signing steps, readback evidence, and rollback/non-claim wording.
- Keep implementation changes documentation/test bounded unless prerequisites are satisfied and explicit gates allow a live replay.

**Gate:**

Do not publish to relays, spend money, use production/private keys, contact specific people directly, claim live verification, or create public CI/status events unless the documented prerequisite gates are satisfied and command/network evidence is recorded.

**Current result:**

Completed as safe planning only. `command -v rad` found no `rad` executable on `PATH`, so `rad --version` and any local Radicle replay were not run. Added `docs/live-adapter-replay-plan.md` and `fixtures/live-adapter-replay-checklist.json` to capture Radicle temporary-`RAD_HOME` prerequisites, Nostr disposable-key publish/readback prerequisites, evidence capture, rollback, promotion criteria, and hard non-claim gates. Tests validate the checklist remains secret-free, non-live, and blocked on the missing Radicle binary. No Radicle CLI action, relay publishing/readback, key generation, signing, public status event, spending, direct outreach, or live protocol verification occurred.

## Loop 21: Approved tooling install and disposable Nostr key prerequisite

**Goal:** Satisfy the missing CLI/key prerequisite without performing Radicle replay or Nostr relay publication.

**Completed:**

- Installed Radicle user-local binaries under `~/.local/bin`: `rad`, `radicle-node`, and `git-remote-rad` version 1.9.1.
- Installed Nostr CLI `nak` under `~/.local/bin` version v0.20.0.
- Generated a disposable/project-scoped Nostr secret key outside the repo at `~/.hermes/keys/decentralized-forge/nostr-project.nsec` with `0600` permissions; only public identifiers are recorded in project docs.
- Added offline signed proof event `evidence/nostr-offline-key-proof-2026-06-22.json`; verified locally with `nak verify`; not published.
- Updated the live replay plan, machine-readable checklist, status, context, and tests for the installed/key-ready but still non-live state.

**Gate preserved:**

No Radicle replay, Radicle node start, Nostr relay publishing/readback, Radicle seed publishing, spending, production/private personal keys, unsupported claims, or direct outreach occurred.

## Loop 22: Radicle local replay preflight

**Goal:** Confirm exact safe local-only Radicle command surface before repository replay.

**Candidate tasks:**

- Read local `rad --help` and selected subcommand help/manpage output.
- Create `evidence/radicle-local-replay-preflight-YYYY-MM-DD.md` with the smallest safe command sequence.
- Update `docs/next-live-adapter-loops.md`, checklist/status/context if help output changes the plan.

**Gate:**

Stateful Radicle commands such as auth, identity generation, repository initialization, node start, seed publish, sync, announce, or remote peer configuration require Permission A from `docs/next-live-adapter-loops.md`.

**Current result:**

Completed as read-only CLI help/version preflight. Added `evidence/radicle-local-replay-preflight-2026-06-22.md`, recording `rad` path/version, inspected `rad --help`, `rad init --help`, `rad inspect --help`, identity/node-related help surfaces, and the fact that `rad status` is not a known command in Radicle 1.9.1. The smallest Loop 23 path is temporary `RAD_HOME`, disposable Git repo, disposable `rad auth` only if required, `rad init --no-confirm --no-seed --private`, and local `rad inspect` commands. No `rad auth`, `rad init`, node start, seed/publish/sync/announce, peer configuration, production/private personal key use, spending, or public Radicle network verification occurred.

## Loop 23: Radicle temporary-`RAD_HOME` disposable repo replay

**Goal:** Run a bounded local Radicle replay with disposable state and capture command evidence.

**Requires:** Permission A.

**Candidate tasks:**

- Create temporary `RAD_HOME` and disposable Git repo.
- Create a minimal disposable Git commit.
- Run only the smallest local Radicle init/inspect commands confirmed by Loop 22.
- Capture stdout/stderr into `evidence/` without secrets.
- Update docs/tests to distinguish local CLI verification from public seed/network verification.

**Gate:**

Abort if the command asks for persistent personal identity, attempts node/seed/network actions, exposes secrets, or makes local-only behavior ambiguous.

## Loop 24: Nostr relay selection and event payload review

**Goal:** Choose safe public relay targets and finalize the exact prototype payload before publication.

**Candidate tasks:**

- Read relay info endpoints/docs and record terms/rate-limit/retention notes where discoverable.
- Draft the exact prototype-labeled event payload locally.
- Sign and verify locally only if it remains unpublished and secret-free.
- Create `docs/nostr-relay-publish-readback-plan.md` and `evidence/nostr-relay-selection-YYYY-MM-DD.md`.

**Gate:**

Relay publication requires Permission B from `docs/next-live-adapter-loops.md` because Nostr events may be public and retained.

## Loop 25: Nostr disposable publish/readback

**Goal:** Publish a prototype-labeled event with the disposable project key and read it back by event ID.

**Requires:** Permission B.

**Candidate tasks:**

- Sign event locally with `nak` using the project key.
- Verify event ID/signature locally.
- Publish to selected relay(s).
- Read back by event ID and verify returned fields.
- Record relay URLs, event IDs, publish responses, readback payloads, verification, and non-claims.

**Gate:**

Abort if relay requires payment/production credentials, rejects in a way that needs human choice, payload review finds overclaiming content, or secret-marker scan fails.

## Loop 26: Live evidence import into adapter/renderer

**Goal:** Import narrow live-evidence metadata into fixtures/renderer without replacing fixture-only claims improperly.

**Candidate tasks:**

- Add or update `fixtures/live-evidence-index.json` if useful.
- Update `fixtures/live-adapter-replay-checklist.json` with verified evidence only.
- Update renderer/tests only if a live/local/fixture distinction needs to be displayed.
- Run tests, static preflight, and secret-marker scan.

**Gate:**

No claim may be upgraded to live-verified without command/network evidence from Loop 23 and/or Loop 25.

## Loop 27: Public project update draft

**Goal:** Draft a concise public status update for GitHub project channels explaining verified scope and next gates.

**Candidate tasks:**

- Draft locally in `docs/public-update-drafts/`.
- Include exact non-claims and next gates.

**Gate:**

Posting the update publicly requires separate public-post approval unless Eric explicitly grants it with the permission bundle. No direct outreach or unsupported security/durability/censorship-proof claims.
