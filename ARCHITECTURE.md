# Architecture

## Proposed architecture

```text
GitHub-like Web/Desktop UI
        ↓
Forge Aggregator API
        ↓
┌─────────────────────────────────────────────┐
│ Identity Layer                               │
│ - Nostr pubkeys / Radicle IDs / DIDs         │
│ - Maintainer role grants                     │
├─────────────────────────────────────────────┤
│ Collaboration Layer                          │
│ - Issues, comments, patches, reviews         │
│ - Nostr NIP-34/NIP-35 or Radicle COBs        │
│ - ForgeFed bridge later                      │
├─────────────────────────────────────────────┤
│ Code Layer                                   │
│ - Git repositories                           │
│ - Radicle P2P replication                    │
│ - HTTP/SSH mirrors                           │
├─────────────────────────────────────────────┤
│ Artifact Layer                               │
│ - IPFS/Filecoin/Arweave optional             │
│ - Release bundles, docs, package blobs       │
├─────────────────────────────────────────────┤
│ Trust Layer                                  │
│ - Signed commits/tags                        │
│ - Sigstore/cosign/in-toto/SLSA attestations  │
└─────────────────────────────────────────────┘
```

## Design principle

Every layer should be replaceable. The user gets a normal forge interface; the system can route underlying data to Git mirrors, Radicle nodes, Nostr relays, ActivityPub forges, and IPFS pinning services.

## Initial architecture recommendation

Use the following early sequence:

1. Local Git repo browser.
2. Project registry object.
3. Nostr NIP-34-compatible repo announcement representation.
4. Local issue/patch objects shaped to map to Nostr/Radicle/ForgeFed.
5. IPFS-compatible release artifact metadata.
6. Radicle integration spike.
7. ForgeFed bridge spike.

## Why not one protocol?

GitHub is not one feature. It is code hosting, identity, issue tracking, pull requests, releases, CI, packages, search, auth, reputation, and social discovery. No single decentralized protocol currently replaces all of that well.

The likely winning system is a productized bundle of protocols behind a simple UI.
