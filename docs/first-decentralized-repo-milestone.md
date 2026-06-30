# First Decentralized Repo Milestone

As of Loop 74, this project has usable public Radicle direct-seed paths for the
retained project RID.

## What Works

- RID: `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`
- Primary public seed: `z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776`
- Second public seed: `z6MksRdjzuN2VYV4HTXdVSchitJ8Bq1zbx8WhBb3KhyfSm6A@187.77.19.162:8877`
- Verified milestone commit: `ef16e2ad39d3e13bdcc9d454443c5bbb17733c68`
- Seed host: `openclaw`
- Seed mode: follower seed, not retained maintainer key material
- Service mode: enabled user-level `systemd` service with restart policy
- Health check: `scripts/check_public_radicle_seed.py`
- External monitor: `decentralized-forge-radicle-healthcheck.timer` on `ubuntu-work`
- Second follower seed: `z6MksRdjzuN2VYV4HTXdVSchitJ8Bq1zbx8WhBb3KhyfSm6A@100.83.206.66:8877`
- Second seed host: `ubuntu-work`
- Second seed mode: enabled user-level `systemd` follower seed with separate Radicle state
- Second seed reachability: verified from `openclaw` over Tailnet in Loop 73 and through public `openclaw` relay port `8877` from `ubuntu-work` in Loop 74

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
ef16e2ad39d3e13bdcc9d454443c5bbb17733c68
```

## Verify With The Health Check

```sh
python scripts/check_public_radicle_seed.py \
  --seed z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776 \
  --rid rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy \
  --expected-commit ef16e2ad39d3e13bdcc9d454443c5bbb17733c68
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

## Non-Claims

This milestone does not prove permanent durability, automatic future update
propagation, default public routing, global replication, censorship resistance,
security, identity trust, full Radicle compatibility, SLSA compliance, or
production readiness. Loop 74 adds a second public direct-seed address, but the
second seed still uses `openclaw` as public ingress to reach the `ubuntu-work`
seed over Tailnet, so it is not proof of independent provider or network
availability.
