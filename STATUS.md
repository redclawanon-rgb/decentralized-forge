# Status

## Current milestone

Current completion state: **Milestone 1 complete as an evidence-scoped static prototype with hosted local-verification CI passing on `main`**. This does not claim production readiness, durable storage, censorship resistance, broad protocol availability, security guarantees, real signing, Sigstore/in-toto verification, Rekor upload, or SLSA compliance.

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

### Loop 19: Static artifact release/preflight polish

Status: **complete as local static artifact preflight and public usage polish; no hosting, relay publishing, signing, or live protocol verification**.

Outputs:

- `scripts/preflight_static_artifact.py` added as a stdlib-only preflight for `output/demo-project.html`.
- The preflight checks that the HTML artifact exists, matches a regenerated all-fixture renderer output, contains expected local/synthetic/non-claim and optional NIP-34 fixture sections, and omits selected unsupported live-protocol/security/durability claim phrases.
- `tests/test_registry_fixture.py` now covers preflight success, stale/overclaim detection, and the documented CLI command.
- README usage instructions now show how to regenerate, locally open, preflight, and fully verify the static artifact while preserving local/synthetic/live-unverified boundaries.
- `output/demo-project.html` regenerated with all optional local NIP-34 fixtures.
- `.hermes/context.md` and `AGENT-LOOPS.md` updated for Loop 19 completion and the next loop recommendation.

Verified commands:

- `python3 -m json.tool schemas/project-registry.schema.json` — passed.
- `python3 -m json.tool fixtures/example-project.registry.json` — passed.
- `python3 -m json.tool fixtures/radicle-backed-project.registry.json` — passed.
- `python3 -m json.tool fixtures/nostr-repo-announcement.json` — passed.
- `python3 -m json.tool fixtures/nostr-collaboration-events.json` — passed.
- `python3 -m json.tool fixtures/nostr-repo-state-status.json` — passed.
- `python3 scripts/render_project_page.py fixtures/example-project.registry.json output/demo-project.html --nip34-repo-fixture fixtures/nostr-repo-announcement.json --nip34-collaboration-fixture fixtures/nostr-collaboration-events.json --nip34-state-status-fixture fixtures/nostr-repo-state-status.json` — passed.
- `python3 scripts/nip34_adapter.py fixtures/nostr-repo-announcement.json fixtures/nostr-collaboration-events.json fixtures/nostr-repo-state-status.json` — passed.
- `python3 scripts/preflight_static_artifact.py` — passed.
- `python3 -m unittest discover -s tests` — passed, 38 tests.

Boundaries:

- Static artifact preflight is local command evidence only.
- The generated HTML is a local file artifact, not a hosted release page or signed authority.
- No relay publishing/readback, relay fetching, key use, event signing, fixture ID replacement, public CI/status event creation, live Radicle/IPFS/Sigstore verification, paid screenshot/hosting tooling, spending, production/private keys, direct outreach, or unsupported security/durability/censorship-proof claims were performed.

### Loop 20: Safe live-gated adapter replay planning

Status: **complete as planning/checklist only; no live protocol actions**.

Outputs:

- `docs/live-adapter-replay-plan.md` added with Radicle local replay prerequisites, temporary `RAD_HOME` guidance, disposable repo flow, evidence capture, failure/rollback, promotion criteria, and explicit no-public-seed-publish default.
- The same plan includes a Nostr disposable/project-scoped publish/readback checklist covering key storage without recording secret values, relay selection, signing, publish, readback, event ID verification, fixture-to-live transition criteria, rollback, and non-claims.
- `fixtures/live-adapter-replay-checklist.json` added as a secret-free machine-readable gate checklist.
- `tests/test_registry_fixture.py` validates the checklist remains non-live, secret-free, and blocked on the missing Radicle CLI prerequisite.
- README, `.hermes/context.md`, and `AGENT-LOOPS.md` updated for Loop 20 completion and Loop 21 gating.

Verified commands:

- `command -v rad` — no `rad` executable found on `PATH`; `rad --version` was not run.
- `python3 -m json.tool schemas/project-registry.schema.json` — passed.
- `python3 -m json.tool fixtures/example-project.registry.json` — passed.
- `python3 -m json.tool fixtures/radicle-backed-project.registry.json` — passed.
- `python3 -m json.tool fixtures/nostr-repo-announcement.json` — passed.
- `python3 -m json.tool fixtures/nostr-collaboration-events.json` — passed.
- `python3 -m json.tool fixtures/nostr-repo-state-status.json` — passed.
- `python3 -m json.tool fixtures/live-adapter-replay-checklist.json` — passed.
- `python3 scripts/render_project_page.py fixtures/example-project.registry.json output/demo-project.html --nip34-repo-fixture fixtures/nostr-repo-announcement.json --nip34-collaboration-fixture fixtures/nostr-collaboration-events.json --nip34-state-status-fixture fixtures/nostr-repo-state-status.json` — passed.
- `python3 scripts/nip34_adapter.py fixtures/nostr-repo-announcement.json fixtures/nostr-collaboration-events.json fixtures/nostr-repo-state-status.json` — passed.
- `python3 scripts/preflight_static_artifact.py` — passed.
- `python3 -m unittest discover -s tests` — passed, 39 tests.

Boundaries:

- Loop 20 performed safe local discovery and documentation/checklist work only.
- No unsafe installer, package install, Radicle CLI action, `RAD_HOME` replay, public seed publishing, Nostr key generation, event signing, relay publishing/readback, public CI/status event creation, spending, production/private key use, direct outreach, or live protocol verification occurred.

### Loop 21: approved tooling install and disposable Nostr key prerequisite

Status: **complete as prerequisite-only tooling/key setup; no live relay or Radicle replay**.

Eric approved installing needed tooling and generating Harry-owned Nostr keys via Telegram on 2026-06-22.

Outputs:

- Installed Radicle user-local binaries under `~/.local/bin`: `rad`, `radicle-node`, and `git-remote-rad`.
- Installed Nostr CLI `nak` as `~/.local/bin/nak`.
- Generated a disposable/project-scoped Nostr secret key outside the repo at `~/.hermes/keys/decentralized-forge/nostr-project.nsec` with `0600` permissions; the secret value is not recorded in repo docs, fixtures, evidence, or status.
- Recorded public key only: `npub1ve55y0h8dkw44hyws80hj2rvy457m0j6hp8nudgy8km354807hyqp97suy` / `6669423ee76d9d5adc8e81df79286c2569edbe5ab84f3e35043db71a54eff5c8`.
- Added offline signed proof event at `evidence/nostr-offline-key-proof-2026-06-22.json`; verified locally, not published.
- Updated `docs/live-adapter-replay-plan.md`, `fixtures/live-adapter-replay-checklist.json`, and tests for the installed/key-ready prerequisite state.

Verified commands:

- `rad --version` — `rad 1.9.1 (5bd3569e120a6172d9df68e1d1d0eed15e8104b1)`.
- `radicle-node --version` — `radicle-node 1.9.1 (5bd3569e120a6172d9df68e1d1d0eed15e8104b1)`.
- `git-remote-rad --version` — `git-remote-rad 1.9.1 (5bd3569e120a6172d9df68e1d1d0eed15e8104b1)`.
- `nak --version` — `nak version v0.20.0`.
- `nak verify < evidence/nostr-offline-key-proof-2026-06-22.json` — passed with no output.

Boundaries:

- No `sudo`/root package install was possible or used; installs are user-local.
- No curl-pipe-shell installer was executed.
- No Radicle identity/repo replay, temporary `RAD_HOME` replay, Radicle node start, public seed publishing, Nostr relay publishing/readback, paid infrastructure, production/private personal key use, direct outreach, or live protocol verification occurred.

### Loop 22: Radicle local replay preflight

Status: **complete as read-only CLI help/version preflight; no stateful Radicle replay**.

Outputs:

- Added `evidence/radicle-local-replay-preflight-2026-06-22.md` with inspected help output, safe Loop 23 command path, and explicit non-actions.
- Updated `fixtures/live-adapter-replay-checklist.json` to record Loop 22 preflight state and keep Radicle replay unexecuted.
- Updated tests so the machine-readable checklist asserts Loop 22 evidence, safe command-surface labels, and first-replay forbidden actions.

Verified commands:

- `command -v rad` — `/home/openclaw/.local/bin/rad`.
- `rad --version` — `rad 1.9.1 (5bd3569e120a6172d9df68e1d1d0eed15e8104b1)`.
- `rad --help` — passed; top-level command list inspected.
- `rad init --help` — passed; `--no-confirm`, `--no-seed`, `--private`, and default-branch options inspected.
- `rad inspect --help` — passed; `--rid`, `--identity`, `--refs`, and `--visibility` options inspected.
- `rad auth --help`, `rad self --help`, `rad id --help`, `rad node --help`, and `rad path --help` — passed as help-only preflight.
- `rad status --help` — failed as expected because `rad status` is not a known command in Radicle 1.9.1; use `rad inspect` instead.

Boundaries:

- Loop 22 did not run `rad auth`, `rad init`, create temporary Radicle state, start a node, publish/seed/sync/announce, configure remotes/peers, use production/private personal keys, spend money, or verify public Radicle networking.
- Loop 23 may run the approved temporary-`RAD_HOME` disposable replay, but must abort if local-only behavior becomes ambiguous or a command attempts node/network/seed/publish/sync/announce behavior.

### Loop 23: Radicle temporary-`RAD_HOME` disposable repo replay

Status: **complete as local CLI verification only; no public Radicle network action**.

Outputs:

- `evidence/radicle-local-replay-2026-06-22.md` records the bounded replay evidence.
- `fixtures/live-adapter-replay-checklist.json` records Loop 23 state.
- `tests/test_registry_fixture.py` validates Loop 23 evidence remains bounded/secret-free and does not claim public network replication.

Verified commands/evidence:

