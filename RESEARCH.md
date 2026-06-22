# Research

Research notes for a decentralized GitHub-class forge.

Retrieval date for all cited protocol/source claims in this revision: **2026-06-22**.

## Method

Use source-grounded research. Prefer official docs, specs, repositories, and current project pages. Record URLs, dates, commit SHAs where source repositories are inspected, and distinguish facts from recommendations.

## Executive recommendation

Use a hybrid, spec-first architecture rather than betting the MVP on one protocol:

1. **Git remains the code layer.** It is already decentralized, content-addressed by object IDs, and familiar.
2. **Project registry is the product/control-plane object.** A small signed JSON-compatible object should list project identity, maintainers, clone URLs, web URLs, issue/patch endpoints, releases, and substrate hints.
3. **Nostr NIP-34 is the first public-event shape to model.** It is simple, signed, relay-addressable, and has explicit repository/issue/patch event kinds.
4. **Radicle is the strongest integrated forge substrate to spike next.** It already combines Git, P2P replication, identities, issues, and patches.
5. **ForgeFed is an interoperability bridge, not the day-one core.** It is the best-aligned cross-forge federation vocabulary, but the MVP can model its objects locally before running an ActivityPub service.
6. **IPFS/IPLD are artifact/snapshot layers, not the collaboration layer.** Use CIDs in release metadata and registry fields; defer pinning/payment.
7. **Sigstore/cosign/in-toto/SLSA define release trust.** Start with hashes and signature placeholders, then add real attestations after the local registry works.
8. **AT Protocol, Hypercore, and SSB are design references or later integrations.** They are valuable models for portable signed repos and append-only/offline logs, but they add ecosystem risk for the first MVP.

## Radicle

### Observed facts

- Radicle describes itself as a sovereign code forge built on Git and as an open-source peer-to-peer code collaboration stack. Source: https://radicle.xyz/ retrieved 2026-06-22.
- Radicle stores social artifacts in Git and signs them with public-key cryptography; the site says Radicle verifies authenticity and authorship. Source: https://radicle.xyz/ retrieved 2026-06-22.
- Radicle uses cryptographic identities, Git for data transfer, and a custom gossip protocol for repository metadata. Source: https://radicle.xyz/ retrieved 2026-06-22.
- Radicle names Collaborative Objects (COBs) as the primitive for issues, discussions, code review, and custom collaboration workflows, implemented as Git objects. Source: https://radicle.xyz/ retrieved 2026-06-22.
- The Radicle stack includes CLI, web interface, TUI, Radicle Node, and HTTP daemon components. Source: https://radicle.xyz/ retrieved 2026-06-22.

### Fit for this forge

Radicle is the closest existing system to the desired product: Git-native, local-first, cryptographically identified, and already modeling issues/patches. It could become either a primary backend or a bridge-backed import/export target.

### Risks / gaps

- Product control: using Radicle as the primary substrate may inherit its identity/workflow constraints.
- Integration effort: the MVP still needs a GitHub-like UX, registry object, static/demo rendering, and possibly a separate event layer for non-Radicle users.
- Hands-on verification remains required: install, create a local test repo, inspect exported objects/API, and map issues/patches.

## ForgeFed / ActivityPub

### Observed facts

- ForgeFed is a federation protocol for software forges and code collaboration tools, covering repository hosting websites, issue trackers, code review applications, and more. Source: https://forgefed.org/ retrieved 2026-06-22.
- ForgeFed is an ActivityPub extension. It defines vocabulary terms related to repositories, commits, patches, issues, and protocols for interacting with those objects across servers. Source: https://forgefed.org/ retrieved 2026-06-22.
- ForgeFed describes repository and issue-tracker inboxes through which objects can be remotely and safely interacted with. Source: https://forgefed.org/ retrieved 2026-06-22.
- ForgeFed lists Vervis as a reference implementation, Forgejo as implementing federation, and an unmaintained Pagure plugin. Source: https://forgefed.org/ retrieved 2026-06-22.
- The ForgeFed repository states it is an ActivityPub-based federation protocol for forge services and that specification source lives under `spec/`. Source: https://github.com/forgefed/forgefed retrieved 2026-06-22.

### Fit for this forge

ForgeFed is the best cross-forge interoperability layer: it matches repository/issue/patch vocabulary and account-on-different-server workflows. It should inform local object schemas and later federation adapters.

### Risks / gaps

- Requires running web services, actors, inboxes/outboxes, HTTP signatures/ActivityPub machinery, moderation, and abuse controls.
- MVP should not block on live ActivityPub federation.
- Current implementation status should be verified directly against Forgejo/Vervis before choosing it as a core runtime.

## Nostr NIP-34 / NIP-35

### Observed facts

