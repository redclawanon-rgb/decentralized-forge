# Status

## Current milestone

Milestone 1 — Local registry/static forge prototype and protocol mapping.

## Current loop state

### Loop 1: Research corpus and protocol matrix

Status: **complete**.

Outputs:

- `RESEARCH.md` expanded with source-grounded sections for Radicle, ForgeFed/ActivityPub, Nostr NIP-34/NIP-35, IPFS/IPLD/Filecoin/Arweave, Sigstore/cosign/in-toto/SLSA, AT Protocol/PDS, Hypercore, and Secure Scuttlebutt/git-ssb.
- `PROTOCOL-MATRIX.md` filled with scores and concise justifications.
- `SPEC-FIRST.md` strengthened with Loop 2 and Loop 3 MVP acceptance criteria.
- `ARCHITECTURE.md` strengthened with recommended architecture and open decision points.

### Loop 2: MVP registry object and static repo page prototype

Status: **complete**.

Outputs:

- `schemas/project-registry.schema.json`
- `fixtures/example-project.registry.json`
- `scripts/render_project_page.py`
- `output/demo-project.html`
- `tests/test_registry_fixture.py`

Verified commands:

- `python3 scripts/render_project_page.py fixtures/example-project.registry.json output/demo-project.html` — passed.
- `python3 -m unittest discover -s tests` — passed, 7 tests.

### Loop 3: NIP-34 dry-run docs/fixtures

Status: **complete**.

Outputs:

- `docs/nip34-event-shapes.md`
- `fixtures/nostr-repo-announcement.json`

Verified commands:

- `python3 -m json.tool fixtures/nostr-repo-announcement.json` — passed.
- No public relay publishing performed.

### Loop 4: Radicle local integration spike

Status: **complete as source-inspected local spike; live CLI not installed/verified**.

Outputs:

- `docs/radicle-mapping.md`
- `fixtures/radicle-backed-project.registry.json`
- `tests/test_registry_fixture.py` updated to validate all registry fixtures plus Radicle-specific mapping/verification flags.
- README/context/loop notes updated to record local-only Radicle scope.

Verified commands:

- `python3 -m json.tool fixtures/radicle-backed-project.registry.json` — passed.
- `python3 -m unittest discover -s tests` — passed, 10 tests.

Notes:

- Radicle CLI was not available in this environment.
- The unsafe `curl https://radicle.dev/install | sh` installation path was not used.
- Mapping evidence was inspected from `/tmp/radicle-heartwood` at commit `90aaec1c9eee77a0beebece48f460c1424c1c8bd`.
- No `rad init`, network node, public seed connection, publish action, account creation, private key, or spending occurred.

### Loop 5: Nostr local/dev relay or stronger dry-run issue/patch fixtures

Status: **complete as dry-run collaboration fixtures; local relay/tool not installed/verified**.

Outputs:

- `fixtures/nostr-collaboration-events.json`
- `docs/nip34-event-shapes.md` expanded with Loop 5 local relay check, issue/patch fixture semantics, and NIP-35 boundary.
- `tests/test_registry_fixture.py` updated to validate NIP-34 issue (`kind: 1621`) and patch (`kind: 1617`) dry-run event shapes and NIP-35 non-collaboration boundary.

Verified commands:

- `command -v nak`, `command -v nostril`, `command -v strfry`, and `command -v nostr-rs-relay` — no installed tool found in this environment.
- `python3 -m json.tool fixtures/nostr-collaboration-events.json` — passed.
- `python3 -m unittest discover -s tests` — passed, 12 tests.

Notes:

- No local relay was started because no free/safe relay or Nostr CLI was already installed and usable.
- No unsafe installer, paid service, production/private key, public relay, or public post was used.
- Collaboration events use obvious repeated-hex synthetic pubkeys and non-computed dry-run IDs/signatures only.

### Loop 6: release/artifact metadata and IPFS-CID-compatible local fixture

Status: **complete as local/free artifact metadata fixture; no live IPFS/pinning/durability verification**.

Outputs:

