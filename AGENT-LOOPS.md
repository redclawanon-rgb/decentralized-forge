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

**Current result:**

Completed as a bounded local CLI replay. Used temporary `RAD_HOME`, a disposable Git repo, disposable `rad auth --stdin`, `rad init --private --no-confirm --no-seed`, and local `rad inspect` commands. Evidence is `evidence/radicle-local-replay-2026-06-22.md`. Local RID `rad:z33oByNZxkxXAChhD54B4XiSsQkao`, delegate DID `did:key:z6MkutM4LWh4y9qdeSMTWW88pMDVJBBhnjkoGPgZq1aSYN2n`, visibility `private`. No node start, seed publish, sync/announce, remote peer configuration, paid infrastructure, production/private personal key use, direct outreach, public network replication, or live public Radicle verification occurred.

## Loop 24: Nostr relay selection and event payload review

**Goal:** Choose safe public relay targets and finalize the exact prototype payload before publication.

**Current result:**

Completed as relay/payload selection plus local signature verification. Selected `wss://relay.damus.io` and `wss://nos.lol` after `nak relay` NIP-11 checks showed both reachable and reported `auth_required: false`, `payment_required: false`, and `restricted_writes: false`. Added `docs/nostr-relay-publish-readback-plan.md`, `evidence/nostr-relay-selection-2026-06-22.md`, `evidence/nostr-loop24-unsigned-payload-2026-06-22.json`, and `evidence/nostr-loop24-signed-event-preview-2026-06-22.json`. The signed local event preview is a prototype/research-labeled kind `30617` repository announcement with event ID `4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba`, using only the disposable project pubkey `6669423ee76d9d5adc8e81df79286c2569edbe5ab84f3e35043db71a54eff5c8`; `nak verify` exited 0. No relay publication/readback occurred in Loop 24.

**Gate:**

Loop 25 may publish/read back the exact signed event preview under Permission B. Treat publication as public/irreversible. Abort if a relay requires payment/production credentials, if readback ambiguity requires human choice, or if any secret marker appears in evidence. Do not claim durability, global propagation, censorship resistance, identity trust, production readiness, or full protocol compatibility from relay acceptance/readback.

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

**Current result:**

Completed as selected public relay acceptance/readback for one prototype-labeled disposable-key event. Published exact signed preview `4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba` to `wss://relay.damus.io` and `wss://nos.lol`; both publish commands exited 0 and both relays returned the matching event by ID. Local and readback `nak verify` checks exited 0. Evidence: `evidence/nostr-loop25-publish-readback-2026-06-22.md` and `.json`. No spending, paid infrastructure, production/private personal key, direct outreach, durability/global-propagation/censorship-resistance/identity-trust/production-readiness/security/full-compatibility claim, or Radicle public network action occurred.

## Loop 26: Live evidence import into adapter/renderer

**Goal:** Import narrow live-evidence metadata into fixtures/renderer without replacing fixture-only claims improperly.

**Current result:**

Completed as a bounded evidence import. Added `fixtures/live-evidence-index.json` for Loop 23 Radicle local CLI/private replay evidence and Loop 25 Nostr selected-relay publish/readback evidence. `scripts/render_project_page.py` now accepts `--live-evidence-index` and renders a **Live evidence index** section that distinguishes `local-cli-verified` from `selected-relay-readback-verified` while preserving non-claims. `scripts/preflight_static_artifact.py`, `tests/test_registry_fixture.py`, `fixtures/live-adapter-replay-checklist.json`, and `output/demo-project.html` were updated accordingly. No new live network action, Nostr publish, Radicle node/seed/sync/publish/remote clone, spending, production/private personal key use, direct outreach, or unsupported durability/global-propagation/censorship-resistance/security/production-readiness/full-compatibility claim occurred.

**Gate:**

No claim may be upgraded to live-verified without command/network evidence from Loop 23 and/or Loop 25. Loop 27 is the next approved public update draft/post path if accurate, non-spammy, and prototype/research-labeled.

## Loop 27: Public project update draft

**Goal:** Draft a concise public status update for GitHub project channels explaining verified scope and next gates.

**Candidate tasks:**

- Draft locally in `docs/public-update-drafts/`.
- Include exact non-claims and next gates.

**Gate:**

Posting the update publicly requires separate public-post approval unless Eric explicitly grants it with the permission bundle. No direct outreach or unsupported security/durability/censorship-proof claims.

**Current result:**

Completed as a public project-channel update. Drafted `docs/public-update-drafts/2026-06-22-live-adapter-evidence-update.md` and posted it to GitHub Discussions / Announcements: https://github.com/redclawanon-rgb/decentralized-forge/discussions/6. The update is explicitly research/prototype-labeled and distinguishes Radicle local CLI/private replay from Nostr selected-relay acceptance/readback evidence. No direct outreach, spending, production/private key use, Radicle public-network action, paid storage/wallet action, or unsupported durability/global-propagation/censorship-resistance/security/production-readiness/full-compatibility claim occurred.

## Loop 28: Nostr readback persistence/divergence check

**Goal:** Re-read the Loop 25 event after time has passed and record whether selected relays still return the same event.

**Current result:**

Completed as low-volume readback persistence/divergence evidence. Re-read event `4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba` from the Loop 25 selected relays `wss://relay.damus.io` and `wss://nos.lol` plus Permission-E extra readback-only relays `wss://relay.primal.net` and `wss://nostr.wine`. The selected relays and `wss://relay.primal.net` returned the exact event with fields matching the signed preview and `nak verify` passing; `wss://nostr.wine` did not return the event during this check. Evidence: `evidence/nostr-loop28-readback-check-2026-06-22.md` and `.json`. No new Nostr event was published, no secret key material was read/printed, and no paid/authenticated relay, production/private personal key, direct outreach, or Radicle public-network action was used.

**Candidate tasks:**

- Query `wss://relay.damus.io` and `wss://nos.lol` by Loop 25 event ID.
- Optionally query a small number of extra free public relays if Permission E is granted.
- Verify returned event IDs/signatures with `nak verify`.
- Record relay divergence: returned/not returned, fields match, verify pass/fail.

**Gate:**

Extra relays or any additional Nostr publish require Permission E. Stop if a relay requires payment/auth/production credentials or if checks become broad/spammy.

## Loop 29: NIP-34 live-event adapter import

