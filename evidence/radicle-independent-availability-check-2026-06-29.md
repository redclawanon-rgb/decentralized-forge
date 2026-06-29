# Radicle independent availability check - 2026-06-29

## Scope

Loop 65 checked whether the retained Radicle RID could be advanced to the current Git commit and then read back through an independent follower seed.

## Result

- RID: `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`
- Prior verified commit: `f800bae387f33452fdeb79ecf5c795d25f7246ac`
- Current source commit: `7262f69b82e442263d6261414f6b771be04c6b6f`
- Same retained RID observed: `True`
- Reader A cloned from maintainer seed: `True`
- Reader A readback commit: `7262f69b82e442263d6261414f6b771be04c6b6f`
- Reader A readback matched source: `True`
- Reader A follower seed succeeded: `True`
- Reader B connected to follower: `True`
- Reader B cloned from follower seed: `True`
- Reader B readback commit: `7262f69b82e442263d6261414f6b771be04c6b6f`
- Reader B readback matched source: `True`
- Overall verification passed: `True`

## Evidence

Machine-readable command evidence is in `evidence/radicle-independent-availability-check-2026-06-29.json`.

## Non-claims

This does not prove permanent durability, censorship resistance, security, global replication, identity trust, production readiness, full Radicle compatibility, future default public-routing availability, persistent public seed operation, or general Radicle availability. It records only this exact retained-RID update and independent follower-seed readback attempt.
