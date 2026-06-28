# Roadmap

This is a research/prototype roadmap for a decentralized GitHub-class forge. It is not production software and does not claim durable storage, artifact signing, Sigstore/in-toto verification, SLSA compliance, censorship-proof guarantees, security guarantees, broad network availability, or production readiness.

## Current prototype baseline

Completed baseline:

1. Local registry schema, example fixtures, stdlib static renderer, generated demo artifact, preflight, and unit tests.
2. Nostr NIP-34 dry-run repository/issue/patch/state fixtures plus parser/conformance checks.
3. One imported selected-relay Nostr repository-announcement readback event from Loop 25, kept separate from dry-run fixtures.
4. Radicle source-inspected mapping, disposable local/private replay evidence, and one bounded disposable public seed/remote-clone smoke.
5. Local release artifact SHA-256/CID metadata plus lockfile-backed local CAR/CID readback evidence.
6. Synthetic CI/provenance fields for schema/UI modeling only; no real signing, Sigstore, Rekor, in-toto, or SLSA verification.
7. Public GitHub issues/discussions used as temporary coordination scaffolding while decentralized collaboration remains prototype-scoped.
8. Loop 35 consolidation of the current evidence set and remaining gates.

## Verification-state labels

Use these labels consistently in public docs, UI, and issues:

| Label | Meaning | Examples in this repo |
|---|---|---|
| `local fixture` | Data exists in repository files and local tests can inspect it. | Registry JSON, issue/patch summaries, local artifact bytes. |
| `dry-run protocol shape` | A protocol-shaped object is represented but not signed/published/read back. | NIP-34 repository/issue/patch fixtures. |
| `source-inspected mapping` | Mapping is based on official docs/source but not live tool execution. | Radicle mapping from `/tmp/radicle-heartwood`. |
| `synthetic provenance` | Trust/CI fields are fake local records for schema/UI tests. | `local-fake` CI checks and fake attestation fields. |
| `live-verified` | A command/network/tool interaction actually ran and evidence is documented. | Narrow Nostr selected-relay readback import, Radicle local/private replay, and exact disposable public Radicle smoke. |
| `durable/pinned` | A storage provider or persistence mechanism is selected and verified. | Not currently claimed. |

## Near-term collaboration tracks

### 1. Renderer and UX

Make the static project page easier to read and useful as a public prototype artifact:

- clearer summary cards for repository identity, maintainers, issues, patches, releases, and CI/provenance;
- fixture/non-claim badges that distinguish local/dry-run/source-inspected/synthetic data from live-verified data;
- optional machine-readable exports for other clients.

### 2. Protocol adapters and conformance fixtures

Turn the dry-run protocol shapes into reusable adapter seams:

- Nostr NIP-34 repository/issue/patch parser and fixture conformance checks;
- Radicle fixture adapter backed by source-pinned examples and the narrow Loop 23/34 evidence;
- ForgeFed/ActivityPub object-shape research for future federation mapping.

### 3. Artifact and provenance trust model

Strengthen release metadata without overstating guarantees:

- local CID/hash consistency checks;
- explicit states for local CID-compatible metadata, live IPFS availability, pinned provider availability, and durable paid storage;
- synthetic provenance fixture evolution toward real, optional signing only after key/network boundaries are explicit.

### 4. Public collaboration surface

Use GitHub Issues/Discussions as the temporary public coordination layer while the decentralized collaboration pieces are still fixtures:

- public issues for bounded research/prototype tasks;
- concise status updates that invite collaboration without claiming production readiness;
- no direct outreach to specific people without separate approval.

## Next implementation decision matrix

| Candidate | User-visible value | Why now / why not | Gate to start | Gate to claim done |
|---|---|---|---|---|
| Live IPFS add/fetch/gateway check | Shows whether the local CID can be retrieved from public IPFS paths | Useful next storage evidence, but requires explicit approval and must not imply durability | New explicit live-storage target; no paid pinning/wallet/spend | Evidence records exact commands, gateway/daemon behavior, failures, and non-claims. |
| Broader Radicle public-network check | Tests whether the Loop 34 smoke generalizes beyond one disposable localhost-seeded run | Higher risk of overclaiming and network noise | New explicit target for repeated/broader public Radicle testing | Bounded evidence across declared attempts; no durability/censorship/security/production claim. |
| Public update about Loops 33-34 | Lets collaborators know what was actually verified | Useful only if concise, accurate, and prototype-labeled | Explicit public-update target | Posted or drafted update cites exact evidence and non-claims. |
| Optional real signing/provenance spike | Starts replacing fake attestations with verifiable trust evidence | Useful, but key/identity/SLSA overclaim risk is higher | Disposable test keys or documented keyless test flow | Signing and verification commands pass on test artifact; no production keys or unsupported SLSA claim. |
| ForgeFed object-shape mapping | Keeps cross-forge federation path open | Live actor is too heavy before moderation/security design | Source-pinned spec/examples | Mapping doc exists; no live federation claim. |

Recommended order after Loop 35: get an explicit target for one lane, then prefer **live IPFS add/fetch/gateway check** or **prototype-labeled public update** before broader Radicle network testing. Keep paid storage, wallets, production/private keys, direct outreach, and stronger durability/censorship/security/production claims gated.

## Hard boundaries

Do not use this roadmap to justify:

- spending money or provisioning paid infrastructure;
- production/private personal keys;
- direct contact with specific people outside public project channels;
- unsupported security, privacy, compliance, SLSA, production-readiness, live-protocol, durable-storage, or censorship-proof claims.
