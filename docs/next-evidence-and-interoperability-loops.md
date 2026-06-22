# Next evidence and interoperability loop set

Created 2026-06-22 after Loops 22–25 completed Radicle local replay and selected-relay Nostr publish/readback evidence.

This document sets up the next six logical loops without executing live/public actions. It is safe to commit because it contains no secrets and does not publish, seed, pin, deploy, spend, or contact anyone by itself.

## Current verified evidence inputs

- **Loop 23 Radicle local replay:** `evidence/radicle-local-replay-2026-06-22.md`
  - Temporary `RAD_HOME` and disposable private repository replay succeeded locally.
  - No Radicle node start, public seed, sync, remote peer, or public network replication was performed.
- **Loop 25 Nostr selected-relay publish/readback:**
  - `evidence/nostr-loop25-publish-readback-2026-06-22.md`
  - `evidence/nostr-loop25-publish-readback-2026-06-22.json`
  - Event `4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba` was published to and read back from `wss://relay.damus.io` and `wss://nos.lol` using only the disposable project key.
  - This proves selected-relay acceptance/readback only, not durability, global propagation, censorship resistance, identity trust, security, production readiness, or full protocol compatibility.

## Existing approvals that still cover some work

Eric already granted, on 2026-06-22 via Telegram:

- Permission A: bounded Radicle local replay with temporary/disposable state and no public seed/network publication.
- Permission B: public Nostr relay publish/readback using only the disposable project key, prototype/research-labeled, no spam, no overclaims.
- Permission C: low-noise durable controller automation for approved loops.
- Public update posting when accurate, non-spammy, and prototype/research-labeled.

Still forbidden unless Eric explicitly grants a new approval:

- spending money;
- paid infrastructure;
- production/private personal keys;
- direct outreach to specific people;
- unsupported security/durability/censorship-resistance/production-readiness claims;
- public Radicle seed/publish/sync/remote replication beyond local replay;
- IPFS/Filecoin/Arweave pinning, wallet use, or paid storage.

## New approval recorded for this loop set

**Granted 2026-06-22 via Telegram voice:** Eric approved Permission D + Permission E + Permission F + Permission H for Loops 26–32. Per Harry's recommendation, Eric explicitly chose to hold Permission G for now and see where the preflight work lands.

This means the next controller may run Loops 26–32 within D/E/F/H, but must stop before any public Radicle seed/publish/sync/node/remote clone action, spending, paid infrastructure, production/private personal keys, direct outreach, paid storage/wallet use, or unsupported security/durability/censorship-resistance/production-readiness claims.

## New/renewed permission bundles to remove roadblocks

Eric can approve these individually or as a bundle before execution.

### Permission D — Renew low-noise controller for Loops 26–31

Allow Harry to create a bounded low-noise Hermes cron/controller for this next loop set that:

- runs from `/home/openclaw/projects/decentralized-forge`;
- reads `.hermes/context.md`, `STATUS.md`, `AGENT-LOOPS.md`, this file, and prior evidence before acting;
- executes only loops covered by existing or newly granted approvals;
- commits and pushes only after tests/preflight/secret scans pass;
- sends concise Telegram summaries at loop boundaries or blockers only;
- stops before any unapproved gate.

### Permission E — Nostr follow-up live evidence using disposable project key

Allow one or more additional low-volume Nostr checks/events using only the disposable project key:

- re-read Loop 25 event from selected and optional extra free public relays;
- optionally publish one additional prototype/research-labeled metadata/status event if needed for adapter testing;
- record relay URLs, event IDs, publish/readback responses, and `nak verify` results;
- no spam, no production keys, no unsupported claims.

Existing Permission B already covers this in spirit, but this renewed bundle makes it explicit for the next loop set.

### Permission F — Radicle public-network preflight only, no seed yet

Allow read-only/preflight research for a later Radicle public-network gate:

- inspect `rad publish`, `rad seed`, `rad sync`, node/start, remote, and clone/fetch help/docs;
- draft a no-surprises public-seed/remote-clone plan;
- do **not** run `rad node start`, `rad publish`, `rad seed`, `rad sync`, peer announce, or remote clone/fetch yet.

### Permission G — Radicle public seed/remote clone smoke

