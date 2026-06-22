# Protocol Matrix

Scores: 1 = weak/immature fit, 5 = strong/mature fit. Retrieval date for protocol claims: **2026-06-22**.

## Protocol fit matrix

| Protocol / Tool | Layer fit | Maturity | UX fit | Censorship resistance | GitHub feature coverage | Current repo status | Score rationale |
|---|---|---:|---:|---:|---:|---|---|
| Git | Code/versioning | 5 | 5 | 4 | 5 | Local metadata/fixtures only | Canonical distributed version-control substrate. Excellent for code/branches/tags, but not the social forge product by itself. |
| Radicle | P2P forge backend | 4 | 4 | 5 | 4 | Source-inspected synthetic fixture; no live CLI verification | Git-native P2P forge with cryptographic identity, gossip, COB issues/patches, CLI/web/node/httpd. Best integrated substrate to replay safely. Source: https://radicle.xyz/ retrieved 2026-06-22. |
| ForgeFed / ActivityPub | Federated forge interop | 3 | 3 | 3 | 4 | Research target only | Purpose-built federation protocol for repositories, issues, patches, code review, and forge servers. Strong interop model but heavier server/federation/moderation machinery. Source: https://forgefed.org/ retrieved 2026-06-22. |
| Nostr NIP-34 | Open collaboration event layer | 3 | 3 | 4 | 4 | Dry-run repository/issue/patch fixtures; no relay publish/readback | Defines signed repository announcements, repo state, patches, PRs, issues, replies, statuses. Simple to fixture locally; relay durability/spam are risks. Source: https://github.com/nostr-protocol/nips/blob/master/34.md retrieved 2026-06-22. |
| Nostr NIP-35 | Artifact/torrent adjunct | 2 | 2 | 4 | 1 | Boundary documented; not used for forge collaboration | Defines torrent index/comment events, useful only as possible large-artifact distribution inspiration, not forge collaboration. Source: https://github.com/nostr-protocol/nips/blob/master/35.md retrieved 2026-06-22. |
| IPFS | Immutable blobs/snapshots | 4 | 3 | 4 | 2 | Local CID-compatible metadata only; no live add/fetch/pin | Good for content-addressed release artifacts, snapshots, docs, bundles. Not a storage provider and not an issue/patch layer. Source: https://docs.ipfs.tech/concepts/what-is-ipfs/ retrieved 2026-06-22. |
| IPLD | Content-addressed data model | 3 | 2 | 4 | 2 | Research target only | Useful for cross-protocol hash-linked objects and optional future registry encoding; too much for first static MVP. Source: https://ipld.io/ retrieved 2026-06-22. |
| Filecoin | Long-term storage market | 3 | 2 | 4 | 1 | Deferred; no wallet/spend | Adds incentivized storage/proofs for artifacts, but introduces payment/provider choices; later only. Source: https://docs.filecoin.io/basics/what-is-filecoin retrieved 2026-06-22. |
| Arweave | Permanent artifact storage | 3 | 2 | 4 | 1 | Deferred; no wallet/spend | Permanent-data option with HTTP APIs, but requires wallet/funding decisions; not approved for autonomous loop. Source: https://docs.arweave.org/developers/arweave-node-server/http-api retrieved 2026-06-22. |
| Sigstore/cosign | Artifact signatures | 4 | 4 | 3 | 2 | Synthetic provenance fields only; no signing/verification | Strong signing/verification for releases, binaries, containers, SBOMs; public services/OIDC assumptions need mapping to decentralized identity. Source: https://docs.sigstore.dev/ retrieved 2026-06-22. |
| in-toto/SLSA | Build provenance | 4 | 3 | 3 | 2 | Synthetic provenance fields only; no SLSA claim | Good CI/release trust primitive; SLSA is a specification for incremental supply-chain guarantees, not a forge. Sources: https://in-toto.io/ and https://slsa.dev/spec/v1.0/ retrieved 2026-06-22. |
| AT Protocol / PDS | Portable signed user data | 3 | 3 | 3 | 2 | Research/reference only | Strong reference for DIDs, signed data repositories, PDS migration, and AppViews; no forge lexicon today. Sources: https://atproto.com/guides/overview and https://atproto.com/specs/repository retrieved 2026-06-22. |
| Hypercore | Append-only P2P data | 3 | 3 | 4 | 2 | Research/reference only | Secure distributed append-only logs with signed Merkle verification and sparse replication. Promising event-log primitive but not forge-specific. Source: https://github.com/holepunchto/hypercore retrieved 2026-06-22. |
| Secure Scuttlebutt | Offline/social append-only logs | 2 | 2 | 4 | 2 | Historical/reference only | Good offline signed-feed precedent; modern git-ssb status uncertain and direct git-ssb sources were not reliable in this run. Source: https://ssbc.github.io/scuttlebutt-protocol-guide/ retrieved 2026-06-22. |

