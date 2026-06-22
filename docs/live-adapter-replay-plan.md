# Live-gated adapter replay plan

Loop 20 prepares replay checklists for future Radicle and Nostr adapter verification without executing live protocol actions in this loop.

## Loop 20 discovery result

- Safe discovery command run: `command -v rad`.
- Result in this environment: no `rad` executable was found on `PATH`.
- Follow-up: `rad --version` was not run because no approved local binary path was discovered.
- Installers were not run. In particular, no curl-pipe-shell installer, package install, network node startup, seed publish, relay publish, key generation, signing, or spending occurred.

Because the Radicle CLI was unavailable during Loop 20, this plan began as a prerequisite checklist only. It did not promote any Radicle or Nostr scope to `live-verified`.

## Loop 21 prerequisite update

Eric approved installing needed tooling and generating Harry-owned Nostr keys on 2026-06-22 via Telegram. Loop 21 satisfied the tooling/key prerequisite only:

- Radicle CLI installed as user-local binaries under `~/.local/bin`; no sudo/root package install and no curl-pipe-shell execution.
- `rad --version`: `rad 1.9.1 (5bd3569e120a6172d9df68e1d1d0eed15e8104b1)`.
- `radicle-node --version`: `radicle-node 1.9.1 (5bd3569e120a6172d9df68e1d1d0eed15e8104b1)`.
- `git-remote-rad --version`: `git-remote-rad 1.9.1 (5bd3569e120a6172d9df68e1d1d0eed15e8104b1)`.
- Nostr CLI installed as `~/.local/bin/nak`.
- `nak --version`: `nak version v0.20.0`.
- Disposable/project-scoped Nostr secret key generated outside the repository at `~/.hermes/keys/decentralized-forge/nostr-project.nsec` with `0600` permissions. Do not record the secret value in repo docs, logs, fixtures, screenshots, or chat.
- Public Nostr key: `npub1ve55y0h8dkw44hyws80hj2rvy457m0j6hp8nudgy8km354807hyqp97suy` / `6669423ee76d9d5adc8e81df79286c2569edbe5ab84f3e35043db71a54eff5c8`.
- Offline signed proof event saved at `evidence/nostr-offline-key-proof-2026-06-22.json` and verified locally with `nak verify`; event ID `129cc3a22b3da01ad92eefd6cf56ebfdad64ecc657f7d373e21d6c3a8d51fe22`.
- No Radicle identity/repo replay, Radicle node start, seed publishing, Nostr relay publishing, relay readback, paid infrastructure, production/private personal keys, or live protocol verification occurred.

This update promotes prerequisites from "missing" to "installed/key-ready" only. Radicle temporary-`RAD_HOME` replay and Nostr public relay publish/readback remain separate gates with evidence requirements below.

## Loop 22 Radicle preflight update

Loop 22 completed read-only Radicle CLI help/version preflight and recorded evidence at `evidence/radicle-local-replay-preflight-2026-06-22.md`.

- `command -v rad`: `/home/openclaw/.local/bin/rad`.
- `rad --version`: `rad 1.9.1 (5bd3569e120a6172d9df68e1d1d0eed15e8104b1)`.
- Help inspected: `rad --help`, `rad init --help`, `rad inspect --help`, `rad auth --help`, `rad self --help`, `rad id --help`, `rad node --help`, and `rad path --help`.
- `rad status --help` is not available in Radicle 1.9.1; use `rad inspect` for repository inspection.
- Candidate replay surface is temporary `RAD_HOME`, disposable Git repo, disposable `rad auth` only if required, `rad init --no-confirm --no-seed --private`, and local `rad inspect` commands.
- Still not executed: `rad auth`, `rad init`, temporary-`RAD_HOME` replay, node start, publish/seed/sync/announce, peer/remote configuration, public network verification, spending, or production/private personal key use.

## Hard gates for any future replay

A future live replay must stop unless all relevant gates are satisfied and recorded in status docs:

1. Use only approved tooling paths. Do not run unsafe installers or curl-pipe-shell commands.
2. Use disposable, project-scoped state and credentials only.
3. Do not use production/private personal keys.
4. Do not spend money or provision paid infrastructure.
5. Do not publish to public Radicle seeds by default.
6. Do not sign or publish Nostr relay events until disposable-key storage, relay selection, signing, publish, readback, and verification steps are explicitly approved.
7. Do not create public CI/status events as part of adapter replay unless that is separately scoped and approved.
8. Do not claim production readiness, security guarantees, censorship resistance, durable availability, relay acceptance, Radicle replication, or live protocol verification unless command/network evidence has actually been captured.
9. Do not directly contact specific people; use public project channels only when public updates are separately in scope.
10. Keep rollback simple: delete temporary local directories, stop local processes, remove disposable keys if generated, and revert documentation if evidence does not pass promotion criteria.

## Radicle local replay prerequisites

### Preconditions

- An approved `rad` binary exists at a recorded path from `command -v rad` or another safe, reviewed package path.
- `rad --version` succeeds locally and its output is recorded.
- The replay uses a temporary `RAD_HOME`, for example `RAD_HOME=$(mktemp -d)`.
- The replay uses a disposable local Git repository created under a temporary directory.
- The replay does not use existing personal Radicle state, production identities, or long-lived secrets.
- The replay does not publish to public seeds by default. Any command that would announce, sync, seed, or publish externally must be reviewed as a separate explicit gate.