- `rad auth --alias decentralized-forge-replay --stdin` with a disposable passphrase and temporary `RAD_HOME` — exited 0.
- `rad init --name decentralized-forge-disposable-replay --description ... --default-branch master --private --no-confirm --no-seed /tmp/<temp>/repo` — exited 0.
- `rad inspect --rid /tmp/<temp>/repo` — returned `rad:z33oByNZxkxXAChhD54B4XiSsQkao`.
- `rad inspect --identity /tmp/<temp>/repo` — returned expected project payload, delegate DID, threshold 1, and private visibility.
- `rad inspect --refs /tmp/<temp>/repo` — returned local refs tree.
- `rad inspect --visibility /tmp/<temp>/repo` — returned `private`.

Boundaries:

- Temporary `RAD_HOME` and disposable repo were removed after evidence capture.
- No `rad node start`, `rad publish`, `rad sync`, `rad seed`, peer announce, remote peer configuration, paid infrastructure, production/private personal key use, direct outreach, or public network verification occurred.
- This promotes Radicle only to **local CLI verified** for the narrow disposable replay path; public seed/network replication, remote clone/fetch, durability, censorship resistance, and production readiness remain unverified.

### Loop 24: Nostr relay selection and event payload review

Status: **complete as relay/payload selection plus local signature verification; no relay publication/readback**.

Outputs:

- `docs/nostr-relay-publish-readback-plan.md` records selected relays, disposable-key boundary, exact event ID, and Loop 25 publish/readback commands.
- `evidence/nostr-relay-selection-2026-06-22.md` records NIP-11 relay info and the local signing/verification evidence.
- `evidence/nostr-loop24-unsigned-payload-2026-06-22.json` stores the exact unsigned payload preview.
- `evidence/nostr-loop24-signed-event-preview-2026-06-22.json` stores the signed public event preview; it contains no secret key material.
- `fixtures/live-adapter-replay-checklist.json` and tests now record Loop 24 state.

Verified commands/evidence:

- `~/.local/bin/nak relay wss://relay.damus.io` — NIP-11 info reachable; reports `auth_required: false`, `payment_required: false`, and `restricted_writes: false`.
- `~/.local/bin/nak relay wss://nos.lol` — NIP-11 info reachable; reports `auth_required: false`, `payment_required: false`, and `restricted_writes: false`.
- `~/.local/bin/nak event --force-sign ...` — created signed local event preview using only the disposable project key from `~/.hermes/keys/decentralized-forge/nostr-project.nsec`; the secret value was not logged.
- `~/.local/bin/nak verify < evidence/nostr-loop24-signed-event-preview-2026-06-22.json` — exited 0.
- `python3 -m json.tool evidence/nostr-loop24-signed-event-preview-2026-06-22.json` — passed.

Selected event:

- Kind: `30617` NIP-34 repository announcement.
- Event ID: `4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba`.
- Public key: `6669423ee76d9d5adc8e81df79286c2569edbe5ab84f3e35043db71a54eff5c8`.
- Target relays for Loop 25: `wss://relay.damus.io`, `wss://nos.lol`.

Boundaries:

- Loop 24 did not publish to relays, perform relay readback, spend money, use production/private personal keys, contact specific people, or claim durability/global propagation/censorship resistance/identity trust/production readiness/full protocol compatibility.
- Loop 25 may publish/read back the exact signed event under Permission B, treating publication as public/irreversible and preserving all non-claims.


### Loop 25: Nostr disposable publish/readback

Status: **complete as public relay acceptance/readback for one prototype-labeled disposable-key event**.

Outputs:

- `evidence/nostr-loop25-publish-readback-2026-06-22.md` records publish responses, relay readback, local/readback verification, and non-claims.
- `evidence/nostr-loop25-publish-readback-2026-06-22.json` records the same evidence in machine-readable form.
- `fixtures/live-adapter-replay-checklist.json` records Loop 25 state.
- Tests now validate Loop 25 readback evidence remains secret-free and bounded.

Verified commands/evidence:

- `~/.local/bin/nak verify < evidence/nostr-loop24-signed-event-preview-2026-06-22.json` — exited 0.
- `~/.local/bin/nak event wss://relay.damus.io < evidence/nostr-loop24-signed-event-preview-2026-06-22.json` — exited 0; publish stderr reported `publishing to relay.damus.io... success.`
- `~/.local/bin/nak event wss://nos.lol < evidence/nostr-loop24-signed-event-preview-2026-06-22.json` — exited 0; publish stderr reported `publishing to nos.lol... success.`
- `~/.local/bin/nak req -i 4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba wss://relay.damus.io` — read back the matching event.
- `~/.local/bin/nak req -i 4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba wss://nos.lol` — read back the matching event.
- `nak verify` on both readback events — exited 0.

Selected event:

- Kind: `30617` NIP-34 repository announcement.
- Event ID: `4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba`.
- Public key: `6669423ee76d9d5adc8e81df79286c2569edbe5ab84f3e35043db71a54eff5c8`.
- Relays with verified readback: `wss://relay.damus.io`, `wss://nos.lol`.

Boundaries:

- Publication used only the disposable project key; no secret key value is recorded in repo evidence/docs.
- Loop 25 proves only selected-relay acceptance and readback of the exact prototype event.
- It does not prove durability, global propagation, censorship resistance, identity trust, production readiness, security guarantees, or full NIP-34/forge protocol compatibility.
- No spending, paid infrastructure, production/private personal key, direct outreach, Radicle node/seed action, wallet, or public status/CI event was used.

### Loop 26: Live evidence import into adapter/renderer

Status: **complete as bounded live/local evidence import; no new live network action**.

Outputs:

- `fixtures/live-evidence-index.json` indexes Loop 23 Radicle local CLI/private replay evidence and Loop 25 Nostr selected-relay readback evidence with explicit non-claims.
- `scripts/render_project_page.py` accepts `--live-evidence-index` and renders a **Live evidence index** section.
- `scripts/preflight_static_artifact.py` now regenerates/checks `output/demo-project.html` with the live evidence index.
- `fixtures/live-adapter-replay-checklist.json` records Loop 26 import state.
- `tests/test_registry_fixture.py` validates the index, renderer output, bounded states, and secret-free/non-overclaiming evidence import.
- `output/demo-project.html` was regenerated with all optional NIP-34 fixtures plus the live evidence index.

Verified commands/evidence:

- `python3 scripts/render_project_page.py fixtures/example-project.registry.json output/demo-project.html --nip34-repo-fixture fixtures/nostr-repo-announcement.json --nip34-collaboration-fixture fixtures/nostr-collaboration-events.json --nip34-state-status-fixture fixtures/nostr-repo-state-status.json --live-evidence-index fixtures/live-evidence-index.json` — exited 0.

Boundaries:

- Radicle is still only local CLI verified for one disposable private temporary-`RAD_HOME` init/inspect replay.
- Nostr is only selected-relay acceptance/readback verified for one exact prototype event on `wss://relay.damus.io` and `wss://nos.lol`.
- No new Nostr publish/readback, Radicle node start, Radicle seed/publish/sync/remote clone, public Radicle network replication, spending, paid infrastructure, production/private personal key use, direct outreach, wallet/pinning/storage action, or unsupported durability/global-propagation/censorship-resistance/security/production-readiness/full-compatibility claim occurred.

### Loop 27: Public project update draft/post

Status: **complete as a prototype/research-labeled public project-channel update**.

Outputs:

- `docs/public-update-drafts/2026-06-22-live-adapter-evidence-update.md` records the exact public update body and posting result.
- GitHub Discussion #6 was created in the project Announcements channel: https://github.com/redclawanon-rgb/decentralized-forge/discussions/6.

Verified evidence:

- `gh api graphql ... createDiscussion` returned Discussion #6 with the expected title and URL.

Boundaries:

- The update preserves narrow claims: Radicle remains local CLI/private replay only; Nostr remains selected-relay acceptance/readback only for the exact prototype event.
- No direct outreach, spending, paid infrastructure, production/private personal key use, Radicle node/seed/publish/sync/remote clone, Filecoin/Arweave wallet/pinning/storage action, or unsupported durability/global-propagation/censorship-resistance/security/production-readiness/full-compatibility claim occurred.

### Loop 28: Nostr readback persistence/divergence check

Status: **complete as low-volume readback persistence/divergence evidence; no new publish**.

Outputs:

- `evidence/nostr-loop28-readback-check-2026-06-22.md` records the human-readable readback/divergence result.
- `evidence/nostr-loop28-readback-check-2026-06-22.json` records the machine-readable relay results.
- `fixtures/live-adapter-replay-checklist.json` and tests now record Loop 28 state.

Verified evidence:

- Re-read event `4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba` by ID from `wss://relay.damus.io`, `wss://nos.lol`, `wss://relay.primal.net`, and `wss://nostr.wine`.
- `wss://relay.damus.io`, `wss://nos.lol`, and `wss://relay.primal.net` returned the exact event; field comparisons matched the signed preview and `nak verify` passed.
- `wss://nostr.wine` did not return the event during this check.

Boundaries:

- Loop 28 was readback-only; no new Nostr event was published and no secret key material was read or printed.
- This remains selected/limited relay evidence only. It is not a durability guarantee, global propagation proof, censorship-resistance proof, identity-trust proof, production-readiness claim, security guarantee, or full NIP-34/forge compatibility claim.
- No spending, paid/authenticated relay, production/private personal key, direct outreach, or Radicle public-network action occurred.

### Loop 29: NIP-34 live-event adapter import

Status: **complete as selected-relay readback evidence import; no new Nostr publish/fetch/signing**.

Outputs:

- `fixtures/nostr-live-readback-events.json` records the Loop 25 kind `30617` event as a live-readback adapter fixture with explicit non-claims and missing-semantics notes.
- `scripts/nip34_adapter.py` imports the recorded live event separately from dry-run fixtures, recomputes the NIP-01 event ID locally, and emits one `live-verified` adapter row scoped only to selected-relay readback evidence.
- `scripts/render_project_page.py` and `output/demo-project.html` now render a **NIP-34 live readback import** subsection separate from the dry-run fixture adapter.
- `scripts/preflight_static_artifact.py`, `fixtures/live-adapter-replay-checklist.json`, and `tests/test_registry_fixture.py` were updated for the Loop 29 import.