- NIP-34 is marked draft/optional and defines Git-related code collaboration using Nostr. Source: https://github.com/nostr-protocol/nips/blob/master/34.md retrieved 2026-06-22.
- NIP-34 includes repository announcements (`kind: 30617`) whose tags can include `d`, `name`, `description`, `web`, `clone`, `relays`, `r` with marker `euc`, `maintainers`, and topic tags. Source: https://github.com/nostr-protocol/nips/blob/master/34.md retrieved 2026-06-22.
- NIP-34 includes repository state announcements (`kind: 30618`) for branch/tag refs and HEAD. Source: https://github.com/nostr-protocol/nips/blob/master/34.md retrieved 2026-06-22.
- NIP-34 includes patches (`kind: 1617`) containing `git format-patch` output, and recommends PRs when individual patch events exceed roughly 60KB. Source: https://github.com/nostr-protocol/nips/blob/master/34.md retrieved 2026-06-22.
- NIP-34 has issue/reply/status event shapes for forge collaboration around repositories. Source: https://github.com/nostr-protocol/nips/blob/master/34.md retrieved 2026-06-22.
- NIP-35 is draft/optional and defines torrent indexing/comment events (`kind: 2003`, `kind: 2004`), not Git collaboration. Source: https://github.com/nostr-protocol/nips/blob/master/35.md retrieved 2026-06-22.

### Fit for this forge

NIP-34 is a strong first event-shape target because it can represent repository announcement/discovery, clone URLs, relays to monitor, patches, issues, comments, and statuses without the MVP running a custom server. NIP-35 is less central but can inspire content distribution for large release artifacts via magnet/torrent metadata.

### Risks / gaps

- Relays do not guarantee durable storage; project data needs local cache/export and maybe pinned relays.
- Abuse/spam/moderation is externalized to clients and relay policies.
- Event schemas are draft/optional, so compatibility can shift.
- Patch payload size limits mean large PRs need Git branch/remote references, not just inline events.

## IPFS / IPLD / Filecoin / Arweave

### Observed facts

- IPFS is a set of open protocols for addressing, routing, and transferring data using content addressing and peer-to-peer networking. Source: https://docs.ipfs.tech/concepts/what-is-ipfs/ retrieved 2026-06-22.
- IPFS documentation explicitly says IPFS is not a storage provider or cloud provider; pinning/storage availability must be handled separately. Source: https://docs.ipfs.tech/concepts/what-is-ipfs/ retrieved 2026-06-22.
- IPLD is described as the data model of the content-addressable web and a way to treat hash-linked data structures as a unified information space. Source: https://ipld.io/ retrieved 2026-06-22.
- Filecoin is a peer-to-peer network for reliable decentralized file storage with economic incentives and cryptographic proofs; clients pay storage providers and providers prove storage. Source: https://docs.filecoin.io/basics/what-is-filecoin retrieved 2026-06-22.
- Arweave exposes HTTP node/gateway APIs and can upload data through transactions, but using it in production implies wallet/funding decisions. Source: https://docs.arweave.org/developers/arweave-node-server/http-api retrieved 2026-06-22.

### Fit for this forge

Use content-addressed artifact metadata early: release tarballs, bundles, docs snapshots, SBOMs, and provenance files can include hashes and optional CIDs/transaction IDs. Defer paid durability until a user explicitly approves spending.

### Risks / gaps

- IPFS alone does not provide issue/patch semantics or guaranteed persistence.
- Filecoin/Arweave introduce cost, wallet, and operational complexity.
- Storing live Git object graphs in IPLD is interesting but unnecessary for the local MVP; Git bundles/snapshots are simpler.

## Sigstore / cosign / in-toto / SLSA

### Observed facts

- Sigstore is an open-source project for improving software supply-chain security and helps sign/verify release files, container images, binaries, SBOMs, and more. Source: https://docs.sigstore.dev/ retrieved 2026-06-22.
- Sigstore uses ephemeral/keyless signing, identity binding through Fulcio, and a transparency log through Rekor. Source: https://docs.sigstore.dev/ retrieved 2026-06-22.
- in-toto is a framework to secure software supply-chain integrity from initiation to end-user installation by making steps, actors, and order transparent. Source: https://in-toto.io/ retrieved 2026-06-22.
- SLSA is a specification for describing and incrementally improving supply-chain security with levels and recommended attestation formats including provenance. Source: https://slsa.dev/spec/v1.0/ retrieved 2026-06-22.

### Fit for this forge

This stack should define how releases and builds become trustworthy without GitHub Actions as the sole authority. The MVP can start with hashes and signature/attestation placeholders, then add cosign/in-toto/SLSA attestations when there is a local build pipeline.

### Risks / gaps

