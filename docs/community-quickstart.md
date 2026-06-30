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

Loop 60 adds `evidence/radicle-fresh-readback-check-2026-06-29.json`, which cloned the same RID from a brand-new temporary Radicle profile without reusing the original Loop 59 seed profile or explicitly connecting to its original seed node. The clone resolved the expected commit `fd3f1898d81a4b00be9095c62e3c07fc1a792a95`.

Loop 61 adds `evidence/radicle-update-continuity-check-2026-06-29.json`. A fresh non-original Radicle identity pushed current commit `00404656bcb17ad1aab241fb0ab0dd60487d9699` to the same RID under its own peer namespace, but a default fresh clone still checked out the original delegate main at `fd3f1898d81a4b00be9095c62e3c07fc1a792a95`.

Loop 62 adds `evidence/radicle-retained-delegate-check-2026-06-29.json`. A retained project-scoped Radicle maintainer identity under gitignored `.tmp/radicle-retained-delegate` published RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` for commit `dfc10b8f029c5eb886db2025dcc06c6490e28504`; a fresh default clone and an explicit direct-seed clone both read back that commit. The retained secret state is not committed or bundled.

Loop 63 adds `evidence/radicle-retained-update-check-2026-06-29.json`. The same retained RID advanced to commit `f800bae387f33452fdeb79ecf5c795d25f7246ac`, and a fresh explicit direct-seed clone read back that updated commit. Default public-routing readback was attempted but not observed in that run.

Loop 65 adds `evidence/radicle-independent-availability-check-2026-06-29.json`. The same retained RID advanced to commit `7262f69b82e442263d6261414f6b771be04c6b6f`; a fresh reader cloned from the retained maintainer seed, then a second fresh reader cloned from the first reader acting as a follower seed.

Loop 66 adds `evidence/radicle-seed-restart-check-2026-06-29.json`. The same retained RID advanced to commit `4c8cd6183e2e12d1c62af7d2f013fb085b2d6bf8`; a fresh reader cloned from the retained seed before restart, the seed stopped and restarted on the same local address with the same retained node ID, and another fresh reader cloned the same commit after restart.

Loop 67 adds `evidence/radicle-vps-follower-public-readback-2026-06-29.json`. The same retained RID advanced to commit `610fc3da9757d0cb123aa5976db552b991b766d4`; the `openclaw` VPS follower seed at `z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776` served that RID to a fresh reader on `ubuntu-work`, and readback matched the expected commit.

Loops 68-75 make that path usable as a first decentralized repo milestone. Loop 68 installed the `openclaw` follower seed as an enabled user-level `systemd` service and verified public readback after restart. Loop 69 added `scripts/check_public_radicle_seed.py` as a repeatable direct-seed health check. Loop 70 advanced the same retained RID to commit `64efbada294d4a57c014a27398b92e344c6d68aa`. Loop 71 installed an external `ubuntu-work` health timer. Loop 72 advanced the same retained RID to commit `ef16e2ad39d3e13bdcc9d454443c5bbb17733c68`, synced the `openclaw` follower, stopped the temporary bridge and maintainer seed, and verified a fresh public clone from the VPS follower seed. Loop 73 added a second persistent `ubuntu-work` follower seed and verified readback from `openclaw` over Tailnet. Loop 74 verified the second public direct-seed address `z6MksRdjzuN2VYV4HTXdVSchitJ8Bq1zbx8WhBb3KhyfSm6A@187.77.19.162:8877`. Loop 75 advanced the retained RID to commit `d596024dac0d90605d4f103d567e5851771be5a8`, refreshed stale follower caches with host-local backups, stopped the temporary retained maintainer seed, and verified fresh public readbacks from both public seed addresses. Loop 79 ran the release-candidate `verify-first-public-clone` command from fresh Docker/Linux reader profiles against both public seed addresses and verified the same expected HEAD.

The current community clone path for that retained RID is `docs/radicle-retained-rid-quickstart.md` or the read-only helper:

```sh
python scripts/forge_registry.py radicle-retained-quickstart
```

That path now uses the public seed evidence from Loop 75 and verifies the clone by checking `git rev-parse HEAD` against the expected commit printed by the helper.

To verify the current public clone path directly:

```sh
python scripts/forge_registry.py verify-first-public-clone --plan-only
python scripts/forge_registry.py verify-first-public-clone --json
python scripts/forge_registry.py verify-first-public-clone --seed second --json
```

Loop 79 records the corresponding proof in `evidence/radicle-first-public-clone-primary-d596024-2026-06-30.json` and `evidence/radicle-first-public-clone-second-d596024-2026-06-30.json`.

Treat those as exact run evidence only. They do not prove permanent durability, automatic future update propagation, future default public-routing availability, broad network replication, identity trust, security, or production readiness.
