# First Decentralized Repo Milestone

As of Loop 70, this project has a usable public Radicle direct-seed path for the
retained project RID.

## What Works

- RID: `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`
- Public seed: `z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776`
- Verified milestone commit: `64efbada294d4a57c014a27398b92e344c6d68aa`
- Seed host: `openclaw`
- Seed mode: follower seed, not retained maintainer key material
- Service mode: enabled user-level `systemd` service with restart policy
- Health check: `scripts/check_public_radicle_seed.py`

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
64efbada294d4a57c014a27398b92e344c6d68aa
```

## Verify With The Health Check

```sh
python scripts/check_public_radicle_seed.py \
  --seed z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776 \
  --rid rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy \
  --expected-commit 64efbada294d4a57c014a27398b92e344c6d68aa
```

## Evidence

- `evidence/radicle-vps-follower-public-readback-2026-06-29.json`
- `evidence/radicle-vps-follower-systemd-service-2026-06-29.json`
- `evidence/radicle-public-seed-health-check-2026-06-29.json`
- `evidence/radicle-public-seed-update-propagation-2026-06-29.json`
- `evidence/radicle-public-seed-update-health-check-2026-06-29.json`

## Non-Claims

This milestone does not prove permanent durability, automatic future update
propagation, default public routing, global replication, censorship resistance,
security, identity trust, full Radicle compatibility, SLSA compliance, or
production readiness. It proves a usable direct-seed path for the verified
milestone commit.
