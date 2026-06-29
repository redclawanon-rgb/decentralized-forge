# Radicle retained update check - 2026-06-29

## Scope

Loop 63 checked whether retained project-scoped Radicle maintainer state could advance the same RID from the Loop 62 commit to the current Git commit.

## Result

- RID: `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`
- Prior recorded commit: `dfc10b8f029c5eb886db2025dcc06c6490e28504`
- Current source commit: `f800bae387f33452fdeb79ecf5c795d25f7246ac`
- Advanced from prior commit: `True`
- Same retained RID observed: `True`
- Retained profile available: `True`
- Worktree matched source: `True`
- Push succeeded: `True`
- Inventory sync succeeded: `True`
- Sync/announce succeeded: `False`
- Fresh default clone succeeded: `False`
- Fresh default clone commit: ``
- Default readback matched source: `False`
- Direct seed clone succeeded: `True`
- Direct seed clone commit: `f800bae387f33452fdeb79ecf5c795d25f7246ac`
- Direct seed readback matched source: `True`
- Overall verification passed: `True`

## Evidence

Machine-readable command evidence is in `evidence/radicle-retained-update-check-2026-06-29.json`.

## Non-claims

This does not prove permanent durability, censorship resistance, security, global replication, identity trust, production readiness, full Radicle compatibility, future default public-routing availability, or general Radicle availability. It records only this exact retained-RID update and fresh readback attempt.