Verified evidence:

- The imported event ID is `4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba`; local NIP-01 event-id recomputation in `scripts/nip34_adapter.py` matches the recorded ID.
- Source evidence remains `evidence/nostr-loop25-publish-readback-2026-06-22.json`; Loop 29 did not perform any new relay publish, relay fetch, or signing.

Boundaries:

- Loop 29 imports only the already-recorded Loop 25 selected-relay readback evidence.
- It does not verify durability, global propagation, censorship resistance, identity trust, security, production readiness, full NIP-34/forge compatibility, issue/patch readback, repository-state readback, status semantics, relay discovery, subscription behavior, deletion/replacement behavior, or multi-client behavior.
- No spending, paid infrastructure, production/private personal key use, direct outreach, Radicle public-network action, Filecoin/Arweave wallet/pinning/storage action, or new Nostr event occurred.

### Loop 30: Radicle public-network gate plan/preflight

Status: **complete as Permission-F help-only public-network preflight; Permission G remains blocked**.

Outputs:

- `docs/radicle-public-network-gate-plan.md` drafts the later Permission-G disposable public seed/remote-clone smoke checklist without executing it.
- `evidence/radicle-public-network-preflight-2026-06-22.md` records inspected Radicle help surfaces and non-actions.
- `fixtures/live-adapter-replay-checklist.json` and tests now record Loop 30 state.

Verified evidence:

- `command -v rad` — `/home/openclaw/.local/bin/rad`.
- `rad --version` — `rad 1.9.1 (5bd3569e120a6172d9df68e1d1d0eed15e8104b1)`.
- Help-only inspection covered `rad publish`, `rad seed`, `rad sync`, `rad sync status`, `rad node`, `rad node start`, `rad node status`, `rad node connect`, `rad remote`, `rad remote add`, `rad remote list`, `rad clone`, `rad fetch`, `rad unseed`, and `rad follow`.
- Findings: `rad publish` makes a repo public/discoverable; `rad sync` defaults to fetch+announce; `rad remote add` defaults may fetch/sync unless disabled; `rad clone` uses local node routing or explicit seeds; `rad fetch` is not a known command in Radicle 1.9.1.

Boundaries:

- Loop 30 performed help/docs preflight only.
- No `RAD_HOME` was created, no Radicle identity was created/reused, no node was started, no repository was published/seeded/synced/announced/cloned/fetched/connected/followed/remotely configured, and no public Radicle network action occurred.
- Permission G remains required before any public Radicle seed/publish/sync/node/remote clone/fetch action.

### Loop 31: Public storage/IPFS evidence gate plan/preflight

Status: **complete as Permission-H inventory/plan preflight only; no live storage action**.

Outputs:

- `evidence/storage-tooling-preflight-2026-06-22.md` records installed-tool inventory, local/free runtime inventory, npm package metadata checks, and non-actions.
- `docs/public-storage-evidence-gate-plan.md` drafts a later local CAR/CID fixture verification path plus future live-IPFS and paid/wallet gates.
- `fixtures/live-adapter-replay-checklist.json` and tests now record Loop 31 storage preflight state.

Verified evidence:

- `command -v ipfs`, `kubo`, `ipfs-car`, `car`, `ipld`, `cid`, `ipget`, `ipfs-dag`, `ipfs-cluster-service`, `ipfs-cluster-ctl`, and `go-ipfs` — all missing on this host.
- Python modules `multiformats`, `ipfshttpclient`, `car`, `dag_cbor`, and `cbor2` — missing.
- Local/free runtimes present: Node `v22.22.2`, npm/npx `10.9.7`, corepack `0.34.6`, Python `3.13.5`, uv `0.11.16`; Go/Rust/Cargo missing.
- Read-only `npm view` metadata checked, with no install/execution: `ipfs-car@3.1.0`, `@ipld/car@5.4.6`, `multiformats@14.0.0`, `helia@6.1.4`, and `kubo-rpc-client@7.1.0`, all reporting `Apache-2.0 OR MIT` license in npm metadata.

Boundaries:

- Loop 31 performed preflight/inventory/docs only.
- No package install, IPFS daemon start, IPFS add/fetch/pin, CAR generation/import, public gateway check, Filecoin/Arweave wallet action, paid pinning/storage, spending, production/private key use, direct outreach, or durability/global-availability/censorship-resistance/security/production-readiness claim occurred.
- Recommended next storage loop is local CAR/CID fixture verification. Dependency-backed path needs approval to add project-scoped dev dependencies; no-new-dependency fallback can only strengthen stdlib CID documentation/tests.

### Loop 32: Next controller/report consolidation

Status: **complete as docs/checklist/test consolidation for Loops 26–31**.

Outputs:

- `STATUS.md`, `.hermes/context.md`, `AGENT-LOOPS.md`, and `docs/next-evidence-and-interoperability-loops.md` consolidated around Loop 31 completion and remaining gates.
- Verification and git push are recorded in the final controller report for this run.

Boundaries:

- Loop 32 did not create any new cron jobs, run any public Radicle action, perform live storage action, spend money, use wallets/production keys, or make unsupported durability/security/production claims.

### Loop 33: Local CAR/CID fixture verification

Status: **complete as Permission-I local CAR/CID verification with project-scoped lockfile-backed dev dependencies; no live storage action**.

Outputs:

- `package.json` / `package-lock.json` with project-scoped dev dependencies: `@ipld/car@5.4.6` and `multiformats@14.0.0`.
- `scripts/verify_car_cid_fixture.mjs` to derive the raw CID, write a local CAR, read it back, and emit evidence.
- `evidence/local-car-cid-fixture-2026-06-22.json`.
- `evidence/local-release-artifact-2026-06-22.car`.
- `fixtures/live-adapter-replay-checklist.json` and tests updated for Loop 33.

Verified evidence:

- `npm run verify:car-cid` — passed; verified CID `bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua` for `fixtures/local-release-artifact.txt`.
- Evidence records SHA-256 `3932e28d5b609b3cae25218ca205ea126cd3cf344628dc4c4b9bf094c50668a0`, CAR size `338` bytes, one CAR root matching the CID, one block, block CID match, and block bytes matching the input fixture.

Boundaries:

- No IPFS daemon, IPFS add/fetch/pin, public gateway query, wallet, Filecoin/Arweave action, paid storage, spending, production/private key, direct outreach, durability/global-availability/censorship-resistance/security/production-readiness claim occurred.

### Loop 34: Disposable public Radicle seed/remote-clone smoke

Status: **complete as Permission-G disposable public Radicle smoke; exact bounded evidence only**.

Outputs:

- `scripts/run_radicle_public_smoke.py` for the bounded disposable smoke runner.
- `evidence/radicle-public-network-smoke-2026-06-22.json`.
- `evidence/radicle-public-network-smoke-2026-06-22.md`.
- `fixtures/live-adapter-replay-checklist.json` and tests updated for Loop 34.

Verified evidence:

- `python3 scripts/run_radicle_public_smoke.py` — exited 0.
- Disposable RID: `rad:z2WtozFrCRhygh9CGzyUN57CN7Nwa`.
- Public visibility verified by `rad inspect --visibility`.
- Temporary seed node started on localhost; `rad seed <RID> --no-fetch` succeeded; `rad sync --announce <RID>` succeeded with `Synced with 2 seed(s)`.
- A separate temporary Radicle profile/node connected to the disposable seed over localhost; `rad clone --seed <disposable NID> <RID>` succeeded; cloned README readback matched the disposable fixture text.
- Nodes were stopped and temporary `/tmp/df-radicle-public-smoke-*` state was removed after evidence capture.

Boundaries:

- No production/private personal keys, paid infrastructure, spending, direct outreach, named external peer targeting, or persistent project state was used.
- This proves only the exact disposable public Radicle smoke behavior in the evidence. It does not prove durability, censorship resistance, security, global replication, identity trust, production readiness, full Radicle compatibility, or broad Radicle network availability.

### Loop 35: Consolidation/report

Status: **complete as docs/context/status/checklist/test consolidation; no new live action**.

Outputs:

- `evidence/loop35-consolidation-2026-06-22.md` records the consolidated evidence paths, verified scope, non-claims, and remaining gates for Loops 33–34.
- `fixtures/live-adapter-replay-checklist.json` now advances the controller state to Loop 35 and records that no new network/storage action, public update, or cron job occurred in the consolidation loop.
- `tests/test_registry_fixture.py` now asserts the Loop 35 checklist/evidence state and preserved gates.
- `STATUS.md`, `.hermes/context.md`, `AGENT-LOOPS.md`, and `docs/next-evidence-and-interoperability-loops.md` now mark Loop 35 complete and move further live/storage/public-update work back behind explicit approvals.

Verified evidence:

- Pre-edit consolidation verification passed: `npm run verify:car-cid`, `python3 -m unittest discover -s tests` (50 tests), `python3 scripts/preflight_static_artifact.py`, and the project artifact secret-marker scan excluding `.git`, `node_modules`, `tests`, and binary CAR artifacts.
- Final post-edit verification/commit/push are recorded in the controller's final report for this run.

Boundaries:

- Loop 35 performed consolidation only. No new public protocol action, IPFS/storage action, gateway check, pinning, wallet, spending, paid infrastructure, production/private personal key use, direct outreach, public update, or new cron job occurred.
- Further live storage, repeated/broader Radicle public-network testing, public updates about Loops 33–34, or stronger durability/censorship/security/production claims require a new explicit approval/target.

### Loop 36: Milestone 1 CI and completion state

Status: **complete as hosted local-verification CI and Milestone 1 closure; no new live protocol/storage action**.

Outputs:

- `.github/workflows/ci.yml` runs the local verification suite on pushes to `main` and pull requests.
- `scripts/forge_registry.py` provides reusable `validate`, `render`, `export-summary`, and `verify-local` commands.
- `fixtures/portable-lab.registry.json`, `output/portable-lab.html`, and `output/*.summary.json` provide second-fixture and machine-readable export coverage.
- `COMPLETION-CRITERIA.md` records the Milestone 1 definition of done and marks the reproducible prototype, reusable local tooling, and multi-project fixture lanes complete.

