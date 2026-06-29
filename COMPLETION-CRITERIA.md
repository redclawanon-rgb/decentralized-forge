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
python -m json.tool fixtures/onboarding-sample.registry.json
python -m json.tool fixtures/nostr-repo-announcement.json
python -m json.tool fixtures/nostr-collaboration-events.json
python -m json.tool fixtures/nostr-repo-state-status.json
python -m json.tool fixtures/live-adapter-replay-checklist.json
python -m json.tool fixtures/live-evidence-index.json
python scripts/nip34_adapter.py fixtures/nostr-repo-announcement.json fixtures/nostr-collaboration-events.json fixtures/nostr-repo-state-status.json
python scripts/preflight_static_artifact.py
python scripts/forge_registry.py validate fixtures/example-project.registry.json fixtures/portable-lab.registry.json fixtures/onboarding-sample.registry.json
python scripts/forge_registry.py render fixtures/portable-lab.registry.json output/portable-lab.html
python scripts/forge_registry.py render-app output/forge-app.html
python scripts/forge_registry.py render-app output/forge-app-with-onboarding-sample.html --registry fixtures/example-project.registry.json --registry fixtures/portable-lab.registry.json --registry fixtures/onboarding-sample.registry.json
python scripts/forge_registry.py export-summary fixtures/example-project.registry.json output/demo-project.summary.json
python scripts/forge_registry.py export-summary fixtures/portable-lab.registry.json output/portable-lab.summary.json
python scripts/forge_registry.py export-bundle output/decentralized-forge-verification-bundle.zip
python scripts/forge_registry.py verify-bundle output/decentralized-forge-verification-bundle.zip
python scripts/forge_registry.py verify-bundle-cleanroom output/decentralized-forge-verification-bundle.zip
python scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip --json
python scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip --json --output output/onboarding-sample.bundle-report.json
python scripts/forge_registry.py export-bundle-release-note output/decentralized-forge-verification-bundle.zip
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

- `scripts/forge_registry.py` provides `validate`, `scaffold-registry`, `attach-local-artifact`, `onboard-local-project`, `render`, `render-app`, `export-summary`, `export-bundle`, `verify-bundle`, `verify-bundle-cleanroom`, `report-bundle`, `export-bundle-release-note`, and `verify-local` commands.
- The CLI uses the same validation paths as the renderer and tests.
- Deterministic JSON summaries are generated under `output/*.summary.json`.
- `scaffold-registry` creates a valid unsigned local registry fixture from a local Git worktree with placeholder maintainer identity and explicit non-claims.
- `attach-local-artifact` updates a registry fixture with raw file SHA-256, byte size, media type, `file://` URI, and local-only availability/non-claims without IPFS add/fetch/pin, signing, paid storage, or durability claims.
- `onboard-local-project` chains scaffold, local artifact attach, validation, summary export, rendering, bundle refresh, and bundle report export without live protocol, storage, signing, or production-readiness claims.
- `fixtures/onboarding-sample.registry.json`, `output/onboarding-sample.registry.html`, `output/onboarding-sample.registry.summary.json`, and `output/onboarding-sample.bundle-report.json` provide a committed local-only sample of the one-command onboarding path.

### Lane C: Multi-Project Fixture Coverage

Status: complete.

- `fixtures/portable-lab.registry.json` is the second registry fixture.
- It renders to `output/portable-lab.html` and exports to `output/portable-lab.summary.json` without code changes.
- `fixtures/onboarding-sample.registry.json` is the committed onboarding sample fixture generated by `onboard-local-project`.
- Each fixture's evidence and non-claim language remain project-scoped.

### Lane D: Local Workbench App

Status: active as a static local app.

- `scripts/render_forge_app.py` generates `output/forge-app.html` from committed registry fixtures, live-evidence index data, selected-relay Nostr readback evidence, and the registry-shaped keyless-attestation import.
- `output/forge-app-with-onboarding-sample.html` proves onboarded registries can be imported into the static workbench with explicit `render-app --registry` arguments without changing the default two-project workbench.
- The app provides project overview, issue/patch inspection, release evidence, evidence filtering, and unsigned local Nostr issue/patch draft generation.
- The Project set screen shows embedded registry source paths, the generated output path, and a copyable `render-app --registry ...` command for recreating the current workbench.
- It does not sign, publish, fetch, open WebSockets, use private keys, host a service, or claim production forge readiness.

### Lane E: Portable Verification Bundle

Status: active as a deterministic generated artifact.

