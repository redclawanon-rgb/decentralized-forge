# Radicle temporary-RAD_HOME disposable repo replay — 2026-06-22

## Scope

Loop 23 ran the approved Permission A local replay only. It used temporary `RAD_HOME`, a disposable Git repository, disposable Radicle auth state, `rad init --private --no-confirm --no-seed`, and local `rad inspect` commands. This is local CLI verification only.

No `rad node start` was run. No Radicle node was started. No public seed publishing, `rad publish`, sync, announce, peer/remote configuration, production/private personal identity import, spending, paid infrastructure, or public Radicle network verification occurred.

No secret values are recorded here.

Temporary `RAD_HOME` and work directories were removed after evidence capture.

## Tooling

| Check | Result |
| --- | --- |
| `command -v rad` | `/home/openclaw/.local/bin/rad` |
| `rad --version` | `rad 1.9.1 (5bd3569e120a6172d9df68e1d1d0eed15e8104b1)` |

## Disposable local repository

| Field | Value |
| --- | --- |
| Repository path in transcript | `<TEMP_WORKDIR>/repo` |
| `RAD_HOME` path in transcript | `<TEMP_RAD_HOME>` |
| Git branch | `master` |
| Git commit | `dfa5aad01c1bad5d2b1cda9919251b41e14ee643` |

## Command transcript

Secret values are not present in this transcript. The disposable Radicle passphrase used for `rad auth --stdin` was never written to repo docs/evidence/logs.

### `git init`

Exit code: 0

```text
Initialized empty Git repository in <TEMP_WORKDIR>/repo/.git/
```

`git init` also printed Git's default-branch hint for `master`.

### `git commit -m 'chore: disposable radicle replay fixture'`

Exit code: 0

```text
[master (root-commit) dfa5aad] chore: disposable radicle replay fixture
 1 file changed, 1 insertion(+)
 create mode 100644 README.md
```

### `rad init` before auth

Command:

```sh
RAD_HOME=<TEMP_RAD_HOME> rad init --name decentralized-forge-disposable-replay --description "Disposable local-only Radicle replay for Decentralized Forge prototype evidence" --default-branch master --private --no-confirm --no-seed <TEMP_WORKDIR>/repo
```

Exit code: 1

```text
✗ Error: Radicle profile not found in '<TEMP_RAD_HOME>'.
✗ Hint: To setup your Radicle profile, run `rad auth`.
```

Interpretation: `rad auth` was required for this temporary `RAD_HOME`; this matched the Loop 22 preflight condition for disposable auth only if required.

### `rad auth --alias decentralized-forge-replay --stdin`

Exit code: 0

```text
Initializing your Radicle 👾 identity

✓ Creating your Ed25519 keypair...
✓ Adding your Radicle key to ssh-agent...
✓ Your Radicle DID is did:key:z6MkutM4LWh4y9qdeSMTWW88pMDVJBBhnjkoGPgZq1aSYN2n. This identifies your device. Run `rad self` to show it at all times.
✓ You're all set.

To create a Radicle repository, run `rad init` from a Git repository with at least one commit.
To clone a repository, run `rad clone <rid>`. For example, `rad clone rad:z3gqcJUoA1n9HaHKufZs5FCSGazv5` clones the Radicle 'heartwood' repository.
To get a list of all commands, run `rad`.
```

Boundary: the keypair was created inside temporary disposable Radicle state. The passphrase was generated in process memory, supplied via stdin, not logged, and the temporary state was removed after evidence capture.

### `rad init` after disposable auth

Command:

```sh
RAD_HOME=<TEMP_RAD_HOME> rad init --name decentralized-forge-disposable-replay --description "Disposable local-only Radicle replay for Decentralized Forge prototype evidence" --default-branch master --private --no-confirm --no-seed <TEMP_WORKDIR>/repo
```

Exit code: 0

```text
Initializing private Radicle 👾 repository in <TEMP_WORKDIR>/repo..

✓ Repository decentralized-forge-disposable-replay created.

Your Repository ID (RID) is rad:z33oByNZxkxXAChhD54B4XiSsQkao.
You can show it any time by running `rad .` from this directory.

You have created a private repository.
This repository will only be visible to you, and to peers you explicitly allow.

To make it public, run `rad publish`.
To push changes, run `git push`.
```

Interpretation: local repository identity creation succeeded with `--private` and `--no-seed`. The output describes `rad publish` as a separate future command; it was not run.

### `rad inspect --rid <TEMP_WORKDIR>/repo`

Exit code: 0

```text
rad:z33oByNZxkxXAChhD54B4XiSsQkao
```

### `rad inspect --identity <TEMP_WORKDIR>/repo`

Exit code: 0

```json
{
  "payload": {
    "xyz.radicle.project": {
      "defaultBranch": "master",
      "description": "Disposable local-only Radicle replay for Decentralized Forge prototype evidence",
      "name": "decentralized-forge-disposable-replay"
    }
  },
  "delegates": [
    "did:key:z6MkutM4LWh4y9qdeSMTWW88pMDVJBBhnjkoGPgZq1aSYN2n"
  ],
  "threshold": 1,
  "visibility": {
    "type": "private"
  }
}
```

### `rad inspect --refs <TEMP_WORKDIR>/repo`

Exit code: 0

```text
z6MkutM4LWh4y9qdeSMTWW88pMDVJBBhnjkoGPgZq1aSYN2n
└── refs
    ├── cobs
    │   └── xyz.radicle.id
    │       └── 07584cdc3c50fcdbfd52632a48ead4c4a2abec99
    ├── heads
    │   └── master
    └── rad
        ├── id
        ├── root
        └── sigrefs
```

### `rad inspect --visibility <TEMP_WORKDIR>/repo`

Exit code: 0

```text
private
```

## Verified outcome

Loop 23 promotes Radicle from source-inspected/live-unverified to **local CLI verified for disposable private repo initialization and inspection only**.

This does **not** verify public Radicle seed publication, replication, node connectivity, global discovery, durability, censorship resistance, production readiness, or security guarantees.

## Next gate

Loop 24 is Nostr relay selection and prototype payload review. Publication/readback remains Loop 25 under Permission B and must use only the disposable project key recorded in project docs without printing or committing secret key material.
