# Release artifact metadata and local CID fixture

Loop 6 adds a local/free release-artifact metadata shape to the project registry. The goal is to let a registry carry content-addressed artifact identifiers without requiring IPFS, paid pinning, wallets, Filecoin, Arweave, or live storage infrastructure.

## Registry fields

Release artifacts may include:

- `sha256` and `hashes.sha256` — hex SHA-256 digest of the artifact bytes.
- `media_type` and `size_bytes` — descriptive local metadata.
- `uri` — local fixture URI in this repo for the demo artifact.
- `content_addresses[]` — optional content-addressed identifiers. Loop 6 models IPFS-compatible CIDv1/base32 metadata with:
  - `protocol: "ipfs"`
  - `cid_version: 1`
  - `multibase: "base32"`
  - `multicodec: "raw"`
  - `multihash: "sha2-256"`
  - `verification_status`
- `availability` — explicit non-claim flags for pinning, live IPFS verification, paid storage, and durability.

## Local fixture

`fixtures/local-release-artifact.txt` is the only concrete artifact bytes added in Loop 6. Its registry entry is in `fixtures/example-project.registry.json`.

The fixture CID is computed locally as CIDv1 using raw multicodec plus a SHA-256 multihash of the local file bytes. Tests recompute both the digest and CID shape using only the Python standard library.

Current local fixture values:

- SHA-256: `3932e28d5b609b3cae25218ca205ea126cd3cf344628dc4c4b9bf094c50668a0`
- CID-compatible value: `bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua`

## Boundaries

Loop 6 does **not** claim that the artifact is pinned, retrievable from IPFS, durably stored, production ready, or available from any gateway.

No live IPFS add/fetch/pin was performed. No paid storage, wallet, Filecoin spend, Arweave spend, production/private key, or public infrastructure was used.

Allowed claim: the fixture carries a CIDv1/base32-compatible content address computed from local bytes and verified by local stdlib tests.

Not allowed claim: the artifact is pinned, durable, censorship-proof, replicated, gateway-reachable, Filecoin-backed, Arweave-backed, or production-secure.
