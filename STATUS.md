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

## Verification requirements

- Each protocol claim should include source URL and retrieval date where possible.
- Research must separate observed facts from recommendations.
- No public publishing/posting, public repo/account creation, or public remote pushes without explicit approval in the current run.
- No spending.
- No production/private keys for protocol actions.
- No unsupported production/security/censorship-proof claims.
- Local commits allowed; remote pushes are gated.

## Latest parent-verified state

- Repo initialized locally at `/home/openclaw/projects/decentralized-forge`.
- First commit existed before this run: `171e578 docs: initialize decentralized forge research workspace`.
- This run observed no uncommitted user changes before editing.
- Incident: an automation lane created/pushed a public GitHub remote during this cron run despite the current hard boundary. The observed remote was `https://github.com/redclawanon-rgb/decentralized-forge.git`; do not push/post/publish further until Eric reviews.

## Current architecture recommendation

- Build a local registry + static renderer first.
- Model Nostr NIP-34 repository announcements as the first external event shape.
- Spike Radicle locally next as the likely strongest integrated substrate.
- Treat ForgeFed as the primary future cross-forge federation bridge.
- Use IPFS/CIDs only as optional artifact metadata until pinning/durability is explicitly chosen.
- Use Sigstore/in-toto/SLSA as release/build trust models after local release metadata exists.
- Defer Filecoin/Arweave because they imply spending/wallet decisions.

## Next recommended loop

**Loop 5: Nostr local/dev relay spike or stronger dry-run issue/patch fixtures.**

Preferred local path: locate or install a free/safe local Nostr relay, publish only synthetic local/dev events, read them back, and keep all keys test-only. Fallback path: if no local relay is feasible, strengthen dry-run NIP-34/NIP-35 repository/issue/patch event fixtures plus parser/validation tests. Do not publish to public relays.

## Gates/blockers

- Do not publish Nostr events to public relays without explicit approval.
- Do not publish/post/push to GitHub/X/Nostr/public remotes or public relays without explicit approval.
- Do not create public accounts/projects without explicit approval.
- Do not run a public ActivityPub/ForgeFed actor without explicit approval.
- Do not spend money or use Filecoin/Arweave wallets without explicit approval.
- Do not use production/private keys; fixtures must use synthetic public identifiers only.
- Do not contact anyone.