## Consolidated current decision after Loop 10

- **Canonical MVP product shape:** local project registry JSON + static rendered project page.
- **Current verified implementation:** local fixtures, local renderer, local stdlib tests, and public GitHub coordination issues.
- **Not yet verified:** live Nostr relay publishing/readback, live Radicle CLI repository replay, live ForgeFed federation, live IPFS availability/pinning, Filecoin/Arweave durability, real hosted CI, real signing, Sigstore/cosign/in-toto verification, Rekor upload, or any SLSA level.
- **First adapter target:** Nostr NIP-34 parser/conformance around existing dry-run repository/issue/patch fixtures.
- **First integrated substrate replay:** Radicle local CLI replay once an approved install/binary path exists.
- **Interop bridge target:** ForgeFed/ActivityPub object mapping after local object semantics stabilize; no public actor until moderation/security gates exist.
- **Artifact/trust target:** keep hashes/CID-compatible metadata and synthetic provenance explicit; add live storage/signing only behind separate gates.

## Next-step decision matrix

| Next step | Impact | Cost/risk | Required evidence before claiming support | Decision |
|---|---|---|---|---|
| NIP-34 parser/conformance tests | High: converts existing fixtures into reusable adapter seam | Low: local tests only | Parser round-trips repository/issue/patch fixtures; no claim of relay support | **Proceed next.** |
| Radicle safe local CLI replay | High: validates strongest integrated forge substrate | Medium: install/tooling risk | Approved binary/install path; temp `RAD_HOME`; disposable repo; captured local identity/issue/patch outputs | **Proceed when safe tooling is available.** |
| Artifact state/schema split | Medium-high: prevents CID/pinning/durability confusion | Low: schema/docs/tests | Distinct local CID, live IPFS, pinned, durable paid-storage states in schema/UI/tests | **Proceed alongside adapter work.** |
| Real provenance/signing spike | Medium: moves fake attestation toward real trust | Medium-high: key/identity/network risk | Disposable test signing, verification output, no production keys, no SLSA overclaim | **Defer until state labels are hardened.** |
| ForgeFed object mapping | Medium: preserves federation path | Medium: spec/server/moderation complexity | Source-pinned object-shape mapping and abuse-control notes | **Document first; defer live actor.** |
| Filecoin/Arweave durability | Low for current MVP; useful later for artifacts | High: spending/wallet decisions | Explicit approval, wallet/provider plan, test artifact, cost cap | **Blocked without approval.** |

## Gates before changing the recommendation

1. Promote **Nostr** from fixture to live-verified only after disposable/project-scoped key handling, relay selection, publish/readback output, and parser tests are committed.
2. Promote **Radicle** from source-inspected to live-verified only after an approved local CLI run in a temporary profile captures reproducible project identity, issue, and patch data.
3. Promote **IPFS/artifact storage** from CID-compatible metadata to live availability only after an add/fetch/gateway or node verification path is run and documented; promote to pinned/durable only after provider and cost decisions are explicit.
4. Promote **Sigstore/in-toto/SLSA** from synthetic provenance to real trust only after signing/verification commands run on disposable/test artifacts; do not claim SLSA levels unless the documented criteria are actually met.
5. Promote **ForgeFed** from mapping target to live federation only after service, actor, moderation, abuse, security, and maintenance gates are satisfied.
6. Do not add **Filecoin/Arweave** flows until spending/wallet approval exists.
