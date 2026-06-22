# Radicle public-network gate preflight — 2026-06-22

Created UTC: `2026-06-22T19:28:07Z`

## Scope

Loop 30 ran under Permission F only: read-only/help-output preflight for a later Radicle public-network gate. Permission G is explicitly not granted, so no public seed, publish, sync, node start, remote clone/fetch, peer connect, or remote configuration action was executed.

## Tooling

| Check | Result |
| --- | --- |
| `command -v rad` | `/home/openclaw/.local/bin/rad` |
| `rad --version` | `rad 1.9.1 (5bd3569e120a6172d9df68e1d1d0eed15e8104b1)` |
| `git-remote-rad --version` | `git-remote-rad 1.9.1 (5bd3569e120a6172d9df68e1d1d0eed15e8104b1)` |

## Help surfaces inspected

All commands below were inspected with `--help` only.

| Command | Preflight finding |
| --- | --- |
| `rad publish --help` | Publishing a private repository makes it public and discoverable on the network. It can publish the current repository or an explicit RID and is limited to single-delegate repositories where the delegate is the authenticated user. |
| `rad seed --help` | With an RID, creates/updates a seeding policy; `--scope` can be `all` or `followed`; default behavior can fetch after policy update unless `--no-fetch` is used. |
| `rad sync --help` | Default synchronization fetches from connected seeds and announces local refs to peers. `--fetch`, `--announce`, `--seed`, replica counts, timeout, inventory mode, and signed-ref feature levels are available. |
| `rad sync status --help` | Displays sync status for a repository; help-only inspection did not query a repository. |
| `rad node --help` | Node control/query surface includes `connect`, `config`, `events`, `routing`, `start`, `logs`, `status`, `inventory`, `debug`, and `stop`. |
| `rad node start --help` | Starts the node, optionally foreground/verbose/path plus node options. Not run. |
| `rad node status --help` | Queries node status. Not run in Loop 30 because it may depend on local node state and is unnecessary for help-only preflight. |
| `rad node connect --help` | Connects to a peer by `NID[@ADDR]` with optional timeout. Not run. |
| `rad remote --help` | Repository remote management surface includes `add`, `rm`, and `list`. |
| `rad remote add --help` | Adds a Git remote for a DID/NID; default behavior may fetch and sync unless `--no-fetch --no-sync` are supplied. Not run. |
| `rad remote list --help` | Lists stored remotes. Not run. |
| `rad clone --help` | Clones through the local node routing table or explicit `--seed`; supports timeout, scope, signed-ref feature level, and bare clone. Not run. |
| `rad fetch --help` | `rad-fetch` is not a known Radicle command in this CLI; clone/sync/remote surfaces are the relevant fetch paths. |
| `rad unseed --help` | Removes seeding policy for RIDs. Not run. |
| `rad follow --help` | Without a NID it can list followed nodes; with a NID it updates follow policy. Help-only inspection only. |

## Draft Permission G command shape — not executed

A later public Radicle smoke should be separate and disposable. The exact runnable script must be reviewed immediately before execution, but the safe shape is:

1. Create a temporary `RAD_HOME` and disposable Git repository with a single harmless commit.
2. Run `rad auth --stdin` only inside that temporary `RAD_HOME` with a generated disposable passphrase that is never logged.
3. Run `rad init --name <prototype-name> --description <prototype-label> --default-branch master --public --no-confirm --no-seed <repo>` or, if public init semantics are ambiguous, first run the proven `--private --no-seed` path and then explicitly gate `rad publish`.
4. Start a node only after Permission G and only with explicit logging/cleanup paths.
5. Publish/seed/sync only the disposable prototype RID, capture RID/NID/command results, then perform one bounded remote clone/fetch/readback from separate temporary state if the node/seed evidence is clear.
6. Stop the node and remove temporary state after evidence capture.

## Permission G hard stop

Before any future execution, Eric must explicitly approve Permission G for one disposable public Radicle seed/remote-clone smoke. Without that approval, these remain forbidden:

- `rad node start`
- `rad publish`
- `rad seed <RID>`
- `rad sync` / announce / inventory
- `rad node connect`
- `rad remote add` / remote sync/fetch
- `rad clone` / remote clone/fetch
- production or private personal identity import
- paid infrastructure
- durability, censorship-resistance, security, global availability, or production-readiness claims

## Risks identified

- `rad publish` makes a repository public and discoverable on the network.
- `rad seed` changes seeding policy and may fetch unless guarded with `--no-fetch` where appropriate.
- `rad sync` defaults to both fetching and announcing local refs.
- `rad remote add` defaults may fetch and sync unless disabled.
- `rad clone` uses the local node routing table unless explicit seed behavior is selected.
- Node start/connect/routing surfaces can cross from local CLI evidence into public network behavior.
- Any public Radicle proof would still be only a bounded disposable smoke, not a durability, censorship-resistance, global replication, identity-trust, security, or production-readiness proof.

## Non-actions

No temporary `RAD_HOME` was created. No Radicle identity was created or reused. No node was started. No repository was published, seeded, synced, announced, cloned, fetched, connected, followed, or remotely configured. No spending, paid infrastructure, production/private personal keys, direct outreach, or unsupported claims occurred.
