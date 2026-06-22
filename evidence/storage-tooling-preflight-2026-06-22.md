# Public storage/IPFS tooling preflight — 2026-06-22

Created UTC: `2026-06-22T21:17:48Z`

## Scope

Loop 31 ran under Permission H only: public/free/read-only preflight for artifact storage/IPFS options. This was an inventory and planning loop only.

No IPFS add/fetch/pin, gateway fetch, daemon start, paid pinning, Filecoin/Arweave wallet use, paid storage, spending, production/private key use, or durability/censorship-resistance/production-readiness claim occurred.

## Installed tooling inventory

| Check | Result |
| --- | --- |
| `command -v ipfs` | missing |
| `command -v kubo` | missing |
| `command -v ipfs-car` | missing |
| `command -v car` | missing |
| `command -v ipld` | missing |
| `command -v cid` | missing |
| `command -v ipget` | missing |
| `command -v ipfs-dag` | missing |
| `command -v ipfs-cluster-service` | missing |
| `command -v ipfs-cluster-ctl` | missing |
| `command -v go-ipfs` | missing |
| Python module `multiformats` | missing |
| Python module `ipfshttpclient` | missing |
| Python module `car` | missing |
| Python module `dag_cbor` | missing |
| Python module `cbor2` | missing |

## Local/free runtime inventory

| Check | Result |
| --- | --- |
| `node --version` | `v22.22.2` |
| `npm --version` | `10.9.7` |
| `npx --version` | `10.9.7` |
| `corepack --version` | `0.34.6` |
| `go` | missing |
| `rustc` / `cargo` | missing |
| `python3 --version` | `Python 3.13.5` |
| `uv --version` | `uv 0.11.16 (x86_64-unknown-linux-gnu)` |

## Read-only package metadata checked

The following checks used `npm view` only. No package was installed or executed.

| Package | Version | License | Notes |
| --- | --- | --- | --- |
| `ipfs-car` | `3.1.0` | `Apache-2.0 OR MIT` | Provides an `ipfs-car` CLI according to npm metadata. Candidate for a later local CAR pack/unpack smoke. |
| `@ipld/car` | `5.4.6` | `Apache-2.0 OR MIT` | Library candidate for CAR parsing/writing in tests or scripts. |
| `multiformats` | `14.0.0` | `Apache-2.0 OR MIT` | Library candidate for CID/multihash verification. |
| `helia` | `6.1.4` | `Apache-2.0 OR MIT` | JS IPFS implementation candidate, but a live add/fetch smoke would be a separate gate. |
| `kubo-rpc-client` | `7.1.0` | `Apache-2.0 OR MIT` | RPC client only; requires an IPFS/Kubo node and is not enough by itself. |

## Current conclusion

The current host has no installed IPFS daemon/CLI, CAR CLI, IPLD CLI, or Python multiformats/CAR libraries. The repository already has a stdlib-computed CIDv1 raw/base32-compatible fixture from Loop 6, but no live IPFS availability has been verified.

For the next storage step, local-only CAR/CID verification is enough to improve artifact evidence without crossing paid storage or durability boundaries. It would prove only that the local artifact bytes can be packed into or checked against a content-addressed artifact representation; it would not prove pinning, gateway retrieval, public network availability, persistence, censorship resistance, Filecoin storage, Arweave permanence, or production readiness.

## Candidate next safe step — not executed in Loop 31

A later local-only storage evidence loop can choose one of these paths:

1. **Preferred if installing JS dev tooling is acceptable:** add project-scoped dev dependencies such as `ipfs-car`, `@ipld/car`, and/or `multiformats` with a lockfile, then run a local CAR pack/list/unpack or CID verification smoke against `fixtures/local-release-artifact.txt`.
2. **No new dependency fallback:** keep using the current Python stdlib CIDv1 raw/multihash fixture and add stronger tests/documentation around the exact bytes and CID derivation.
3. **Later live IPFS add/fetch gate:** only after explicit approval, install or use a local IPFS implementation, run a disposable local add/fetch, and record exact command evidence. If public gateway checks are included, they remain availability checks only, not durability guarantees.

## Future approval gates

Separate explicit approval is still required for:

- paid pinning;
- paid storage providers;
- Filecoin wallet/funding/storage deals;
- Arweave wallet/funding/uploads;
- public durability, censorship-resistance, security, or production-readiness claims.

## Non-actions

No package install was performed. No daemon was started. No IPFS add/fetch/pin, CAR pack/unpack, public gateway query, Filecoin/Arweave wallet action, paid storage, spending, production/private key use, direct outreach, or unsupported claim occurred.