Not needed for Loops 26–31 unless Eric wants to remove the next major roadblock early.

If granted later, allow a clearly prototype-labeled disposable/public Radicle repository seed/publish and remote clone/fetch/readback smoke with no production keys, no paid infrastructure, no durability/censorship-resistance claims, and explicit stop conditions.

### Permission H — Public immutable storage preflight only

Allow free/read-only preflight for IPFS/IPLD storage options:

- local-only CID/CAR planning;
- inspect free local daemon/client options if already installed or installable user-locally without curl-pipe-shell risk;
- no paid pinning, no Filecoin/Arweave wallet, no paid storage, no durability claims.

## Loop 26 — Live evidence import into adapter/renderer

**Status:** Complete 2026-06-22 as bounded live/local evidence import; no new live network action.

**Result:**

1. Added `fixtures/live-evidence-index.json` with:
   - Radicle local CLI replay evidence from Loop 23;
   - Nostr selected-relay publish/readback evidence from Loop 25;
   - claim boundaries and non-claims.
2. Updated `fixtures/live-adapter-replay-checklist.json` with Loop 26 import state.
3. Updated `scripts/render_project_page.py`, `scripts/preflight_static_artifact.py`, tests, and `output/demo-project.html` so the UI distinguishes:
   - fixture-only;
   - local CLI verified;
   - selected-relay readback verified;
   - still-unverified protocol claims.
4. Verification is recorded in `STATUS.md` for Loop 26.

**Artifacts:**

- `fixtures/live-evidence-index.json`
- `scripts/render_project_page.py`
- `scripts/preflight_static_artifact.py`
- `tests/test_registry_fixture.py`
- `output/demo-project.html`

**Boundary preserved:**

No claim was upgraded beyond Loop 23/25 evidence. No new Nostr publish/readback, Radicle node/seed/publish/sync/remote clone, spending, paid infrastructure, production/private personal key use, direct outreach, or unsupported durability/global-propagation/censorship-resistance/security/production-readiness/full-compatibility claim occurred.

## Loop 27 — Public project update draft/post

**Status:** Complete 2026-06-22 as a prototype/research-labeled public GitHub Discussion update.

**Result:**

1. Drafted `docs/public-update-drafts/2026-06-22-live-adapter-evidence-update.md`.
2. Posted it to the public project GitHub Discussions / Announcements channel.
3. Posted URL: <https://github.com/redclawanon-rgb/decentralized-forge/discussions/6>.
4. Wording preserves narrow claims: Radicle local CLI/private replay only; Nostr selected-relay acceptance/readback only; no durability/global-propagation/censorship-resistance/security/production-readiness/full-compatibility claim.

**Boundary preserved:**

No direct outreach, spending, paid infrastructure, production/private personal key use, Radicle node/seed/publish/sync/remote clone, Filecoin/Arweave wallet/pinning/storage action, or unsupported claim occurred.

**Goal:** Publish or at least draft a concise public project update that accurately reports the prototype/research evidence and next gates.

**Approval needed:** existing public update approval is sufficient if the update is accurate, non-spammy, and prototype/research-labeled. If confidence is low, draft locally only and ask Eric.

**Tasks:**

1. Draft under `docs/public-update-drafts/`.
2. Include exact verified scope:
   - Radicle local private replay only;
   - Nostr selected-relay acceptance/readback only;
   - no durability/global/censorship/production claims.
3. If posting, use a public project channel/surface, not direct outreach.
4. Record posted URL or keep draft-only status.

**Artifacts:**

- `docs/public-update-drafts/2026-06-22-live-adapter-evidence-update.md`
- optional posted URL evidence if published

**Verification:**

- secret-marker scan;
- non-claim phrase review;
- if posted, fetch/verify public URL if available.

**Stop conditions:**

- Any wording implies production readiness, censorship resistance, durability, or broad protocol compatibility.
- Posting target requires payment, production credentials, or direct person outreach.

## Loop 28 — Nostr readback persistence/divergence check

**Status:** Complete 2026-06-22 as readback-only persistence/divergence evidence; no new publish.

**Result:**

1. Re-read event `4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba` by ID from the two Loop 25 selected relays plus two Permission-E extra readback-only relays.
2. `wss://relay.damus.io`, `wss://nos.lol`, and `wss://relay.primal.net` returned the exact event; fields matched the signed preview and `nak verify` passed.
3. `wss://nostr.wine` did not return the event during this check.
4. No new Nostr event was published and no secret key material was read or printed.

