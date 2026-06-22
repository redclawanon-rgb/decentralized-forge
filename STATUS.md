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

## Verification requirements

- Each protocol claim should include source URL and retrieval date where possible.
- Research must separate observed facts from recommendations.
- No public publishing.
- No spending.
- No production/private keys.
- Local commits allowed.

## Latest parent-verified state

- Repo initialized locally at `/home/openclaw/projects/decentralized-forge`.
- First commit existed before this run: `171e578 docs: initialize decentralized forge research workspace`.
- This run observed no uncommitted user changes before editing.

## Current architecture recommendation

- Build a local registry + static renderer first.
- Model Nostr NIP-34 repository announcements as the first external event shape.
- Spike Radicle locally next as the likely strongest integrated substrate.
- Treat ForgeFed as the primary future cross-forge federation bridge.
- Use IPFS/CIDs only as optional artifact metadata until pinning/durability is explicitly chosen.
- Use Sigstore/in-toto/SLSA as release/build trust models after local release metadata exists.
- Defer Filecoin/Arweave because they imply spending/wallet decisions.

## Next recommended loop

If Loop 2 and Loop 3 complete in this run, next work should be **Loop 4: Radicle local integration spike**:

1. Install or locate Radicle tooling without publishing anything.
2. Create/import a local sample Git repo.
3. Inspect Radicle project identity, issue, patch, and HTTP/API shapes.
4. Write `docs/radicle-mapping.md` mapping Radicle fields to `project-registry.schema.json`.
5. Add one fixture representing a Radicle-backed registry entry.
6. Run tests and commit locally.

## Gates/blockers

- Do not publish Nostr events to public relays without explicit approval.
- Do not run a public ActivityPub/ForgeFed actor without explicit approval.
- Do not spend money or use Filecoin/Arweave wallets without explicit approval.
- Do not use production/private keys; fixtures must use synthetic public identifiers only.