- `schemas/project-registry.schema.json` strengthened with artifact `hashes`, `content_addresses`, and explicit `availability` non-claim flags.
- `fixtures/local-release-artifact.txt` added as the local artifact bytes.
- `fixtures/example-project.registry.json` updated with SHA-256 and CIDv1 raw/base32-compatible metadata computed from the local fixture.
- `fixtures/radicle-backed-project.registry.json` updated with explicit artifact hash/availability flags.
- `docs/artifact-metadata.md`, `docs/nip34-event-shapes.md`, README, and tests updated with boundaries and validation.

Verified commands:

- `python3 -m json.tool schemas/project-registry.schema.json` — passed.
- `python3 -m json.tool fixtures/example-project.registry.json` — passed.
- `python3 -m json.tool fixtures/radicle-backed-project.registry.json` — passed.
- `python3 -m unittest discover -s tests` — passed, 14 tests.

Notes:

- Local fixture SHA-256: `3932e28d5b609b3cae25218ca205ea126cd3cf344628dc4c4b9bf094c50668a0`.
- Local CID-compatible value: `bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua`.
- No IPFS add/fetch/pin, gateway check, paid storage, wallet, Filecoin/Arweave spend, production key, or durability claim occurred.

### Loop 7: CI/provenance model docs and local fake attestation fixtures

Status: **complete as synthetic local CI/provenance fixtures; no real CI, signing, Sigstore, in-toto, Rekor, or SLSA verification**.

Outputs:

- `schemas/project-registry.schema.json` strengthened with optional `ci_checks[]` and artifact `provenance` metadata.
- `fixtures/example-project.registry.json` updated with two `local-fake` CI check records, a fake attestation string, structured artifact provenance, and explicit Sigstore/SLSA non-claim flags.
- `fixtures/radicle-backed-project.registry.json` updated with explicit absent/synthetic Sigstore/SLSA non-claim flags.
- `docs/ci-provenance-model.md` added to document fields and hard boundaries.
- `docs/artifact-metadata.md` updated to point to the provenance attachment and supply-chain trust boundaries.
- `tests/test_registry_fixture.py` updated to validate synthetic-only CI states, coherent artifact hash/commit/repo references, and absence of real signatures/keys/SLSA claims.

Verified commands:

- `python3 -m json.tool schemas/project-registry.schema.json` — passed.
- `python3 -m json.tool fixtures/example-project.registry.json` — passed.
- `python3 -m json.tool fixtures/radicle-backed-project.registry.json` — passed.
- `python3 -m unittest discover -s tests` — passed, 18 tests.

Notes:

- Fake provenance references local artifact SHA-256 `3932e28d5b609b3cae25218ca205ea126cd3cf344628dc4c4b9bf094c50668a0` and synthetic commit `1111111111111111111111111111111111111111`.
- No hosted CI job, public commit status, CI secret/token, real signing key, cosign/Sigstore verification, Rekor upload, in-toto statement verification, SLSA level/compliance claim, paid CI, or public infrastructure was used.

### Loop 8: static UI/renderer improvements

Status: **complete as local static renderer/UI improvement; no public status publication or new infrastructure**.

Outputs:

- `scripts/render_project_page.py` now renders a clearer static page with explicit prototype boundary notice, artifact availability flags, content-address details, provenance/attestation metadata, CI check records, and expanded protocol substrate details.
- `output/demo-project.html` regenerated from `fixtures/example-project.registry.json`.
- `tests/test_registry_fixture.py` updated to assert the new rendered sections/non-claim flags while preserving existing basics.
- README/context updated to describe the renderer output and synthetic CI/provenance caveats.

Verified commands:

- `python3 scripts/render_project_page.py fixtures/example-project.registry.json output/demo-project.html` — passed.
- `python3 -m unittest discover -s tests` — passed, 19 tests.

Notes:

- The renderer remains stdlib-only, static HTML/CSS only, with existing `html.escape`-based escaping paths for fixture-derived values.
- New UI labels explicitly show local-only/synthetic status and non-claims: no public CI status, no live IPFS verification, no paid storage, no durability claim, no real Sigstore/in-toto verification, no Rekor upload, no private key use, and no SLSA level claim.
- No hosted services, paid infrastructure, production/private keys, public posts, or public status publication were used.