### Candidate commands for a later loop

These commands are intentionally not executed by Loop 20. A future loop should adapt them to the discovered binary and confirmed `rad` help output before running:

```sh
command -v rad
rad --version
RAD_HOME=$(mktemp -d)
WORKDIR=$(mktemp -d)
mkdir -p "$WORKDIR/repo"
cd "$WORKDIR/repo"
git init
git config user.name "Decentralized Forge Disposable Replay"
git config user.email "replay@example.invalid"
printf '# disposable replay\n' > README.md
git add README.md
git commit -m 'chore: disposable radicle replay fixture'
# Only under Permission A, after Loop 22 preflight:
# If required, generate a disposable passphrase outside the repo/logs and pipe it to this command via stdin; do not record the value.
# RAD_HOME="$RAD_HOME" rad auth --alias decentralized-forge-replay --stdin
# RAD_HOME="$RAD_HOME" rad init --name decentralized-forge-disposable-replay --description "Disposable local-only Radicle replay for Decentralized Forge prototype evidence" --default-branch master --private --no-confirm --no-seed "$WORKDIR/repo"
# RAD_HOME="$RAD_HOME" rad inspect --rid "$WORKDIR/repo"
# RAD_HOME="$RAD_HOME" rad inspect --identity "$WORKDIR/repo"
# RAD_HOME="$RAD_HOME" rad inspect --refs "$WORKDIR/repo"
# RAD_HOME="$RAD_HOME" rad inspect --visibility "$WORKDIR/repo"
```

Do not run `rad node start`, seed setup, public announce/sync/push, remote peer configuration, or identity import in the first replay unless the future loop explicitly expands scope and records why it is safe.

### Evidence to capture

- `command -v rad` path.
- `rad --version` output.
- Exact temporary `RAD_HOME` path shape, with no secret values.
- Exact disposable repository path shape and Git commit SHA.
- Exact `rad` commands run and their stdout/stderr.
- Generated local Radicle repository identifier only if the command evidence proves it was created locally and not published.
- Confirmation that no public seed publish, peer announce, production state import, or spending occurred.

### Failure and rollback

- If no approved binary exists, stop and keep Radicle state `live-unverified`.
- If help/version output is unavailable or ambiguous about local-only behavior, stop before `rad init`.
- If any command asks for production identity, networking, seed publishing, payment, or persistent state outside temporary paths, abort.
- Remove temporary `RAD_HOME` and disposable work directories after evidence capture.
- Do not update fixtures to live values unless all promotion criteria below pass.

### Promotion criteria

Radicle can move from source-inspected/live-unverified to a live local verification state only when:

- Approved CLI path and version are recorded.
- Commands ran with temporary `RAD_HOME` and disposable repo.
- Evidence shows a local Radicle repo identity or equivalent CLI output.
- Evidence shows no public seed publishing or external replication was performed.
- Tests/docs are updated to distinguish local CLI verification from public network replication.

Public replication, seed availability, censorship resistance, durability, or production readiness remain separate claims and must not be inferred from a local CLI replay.

## Nostr disposable/project-scoped publish/readback checklist

Loop 20 does not generate keys, sign events, publish to relays, or read from relays. A future Nostr replay must satisfy this checklist first.

### Preconditions

- Use a disposable/project-scoped key only.
- Record the key storage location and access policy, but never record secret key material in this repository, logs, docs, fixtures, screenshots, or status files.
- Select one or more relays with public write/read behavior suitable for prototype testing.
- Confirm relay terms, rate limits, retention expectations, and deletion limitations.
- Confirm the event payload is accurately prototype-labeled and does not contain production secrets, private keys, personal data, unsupported claims, or misleading live status.

### Candidate later flow

1. Generate or load a disposable project key in a documented local path outside the repository.
2. Build NIP-34 repository announcement/collaboration/state payloads from existing fixtures with clearly prototype-labeled content.
3. Serialize and sign events locally using reviewed tooling.
4. Compute event IDs and verify signatures locally before publishing.
5. Publish to selected relay(s) only after the relay gate is explicitly approved.
6. Read back by event ID from the same relay(s).
7. Verify readback event ID, pubkey, signature, kind, tags, content, and relay URL.
8. Record evidence without secret values: tool versions, relay URLs, event IDs, timestamps, command transcript, and verification outcome.

### Fixture-to-live transition criteria

A Nostr scope can move from dry-run/local fixture to live relay verification only when:

- Disposable/project-scoped key storage is documented without secret values.
- Event IDs are computed from signed payloads and signatures verify locally.
- At least one selected relay accepts the event and readback returns the same event ID and payload.
- The renderer/adapter clearly distinguishes live relay readback evidence from fixture-only conformance metadata.
- Docs and tests preserve boundaries: relay acceptance is not proof of durability, moderation resistance, censorship-proof behavior, production trust, or standardized public CI/status semantics.

### Rollback and non-claims

- Nostr events may be retained by relays; deletion cannot be assumed. Treat publishing as public and irreversible.
- If a publish/readback fails, keep fixture states local/dry-run and record failure without promoting verification state.
- Do not claim durable availability, global relay propagation, censorship resistance, identity trust, or production readiness from a single relay readback.

## Machine-readable checklist

The secret-free checklist in `fixtures/live-adapter-replay-checklist.json` mirrors these gates for future automation/tests. It contains no credentials, no secret key material, and no live event IDs.
