# Radicle local replay preflight — 2026-06-22

## Scope

Loop 22 performed read-only Radicle CLI help/version discovery only. It did not run `rad auth`, `rad init`, repository identity generation, node start, seed/publish/sync/announce, remote peer configuration, or any temporary-`RAD_HOME` replay.

## Commands run

All commands were run from `/home/openclaw/projects/decentralized-forge` with the installed user-local Radicle binary on `PATH`.

| Command | Result |
| --- | --- |
| `command -v rad` | `/home/openclaw/.local/bin/rad` |
| `rad --version` | `rad 1.9.1 (5bd3569e120a6172d9df68e1d1d0eed15e8104b1)` |
| `rad --help` | succeeded; top-level command list inspected |
| `rad init --help` | succeeded; local replay flags inspected |
| `rad inspect --help` | succeeded; inspection flags inspected |
| `rad path --help` | succeeded; help only |
| `rad auth --help` | succeeded; identity/passphrase behavior inspected, not executed |
| `rad self --help` | succeeded; identity-display help inspected, not executed |
| `rad id --help` | succeeded; repository identity management help inspected, not executed |
| `rad node --help` | succeeded; node/network command surface inspected, not executed |
| `rad status --help` | failed as expected: `rad-status` is not a known command |

## Relevant help findings

- Top-level `rad --help` lists network/stateful commands including `publish`, `sync`, `seed`, `node`, `follow`, `remote`, and `watch`. These remain out of scope for the first replay.
- `rad init --help` supports:
  - `--name <NAME>`
  - `--description <DESCRIPTION>`
  - `--default-branch <BRANCH>`
  - `--private` / `--public`
  - `--no-confirm`
  - `--no-seed` — described as "Don't seed this repository after initializing it"
- `rad inspect --help` supports local inspection by path/RID and options including `--rid`, `--identity`, `--payload`, `--refs`, `--visibility`, and `--policy`.
- `rad auth --help` indicates identity initialization may require a passphrase via prompt, `RAD_PASSPHRASE`, or `--stdin`. Loop 23 must use only disposable credentials/state and must not expose passphrases in repo evidence.
- `rad node --help` includes `start`, `connect`, `routing`, `inventory`, and other node/network operations. Loop 23 should not run `rad node start` or node networking commands.
- There is no `rad status` command in this installed version; use `rad inspect` for local repository inspection instead.

## Smallest safe Loop 23 command path

Permission A has been granted, but Loop 23 should remain bounded to disposable local state:

```sh
export PATH="$HOME/.local/bin:$PATH"
RAD_HOME=$(mktemp -d)
WORKDIR=$(mktemp -d)
REPO="$WORKDIR/repo"
mkdir -p "$REPO"
cd "$REPO"
git init
git config user.name "Decentralized Forge Disposable Replay"
git config user.email "replay@example.invalid"
printf '# disposable radicle replay\n' > README.md
git add README.md
git commit -m 'chore: disposable radicle replay fixture'

# Stateful Radicle commands, allowed only under Permission A and temporary state.
# If `rad auth` is required before init, generate a disposable passphrase outside the repo/logs,
# pipe it via stdin, and do not record the value in evidence.
# <pipe disposable passphrase from process memory here> | RAD_HOME="$RAD_HOME" rad auth --alias decentralized-forge-replay --stdin
RAD_HOME="$RAD_HOME" rad init --name decentralized-forge-disposable-replay --description "Disposable local-only Radicle replay for Decentralized Forge prototype evidence" --default-branch master --private --no-confirm --no-seed "$REPO"
RAD_HOME="$RAD_HOME" rad inspect --rid "$REPO"
RAD_HOME="$RAD_HOME" rad inspect --identity "$REPO"
RAD_HOME="$RAD_HOME" rad inspect --refs "$REPO"
RAD_HOME="$RAD_HOME" rad inspect --visibility "$REPO"
```

Notes:

- If a disposable passphrase is needed, generate it in process memory or a temp file outside the repo, pass it through stdin, and avoid logging it.
- If `rad init --private --no-seed --no-confirm` still attempts to seed, announce, sync, start a node, use non-temporary state, or prompt for persistent personal identity beyond the temporary `RAD_HOME`, abort.
- `master` is used in the candidate command because a fresh `git init` on this host currently creates `master` by default unless configured otherwise. If the disposable repo uses another branch, set `--default-branch` to the actual branch.

## Explicit non-actions

No Radicle identity/repository replay was executed in Loop 22. No `RAD_HOME` temp state was created for Radicle, no `rad auth`, no `rad init`, no node start, no seed publish, no `rad publish`, no `rad sync`, no peer announce, no remote configuration, no spending, no production/private personal keys, and no public network verification occurred.

## Next gate

Loop 23 may run the bounded temporary-`RAD_HOME` replay above under Permission A. It must capture secret-free command output, scrub any accidental sensitive values, remove temporary state after evidence capture, and preserve the distinction between **local CLI verification** and any unverified public Radicle replication/network claims.
