# Protocol Matrix

Scores: 1 = weak/immature fit, 5 = strong/mature fit.

| Protocol / Tool | Layer fit | Maturity | UX fit | Censorship resistance | GitHub feature coverage | Notes |
|---|---|---:|---:|---:|---:|---|
| Git | Code/versioning | 5 | 5 | 4 | 5 | Canonical code object model. Already decentralized, but social/product layer is centralized on GitHub. |
| Radicle | P2P forge backend | TBD | TBD | TBD | TBD | Promising existing sovereign forge. Needs deeper hands-on test. |
| ForgeFed / ActivityPub | Federated forge interop | TBD | TBD | TBD | TBD | Best fit for cross-instance forge federation. Needs implementation status check. |
| Nostr NIP-34/NIP-35 | Open collaboration event layer | TBD | TBD | TBD | TBD | Strong for signed lightweight events; relay persistence/spam are risks. |
| IPFS/IPLD | Immutable blobs/snapshots | TBD | TBD | TBD | TBD | Good for artifacts/snapshots; not enough for full collaboration layer. |
| Filecoin/Arweave | Long-term storage | TBD | TBD | TBD | TBD | Useful for paid permanence; likely later. |
| Sigstore/cosign | Artifact signatures | TBD | TBD | TBD | TBD | Strong supply-chain fit. Needs decentralized transparency-log strategy review. |
| in-toto/SLSA | Build provenance | TBD | TBD | TBD | TBD | Good CI trust primitive. Not a forge by itself. |
| AT Protocol / PDS | Portable user data | TBD | TBD | TBD | TBD | Interesting identity/data portability model; not forge-specific. |
| Hypercore | Append-only P2P data | TBD | TBD | TBD | TBD | Interesting offline-first primitive. Need ecosystem check. |
| Secure Scuttlebutt | Offline/social append-only logs | TBD | TBD | TBD | TBD | Historically relevant for git-ssb; likely inspiration not core. |

## Current leaning

- **Most practical base:** Git + Radicle or Nostr.
- **Most practical interop bridge:** ForgeFed.
- **Most practical artifact layer:** IPFS plus signed hashes.
- **Most practical trust layer:** signed Git tags + Sigstore/cosign/in-toto/SLSA.