### Loop 9: public collaboration surface

Status: **complete as public GitHub collaboration surface; roadmap/docs pushed and public issues verified**.

Outputs:

- `ROADMAP.md` for the public prototype roadmap and collaboration tracks.
- `docs/public-collaboration.md` for public positioning, first issue set, and a concise public update draft.
- Public GitHub issues for bounded collaboration tracks:
  - #1 Renderer UX: clarify fixture vs live-verified states — https://github.com/redclawanon-rgb/decentralized-forge/issues/1
  - #2 Nostr adapter: conformance parser for NIP-34 issue/patch fixtures — https://github.com/redclawanon-rgb/decentralized-forge/issues/2
  - #3 Radicle adapter: safe local CLI verification path — https://github.com/redclawanon-rgb/decentralized-forge/issues/3
  - #4 Artifact metadata: separate local, live CID, pinned, and durable states — https://github.com/redclawanon-rgb/decentralized-forge/issues/4
  - #5 Provenance model: evolve fake attestations toward optional real signing — https://github.com/redclawanon-rgb/decentralized-forge/issues/5

Verified commands:

- `gh issue list --repo redclawanon-rgb/decentralized-forge --state all --limit 20 --json number,title,state,labels,url` — verified issues #1–#5 exist.

Boundaries:

- Use public GitHub issues/discussions only as temporary coordination while decentralized collaboration remains fixture-backed.
- Do not contact specific people directly.
- Do not make unsupported security, SLSA, production-readiness, censorship-proof, live IPFS, or live protocol-verification claims.

### Loop 10: final architecture/roadmap/decision matrix cleanup

Status: **complete as documentation consolidation; no new live protocol verification or public push performed by this subagent**.

Outputs:

- `README.md` now includes a public current-status table separating local fixtures, dry-run/source-inspected mappings, synthetic provenance, and live-unverified protocol support.
- `ARCHITECTURE.md` consolidated the post-Loop-9 architecture, verification-state boundaries, live adapter gates, and next implementation decision matrix.
- `PROTOCOL-MATRIX.md` now includes current repo status per protocol plus a next-step decision matrix and promotion gates.
- `ROADMAP.md` now includes verification-state labels, Loop 10 completion, and recommended next implementation order.
- `docs/public-collaboration.md` now points at the verified public issue set and states that GitHub issues are temporary coordination scaffolding, not decentralized federation evidence.
- `AGENT-LOOPS.md` now records Loop 10 and a bounded Loop 11 recommendation.

Verified commands:

- `python3 -m unittest discover -s tests` — passed, 19 tests.
- `python3 -m json.tool schemas/project-registry.schema.json` — passed.
- `python3 -m json.tool fixtures/example-project.registry.json` — passed.
- `python3 -m json.tool fixtures/radicle-backed-project.registry.json` — passed.
- `python3 -m json.tool fixtures/nostr-repo-announcement.json` — passed.
- `python3 -m json.tool fixtures/nostr-collaboration-events.json` — passed.

Boundaries:

- Loop 10 changed documentation only.
- No spending, production/private keys, public protocol publishing, live Radicle/Nostr/IPFS/ForgeFed/Sigstore verification, or public posts were performed. Local commits/pushes were performed only after parent verification and preflight.

### Loop 11: NIP-34 parser/conformance adapter and fixture round-trip tests

Status: **complete as local stdlib parser/conformance adapter; no relay publishing, keys, signing, or live relay verification**.

Outputs:

- `scripts/nip34_adapter.py` added as a stdlib-only helper for parsing/exporting `fixtures/nostr-repo-announcement.json` and `fixtures/nostr-collaboration-events.json`.
- `tests/test_registry_fixture.py` expanded with round-trip tests for repository id/name/description/web URL, clone URLs, Nostr maintainers, NIP-34 substrate fields, issue and patch title/status/summary/content mappings, and preserved dry-run non-claim fields.
- `docs/nip34-event-shapes.md`, README, `.hermes/context.md`, and `AGENT-LOOPS.md` updated to document adapter behavior and boundaries.