**Goal:** Convert verified live Nostr event/readback evidence into the local NIP-34 adapter path without pretending it is full forge compatibility.

**Candidate tasks:**

- Add a live-event fixture or index entry referencing Loop 25 evidence.
- Show the event as selected-relay-readback verified, separate from fixture-only rows.
- Keep dry-run fixtures separate from live readback evidence.
- Document missing NIP-34 semantics that remain unverified.

**Gate:**

No new live publish is allowed unless Permission E is granted. Abort if renderer wording blurs fixture-only, local CLI, selected-relay readback, or full protocol compatibility.

**Current result:**

Completed as selected-relay readback evidence import. Added `fixtures/nostr-live-readback-events.json`; `scripts/nip34_adapter.py` now imports the recorded Loop 25 kind `30617` event separately from dry-run fixtures, recomputes the NIP-01 event ID locally, and emits a narrowly scoped `live-verified` adapter row for selected-relay readback only. `scripts/render_project_page.py` renders a separate **NIP-34 live readback import** subsection, and static preflight/tests/checklist/output were updated. No new relay publish, relay fetch, signing, key read, spending, direct outreach, Radicle public-network action, or unsupported durability/global-propagation/censorship-resistance/identity-trust/security/production/full-compatibility claim occurred.

## Loop 30: Radicle public-network gate plan

**Goal:** Prepare a no-surprises plan for a later public Radicle seed/publish/remote clone verification.

**Candidate tasks:**

- Inspect `rad publish`, `rad seed`, `rad sync`, `rad node`, `rad remote`, clone/fetch help/docs.
- Identify exact disposable public seed/clone smoke commands.
- Identify identity persistence, network publication, cleanup, peer visibility, and non-claim risks.
- Draft Permission G execution checklist without executing it.

**Gate:**

Permission F covers preflight only. Permission G is required before any public Radicle seed/publish/sync/node/remote clone action.

**Current result:**

Completed as Permission-F help-only preflight. Added `docs/radicle-public-network-gate-plan.md` and `evidence/radicle-public-network-preflight-2026-06-22.md`. Inspected only `--help` surfaces for `rad publish`, `rad seed`, `rad sync`, `rad sync status`, `rad node`, `rad node start`, `rad node status`, `rad node connect`, `rad remote`, `rad remote add`, `rad remote list`, `rad clone`, `rad fetch`, `rad unseed`, and `rad follow`. Findings: `rad publish` makes a repository public/discoverable; `rad sync` defaults to fetch+announce; `rad remote add` defaults may fetch/sync; `rad clone` uses local node routing or explicit seeds; `rad fetch` is not a known command in Radicle 1.9.1. No `RAD_HOME` was created, no Radicle identity was created/reused, no node was started, no repo was published/seeded/synced/announced/cloned/fetched/connected/followed/remotely configured, and no public Radicle network action occurred. Permission G remains required before the public seed/remote-clone smoke.

## Loop 31: Public storage/IPFS evidence gate plan

**Goal:** Plan the next artifact-storage verification step without spending money or claiming durability.

**Current result:**

Completed as Permission-H inventory/plan preflight only. Added `evidence/storage-tooling-preflight-2026-06-22.md` and `docs/public-storage-evidence-gate-plan.md`. Inventory found no installed IPFS/Kubo CLI, CAR/IPLD/CID CLI, IPFS cluster tools, `go-ipfs`, or Python multiformats/CAR modules. Local/free runtimes found Node/npm/npx/corepack, Python, and uv; Go/Rust/Cargo were missing. Read-only `npm view` metadata checked `ipfs-car@3.1.0`, `@ipld/car@5.4.6`, `multiformats@14.0.0`, `helia@6.1.4`, and `kubo-rpc-client@7.1.0` without installing or executing packages. No IPFS daemon start, add/fetch/pin, CAR creation/import, public gateway check, paid pinning/storage, Filecoin/Arweave wallet action, spending, production/private key use, direct outreach, durability claim, or production/security/censorship-resistance claim occurred.

**Candidate next step:** Loop 33 local CAR/CID fixture verification. Dependency-backed path needs explicit approval to add project-scoped dev dependencies; no-new-dependency fallback can only strengthen stdlib CID docs/tests.

**Gate:**

Permission H covered preflight only. Separate explicit approval is required for project-scoped dependency installation, paid pinning, wallet use, Filecoin/Arweave, paid storage, gateway availability checks, live IPFS claims, or durability claims.

## Loop 32: Next controller/report consolidation

**Goal:** Consolidate Loop 26–31 outcomes into project status/context and a concise next-roadblock report.

**Current result:**

Completed as docs/checklist/test consolidation. Updated `STATUS.md`, `.hermes/context.md`, `AGENT-LOOPS.md`, `docs/next-evidence-and-interoperability-loops.md`, `fixtures/live-adapter-replay-checklist.json`, and tests for Loop 31 completion and remaining gates. Verification, commit, push, and final concise report are handled by the controller run.

**Gate:**

No additional cron jobs. No public Radicle seed/publish/sync/node/remote clone without Permission G. No live storage, package install, paid storage, wallet, or durability claim without a new explicit approval.

## Next loop-set setup

`docs/next-evidence-and-interoperability-loops.md` records Loops 26–35. Eric approved Permission G and Permission I on 2026-06-22 via Telegram message: “G & I are approved to keep things moving along.”

## Loop 33: Local CAR/CID fixture verification

**Goal:** Strengthen artifact-storage evidence using only local/free tooling and exact local bytes.

**Current result:** Completed as Permission-I local CAR/CID fixture verification. Added project-scoped lockfile-backed dev dependencies `@ipld/car@5.4.6` and `multiformats@14.0.0`, `scripts/verify_car_cid_fixture.mjs`, `evidence/local-car-cid-fixture-2026-06-22.json`, and `evidence/local-release-artifact-2026-06-22.car`. `npm run verify:car-cid` passed and verified the local artifact bytes map to CID `bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua`; CAR root/block/readback checks passed. No IPFS daemon, add/fetch/pin, gateway, wallet, paid storage, Filecoin/Arweave, or durability/security/production claim occurred.

**Gate preserved:** This is local CAR/CID evidence only. Live IPFS add/fetch/gateway/pinning, Filecoin/Arweave, paid storage, durability/global-availability/censorship-resistance/security/production claims remain separately gated.

