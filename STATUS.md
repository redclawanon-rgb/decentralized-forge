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
- Local `HEAD` matched remote `origin/main` at `c74b62f245bc681fca873a125a07130979b46988` after pushing Loops 5–8 and public-gate updates.

## Current architecture recommendation

- Build a local registry + static renderer first.
- Model Nostr NIP-34 repository announcements as the first external event shape.
- Spike Radicle locally next as the likely strongest integrated substrate.
- Treat ForgeFed as the primary future cross-forge federation bridge.
- Use IPFS/CIDs only as optional artifact metadata until pinning/durability is explicitly chosen.
- Use Sigstore/in-toto/SLSA as release/build trust models after local release metadata exists.
- Defer Filecoin/Arweave because they imply spending/wallet decisions.

## Next recommended loop

**Loop 9: public collaboration surface.**

Use the already verified public GitHub repo carefully: tighten GitHub Issues/Discussions/README roadmap as the public collaboration surface and draft/post a concise public update only if it is accurate, non-spammy, and clearly labeled research/prototype. Do not contact specific people directly. Do not make unsupported security, SLSA, production-readiness, censorship-proof, live IPFS, or live protocol-verification claims.

## Gates/blockers

- Public publishing/posting/pushing and public account/project creation are approved for this project when accurate, non-spammy, and labeled research/prototype.
- Public Nostr relay publishing requires disposable/project-scoped keys only; do not use production/private personal keys.
- Do not run a public ActivityPub/ForgeFed actor unless it is free, clearly prototype-labeled, and does not require paid infrastructure or production credentials.
- Do not spend money or use Filecoin/Arweave wallets without explicit approval.
- Do not use production/private keys; fixtures must use synthetic public identifiers only.
- Do not contact specific people outside public project channels.
