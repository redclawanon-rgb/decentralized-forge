# Retained Radicle RID Quickstart

This is the current community clone path for the first retained Radicle repository for this project.

The verified retained RID is:

```text
rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy
```

Loop 66 verified that this RID advanced to commit:

```text
4c8cd6183e2e12d1c62af7d2f013fb085b2d6bf8
```

The strongest matching evidence is `evidence/radicle-seed-restart-check-2026-06-29.json`: one fresh reader cloned from the retained seed before restart, the retained seed stopped and restarted on the same local address with the same node ID, and another fresh reader cloned the same commit after restart.

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

Loop 66 proved a local retained-seed restart/readback rehearsal, and Loop 65 proved an independent follower-seed handoff. Neither loop created a persistent public seed service, observed a publicly reachable seed address, or proved default public-routing availability. The supported community path is therefore direct seed:

1. A maintainer or follower starts a reachable Radicle seed for the retained RID.
2. The seed operator shares a session-specific peer address in this shape: `<seed-peer-id>@<reachable-host>:<port>`.
3. The reader uses Radicle 1.9.1 or compatible tooling to connect to that peer and clone the retained RID.
4. The reader checks that `git rev-parse HEAD` prints `4c8cd6183e2e12d1c62af7d2f013fb085b2d6bf8`.

Template commands:

```sh
rad auth --alias decentralized-forge-reader --stdin
rad node start
rad node connect <seed-peer-id>@<reachable-host>:<port> --timeout 30s
rad clone --timeout 120s --seed <seed-peer-id> rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy decentralized-forge
cd decentralized-forge
git rev-parse HEAD
```

## Claim Boundary

This quickstart is a narrow reproduction path for the retained RID evidence. It is not a default public-routing claim, not a persistent public seed service claim, not a durability guarantee, not proof of broad Radicle network availability, not proof of censorship resistance, not proof of identity trust, not a security guarantee, not production readiness, and not a committed secret or key backup.

The persistent-seed plan is `docs/radicle-persistent-seed-plan.md`.
