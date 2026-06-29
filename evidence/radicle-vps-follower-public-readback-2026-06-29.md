# Radicle VPS follower public readback - 2026-06-29

## Scope

Loop 67 checked whether a fresh reader on a separate Linux machine could clone the retained Radicle RID from a public VPS follower seed.

## Result

- RID: `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`
- Expected commit: `610fc3da9757d0cb123aa5976db552b991b766d4`
- VPS seed: `z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776`
- Public TCP reachability observed: `True`
- Fresh reader host: `ubuntu-work`
- Fresh reader cloned from VPS seed: `True`
- Fresh reader readback commit: `610fc3da9757d0cb123aa5976db552b991b766d4`
- Fresh reader readback matched expected commit: `True`
- Retained maintainer state copied to VPS: `False`
- VPS follower seed left running: `True`
- Overall verification passed: `True`

## Evidence

Machine-readable evidence is in `evidence/radicle-vps-follower-public-readback-2026-06-29.json`.

## Non-claims

This does not prove permanent durability, censorship resistance, security, global replication, identity trust, production readiness, full Radicle compatibility, or future default public-routing availability. It records only this exact public direct-seed readback through the `openclaw` VPS follower seed.
