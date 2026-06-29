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

Loops 1–21 are complete. Loop 4 (Radicle local integration spike) is complete as a **source-inspected local artifact**, not a live Radicle CLI run. Loop 5 is complete as **dry-run Nostr collaboration fixtures**, not a live Nostr relay run. Loop 6 is complete as **local/free artifact metadata with a stdlib-verified CIDv1 raw/base32-compatible fixture**, not live IPFS pinning or durable storage. Loop 7 is complete as **synthetic local CI/provenance fixtures**, not real CI execution, signing, Sigstore/cosign/in-toto verification, Rekor upload, or SLSA compliance. Loop 8 is complete as a **local static renderer/UI improvement**, not public CI/status publication or new infrastructure. Loop 9 is complete as a **public GitHub collaboration surface**, with roadmap/docs and bounded public issues. Loop 10 is complete as **architecture/roadmap/decision matrix cleanup**, not new live protocol verification. Loop 11 is complete as a **local stdlib NIP-34 parser/conformance adapter**, not event signing, event-id computation, relay publishing, or live relay readback. Loop 12 is complete as a **local NIP-34 renderer/import surface**, not relay publishing, relay fetching, signing, event-id computation, or live protocol verification. Loop 13 is complete as a **local NIP-34 repository state/status fixture follow-up**, not a live Nostr or Radicle run. Loop 14 is complete as **local NIP-01/NIP-34 conformance metadata**, not signing, fixture ID replacement, relay publishing, or live verification. Loop 15 is complete as **local static rendering of conformance metadata**, not signing, fixture ID replacement, relay publishing, or live verification. Loop 16 is complete as **local verification-state label schema/fixture cleanup**, not live protocol verification or publishing. Loop 17 is complete as **local NIP-34 adapter verification-state vocabulary alignment**, not relay publishing, signing, or live protocol verification. Loop 18 is complete as **local static verification-state renderer summaries/grouping**, not live protocol verification or publishing. Loop 19 is complete as **local static artifact preflight and public usage polish**, not hosting, signing, relay publishing, paid screenshot tooling, or live protocol verification.

Public GitHub repo is live at `https://github.com/redclawanon-rgb/decentralized-forge`. Verified public settings: default branch `main`, Issues enabled, Discussions enabled, Wiki disabled. Public building is approved; keep project updates accurate and labeled as research/prototype work.

Loop 20 is complete as **safe live-gated adapter replay planning only**. Safe discovery `command -v rad` found no `rad` executable on `PATH`, so `rad --version` and any Radicle local replay were not run. Outputs are `docs/live-adapter-replay-plan.md`, `fixtures/live-adapter-replay-checklist.json`, and checklist tests. No unsafe installer, Radicle CLI action, Nostr key generation, signing, relay publishing/readback, public status event, spending, production/private key use, direct outreach, or live protocol verification occurred.

Loop 21 is complete as **approved prerequisite-only tooling/key setup**. User-local Radicle binaries (`rad`, `radicle-node`, `git-remote-rad`) are installed under `~/.local/bin` at version 1.9.1, and `nak` is installed at version v0.20.0. A disposable/project-scoped Nostr secret key exists outside the repo at `~/.hermes/keys/decentralized-forge/nostr-project.nsec` with `0600` permissions; only public identifiers are recorded in repo docs. Public key: `npub1ve55y0h8dkw44hyws80hj2rvy457m0j6hp8nudgy8km354807hyqp97suy` / `6669423ee76d9d5adc8e81df79286c2569edbe5ab84f3e35043db71a54eff5c8`. Offline proof event `evidence/nostr-offline-key-proof-2026-06-22.json` verifies locally and was not published. No Radicle replay, Radicle node start, Nostr relay publishing/readback, seed publishing, paid infrastructure, production/private personal key use, direct outreach, or live protocol verification occurred.