Verified evidence:

- Local `npm run verify:local` passed on Windows in this checkout.
- GitHub Actions `ci` run #2 passed on `main` for commit `e69fd5b22e8ec27f52a11e582b705e212690a865`: https://github.com/redclawanon-rgb/decentralized-forge/actions/runs/28335479676

Boundaries:

- Hosted CI is local verification only. It does not sign artifacts, upload to Rekor, verify Sigstore/cosign/in-toto, claim SLSA compliance, publish protocol events, start IPFS/Radicle/Nostr live actions, use production/private keys, spend money, or prove durability/censorship resistance/security/production readiness.

### Loop 37: Public Milestone 1 update

Status: **complete as a prototype-labeled public project-channel update; no new live protocol/storage action**.

Outputs:

- `docs/public-update-drafts/2026-06-28-milestone-1-complete.md` records the exact public update body and posting result.
- GitHub Discussion #7 was created in the project Announcements channel: https://github.com/redclawanon-rgb/decentralized-forge/discussions/7

Verified evidence:

- GitHub GraphQL `createDiscussion` returned Discussion #7 with the expected title and URL.

Boundaries:

- The update preserves narrow claims: Milestone 1 is complete only as a reproducible, evidence-scoped static prototype with hosted local-verification CI.
- No live IPFS/storage action, new Nostr publish/readback, new Radicle public-network action, signing/provenance action, spending, paid infrastructure, production/private personal key use, direct outreach, or unsupported durability/censorship-resistance/security/SLSA/production-readiness claim occurred.

### Loop 38: Approval-bounded next-loop controller

Status: **complete as repo-contained safe automation; no live protocol/storage/signing action**.

Outputs:

- `fixtures/next-loop-controller.json` records approved safe actions and blocked live-action gates.
- `scripts/next_loop_controller.py` runs one approval-bounded verification/reporting pass.
- `docs/autonomy/README.md` documents local and CI usage.
- `.github/workflows/next-loop.yml` exposes a manual GitHub Actions workflow for the same controller.

Gate preserved: Loop 38 does not auto-commit, push, publish, sign, spend, contact people, use wallets or production/private personal keys, or run live IPFS/Nostr/Radicle actions. It stops before stronger durability, censorship-resistance, security, SLSA, broad-availability, or production-readiness claims unless a future explicit target is recorded.

### Loop 39: Standing live-action approval recorded

Status: **complete as controller permission update; no live protocol/storage/signing action executed in this loop**.

Eric stated on 2026-06-28: "For what its worth I am totally ok with live IPFS/Radicle/Nostr/signing actions." The controller now records that standing approval for free, disposable or project-scoped, low-volume, secret-free, evidence-labeled live IPFS, Radicle, Nostr, and signing/provenance actions.

Gate preserved: Spending, wallets, paid infrastructure, production/private personal keys, direct outreach, persistent public seed/background services, and stronger durability/censorship/security/SLSA/broad-availability/production-readiness claims still require separate approval.

### Loop 40: GitHub keyless artifact attestation workflow

Status: **complete as hosted keyless attestation evidence; registry fixture provenance remains synthetic**.

Outputs:

- `.github/workflows/ci.yml` now grants `id-token: write`, `attestations: write`, and `artifact-metadata: write`.
- The `ci` workflow runs `actions/attest@v4` on `main` push after the local verification suite and worktree-clean check.
- Attestation subjects are `output/demo-project.html`, `output/portable-lab.html`, `output/demo-project.summary.json`, `output/portable-lab.summary.json`, `evidence/local-release-artifact-2026-06-22.car`, and `fixtures/local-release-artifact.txt`.
- GitHub Actions run https://github.com/redclawanon-rgb/decentralized-forge/actions/runs/28339280081 passed and the attestation step completed successfully.
- `evidence/github-keyless-attestation-2026-06-28.json` records the run, subject digests, SLSA provenance predicate, builder identity, invocation URL, resolved commit, and transparency-log entry count.

Gate preserved: This uses GitHub OIDC/keyless hosted attestations and no production/private personal signing key. It does not claim local registry provenance fields are imported, SLSA-compliant, production-ready, or consumer-verified.

### Loop 41: Local Helia/IPFS add-get fixture verification

Status: **complete as local in-process Helia add/get evidence; no public storage or durability claim**.

Outputs:

- Added project-scoped dev dependencies `helia@6.1.4` and `@helia/unixfs@7.2.1`.
- Added `scripts/verify_helia_fixture.mjs` and npm script `verify:helia`.
- `npm run verify:helia` creates a non-started offline in-memory project-scoped Helia instance with no libp2p listeners, transports, discovery, routers, or block brokers; adds `fixtures/local-release-artifact.txt`; reads it back with UnixFS `cat`; and writes `evidence/helia-local-ipfs-add-get-2026-06-28.json`.
- The recorded CID is `bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua`; readback SHA-256 matches `3932e28d5b609b3cae25218ca205ea126cd3cf344628dc4c4b9bf094c50668a0`.
- `fixtures/live-evidence-index.json`, `output/demo-project.html`, CI, docs, and tests now include the Loop 41 evidence row.

Gate preserved: This is local offline Helia add/get evidence only. No public gateway was queried, no pinning service was used, no paid storage or wallet was used, no persistent daemon/background service was started, and no durability, global availability, censorship-resistance, security, or production-readiness claim is made.

## Verification requirements

- Each protocol claim should include source URL and retrieval date where possible.
- Research must separate observed facts from recommendations.
- Public building is approved for this project in the current all-night controller run: GitHub publishing/pushes, public project updates, and public collaboration surfaces are allowed when accurate, non-spammy, and labeled as research/prototype work.
- No spending unless separately approved.
- No production/private keys for protocol actions unless separately approved.
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
- Treat current Nostr, Radicle, IPFS, ForgeFed, and provenance data as fixtures/mappings unless a loop records live command/network verification. As of Loop 39, free/disposable/project-scoped live IPFS, Radicle, Nostr, and signing/provenance actions are approved.
- Use the completed local NIP-34 parser/conformance adapter, repository state/status fixture, local NIP-01 conformance reports, adapter verification-state exports, and rendered fixture-adapter/conformance/verification sections as the seam for future Nostr UI/import work, while keeping relay publishing behind disposable-key and explicit relay gates.
- Use the completed safe live-gated replay plan/checklist as the prerequisite gate for Radicle/Nostr live verification. As of Loop 35, `rad` and `nak` are installed user-locally, a disposable project Nostr key exists outside the repo, a Radicle temporary-`RAD_HOME` disposable private replay succeeded locally, Nostr selected-relay publish/readback has been executed for one prototype event, and one disposable public Radicle seed/clone/readback smoke succeeded for exact RID `rad:z2WtozFrCRhygh9CGzyUN57CN7Nwa`.
- Treat Radicle as verified only for (a) the narrow disposable private local replay path and (b) the exact Loop 34 disposable public seed/clone/readback smoke; do not claim durable availability, censorship resistance, security, global replication, identity trust, production readiness, full Radicle compatibility, or broad Radicle network availability.
- Keep ForgeFed as a later object-shape/federation bridge; do not run a public actor until moderation/security gates exist.
- Keep IPFS/CIDs as artifact metadata plus exact local CAR/CID and local Helia add/get evidence. Public gateway checks, pinning, paid storage, Filecoin, and Arweave still require specific targets and stronger evidence because they imply availability, account/token, spending, or wallet decisions.
- Keep Sigstore/in-toto/SLSA as release/build trust models; current provenance is synthetic and no SLSA level should be claimed.
- Use `output/forge-app.html` as the first local product surface for inspecting projects, evidence, releases, selected-relay Nostr issue/patch readback, and unsigned Nostr collaboration drafts. Keep it static and non-publishing until a separate relay-signing/publish flow is designed and verified.

### Loops 42-45: Requested live/import loop set

Status: **complete as bounded evidence; no durability, broad availability, SLSA, security, or production claim**.

Outputs:

- Loop 42 queried three public gateways for CID `bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua`; all timed out and zero matching readbacks were observed. No pinning provider, token, paid storage, wallet, daemon, or persistent service was used.
- Loop 43 used project-scoped `nostr-tools@2.23.8` and an in-memory disposable key to publish and read back one NIP-34-shaped issue event and one patch event from `wss://relay.damus.io` and `wss://nos.lol`. Secret key material is not recorded.
- Loop 44 found no `rad` CLI on this Windows host, so broader Radicle CLI clone/sync is blocked here; it recorded only read-only public route probes for prior disposable RID `rad:z2WtozFrCRhygh9CGzyUN57CN7Nwa`.
- Loop 45 imported hosted keyless attestation evidence into `fixtures/keyless-attestation.registry-verification.json` as a registry-shaped row outside the project-registry fixtures. The `ci.provenance` fixture row remains synthetic.
- `fixtures/live-evidence-index.json`, renderer output, docs, and tests now include Loops 42-45.

Gate preserved: No spending, paid infrastructure, wallet, production/private personal key, direct outreach, persistent service, pinning action, Radicle CLI action, registry provenance replacement, SLSA compliance claim, durability claim, broad availability claim, censorship-resistance claim, security guarantee, or production-readiness claim was introduced.

### Loop 46: Trust hardening and public-tool readiness

Status: **complete as local trust-contract hardening; no new live protocol/storage/signing action**.

Outputs:

- `schemas/live-evidence-index.schema.json` defines the live evidence index shape.
- `fixtures/live-evidence-index.json` now records `evidence_sha256` and `evidence_size_bytes` for each source evidence file.
- `scripts/forge_registry.py` now includes `validate-evidence-index`, `refresh-evidence-hashes`, and read-only `doctor` commands.
- CI and `verify-local` check evidence hashes, evidence path bounds, selected secret markers, and claim-boundary guardrails.
- `docs/threat-model.md` records what the tool helps with and what it does not yet solve.
- `docs/community-quickstart.md` explains the current community verification workflow and future bundle/import direction.