## Loop 34: Disposable public Radicle seed/remote-clone smoke

**Goal:** Run one bounded disposable public Radicle smoke under Permission G.

**Current result:** Completed as exact bounded public Radicle evidence. `scripts/run_radicle_public_smoke.py` created temporary seed/clone Radicle profiles under `/tmp`, initialized disposable public RID `rad:z2WtozFrCRhygh9CGzyUN57CN7Nwa`, started a localhost seed node, updated seed policy, ran sync/announce, started a separate temporary clone node, connected to the disposable seed over localhost, cloned with `rad clone --seed <disposable NID>`, and verified README readback. Evidence: `evidence/radicle-public-network-smoke-2026-06-22.json` and `.md`. Nodes were stopped and temporary state removed.

**Gate preserved:** No production/private personal keys, paid infrastructure, spending, direct outreach, named external peer targeting, or persistent state was used. Do not claim durability, censorship resistance, security, global replication, identity trust, production readiness, full Radicle compatibility, or broad Radicle network availability from this one smoke.

## Loop 35: Consolidation/report

**Goal:** Consolidate the Permission-I and Permission-G results into durable project state and stop at the next approval boundary.

**Current result:** Complete as docs/context/status/checklist/test consolidation. Added `evidence/loop35-consolidation-2026-06-22.md`, advanced `fixtures/live-adapter-replay-checklist.json` to loop 35, and updated tests/status/context/loop docs. Loop 35 did not perform any new public protocol action, storage action, public update, spending, production/private personal key use, direct outreach, or cron creation.

**Gate preserved:** Further live storage, broader/repeated Radicle public-network checks, public updates about Loops 33–34, or stronger durability/censorship/security/production claims need a new explicit approval/target.

## Next useful loop

- Milestone 1 is complete as a reproducible, evidence-scoped static prototype with hosted local-verification CI passing on `main`.
- A prototype-labeled public Milestone 1 update was posted to GitHub Discussion #7.
- Use the approval-bounded next-loop controller for recurring safe verification/reporting: `npm run next:loop` locally or the manual `next-loop-controller` GitHub Actions workflow.
- Live IPFS, Radicle, Nostr, and signing/provenance actions are approved as of 2026-06-28 when they stay free, disposable or project-scoped, low-volume, secret-free, and evidence-labeled.
- Stop before spending, wallets, paid infrastructure, production/private personal keys, direct outreach, persistent public seed/background services, or stronger durability/censorship/security/SLSA/production-readiness claims unless separately approved.

## Loop 38: Approval-bounded next-loop controller

**Goal:** Let safe housekeeping continue without Eric repeatedly prompting for the same next step, while preserving the live-action approval gates.

**Current result:** Complete as a repo-contained controller. Added `fixtures/next-loop-controller.json`, `scripts/next_loop_controller.py`, `docs/autonomy/README.md`, npm scripts `next:loop`/`next:check`, tests, and manual GitHub Actions workflow `.github/workflows/next-loop.yml`.

**Gate preserved:** The controller runs one iteration per invocation. It may check worktree state, run local verification, inventory live-gate tooling without live actions, and draft `docs/autonomy/next-loop-report.md`. It does not auto-commit, push, publish, sign, spend, contact people, use wallets or production/private personal keys, or run live IPFS/Nostr/Radicle actions without a separate explicit target.

## Loop 39: Standing live-action approval recorded

**Goal:** Convert Eric's broad live-action approval into precise controller rules without removing cost, key, outreach, persistence, or claim-scope safety boundaries.

**Current result:** Complete as `fixtures/next-loop-controller.json`, controller report wording, autonomy docs, status docs, and tests. Live IPFS, Radicle, Nostr, and signing/provenance actions are now approved when free, disposable or project-scoped, low-volume, secret-free, and evidence-labeled.

**Gate preserved:** No live protocol/storage/signing action was executed in Loop 39. Spending, wallets, paid infrastructure, production/private personal keys, direct outreach, persistent public seed/background services, and stronger durability/censorship/security/SLSA/production-readiness claims remain separately gated.

## Loop 40: GitHub keyless artifact attestation workflow

**Goal:** Add real hosted keyless provenance generation for reproducible prototype artifacts without private signing keys.

**Current result:** Complete as hosted keyless attestation evidence. The `ci` workflow grants GitHub OIDC/attestation permissions and runs `actions/attest@v4` on `main` pushes for generated HTML, summary JSON, the local CAR fixture, and the local release artifact fixture. GitHub Actions run https://github.com/redclawanon-rgb/decentralized-forge/actions/runs/28339280081 passed, the attestation step completed successfully, and `evidence/github-keyless-attestation-2026-06-28.json` records subject digests plus the SLSA provenance predicate, builder identity, invocation URL, resolved commit, and transparency-log entry count.

**Gate preserved:** This is GitHub-hosted keyless attestation generation only. It does not use production/private personal keys, paid infrastructure, wallets, direct outreach, persistent background services, or stronger durability/censorship/security/SLSA/production-readiness claims. Local registry fixture provenance fields remain synthetic until a later import loop records a concrete workflow run and verification evidence.

## Loop 41: Local Helia/IPFS add-get fixture verification

**Goal:** Turn the approved live IPFS/storage lane into one bounded, project-scoped local add/get check for the existing release artifact fixture.

**Current result:** Complete as local Helia add/get evidence. Added `helia@6.1.4` and `@helia/unixfs@7.2.1` as lockfile-backed dev dependencies, `scripts/verify_helia_fixture.mjs`, npm script `verify:helia`, and `evidence/helia-local-ipfs-add-get-2026-06-28.json`. The verifier creates a non-started offline in-memory Helia instance with no libp2p listeners, transports, discovery, routers, or block brokers; adds `fixtures/local-release-artifact.txt`; reads the exact bytes back; and records CID `bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua` plus matching SHA-256 `3932e28d5b609b3cae25218ca205ea126cd3cf344628dc4c4b9bf094c50668a0`. The live evidence index, renderer output, CI, docs, and tests now include this row.

**Gate preserved:** This is local in-process Helia evidence only. No public gateway, public pinning service, paid storage, Filecoin, Arweave, wallet, production/private personal key, persistent daemon, background service, direct outreach, durability claim, global availability claim, censorship-resistance claim, security guarantee, or production-readiness claim was introduced.

