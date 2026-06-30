# First Public Clone Outside-Reader Rehearsal

This rehearsal is the copy/paste path for a reader who wants to verify the current public Radicle direct-seed clone without receiving maintainer state or private key material.

## Plan First

From a fresh clone of this repository:

```sh
python scripts/run_first_public_clone_rehearsal.py
python scripts/run_first_public_clone_rehearsal.py --seed primary
python scripts/run_first_public_clone_rehearsal.py --seed second
```

The default command only prints a JSON plan. It does not contact public seeds, start daemons, sign, publish, copy maintainer state, or write evidence.

## Execute On A Reader Machine

After installing Radicle CLI on a Linux reader machine:

```sh
python scripts/run_first_public_clone_rehearsal.py --execute --seed both --output evidence/first-public-clone-outside-reader-rehearsal.json
```

For manual execution, the underlying commands are:

```sh
python scripts/forge_registry.py verify-first-public-clone --seed primary --json --output evidence/radicle-first-public-clone-outside-reader-primary-YYYY-MM-DD.json
python scripts/forge_registry.py verify-first-public-clone --seed second --json --output evidence/radicle-first-public-clone-outside-reader-second-YYYY-MM-DD.json
```

Successful output verifies that the selected public seed cloned retained RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` and that `git rev-parse HEAD` matched commit `d596024dac0d90605d4f103d567e5851771be5a8`.

## Status Artifact

The current committed public seed evidence is summarized by:

```sh
python scripts/forge_registry.py public-seed-status output/public-seed-status.json
```

The artifact is machine-readable and evidence-bounded. It is suitable for a release handoff or outside-reader checklist, but it is not an uptime monitor.

## Non-Claims

- This does not prove permanent durability or default public routing.
- This does not prove automatic repair and is not proof of automatic future update propagation.
- This does not prove broad Radicle network availability, identity trust, security, or production readiness.
- Execute mode verifies only the exact selected direct-seed path for the exact retained RID and expected commit printed in the output.
