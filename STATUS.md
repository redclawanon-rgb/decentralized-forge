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
- Use the completed safe live-gated replay plan/checklist as the prerequisite gate for Radicle/Nostr live verification. As of Loop 35, `rad` and `nak` are installed user-locally, a disposable project Nostr key exists outside the repo, a Radicle temporary-`RAD_HOME` disposable private replay succeeded locally, Nostr selected-relay publish/readback has been executed for one prototype event, and one disposable public Radicle seed/clone/readback smoke succeeded for exact RID `rad:z2WtozFrCRhygh9CGzyUN57CN7Nwa`.
- Treat Radicle as verified only for (a) the narrow disposable private local replay path and (b) the exact Loop 34 disposable public seed/clone/readback smoke; do not claim durable availability, censorship resistance, security, global replication, identity trust, production readiness, full Radicle compatibility, or broad Radicle network availability.
- Keep ForgeFed as a later object-shape/federation bridge; do not run a public actor until moderation/security gates exist.
- Keep IPFS/CIDs as artifact metadata until live add/fetch/pin verification is explicitly performed; defer Filecoin/Arweave because they imply spending/wallet decisions.
- Keep Sigstore/in-toto/SLSA as release/build trust models; current provenance is synthetic and no SLSA level should be claimed.

## Next recommended loop

**Next:** Milestone 1 is complete as a reproducible, evidence-scoped static prototype. The next step is an explicit Eric approval/target before any further live storage (IPFS daemon/add/fetch/gateway/pinning/wallet), repeated or broader Radicle public-network testing, public update posting about these results, or stronger durability/censorship/security/production claims.

Recent completed loops:

- Loop 33: local CAR/CID fixture verification — complete as project-scoped `@ipld/car`/`multiformats` evidence in `evidence/local-car-cid-fixture-2026-06-22.json`; no live storage action.
- Loop 34: disposable public Radicle seed/remote-clone smoke — complete as exact bounded evidence in `evidence/radicle-public-network-smoke-2026-06-22.json`; RID `rad:z2WtozFrCRhygh9CGzyUN57CN7Nwa`; no broad durability/censorship/security/production/network-availability claim.
- Loop 35: consolidation/report — complete as `evidence/loop35-consolidation-2026-06-22.md` plus checklist/test/context/status updates; no new live protocol/storage action, public update, or cron job.
- Loop 36: hosted local-verification CI and Milestone 1 completion state — complete as `.github/workflows/ci.yml` plus `COMPLETION-CRITERIA.md` updates; CI passed on `main`; no signing/SLSA/live protocol/storage claim.

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
