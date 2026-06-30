# First Public Clone Release Candidate

Draft date: 2026-06-30

`decentralized-forge` now has a first public Radicle direct-seed clone release
candidate.

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

## Evidence

- `evidence/radicle-public-seed-update-d596024-2026-06-30.json`
- `evidence/radicle-first-public-clone-primary-d596024-2026-06-30.json`
- `evidence/radicle-first-public-clone-second-d596024-2026-06-30.json`

The fresh public clone evidence was produced from Docker/Linux reader profiles
using disposable Radicle state. Both public seed addresses cloned the retained
RID and read back `d596024dac0d90605d4f103d567e5851771be5a8`.

## Portable Bundle

- Bundle: `output/decentralized-forge-verification-bundle.zip`
- Bundle SHA-256: `9c740f82324da14de34c01d236ea01d63550525b6ddcc0adcbd6908a54f9b3c5`
- Bundle size: `2137983` bytes
- Local source commit before this RC draft commit: `eacf9844ddbf34d173a3ce38640c81e755e30dce`
- Release commit: use the pushed commit that contains this draft, the Loop 79 evidence, and the regenerated bundle.

Verify the bundle:

```sh
python scripts/forge_registry.py verify-bundle output/decentralized-forge-verification-bundle.zip
python scripts/forge_registry.py verify-bundle-cleanroom output/decentralized-forge-verification-bundle.zip
python scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip
python scripts/forge_registry.py export-bundle-release-note output/decentralized-forge-verification-bundle.zip
```

## Boundaries

This is a public direct-seed clone proof for the exact retained RID, seed
addresses, and expected commit above. It is not a production forge, not a
durability guarantee, not proof of automatic future update propagation, not
proof of default public routing, not proof of independent provider/network
availability, not a censorship-resistance claim, not an identity-trust claim,
not a security guarantee, and not a SLSA or production-readiness claim.
