# CI/provenance model, hosted local checks, and fake local attestation fixture

Loop 7 adds a local-only model for CI check status and release provenance so future renderers/protocol adapters can display build trust metadata without depending on paid CI, production secrets, real Sigstore, cosign, in-toto, or SLSA infrastructure.

After Milestone 1 completion, the repository also has GitHub Actions CI at `.github/workflows/ci.yml`. That workflow runs the local verification suite, checks that generated artifacts stay current, and on `main` push uses GitHub OIDC with `actions/attest@v4` to generate keyless provenance attestations for the generated HTML/summary artifacts plus the local CAR/CID fixture artifacts.

The workflow-level attestation is real hosted keyless provenance evidence for the named subject files in GitHub Actions. The registry fixture `ci_checks[]`, fake attestation string, and structured `provenance` object remain synthetic local fixture data until a later loop imports the hosted attestation result back into registry fields with a concrete run URL and verification evidence.

## Registry fields

`fixtures/example-project.registry.json` now includes:

- `ci_checks[]` — synthetic check-run/status records with:
  - `provider: "local-fake"`
  - repository and commit coordinates
  - lifecycle fields (`status`, `conclusion`, timestamps)
  - explicit `synthetic: true` and `published: false` flags
- `releases[].artifacts[].attestation` — still a plain string, now carrying a fake local attestation summary that names the artifact SHA-256, synthetic commit, repository, and `no-slsa-claim=true`.
- `releases[].artifacts[].provenance` — structured local metadata for renderer/protocol mapping:
  - artifact name and SHA-256
  - repository, synthetic commit, and release tag
  - material digest references
  - referenced synthetic CI check IDs
  - verification flags proving this is local schema data only
  - boundaries such as `no-real-signature`, `no-private-key`, and `no-slsa-level-claim`
- `substrates.sigstore_slsa` — explicit non-claim flags for Sigstore/cosign/in-toto/SLSA status.
- Top-level `verification_states[]` — compact scope labels for renderer/docs consumers. Current CI/provenance rows are `synthetic-fixture` or `live-unverified` with `live_verified: false`; they do not upgrade fake attestations into real supply-chain evidence.

The JSON Schema allows these optional fields while retaining the older artifact `signature` and `attestation` string fields for compatibility.

## Current fake fixture

The concrete Loop 7 provenance fixture is attached to `local-release-artifact.txt` in `fixtures/example-project.registry.json`.

Key coordinates:

- Artifact SHA-256: `3932e28d5b609b3cae25218ca205ea126cd3cf344628dc4c4b9bf094c50668a0`
- Synthetic commit: `1111111111111111111111111111111111111111`
- Repository URI: `file:///home/openclaw/projects/decentralized-forge`
- CI checks: `local-fake-ci-001`, `local-fake-ci-002`
- Predicate type URI: `https://example.invalid/decentralized-forge/fake-slsa-provenance/v0`

The predicate URI is intentionally under `example.invalid` and describes a fake fixture shape, not a real SLSA predicate or compliance claim.

## Boundaries

Loop 7 and the local registry fixture do **not** perform or claim any of the following:

- CI secrets, CI tokens, deployment keys, or production/private signing keys
- DSSE envelope generation or verification
- in-toto statement generation or verification
- SLSA level, SLSA compliance, supply-chain security guarantee, or production readiness
- paid CI minutes, paid storage, wallets, or public infrastructure provisioning

Loop 40 allowed claim after the updated CI workflow passes on `main`: GitHub Actions generated keyless artifact attestations for the named subject files using GitHub OIDC and GitHub's artifact attestation service. This is hosted workflow evidence, not yet imported into the local registry provenance fixture as a replacement for the synthetic fields.

Concrete Loop 40 evidence is recorded in `evidence/github-keyless-attestation-2026-06-28.json` from GitHub Actions run https://github.com/redclawanon-rgb/decentralized-forge/actions/runs/28339280081.

Still not allowed claim: the registry fixture itself is signed, the project is production supply-chain secure, consumers have verified the attestations, a custom in-toto policy was enforced, paid/private infrastructure was used, or a production readiness guarantee exists.

Loop 16 allowed claim: `verification_states[]` consistently labels CI/provenance scopes as synthetic or live-unverified until real hosted CI/signing/verifier evidence exists.

Not allowed claim for local registry fields until a later import loop: the artifact's registry provenance object is SLSA-compliant, Sigstore-verified, in-toto-verified, backed by an imported verified provenance attestation, secured by production keys, or suitable for production supply-chain trust.

## Validation

`tests/test_registry_fixture.py` validates that:

- CI checks are synthetic, local, unpublished, and in sensible lifecycle states.
- The fake attestation/provenance references the same artifact hash, commit, repository, release tag, and CI check IDs.
- No real signature, private key, Sigstore/cosign/in-toto verification, Rekor upload, or SLSA level claim is represented.

Run:

```sh
python3 -m json.tool schemas/project-registry.schema.json >/dev/null
python3 -m json.tool fixtures/example-project.registry.json >/dev/null
python3 -m unittest discover -s tests
```