- Public Sigstore relies on public-good services and OIDC identity flows; decentralized forge identity may not map cleanly at first.
- Full SLSA conformance is out of scope for MVP.
- Keyless signing needs network and identity provider assumptions; offline/local mode may need traditional keys.

## AT Protocol / PDS

### Observed facts

- AT Protocol describes itself as a decentralized protocol for large-scale social web applications. Source: https://atproto.com/guides/overview retrieved 2026-06-22.
- AT Protocol users have permanent DIDs and configurable domain handles. Source: https://atproto.com/guides/overview retrieved 2026-06-22.
- AT Protocol exchanges signed data repositories containing records; the overview compares them to Git repos for database records. Source: https://atproto.com/guides/overview retrieved 2026-06-22.
- AT Protocol has a federated architecture with Personal Data Servers (PDS), Relays, and App Views, and supports account migration without the original server's involvement. Source: https://atproto.com/guides/overview retrieved 2026-06-22.
- The repository spec says each account has a public, verifiable, self-certifying repository represented as a content-addressed Merkle-tree structure with signed commits; blobs are referenced by content hash and not stored directly in the repo. Source: https://atproto.com/specs/repository retrieved 2026-06-22.

### Fit for this forge

AT Protocol is a strong reference for portable signed account data and indexed app views. A forge could define lexicons for repository/issue/patch records, but this would be a significant protocol/product bet.

### Risks / gaps

- Current ecosystem is social-app centered, not forge centered.
- It is federated around PDS/AppView infrastructure rather than simple P2P Git collaboration.
- Custom lexicons and indexing would be required.

## Hypercore

### Observed facts

- Hypercore describes itself as a secure, distributed append-only log for sharing large datasets and realtime data streams. Source: https://github.com/holepunchto/hypercore retrieved 2026-06-22.
- Hypercore supports sparse replication, realtime updates, flat-file storage, signed Merkle-tree verification, and modular stream distribution. Source: https://github.com/holepunchto/hypercore retrieved 2026-06-22.
- Holepunch/Pear positions its stack as a peer-to-peer runtime for zero-infrastructure apps across mobile, desktop, and terminal. Source: https://docs.holepunch.to/building-blocks/hypercore retrieved 2026-06-22.

### Fit for this forge

Hypercore is a plausible append-only event log substrate for issues, patches, and project feeds, especially for local-first/offline-first sync.

### Risks / gaps

- It would require designing a forge schema and bridge tooling from scratch.
- Ecosystem is less directly forge-specific than Radicle/NIP-34/ForgeFed.
- Node/JS dependency and runtime choices may conflict with the desire for a small stdlib MVP.

## Secure Scuttlebutt / git-ssb

### Observed facts

- Scuttlebutt is a protocol for decentralized apps that work offline, have no central server, and connect peers directly to exchange data. Source: https://ssbc.github.io/scuttlebutt-protocol-guide/ retrieved 2026-06-22.
- Scuttlebutt identities are Ed25519 key pairs; identities have feeds, and public keys/feed IDs identify authors. Source: https://ssbc.github.io/scuttlebutt-protocol-guide/ retrieved 2026-06-22.
- Scuttlebutt supports peer discovery, authenticated secure connections, replication, blob exchange, social follow graphs, private messaging, pubs, and rooms. Source: https://ssbc.github.io/scuttlebutt-protocol-guide/ retrieved 2026-06-22.
- A direct git-ssb web source was not reliably retrievable in this run; preserve it as historical inspiration rather than an active MVP dependency until repository/tooling status is verified. Attempted sources: https://git.scuttlebot.io/%25n92DiQh9S4%2B4Lv7I2P9Z3S1F1Sw%2Bv3W4rZp89I08sFk%3D.sha256 and https://git-ssb.celehner.com/%25n92DiQh9S4%2B4Lv7I2P9Z3S1F1Sw%2Bv3W4rZp89I08sFk%3D.sha256 retrieved/attempted 2026-06-22.

### Fit for this forge

SSB is useful as a design precedent for offline-first signed feeds and social replication, especially for issue/comment/event feeds. It should not be a day-one dependency unless modern git-ssb maintenance is confirmed.

### Risks / gaps

- Ecosystem age/maintenance uncertainty.
- Onboarding and discovery through pubs/invites are product-heavy.
- Mapping GitHub-class repository workflows would require substantial custom design.

## Open research tasks for next hands-on loops

1. Install Radicle locally and map project identity, issue, patch, and HTTP API data to the registry schema.
2. Validate NIP-34 event shapes with local fixture generation only; do not publish to relays.
3. Inspect Forgejo federation status and object shapes for ForgeFed compatibility.
4. Add release metadata fixture with hashes, optional CID, and signature/attestation placeholders.
5. Decide whether MVP issue/patch objects are stored first as local JSON fixtures, Nostr-like events, or Radicle COB imports.
