# Roadmap

This is a research/prototype roadmap for a decentralized GitHub-class forge. It is not production software and does not currently claim live protocol interoperability, durable storage, artifact signing, Sigstore/in-toto verification, SLSA compliance, censorship-proof guarantees, or production readiness.

## Current prototype baseline

Completed loops:

1. Source-grounded protocol research and protocol matrix.
2. Project registry schema, example fixture, and static page renderer.
3. Nostr NIP-34 repository announcement dry-run fixture.
4. Source-inspected Radicle mapping fixture; no live Radicle CLI verification yet.
5. Nostr NIP-34 collaboration dry-run fixtures for issue and patch shapes; no public relay publishing.
6. Local release artifact metadata with stdlib-verified SHA-256 and CIDv1 raw/base32-compatible identifier; no IPFS pin/fetch/gateway verification.
7. Synthetic local CI/provenance fixture; no real signing, Sigstore, Rekor, in-toto, or SLSA verification.
8. Static renderer improvements for artifact availability, content-addresses, provenance, CI checks, and substrate details.
9. Public GitHub collaboration surface with bounded issues/discussions as temporary coordination scaffolding.
10. Architecture/protocol matrix/roadmap cleanup to make fixture-vs-live verification boundaries explicit.

## Verification-state labels

Use these labels consistently in public docs, UI, and issues:

| Label | Meaning | Examples in this repo |
|---|---|---|
| `local fixture` | Data exists in repository files and local tests can inspect it. | Registry JSON, issue/patch summaries, local artifact bytes. |
| `dry-run protocol shape` | A protocol-shaped object is represented but not signed/published/read back. | NIP-34 repository/issue/patch fixtures. |
| `source-inspected mapping` | Mapping is based on official docs/source but not live tool execution. | Radicle mapping from `/tmp/radicle-heartwood`. |
| `synthetic provenance` | Trust/CI fields are fake local records for schema/UI tests. | `local-fake` CI checks and fake attestation fields. |
| `live-verified` | A command/network/tool interaction actually ran and evidence is documented. | Not currently claimed for Nostr, Radicle, IPFS, ForgeFed, Sigstore, in-toto, or SLSA. |
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
- Radicle fixture adapter backed by source-pinned examples until a safe CLI install path is available;
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
| NIP-34 parser/conformance adapter | Makes decentralized issue/patch fixtures importable/exportable in a repeatable way | Builds directly on existing fixtures with low infrastructure risk | Existing fixture JSON and tests pass | Round-trip parser tests pass; docs still state no relay verification unless actually performed. |
| Radicle safe local replay | Validates the strongest integrated decentralized forge substrate | High value, but blocked on safe tool availability | Approved binary/install path, temporary `RAD_HOME`, disposable repo plan | Captured local `rad` outputs for identity/issues/patches; no public seed publish unless separately approved. |
| Artifact state model hardening | Prevents users from confusing a CID with availability/durability | Low-risk schema/UI/test cleanup | Current artifact tests pass | Schema/UI/tests distinguish local, live IPFS, pinned, and durable states. |
| Optional real signing/provenance spike | Starts replacing fake attestations with verifiable trust evidence | Useful, but key/identity/SLSA overclaim risk is higher | Disposable test keys or documented keyless test flow | Signing and verification commands pass on test artifact; no production keys or unsupported SLSA claim. |
| ForgeFed object-shape mapping | Keeps cross-forge federation path open | Live actor is too heavy before moderation/security design | Source-pinned spec/examples | Mapping doc exists; no live federation claim. |

Recommended order: **NIP-34 parser/conformance → artifact state hardening → Radicle safe local replay when tooling is available → optional real signing spike → ForgeFed mapping/live federation later.**

## Hard boundaries

Do not use this roadmap to justify:

- spending money or provisioning paid infrastructure;
- production/private personal keys;
- direct contact with specific people outside public project channels;
- unsupported security, privacy, compliance, SLSA, production-readiness, live-protocol, durable-storage, or censorship-proof claims.
