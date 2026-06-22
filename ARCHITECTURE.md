# Architecture

## Current architecture status after Loop 10

This repository is currently a **local registry/static renderer prototype plus protocol-mapping fixture set**. It is not a live decentralized forge runtime yet.

| Area | Current implementation | Live-verified protocol support? | Boundary |
|---|---|---:|---|
| Project identity/control plane | JSON registry schema and fixtures | No | Structured local object only; signature block remains a placeholder. |
| Web/UI | Stdlib static HTML renderer and generated demo page | No | Local rendering only; no hosted forge service. |
| Git/code | Local clone URL metadata and fixture repository coordinates | Local only | Git remains the code substrate, but no decentralized code replication is verified by this repo. |
| Nostr/NIP-34 | Repository announcement, issue, and patch dry-run fixtures | No | No relay publish/readback, no real keys, no valid event signatures. |
| Radicle | Source-inspected mapping and synthetic Radicle-backed registry fixture | No | `rad` CLI was not installed/run; fake RID/DIDs only. |
| ForgeFed/ActivityPub | Architecture/research target | No | No actor, inbox/outbox, server, federation, or moderation system. |
| Artifact storage | Local artifact bytes with stdlib-verified SHA-256 and CIDv1 raw/base32-compatible value | No | No IPFS add/fetch/pin/gateway check; no Filecoin/Arweave spend or durability claim. |
| CI/provenance/trust | Synthetic local CI/provenance fields and renderer display | No | No hosted CI, signing, Sigstore/cosign/in-toto verification, Rekor upload, or SLSA claim. |
| Public collaboration | GitHub repo/issues/discussions as temporary coordination surface | GitHub only | Decentralized issue/patch collaboration remains fixture-backed. |

## Proposed architecture

```text
GitHub-like Web/Desktop UI
        ↓
Forge Aggregator API / Static Renderer
        ↓
┌─────────────────────────────────────────────┐
│ Project Registry Layer                       │
│ - JSON-compatible registry object            │
│ - Maintainers, clone URLs, releases          │
│ - Substrate hints and protocol mappings      │
│ - Signature policy placeholder               │
├─────────────────────────────────────────────┤
│ Identity Layer                               │
│ - Nostr pubkeys / Radicle IDs / DIDs / SSH   │
│ - Maintainer role grants                     │
│ - Multi-key authority policy later           │
├─────────────────────────────────────────────┤
│ Collaboration Layer                          │
│ - Issues, comments, patches, reviews         │
│ - Local JSON fixtures now                    │
│ - NIP-34/Radicle/ForgeFed adapters later     │
├─────────────────────────────────────────────┤
│ Code Layer                                   │
│ - Git repositories                           │
│ - Local clone/mirrors now                    │
│ - Radicle P2P replication after verification │
│ - HTTP/SSH mirrors where available           │
├─────────────────────────────────────────────┤
│ Artifact Layer                               │
│ - Release bundles, docs, SBOMs               │
│ - SHA-256 + local CID-compatible metadata now│
│ - IPFS/Filecoin/Arweave optional later       │
├─────────────────────────────────────────────┤
│ Trust Layer                                  │
│ - Signed commits/tags                        │
│ - Synthetic CI/provenance fixtures now       │
│ - Real Sigstore/in-toto/SLSA only after tests│
└─────────────────────────────────────────────┘
```

## Design principle

Every layer should be replaceable. The user gets a normal forge interface; the system can route underlying data to Git mirrors, Radicle nodes, Nostr relays, ActivityPub forges, and content-addressed artifact stores as those integrations become verified.

## Consolidated phased architecture

### Phase 1: local deterministic product skeleton — complete

Build a local-only project registry, fixture, renderer, and tests. This makes the product shape concrete without choosing a permanent network substrate too early.

- Registry: `schemas/project-registry.schema.json`
- Example data: `fixtures/example-project.registry.json`
- Renderer: `scripts/render_project_page.py`
- Output: `output/demo-project.html`
- Tests: stdlib `unittest`

### Phase 2: dry-run protocol event compatibility — complete as fixtures

Map the registry to Nostr NIP-34 repository announcement, issue, and patch shapes. This remains a dry run: no relay publication, no relay readback, no real keys, and no valid event signatures.

### Phase 3: source-inspected Radicle mapping — complete as fixture, not live CLI verification

Radicle concepts have been mapped from official source/manpage/examples into the registry model and a synthetic fixture. The next Radicle step is a safe local replay with an approved binary/install path and a temporary `RAD_HOME`; until that happens, Radicle support must be described as **source-inspected and synthetic**, not live-verified.

### Phase 4: artifact/provenance display — complete as local metadata, not live trust