Verified commands:

- `python3 -m unittest discover -s tests` — passed, 22 tests.
- `python3 -m json.tool fixtures/nostr-repo-announcement.json` — passed.
- `python3 -m json.tool fixtures/nostr-collaboration-events.json` — passed.
- `python3 scripts/nip34_adapter.py fixtures/nostr-repo-announcement.json fixtures/nostr-collaboration-events.json` — passed.

Boundaries:

- Adapter is local fixture parsing/export only.
- No relay publishing/readback, key use, event signing, event ID computation, public protocol verification, spending, production/private keys, or unsupported live-protocol/security/durability/SLSA/censorship-proof claims were performed. Local commits/pushes were performed only after parent verification and preflight.

### Loop 12: NIP-34 renderer/import follow-up

Status: **complete as local renderer/import surface; no relay publishing, signing, or live protocol verification**.

Outputs:

- `scripts/render_project_page.py` now accepts paired optional `--nip34-repo-fixture` and `--nip34-collaboration-fixture` arguments.
- The renderer imports the fixture pair through `scripts/nip34_adapter.py` and displays a clearly labeled **NIP-34 fixture adapter** section with repo id/name/kind, relay hints, dry-run publish status, issue/patch counts, imported issue/patch titles/statuses/summaries/source kinds, and dry-run/non-claim JSON fields.
- `output/demo-project.html` regenerated with the optional NIP-34 fixture adapter section.
- `tests/test_registry_fixture.py` expanded with renderer coverage for the adapter section, boundary labels, dry-run placeholders, and paired-argument validation.
- README, `.hermes/context.md`, `AGENT-LOOPS.md`, and `docs/nip34-event-shapes.md` updated for the local renderer/import surface.

Verified commands:

- `python3 -m unittest tests.test_registry_fixture` — passed, 24 tests.
- `python3 scripts/render_project_page.py fixtures/example-project.registry.json output/demo-project.html --nip34-repo-fixture fixtures/nostr-repo-announcement.json --nip34-collaboration-fixture fixtures/nostr-collaboration-events.json` — passed.
- `python3 -m json.tool fixtures/example-project.registry.json` — passed.
- `python3 -m json.tool fixtures/nostr-repo-announcement.json` — passed.
- `python3 -m json.tool fixtures/nostr-collaboration-events.json` — passed.

Boundaries:

- Renderer import/display is local fixture parsing only.
- No relay publishing/readback, relay fetching, key use, event signing, event ID computation, public protocol verification, spending, production/private keys, or unsupported live-protocol/security/durability/SLSA/censorship-proof claims were performed. Local commits/pushes were performed only after parent verification and preflight.

### Loop 13: NIP-34 repository state/status fixture follow-up

Status: **complete as local fixture/parser/renderer follow-up; no relay publishing, signing, public CI status, or live protocol verification**.

Outputs:

- `fixtures/nostr-repo-state-status.json` added with a dry-run NIP-34 repository state event (`kind: 30618`) generated from the local `git rev-parse HEAD` recorded at fixture creation time (`32f88a7a42498328a515e4763e28d84216420a98`). Later commits may make this recorded SHA an ancestor rather than current `HEAD`.
- The same fixture includes fixture-only status/check projections tied to the repository state commit and existing synthetic CI/provenance names; these are not claimed as standardized/live NIP status events.
- `scripts/nip34_adapter.py` now parses/exports repository state HEAD/ref/commit mappings, fixture-only status/check projections, and state/status dry-run non-claim fields.
- `scripts/render_project_page.py` now accepts optional `--nip34-state-status-fixture` alongside the paired repository/collaboration fixtures and displays repository state/status data in the local NIP-34 fixture adapter section.
- `output/demo-project.html` regenerated with the repository state/status fixture display.
- `tests/test_registry_fixture.py` expanded with current Git HEAD mapping and dry-run non-claim preservation tests.
- README, `.hermes/context.md`, `AGENT-LOOPS.md`, and `docs/nip34-event-shapes.md` updated for Loop 13 behavior and boundaries.

