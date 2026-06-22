# Radicle public-network gate plan

Created 2026-06-22 from Loop 30 Permission-F preflight.

## Status

**Permission G was granted and one disposable smoke is complete.**

This file originally prepared a public Radicle seed/publish/remote-clone smoke. Eric approved Permission G on 2026-06-22 via Telegram message “G & I are approved to keep things moving along.” The bounded smoke evidence is in `evidence/radicle-public-network-smoke-2026-06-22.json` and `.md`; the help-only preflight remains in `evidence/radicle-public-network-preflight-2026-06-22.md`.

## Current verified baseline

- Radicle CLI is installed user-locally at `/home/openclaw/.local/bin/rad`.
- Version inspected in Loop 30: `rad 1.9.1 (5bd3569e120a6172d9df68e1d1d0eed15e8104b1)`.
- Loop 23 already verified only a temporary private local replay with `rad init --private --no-confirm --no-seed` and `rad inspect`.
- Before Loop 34, no public Radicle node, seed, publish, sync, remote clone, or network replication had been verified.
- Loop 34 verified one exact disposable public Radicle smoke for RID `rad:z2WtozFrCRhygh9CGzyUN57CN7Nwa`: public init/visibility, localhost node start, seed policy update, sync/announce, separate temporary clone node connection, `rad clone --seed <disposable NID>`, and README readback. This remains exact-smoke evidence only, not a durability/censorship-resistance/security/global-replication/production claim.

## Help-only findings that matter

- `rad publish` makes a private repository public and discoverable on the network.
- `rad seed <RID>` creates/updates a seeding policy; default behavior can fetch after policy update unless `--no-fetch` is used.
- `rad sync` defaults to fetching from connected seeds and announcing local refs to peers.
- `rad node start` starts the local Radicle node and is the boundary between local CLI evidence and network behavior.
- `rad node connect <NID[@ADDR]>` initiates peer connection.
- `rad remote add <NID>` defaults may fetch and sync unless `--no-fetch --no-sync` are used.
- `rad clone <RID>` uses the local node routing table or explicit `--seed` values to fetch a repository.
- `rad fetch` is not a known command in Radicle 1.9.1.

## Draft Permission G checklist

Do not execute this checklist unless Eric explicitly grants Permission G.

### Preconditions

- Eric approves: “Permission G for one disposable public Radicle seed/remote-clone smoke.”
- No paid infrastructure, production/private personal keys, or direct outreach.
- A fresh `git status --short --branch` is clean or changes are understood.
- A disposable `RAD_HOME` and disposable Git repo are used.
- Evidence paths are chosen before execution and must not contain secrets.
- The public update language is prototype/research-only.

### Candidate smoke sequence

1. Create a temporary `RAD_HOME` and disposable Git repository.
2. Create a harmless README-only commit that clearly identifies the repo as a Decentralized Forge prototype smoke.
3. Run `rad auth --stdin` inside the temporary `RAD_HOME` only.
4. Initialize the disposable repo with the least-surprising public path:
   - preferred only if help/output confirms intent: `rad init --name <name> --description <prototype description> --default-branch master --public --no-confirm --no-seed <repo>`;
   - fallback if public init semantics are unclear: repeat the proven private `--no-seed` path and stop before `rad publish` until the exact publish step is reviewed.
5. Inspect RID/identity/refs/visibility locally.
6. Start the Radicle node only under Permission G and capture node ID/status without dumping noisy logs.
7. Publish/seed/sync only the disposable RID, with explicit timeouts and bounded replica/seed expectations.
8. Attempt one remote clone/fetch/readback from separate temporary state only if seed/publish output is clear and no paid/auth gate appears.
9. Stop node/processes and remove temporary state.
10. Update evidence, tests/checklist, project status, context, and non-claim wording.

## Abort conditions

Stop immediately if any of these occur:

- CLI asks for production/private personal identity material.
- A command requires payment, hosted infrastructure, account setup, or a paid seed.
- A command tries to affect a non-disposable repo or persistent personal `RAD_HOME`.
- Public behavior is ambiguous or cannot be labeled as disposable prototype work.
- A peer/remote selection would become direct outreach or target a specific person.
- Evidence would require recording secrets.
- Results would tempt unsupported claims about durability, censorship resistance, identity trust, security, global replication, or production readiness.

## Claims allowed after a future successful Permission-G smoke

Only if backed by command evidence:

- “A disposable prototype Radicle repository was publicly published/seeded and cloned/fetched in one bounded smoke.”
- “The specific RID/NID/commands in the evidence succeeded at that time.”

Still not allowed without much more evidence:

- durable availability;
- censorship resistance;
- global propagation;
- security guarantees;
- identity trust;
- production readiness;
- full Radicle compatibility;
- full decentralized forge viability.

## Current next gate

The single approved Permission-G disposable smoke is complete. Further Radicle public-network actions — for example repeated availability checks, broader peer/seed testing, long-running seed persistence, public claims beyond the exact smoke, or use of non-disposable identities/infrastructure — require a new explicit approval/target. Radicle is now verified only for (a) the Loop 23 local private replay and (b) the exact Loop 34 disposable public seed/clone/readback smoke.
