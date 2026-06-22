# Loop 35 consolidation — 2026-06-22

Created UTC: `2026-06-22T22:58:02Z`

## Scope

Loop 35 consolidated the just-completed Permission-I local CAR/CID fixture verification and Permission-G disposable public Radicle smoke into the project status/context/checklist/test surface.

No new public protocol action, storage action, publish/post, gateway check, pinning, wallet use, spending, paid infrastructure, production/private personal key use, direct outreach, or new cron job was performed in this consolidation loop.

## Evidence consolidated

- Loop 33 local CAR/CID fixture evidence: `evidence/local-car-cid-fixture-2026-06-22.json`.
- Loop 33 local CAR file: `evidence/local-release-artifact-2026-06-22.car`.
- Loop 33 verification script: `scripts/verify_car_cid_fixture.mjs`.
- Loop 33 project-scoped lockfile-backed dependencies: `@ipld/car@5.4.6` and `multiformats@14.0.0` in `package-lock.json`.
- Loop 34 disposable public Radicle smoke evidence: `evidence/radicle-public-network-smoke-2026-06-22.json`.
- Loop 34 human-readable report: `evidence/radicle-public-network-smoke-2026-06-22.md`.
- Loop 34 smoke runner: `scripts/run_radicle_public_smoke.py`.

## Verified scope

- CAR/CID: local fixture bytes map to SHA-256 `3932e28d5b609b3cae25218ca205ea126cd3cf344628dc4c4b9bf094c50668a0` and CID `bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua`; the CAR root/block/readback checks passed locally.
- Radicle: one disposable public smoke for RID `rad:z2WtozFrCRhygh9CGzyUN57CN7Nwa` completed with temporary state: public init/visibility, localhost seed node start, seed policy update, sync/announce, separate temporary clone node connection, `rad clone --seed <disposable NID>`, and README readback match.

## Non-claims preserved

- No IPFS daemon, `ipfs add`, fetch, pin, public gateway query, Filecoin/Arweave wallet, paid storage, durability, global availability, censorship-resistance, security, or production-readiness claim.
- No production/private personal Radicle keys, paid infrastructure, spending, direct outreach, named external peer targeting, persistent seed operation, durability, censorship-resistance, security, global replication, identity trust, production-readiness, full Radicle compatibility, or broad Radicle network availability claim.

## Verification run before this consolidation artifact

```text
npm run verify:car-cid — passed; Local CAR/CID fixture verification passed: bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua
python3 -m unittest discover -s tests — passed; Ran 50 tests in 0.673s; OK
python3 scripts/preflight_static_artifact.py — passed; static artifact matched regenerated renderer output and unsupported claim phrases were absent
project artifact secret-marker scan — passed; excluded .git, node_modules, tests, and binary CAR artifacts
```

The controller should rerun the required verification commands after doc/checklist/test edits and before commit/push.

## Remaining gates

Further live storage, IPFS daemon/add/fetch/gateway checks, paid pinning/storage, Filecoin/Arweave wallet use, repeated or broader Radicle public-network checks, public updates about the Loop 33/34 results, or stronger durability/censorship/security/production claims require a new explicit approval/target.