Verified commands:

- `git rev-parse HEAD` — returned `32f88a7a42498328a515e4763e28d84216420a98` at fixture creation time and was recorded in the state fixture.
- `python3 -m unittest discover -s tests` — passed, 26 tests.
- `python3 scripts/render_project_page.py fixtures/example-project.registry.json output/demo-project.html --nip34-repo-fixture fixtures/nostr-repo-announcement.json --nip34-collaboration-fixture fixtures/nostr-collaboration-events.json --nip34-state-status-fixture fixtures/nostr-repo-state-status.json` — passed.
- `python3 -m json.tool fixtures/nostr-repo-announcement.json` — passed.
- `python3 -m json.tool fixtures/nostr-collaboration-events.json` — passed.
- `python3 -m json.tool fixtures/nostr-repo-state-status.json` — passed.

Boundaries:

- Repository state/status evidence is local fixture parsing/display only.
- No Radicle CLI was installed or run, because `rad` was unavailable in the parent check.
- No relay publishing/readback, relay fetching, key use, event signing, event ID computation, public CI/status event creation, public protocol verification, spending, production/private keys, or unsupported live-protocol/security/durability/SLSA/censorship-proof claims were performed. Local commits/pushes were performed only after parent verification and preflight.

### Loop 14: NIP-01/NIP-34 conformance metadata for dry-run fixtures

Status: **complete as local conformance metadata; no signing, relay publishing, fixture ID replacement, or live protocol verification**.

Outputs:

- `scripts/nip34_adapter.py` now validates local NIP-01 event shape for dry-run fixtures: required fields, exact non-bool integer `kind`/`created_at`, string `content`, array-of-string `tags`, and fixture pubkey shape.
- The adapter exports `dry_run.conformance.reports[]` for repository announcement (`30617`), issue (`1621`), patch (`1617`), and repository state (`30618`) fixtures.
- Reports preserve placeholder id/signature detection and explicit `event_id_computed: false`, `signed: false`, and `published: false` fields.
- Reports include local-only `serialized_event_payload` and `possible_event_id` references when NIP-01 shape permits; fixture `id`/`sig` values are not replaced.
- `tests/test_registry_fixture.py` covers valid reports, placeholder id/signature metadata, local possible event IDs, and invalid bool integer/tag/content/pubkey rejection.
- README, `.hermes/context.md`, `AGENT-LOOPS.md`, and `docs/nip34-event-shapes.md` updated for Loop 14 behavior and boundaries.

Verified commands:

- `python3 -m unittest discover -s tests` — passed, 31 tests.
- `python3 -m json.tool fixtures/nostr-repo-announcement.json` — passed.
- `python3 -m json.tool fixtures/nostr-collaboration-events.json` — passed.
- `python3 -m json.tool fixtures/nostr-repo-state-status.json` — passed.

Boundaries:

- Conformance reports are local dry-run metadata only.
- NIP-01 possible event IDs are computed references only, not fixture IDs and not proof of signing or relay acceptance.
- No relay publishing/readback, relay fetching, key use, event signing, fixture ID replacement, public CI/status event creation, public protocol verification, spending, production/private keys, or unsupported live-protocol/security/durability/SLSA/censorship-proof claims were performed.

### Loop 15: Render NIP-34 conformance metadata in static HTML

Status: **complete as local renderer metadata display; no signing, relay publishing, fixture ID replacement, or live protocol verification**.

Outputs:

- `scripts/render_project_page.py` now renders `dry_run.conformance.reports[]` from the local NIP-34 adapter as a concise **Local NIP-34 conformance summary**.
- The summary displays report count, known NIP-34 kind count, conformance scope/source, and per-event label, kind, local fixture validity, placeholder id/signature flags, signed/published false fields, and `possible_event_id` labeled as local reference only.
- Full serialized event payloads are not dumped by default in the static HTML.
- `output/demo-project.html` regenerated with all optional NIP-34 fixtures.
- `tests/test_registry_fixture.py` expanded with renderer assertions for conformance summary text, possible-event-ID labels/values, placeholder metadata, local-only boundary wording, and low-noise payload omission.
- README, `.hermes/context.md`, `AGENT-LOOPS.md`, and `docs/nip34-event-shapes.md` updated for Loop 15 behavior and boundaries.