Loop 22 is complete as **read-only Radicle CLI help/version preflight**. Evidence is `evidence/radicle-local-replay-preflight-2026-06-22.md`. Verified `command -v rad` (`/home/openclaw/.local/bin/rad`), `rad --version` (`rad 1.9.1 (5bd3569e120a6172d9df68e1d1d0eed15e8104b1)`), and selected help output for `rad init`, `rad inspect`, `rad auth`, `rad self`, `rad id`, `rad node`, and `rad path`; `rad status` is not available in this version. Safe Loop 23 path is temporary `RAD_HOME`, disposable Git repo, disposable auth only if required, `rad init --no-confirm --no-seed --private`, and local `rad inspect` commands. No `rad auth`, `rad init`, temporary Radicle state, node start, publish/seed/sync/announce, peer/remote configuration, spending, production/private personal keys, public Radicle network verification, or Nostr publication occurred.

Loop 23 is complete as **local CLI verification of temporary private Radicle repo init/inspect only**. Evidence is `evidence/radicle-local-replay-2026-06-22.md`. Under Permission A, temporary `RAD_HOME` and a disposable Git repo were used; `rad auth --stdin` succeeded with a disposable passphrase that was not logged; `rad init --private --no-confirm --no-seed` created local RID `rad:z33oByNZxkxXAChhD54B4XiSsQkao`; `rad inspect --rid/--identity/--refs/--visibility` succeeded and visibility was `private`; temporary state was removed. No `rad node start`, `rad publish`, sync, announce, public seed publication, peer/remote configuration, public network replication verification, spending, paid infrastructure, production/private personal identity import, durability/censorship-resistance/security/production-readiness claim, or Nostr publication occurred.

Loop 25 is complete as **selected public Nostr relay acceptance/readback for one prototype-labeled disposable-key event**. Evidence is `evidence/nostr-loop25-publish-readback-2026-06-22.md` and `evidence/nostr-loop25-publish-readback-2026-06-22.json`. Event `4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba` (kind `30617`) was published to and read back from `wss://relay.damus.io` and `wss://nos.lol`; local/readback `nak verify` passed. This proves only selected-relay acceptance/readback of the exact prototype event, not durability, global propagation, censorship resistance, identity trust, production readiness, security guarantees, or full NIP-34/forge compatibility.

Loop 26 is complete as **bounded live/local evidence import into fixtures/renderer**. Evidence/index is `fixtures/live-evidence-index.json`; renderer support is `scripts/render_project_page.py --live-evidence-index`; static preflight now includes this index and `output/demo-project.html` was regenerated. It imports Loop 23 Radicle as `local-cli-verified` only and Loop 25 Nostr as `selected-relay-readback-verified` only. No new live network action, Nostr publish/readback, Radicle node/seed/sync/publish/remote clone, spending, production/private personal key use, direct outreach, or unsupported durability/global-propagation/censorship-resistance/security/production-readiness/full-compatibility claim occurred.

Loop 27 is complete as a **prototype/research-labeled public project-channel update**. Draft is `docs/public-update-drafts/2026-06-22-live-adapter-evidence-update.md`; posted discussion is https://github.com/redclawanon-rgb/decentralized-forge/discussions/6. The update keeps claims narrow: Radicle local CLI/private replay only and Nostr selected-relay acceptance/readback only. No direct outreach, spending, paid infrastructure, production/private personal key use, Radicle public-network action, paid storage/wallet action, or unsupported durability/global-propagation/censorship-resistance/security/production-readiness/full-compatibility claim occurred.

Loop 29 is complete as **selected-relay NIP-34 live-event adapter import; no new Nostr publish/fetch/signing**. Evidence fixture is `fixtures/nostr-live-readback-events.json`; adapter/renderer/preflight/tests/output import the recorded Loop 25 kind `30617` event as selected-relay readback evidence only and keep dry-run fixture rows separate. This does not verify durability, global propagation, censorship resistance, identity trust, security, production readiness, full NIP-34/forge compatibility, issue/patch readback, repository-state readback, status semantics, relay discovery, subscription behavior, deletion/replacement behavior, or multi-client behavior.

