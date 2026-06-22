# Public storage/IPFS evidence gate plan

Created 2026-06-22 from Loop 31 Permission-H preflight.

## Status

**Planning/preflight only.** Permission H allowed free/read-only storage/IPFS preflight, but did not authorize paid pinning, wallets, paid storage, Filecoin/Arweave use, public durability claims, or live storage claims.

Evidence for this preflight is in `evidence/storage-tooling-preflight-2026-06-22.md`.

## Current verified baseline

- Loop 6 already computed a local CIDv1 raw/base32-compatible fixture for `fixtures/local-release-artifact.txt`.
- Fixture SHA-256: `3932e28d5b609b3cae25218ca205ea126cd3cf344628dc4c4b9bf094c50668a0`.
- Fixture CID-compatible value: `bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua`.
- Current fixtures explicitly keep `pinned: false`, `live_ipfs_verified: false`, `paid_storage: false`, and `durability_claim: false`.
- Loop 31 found no installed IPFS/Kubo CLI, CAR CLI, IPLD CLI, or Python multiformats/CAR libraries on this host.
- Node/npm/npx/corepack and uv are available, so a future local-only dependency-based CAR/CID smoke is feasible without root if explicitly chosen.

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

### Later live IPFS add/fetch gate

A later explicit live-storage approval could allow:

1. Install/use a local IPFS implementation through a reviewed user-local path.
2. Run a disposable local add/fetch smoke against the fixture.
3. Optionally query a small number of public gateways if approved and if terms/costs are acceptable.
4. Record exact CID, command outputs, timeouts, and non-claims.

Even if successful, that would prove only the exact add/fetch/gateway behavior at that time. It would not prove paid pinning, long-term persistence, global availability, censorship resistance, security, or production readiness.

## Future paid/wallet gates

Do not proceed without Eric's explicit approval for each relevant lane:

- paid pinning provider account/API token;
- Filecoin wallet/funding/storage deal;
- Arweave wallet/funding/upload;
- any spending or recurring infrastructure;
- any public claim that artifacts are durable, censorship-resistant, permanent, secure, or production-ready.

## Current next roadblock

The lowest-risk next step is a **local CAR/CID fixture verification loop**. It needs approval to add project-scoped dev dependencies if we choose the dependency-backed path. Otherwise, the no-new-dependency fallback can improve documentation/tests but will not advance beyond local CID-compatible metadata.
