# Next live-adapter loop set

Created 2026-06-22 after Eric asked Harry to create the next set of loops and identify any permissions needed before execution.

This document intentionally separates **loop creation** from **live execution**. It is safe to commit because it contains no secrets and does not publish, seed, or contact any protocol network by itself.

## Current prerequisite state

- Radicle tooling is installed user-locally:
  - `~/.local/bin/rad`
  - `~/.local/bin/radicle-node`
  - `~/.local/bin/git-remote-rad`
- Nostr tooling is installed user-locally:
  - `~/.local/bin/nak`
- A disposable/project-scoped Nostr secret key exists outside this repository at `~/.hermes/keys/decentralized-forge/nostr-project.nsec` with `0600` permissions.
- Public Nostr key only: `npub1ve55y0h8dkw44hyws80hj2rvy457m0j6hp8nudgy8km354807hyqp97suy` / `6669423ee76d9d5adc8e81df79286c2569edbe5ab84f3e35043db71a54eff5c8`.
- Offline proof event exists at `evidence/nostr-offline-key-proof-2026-06-22.json` and verifies locally.

## Permission bundles requested before autonomous execution

Eric can approve these individually or as a bundle.

### Permission A — Radicle local replay

Allow Harry to run a **temporary local Radicle replay** using:

- temporary `RAD_HOME` created via `mktemp -d`;
- disposable local Git repository under `mktemp -d`;
- local `rad` commands needed to initialize/inspect a repository identity and map outputs into evidence;
- no `rad node start` unless a later loop shows it is required and separately safe;
- no public seed publishing, peer announce, remote sync, or external replication;
- cleanup of temp directories after evidence is captured.

This permission is intended to prove only local CLI behavior, not network replication or censorship resistance.

### Permission B — Nostr public relay publish/readback

Allow Harry to publish one or more clearly prototype-labeled Nostr events using the disposable project key to one or two free public relays, then read them back by event ID.

Important: Nostr relay publication is public and may be retained by relays. Deletion cannot be assumed.

Boundaries:

- use only the disposable project key, never production/private personal keys;
- content must be prototype/research-labeled and secret-free;
- no spammy repetition;
- record relay URLs, event IDs, publish responses, readback payloads, and local verification;
- no claims of durability, global propagation, censorship resistance, identity trust, or production readiness from a single relay readback.

### Permission C — durable controller automation

Allow Harry to create a low-noise one-shot or recurring Hermes cron controller for this project that:

- runs from `/home/openclaw/projects/decentralized-forge`;
- uses the default provider unless explicitly overridden later;
- completes approved loops autonomously;
- commits and pushes only after tests/preflight/secret scans pass;
- sends concise Telegram summaries only at loop boundaries or blockers;
- never crosses unapproved gates (spending, production/private keys, direct outreach, unsupported claims, paid infra, or live protocol publishing if Permission B is not granted).

If provider auth/rate limits block a run, the controller should stop with a concise auth/rate-limit message rather than retry-spamming Telegram.

## Loop 22 — Radicle local replay preflight

**Goal:** Confirm exact safe local-only Radicle command surface before repository replay.

**Allowed without Permission A:** read local `rad --help` / manpage output and update this plan.

**Needs Permission A before execution:** running any `rad auth`, `rad init`, identity generation, repository initialization, or other stateful Radicle command.

**Artifacts:**

- `evidence/radicle-local-replay-preflight-YYYY-MM-DD.md`
- updates to `fixtures/live-adapter-replay-checklist.json`
- status/context updates

**Verification:**

- `rad --version`
- selected `rad <subcommand> --help` commands
- tests remain green
- secret-marker scan passes

## Loop 23 — Radicle temporary-`RAD_HOME` disposable repo replay

**Goal:** Run a bounded local Radicle replay with disposable state and capture command evidence.

**Requires Permission A.**

**Steps:**

1. Create temp `RAD_HOME` and temp Git repo.
2. Create a minimal disposable Git commit.
3. Run only the smallest local Radicle init/inspect commands confirmed by Loop 22.
4. Capture stdout/stderr into `evidence/` without secrets.
5. Update docs/tests to distinguish local CLI verification from public seed/network verification.
6. Cleanup temp state unless a specific evidence path needs to remain.

**Stop conditions:**

- command asks for persistent personal identity;
- command attempts to start a node, publish to seed, sync, announce, or configure remote peers;
- output includes secret material;
- local-only behavior is ambiguous.

## Loop 24 — Nostr relay selection and event payload review

**Goal:** Choose safe public relay target(s) and finalize the exact prototype payload before publication.

**Allowed without Permission B:** read relay info docs/endpoints and draft payload locally.

**Requires Permission B before publication.**

**Artifacts:**

- `docs/nostr-relay-publish-readback-plan.md`
- `evidence/nostr-relay-selection-YYYY-MM-DD.md`
- fixture/checklist updates

**Verification:**

- relay URL(s), terms/rate-limit/retention notes where discoverable;
- exact unsigned/signed event preview without secret values;
- local `nak verify` on signed event;
- tests and secret-marker scan.

## Loop 25 — Nostr disposable publish/readback

**Goal:** Publish a prototype-labeled event with the disposable project key and read it back by event ID.

**Requires Permission B.**

**Steps:**

1. Sign event locally with `nak` using the project key.
2. Verify event ID/signature locally.
3. Publish to selected relay(s).
4. Read back by event ID.
5. Verify readback event ID, pubkey, signature, kind, tags, content, and relay URL.
6. Record evidence and non-claims.

**Stop conditions:**

- relay requires payment or production credentials;
- relay rejects event for reasons that need human choice;
- payload review finds ambiguous or overclaiming content;
- secret marker scan fails.

## Loop 26 — Live evidence import into adapter/renderer

**Goal:** Import narrow live-evidence metadata into project fixtures and renderer without replacing fixture-only claims improperly.

**Inputs:** Loop 23 and/or Loop 25 evidence.

**Artifacts:**

- updated `fixtures/live-adapter-replay-checklist.json`
- optional `fixtures/live-evidence-index.json`
- renderer updates only if useful
- tests proving live/local/fixture states remain visually separate

**Verification:**

- `python3 -m unittest discover -s tests`
- `python3 scripts/preflight_static_artifact.py`
- secret-marker scan

## Loop 27 — Public project update draft

**Goal:** Draft a concise public status update for GitHub project channels explaining verified scope and next gates.

**Requires separate public-post approval unless Eric includes it in the permission bundle.**

**Allowed without public-post approval:** draft locally in `docs/public-update-drafts/`.

**Boundaries:**

- no direct outreach;
- no unsupported claims;
- no claims of censorship resistance, durability, production readiness, or full protocol compatibility.

## Automation policy

If Permission C is granted, the controller may run Loop 22 immediately and proceed through any later loops whose required permissions are also granted. If a loop hits an unapproved gate, the controller must stop and ask Eric with the exact permission needed.
