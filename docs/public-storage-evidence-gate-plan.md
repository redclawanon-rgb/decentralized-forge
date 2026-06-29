# Public storage/IPFS evidence gate plan

Created 2026-06-22 from Loop 31 Permission-H preflight.

## Status

**Loop 41 local Helia add/get verification is complete.** Permission H originally allowed free/read-only storage/IPFS preflight; Permission I later allowed one local CAR/CID fixture verification loop with project-scoped lockfile-backed dev dependencies. The 2026-06-28 standing approval then allowed free, project-scoped, low-volume, secret-free live IPFS/storage follow-up, which was used only for an in-process local Helia add/get check. It still did not authorize paid pinning, wallets, paid storage, Filecoin/Arweave use, public gateway checks, public durability claims, persistent daemons, or production/security claims.

Preflight evidence is in `evidence/storage-tooling-preflight-2026-06-22.md`. Loop 33 local CAR/CID evidence is in `evidence/local-car-cid-fixture-2026-06-22.json`; local CAR file is `evidence/local-release-artifact-2026-06-22.car`. Loop 41 local Helia evidence is in `evidence/helia-local-ipfs-add-get-2026-06-28.json`.

## Current verified baseline

- Loop 6 already computed a local CIDv1 raw/base32-compatible fixture for `fixtures/local-release-artifact.txt`.
- Fixture SHA-256: `3932e28d5b609b3cae25218ca205ea126cd3cf344628dc4c4b9bf094c50668a0`.
- Fixture CID-compatible value: `bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua`.
- Current fixtures explicitly keep `pinned: false`, `live_ipfs_verified: false`, `paid_storage: false`, and `durability_claim: false`.
- Loop 31 found no installed IPFS/Kubo CLI, CAR CLI, IPLD CLI, or Python multiformats/CAR libraries on this host.
- Node/npm/npx/corepack and uv are available, so a future local-only dependency-based CAR/CID smoke is feasible without root if explicitly chosen.
- Loop 33 completed the dependency-backed local CAR/CID path with `@ipld/car@5.4.6` and `multiformats@14.0.0` in `package-lock.json`; `npm run verify:car-cid` passed. The generated CAR has one root matching `bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua`, one block, and block bytes matching `fixtures/local-release-artifact.txt`.
- Loop 41 completed a project-scoped local Helia add/get path with `helia@6.1.4` and `@helia/unixfs@7.2.1`; `npm run verify:helia` passed. The local non-started offline in-memory Helia instance, configured with no libp2p listeners, transports, discovery, routers, or block brokers, added `fixtures/local-release-artifact.txt` and read back the exact bytes for CID `bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua`.

## What Loop 31 did not do

- No IPFS daemon was started.
- No `ipfs add`, `ipfs get`, `ipfs cat`, gateway fetch, pin, unpin, or provider action occurred.
- No CAR file was generated or imported.
- No package was installed or executed.
- No paid pinning/storage, Filecoin wallet, Arweave wallet, or paid infrastructure was used.
- No durability, censorship-resistance, global availability, security, or production-readiness claim was made.

## Recommended next storage evidence loop

### Loop 33 candidate: local CAR/CID fixture verification

Goal: strengthen artifact-storage evidence using only local/free tooling and exact local bytes.

Preferred path if dependency installation is approved:

1. Keep all work project-scoped; do not install global packages unless necessary.
2. Add a lockfile-backed Node dev dependency path for CAR/CID tooling, likely one of:
   - `ipfs-car` CLI for local CAR pack/list/unpack;
   - `@ipld/car` and `multiformats` for a small deterministic JS verification script.
3. Use only `fixtures/local-release-artifact.txt` or a generated test copy as input.
4. Produce evidence that local bytes map to the expected CID and, if a CAR file is created, that the CAR root and contained bytes match.
5. Update fixtures/docs/tests with a new state such as `local-car-verified`, while leaving `live_ipfs_verified`, `pinned`, `paid_storage`, and `durability_claim` false.
6. Run unit tests, static preflight, and secret-marker scan before commit/push.

Fallback path with no new dependencies:

1. Keep using Python stdlib CIDv1 raw/multihash derivation.
2. Add a small evidence artifact that records the exact derivation and byte length.
3. Strengthen tests that recompute SHA-256 and CID-compatible metadata from local bytes.
4. Continue to label this as local CID metadata only, not live IPFS availability.

### Loop 41 completed: local Helia add/get fixture verification

Goal: prove one local IPFS/UnixFS implementation can add and read back the exact fixture bytes without touching paid storage, wallets, public gateways, or persistent infrastructure.

Completed path:

1. Added project-scoped dev dependencies `helia@6.1.4` and `@helia/unixfs@7.2.1`.
2. Added `scripts/verify_helia_fixture.mjs` and npm script `verify:helia`.
3. Used only `fixtures/local-release-artifact.txt` as input.
4. Recorded exact CID, SHA-256, byte-count, dependency, and non-claim evidence in `evidence/helia-local-ipfs-add-get-2026-06-28.json`.
5. Updated `fixtures/live-evidence-index.json`, renderer output, tests, and CI.
6. Left `pinned`, `paid_storage`, `durability_claim`, and public gateway claims false.

### Later public gateway/pinning gate

A later explicit public-gateway or pinning target could allow:

1. Optionally query a small number of public gateways if approved and if terms/costs are acceptable.
2. Optionally use a free pinning service only if account/token handling and terms are reviewed.
3. Record exact CID, gateway/provider responses, timeouts, and non-claims.

Even if successful, that would prove only the exact gateway or pinning behavior at that time. It would not prove paid pinning, long-term persistence, global availability, censorship resistance, security, or production readiness.

## Future paid/wallet gates

Do not proceed without Eric's explicit approval for each relevant lane:

- paid pinning provider account/API token;
- Filecoin wallet/funding/storage deal;
- Arweave wallet/funding/upload;
- any spending or recurring infrastructure;
- any public claim that artifacts are durable, censorship-resistant, permanent, secure, or production-ready.

## Current next roadblock

The lowest-risk local CAR/CID and local Helia add/get steps are complete. Remaining storage gates are public gateway checks, pinning, paid storage, and Filecoin/Arweave wallet lanes; each requires a specific target and appropriate approval. The project must still avoid durability, censorship-resistance, global availability, security, or production-readiness claims until backed by much stronger evidence.