Release artifact metadata now carries hashes, a locally computed CID-compatible value, availability flags, and synthetic provenance/CI fields. This proves the data model and renderer display, not storage durability or supply-chain security.

### Phase 5: public collaboration scaffolding — complete on GitHub, temporary by design

Public GitHub issues/discussions are available for bounded collaboration while decentralized collaboration support remains fixture-backed. Public claims should continue to label the project as research/prototype work.

### Phase 6: live adapter gates — next architecture phase

Only promote a protocol from fixture/supporting research to live support when the repository contains reproducible evidence:

1. **Nostr NIP-34 adapter:** local or disposable-project-key signing, relay selection, publish/readback evidence, parser tests, and documented event/key storage boundaries.
2. **Radicle adapter:** approved installation path, temporary local `RAD_HOME`, disposable repo, captured `rad .` / identity payload / issue / patch evidence, and no accidental public seed publishing.
3. **Artifact storage adapter:** explicit state split among local hash, live IPFS add/fetch, pinned provider, and paid durable storage; no Filecoin/Arweave wallet/spend without approval.
4. **Provenance adapter:** optional real signing/verification path with test artifacts, no production/private keys, no SLSA level claim unless actually satisfied and documented.
5. **ForgeFed bridge:** object-shape mapping first; do not run a public actor until moderation, security, and abuse-control gates exist.

## Recommended MVP object model

### Project registry

The canonical MVP object. Contains:

- Schema/version metadata.
- Project id, name, description, default branch.
- Maintainers with identity type and public id.
- Clone URLs and web URLs.
- Issue and patch summary lists for static rendering.
- Release metadata including hashes and optional content-addressed URIs.
- Optional CI/provenance fields with explicit synthetic/live status flags.
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

MVP releases include version, tag, artifact names, SHA-256 hashes, signature placeholders, attestation placeholders, optional CID-compatible metadata, and explicit availability/trust flags. Real signing/storage comes after local rendering and fixture validation.

## Decision matrix for the next implementation step

| Candidate next step | Why it matters | Current evidence | Promotion gate | Recommendation |
|---|---|---|---|---|
| Nostr NIP-34 parser/conformance adapter | Turns dry-run events into reusable import/export seam | Repository/issue/patch fixtures and tests exist | Round-trip fixture parser plus, later, disposable-key relay publish/readback | **Do first** because it is low-cost and improves existing fixtures without new infrastructure. |
| Radicle safe local CLI replay | Tests the strongest integrated forge substrate | Source-inspected mapping fixture exists | Approved install/binary, temporary `RAD_HOME`, disposable repo, captured local evidence | **Do next** if a safe install path is available. |
| Artifact state model hardening | Prevents overclaiming around CIDs, pinning, and durability | Local hash/CID-compatible fixture exists | Separate schema/UI states for local, live IPFS, pinned, paid durable | **Do alongside adapters** because it is mostly schema/docs/test work. |
| Real provenance/signing spike | Moves from fake attestation to optional real trust | Synthetic provenance fixture exists | Disposable test keys or keyless flow, verification command output, no SLSA overclaim | **Defer until adapter/status states are clearer.** |
| ForgeFed object mapping | Keeps cross-forge interop path open | Research only | Source-pinned object mapping and moderation/security notes | **Defer live service; document shapes first.** |

## Open decision points

1. **Primary collaboration substrate:** Nostr NIP-34 first, Radicle first, or dual-target local objects?
   - Current recommendation: keep the registry as the canonical object, build a NIP-34 parser/conformance adapter first, then run a safe Radicle local replay.
2. **Identity canonicalization:** Should project authority be a Nostr pubkey, Radicle ID, DID, SSH signing key, or multi-key policy?
   - Current recommendation: registry supports multiple identifier types; do not force one yet.
3. **Issue/patch storage:** Embedded in registry for demos, separate signed objects for real use, or backend-specific objects?
   - Current recommendation: embedded summaries for static demo; signed/event objects after parser and adapter seams are proven.
4. **Relay/federation persistence:** Which relays/instances/pinning services become availability providers?
   - Current recommendation: none in MVP; use local fixtures only until explicit verification gates pass.
5. **Release signing model:** Traditional maintainer keys, Sigstore keyless, or both?
   - Current recommendation: model both; implement no production signing in autonomous loops.
6. **Moderation and abuse control:** How does a project reject spam issues/patches across public protocols?
   - Current recommendation: client-side/project-maintainer curation list in registry before public publishing.

## Why not one protocol?

GitHub is not one feature. It is code hosting, identity, issue tracking, pull requests, releases, CI, packages, search, auth, reputation, and social discovery. No single decentralized protocol currently replaces all of that well.

The likely winning system is a productized bundle of protocols behind a simple UI, with a small canonical registry object tying them together and explicit verification states for each substrate.