Gate preserved: Loop 46 performs local validation, hashing, documentation, and rendering only. It does not run live Nostr/Radicle/IPFS actions, spend money, use wallets, use production/private personal keys, start persistent services, replace registry provenance, or introduce durability, censorship-resistance, broad-availability, security, SLSA, or production-readiness claims.

### Loop 47: Static forge workbench app

Status: **complete as a local static workbench app; no protocol publishing or signing action**.

Outputs:

- `scripts/render_forge_app.py` generates `output/forge-app.html` from committed registry fixtures, the live evidence index, NIP-34 fixture/readback data, Loop 43 issue/patch selected-relay readback evidence, and the registry-shaped keyless-attestation import.
- `scripts/forge_registry.py render-app output/forge-app.html` is part of `verify-local` and CI.
- The workbench includes project overview metrics, issues/patches, release/artifact evidence, evidence filtering, and an unsigned local Nostr issue/patch draft generator.
- `.github/workflows/ci.yml` includes `output/forge-app.html` in generated-artifact verification and keyless attestation subjects.

Verified evidence:

- `python -m unittest discover -s tests` passed, 67 tests.
- Headless Chrome DevTools verification loaded `output/forge-app.html` and exercised overview, collaboration filtering, evidence filtering, and unsigned issue/patch draft generation.

Gate preserved: Loop 47 is local static UI generation only. It does not open WebSockets, fetch from relays, sign events, publish events, import private keys, spend money, use wallets, start persistent services, replace registry provenance, or introduce durability, censorship-resistance, broad-availability, security, SLSA, or production-readiness claims.

### Loop 48: Portable verification bundle

Status: **complete as deterministic local bundle export/verification; no live protocol/storage/signing action**.

Outputs:

- `scripts/forge_registry.py export-bundle output/decentralized-forge-verification-bundle.zip` regenerates the portable outputs and writes a deterministic ZIP with fixed file order and ZIP metadata.
- The bundle includes schemas, fixtures, source evidence files, generated HTML, deterministic summaries, `output/forge-app.html`, verifier scripts, package metadata, and `verification-bundle.manifest.json`.
- `scripts/forge_registry.py verify-bundle output/decentralized-forge-verification-bundle.zip` validates the manifest, file sizes, SHA-256 hashes, required payloads, and live-evidence-index evidence bindings.
- CI exports/verifies the bundle and includes it in keyless artifact attestation subjects.

Verified evidence:

- `python -m unittest tests.test_registry_fixture.RegistryFixtureTests.test_verification_bundle_is_current_and_self_verifying` passed.
- Bundle verification passed for `output/decentralized-forge-verification-bundle.zip`; manifest records 56 payload files and 9 indexed evidence entries.

Gate preserved: Loop 48 packages existing local/generated evidence only. It does not publish protocol events, sign events, fetch from relays, pin storage, start daemons, spend money, use wallets, import private keys, replace registry provenance, or introduce durability, censorship-resistance, broad-availability, security, SLSA, or production-readiness claims.

### Loop 49: Clean-room bundle consumer check

Status: **complete as temporary extraction/import verification; no live protocol/storage/signing action**.

Outputs:

- `scripts/forge_registry.py verify-bundle-cleanroom output/decentralized-forge-verification-bundle.zip` verifies the ZIP directly, safely extracts it to a temporary directory, copies the ZIP into that extracted tree, and runs bundled verification commands from the extracted tree.
- The clean-room path validates `verification-bundle.manifest.json`, `verify-bundle`, `validate-evidence-index`, and static artifact preflight without relying on the original checkout's files.
- The bundle manifest now lists `verify-bundle-cleanroom` as a suggested verification command.
- CI runs the clean-room verifier after exporting and direct-verifying the bundle.

Verified evidence:

- `python scripts/forge_registry.py verify-bundle-cleanroom output/decentralized-forge-verification-bundle.zip` passed locally.
- The bundle remains deterministic across Windows and Linux container generation.

Gate preserved: Loop 49 only unpacks and verifies the local bundle in temporary storage. It does not publish protocol events, sign events, fetch from relays, pin storage, start daemons, spend money, use wallets, import private keys, replace registry provenance, or introduce durability, censorship-resistance, broad-availability, security, SLSA, or production-readiness claims.

### Loop 50: Bundle import/report command

Status: **complete as local bundle import/readback reporting; no live protocol/storage/signing action**.

Outputs:

- `scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip` reads a portable bundle ZIP and emits a human review report.
- `scripts/forge_registry.py report-bundle <extracted-bundle-dir> --json` reads an extracted bundle directory and emits deterministic JSON with project identity summaries, file role counts, evidence protocol/state counts, non-claims, verification gaps, and suggested commands.
- The bundle manifest now lists `report-bundle` as a suggested verification command.
- CI runs the report command in JSON mode after exporting and verifying the bundle.

Verified evidence:

- `python scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip` produced a valid report locally.
- Tests assert that ZIP and extracted-directory reports are valid and agree on bundle/evidence content.

Gate preserved: Loop 50 only reads committed/generated local bundle contents and produces a summary. It does not publish protocol events, sign events, fetch from relays, pin storage, start daemons, spend money, use wallets, import private keys, replace registry provenance, or introduce durability, censorship-resistance, broad-availability, security, SLSA, or production-readiness claims.

### Loop 51: Portable bundle review checklist

Status: **complete as release-facing review guidance; no live protocol/storage/signing action**.

Outputs:

- `docs/portable-bundle-review-checklist.md` defines required local checks, `report-bundle` review expectations, non-claims, attachment metadata, stop conditions, and a neutral release-note template.
- The checklist is included in `output/decentralized-forge-verification-bundle.zip` so bundle consumers receive the review guidance with the evidence package.
- `docs/community-quickstart.md`, `README.md`, `COMPLETION-CRITERIA.md`, `AGENT-LOOPS.md`, and `.hermes/context.md` now describe the checklist as part of the portable bundle workflow.

Verified evidence:

- Tests assert the checklist includes the required bundle verification/report commands and preserves non-claim boundaries.
- Bundle export includes `docs/portable-bundle-review-checklist.md` as documentation payload.

Gate preserved: Loop 51 only adds local review documentation. It does not publish protocol events, sign events, fetch from relays, pin storage, start daemons, spend money, use wallets, import private keys, replace registry provenance, or introduce durability, censorship-resistance, broad-availability, security, SLSA, or production-readiness claims.

### Loop 52: Bundle release-note export

Status: **complete as deterministic release-facing markdown export; no live protocol/storage/signing action**.

Outputs:

- `scripts/forge_registry.py export-bundle-release-note output/decentralized-forge-verification-bundle.zip` emits a markdown release note to stdout by default, or writes a file when an output path is supplied.
- The release note includes the exact current Git commit SHA, bundle SHA-256, bundle byte size, verification status, project summaries, required commands, non-claims, verification gaps, checklist stop conditions, and attachment list.
- `npm run report:bundle-release-note`, CI, `verify-local`, the bundle manifest suggested commands, README, community quickstart, completion criteria, and checklist now reference the command.

Verified evidence:

- Tests assert the release note includes the current commit SHA, bundle digest field, required verification/report commands, project IDs, stop conditions, and non-claim boundaries, and that optional file output is byte-for-byte the generated note.
- CI runs `export-bundle-release-note` after bundle export, direct verification, clean-room verification, and JSON bundle reporting.

Gate preserved: Loop 52 only reads local committed/generated evidence and emits markdown. It does not publish protocol events, sign events, fetch from relays, pin storage, start daemons, spend money, use wallets, import private keys, replace registry provenance, or introduce durability, censorship-resistance, broad-availability, security, SLSA, or production-readiness claims.

### Loop 53: Local registry import scaffold

Status: **complete as local Git worktree scaffold; no live protocol/storage/signing action**.

Outputs:

- `scripts/forge_registry.py scaffold-registry <repo> <output>` creates a valid starter project registry fixture from a local Git worktree.
- The scaffold records project id/name/default branch, a `file://` Git clone URL, placeholder maintainer identity, empty issues/patches/releases, absent IPFS/provenance claims, unsigned fixture signature, and a `registry.local_import_scaffold` verification state.
- The command validates the written fixture immediately and prints next-step guidance for validation, summary export, rendering, identity review, artifact evidence, and non-claim preservation.
- `npm run scaffold:registry -- <repo> <output>` exposes the same workflow through package scripts.

Verified evidence:

- Tests create a temporary Git repository, commit a file, scaffold a registry fixture from it, validate the fixture, and assert placeholder identity and non-claim boundaries.

Gate preserved: Loop 53 only reads local Git metadata and writes a local fixture. It does not publish protocol events, sign events, fetch from remotes, pin storage, start daemons, spend money, use wallets, import private keys, replace registry provenance, or introduce durability, censorship-resistance, broad-availability, security, SLSA, or production-readiness claims.

### Loop 54: Local artifact metadata attach

Status: **complete as local file artifact metadata; no IPFS/storage/signing action**.

Outputs:

- `scripts/forge_registry.py attach-local-artifact <registry> <artifact>` updates a registry fixture in place with a release artifact entry.
- The command records raw file SHA-256, byte size, media type, `file://` URI, local-only availability, unsigned local artifact metadata, and a `registry.local_artifact_metadata` verification state.
- Re-running the command with the same release/tag/artifact name replaces the existing artifact entry instead of duplicating it.
- `npm run attach:artifact -- <registry> <artifact> --version <version>` exposes the same workflow through package scripts.

Verified evidence:

- Tests create a temporary Git repository, scaffold a registry, attach a CRLF-containing local artifact, validate the output, assert raw-byte SHA-256/size/media-type/URI fields, assert idempotency, and check non-claim boundaries.