## Loop 42: Public gateway/pinning preflight

**Goal:** Query a small set of public IPFS gateways for the local release artifact CID and record pinning preflight status without making a durability claim.

**Current result:** Complete as `evidence/public-gateway-pinning-preflight-2026-06-28.json`. Three public gateway GET requests timed out for CID `bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua`; zero matching fixture readbacks were observed. No pinning provider account/token or pin request was used.

**Gate preserved:** No daemon, persistent service, pinning, paid storage, Filecoin, Arweave, wallet, spending, durability, global availability, censorship-resistance, security, or production-readiness claim.

## Loop 43: Nostr issue/patch readback

**Goal:** Publish and read back disposable NIP-34-shaped issue and patch events using project-scoped tooling.

**Current result:** Complete as `evidence/nostr-loop43-issue-patch-readback-2026-06-28.json`. Added lockfile-backed `nostr-tools@2.23.8`; generated one in-memory disposable key; published one issue event and one patch event to `wss://relay.damus.io` and `wss://nos.lol`; read both back from selected relays with signature verification.

**Gate preserved:** No secret key material is recorded. No production/private personal key, paid relay, spending, direct outreach, durability, global propagation, censorship-resistance, identity trust, full NIP-34/forge compatibility, security, or production-readiness claim.

## Loop 44: Broader Radicle check

**Goal:** Attempt the next broader disposable Radicle check under current host constraints.

**Current result:** Complete as current-host blocker/read-only evidence in `evidence/radicle-loop44-broader-check-2026-06-28.json`. No `rad` CLI is available on this Windows host (`spawnSync rad ENOENT`), so broader disposable CLI clone/sync was not executable here. The loop recorded read-only public route probes for the prior disposable RID `rad:z2WtozFrCRhygh9CGzyUN57CN7Nwa`.

**Gate preserved:** No Radicle identity, `RAD_HOME`, node, seed, publish, sync, clone, connect, remote command, production/private personal key, paid infrastructure, persistent service, direct outreach, broad availability, durability, censorship-resistance, security, identity-trust, or production-readiness claim.

## Loop 45: Registry-shaped keyless-attestation import

**Goal:** Import hosted keyless attestation evidence into registry-shaped verification rows without replacing synthetic registry fixture provenance.

**Current result:** Complete as `fixtures/keyless-attestation.registry-verification.json`. The import records one `live-verified` registry-shaped row for `github-actions.keyless_artifact_attestation` outside the project-registry fixtures, tied to GitHub Actions run 28339280081 and six prototype artifact subjects.

**Gate preserved:** `fixtures/example-project.registry.json` keeps `ci.provenance` synthetic. No SLSA compliance, production supply-chain security, consumer policy verification, production/private signing key, or production-readiness claim.

## Loop 46: Trust hardening and public-tool readiness

**Goal:** Make the recorded evidence set harder to tamper with or misunderstand before building a broader public tool surface.

**Current result:** Complete as local trust-contract hardening. Added `schemas/live-evidence-index.schema.json`, evidence-file `evidence_sha256` and `evidence_size_bytes` metadata in `fixtures/live-evidence-index.json`, `validate-evidence-index`, `refresh-evidence-hashes`, and read-only `doctor` commands in `scripts/forge_registry.py`, CI coverage for those commands, and public-facing `docs/threat-model.md` plus `docs/community-quickstart.md`.

**Gate preserved:** No new live protocol/storage/signing action, spending, wallet, production/private personal key, direct outreach, persistent service, registry provenance replacement, SLSA compliance claim, durability claim, broad availability claim, censorship-resistance claim, security guarantee, or production-readiness claim.

## Loop 47: Static forge workbench app

**Goal:** Build the first usable local product surface around the recorded registry, evidence, and collaboration model without adding live protocol side effects.

**Current result:** Complete as a local static app. Added `scripts/render_forge_app.py` and generated `output/forge-app.html`, with `scripts/forge_registry.py render-app` wired into local verification and CI. The app renders project overview metrics, issues/patches, release/artifact evidence, evidence filtering, selected-relay Nostr issue/patch readback, and an unsigned local Nostr issue/patch draft workflow. Tests assert the generated app is current, embeds the expected evidence model, and does not contain relay publishing/signing runtime calls. Headless Chrome verification exercised overview, collaboration filtering, evidence filtering, and issue/patch draft generation.

**Gate preserved:** This is a committed static HTML app over committed fixture/evidence data. It does not fetch, open WebSockets, sign events, publish to relays, import private keys, run a hosted service, spend money, use wallets, replace registry provenance, or claim durability, censorship resistance, broad availability, security, SLSA compliance, or production readiness.

## Loop 48: Portable verification bundle

**Goal:** Package the current prototype state into a deterministic portable artifact that can be inspected and hash-checked without treating GitHub as the data authority.

**Current result:** Complete as local bundle export/verification. Added `scripts/forge_registry.py export-bundle` and `verify-bundle`, generated `output/decentralized-forge-verification-bundle.zip`, and wired the commands into `verify-local`, CI, tests, and attestation subjects. The ZIP contains schemas, fixtures, source evidence, generated HTML, summaries, `output/forge-app.html`, verifier scripts, package metadata, and `verification-bundle.manifest.json`. The verifier checks manifest schema, file sizes, SHA-256 hashes, required payloads, and live-evidence-index bindings. Tests compare a freshly generated bundle byte-for-byte against the committed bundle.

**Gate preserved:** This is local packaging of existing committed/generated evidence only. It does not publish protocol events, sign events, fetch from relays, pin storage, start daemons, spend money, use wallets, import private keys, replace registry provenance, or claim durability, censorship resistance, broad availability, security, SLSA compliance, or production readiness.

## Loop 49: Clean-room bundle consumer check

**Goal:** Verify that the portable bundle can be consumed from a temporary extracted tree without depending on the original checkout.

**Current result:** Complete as `scripts/forge_registry.py verify-bundle-cleanroom`. The command direct-verifies the ZIP, safely extracts it to a temporary directory with path-traversal checks, copies the ZIP into the extracted tree, and runs bundled checks from that tree: manifest JSON validation, `verify-bundle`, `validate-evidence-index`, and static artifact preflight. The bundle manifest now lists the clean-room command as a suggested verification command, tests assert the clean-room verifier passes, and CI runs it after bundle export/direct verification.