Verified commands:

- `python3 scripts/render_project_page.py fixtures/example-project.registry.json output/demo-project.html --nip34-repo-fixture fixtures/nostr-repo-announcement.json --nip34-collaboration-fixture fixtures/nostr-collaboration-events.json --nip34-state-status-fixture fixtures/nostr-repo-state-status.json` — passed.
- `python3 -m unittest discover -s tests` — passed, 31 tests.
- `python3 -m json.tool fixtures/nostr-repo-announcement.json` — passed.
- `python3 -m json.tool fixtures/nostr-collaboration-events.json` — passed.
- `python3 -m json.tool fixtures/nostr-repo-state-status.json` — passed.

Boundaries:

- Renderer output is local dry-run fixture metadata only.
- NIP-01 possible event IDs are displayed as local references only, not fixture IDs and not proof of signing or relay acceptance.
- No relay publishing/readback, relay fetching, key use, event signing, fixture ID replacement, public CI/status event creation, public protocol verification, spending, production/private keys, or unsupported live-protocol/security/durability/SLSA/censorship-proof claims were performed.

### Loop 16: Verification-state label schema/fixture cleanup

Status: **complete as local schema/fixture/renderer cleanup; no live protocol verification or publishing**.

Outputs:

- `schemas/project-registry.schema.json` now allows optional top-level `verification_states[]` records with explicit `scope`, `state`, `evidence`, `live_verified`, `synthetic`, `claim_boundary`, `last_checked_at`, and `notes` fields.
- `fixtures/example-project.registry.json` and `fixtures/radicle-backed-project.registry.json` now include compact verification-state rows for registry/renderer, NIP-34, Radicle, artifact/IPFS, and CI/provenance scopes as applicable.
- `scripts/render_project_page.py` now renders a **Verification states** section before substrate details.
- `output/demo-project.html` regenerated with all optional local NIP-34 fixtures and the new verification-state section.
- `tests/test_registry_fixture.py` now verifies schema enum coverage, explicit fixture states, no `live_verified: true` for unverified protocol scopes, renderer display, and absence of unsupported claim phrases in verification-state rows.
- README, `.hermes/context.md`, `AGENT-LOOPS.md`, `docs/artifact-metadata.md`, and `docs/ci-provenance-model.md` updated for the new labels and boundaries.

Verified commands:

- `python3 -m json.tool schemas/project-registry.schema.json` — passed.
- `python3 -m json.tool fixtures/example-project.registry.json` — passed.
- `python3 -m json.tool fixtures/radicle-backed-project.registry.json` — passed.
- `python3 scripts/render_project_page.py fixtures/example-project.registry.json output/demo-project.html --nip34-repo-fixture fixtures/nostr-repo-announcement.json --nip34-collaboration-fixture fixtures/nostr-collaboration-events.json --nip34-state-status-fixture fixtures/nostr-repo-state-status.json` — passed.
- `python3 -m unittest discover -s tests` — passed, 34 tests.

Boundaries:

- Verification-state labels are descriptive local metadata only; no row claims live verification unless backed by future command/network evidence.
- No relay publishing/readback, relay fetching, key use, event signing, fixture ID replacement, public CI/status event creation, live Radicle/IPFS/Sigstore verification, spending, production/private keys, or unsupported security/durability/censorship-proof claims were performed.

### Loop 17: NIP-34 adapter verification-state vocabulary alignment

Status: **complete as local adapter/renderer vocabulary alignment; no relay publishing, signing, or live protocol verification**.

Outputs:

