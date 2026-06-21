# Decentralized Forge Project Context

## Mission

Build a GitHub-class decentralized forge that feels accessible to normal developers while avoiding dependence on any single platform, host, account provider, or censorship chokepoint.

## Eric's intent

Eric wants more than a Nostr experiment. He wants serious research into combining the best available decentralized protocols to recreate GitHub-like functionality in a fully decentralized or censorship-resistant way.

## Operating principles from Eric's X bookmark signal

Recent bookmarks point to these execution patterns:

1. **Scope before build** — turn the big idea into bounded loops and artifacts.
2. **Canonical project brain** — keep markdown docs as the durable source of truth.
3. **Loop engineering** — define repeatable agent loops; do not babysit each step.
4. **Subagents/background threads** — use independent agents for research/build/review work.
5. **Verification stack** — assume agent summaries can be wrong; verify with source links, tests, files, and git state.
6. **Search → Extract → Interact** — search broad, extract known sources, use browser/interactive fallback only when needed.
7. **Harness over prompts** — create the system that runs loops, not one giant prompt.

## Current product thesis

The winning design is likely a protocol-aggregating decentralized forge:

- Git remains the canonical code object model.
- Decentralized/federated protocols handle identity, discovery, issues, PRs, reviews, releases, and replication.
- Multiple substrates are supported behind a normal GitHub-like UX.

## Candidate protocol layers

- Code/versioning: Git
- P2P repo replication: Radicle, libp2p-like approaches
- Federation: ForgeFed / ActivityPub
- Open event layer: Nostr NIP-34/NIP-35
- Durable immutable blobs: IPFS/IPLD/Filecoin/Arweave
- Build/release trust: Sigstore, cosign, in-toto, SLSA
- Optional user data portability: AT Protocol / PDS
- Offline append-only inspiration: Hypercore, Secure Scuttlebutt

## Hard boundaries / gates

Allowed without Eric approval:

- Local files/docs/specs/prototypes in this repo
- Read-only web/X/API research
- Local code prototypes
- Local tests
- Local git commits

Requires Eric approval:

- Posting publicly
- Creating public accounts/projects
- Publishing to Nostr/X/GitHub/Codeberg/etc.
- Spending money or provisioning paid infrastructure
- Using private keys beyond local prototype keys
- Making public claims/security guarantees

## Current next recommended loop

**Loop 1: Research corpus and protocol matrix**

Create pinned-source research notes for Radicle, ForgeFed, Nostr NIP-34/NIP-35, IPFS/IPLD, Sigstore/in-toto/SLSA, AT Protocol, Hypercore, and SSB. Produce a protocol matrix and first architecture recommendation.
