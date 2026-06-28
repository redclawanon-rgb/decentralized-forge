# Live Completion Gates

Milestone 1 can finish without additional live protocol actions. The current evidence set is already enough for a reproducible static prototype when CI, reusable CLI tooling, second-fixture coverage, and exports are complete.

Further live work is optional and must be targeted explicitly. Use `scripts/live_gate_inventory.py` to inspect local tool availability before choosing a lane:

```sh
python scripts/live_gate_inventory.py
```

The inventory script is intentionally read-only. It does not start daemons, publish events, fetch from relays, run Radicle network commands, sign artifacts, use keys, spend money, or contact anyone.

## Gate 1: Live IPFS Storage Check

Allowed only after an explicit live-storage target.

Possible evidence:

- exact tool versions;
- local daemon or client command used;
- `ipfs add` or equivalent for the existing local artifact/CAR;
- fetch/readback result from the chosen local daemon or public gateway;
- failures and divergence recorded without retry spam.

Non-claims:

- no durability guarantee;
- no pinning guarantee unless pinning is actually configured and verified;
- no Filecoin/Arweave claim without wallet/spend approval;
- no censorship-resistance or production-readiness claim.

## Gate 2: Nostr Issue/Patch Readback

Allowed only with a disposable project-scoped key target.

Possible evidence:

- one issue event and one patch event derived from existing fixtures;
- selected free relays declared before publication;
- local event ID/signature verification;
- readback by event ID from selected relays;
- explicit relay divergence.

Non-claims:

- no global propagation guarantee;
- no durability guarantee;
- no identity-trust guarantee;
- no full NIP-34 or forge compatibility claim.

## Gate 3: Broader Radicle Public-Network Check

Allowed only with an explicit repeated/broader Radicle target.

Possible evidence:

- repeated disposable public smoke runs;
- declared seed/clone topology;
- temporary state cleanup;
- exact RID/NID values;
- readback results and failures.

Non-claims:

- no persistent seed operation unless separately approved;
- no broad network availability claim from a small smoke set;
- no durability, censorship-resistance, security, or production-readiness claim.

## Gate 4: Optional Signing/Provenance

Allowed only with disposable or keyless test-signing material.

Possible evidence:

- exact signing command;
- verification command;
- artifact digest;
- public transparency log result only if actually used;
- clear replacement path from synthetic provenance to verified test provenance.

Non-claims:

- no production signing claim;
- no SLSA level claim unless the full SLSA criteria are met and documented;
- no private personal key use.