Loop 30 is complete as **Permission-F Radicle public-network preflight only; Permission G remains blocked**. Evidence is `evidence/radicle-public-network-preflight-2026-06-22.md`; plan is `docs/radicle-public-network-gate-plan.md`. Help-only inspection covered Radicle publish/seed/sync/node/remote/clone surfaces and found the later public smoke boundaries: `rad publish` makes a repo public/discoverable, `rad sync` defaults to fetch+announce, `rad remote add` defaults may fetch/sync, `rad clone` uses local node routing or explicit seeds, and `rad fetch` is not a known command in Radicle 1.9.1. No `RAD_HOME` was created, no identity was created/reused, no node was started, and no publish/seed/sync/announce/clone/fetch/connect/follow/remote configuration occurred.

Loop 28 is complete as **low-volume Nostr readback persistence/divergence evidence; no new publish**. Evidence is `evidence/nostr-loop28-readback-check-2026-06-22.md` and `evidence/nostr-loop28-readback-check-2026-06-22.json`. The Loop 25 event `4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba` was re-read by ID from `wss://relay.damus.io`, `wss://nos.lol`, `wss://relay.primal.net`, and `wss://nostr.wine`; the first three returned the exact event with field matches and `nak verify` passing, while `wss://nostr.wine` did not return it during this check. This is selected/limited relay evidence only, not durability, global propagation, censorship resistance, identity trust, production readiness, security, or full NIP-34/forge compatibility. No new Nostr event was published, no secret key material was read/printed, and no paid/authenticated relay, production/private personal key, direct outreach, or Radicle public-network action occurred.

Loop 31 is complete as **Permission-H public storage/IPFS inventory and plan preflight only**. Evidence is `evidence/storage-tooling-preflight-2026-06-22.md`; plan is `docs/public-storage-evidence-gate-plan.md`. Inventory found no installed `ipfs`, `kubo`, `ipfs-car`, `car`, `ipld`, `cid`, `ipget`, IPFS cluster tools, `go-ipfs`, or Python multiformats/CAR modules. Read-only `npm view` metadata checked local/free candidates (`ipfs-car`, `@ipld/car`, `multiformats`, `helia`, `kubo-rpc-client`) without installing or executing packages. No package install, IPFS daemon start, IPFS add/fetch/pin, CAR creation/import, public gateway check, paid storage, wallet, Filecoin/Arweave action, durability claim, or production-readiness/security/censorship-resistance claim occurred.

Loop 32 is complete as **controller/report consolidation**. `STATUS.md`, `.hermes/context.md`, `AGENT-LOOPS.md`, `docs/next-evidence-and-interoperability-loops.md`, the live-adapter checklist, and tests were updated for Loop 31 completion and remaining gates. No new cron jobs were created.

Loop 33 is complete as **Permission-I local CAR/CID fixture verification with project-scoped lockfile-backed dev dependencies**. Evidence is `evidence/local-car-cid-fixture-2026-06-22.json`; local CAR file is `evidence/local-release-artifact-2026-06-22.car`; verification script is `scripts/verify_car_cid_fixture.mjs`; dependencies are `@ipld/car@5.4.6` and `multiformats@14.0.0` recorded in `package-lock.json`. The local fixture bytes map to SHA-256 `3932e28d5b609b3cae25218ca205ea126cd3cf344628dc4c4b9bf094c50668a0` and CID `bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua`; CAR root/block/readback checks passed. No IPFS daemon, IPFS add/fetch/pin, public gateway query, wallet, paid storage, Filecoin/Arweave action, durability/global-availability/censorship-resistance/security/production claim occurred.

