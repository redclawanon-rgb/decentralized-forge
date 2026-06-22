# Protocol Matrix

Scores: 1 = weak/immature fit, 5 = strong/mature fit. Retrieval date for protocol claims: **2026-06-22**.

| Protocol / Tool | Layer fit | Maturity | UX fit | Censorship resistance | GitHub feature coverage | Score rationale |
|---|---|---:|---:|---:|---:|---|
| Git | Code/versioning | 5 | 5 | 4 | 5 | Canonical distributed version-control substrate. Excellent for code/branches/tags, but not the social forge product by itself. |
| Radicle | P2P forge backend | 4 | 4 | 5 | 4 | Git-native P2P forge with cryptographic identity, gossip, COB issues/patches, CLI/web/node/httpd. Best integrated substrate to spike. Source: https://radicle.xyz/ retrieved 2026-06-22. |
| ForgeFed / ActivityPub | Federated forge interop | 3 | 3 | 3 | 4 | Purpose-built federation protocol for repositories, issues, patches, code review, and forge servers. Strong interop model but heavier server/federation machinery. Source: https://forgefed.org/ retrieved 2026-06-22. |
| Nostr NIP-34 | Open collaboration event layer | 3 | 3 | 4 | 4 | Defines signed repository announcements, repo state, patches, PRs, issues, replies, statuses. Simple to fixture locally; relay durability/spam are risks. Source: https://github.com/nostr-protocol/nips/blob/master/34.md retrieved 2026-06-22. |
| Nostr NIP-35 | Artifact/torrent adjunct | 2 | 2 | 4 | 1 | Defines torrent index/comment events, useful only as possible large-artifact distribution inspiration, not forge collaboration. Source: https://github.com/nostr-protocol/nips/blob/master/35.md retrieved 2026-06-22. |
| IPFS | Immutable blobs/snapshots | 4 | 3 | 4 | 2 | Good for content-addressed release artifacts, snapshots, docs, bundles. Not a storage provider and not an issue/patch layer. Source: https://docs.ipfs.tech/concepts/what-is-ipfs/ retrieved 2026-06-22. |
| IPLD | Content-addressed data model | 3 | 2 | 4 | 2 | Useful for cross-protocol hash-linked objects and optional future registry encoding; too much for first static MVP. Source: https://ipld.io/ retrieved 2026-06-22. |
| Filecoin | Long-term storage market | 3 | 2 | 4 | 1 | Adds incentivized storage/proofs for artifacts, but introduces payment/provider choices; later only. Source: https://docs.filecoin.io/basics/what-is-filecoin retrieved 2026-06-22. |
| Arweave | Permanent artifact storage | 3 | 2 | 4 | 1 | Permanent-data option with HTTP APIs, but requires wallet/funding decisions; not approved for autonomous loop. Source: https://docs.arweave.org/developers/arweave-node-server/http-api retrieved 2026-06-22. |
| Sigstore/cosign | Artifact signatures | 4 | 4 | 3 | 2 | Strong signing/verification for releases, binaries, containers, SBOMs; public services/OIDC assumptions need mapping to decentralized identity. Source: https://docs.sigstore.dev/ retrieved 2026-06-22. |
| in-toto/SLSA | Build provenance | 4 | 3 | 3 | 2 | Good CI/release trust primitive; SLSA is a specification for incremental supply-chain guarantees, not a forge. Sources: https://in-toto.io/ and https://slsa.dev/spec/v1.0/ retrieved 2026-06-22. |
| AT Protocol / PDS | Portable signed user data | 3 | 3 | 3 | 2 | Strong reference for DIDs, signed data repositories, PDS migration, and AppViews; no forge lexicon today. Sources: https://atproto.com/guides/overview and https://atproto.com/specs/repository retrieved 2026-06-22. |
| Hypercore | Append-only P2P data | 3 | 3 | 4 | 2 | Secure distributed append-only logs with signed Merkle verification and sparse replication. Promising event-log primitive but not forge-specific. Source: https://github.com/holepunchto/hypercore retrieved 2026-06-22. |
| Secure Scuttlebutt | Offline/social append-only logs | 2 | 2 | 4 | 2 | Good offline signed-feed precedent; modern git-ssb status uncertain and direct git-ssb sources were not reliable in this run. Source: https://ssbc.github.io/scuttlebutt-protocol-guide/ retrieved 2026-06-22. |

## Current decision

- **MVP product shape:** local project registry JSON + static rendered project page.
- **First event target:** Nostr NIP-34-compatible repository announcement fixture.
- **First integrated substrate spike:** Radicle local installation/API/object mapping.
- **Interop bridge target:** ForgeFed/ActivityPub after local object semantics stabilize.
- **Artifact/trust target:** hashes now, optional IPFS CIDs and Sigstore/in-toto/SLSA attestations later.

## Gates before changing the recommendation

1. If Radicle local install/API mapping proves straightforward, consider Radicle as primary backend.
2. If NIP-34 tooling can round-trip local events cleanly without public relay dependency, keep Nostr as public discovery/collaboration event layer.
3. If Forgejo federation is production-ready enough, prioritize ForgeFed bridge earlier.
4. Do not add Filecoin/Arweave flows until spending/wallet approval exists.