Gate preserved: Loop 54 only reads local file bytes and updates a local fixture. It does not publish protocol events, sign events, fetch from relays or gateways, add/fetch/pin IPFS content, start daemons, spend money, use wallets, import private keys, replace registry provenance, or introduce durability, censorship-resistance, broad-availability, security, SLSA, or production-readiness claims.

### Loop 55: Local project onboarding command

Status: **complete as chained local onboarding; no live protocol/storage/signing action**.

Outputs:

- `scripts/forge_registry.py onboard-local-project <repo> <artifact>` chains local registry scaffold, local artifact metadata attachment, validation, summary export, HTML rendering, verification bundle refresh, bundle verification, and bundle report generation.
- The command defaults to `fixtures/<project-id>.registry.json`, `output/<registry-stem>.summary.json`, `output/<registry-stem>.html`, and `output/decentralized-forge-verification-bundle.zip`, with options to override each output for dry runs.
- `collect_verification_bundle_paths()` now includes repository-local `output/*.html` and `output/*.summary.json` generated outputs in addition to the fixed workbench artifacts.
- `npm run onboard:local-project -- <repo> <artifact> --project-id <id> --version <version>` exposes the workflow through package scripts.

Verified evidence:

- Tests create a temporary Git repository and binary artifact, run the onboarding command with temporary output paths, validate the registry, inspect summary/HTML output, verify the produced bundle, and assert the report/non-claim boundaries.

Gate preserved: Loop 55 only reads local Git metadata and local file bytes, then writes local fixture/generated/bundle/report outputs. It does not publish protocol events, sign events, fetch from relays or gateways, add/fetch/pin IPFS content, start daemons, spend money, use wallets, import private keys, replace registry provenance, or introduce durability, censorship-resistance, broad-availability, security, SLSA, or production-readiness claims.

### Loop 56: Committed onboarding sample

Status: **complete as committed local onboarding sample; no live protocol/storage/signing action**.

Outputs:

- `fixtures/onboarding-sample-artifact.txt` is a small local-only artifact used to demonstrate onboarding metadata.
- `fixtures/onboarding-sample.registry.json` was generated through `onboard-local-project` from this repository, records a repo-relative `file://.` clone URL, placeholder maintainer identity, local-only artifact metadata, and explicit non-claims.
- `output/onboarding-sample.registry.summary.json` and `output/onboarding-sample.registry.html` are the generated summary/page for the committed sample.
- `output/onboarding-sample.bundle-report.json` is generated by `report-bundle --json --output` after bundle refresh.
- CI and `verify-local` now validate the onboarding sample and regenerate the sample bundle report before the worktree-clean check.

Verified evidence:

- Tests validate the committed onboarding registry, check artifact SHA-256/size/URI against the committed artifact bytes, assert the scaffold commit remains current or an ancestor, compare regenerated HTML/summary/report output, and check non-claim boundaries.

Gate preserved: Loop 56 uses committed local files and local Git metadata only. It does not publish protocol events, sign events, fetch from relays or gateways, add/fetch/pin IPFS content, start daemons, spend money, use wallets, import private keys, replace registry provenance, or introduce durability, censorship-resistance, broad-availability, security, SLSA, or production-readiness claims.

### Loop 57: Optional workbench import for onboarding sample

Status: **complete as static workbench import path; no live protocol/storage/signing action**.

Outputs:

- `output/forge-app-with-onboarding-sample.html` is generated by `render-app` with explicit registries: demo project, portable lab, and onboarding sample.
- The default `output/forge-app.html` remains the two-project workbench; the onboarding sample import is opt-in through repeated `--registry` arguments.
- CI and `verify-local` regenerate the optional workbench before bundle export and the worktree-clean check.
- The optional workbench is included in the verification bundle and GitHub attestation subject list.

Verified evidence:

- Tests regenerate the optional workbench, compare it to the committed output, inspect embedded app data for the three expected projects, assert the onboarding artifact appears, and preserve no-fetch/no-sign/no-publish runtime checks.

Gate preserved: Loop 57 only renders committed local registry/evidence data into static HTML. It does not publish protocol events, sign events, fetch from relays or gateways, add/fetch/pin IPFS content, start daemons, spend money, use wallets, import private keys, replace registry provenance, or introduce durability, censorship-resistance, broad-availability, security, SLSA, or production-readiness claims.

### Loop 58: Workbench project set handoff

Status: **complete as static in-app recreate command; no live protocol/storage/signing action**.

Outputs:

- `scripts/render_forge_app.py` now embeds `generated_from.output` and renders a Project set screen.
- `output/forge-app.html` and `output/forge-app-with-onboarding-sample.html` list their embedded registry source paths and show a copyable `render-app --registry ...` command for recreating the current project set.
- The default workbench command remains the two-project set; the onboarding sample workbench command includes the onboarding registry as the third `--registry` input.

Verified evidence:

- Tests regenerate both workbenches, compare them to the committed outputs, assert the embedded output/registry source paths, and preserve no-fetch/no-sign/no-publish runtime checks.

Gate preserved: Loop 58 only renders committed local registry/evidence data into static HTML. It does not publish protocol events, sign events, fetch from relays or gateways, add/fetch/pin IPFS content, start daemons, spend money, use wallets, import private keys, replace registry provenance, or introduce durability, censorship-resistance, broad-availability, security, SLSA, or production-readiness claims.

### Loop 59: Project-scoped Radicle repository smoke

Status: **complete as first project-scoped Radicle repo evidence; no durability/broad-availability/security/production claim**.

Outputs:

- `scripts/run_radicle_project_repo_smoke.py` runs a Docker/Linux-oriented Radicle smoke using temporary seed and clone `RAD_HOME` directories.
- `evidence/radicle-project-repo-smoke-2026-06-29.json` and `.md` record the current `decentralized-forge` checkout at commit `fd3f1898d81a4b00be9095c62e3c07fc1a792a95` initialized as public Radicle RID `rad:zWGy1Ssjb7tBbwDbdGLqeHCsUqwr`.
- The smoke started a temporary seed node, ran publish/seed/sync, connected a separate temporary Radicle profile, cloned the RID, and verified the cloned Git commit matched the source commit.
- `fixtures/live-evidence-index.json` now imports the Loop 59 evidence row and bumps the live evidence index to loop 59.
- `output/forge-app.html`, `output/forge-app-with-onboarding-sample.html`, and the portable verification bundle now include the Loop 59 evidence row.

Verified evidence:

- Direct evidence tests assert RID shape, public visibility, source/clone commit equality, seed/sync/clone success, separate-profile readback, and no secret-marker leakage.
- Evidence-index tests assert canonical evidence hash/size metadata and bounded non-claims.

Gate preserved: Loop 59 uses temporary project-scoped Radicle state in a Linux container. It does not keep a persistent seed, use production/private personal keys, spend money, use paid infrastructure, contact specific people, or introduce durability, censorship-resistance, broad-network-availability, security, SLSA, identity-trust, or production-readiness claims.

### Loop 60: Fresh-state Radicle RID readback

Status: **complete as fresh temporary-profile readback observed; no permanent-durability/security/production claim**.

Outputs:

- `scripts/run_radicle_fresh_readback_check.py` runs a Docker/Linux-oriented Radicle readback check using a brand-new temporary `RAD_HOME`.
- `evidence/radicle-fresh-readback-check-2026-06-29.json` and `.md` record a successful clone of `rad:zWGy1Ssjb7tBbwDbdGLqeHCsUqwr` at expected commit `fd3f1898d81a4b00be9095c62e3c07fc1a792a95`.
- The check did not reuse the original Loop 59 seed profile and did not explicitly connect to the original seed node with `rad node connect` or `--seed`.
- `fixtures/live-evidence-index.json` now imports the Loop 60 evidence row and bumps the live evidence index to loop 60.

Verified evidence:

- Direct evidence tests assert schema, target RID, expected/clone commit equality, fresh-profile boundaries, no explicit original-seed command, and no secret-marker leakage.
- Evidence-index tests assert the Loop 60 row, canonical evidence hash/size metadata, fresh readback state, and bounded non-claims.

Gate preserved: Loop 60 is one exact fresh-state readback observation through Radicle's normal network path. It does not keep a persistent seed, use production/private personal keys, spend money, use paid infrastructure, contact specific people, or introduce permanent-durability, censorship-resistance, global-replication, security, SLSA, identity-trust, full-compatibility, or production-readiness claims.

### Loop 61: Radicle update continuity check

Status: **complete as fresh-peer same-RID publication observed; canonical/default update continuity not yet observed**.

Outputs:

- `scripts/run_radicle_update_continuity_check.py` runs a Docker/Linux-oriented same-RID update-continuity check using fresh non-original Radicle identities.
- `evidence/radicle-update-continuity-check-2026-06-29.json` and `.md` record a successful push of current commit `00404656bcb17ad1aab241fb0ab0dd60487d9699` to `rad:zWGy1Ssjb7tBbwDbdGLqeHCsUqwr` under a fresh peer namespace.
- A separate fresh readback clone still checked out the original delegate main at `fd3f1898d81a4b00be9095c62e3c07fc1a792a95`.
- `fixtures/live-evidence-index.json` now imports the Loop 61 evidence row and bumps the live evidence index to loop 61.

Verified evidence:

- Direct evidence tests assert prior/current commit ancestry, fresh-peer push success, same-RID peer namespace publication, default readback remaining on the original delegate commit, and no secret-marker leakage.
- Evidence-index tests assert the Loop 61 row, canonical evidence hash/size metadata, fresh-peer/default-readback boundary, and bounded non-claims.

Gate preserved: Loop 61 does not reuse the original Loop 59 delegate key, keep persistent seed state, use production/private personal keys, spend money, contact specific people, or introduce canonical-continuity, permanent-durability, censorship-resistance, global-replication, security, SLSA, identity-trust, full-compatibility, or production-readiness claims.

### Loop 62: Retained Radicle maintainer lane

Status: **complete as retained project-scoped maintainer RID with fresh default and direct-seed readback**.

Outputs:

- `scripts/run_radicle_retained_delegate_check.py` creates or reuses gitignored project-scoped Radicle maintainer state under `.tmp/radicle-retained-delegate`.
- `evidence/radicle-retained-delegate-check-2026-06-29.json` and `.md` record retained RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` for source commit `dfc10b8f029c5eb886db2025dcc06c6490e28504`.
- A fresh default clone read back commit `dfc10b8f029c5eb886db2025dcc06c6490e28504`.
- An explicit direct-seed clone from the retained node also read back commit `dfc10b8f029c5eb886db2025dcc06c6490e28504`.
- `fixtures/live-evidence-index.json` now imports the Loop 62 evidence row and bumps the live evidence index to loop 62.

Verified evidence:

- Direct evidence tests assert retained state stays under gitignored `.tmp`, no secret values are recorded, the retained RID/delegate/peer identifiers are public-shaped, the worktree/source commits match, publish/seed/sync succeeded, and both default and direct-seed readbacks matched the source commit.
- Evidence-index tests assert the Loop 62 row, canonical evidence hash/size metadata, retained-state non-commitment, matching readback commits, and bounded non-claims.

Gate preserved: Loop 62 does not commit or bundle the retained Radicle secret state, keep a persistent public seed service running, use production/private personal keys, spend money, contact specific people, or introduce permanent-durability, future-default-routing-availability, censorship-resistance, global-replication, security, SLSA, identity-trust, full-compatibility, or production-readiness claims.

### Loop 63: Retained Radicle same-RID update

Status: **complete as retained same-RID update with fresh direct-seed readback; default public-routing readback not observed in this run**.

Outputs:

- `scripts/run_radicle_retained_update_check.py` reuses retained project-scoped Radicle maintainer state without Docker.
- `evidence/radicle-retained-update-check-2026-06-29.json` and `.md` record the same retained RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` advancing from commit `dfc10b8f029c5eb886db2025dcc06c6490e28504` to commit `f800bae387f33452fdeb79ecf5c795d25f7246ac`.
- The final passing run used host-local Ubuntu WSL retained state, avoiding Docker exposure for secret-bearing Radicle state and avoiding Radicle node sockets on the Windows-mounted filesystem.
- A fresh explicit direct-seed clone read back commit `f800bae387f33452fdeb79ecf5c795d25f7246ac`.
- Fresh default public-routing clone was attempted but did not read back the updated commit in this run.
- `fixtures/live-evidence-index.json` now imports the Loop 63 evidence row and bumps the live evidence index to loop 63.

Verified evidence:

- Direct evidence tests assert same RID, prior/current ancestry, update advancement, retained profile availability, matching worktree/current commit, successful push, successful explicit direct-seed readback, default public-routing non-observation, and no secret-marker leakage.
- Evidence-index tests assert the Loop 63 row, canonical evidence hash/size metadata, retained-state non-commitment, direct-seed readback boundary, and bounded non-claims.

Gate preserved: Loop 63 does not commit or bundle retained Radicle secret state, keep a persistent public seed service running, use production/private personal keys, spend money, contact specific people, or introduce permanent-durability, future-default-routing-availability, censorship-resistance, global-replication, security, SLSA, identity-trust, full-compatibility, or production-readiness claims.

## Loop 64: Retained RID community direct-seed quickstart

Outputs:

- `docs/radicle-retained-rid-quickstart.md` documents the current community clone path for retained RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`.
- `python scripts/forge_registry.py radicle-retained-quickstart` now emits an evidence-derived recipe and optional JSON model from `fixtures/live-evidence-index.json`.
- The helper checks that Loop 63 direct-seed readback matched commit `f800bae387f33452fdeb79ecf5c795d25f7246ac`, that default public-routing readback was not observed, and that retained secret state was not committed or recorded.
- `docs/community-quickstart.md`, `docs/portable-bundle-review-checklist.md`, README, tests, and the portable bundle manifest now include the quickstart path.

Gate preserved: Loop 64 is documentation and read-only local CLI output only. It does not start Radicle nodes, connect to peers, clone, publish, sign, use private keys, expose retained secret state, run a persistent seed, or introduce permanent-durability, default-routing-availability, broad-network-availability, censorship-resistance, security, identity-trust, full-compatibility, or production-readiness claims.

## Loop 65: Retained RID independent follower-seed readback

Outputs:

- `scripts/run_radicle_independent_availability_check.py` advances the retained RID to the current checkout and tests an independent follower-seed handoff.
- `evidence/radicle-independent-availability-check-2026-06-29.json` and `.md` record retained RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` advancing to commit `7262f69b82e442263d6261414f6b771be04c6b6f`.
- Reader A used a fresh temporary Radicle profile to clone from the retained maintainer seed.
- Reader A then seeded the RID from its temporary profile.
- Reader B used another fresh temporary Radicle profile to clone from reader A and read back the same commit.
- `fixtures/live-evidence-index.json` now imports the Loop 65 evidence row and bumps the live evidence index to loop 65.
- `docs/radicle-persistent-seed-plan.md` records the minimum plan for a future reachable/persistent seed service without turning one on in this loop.

Verified evidence:

- Direct evidence tests assert same retained RID, current source commit, reader A readback, follower seed success, reader B readback, temporary reader-state removal, secret-free committed evidence, and non-claim boundaries.
- The retained quickstart helper now prefers the Loop 65 row when present and prints commit `7262f69b82e442263d6261414f6b771be04c6b6f`.

Gate preserved: Loop 65 does not commit or bundle retained Radicle secret state, keep a persistent public seed service running, use production/private personal keys, spend money, contact specific people, or introduce permanent-durability, future-default-routing-availability, censorship-resistance, global-replication, security, SLSA, identity-trust, full-compatibility, or production-readiness claims.

## Loop 66: Retained seed restart/readback rehearsal

Outputs:

- `scripts/run_radicle_seed_restart_check.py` advances the retained RID to the current checkout and tests retained seed restart/readback behavior.
- `evidence/radicle-seed-restart-check-2026-06-29.json` and `.md` record retained RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` advancing to commit `4c8cd6183e2e12d1c62af7d2f013fb085b2d6bf8`.
- A first fresh temporary Radicle profile cloned from the retained seed before restart.
- The retained seed stopped and restarted on `127.0.0.1:8799` with the same retained node ID.
- A second fresh temporary Radicle profile cloned from the retained seed after restart and read back the same commit.
- `fixtures/live-evidence-index.json` now imports the Loop 66 evidence row and bumps the live evidence index to loop 66.
- The retained quickstart helper now prefers the Loop 66 row when present and prints commit `4c8cd6183e2e12d1c62af7d2f013fb085b2d6bf8`.

Verified evidence:

- Direct evidence tests assert same retained RID, current source commit, pre-restart readback, retained seed stop, post-restart same node ID, post-restart readback, final stop, secret-free committed evidence, and non-claim boundaries.
- Evidence-index tests assert the Loop 66 row, canonical evidence hash/size metadata, no public seed reachability claim, no separate-host readback claim, retained-state non-commitment, and bounded non-claims.

Gate preserved: Loop 66 does not publish a stable public seed address, prove separate-network reachability, leave a persistent public seed service running, commit or bundle retained Radicle secret state, use production/private personal keys, spend money, contact specific people, or introduce permanent-durability, future-default-routing-availability, censorship-resistance, global-replication, security, SLSA, identity-trust, full-compatibility, or production-readiness claims.

## Loop 67: Public VPS follower-seed readback

Outputs:

- `evidence/radicle-vps-follower-public-readback-2026-06-29.json` and `.md` record the first public direct-seed readback for retained RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`.
- The `openclaw` VPS follower seed runs at `z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776`.
- The VPS follower seed is a fresh follower identity; retained maintainer key material was not copied to the VPS.
- A fresh reader on `ubuntu-work` connected to the public VPS seed, cloned the retained RID, and read back commit `610fc3da9757d0cb123aa5976db552b991b766d4`.
- `fixtures/live-evidence-index.json` now imports the Loop 67 evidence row and bumps the live evidence index to loop 67.
- The retained quickstart helper now prefers the Loop 67 row and prints the public VPS seed address.

Verified evidence:

- TCP reachability to `187.77.19.162:8776` was observed from the coordinator and from `ubuntu-work`.
- Direct evidence tests assert public seed address, fresh-reader readback, retained-state non-copy to VPS, secret-free committed evidence, and non-claim boundaries.

Gate preserved: Loop 67 does not copy retained maintainer key material to the VPS, commit or bundle secret state, use production/private personal keys, introduce new spending beyond the already-available VPS, contact specific people, or introduce permanent-durability, future-default-routing-availability, censorship-resistance, global-replication, security, SLSA, identity-trust, full-compatibility, or production-readiness claims.

## Next recommended loop

**Next:** Add independent mirror/fallback seed coverage or a scheduled external health-check readout. The caveat remains that permanent durability still requires independent operators, backups, and repeated checks over time.

Recent completed loops:

- Loop 33: local CAR/CID fixture verification — complete as project-scoped `@ipld/car`/`multiformats` evidence in `evidence/local-car-cid-fixture-2026-06-22.json`; no live storage action.
- Loop 34: disposable public Radicle seed/remote-clone smoke — complete as exact bounded evidence in `evidence/radicle-public-network-smoke-2026-06-22.json`; RID `rad:z2WtozFrCRhygh9CGzyUN57CN7Nwa`; no broad durability/censorship/security/production/network-availability claim.
- Loop 35: consolidation/report — complete as `evidence/loop35-consolidation-2026-06-22.md` plus checklist/test/context/status updates; no new live protocol/storage action, public update, or cron job.
- Loop 36: hosted local-verification CI and Milestone 1 completion state — complete as `.github/workflows/ci.yml` plus `COMPLETION-CRITERIA.md` updates; CI passed on `main`; no signing/SLSA/live protocol/storage claim.
- Loop 37: public Milestone 1 update — complete as GitHub Discussion #7: https://github.com/redclawanon-rgb/decentralized-forge/discussions/7; no new live protocol/storage/signing action.

