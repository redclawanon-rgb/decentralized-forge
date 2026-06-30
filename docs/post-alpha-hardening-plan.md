# Post-Alpha Hardening Plan

This plan starts after the v0.1.0-alpha candidate path is usable: a reader can find the public Radicle direct-seed clone path, verify the retained RID commit, inspect the bundle, see public seed status, and inspect an alpha collaboration path.

## Target Outcome

The next public-ready step is stronger outside-reader and release evidence without changing the claim boundary:

```text
post-alpha hardening is useful when:
1. outside-reader clone evidence exists from a separate Linux host,
2. seed status points at the latest outside-reader evidence,
3. release handoff text names the exact candidate commit and bundle digest,
4. decentralized collaboration has either fresh selected-relay evidence or a clear live replay gate,
5. signing/provenance and durable storage gaps are explicit next gates,
6. CI remains green on main.
```

This does not require a Git tag, GitHub Release, public announcement, paid storage, wallets, production/private personal keys, permanent durability, censorship resistance, security guarantees, SLSA compliance, or production readiness.

## Autonomous Loop Sequence

### Loop 89: Outside Reader Evidence Import

**Goal:** Replace the plan-only outside-reader fallback with actual separate-host clone proof.

**Current result:** `ubuntu-work` ran `verify-first-public-clone` from a fresh checkout at commit `e0f71448005b5ba8ed4a4e7ee55fa05b721ae23f` against both public seed addresses. Both read back `d596024dac0d90605d4f103d567e5851771be5a8`.

**Verification:** evidence index validation, public seed status regeneration, bundle verification, CI.

### Loop 90: Latest Seed Status Surface

**Goal:** Make status/report/release-note output prefer the latest passing outside-reader evidence per seed.

**Verification:** `output/public-seed-status.json` names the Loop 89 evidence rows and keeps uptime, durability, automatic repair, security, and production-readiness non-claims.

### Loop 91: Release Decision Package

**Goal:** Prepare an exact tag/GitHub Release decision packet without creating the tag or release.

**Verification:** release draft includes candidate commit, bundle digest, outside-reader evidence, CI URL, non-claims, and stop conditions.

### Loop 92: Collaboration Live Refresh Gate

**Goal:** Decide whether to refresh selected-relay Nostr issue/patch evidence or keep the unsigned local draft path as the alpha collaboration boundary.

**Verification:** new live evidence is secret-free and selected-relay bounded, or the blocker is documented with exact commands.

### Loop 93: Signing And Provenance Hardening Gate

**Goal:** Move from synthetic/keyless-attestation evidence toward a clearer release provenance story.

**Verification:** no production/private personal keys; no SLSA/security claim unless separately proven.

### Loop 94: Durable Storage Gate Plan

**Goal:** Prepare the IPFS/pinning/durable-storage decision without spending or using paid services.

**Verification:** free local/gateway checks only unless separate approval records cost, key, wallet, and durability boundaries.

## Stop Conditions

- Stop before creating Git tags, GitHub Releases, or public announcements.
- Stop before spending, paid services, wallets, production/private personal keys, direct outreach, or persistent new background services.
- Stop before claiming durability, censorship resistance, broad availability, security, SLSA compliance, or production readiness.