- `scripts/nip34_adapter.py` now exports adapter-local `verification_states[]` rows using the same vocabulary as the top-level registry fixtures.
- Adapter rows cover repository announcement import, issue/patch collaboration import, local conformance reports, repository state import, and synthetic fixture-only status/check projections.
- `scripts/render_project_page.py` now displays those adapter verification states compactly inside the optional NIP-34 fixture adapter section, separate from the registry-level **Verification states** section.
- `output/demo-project.html` regenerated with all optional local NIP-34 fixtures and the adapter verification-state section.
- `tests/test_registry_fixture.py` now verifies adapter verification-state scopes, non-live/synthetic/local values, renderer display, and absence of unsupported live/security/durability/censorship-proof claim phrases in adapter rows.
- README, `.hermes/context.md`, `AGENT-LOOPS.md`, and `docs/nip34-event-shapes.md` updated for Loop 17 behavior and boundaries.

Verified commands:

- `python3 -m json.tool schemas/project-registry.schema.json` — passed.
- `python3 -m json.tool fixtures/example-project.registry.json` — passed.
- `python3 -m json.tool fixtures/radicle-backed-project.registry.json` — passed.
- `python3 -m json.tool fixtures/nostr-repo-announcement.json` — passed.
- `python3 -m json.tool fixtures/nostr-collaboration-events.json` — passed.
- `python3 -m json.tool fixtures/nostr-repo-state-status.json` — passed.
- `python3 scripts/render_project_page.py fixtures/example-project.registry.json output/demo-project.html --nip34-repo-fixture fixtures/nostr-repo-announcement.json --nip34-collaboration-fixture fixtures/nostr-collaboration-events.json --nip34-state-status-fixture fixtures/nostr-repo-state-status.json` — passed.
- `python3 scripts/nip34_adapter.py fixtures/nostr-repo-announcement.json fixtures/nostr-collaboration-events.json fixtures/nostr-repo-state-status.json` — passed.
- `python3 -m unittest discover -s tests` — passed, 35 tests.

Boundaries:

- Adapter verification rows are local fixture metadata only and all current rows are non-live/synthetic/local or source-inspected mappings.
- No relay publishing/readback, relay fetching, key use, event signing, fixture ID replacement, public CI/status event creation, live Radicle/IPFS/Sigstore verification, spending, production/private keys, or unsupported security/durability/censorship-proof claims were performed.

### Loop 18: Static verification-state renderer summaries/grouping

Status: **complete as local static renderer UX/status improvement; no live protocol verification or publishing**.

Outputs:

- `scripts/render_project_page.py` now summarizes both registry-level and adapter-level `verification_states[]` rows with total counts, live-verified counts, live-unverified/local counts, synthetic/non-synthetic counts, counts by state, grouped rows by state, and claim-boundary summaries.
- The static CSS now adds visible classes for local fixture, source-inspected mapping, synthetic fixture, live-unverified, and live-verified verification labels without requiring JavaScript.
- `output/demo-project.html` regenerated with all optional local NIP-34 fixtures and the new verification summaries/grouping.
- `tests/test_registry_fixture.py` now asserts registry and adapter summaries, zero live-verified fixture counts, grouped state counts, visible state classes, and no synthetic live-verified count drift.
- README, `.hermes/context.md`, `AGENT-LOOPS.md`, and `docs/nip34-event-shapes.md` updated for Loop 18 behavior and boundaries.

Verified commands:

- `python3 -m json.tool schemas/project-registry.schema.json` — passed.
- `python3 -m json.tool fixtures/example-project.registry.json` — passed.
- `python3 -m json.tool fixtures/radicle-backed-project.registry.json` — passed.
- `python3 -m json.tool fixtures/nostr-repo-announcement.json` — passed.
- `python3 -m json.tool fixtures/nostr-collaboration-events.json` — passed.
- `python3 -m json.tool fixtures/nostr-repo-state-status.json` — passed.
- `python3 scripts/render_project_page.py fixtures/example-project.registry.json output/demo-project.html --nip34-repo-fixture fixtures/nostr-repo-announcement.json --nip34-collaboration-fixture fixtures/nostr-collaboration-events.json --nip34-state-status-fixture fixtures/nostr-repo-state-status.json` — passed.
- `python3 scripts/nip34_adapter.py fixtures/nostr-repo-announcement.json fixtures/nostr-collaboration-events.json fixtures/nostr-repo-state-status.json` — passed.
- `python3 -m unittest discover -s tests` — passed, 35 tests.

