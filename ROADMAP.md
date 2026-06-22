# Roadmap

This is a research/prototype roadmap for a decentralized GitHub-class forge. It is not production software and does not currently claim live protocol interoperability, durable storage, artifact signing, Sigstore/in-toto verification, SLSA compliance, censorship-proof guarantees, or production readiness.

## Current prototype baseline

Completed local loops:

1. Source-grounded protocol research and protocol matrix.
2. Project registry schema, example fixture, and static page renderer.
3. Nostr NIP-34 repository announcement dry-run fixture.
4. Source-inspected Radicle mapping fixture; no live Radicle CLI verification yet.
5. Nostr NIP-34 collaboration dry-run fixtures for issue and patch shapes; no public relay publishing.
6. Local release artifact metadata with stdlib-verified SHA-256 and CIDv1 raw/base32-compatible identifier; no IPFS pin/fetch/gateway verification.
7. Synthetic local CI/provenance fixture; no real signing, Sigstore, Rekor, in-toto, or SLSA verification.
8. Static renderer improvements for artifact availability, content-addresses, provenance, CI checks, and substrate details.

## Near-term collaboration tracks

### 1. Renderer and UX

Make the static project page easier to read and useful as a public prototype artifact:

- clearer summary cards for repository identity, maintainers, issues, patches, releases, and CI/provenance;
- fixture/non-claim badges that distinguish local/dry-run from live-verified data;
- optional machine-readable exports for other clients.

### 2. Protocol adapters and conformance fixtures

Turn the dry-run protocol shapes into reusable adapter seams:

- Nostr NIP-34 issue/patch parser and fixture conformance checks;
- Radicle fixture adapter backed by source-pinned examples until a safe CLI install path is available;
- ForgeFed/ActivityPub object-shape research for future federation mapping.

### 3. Artifact and provenance trust model

Strengthen release metadata without overstating guarantees:

- local CID/hash consistency checks;
- synthetic provenance fixture evolution toward real, optional signing;
- explicit separation between local fixture, live-verified artifact, pinned artifact, and durable paid storage.

### 4. Public collaboration surface

Use GitHub Issues/Discussions as the temporary public coordination layer while the decentralized collaboration pieces are still fixtures:

- public issues for bounded research/prototype tasks;
- concise status updates that invite collaboration without claiming production readiness;
- no direct outreach to specific people without separate approval.

## Hard boundaries

Do not use this roadmap to justify:

- spending money or provisioning paid infrastructure;
- production/private personal keys;
- direct contact with specific people outside public project channels;
- unsupported security, privacy, compliance, SLSA, production-readiness, live-protocol, durable-storage, or censorship-proof claims.
