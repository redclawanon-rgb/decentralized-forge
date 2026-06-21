# Research

Research notes for a decentralized GitHub-class forge.

## Method

Use source-grounded research. Prefer official docs, specs, repositories, and current project pages. Record URLs, dates, commit SHAs where source repositories are inspected, and distinguish facts from recommendations.

## Protocols to evaluate

### Radicle

Questions:

- How are identities represented?
- How is Git replication performed?
- How are issues, patches, comments, and reviews stored?
- What does the web UI/API expose?
- Can this be used as a backend substrate for a GitHub-like UX?

### ForgeFed / ActivityPub

Questions:

- What repository/issue/patch objects are defined?
- What is implemented today by Forgejo or reference implementations?
- Is it suitable for cross-forge interoperability?

### Nostr NIP-34 / NIP-35

Questions:

- What event kinds/tags exist for repository announcements, state, issues, patches, PRs, replies, and statuses?
- What tools already implement it?
- How much can be done without a custom relay?

### IPFS / IPLD / Filecoin / Arweave

Questions:

- What belongs in content-addressed storage?
- How do we handle pinning/availability?
- Are Git repos better stored as bundles, snapshots, release artifacts, or IPLD object graphs?

### Sigstore / cosign / in-toto / SLSA

Questions:

- How can CI/build results be signed without GitHub Actions as the trust anchor?
- What is the minimal release verification stack?

### AT Protocol / PDS

Questions:

- Can user-owned repositories/records inspire portable forge identity/data?
- Is it useful now, or too social-app-specific for this use case?

### Hypercore / Secure Scuttlebutt

Questions:

- Are append-only logs useful for offline-first forge events?
- Is the ecosystem active enough to justify MVP dependency?

## Initial observed facts from first pass

- Radicle positions itself as a sovereign P2P code forge built on Git, with Git-native storage, cryptographic identity, P2P replication, issues, patches, CLI/web/node/httpd components.
- ForgeFed is an ActivityPub extension for software forges and code collaboration tools, including repository hosting, issue trackers, and code review. Forgejo is listed as implementing federation.
- Nostr NIP-34 defines Git-related collaboration events: repository announcements, repository state, patches, pull requests, issues, replies/comments, and statuses. Tools such as `n34` exist for NIP-34 workflows.
- IPFS is a strong fit for immutable snapshots/artifacts, but by itself does not provide GitHub-like collaboration semantics.
- Sigstore/cosign/in-toto/SLSA are strong fits for signed releases and CI/build provenance.

## Recommendation draft

Start with a hybrid:

1. Git as code layer.
2. Nostr or Radicle as initial collaboration/event layer.
3. IPFS-light for release artifacts/snapshots.
4. ForgeFed as an interoperability bridge rather than day-one core.
5. Sigstore/in-toto/SLSA as the trust model for CI/release artifacts.