**Gate preserved:** This is temporary local extraction and verification only. It does not publish protocol events, sign events, fetch from relays, pin storage, start daemons, spend money, use wallets, import private keys, replace registry provenance, or claim durability, censorship resistance, broad availability, security, SLSA compliance, or production readiness.

## Loop 50: Bundle import/report command

**Goal:** Let a reviewer inspect a portable bundle or extracted bundle directory without manually reading manifest and evidence JSON.

**Current result:** Complete as `scripts/forge_registry.py report-bundle`. The command reads either `output/decentralized-forge-verification-bundle.zip` or an extracted bundle directory and emits a concise human report, with `--json` for deterministic machine-readable output. The report summarizes file role counts, registry project identity/counts, evidence protocol/state counts, explicit non-claims, verification gaps, and suggested verification commands. Tests assert the ZIP and extracted-directory report paths agree, the manifest lists the report command, and CI runs `report-bundle --json`.

**Gate preserved:** This is local bundle readback and reporting only. It does not publish protocol events, sign events, fetch from relays, pin storage, start daemons, spend money, use wallets, import private keys, replace registry provenance, or claim durability, censorship resistance, broad availability, security, SLSA compliance, or production readiness.

## Loop 51: Portable bundle review checklist

**Goal:** Give maintainers a release-facing checklist for reviewing and describing the portable bundle without overstating evidence.

**Current result:** Complete as `docs/portable-bundle-review-checklist.md`. The checklist defines required local checks, `report-bundle` review expectations, explicit non-claims, attachment metadata, stop conditions, and neutral release-note wording. The checklist is included in the portable verification bundle, referenced from README/community/completion docs, and covered by tests that assert required commands and claim boundaries remain present.

**Gate preserved:** This is local review documentation only. It does not publish protocol events, sign events, fetch from relays, pin storage, start daemons, spend money, use wallets, import private keys, replace registry provenance, or claim durability, censorship resistance, broad availability, security, SLSA compliance, or production readiness.

## Loop 52: Bundle release-note export

**Goal:** Generate a shareable release-facing markdown note from the current bundle report, exact commit SHA, and checklist stop conditions.

**Current result:** Complete as `scripts/forge_registry.py export-bundle-release-note`. The command emits markdown to stdout by default, or writes a file when an output path is supplied. The note includes the current Git commit, bundle SHA-256 and byte size, verification status, project summaries, required commands, non-claims, verification gaps, stop conditions from `docs/portable-bundle-review-checklist.md`, and attachment guidance. It is wired into `verify-local`, CI, npm scripts, README, community quickstart, completion criteria, checklist, tests, and the bundle manifest suggested commands.

**Gate preserved:** This is local readback and markdown export only. It does not publish protocol events, sign events, fetch from relays, pin storage, start daemons, spend money, use wallets, import private keys, replace registry provenance, or claim durability, censorship resistance, broad availability, security, SLSA compliance, or production readiness.

## Loop 53: Local registry import scaffold

**Goal:** Let a maintainer create a valid starter registry fixture from a local Git repository without hand-authoring every required field.

**Current result:** Complete as `scripts/forge_registry.py scaffold-registry <repo> <output>`. The command reads local Git worktree metadata only, writes a valid unsigned local registry fixture with placeholder maintainer identity, file-based clone URL, empty collaboration/release sections, absent IPFS/provenance claims, and a local import verification state. It validates the output immediately and prints next-step guidance. Tests create a temporary Git repository and assert the scaffold is valid and non-claim bounded. `npm run scaffold:registry -- <repo> <output>` exposes the workflow through package scripts.

**Gate preserved:** This is local Git metadata readback and fixture writing only. It does not publish protocol events, sign events, fetch from remotes, pin storage, start daemons, spend money, use wallets, import private keys, replace registry provenance, or claim durability, censorship resistance, broad availability, security, SLSA compliance, or production readiness.

## Loop 54: Local artifact metadata attach

**Goal:** Let a maintainer update a scaffolded registry with local artifact metadata without hand-authoring release hashes or implying live storage/signing evidence.

**Current result:** Complete as `scripts/forge_registry.py attach-local-artifact <registry> <artifact>`. The command reads exact local file bytes, records raw SHA-256, byte size, media type, `file://` URI, local-only availability, unsigned metadata, and a `registry.local_artifact_metadata` verification state, then validates the registry. It is idempotent for the same release/tag/artifact name. Tests scaffold a temporary registry, attach a CRLF-containing artifact, validate the output, assert raw-byte hash/size/media-type/URI fields, and assert no unsupported live availability, signing, durability, SLSA, or production claims. `npm run attach:artifact -- <registry> <artifact> --version <version>` exposes the workflow through package scripts.

**Gate preserved:** This is local file byte hashing and fixture writing only. It does not publish protocol events, sign events, fetch from relays or gateways, add/fetch/pin IPFS content, start daemons, spend money, use wallets, import private keys, replace registry provenance, or claim durability, censorship resistance, broad availability, security, SLSA compliance, or production readiness.

## Loop 55: Local project onboarding command

**Goal:** Give maintainers one local command that executes the scaffold, artifact metadata, validation, render, bundle, and report path for an arbitrary local project.

**Current result:** Complete as `scripts/forge_registry.py onboard-local-project <repo> <artifact>`. The command scaffolds a local registry fixture, attaches local artifact metadata, validates the fixture, writes a deterministic summary, renders HTML, refreshes and verifies the portable bundle, and optionally writes a bundle report JSON. Output paths default to repository conventions and can be overridden for dry runs. The bundle collector now includes repository-local `output/*.html` and `output/*.summary.json`. Tests run the full command against a temporary Git repository and binary artifact, then validate the registry, summary, HTML, bundle, report, and non-claim boundaries. `npm run onboard:local-project -- <repo> <artifact> --project-id <id> --version <version>` exposes the workflow through package scripts.

**Gate preserved:** This is local Git metadata readback, local file byte hashing, local rendering, and local bundle/report generation only. It does not publish protocol events, sign events, fetch from relays or gateways, add/fetch/pin IPFS content, start daemons, spend money, use wallets, import private keys, replace registry provenance, or claim durability, censorship resistance, broad availability, security, SLSA compliance, or production readiness.

## Loop 56: Committed onboarding sample