- `output/decentralized-forge-verification-bundle.zip` contains committed fixtures, schemas, source evidence files, generated HTML, summaries, the static workbench app, verifier scripts, and `verification-bundle.manifest.json`.
- `python scripts/forge_registry.py verify-bundle output/decentralized-forge-verification-bundle.zip` validates manifest schema, file sizes, SHA-256 hashes, and live-evidence-index bindings.
- `python scripts/forge_registry.py verify-bundle-cleanroom output/decentralized-forge-verification-bundle.zip` extracts the bundle into a temporary directory and runs bundled verification paths from that extracted tree.
- `python scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip` imports either a bundle ZIP or extracted bundle directory and reports project identity, evidence rows, non-claims, verification gaps, and suggested commands.
- `python scripts/forge_registry.py export-bundle-release-note output/decentralized-forge-verification-bundle.zip` emits a shareable markdown note with the exact current commit SHA, bundle digest, report summary, non-claims, verification gaps, and checklist stop conditions.
- `docs/portable-bundle-review-checklist.md` defines the maintainer review, attachment, non-claim, and stop-condition checklist for release-facing bundle handoffs.
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

Loop 59 added the first project-scoped Radicle repository smoke for this repo: RID `rad:zWGy1Ssjb7tBbwDbdGLqeHCsUqwr` at commit `fd3f1898d81a4b00be9095c62e3c07fc1a792a95`, seeded/synced from temporary state and cloned/read back from a separate temporary Radicle profile. This is exact evidence for that bounded run only; it does not claim durable availability, broad network replication, identity trust, security, or production readiness.

Loop 60 added a fresh-state readback check for the same RID and commit. A brand-new temporary Radicle profile cloned `rad:zWGy1Ssjb7tBbwDbdGLqeHCsUqwr` at commit `fd3f1898d81a4b00be9095c62e3c07fc1a792a95` without reusing the original Loop 59 seed profile or explicitly connecting to the original seed node. This strengthens the first decentralized-repo evidence beyond localhost-only smoke, but still does not claim permanent durability, broad replication, identity trust, security, or production readiness.

Loop 61 added update-continuity evidence for the same RID. A fresh non-original Radicle identity pushed current commit `00404656bcb17ad1aab241fb0ab0dd60487d9699` to `rad:zWGy1Ssjb7tBbwDbdGLqeHCsUqwr` under its own peer namespace, but a default fresh clone still checked out the original delegate main at `fd3f1898d81a4b00be9095c62e3c07fc1a792a95`. This identifies the next real usability requirement: retained maintainer delegate state or a deliberate multi-peer/ref policy for canonical update continuity.

Loop 62 added the retained maintainer lane. A project-scoped Radicle identity and maintainer worktree now live under gitignored `.tmp/radicle-retained-delegate`, outside the portable bundle and outside committed evidence. Using that retained state, the project published RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` for commit `dfc10b8f029c5eb886db2025dcc06c6490e28504`; a fresh default clone and an explicit direct-seed clone both read back the same commit. This is the first usable retained-maintainer Radicle path, but it still does not prove permanent durability, future default-routing availability, broad replication, identity trust, security, or production readiness.

Loop 63 added same-RID update evidence for that retained maintainer lane. The retained state was moved to host-local WSL storage to avoid exposing secret-bearing state to Docker and to keep Radicle node sockets off the Windows-mounted filesystem. Using the same RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`, the project advanced from commit `dfc10b8f029c5eb886db2025dcc06c6490e28504` to commit `f800bae387f33452fdeb79ecf5c795d25f7246ac`; a fresh explicit direct-seed clone read back the updated commit. Default public-routing readback was not observed in this run, so the supported update claim is direct-seed readback only.

Loop 64 added the retained RID community handoff. `docs/radicle-retained-rid-quickstart.md` and `python scripts/forge_registry.py radicle-retained-quickstart` now provide an evidence-derived maintainer-assisted direct-seed clone recipe for RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` at commit `f800bae387f33452fdeb79ecf5c795d25f7246ac`. This is a read-only usability layer over Loop 63 evidence; it does not prove default public routing, persistent seeding, durable availability, broad replication, identity trust, security, or production readiness.

## Release Rule

Milestone 1 is complete as an evidence-scoped static prototype after CI passed on `main` for commit `e69fd5b22e8ec27f52a11e582b705e212690a865`, the README points to this file, and `STATUS.md` names the current completion state without contradicting the evidence index.