Loop 34 is complete as **Permission-G disposable public Radicle seed/remote-clone smoke**. Evidence is `evidence/radicle-public-network-smoke-2026-06-22.json` and report `evidence/radicle-public-network-smoke-2026-06-22.md`. Disposable RID `rad:z2WtozFrCRhygh9CGzyUN57CN7Nwa` was initialized public from temporary `/tmp` state, node start/seed/sync succeeded, a separate temporary Radicle profile/node connected to the disposable seed over localhost, `rad clone --seed <disposable NID>` succeeded, and README readback matched. Temporary state was removed and nodes stopped. This proves only the exact bounded disposable smoke; it does not prove durable availability, censorship resistance, global replication, identity trust, security, production readiness, full Radicle compatibility, or broad network availability.

Loop 35 is complete as **docs/context/status/checklist/test consolidation; no new live action**. Evidence is `evidence/loop35-consolidation-2026-06-22.md`; checklist state is `fixtures/live-adapter-replay-checklist.json` at loop `35`; tests assert the consolidation state. No new public protocol action, storage action, gateway check, pinning, wallet, spending, paid infrastructure, production/private personal key use, direct outreach, public update, or cron job occurred. Further live storage, repeated/broader Radicle public-network testing, public updates about Loops 33–34, or stronger durability/censorship/security/production claims require a new explicit approval/target.

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

Nostr caveat: no local relay/client tool (`nak`, `nostril`, `strfry`, or `nostr-rs-relay`) was installed or immediately usable, so Loop 5 used dry-run fixtures only. Loop 11 added `scripts/nip34_adapter.py` to parse those fixtures locally and round-trip them to registry-shaped concepts while preserving dry-run notices, placeholder IDs/signatures, relay fallback state, synthetic key policy, NIP-35 boundary, and `published: false`. Loop 12 wires that adapter into `scripts/render_project_page.py` with optional paired fixture arguments and regenerates `output/demo-project.html` with a clearly labeled **NIP-34 fixture adapter** section. Loop 13 adds `fixtures/nostr-repo-state-status.json`, a local-only `kind: 30618` repository state fixture generated from recorded local Git commit `32f88a7a42498328a515e4763e28d84216420a98` at fixture creation time plus fixture-only status/check projections from existing synthetic CI names; later commits may make that recorded SHA an ancestor rather than current `HEAD`. Loop 14 adds local NIP-01 shape/conformance reports and possible reference event IDs under `dry_run.conformance`, while keeping `event_id_computed: false`, `signed: false`, and fixture IDs/signatures unchanged. Loop 15 renders those conformance reports in static HTML as a concise local-only summary without dumping full serialized payloads by default. Loop 17 makes the adapter export `verification_states[]`-compatible rows for imported fixture evidence and renders them separately from top-level registry verification states; all current adapter rows are non-live/synthetic/local or source-inspected mapping evidence. Loop 18 adds static summaries/grouping for both registry and adapter verification states, including zero live-verified counts for current fixtures, state chips, grouped rows, and claim-boundary summaries. No public relay post, relay fetch, private key, production key, event signing, fixture ID replacement, live relay readback, public CI/status event creation, or unsafe installer was used. The synthetic issue (`kind: 1621`), patch (`kind: 1617`), and repository state (`kind: 30618`) events have placeholder IDs/signatures and repeated-hex pubkeys.

Radicle caveat: `rad` was unavailable in the environment, and the documented `curl https://radicle.dev/install | sh` installer was not used. The mapping was derived from official source/manpage/examples in `/tmp/radicle-heartwood` at commit `90aaec1c9eee77a0beebece48f460c1424c1c8bd`. Do not claim live Radicle verification until an approved binary/install path is available and a temporary local `RAD_HOME` replay has been run.

Loop 9 outputs:

