# First Decentralized Repo Milestone

As of Loop 89, this project has usable public Radicle direct-seed paths for the
retained project RID plus a release-candidate verifier command that both fresh
Docker/Linux reader profiles and a separate `ubuntu-work` outside-reader host
used successfully against both public seed addresses. Loop 96 also proves the
first customer-facing `start-project` path can hand a fresh local Git project to
a bounded disposable Radicle genesis/readback gate.

## What Works

- RID: `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`
- Primary public seed: `z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776`
- Second public seed: `z6MksRdjzuN2VYV4HTXdVSchitJ8Bq1zbx8WhBb3KhyfSm6A@187.77.19.162:8877`
- Verified milestone commit: `d596024dac0d90605d4f103d567e5851771be5a8`
- Seed host: `openclaw`
- Seed mode: follower seed, not retained maintainer key material
- Service mode: enabled user-level `systemd` service with restart policy
- Health check: `scripts/check_public_radicle_seed.py`
- Public clone verifier: `python scripts/forge_registry.py verify-first-public-clone`
- External monitor: `decentralized-forge-radicle-healthcheck.timer` on `ubuntu-work`
- Second follower seed: `z6MksRdjzuN2VYV4HTXdVSchitJ8Bq1zbx8WhBb3KhyfSm6A@100.83.206.66:8877`
- Second seed host: `ubuntu-work`
- Second seed mode: enabled user-level `systemd` follower seed with separate Radicle state
- Second seed reachability: verified from `openclaw` over Tailnet in Loop 73 and through public `openclaw` relay port `8877` from `ubuntu-work` in Loop 74
- Started-project sample gate: `scripts/run_started_project_radicle_genesis.py` verified one fresh sample Git project completed `start-project`, received disposable public RID `rad:z3pDfyAoThNEx8Laqnjg6sHLUVzhX`, and cloned/read back commit `b6d3a2aab4a879c8be88d38958f04f37c02c4a24` from a separate temporary Radicle profile.

## Current Seed Status

| Path | Address | Latest verified commit | Evidence |
|---|---|---|---|
| Primary public follower seed | `z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776` | `d596024dac0d90605d4f103d567e5851771be5a8` | `evidence/radicle-public-seed-primary-health-d596024-2026-06-30.json` |
| Second public follower seed | `z6MksRdjzuN2VYV4HTXdVSchitJ8Bq1zbx8WhBb3KhyfSm6A@187.77.19.162:8877` | `d596024dac0d90605d4f103d567e5851771be5a8` | `evidence/radicle-public-seed-second-health-d596024-2026-06-30.json` |
| Update propagation summary | both public seed addresses | `d596024dac0d90605d4f103d567e5851771be5a8` | `evidence/radicle-public-seed-update-d596024-2026-06-30.json` |
| First public clone verifier | primary public follower seed | `d596024dac0d90605d4f103d567e5851771be5a8` | `evidence/radicle-first-public-clone-primary-d596024-2026-06-30.json` |
| First public clone verifier | second public follower seed | `d596024dac0d90605d4f103d567e5851771be5a8` | `evidence/radicle-first-public-clone-second-d596024-2026-06-30.json` |
| Outside-reader verifier | primary public follower seed | `d596024dac0d90605d4f103d567e5851771be5a8` | `evidence/radicle-first-public-clone-outside-reader-ubuntu-work-primary-e0f7144-2026-06-30.json` |
| Outside-reader verifier | second public follower seed | `d596024dac0d90605d4f103d567e5851771be5a8` | `evidence/radicle-first-public-clone-outside-reader-ubuntu-work-second-e0f7144-2026-06-30.json` |

## Clone

```sh
rad auth --alias decentralized-forge-reader --stdin
rad node start
rad node connect z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776 --timeout 30s
rad clone --timeout 120s --seed z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy decentralized-forge
cd decentralized-forge
git rev-parse HEAD
```

Expected HEAD:

```text
d596024dac0d90605d4f103d567e5851771be5a8
```

## Verify With The Health Check

```sh
python scripts/check_public_radicle_seed.py \
  --seed z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776 \
  --rid rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy \
  --expected-commit d596024dac0d90605d4f103d567e5851771be5a8
```

## Verify With The RC Command

Plan mode is read-only:

```sh
python scripts/forge_registry.py verify-first-public-clone --plan-only
```

Live mode starts disposable reader state, connects to the explicit seed, clones
the retained RID, and checks the clone HEAD:

```sh
python scripts/forge_registry.py verify-first-public-clone --json
python scripts/forge_registry.py verify-first-public-clone --seed second --json
```

## Evidence

- `evidence/radicle-vps-follower-public-readback-2026-06-29.json`
- `evidence/radicle-vps-follower-systemd-service-2026-06-29.json`
- `evidence/radicle-public-seed-health-check-2026-06-29.json`
- `evidence/radicle-public-seed-update-propagation-2026-06-29.json`
- `evidence/radicle-public-seed-update-health-check-2026-06-29.json`
- `evidence/radicle-external-health-timer-2026-06-29.json`
- `evidence/radicle-public-seed-update-ef16e2a-2026-06-29.json`
- `evidence/radicle-public-seed-update-health-check-ef16e2a-2026-06-29.json`
- `evidence/radicle-ubuntu-work-follower-bootstrap-2026-06-29.json`
- `evidence/radicle-second-seed-tailnet-health-2026-06-29.json`
- `evidence/radicle-second-public-seed-health-2026-06-29.json`
- `evidence/radicle-public-seed-update-d596024-2026-06-30.json`
- `evidence/radicle-public-seed-primary-health-d596024-2026-06-30.json`
- `evidence/radicle-public-seed-second-health-d596024-2026-06-30.json`
- `evidence/radicle-first-public-clone-primary-d596024-2026-06-30.json`
- `evidence/radicle-first-public-clone-second-d596024-2026-06-30.json`
- `evidence/radicle-first-public-clone-outside-reader-ubuntu-work-primary-e0f7144-2026-06-30.json`
- `evidence/radicle-first-public-clone-outside-reader-ubuntu-work-second-e0f7144-2026-06-30.json`
- `evidence/radicle-start-project-genesis-2026-06-30.json`

## Non-Claims

This milestone does not prove permanent durability, is not proof of automatic future update propagation, and does not prove default public routing, global replication, censorship resistance, security, identity trust, full Radicle compatibility, full forge compatibility, SLSA compliance, or production readiness. The started-project sample gate is disposable and does not keep a public seed running. Loop 75 verifies that both public direct-seed addresses
serve the current retained-RID commit. Loop 79 verifies that the release-candidate public clone command works from fresh Docker/Linux reader profiles against both public seed addresses. Loop 74 adds a second public direct-seed address, but the
second seed still uses `openclaw` as public ingress to reach the `ubuntu-work`
seed over Tailnet, so it is not proof of independent provider or network availability.
Loop 89 adds a separate `ubuntu-work` outside-reader proof for both public seed
addresses. Loop 96 proves one disposable started-project Radicle genesis/readback
path, but it does not keep a persistent seed or prove durability for future
customer projects.