**Goal:** Provide a committed example of the full one-command onboarding path so reviewers can inspect output without supplying their own project.

**Current result:** Complete as `fixtures/onboarding-sample-artifact.txt`, `fixtures/onboarding-sample.registry.json`, `output/onboarding-sample.registry.summary.json`, `output/onboarding-sample.registry.html`, and `output/onboarding-sample.bundle-report.json`. The sample was generated with `onboard-local-project` from this repository and records repo-relative local file URIs, placeholder identity, local-only artifact metadata, and explicit non-claims. `report-bundle --json --output` now writes report files, and CI/`verify-local` regenerate the committed onboarding report after bundle refresh. Tests validate the sample fixture, artifact hash/size/URI, ancestor commit, regenerated HTML/summary/report, bundle contents, workflow wiring, and non-claim boundaries.

**Gate preserved:** This is committed local sample data plus local report generation only. It does not publish protocol events, sign events, fetch from relays or gateways, add/fetch/pin IPFS content, start daemons, spend money, use wallets, import private keys, replace registry provenance, or claim durability, censorship resistance, broad availability, security, SLSA compliance, or production readiness.

## Loop 57: Optional workbench import for onboarding sample

**Goal:** Prove that onboarded registries can be inspected inside the static workbench without changing the default fixture set.

**Current result:** Complete as `output/forge-app-with-onboarding-sample.html`, generated with `render-app --registry fixtures/example-project.registry.json --registry fixtures/portable-lab.registry.json --registry fixtures/onboarding-sample.registry.json`. The default `output/forge-app.html` remains the two-project workbench. CI and `verify-local` regenerate the optional workbench, the bundle includes it through the `output/*.html` rule, and the GitHub attestation subject list includes it. Tests compare regenerated output, inspect embedded app data for exactly demo, portable, and onboarding sample projects, assert the onboarding artifact appears, and keep the no-fetch/no-sign/no-publish checks.

**Gate preserved:** This is static local HTML generation from committed fixture/evidence data only. It does not publish protocol events, sign events, fetch from relays or gateways, add/fetch/pin IPFS content, start daemons, spend money, use wallets, import private keys, replace registry provenance, or claim durability, censorship resistance, broad availability, security, SLSA compliance, or production readiness.

## Loop 58: Workbench project set handoff

**Goal:** Let a reviewer recreate the exact static workbench project set from inside the generated app without reading docs first.

**Current result:** Complete as a Project set screen in `output/forge-app.html` and `output/forge-app-with-onboarding-sample.html`. The app data now embeds `generated_from.output` alongside the registry source paths, and the screen lists those inputs plus a copyable `python scripts/forge_registry.py render-app ... --registry ...` command. Tests compare regenerated workbench outputs, assert the embedded output/registry source paths for the default and onboarding workbenches, and preserve the no-fetch/no-sign/no-publish runtime checks.

**Gate preserved:** This is static local HTML generation from committed fixture/evidence data only. It does not publish protocol events, sign events, fetch from relays or gateways, add/fetch/pin IPFS content, start daemons, spend money, use wallets, import private keys, replace registry provenance, or claim durability, censorship resistance, broad availability, security, SLSA compliance, or production readiness.

## Loop 59: Project-scoped Radicle repository smoke

**Goal:** Move from local prototype polish to the first evidence that this project can exist as a live Radicle repository.

**Current result:** Complete as `scripts/run_radicle_project_repo_smoke.py` plus `evidence/radicle-project-repo-smoke-2026-06-29.json` and `.md`. The script ran in a Linux Docker container with Radicle 1.9.1 installed into a repo-local temp prefix, cloned the current checkout into temporary state, initialized it as public RID `rad:zWGy1Ssjb7tBbwDbdGLqeHCsUqwr`, seeded/synced it from a temporary Radicle profile, cloned it from a separate temporary profile, and verified the cloned commit matched source commit `fd3f1898d81a4b00be9095c62e3c07fc1a792a95`. The live evidence index is now loop 59 and imports the new evidence row.

**Gate preserved:** This is bounded project-scoped Radicle evidence only. It does not keep a persistent seed, use production/private personal keys, spend money, use paid infrastructure, contact specific people, or claim durability, censorship resistance, broad availability, identity trust, security, SLSA compliance, full Radicle compatibility, or production readiness.

## Loop 60: Fresh-state Radicle RID readback

**Goal:** Check whether the Loop 59 project RID can be fetched from fresh Radicle state without relying on the original temporary seed profile.

**Current result:** Complete as `scripts/run_radicle_fresh_readback_check.py` plus `evidence/radicle-fresh-readback-check-2026-06-29.json` and `.md`. The script ran in a Linux Docker container with Radicle 1.9.1, created a brand-new temporary `RAD_HOME`, started a fresh node, cloned `rad:zWGy1Ssjb7tBbwDbdGLqeHCsUqwr` through Radicle's normal network path without `rad node connect` or `--seed`, and verified the cloned commit matched the Loop 59 expected commit `fd3f1898d81a4b00be9095c62e3c07fc1a792a95`. The live evidence index is now loop 60 and imports the new evidence row.

**Gate preserved:** This is one exact fresh-state readback observation. It does not keep a persistent seed, use production/private personal keys, spend money, use paid infrastructure, contact specific people, or claim permanent durability, censorship resistance, global replication, identity trust, security, SLSA compliance, full Radicle compatibility, or production readiness.

## Loop 61: Radicle update continuity check

**Goal:** Determine whether the first project RID can move forward to the current Git commit without the original disposable Loop 59 delegate state.

**Current result:** Complete as `scripts/run_radicle_update_continuity_check.py` plus `evidence/radicle-update-continuity-check-2026-06-29.json` and `.md`. A fresh non-original Radicle identity cloned `rad:zWGy1Ssjb7tBbwDbdGLqeHCsUqwr`, imported current source commit `00404656bcb17ad1aab241fb0ab0dd60487d9699`, pushed `main` to `rad://zWGy1Ssjb7tBbwDbdGLqeHCsUqwr/<fresh-peer-id>`, and synced with public seeds. A separate fresh readback clone still checked out the original delegate branch at `fd3f1898d81a4b00be9095c62e3c07fc1a792a95`, so canonical/default update continuity was not observed.

