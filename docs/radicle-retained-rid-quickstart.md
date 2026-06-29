# Retained Radicle RID Quickstart

This is the current community clone path for the first retained Radicle repository for this project.

The verified retained RID is:

```text
rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy
```

Loop 63 verified that this RID advanced to commit:

```text
f800bae387f33452fdeb79ecf5c795d25f7246ac
```

The matching evidence is `evidence/radicle-retained-update-check-2026-06-29.json`.

## Generate The Current Recipe

Run this read-only command from a checkout of the repository:

```sh
python scripts/forge_registry.py radicle-retained-quickstart
```

For machine-readable output:

```sh
python scripts/forge_registry.py radicle-retained-quickstart --json
```

The command reads `fixtures/live-evidence-index.json`, checks the Loop 63 direct-seed readback fields, and prints the exact retained RID, expected commit, commands, and non-claims. It does not start a Radicle node, connect to peers, clone, publish, sign, or use private keys.

## Maintainer-Assisted Direct-Seed Clone

Loop 63 did not observe default public-routing readback for the updated commit. The supported community path is therefore direct seed:

1. A maintainer starts a reachable Radicle seed for the retained RID.
2. The maintainer shares a session-specific peer address in this shape: `<maintainer-peer-id>@<reachable-host>:<port>`.
3. The reader uses Radicle 1.9.1 or compatible tooling to connect to that peer and clone the retained RID.
4. The reader checks that `git rev-parse HEAD` prints `f800bae387f33452fdeb79ecf5c795d25f7246ac`.

Template commands:

```sh
rad auth --alias decentralized-forge-reader --stdin
rad node start
rad node connect <maintainer-peer-id>@<reachable-host>:<port> --timeout 30s
rad clone --timeout 120s --seed <maintainer-peer-id> rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy decentralized-forge
cd decentralized-forge
git rev-parse HEAD
```

## Claim Boundary

This quickstart is a narrow reproduction path for the retained RID evidence. It is not a default public-routing claim, not a persistent public seed service claim, not a durability guarantee, not proof of broad Radicle network availability, not proof of censorship resistance, not proof of identity trust, not a security guarantee, not production readiness, and not a committed secret or key backup.
