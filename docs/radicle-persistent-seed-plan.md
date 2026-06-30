# Radicle Persistent Seed Plan

This plan defines the minimum path from the current retained-RID evidence to a user-facing always-available Radicle clone path.

## Current Evidence

- Retained RID: `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`
- Current verified commit: `ef16e2ad39d3e13bdcc9d454443c5bbb17733c68`
- Loop 73 evidence: `evidence/radicle-second-seed-tailnet-health-2026-06-29.json`
- Loop 73 bootstrap evidence: `evidence/radicle-ubuntu-work-follower-bootstrap-2026-06-29.json`
- Loop 74 evidence: `evidence/radicle-second-public-seed-health-2026-06-29.json`
- Loop 72 evidence: `evidence/radicle-public-seed-update-ef16e2a-2026-06-29.json`
- Loop 71 evidence: `evidence/radicle-external-health-timer-2026-06-29.json`
- Loop 70 evidence: `evidence/radicle-public-seed-update-propagation-2026-06-29.json`
- Loop 69 evidence: `evidence/radicle-public-seed-health-check-2026-06-29.json`
- Loop 68 evidence: `evidence/radicle-vps-follower-systemd-service-2026-06-29.json`
- Loop 67 evidence: `evidence/radicle-vps-follower-public-readback-2026-06-29.json`
- Loop 66 evidence: `evidence/radicle-seed-restart-check-2026-06-29.json`
- Loop 65 evidence: `evidence/radicle-independent-availability-check-2026-06-29.json`
- Reader A cloned the retained RID from the retained maintainer seed.
- Reader A then acted as a follower seed.
- Reader B cloned the retained RID from reader A and read back the same commit.
- Loop 66 started the retained seed on a local address, verified a fresh clone, stopped the seed, restarted it on the same local address with the same retained node ID, and verified a second fresh clone after restart.
- Loop 67 started a public VPS follower seed at `z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776`; a fresh reader on a separate Linux machine cloned the retained RID from that seed and read back the expected commit.
- Loop 68 installed the `openclaw` follower seed as an enabled user-level `systemd` service with restart policy and verified a fresh public readback after explicit service restart.
- Loop 69 added `scripts/check_public_radicle_seed.py` and used it for a fresh-profile public seed health check.
- Loop 70 advanced the same retained RID to `64efbada294d4a57c014a27398b92e344c6d68aa`, synced the `openclaw` follower through a temporary maintainer bridge, stopped the bridge and maintainer seed, and verified a fresh public readback from the VPS follower seed.
- Loop 71 installed an external `ubuntu-work` health timer that runs the public seed health check and wrote a passing latest JSON.
- Loop 72 advanced the same retained RID to `ef16e2ad39d3e13bdcc9d454443c5bbb17733c68`, synced the `openclaw` follower, stopped the bridge and maintainer seed, and verified a fresh public readback from the VPS follower seed.
- Loop 73 bootstrapped a second follower seed on `ubuntu-work` with node ID `z6MksRdjzuN2VYV4HTXdVSchitJ8Bq1zbx8WhBb3KhyfSm6A`, installed it as an enabled user-level `systemd` service, bound it to Tailnet address `100.83.206.66:8877`, and verified a fresh readback from `openclaw` over Tailnet.
- Loop 74 opened the approved `openclaw` public relay on TCP `8877`, verified public TCP reachability from Windows and `ubuntu-work`, and verified a fresh Radicle clone/readback through `z6MksRdjzuN2VYV4HTXdVSchitJ8Bq1zbx8WhBb3KhyfSm6A@187.77.19.162:8877`.

This proves an independent follower-seed handoff, a local seed restart/readback rehearsal, a restart-safe public follower service, a repeatable health check, one manual update propagation through the VPS follower, a second persistent follower seed with separate state, and a second public direct-seed address. It does not prove durability, broad public routing, automatic future update propagation, default public-routing availability, or independent provider/network availability for the second seed because public ingress still uses `openclaw`.

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
test "$(git rev-parse HEAD)" = "ef16e2ad39d3e13bdcc9d454443c5bbb17733c68"
```

Record health-check evidence only if command output is secret-free.

## Promotion Gate

Promote the persistent seed address into the public quickstart only after:

- A seed node is reachable from a separate network context.
- A fresh profile clone/readback matches the expected commit.
- A second repeated check passes after a time gap.
- Any new public internet relay port is explicitly approved before installation and verified with a fresh public readback.
- Retained state backup has been tested or at least manually verified.
- Failure modes are documented: stale commit, unreachable seed, bad peer address, corrupted retained state, and missing passphrase.

## Non-Claims

Even after a persistent seed is running, do not claim permanent durability, censorship resistance, global replication, identity trust, security, production readiness, SLSA compliance, full Radicle compatibility, or future default public-routing availability unless separate evidence supports those exact claims.