**Gate preserved:** This is one exact update-continuity observation. It does not reuse the original delegate key, keep persistent seed state, use production/private personal keys, spend money, contact specific people, or claim canonical continuity, permanent durability, censorship resistance, global replication, identity trust, security, SLSA compliance, full Radicle compatibility, or production readiness.

## Loop 62: Retained Radicle maintainer lane

**Goal:** Create or reuse project-scoped retained Radicle maintainer state so the project has a real update lane instead of only disposable RIDs.

**Current result:** Complete as `scripts/run_radicle_retained_delegate_check.py` plus `evidence/radicle-retained-delegate-check-2026-06-29.json` and `.md`. The script keeps reusable Radicle state under gitignored `.tmp/radicle-retained-delegate`, not in the repository or verification bundle. Using that state, RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` published source commit `dfc10b8f029c5eb886db2025dcc06c6490e28504`; a fresh default clone and explicit direct-seed clone both read back the same commit.

**Gate preserved:** This is one retained project-scoped maintainer observation. It does not commit or bundle secret state, keep a persistent public seed service running, use production/private personal keys, spend money, contact specific people, or claim permanent durability, future default public-routing availability, censorship resistance, global replication, identity trust, security, SLSA compliance, full Radicle compatibility, or production readiness.

## Loop 63: Retained Radicle same-RID update

**Goal:** Verify that the retained maintainer lane can advance the same RID to the next committed Git state.

**Current result:** Complete as `scripts/run_radicle_retained_update_check.py` plus `evidence/radicle-retained-update-check-2026-06-29.json` and `.md`. The retained state was copied to host-local WSL storage and the check ran in Ubuntu WSL, not Docker. The same RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` advanced from commit `dfc10b8f029c5eb886db2025dcc06c6490e28504` to commit `f800bae387f33452fdeb79ecf5c795d25f7246ac`; a fresh explicit direct-seed clone read back the updated commit. Default public-routing readback was attempted but not observed.

**Gate preserved:** This is one retained-RID update observation. It does not commit or bundle secret state, keep a persistent public seed service running, use production/private personal keys, spend money, contact specific people, or claim permanent durability, future default public-routing availability, censorship resistance, global replication, identity trust, security, SLSA compliance, full Radicle compatibility, or production readiness.

## Loop 64: Retained RID community direct-seed quickstart

**Goal:** Turn the retained RID update lane into a concrete reader handoff without overstating default routing or durability.

**Current result:** Complete as `docs/radicle-retained-rid-quickstart.md` plus `python scripts/forge_registry.py radicle-retained-quickstart`. The helper reads the committed live evidence index, validates the strongest retained RID readback row available, and prints a direct-seed clone recipe for RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`. `docs/community-quickstart.md`, `docs/portable-bundle-review-checklist.md`, README, tests, and the verification bundle manifest now include the handoff path.

**Gate preserved:** This is read-only documentation and local CLI output. It does not start Radicle nodes, connect to peers, clone, publish, sign, use private keys, expose retained secret state, run a persistent seed, or claim permanent durability, future default public-routing availability, censorship resistance, global replication, identity trust, security, SLSA compliance, full Radicle compatibility, or production readiness.

## Loop 65: Retained RID independent follower-seed readback

**Goal:** Move closer to a usable product by proving the retained RID can be served by an independent follower seed, not only the retained maintainer seed.

**Current result:** Complete as `scripts/run_radicle_independent_availability_check.py` plus `evidence/radicle-independent-availability-check-2026-06-29.json` and `.md`. The check ran in Ubuntu WSL using WSL-local retained maintainer state and temporary `/tmp` reader states. The same retained RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` advanced from prior verified commit `f800bae387f33452fdeb79ecf5c795d25f7246ac` to current commit `7262f69b82e442263d6261414f6b771be04c6b6f`; reader A cloned from the retained maintainer seed, reader A seeded the RID from its own temporary profile, and reader B cloned/read back the same commit from reader A. `docs/radicle-persistent-seed-plan.md` records the minimum service plan for a future persistent seed.

**Gate preserved:** This is one retained-RID independent follower-seed readback observation. It does not commit or bundle secret state, keep a persistent public seed service running, use production/private personal keys, spend money, contact specific people, or claim permanent durability, future default public-routing availability, censorship resistance, global replication, identity trust, security, SLSA compliance, full Radicle compatibility, or production readiness.

## Loop 66: Retained seed restart/readback rehearsal

**Goal:** Move closer to a usable retained Radicle repo by proving the retained seed can stop, restart on the same local address, and still serve the current retained RID to fresh readers.

**Current result:** Complete as `scripts/run_radicle_seed_restart_check.py` plus `evidence/radicle-seed-restart-check-2026-06-29.json` and `.md`. The check ran in Ubuntu WSL using WSL-local retained maintainer state and temporary `/tmp` reader states. The same retained RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` advanced from prior verified commit `7262f69b82e442263d6261414f6b771be04c6b6f` to current commit `4c8cd6183e2e12d1c62af7d2f013fb085b2d6bf8`; one fresh reader cloned from the retained seed before restart, the retained seed stopped and restarted on `127.0.0.1:8799` with the same node ID, and another fresh reader cloned/read back the same commit after restart. The retained quickstart helper now prefers the Loop 66 row when present.

**Gate preserved:** This is one local retained-seed restart/readback rehearsal. It does not publish a stable public seed address, prove separate-network reachability, leave a persistent public seed service running, commit or bundle secret state, use production/private personal keys, spend money, contact specific people, or claim permanent durability, future default public-routing availability, censorship resistance, global replication, identity trust, security, SLSA compliance, full Radicle compatibility, or production readiness.

## Loop 67: Public VPS follower-seed readback

**Goal:** Move from local restartability to a usable public direct-seed path for the retained Radicle RID.

**Current result:** Complete as `evidence/radicle-vps-follower-public-readback-2026-06-29.json` and `.md`. The `openclaw` VPS runs a fresh follower Radicle identity, not the retained maintainer identity, at `z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776`. A fresh reader on `ubuntu-work` connected to that public seed address, cloned retained RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`, and verified `HEAD` matched commit `610fc3da9757d0cb123aa5976db552b991b766d4`. The retained quickstart helper now prefers the Loop 67 row and prints the public VPS seed address.