**Artifacts:**

- `evidence/nostr-loop28-readback-check-2026-06-22.md`
- `evidence/nostr-loop28-readback-check-2026-06-22.json`

**Boundary preserved:**

This is selected/limited relay readback evidence only. It is not a durability guarantee, global propagation proof, censorship-resistance proof, identity-trust proof, production-readiness claim, security guarantee, or full NIP-34/forge compatibility claim. No paid/authenticated relay, production/private personal key, direct outreach, spending, or Radicle public-network action occurred.

**Goal:** Re-read the Loop 25 event after time has passed and record whether selected relays still return the same event.

**Approval needed:** Permission E if querying additional public relays or publishing another event. Re-reading the two already-used relays is low-risk and covered by prior live evidence scope.

**Tasks:**

1. Query `wss://relay.damus.io` and `wss://nos.lol` by Loop 25 event ID.
2. Optionally query a small number of extra free public relays if Permission E is granted.
3. Verify returned event IDs/signatures with `nak verify`.
4. Record divergence: returned/not returned, fields match, verify pass/fail.

**Artifacts:**

- `evidence/nostr-loop28-readback-check-YYYY-MM-DD.json`
- `evidence/nostr-loop28-readback-check-YYYY-MM-DD.md`

**Verification:**

- `nak verify` on all readback events that are returned;
- JSON schema/shape check;
- tests if imported into fixtures.

**Stop conditions:**

- Relay requires payment/auth/production credentials.
- Extra relay use would become spammy or broad scanning.

## Loop 29 — NIP-34 live-event adapter import

**Status:** Complete 2026-06-22 as selected-relay readback evidence import; no new Nostr publish/fetch/signing.

**Result:**

1. Added `fixtures/nostr-live-readback-events.json` referencing Loop 25 evidence.
2. Updated `scripts/nip34_adapter.py` to import the recorded kind `30617` live event separately from dry-run fixtures, recompute the NIP-01 event ID locally, and emit a narrowly scoped `live-verified` adapter row for selected-relay readback only.
3. Updated `scripts/render_project_page.py`, static preflight, tests, checklist, and `output/demo-project.html` to show **NIP-34 live readback import** without broad compatibility claims.
4. No new relay publish, relay fetch, signing, key read, or live network action occurred in Loop 29.

**Boundary preserved:** selected-relay readback evidence only. This does not verify durability, global propagation, censorship resistance, identity trust, security, production readiness, full NIP-34/forge compatibility, issue/patch readback, repository-state readback, status semantics, relay discovery, subscription behavior, deletion/replacement behavior, or multi-client behavior.

**Goal:** Convert the verified live Nostr event/readback evidence into the local NIP-34 adapter path without pretending it is full forge compatibility.

**Approval needed:** none if using existing evidence only; Permission E if a new event is published for adapter coverage.

**Tasks:**

1. Add a live-event fixture or index entry referencing Loop 25 evidence.
2. Teach the adapter/renderer/tests to show this as `selected_relay_readback_verified` or similar.
3. Keep existing dry-run fixtures separate from live readback evidence.
4. Document missing NIP-34 semantics that remain unverified.

**Artifacts:**

- optional `fixtures/nostr-live-readback-events.json`
- adapter/renderer/tests if needed
- docs update explaining live-event import boundaries

**Verification:**

- unit tests for adapter import state;
- static preflight;
- secret-marker scan.

**Stop conditions:**

- Import would blur fixture-only and live-readback states.
- Renderer wording overclaims full protocol compatibility.

## Loop 30 — Radicle public-network gate plan

**Status:** Complete 2026-06-22 as Permission-F help-only public-network preflight; Permission G remains ungranted/blocked.

**Result:**

