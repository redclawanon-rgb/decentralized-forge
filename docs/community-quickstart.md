# Community Quickstart

This project is currently a verification-oriented prototype. The safest way to use it today is to clone the repository, run the local checks, and inspect the rendered report plus the evidence files.

## Verify This Repository

```sh
git clone https://github.com/redclawanon-rgb/decentralized-forge.git
cd decentralized-forge
npm ci
npm run forge:doctor
npm run verify:evidence-index
npm run verify:local
```

The doctor command is read-only. It checks local tool availability, Git state, and live evidence index integrity. It does not publish events, start daemons, use keys, spend money, or contact services beyond what the invoked command explicitly says.

## Inspect The Report

```sh
python scripts/forge_registry.py render fixtures/example-project.registry.json output/demo-project.html \
  --nip34-repo-fixture fixtures/nostr-repo-announcement.json \
  --nip34-collaboration-fixture fixtures/nostr-collaboration-events.json \
  --nip34-state-status-fixture fixtures/nostr-repo-state-status.json \
  --nip34-live-readback-fixture fixtures/nostr-live-readback-events.json \
  --live-evidence-index fixtures/live-evidence-index.json
```

Open `output/demo-project.html`. Treat it as a readable verification report, not a hosted forge.

## Review The Portable Bundle

```sh
python scripts/forge_registry.py export-bundle output/decentralized-forge-verification-bundle.zip
python scripts/forge_registry.py verify-bundle output/decentralized-forge-verification-bundle.zip
python scripts/forge_registry.py verify-bundle-cleanroom output/decentralized-forge-verification-bundle.zip
python scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip
python scripts/forge_registry.py export-bundle-release-note output/decentralized-forge-verification-bundle.zip
```

Before attaching or describing the bundle outside this repository, read `docs/portable-bundle-review-checklist.md`. The checklist explains the required local checks, report review, release-note export, non-claims, attachment metadata, and stop conditions.

## Read Claims Correctly

- `local-fixture` means committed local data was parsed or rendered.
- `synthetic-fixture` means test data only.
- `local-cli-verified` means a local command path worked for the exact recorded scenario.
- `selected-relay-readback-verified` means selected Nostr relays returned the exact event during the recorded check.
- `hosted-keyless-attestation-generated` means GitHub Actions produced a hosted keyless attestation for the listed subjects.
- `public-gateway-no-readback-observed` means gateways were queried and did not return matching bytes during that run.

None of those labels means production readiness, durable storage, global propagation, broad network availability, censorship resistance, or a security guarantee unless a future evidence row says exactly that.

## Bring Another Project Later

The intended public tool flow is:

1. Run the chained local path with `python scripts/forge_registry.py onboard-local-project path/to/repo path/to/artifact --project-id project --version 0.1.0-local --tag v0.1.0-local`.
2. Or run the individual steps: scaffold with `scaffold-registry`, attach artifact metadata with `attach-local-artifact`, then validate and render.
3. Add optional transport evidence from Nostr, Radicle, IPFS, or hosted attestations.
4. Export a static report and evidence bundle that others can verify without trusting the original platform.

The current bundle workflow is local and fixture-backed. Local onboarding records Git metadata, file hash, size, media type, and `file://` availability only; it does not add/fetch/pin IPFS content, sign releases, publish protocol events, or prove durable availability. Until live importers are broader and evidence-backed, use the fixtures as examples and keep new evidence rows explicit, bounded, and secret-free.

The committed onboarding sample at `fixtures/onboarding-sample.registry.json` and `output/onboarding-sample.registry.html` shows the full local path without requiring a separate project.
To inspect it inside the static workbench, render `output/forge-app-with-onboarding-sample.html` with `render-app --registry fixtures/example-project.registry.json --registry fixtures/portable-lab.registry.json --registry fixtures/onboarding-sample.registry.json`.
The workbench Project set screen lists the embedded registry inputs and shows the matching recreate command for the current project set.

## First Radicle Repo Smoke

Loop 59 records the first project-scoped Radicle repository smoke for this repo in `evidence/radicle-project-repo-smoke-2026-06-29.json`. The recorded RID is `rad:zWGy1Ssjb7tBbwDbdGLqeHCsUqwr`, tied to source commit `fd3f1898d81a4b00be9095c62e3c07fc1a792a95`, with a separate temporary Radicle profile clone/readback of that same commit.

Treat that as exact run evidence only. It does not prove durable availability, broad network replication, identity trust, security, or production readiness.