**Gate preserved:** This is one public direct-seed readback through a VPS follower seed. It does not copy retained maintainer key material to the VPS, commit or bundle secret state, use production/private personal keys, spend money beyond the already-available VPS, contact specific people, or claim permanent durability, future default public-routing availability, censorship resistance, global replication, identity trust, security, SLSA compliance, full Radicle compatibility, or production readiness.

## Loop 68: Public VPS follower seed service hardening

**Goal:** Move the public follower seed from a hand-started process to a restart-safe service.

**Current result:** Complete as `evidence/radicle-vps-follower-systemd-service-2026-06-29.json` and `.md`. `openclaw` runs `decentralized-forge-radicle-seed.service` as an enabled user-level `systemd` service with `Restart=always`, user lingering enabled, and `radicle-node --listen 0.0.0.0:8776 --force`. The VPS stores follower seed state and a private local passphrase EnvironmentFile; retained maintainer key material was not copied to the VPS. After an explicit service restart, a fresh `ubuntu-work` reader cloned the retained RID from the public seed and verified commit `610fc3da9757d0cb123aa5976db552b991b766d4`.

**Gate preserved:** This proves restart-safe user-service operation plus post-restart direct-seed readback. It does not prove permanent durability, security, identity trust, censorship resistance, global replication, default public routing, or production readiness.

## Loop 69: Public seed health check

**Goal:** Make the public Radicle seed check a repeatable command.

**Current result:** Complete as `scripts/check_public_radicle_seed.py`, `evidence/radicle-public-seed-health-check-2026-06-29.json`, and `.md`. The script creates a fresh temporary Radicle profile, connects to one explicit seed, clones one RID, checks `git rev-parse HEAD`, stops the reader node, and removes temporary state by default. The first run from `ubuntu-work` cloned the retained RID from the public `openclaw` seed and verified commit `610fc3da9757d0cb123aa5976db552b991b766d4`.

**Gate preserved:** This is a point-in-time health check, not a durability, automatic update, security, identity-trust, default-routing, or production-readiness claim.

## Loop 70: Public seed update propagation

**Goal:** Prove the public follower seed can serve an updated retained RID commit, not just a one-time snapshot.

**Current result:** Complete as `evidence/radicle-public-seed-update-propagation-2026-06-29.json` and `.md`. The retained RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` advanced from `610fc3da9757d0cb123aa5976db552b991b766d4` to `64efbada294d4a57c014a27398b92e344c6d68aa`. The `openclaw` follower synced the update through a temporary bridge to the retained maintainer seed, then the bridge and maintainer seed were stopped. A fresh reader on `ubuntu-work` connected to the public VPS seed and cloned the updated commit.

**Gate preserved:** This proves one manual update propagation through the public follower seed. It does not prove automatic future propagation, permanent durability, security, identity trust, global replication, default public routing, or production readiness.

## Loop 71: External public seed health timer

**Goal:** Make public seed health visible from outside the VPS without manual checks.

**Current result:** Complete as `scripts/install_radicle_health_timer.py`, `evidence/radicle-external-health-timer-2026-06-29.json`, and `.md`. `ubuntu-work` runs `decentralized-forge-radicle-healthcheck.timer` as an enabled user-level `systemd` timer that invokes `scripts/check_public_radicle_seed.py` against the `openclaw` seed every 15 minutes after boot. The first forced run wrote `~/.local/state/decentralized-forge/radicle-health/latest.json` and verified commit `ef16e2ad39d3e13bdcc9d454443c5bbb17733c68`.

**Gate preserved:** This is external monitoring evidence. It does not prove automatic repair, permanent durability, security, identity trust, global replication, default public routing, or production readiness.

## Loop 72: Public seed update to hardening commit

**Goal:** Move the public Radicle seed forward to include the prior public-seed hardening commit.

**Current result:** Complete as `evidence/radicle-public-seed-update-ef16e2a-2026-06-29.json` and `.md`. The retained RID advanced from `64efbada294d4a57c014a27398b92e344c6d68aa` to `ef16e2ad39d3e13bdcc9d454443c5bbb17733c68`; `openclaw` synced through a temporary maintainer bridge; the bridge and maintainer seed were stopped; and a fresh reader on `ubuntu-work` cloned the updated commit from the public VPS seed.

**Gate preserved:** This proves one manual update propagation to the hardening commit. It does not prove automatic future propagation, permanent durability, security, identity trust, global replication, default public routing, or production readiness.

## Loop 73: Second follower seed staging

**Goal:** Add a second always-on follower seed process/state store without copying retained maintainer key material.

**Current result:** Complete as `scripts/bootstrap_radicle_follower_seed.py`, `evidence/radicle-ubuntu-work-follower-bootstrap-2026-06-29.json`, and `evidence/radicle-second-seed-tailnet-health-2026-06-29.json`. `ubuntu-work` bootstrapped a separate follower identity `z6MksRdjzuN2VYV4HTXdVSchitJ8Bq1zbx8WhBb3KhyfSm6A`, installed it as an enabled user-level `systemd` service on `100.83.206.66:8877`, and `openclaw` cloned/read back the retained RID over Tailnet at commit `ef16e2ad39d3e13bdcc9d454443c5bbb17733c68`.

**Gate preserved:** This proves a second persistent follower seed with separate state reachable over Tailnet. It does not prove a second public internet seed, durability, security, identity trust, default public routing, or production readiness. Opening an `openclaw` public relay on port `8877` requires explicit approval because it changes the VPS public network surface.

## Loop 74: Second public seed readback

**Goal:** Promote the staged `ubuntu-work` follower seed into a second public direct-seed address after explicit approval.

**Current result:** Complete as `evidence/radicle-second-public-seed-health-2026-06-29.json`. `openclaw` runs `decentralized-forge-radicle-mirror-public-relay.service`, listening on public TCP `8877` and relaying to `ubuntu-work` Tailnet `100.83.206.66:8877`. Public TCP `187.77.19.162:8877` was reachable from Windows and `ubuntu-work`; a fresh `ubuntu-work` reader connected to `z6MksRdjzuN2VYV4HTXdVSchitJ8Bq1zbx8WhBb3KhyfSm6A@187.77.19.162:8877`, cloned retained RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`, and verified HEAD `ef16e2ad39d3e13bdcc9d454443c5bbb17733c68`.

**Gate preserved:** This proves a second public direct-seed address for the retained RID. It does not prove permanent durability, default public routing, automatic future propagation, independent provider/network availability, security, identity trust, or production readiness.