1. Added `docs/radicle-public-network-gate-plan.md` with a draft Permission-G disposable public seed/remote-clone smoke checklist.
2. Added `evidence/radicle-public-network-preflight-2026-06-22.md` with help-only command-surface findings.
3. Inspected `rad publish`, `rad seed`, `rad sync`, `rad sync status`, `rad node`, `rad node start`, `rad node status`, `rad node connect`, `rad remote`, `rad remote add`, `rad remote list`, `rad clone`, `rad fetch`, `rad unseed`, and `rad follow` via `--help` only.
4. Recorded that `rad publish` makes a repository public/discoverable, `rad sync` defaults to fetch+announce, `rad remote add` defaults may fetch/sync, `rad clone` uses local node routing or explicit seeds, and `rad fetch` is not a known command in Radicle 1.9.1.

**Boundary preserved:** No `RAD_HOME` was created, no Radicle identity was created/reused, no node was started, no repository was published/seeded/synced/announced/cloned/fetched/connected/followed/remotely configured, and no public Radicle network action occurred. Permission G remains required before any public Radicle seed/publish/sync/node/remote clone/fetch action.

**Goal:** Prepare a no-surprises plan for the next major Radicle milestone: public seed/publish/remote clone verification.

**Approval needed:** Permission F for preflight. Permission G is required before any public seed/publish/sync/node/remote clone action.

**Tasks under Permission F:**

1. Inspect local `rad publish`, `rad seed`, `rad sync`, `rad node`, `rad remote`, clone/fetch help/docs.
2. Identify exact commands that would be needed for a disposable public Radicle seed/clone smoke.
3. Identify risks: identity persistence, network publication, cleanup, peer visibility, unsupported claims.
4. Draft the Permission G execution checklist but do not execute it.

**Artifacts:**

- `docs/radicle-public-network-gate-plan.md`
- optional `evidence/radicle-public-network-preflight-YYYY-MM-DD.md`

**Verification:**

- help/docs captured;
- no stateful/public Radicle network command executed;
- tests/static preflight unchanged or passing.

**Stop conditions:**

- Any command would start node/network behavior before Permission G.
- Any plan requires production keys, paid infrastructure, or unsupported claims.

## Loop 31 — Public storage/IPFS evidence gate plan

**Goal:** Plan the next artifact-storage verification step without spending money or claiming durability.

**Approval needed:** Permission H for public/free preflight; separate explicit approval required for any paid pinning, wallet, Filecoin/Arweave, or durability claim.

**Tasks under Permission H:**

1. Inventory installed local IPFS/IPLD/CAR tooling if any.
2. Decide whether local-only CAR/CID verification is enough for next step.
3. Draft a free/local add-fetch plan if tooling is already safe or user-local installable.
4. Keep Filecoin/Arweave/pinning as future paid/wallet gates.

**Artifacts:**

- `docs/public-storage-evidence-gate-plan.md`
- optional `evidence/storage-tooling-preflight-YYYY-MM-DD.md`

**Verification:**

- local command inventory;
- no paid service use;
- no public durability claim.

**Stop conditions:**

- Tooling install path is unsafe or requires root/paid account.
- Any step would imply paid pinning/wallet usage or durability guarantee.

## Loop 32 — Next controller/report consolidation

**Goal:** Consolidate loop outcomes into a concise next-roadblock report and either stop or request any remaining approvals.

**Approval needed:** Permission D if run by controller; none if done manually as local docs.

**Tasks:**

1. Update `STATUS.md`, `.hermes/context.md`, and `AGENT-LOOPS.md` with Loop 26–31 results.
2. Run full verification.
3. Commit/push if all checks pass.
4. Report:
   - completed loops;
   - evidence paths;
   - remaining gates;
   - exact next approval request if needed.

**Artifacts:**

- updated project status/context/loop docs
- final concise Telegram summary

**Verification:**

- `python3 -m unittest discover -s tests`
- `python3 scripts/preflight_static_artifact.py`
- project artifact secret-marker scan
- `git status --short --branch`
- remote sync check after push

## Recommended low-friction approval bundle

To remove the most roadblocks while preserving safety, Eric can say:

> Approve D + E + F + H for Loops 26–32. Do not approve G yet.

That lets Harry run evidence import, public update, Nostr follow-up checks, Radicle public-network preflight, and IPFS/storage preflight, while still stopping before the riskier public Radicle seed/publish/remote clone gate.

If Eric wants to remove the next major Radicle roadblock too, he can add:

> Also approve G for one disposable public Radicle seed/remote-clone smoke, no production keys, no paid infra, no durability/censorship/production claims.
