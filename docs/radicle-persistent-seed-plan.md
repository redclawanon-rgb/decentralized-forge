# Radicle Persistent Seed Plan

This plan defines the minimum path from the current retained-RID evidence to a user-facing always-available Radicle clone path.

## Current Evidence

- Retained RID: `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`
- Current verified commit: `610fc3da9757d0cb123aa5976db552b991b766d4`
- Loop 67 evidence: `evidence/radicle-vps-follower-public-readback-2026-06-29.json`
- Loop 66 evidence: `evidence/radicle-seed-restart-check-2026-06-29.json`
- Loop 65 evidence: `evidence/radicle-independent-availability-check-2026-06-29.json`
- Reader A cloned the retained RID from the retained maintainer seed.
- Reader A then acted as a follower seed.
- Reader B cloned the retained RID from reader A and read back the same commit.
- Loop 66 started the retained seed on a local address, verified a fresh clone, stopped the seed, restarted it on the same local address with the same retained node ID, and verified a second fresh clone after restart.
- Loop 67 started a public VPS follower seed at `z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776`; a fresh reader on a separate Linux machine cloned the retained RID from that seed and read back the expected commit.

This proves an independent follower-seed handoff, a local seed restart/readback rehearsal, and one public direct-seed readback through the VPS follower. It does not prove durability, broad public routing, or default public-routing availability.

## Usable Product Claim To Target

The first usable product claim should be:

```text
A user can clone decentralized-forge from a published Radicle seed address and verify that HEAD equals the expected retained-RID commit.
```

Do not claim durable storage, censorship resistance, global availability, identity trust, security, or production readiness from that alone.

## Minimum Seed Service

A persistent seed needs:

- A host that can run `rad node` continuously.
- A stable reachable address and port for Radicle peer connections.
- Retained project Radicle state stored outside the Git repository and outside the portable verification bundle.
- A documented secret backup and recovery process for the retained maintainer state.
- A non-secret public seed address that can be published in `docs/radicle-retained-rid-quickstart.md`.
- A health check that verifies clone/readback against the expected commit from a separate fresh Radicle profile.
- A stop/runbook that can intentionally stop the seed without corrupting retained state.

## Candidate Runtime

Use a small Linux host or VM with:

```sh
export RAD_HOME=/srv/decentralized-forge/radicle/maintainer-rad-home
export RAD_PASSPHRASE_FILE=/srv/decentralized-forge/secrets/maintainer.passphrase
export RADICLE_BIN_DIR=/opt/radicle/bin

rad node start -- --listen 0.0.0.0:<port>
rad seed rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy --scope all --no-fetch
rad sync --inventory
rad sync --announce --timeout 60s --replicas 1 rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy
```

The exact service manager can be systemd, a supervised container, or another host-native process manager. Do not commit the passphrase, Radicle key material, or retained state.

## Health Check

The health check should run from separate disposable state:

```sh
rad auth --alias decentralized-forge-healthcheck --stdin
rad node start
rad node connect z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776 --timeout 30s
rad clone --timeout 120s --seed z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy decentralized-forge
cd decentralized-forge
test "$(git rev-parse HEAD)" = "610fc3da9757d0cb123aa5976db552b991b766d4"
```

Record health-check evidence only if command output is secret-free.

## Promotion Gate

Promote the persistent seed address into the public quickstart only after:

- A seed node is reachable from a separate network context.
- A fresh profile clone/readback matches the expected commit.
- A second repeated check passes after a time gap.
- Retained state backup has been tested or at least manually verified.
- Failure modes are documented: stale commit, unreachable seed, bad peer address, corrupted retained state, and missing passphrase.

## Non-Claims

Even after a persistent seed is running, do not claim permanent durability, censorship resistance, global replication, identity trust, security, production readiness, SLSA compliance, full Radicle compatibility, or future default public-routing availability unless separate evidence supports those exact claims.