- Loop 38: approval-bounded next-loop controller - complete as config, script, docs, tests, npm scripts, and manual GitHub Actions workflow; no background daemon or live action.
- Loop 39: standing live-action approval recorded - complete as controller/status/test updates; no live protocol/storage/signing action executed in this loop.
- Loop 40: GitHub keyless artifact attestation workflow - complete as hosted keyless attestation evidence in `evidence/github-keyless-attestation-2026-06-28.json`.
- Loop 41: local Helia/IPFS add-get fixture verification - complete as project-scoped local add/get evidence in `evidence/helia-local-ipfs-add-get-2026-06-28.json`; no public gateway, pinning, paid storage, wallet, persistent daemon, or durability/security/production claim.
- Loop 42: public gateway/pinning preflight - complete as three public gateway timeouts and no pinning action in `evidence/public-gateway-pinning-preflight-2026-06-28.json`.
- Loop 43: Nostr issue/patch readback - complete as two disposable selected-relay collaboration events in `evidence/nostr-loop43-issue-patch-readback-2026-06-28.json`.
- Loop 44: broader Radicle check - complete as current-host `rad` CLI blocker plus read-only route probes in `evidence/radicle-loop44-broader-check-2026-06-28.json`.
- Loop 45: registry-shaped keyless-attestation import - complete as `fixtures/keyless-attestation.registry-verification.json`; project registry provenance remains synthetic.
- Loop 46: trust hardening and public-tool readiness - complete as evidence hash checks, read-only doctor output, schema validation, threat model, and community quickstart.
- Loop 47: static forge workbench app - complete as `scripts/render_forge_app.py` plus `output/forge-app.html`; app remains static, local, unsigned, and non-publishing.
- Loop 48: portable verification bundle - complete as `output/decentralized-forge-verification-bundle.zip` plus `export-bundle`/`verify-bundle`; bundle remains local evidence packaging, not a signing/durability/security proof.
- Loop 49: clean-room bundle consumer check - complete as `verify-bundle-cleanroom`; verifies an extracted temporary bundle tree without relying on the original checkout.
- Loop 50: bundle import/report command - complete as `report-bundle`; summarizes ZIP or extracted bundle contents for human review without live action.
- Loop 51: portable bundle review checklist - complete as `docs/portable-bundle-review-checklist.md`; gives maintainers required checks, non-claims, attachments, stop conditions, and neutral release-note wording.
- Loop 52: bundle release-note export - complete as `export-bundle-release-note`; emits shareable markdown tied to the current commit, bundle digest, report summary, non-claims, gaps, and checklist stop conditions.
- Loop 53: local registry import scaffold - complete as `scaffold-registry`; creates a valid unsigned local registry fixture from a local Git worktree with placeholder identity and non-claim guidance.
- Loop 54: local artifact metadata attach - complete as `attach-local-artifact`; records local file hash, size, media type, URI, availability, and verification state without IPFS add/fetch/pin or signing.
- Loop 55: local project onboarding command - complete as `onboard-local-project`; chains scaffold, artifact attach, validation, summary, render, bundle refresh, and report generation with local-only boundaries.
- Loop 56: committed onboarding sample - complete as `fixtures/onboarding-sample.registry.json`, generated sample summary/page/report, tests, CI wiring, and bundle refresh.
- Loop 57: optional workbench import for onboarding sample - complete as `output/forge-app-with-onboarding-sample.html`; proves `render-app --registry` imports onboarded registries without changing the default workbench.
- Loop 58: workbench project set handoff - complete as a static Project set screen with embedded output/registry paths and a copyable recreate command.
- Loop 59: project-scoped Radicle repository smoke - complete as RID `rad:zWGy1Ssjb7tBbwDbdGLqeHCsUqwr` for commit `fd3f1898d81a4b00be9095c62e3c07fc1a792a95`, seeded/synced/cloned/read back from separate temporary Radicle state with bounded non-claims.
- Loop 60: fresh-state Radicle RID readback - complete as brand-new temporary profile clone/readback of `rad:zWGy1Ssjb7tBbwDbdGLqeHCsUqwr` at commit `fd3f1898d81a4b00be9095c62e3c07fc1a792a95`, without reusing the original Loop 59 seed profile or explicit original-seed connection.
- Loop 61: Radicle update continuity check - complete as fresh-peer publication of current commit `00404656bcb17ad1aab241fb0ab0dd60487d9699` to the same RID, while default readback remained on the original delegate commit.
- Loop 62: retained Radicle maintainer lane - complete as retained RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` with fresh default and direct-seed readback of commit `dfc10b8f029c5eb886db2025dcc06c6490e28504`.
- Loop 63: retained Radicle same-RID update - complete as the same RID advanced to commit `f800bae387f33452fdeb79ecf5c795d25f7246ac`, with fresh direct-seed readback matching the updated commit and default public-routing readback not observed.
- Loop 64: retained RID community direct-seed quickstart - complete as `docs/radicle-retained-rid-quickstart.md` plus `radicle-retained-quickstart`, a read-only evidence-derived recipe for maintainer-assisted direct-seed clones.
- Loop 65: retained RID independent follower-seed readback - complete as the same RID advanced to commit `7262f69b82e442263d6261414f6b771be04c6b6f`; reader A cloned from retained maintainer seed and reader B cloned from reader A acting as a follower seed.
- Loop 66: retained seed restart/readback rehearsal - complete as the same RID advanced to commit `4c8cd6183e2e12d1c62af7d2f013fb085b2d6bf8`; fresh readers cloned before and after retained seed restart on the same local address.
- Loop 67: public VPS follower-seed readback - complete as `openclaw` served retained RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` at commit `610fc3da9757d0cb123aa5976db552b991b766d4` to a fresh reader on `ubuntu-work`.
- Loop 68: public VPS follower seed service hardening - complete as an enabled user-level `systemd` service on `openclaw` with restart policy, linger enabled, retained maintainer key material kept off the VPS, and post-restart fresh public readback.
- Loop 69: repeatable public seed health check - complete as `scripts/check_public_radicle_seed.py` plus fresh-profile public readback evidence from `ubuntu-work`.
- Loop 70: public seed update propagation - complete as the same retained RID advanced to commit `64efbada294d4a57c014a27398b92e344c6d68aa`, the `openclaw` follower synced it through a temporary bridge, the bridge and maintainer seed were stopped, and a fresh reader cloned the updated commit from the public VPS seed.

The prior loop set is defined in `docs/next-evidence-and-interoperability-loops.md` and `AGENT-LOOPS.md`:

- Loop 26: Live evidence import into adapter/renderer — complete as `fixtures/live-evidence-index.json` plus renderer/preflight/test updates; no new live network action.
- Loop 27: Public project update draft/post — complete as GitHub Discussion #6: https://github.com/redclawanon-rgb/decentralized-forge/discussions/6.
- Loop 28: Nostr readback persistence/divergence check — complete as readback-only evidence in `evidence/nostr-loop28-readback-check-2026-06-22.md`/`.json`; selected Loop 25 relays still returned and verified the event; `wss://relay.primal.net` also returned it; `wss://nostr.wine` did not during this check.
- Loop 29: NIP-34 live-event adapter import — complete as selected-relay readback evidence import without full protocol compatibility claims.
- Loop 30: Radicle public-network gate plan — complete as Permission-F help-only preflight; Permission G still required before public seed/publish/sync/node/remote clone.
- Loop 31: Public storage/IPFS evidence gate plan — complete as Permission-H inventory/plan preflight only; no package install, IPFS add/fetch/pin, gateway check, paid storage, wallet, or durability claim.
- Loop 32: Next controller/report consolidation — complete as status/context/loop doc and checklist/test consolidation.

## Next approval bundles to remove roadblocks

- **Permission G:** Radicle public seed/remote clone smoke with only disposable/project-scoped state; approved 2026-06-22 via Telegram message “G & I are approved to keep things moving along.” Still no production/private personal keys, paid infrastructure, spending, direct outreach, durability/censorship-resistance/production-readiness/security claims, or unsupported replication claims.
- **Permission I:** local CAR/CID fixture verification with project-scoped dev dependencies; approved 2026-06-22 via Telegram message “G & I are approved to keep things moving along.” Allows adding lockfile-backed local JS tooling such as `ipfs-car`, `@ipld/car`, and/or `multiformats`, but still no daemon, gateway, pinning, wallet, paid storage, public storage action, or durability claim unless separately approved.

Completed approval bundles for the just-finished loop set:

- **Permission D:** Renew low-noise controller for Loops 26–32 — granted 2026-06-22 and completed through Loop 32.
- **Permission E:** Nostr follow-up live evidence using only the disposable project key — granted 2026-06-22 and used for Loop 28 readback-only checks; no new publish.
- **Permission F:** Radicle public-network preflight only — granted 2026-06-22 and completed in Loop 30.
- **Permission H:** Public immutable storage/IPFS preflight only — granted 2026-06-22 and completed in Loop 31; no paid pinning, wallets, Filecoin/Arweave spend, paid storage, or durability claims.

**Granted 2026-06-22 via Telegram voice:** Eric approved **D + E + F + H** and explicitly held off on **G** per Harry's recommendation.

Needed permission bundles already granted before autonomous execution are recorded in `docs/next-live-adapter-loops.md`: Permission A (Radicle local replay), Permission B (Nostr public relay publish/readback), and Permission C (low-noise durable cron controller). Eric granted A+B+C plus public update posting on 2026-06-22 via Telegram, while preserving gates against spending, production/private personal keys, paid infrastructure, direct person outreach, and unsupported security/durability/censorship-proof/production-readiness claims.

## Gates/blockers

- Public publishing/posting/pushing and public account/project creation are approved for this project when accurate, non-spammy, and labeled research/prototype.
- Public Nostr relay publishing requires disposable/project-scoped keys only; do not use production/private personal keys.
- Do not run a public ActivityPub/ForgeFed actor unless it is free, clearly prototype-labeled, and does not require paid infrastructure or production credentials.
- Do not spend money or use Filecoin/Arweave wallets without explicit approval.
- Do not use production/private keys; fixtures must use synthetic public identifiers only.
- Do not contact specific people outside public project channels.
