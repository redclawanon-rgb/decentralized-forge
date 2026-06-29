# Radicle seed restart check - 2026-06-29

## Scope

Loop 66 checked whether the retained Radicle seed can be stopped, restarted on the same local address, and still serve the retained RID to fresh readers.

## Result

- RID: `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`
- Prior verified commit: `7262f69b82e442263d6261414f6b771be04c6b6f`
- Current source commit: `4c8cd6183e2e12d1c62af7d2f013fb085b2d6bf8`
- Seed listen address: `127.0.0.1:8799`
- First fresh reader cloned before restart: `True`
- First reader readback commit: `4c8cd6183e2e12d1c62af7d2f013fb085b2d6bf8`
- First reader readback matched source: `True`
- Seed stop after first reader succeeded: `True`
- Restarted seed node ID matched retained peer: `True`
- Second fresh reader cloned after restart: `True`
- Second reader readback commit: `4c8cd6183e2e12d1c62af7d2f013fb085b2d6bf8`
- Second reader readback matched source: `True`
- Persistent service left running: `False`
- Overall verification passed: `True`

## Evidence

Machine-readable command evidence is in `evidence/radicle-seed-restart-check-2026-06-29.json`.

## Non-claims

This does not prove permanent durability, censorship resistance, security, global replication, identity trust, production readiness, full Radicle compatibility, future default public-routing availability, public reachability, separate-network availability, or always-on seed operation. It records only this exact retained-RID local seed restart/readback rehearsal.
