# Architecture

## Proposed architecture

```text
GitHub-like Web/Desktop UI
        ↓
Forge Aggregator API / Static Renderer
        ↓
┌─────────────────────────────────────────────┐
│ Project Registry Layer                       │
│ - Signed JSON-compatible registry object     │
│ - Maintainers, clone URLs, releases          │
│ - Substrate hints and protocol mappings      │
├─────────────────────────────────────────────┤
│ Identity Layer                               │
│ - Nostr pubkeys / Radicle IDs / DIDs / SSH   │
│ - Maintainer role grants                     │
├─────────────────────────────────────────────┤
│ Collaboration Layer                          │
│ - Issues, comments, patches, reviews         │
│ - Local JSON first                           │
│ - Nostr NIP-34/Radicle COB/ForgeFed mapping  │
├─────────────────────────────────────────────┤
│ Code Layer                                   │
│ - Git repositories                           │
│ - Local clone/mirrors                        │
│ - Radicle P2P replication later              │
│ - HTTP/SSH mirrors where available           │
├─────────────────────────────────────────────┤
│ Artifact Layer                               │
│ - Release bundles, docs, SBOMs               │
│ - SHA-256 hashes now                         │
│ - IPFS/Filecoin/Arweave optional later       │
├─────────────────────────────────────────────┤
│ Trust Layer                                  │
│ - Signed commits/tags                        │
│ - Signature placeholders in MVP              │
│ - Sigstore/cosign/in-toto/SLSA attestations  │
└─────────────────────────────────────────────┘
```

## Design principle

Every layer should be replaceable. The user gets a normal forge interface; the system can route underlying data to Git mirrors, Radicle nodes, Nostr relays, ActivityPub forges, and content-addressed artifact stores.

## Recommended architecture after Loop 1 research

### Phase 1: local deterministic product skeleton

Build a local-only project registry, fixture, renderer, and tests. This makes the product shape concrete without choosing a permanent network substrate too early.

- Registry: `schemas/project-registry.schema.json`
- Example data: `fixtures/example-project.registry.json`
- Renderer: `scripts/render_project_page.py`
- Output: `output/demo-project.html`
- Tests: stdlib `unittest`

### Phase 2: event-shape compatibility

Map the registry to Nostr NIP-34 repository announcement shapes and document how issues/patches/statuses would map. Keep this as a dry run: no relay publication, no private keys.

### Phase 3: Radicle integration spike

Install/use Radicle locally, create/import a sample repo, and inspect how Radicle IDs, COB issues, patches, and HTTP daemon data map to the registry object.

### Phase 4: ForgeFed bridge spike

After local objects are stable, map registry/issues/patches to ForgeFed/ActivityPub actors, inbox/outbox flows, and repository/issue/patch vocabulary. Avoid running a public actor until moderation and security gates exist.

### Phase 5: release trust and artifact storage

Add release artifact hashes, then optional IPFS CIDs, then Sigstore/cosign/in-toto/SLSA attestations. Filecoin/Arweave are later and require explicit approval because they imply payment/wallet decisions.

## Recommended MVP object model

### Project registry

The canonical MVP object. Contains:

- Schema/version metadata.
- Project id, name, description, default branch.
- Maintainers with identity type and public id.
- Clone URLs and web URLs.
- Issue and patch summary lists for static rendering.
- Release metadata including hashes and optional content-addressed URIs.
- Substrate hints for NIP-34, Radicle, ForgeFed, IPFS, and Sigstore/SLSA.
- Signature block placeholder.

### Issues

MVP issues can be embedded summaries in the registry fixture. Later they should become separate signed objects/events with fields that map to:

- Nostr NIP-34 issue events and replies.
- Radicle COB issues.
- ForgeFed issue objects.

### Patches / PRs

MVP patches can be embedded summaries. Later they should support:

- Inline `git format-patch` for small NIP-34-compatible patches.
- Branch/remote references for larger PR-like proposals.
- Status events/checks.
- Maintainer review decisions.

### Releases

MVP releases include version, tag, artifact names, SHA-256 hashes, signature placeholders, attestation placeholders, and optional CID/URI. Real signing comes after local rendering and fixture validation.

## Open decision points

1. **Primary collaboration substrate:** Nostr NIP-34 first, Radicle first, or dual-target local objects?
   - Current recommendation: local object model + NIP-34 fixture first; Radicle hands-on spike next.
2. **Identity canonicalization:** Should project authority be a Nostr pubkey, Radicle ID, DID, SSH signing key, or multi-key policy?
   - Current recommendation: registry supports multiple identifier types; do not force one yet.
3. **Issue/patch storage:** Embedded in registry for demos, separate signed objects for real use, or backend-specific objects?
   - Current recommendation: embedded summaries for static demo, separate objects after renderer proof.
4. **Relay/federation persistence:** Which relays/instances/pinning services become availability providers?
   - Current recommendation: none in MVP; use local fixtures only.
5. **Release signing model:** Traditional maintainer keys, Sigstore keyless, or both?
   - Current recommendation: model both; implement no production signing in autonomous loop.
6. **Moderation and abuse control:** How does a project reject spam issues/patches across public protocols?
   - Current recommendation: client-side/project-maintainer curation list in registry before public publishing.

## Why not one protocol?

GitHub is not one feature. It is code hosting, identity, issue tracking, pull requests, releases, CI, packages, search, auth, reputation, and social discovery. No single decentralized protocol currently replaces all of that well.

The likely winning system is a productized bundle of protocols behind a simple UI, with a small canonical registry object tying them together.