- `ROADMAP.md`
- `docs/public-collaboration.md`
- bounded public GitHub issues for renderer UX, Nostr fixtures, Radicle verification, artifact state model, and provenance evolution (#1–#5): https://github.com/redclawanon-rgb/decentralized-forge/issues

Loop 9 caveat: public GitHub issues are temporary coordination scaffolding while decentralized collaboration remains fixture-backed. No direct contact with specific people, paid services, production/private keys, live protocol verification claims, or unsupported security/SLSA/production/censorship-proof claims were used.

Loop 11 outputs:

- `scripts/nip34_adapter.py`
- expanded NIP-34 adapter round-trip tests in `tests/test_registry_fixture.py`
- updated `docs/nip34-event-shapes.md`, README, status, context, and loop notes for local parser behavior and non-claims

Loop 12 outputs:

- optional NIP-34 fixture args in `scripts/render_project_page.py`
- regenerated `output/demo-project.html` with the local NIP-34 fixture adapter section
- renderer tests for adapter import display, boundary labels, dry-run placeholders, and paired-argument enforcement

Loop 13 outputs:

- `fixtures/nostr-repo-state-status.json`
- `scripts/nip34_adapter.py` parsing/export support for repository state and fixture-only status/check projections
- `scripts/render_project_page.py` display support for repository state/status fields in the local NIP-34 adapter section
- regenerated `output/demo-project.html`
- tests for current Git HEAD mapping and dry-run non-claim preservation

Loop 14 outputs:

- NIP-01 event shape helpers in `scripts/nip34_adapter.py`
- `dry_run.conformance.reports[]` exported for repository announcement, issue, patch, and repository state fixtures
- tests for placeholder id/signature reporting, local possible event ID references, and invalid tag/content rejection

Loop 15 outputs:

- `scripts/render_project_page.py` conformance summary rendering for `dry_run.conformance.reports[]`
- regenerated `output/demo-project.html` with report/known-kind counts, placeholder flags, signed/published false fields, and possible-event-ID local reference labels
- renderer tests for conformance summary, boundary wording, possible-event-ID values, and omission of full serialized payload dumps

Loop 16 outputs:

- optional top-level `verification_states[]` schema records for compact scope/state/evidence/live/synthetic/claim-boundary labels
- populated verification-state rows in both registry fixtures for renderer, NIP-34, Radicle, artifact/IPFS, and CI/provenance scopes as applicable
- `scripts/render_project_page.py` **Verification states** section
- tests that assert explicit non-overclaiming states and no `live_verified: true` for unverified protocol scopes

Loop 17 outputs:

- `scripts/nip34_adapter.py` adapter-local `verification_states[]` rows for repository announcement, collaboration events, conformance reports, repository state, and synthetic status/check projections
- `scripts/render_project_page.py` display of adapter verification-state rows separate from registry-level verification states
- regenerated `output/demo-project.html` with all optional local NIP-34 fixtures and adapter verification-state labels
- tests for adapter verification states, non-live/synthetic/local values, renderer display, and unsupported-claim absence

Loop 18 outputs:

- `scripts/render_project_page.py` verification-state summaries for registry and adapter rows
- regenerated `output/demo-project.html` with row counts, live/synthetic counts, state chips, grouped rows by state, and claim-boundary summaries
- tests for registry and adapter summaries with current live-verified counts remaining zero

Loop 19 outputs:

- `scripts/preflight_static_artifact.py` stdlib preflight for generated static artifact freshness, required boundary sections, optional NIP-34 fixture sections, and selected unsupported claim phrases
- README usage instructions for regenerating, opening, preflighting, and fully verifying `output/demo-project.html`
- regenerated `output/demo-project.html` with all optional local NIP-34 fixtures
- tests for preflight pass/fail behavior and CLI command

Loop 20 outputs:

- `docs/live-adapter-replay-plan.md` with Radicle temporary-`RAD_HOME` replay prerequisites, Nostr disposable-key relay checklist, evidence capture, rollback, promotion criteria, and hard non-claim gates
- `fixtures/live-adapter-replay-checklist.json` secret-free machine-readable checklist recording `rad` unavailable and live actions not executed
- tests for the checklist's non-live/secret-free gate state

## Current next recommended loop

Loops 33–57 are complete. The latest default product surface is `output/forge-app.html`, generated by `scripts/render_forge_app.py` and `scripts/forge_registry.py render-app`. It is a local static workbench over committed registry fixtures, evidence-index rows, selected-relay Nostr issue/patch readback evidence, and unsigned local Nostr issue/patch drafts. Loop 48 adds `output/decentralized-forge-verification-bundle.zip`, generated by `scripts/forge_registry.py export-bundle` and checked by `verify-bundle`; the bundle carries schemas, fixtures, source evidence, generated HTML/summaries, the workbench app, verifier scripts, and `verification-bundle.manifest.json`. Loop 49 adds `verify-bundle-cleanroom`, which extracts the bundle to a temporary tree and runs bundled checks without relying on the original checkout. Loop 50 adds `report-bundle`, which reads the ZIP or an extracted bundle directory and summarizes project identity, evidence rows, non-claims, verification gaps, and suggested commands. Loop 51 adds `docs/portable-bundle-review-checklist.md`, which gives maintainers required checks, report review, non-claims, attachment metadata, stop conditions, and neutral release-note wording. Loop 52 adds `export-bundle-release-note`, which emits shareable markdown with the current commit SHA, bundle digest, report summary, non-claims, gaps, and checklist stop conditions. Loop 53 adds `scaffold-registry`, which creates a valid unsigned local registry fixture from a local Git worktree with placeholder identity and non-claim guidance. Loop 54 adds `attach-local-artifact`, which records raw local file SHA-256, size, media type, `file://` URI, local-only availability, and a local artifact verification state without IPFS add/fetch/pin or signing. Loop 55 adds `onboard-local-project`, which chains scaffold, artifact attach, validation, summary export, HTML render, bundle refresh/verification, and optional report JSON export for arbitrary local projects. Loop 56 adds a committed onboarding sample fixture, artifact, summary, page, and bundle report generated through that path. Loop 57 adds `output/forge-app-with-onboarding-sample.html`, an optional static workbench generated with explicit `render-app --registry` arguments for demo, portable, and onboarding sample registries. Neither the app nor bundle fetches, opens WebSockets, signs, publishes, imports private keys, hosts a service, or claims production readiness.

**Next:** Add an in-workbench project import/export panel that reads embedded registry source paths and shows a copyable `render-app --registry ...` command for recreating the current project set, keeping it static and non-publishing. The still-blocked parallel lane is locating an approved `rad` CLI on this Windows host for broader disposable Radicle clone/sync checks.

Current override after Loop 58: The in-workbench project import/export panel is complete as the Project set screen in `output/forge-app.html` and `output/forge-app-with-onboarding-sample.html`. `scripts/render_forge_app.py` embeds `generated_from.output` plus registry source paths and renders a copyable recreate command. The next loop is a static bundle handoff screen or section that summarizes the committed verification bundle/report commands from inside the workbench, while keeping all no-fetch/no-WebSocket/no-sign/no-publish/no-production-readiness boundaries.

Current override after Loop 59: The first project-scoped Radicle repository smoke is complete. `scripts/run_radicle_project_repo_smoke.py` ran in a Linux Docker container with Radicle 1.9.1 from a repo-local temp prefix, initialized the current checkout as public RID `rad:zWGy1Ssjb7tBbwDbdGLqeHCsUqwr`, seeded/synced it from temporary state, cloned it from a separate temporary Radicle profile, and verified clone commit `fd3f1898d81a4b00be9095c62e3c07fc1a792a95` matched the source commit. Evidence is `evidence/radicle-project-repo-smoke-2026-06-29.json` and `.md`; `fixtures/live-evidence-index.json` is now loop 59. Next useful work is either a fresh-container readback of that RID without the original temporary seed profile, or a workbench summary that foregrounds this RID and its exact non-claims. Do not claim durable availability, broad replication, identity trust, security, full Radicle compatibility, or production readiness.

Current override after Loop 60: Fresh-state Radicle readback is complete. `scripts/run_radicle_fresh_readback_check.py` ran in Docker/Linux with Radicle 1.9.1, created a new temporary `RAD_HOME`, started a fresh node, and cloned `rad:zWGy1Ssjb7tBbwDbdGLqeHCsUqwr` at commit `fd3f1898d81a4b00be9095c62e3c07fc1a792a95` without reusing the original Loop 59 seed profile or explicitly using `rad node connect`/`--seed`. Evidence is `evidence/radicle-fresh-readback-check-2026-06-29.json` and `.md`; `fixtures/live-evidence-index.json` is now loop 60. Next useful work is update continuity: publish or document a way to move the current post-Loop-60 Git commit forward on the same Radicle RID where possible. Do not claim permanent durability, broad replication, identity trust, security, full Radicle compatibility, or production readiness.

Current override after Loop 61: Radicle update continuity check is complete. `scripts/run_radicle_update_continuity_check.py` showed a fresh non-original identity could push current commit `00404656bcb17ad1aab241fb0ab0dd60487d9699` to `rad:zWGy1Ssjb7tBbwDbdGLqeHCsUqwr` under its own peer namespace, but a default fresh clone still checked out original delegate commit `fd3f1898d81a4b00be9095c62e3c07fc1a792a95`. Evidence is `evidence/radicle-update-continuity-check-2026-06-29.json` and `.md`; `fixtures/live-evidence-index.json` is now loop 61. Next useful work is a retained project-scoped Radicle delegate/maintainer identity path so default clones can read back current commits. Do not claim canonical continuity, permanent durability, broad replication, identity trust, security, full Radicle compatibility, or production readiness.

Current override after Loop 62: Retained Radicle maintainer lane is complete. `scripts/run_radicle_retained_delegate_check.py` keeps reusable project-scoped Radicle state under gitignored `.tmp/radicle-retained-delegate`, not in the committed repo or bundle. It published retained RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` for commit `dfc10b8f029c5eb886db2025dcc06c6490e28504`; fresh default and explicit direct-seed readbacks both matched that commit. Evidence is `evidence/radicle-retained-delegate-check-2026-06-29.json` and `.md`; `fixtures/live-evidence-index.json` is now loop 62. Next useful work is retained-RID update continuity after this commit lands: rerun the retained delegate script from the new clean commit and verify the same RID advances. Do not claim permanent durability, future default public-routing availability, broad replication, identity trust, security, full Radicle compatibility, or production readiness.

Current override after Loop 63: Retained same-RID Radicle update is complete. `scripts/run_radicle_retained_update_check.py` ran in local Ubuntu WSL using WSL-local retained state, not Docker, after Docker was rejected for exposing secret-bearing retained state. It advanced RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` from commit `dfc10b8f029c5eb886db2025dcc06c6490e28504` to commit `f800bae387f33452fdeb79ecf5c795d25f7246ac`; fresh explicit direct-seed readback matched the updated commit. Default public-routing readback was attempted but not observed. Evidence is `evidence/radicle-retained-update-check-2026-06-29.json` and `.md`; `fixtures/live-evidence-index.json` is now loop 63. Next useful work is a community clone quickstart for the retained RID plus explicit peer/direct-seed path. Do not claim permanent durability, future default public-routing availability, broad replication, identity trust, security, full Radicle compatibility, or production readiness.

Current override after Loop 64: Retained RID community direct-seed quickstart is complete. `docs/radicle-retained-rid-quickstart.md` and `python scripts/forge_registry.py radicle-retained-quickstart` now provide a read-only, evidence-derived maintainer-assisted clone recipe for retained RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` at expected commit `f800bae387f33452fdeb79ecf5c795d25f7246ac`. The helper validates Loop 63 direct-seed readback fields from the committed live evidence index and preserves the caveat that default public-routing readback was not observed. Next useful work is independent availability: either a second independent seed/readback lane or a persistent-seed service plan without turning on unsupported infrastructure. Do not claim permanent durability, future default public-routing availability, broad replication, identity trust, security, full Radicle compatibility, or production readiness.

Current override after Loop 65: Retained RID independent follower-seed readback is complete. `scripts/run_radicle_independent_availability_check.py` ran in Ubuntu WSL using WSL-local retained maintainer state plus temporary reader states. It advanced RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` from `f800bae387f33452fdeb79ecf5c795d25f7246ac` to current commit `7262f69b82e442263d6261414f6b771be04c6b6f`; reader A cloned from the retained maintainer seed, seeded the RID from its own temporary Radicle profile, and reader B cloned/read back the same commit from reader A. Evidence is `evidence/radicle-independent-availability-check-2026-06-29.json` and `.md`; `fixtures/live-evidence-index.json` is now loop 65. `docs/radicle-persistent-seed-plan.md` records the minimum future service plan. Next useful work is a reachable seed pilot or service rehearsal from a separate network context. Do not claim permanent durability, future default public-routing availability, broad replication, identity trust, security, full Radicle compatibility, or production readiness.

Current override after Loop 66: Retained seed restart/readback rehearsal is complete. `scripts/run_radicle_seed_restart_check.py` ran in Ubuntu WSL using WSL-local retained maintainer state plus temporary reader states. It advanced RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` from `7262f69b82e442263d6261414f6b771be04c6b6f` to current commit `4c8cd6183e2e12d1c62af7d2f013fb085b2d6bf8`; one fresh reader cloned from the retained seed before restart, the retained seed stopped and restarted on `127.0.0.1:8799` with the same node ID, and another fresh reader cloned/read back the same commit after restart. Evidence is `evidence/radicle-seed-restart-check-2026-06-29.json` and `.md`; `fixtures/live-evidence-index.json` is now loop 66. The retained quickstart helper now prefers Loop 66. Next useful work is a real reachable seed pilot from a separate network context or host. Do not claim permanent durability, public seed reachability, future default public-routing availability, broad replication, identity trust, security, full Radicle compatibility, or production readiness.

Current override after Loop 67: Public VPS follower-seed readback is complete. `openclaw` runs a fresh follower seed, not retained maintainer state, at `z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776`. A fresh reader on `ubuntu-work` connected to that public seed, cloned retained RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`, and verified commit `610fc3da9757d0cb123aa5976db552b991b766d4`. Evidence is `evidence/radicle-vps-follower-public-readback-2026-06-29.json` and `.md`; `fixtures/live-evidence-index.json` is now loop 67. The retained quickstart helper now prints the real VPS seed address. Next useful work is service hardening for the follower seed: systemd/supervisor restart policy, periodic health check, and repeated readback after a time gap. Do not claim permanent durability, future default public-routing availability, broad replication, identity trust, security, full Radicle compatibility, or production readiness.

Current override after Loop 70: Public Radicle direct-seed MVP is complete for commit `64efbada294d4a57c014a27398b92e344c6d68aa`. `openclaw` runs the follower seed as an enabled user-level `systemd` service at `z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776`; `scripts/check_public_radicle_seed.py` provides a fresh-profile health check; the retained RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` advanced from Loop 67 and was cloned from the public seed after the temporary bridge and maintainer seed were stopped. Evidence is `evidence/radicle-public-seed-update-propagation-2026-06-29.json`; `fixtures/live-evidence-index.json` is now loop 70. Do not claim automatic future propagation, permanent durability, future default public-routing availability, broad replication, identity trust, security, full Radicle compatibility, or production readiness.

Current override after Loop 72: The public Radicle direct-seed path now serves commit `ef16e2ad39d3e13bdcc9d454443c5bbb17733c68`, and `ubuntu-work` runs `decentralized-forge-radicle-healthcheck.timer` as an external scheduled health check. Strongest evidence is `evidence/radicle-public-seed-update-ef16e2a-2026-06-29.json`; live evidence index is loop 72. Do not claim automatic future propagation, automatic repair, permanent durability, future default public-routing availability, broad replication, identity trust, security, full Radicle compatibility, or production readiness.