Boundaries:

- Renderer summaries are static displays of existing local fixture metadata only.
- Current fixtures still have zero live-verified rows.
- No relay publishing/readback, relay fetching, key use, event signing, fixture ID replacement, public CI/status event creation, live Radicle/IPFS/Sigstore verification, spending, production/private keys, or unsupported security/durability/censorship-proof claims were performed.

## Verification requirements

- Each protocol claim should include source URL and retrieval date where possible.
- Research must separate observed facts from recommendations.
- Public building is approved for this project in the current all-night controller run: GitHub publishing/pushes, public project updates, and public collaboration surfaces are allowed when accurate, non-spammy, and labeled as research/prototype work.
- No spending.
- No production/private keys for protocol actions.
- No unsupported production/security/censorship-proof claims.
- Local commits and public GitHub pushes are allowed after tests/preflight pass.

## Latest parent-verified state

- Repo initialized locally at `/home/openclaw/projects/decentralized-forge`.
- First commit existed before this run: `171e578 docs: initialize decentralized forge research workspace`.
- This run observed no uncommitted user changes before editing.
- Public GitHub repo created and verified: `https://github.com/redclawanon-rgb/decentralized-forge`.
- Public settings verified: visibility PUBLIC, default branch `main`, Issues enabled, Discussions enabled, Wiki disabled.
- Remote sync is verified in the final controller report with `git rev-parse HEAD` and `git ls-remote origin refs/heads/main`; keep this line non-SHA-specific to avoid making the status-only commit stale.

## Current architecture recommendation

- Keep the local registry JSON as the canonical control-plane object and the static renderer as the first user-visible surface.
- Treat all current Nostr, Radicle, IPFS, ForgeFed, and provenance data as fixtures/mappings unless a future loop records live command/network verification.
- Use the completed local NIP-34 parser/conformance adapter, repository state/status fixture, local NIP-01 conformance reports, adapter verification-state exports, and rendered fixture-adapter/conformance/verification sections as the seam for future Nostr UI/import work, while keeping relay publishing behind disposable-key and explicit relay gates.
- Run a safe Radicle local CLI replay when an approved binary/install path is available; use a temporary `RAD_HOME`, disposable repo, and no public seed publishing by default.
- Keep ForgeFed as a later object-shape/federation bridge; do not run a public actor until moderation/security gates exist.
- Keep IPFS/CIDs as artifact metadata until live add/fetch/pin verification is explicitly performed; defer Filecoin/Arweave because they imply spending/wallet decisions.
- Keep Sigstore/in-toto/SLSA as release/build trust models; current provenance is synthetic and no SLSA level should be claimed.

## Next recommended loop

**Loop 19: release/preflight polish for generated static artifact and public usage instructions, or safe live-gated replay if prerequisites appear.**

Loop 18 is complete locally. The next bounded candidate is release/preflight polish around the generated static HTML artifact and public README screenshots/usage instructions, keeping all local/synthetic/live-unverified boundaries visible. A safe Radicle local CLI replay remains an alternative only if an approved `rad` binary/install path is available. Keep all live protocol claims gated by actual command/network verification, and keep relay publishing out of scope unless disposable/project-scoped keys, relay selection, and public protocol gates are explicitly satisfied.

## Gates/blockers

- Public publishing/posting/pushing and public account/project creation are approved for this project when accurate, non-spammy, and labeled research/prototype.
- Public Nostr relay publishing requires disposable/project-scoped keys only; do not use production/private personal keys.
- Do not run a public ActivityPub/ForgeFed actor unless it is free, clearly prototype-labeled, and does not require paid infrastructure or production credentials.
- Do not spend money or use Filecoin/Arweave wallets without explicit approval.
- Do not use production/private keys; fixtures must use synthetic public identifiers only.
- Do not contact specific people outside public project channels.
