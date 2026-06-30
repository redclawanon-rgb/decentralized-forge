# Retained Radicle RID Quickstart

This is the current community clone path for the first retained Radicle repository for this project.

The verified retained RID is:

```text
rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy
```

Loop 75 verified that this RID advanced to commit:

```text
d596024dac0d90605d4f103d567e5851771be5a8
```

The strongest matching evidence is `evidence/radicle-public-seed-update-d596024-2026-06-30.json`: the retained RID advanced to the updated commit, stale follower caches were refreshed with host-local backups, the temporary retained maintainer seed was stopped, and a fresh reader on `ubuntu-work` cloned the updated commit from both public seed addresses.

Loop 73 added a second persistent follower seed on `ubuntu-work` with its own Radicle state and node ID `z6MksRdjzuN2VYV4HTXdVSchitJ8Bq1zbx8WhBb3KhyfSm6A`. Loop 74 verified public readback through `z6MksRdjzuN2VYV4HTXdVSchitJ8Bq1zbx8WhBb3KhyfSm6A@187.77.19.162:8877`, which relays from `openclaw` public ingress to the `ubuntu-work` seed over Tailnet. Loop 75 verified that both public seed addresses now serve the current commit.

## Generate The Current Recipe

Run this read-only command from a checkout of the repository:

```sh
python scripts/forge_registry.py radicle-retained-quickstart
```

For machine-readable output:

```sh
python scripts/forge_registry.py radicle-retained-quickstart --json
```

The command reads `fixtures/live-evidence-index.json`, checks the strongest retained-RID readback fields, and prints the exact retained RID, expected commit, commands, and non-claims. It does not start a Radicle node, connect to peers, clone, publish, sign, or use private keys.

## Maintainer-Assisted Direct-Seed Clone

Loop 75 proved public direct-seed update readback through both public follower seed addresses. Default public-routing availability is still not claimed, so the supported community path is direct seed:

1. Use the current public seed address: `z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776`.
2. Connect to that peer from a fresh Radicle profile.
3. The reader uses Radicle 1.9.1 or compatible tooling to connect to that peer and clone the retained RID.
4. The reader checks that `git rev-parse HEAD` prints `d596024dac0d90605d4f103d567e5851771be5a8`.

Template commands:

```sh
rad auth --alias decentralized-forge-reader --stdin
rad node start
rad node connect z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776 --timeout 30s
rad clone --timeout 120s --seed z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy decentralized-forge
cd decentralized-forge
git rev-parse HEAD
```

Fallback public seed:

```sh
rad node connect z6MksRdjzuN2VYV4HTXdVSchitJ8Bq1zbx8WhBb3KhyfSm6A@187.77.19.162:8877 --timeout 30s
rad clone --timeout 120s --seed z6MksRdjzuN2VYV4HTXdVSchitJ8Bq1zbx8WhBb3KhyfSm6A rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy decentralized-forge
```

## Claim Boundary

This quickstart is a narrow reproduction path for the retained RID evidence. It is not a default public-routing claim, not a durability guarantee, not proof of automatic future update propagation, not proof of broad Radicle network availability, not proof of independent provider availability for the second seed, not proof of censorship resistance, not proof of identity trust, not a security guarantee, not production readiness, not a committed secret or key backup, and not maintainer key material on the VPS or `ubuntu-work`.

The persistent-seed plan is `docs/radicle-persistent-seed-plan.md`.
