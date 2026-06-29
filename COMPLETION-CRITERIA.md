# Completion Criteria

This project is complete for **Milestone 1** when it is a reproducible, evidence-scoped static decentralized-forge prototype that another project can copy, validate, render, and inspect without relying on GitHub as the authority for the prototype data.

Milestone 1 completion does **not** mean this is a production forge. It does not claim durable storage, censorship resistance, broad protocol availability, security guarantees, identity trust, SLSA compliance, or production readiness.

## Milestone 1 Definition Of Done

The repository must provide:

1. A documented project registry schema and at least two registry fixtures.
2. A reusable local CLI that validates registry fixtures, renders static project pages, exports machine-readable summaries, and runs the local verification suite.
3. A generated static demo artifact that is byte-for-byte reproducible from committed fixtures.
4. A live evidence index that separates local fixtures, selected-relay readback, disposable Radicle smoke evidence, and non-claims.
5. CI that runs the same local checks documented in the README.
6. Clear gates for optional live IPFS, Nostr, Radicle, and signing/provenance follow-up work.
7. No secret material, production/private personal keys, paid infrastructure, direct outreach, or unsupported security/durability/censorship/production claims.

## Required Verification

These commands must pass before release-oriented pushes:

```sh
python -m json.tool schemas/project-registry.schema.json
python -m json.tool fixtures/example-project.registry.json
python -m json.tool fixtures/portable-lab.registry.json
python -m json.tool fixtures/radicle-backed-project.registry.json
python -m json.tool fixtures/nostr-repo-announcement.json
python -m json.tool fixtures/nostr-collaboration-events.json
python -m json.tool fixtures/nostr-repo-state-status.json
python -m json.tool fixtures/live-adapter-replay-checklist.json
python -m json.tool fixtures/live-evidence-index.json
python scripts/nip34_adapter.py fixtures/nostr-repo-announcement.json fixtures/nostr-collaboration-events.json fixtures/nostr-repo-state-status.json
python scripts/preflight_static_artifact.py
python scripts/forge_registry.py validate fixtures/example-project.registry.json fixtures/portable-lab.registry.json
python scripts/forge_registry.py render fixtures/portable-lab.registry.json output/portable-lab.html
python scripts/forge_registry.py render-app output/forge-app.html
python scripts/forge_registry.py export-summary fixtures/example-project.registry.json output/demo-project.summary.json
python scripts/forge_registry.py export-summary fixtures/portable-lab.registry.json output/portable-lab.summary.json
python scripts/forge_registry.py export-bundle output/decentralized-forge-verification-bundle.zip
python scripts/forge_registry.py verify-bundle output/decentralized-forge-verification-bundle.zip
python scripts/live_gate_inventory.py
python -m unittest discover -s tests
npm ci
npm run verify:car-cid
npm run verify:helia
```

## Completion Lanes

### Lane A: Reproducible Prototype

Status: complete.

- CI for the required verification commands exists at `.github/workflows/ci.yml` and passed on `main` for commit `e69fd5b22e8ec27f52a11e582b705e212690a865`.
- Fixture bytes are kept stable across platforms through `.gitattributes`.
- Generated HTML is checked by `scripts/preflight_static_artifact.py` and the CI worktree-clean check.

### Lane B: Reusable Local Tooling

Status: complete.

- `scripts/forge_registry.py` provides `validate`, `render`, `render-app`, `export-summary`, `export-bundle`, `verify-bundle`, and `verify-local` commands.
- The CLI uses the same validation paths as the renderer and tests.
- Deterministic JSON summaries are generated under `output/*.summary.json`.

### Lane C: Multi-Project Fixture Coverage

Status: complete.

- `fixtures/portable-lab.registry.json` is the second registry fixture.
- It renders to `output/portable-lab.html` and exports to `output/portable-lab.summary.json` without code changes.
- Its evidence and non-claim language remain project-scoped.

### Lane D: Local Workbench App

Status: active as a static local app.

- `scripts/render_forge_app.py` generates `output/forge-app.html` from committed registry fixtures, live-evidence index data, selected-relay Nostr readback evidence, and the registry-shaped keyless-attestation import.
- The app provides project overview, issue/patch inspection, release evidence, evidence filtering, and unsigned local Nostr issue/patch draft generation.
- It does not sign, publish, fetch, open WebSockets, use private keys, host a service, or claim production forge readiness.

### Lane E: Portable Verification Bundle

Status: active as a deterministic generated artifact.

- `output/decentralized-forge-verification-bundle.zip` contains committed fixtures, schemas, source evidence files, generated HTML, summaries, the static workbench app, verifier scripts, and `verification-bundle.manifest.json`.
- `python scripts/forge_registry.py verify-bundle output/decentralized-forge-verification-bundle.zip` validates manifest schema, file sizes, SHA-256 hashes, and live-evidence-index bindings.
- It does not replace signing/provenance verification, durable storage evidence, availability evidence, SLSA compliance, or production security review.

### Lane F: Optional Live Evidence

Status: active under standing approval.

Approved as of 2026-06-28 when free/disposable/project-scoped, low-volume, secret-free, and evidence-labeled:

- live IPFS add/fetch/gateway checks for the local CAR/CID fixture;
- Nostr issue/patch readback using disposable project-scoped keys;
- repeated or broader Radicle public-network checks using disposable state;
- optional signing/provenance verification with disposable or keyless test material.

Still forbidden without separate explicit approval: spending money, paid pinning/storage, wallets, production/private personal keys, direct person outreach, persistent public seed operation, or stronger durability/censorship/security/production claims.

Loop 40 added GitHub Actions keyless artifact attestation generation for committed/generated prototype artifacts and recorded the passed run in `evidence/github-keyless-attestation-2026-06-28.json`. This is hosted provenance evidence; it does not by itself upgrade local registry fixture provenance fields to SLSA compliance or production supply-chain trust.

Loop 41 added project-scoped local Helia UnixFS/IPFS add-get readback evidence for `fixtures/local-release-artifact.txt` in `evidence/helia-local-ipfs-add-get-2026-06-28.json`. This verifies one local add/get execution only; it does not claim public gateway availability, pinning, durability, censorship resistance, security, or production readiness.

## Release Rule

Milestone 1 is complete as an evidence-scoped static prototype after CI passed on `main` for commit `e69fd5b22e8ec27f52a11e582b705e212690a865`, the README points to this file, and `STATUS.md` names the current completion state without contradicting the evidence index.
