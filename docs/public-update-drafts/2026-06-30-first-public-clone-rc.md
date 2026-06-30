# First Public Clone Release Candidate

Draft date: 2026-06-30

`decentralized-forge` now has a first public Radicle direct-seed clone release
candidate. After the initial Docker/Linux reader proof, Loop 89 repeated the
same public clone verifier from a separate `ubuntu-work` Linux host and fresh
checkout at commit `e0f71448005b5ba8ed4a4e7ee55fa05b721ae23f`.

## What To Verify

- Retained RID: `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`
- Expected retained-RID commit: `d596024dac0d90605d4f103d567e5851771be5a8`
- Primary public seed: `z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776`
- Second public seed: `z6MksRdjzuN2VYV4HTXdVSchitJ8Bq1zbx8WhBb3KhyfSm6A@187.77.19.162:8877`

Read-only plan:

```sh
python scripts/forge_registry.py verify-first-public-clone --plan-only
```

Live verifier:

```sh
python scripts/forge_registry.py verify-first-public-clone --json
python scripts/forge_registry.py verify-first-public-clone --seed second --json
```

Machine-readable public seed status:

```sh
python scripts/forge_registry.py public-seed-status output/public-seed-status.json
python scripts/run_first_public_clone_rehearsal.py
```

## Alpha Handoff Status

This draft is release-candidate handoff text for reviewers and outside readers. No Git tag, GitHub Release, public announcement, production service, or release-signing ceremony has been created by this draft. Creating any of those remains a separate maintainer approval step after CI passes on the final pushed commit.

## Evidence

- `evidence/radicle-public-seed-update-d596024-2026-06-30.json`
- `evidence/radicle-first-public-clone-primary-d596024-2026-06-30.json`
- `evidence/radicle-first-public-clone-second-d596024-2026-06-30.json`
- `evidence/radicle-first-public-clone-outside-reader-ubuntu-work-primary-e0f7144-2026-06-30.json`
- `evidence/radicle-first-public-clone-outside-reader-ubuntu-work-second-e0f7144-2026-06-30.json`

The fresh public clone evidence was produced from Docker/Linux reader profiles
using disposable Radicle state. Both public seed addresses cloned the retained
RID and read back `d596024dac0d90605d4f103d567e5851771be5a8`.
Loop 89 then repeated the verifier from the separate `ubuntu-work` Linux host,
again using disposable reader state and no maintainer key material.

## Portable Bundle

- Bundle: `output/decentralized-forge-verification-bundle.zip`
- Bundle SHA-256: `8f064a012d5de7ed9df5773f9acedda1f4ca4bf40a607fec8bb15fc93a2f8bd8`
- Bundle size: `2316042` bytes
- Local source commit before this RC draft commit: `eacf9844ddbf34d173a3ce38640c81e755e30dce`
- Release commit: use the pushed commit that contains this draft, the Loop 79 evidence, and the regenerated bundle.
- Public seed status: `output/public-seed-status.json`

Verify the bundle:

```sh
python scripts/forge_registry.py verify-bundle output/decentralized-forge-verification-bundle.zip
python scripts/forge_registry.py verify-bundle-cleanroom output/decentralized-forge-verification-bundle.zip
python scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip
python scripts/forge_registry.py export-bundle-release-note output/decentralized-forge-verification-bundle.zip
python scripts/forge_registry.py public-seed-status output/public-seed-status.json
```

## Boundaries

This is a public direct-seed clone proof for the exact retained RID, seed
addresses, and expected commit above. It is not a production forge, not a
durability guarantee, not proof of automatic future update propagation, not
proof of default public routing, not proof of independent provider/network
availability, not a censorship-resistance claim, not an identity-trust claim,
not a security guarantee, and not a SLSA or production-readiness claim.
