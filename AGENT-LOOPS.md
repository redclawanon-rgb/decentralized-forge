# Agent Loops

This file turns the broad mission into bounded, verifiable loops.

## Loop design rules

Inspired by Eric's X bookmark signal around loop engineering, subagents, scoping, and verification:

1. Every loop has a named deliverable.
2. Every loop has gates and stop conditions.
3. Every loop writes/updates docs before moving on.
4. Every subagent result is parent-verified with files, source links, tests, or git state.
5. A loop can continue overnight if it is bounded, reversible, or covered by the standing public-build approval.
6. Public actions are allowed for this project when accurate, non-spammy, prototype-labeled, and not dependent on paid infrastructure or production/private keys.

## Loop 1: Research corpus and protocol matrix

**Goal:** Build the source-grounded knowledge base.

**Tasks:**

- Research Radicle current architecture and collaboration model.
- Research ForgeFed/ActivityPub forge federation status.
- Research Nostr NIP-34/NIP-35 and tools like n34/ngit.
- Research IPFS/IPLD/Filecoin/Arweave for repo snapshots and artifacts.
- Research Sigstore/cosign/in-toto/SLSA for signed CI/release trust.
- Research AT Protocol/PDS, Hypercore, and SSB as optional inspiration.
- Fill `PROTOCOL-MATRIX.md`.
- Write recommendation in `ARCHITECTURE.md`.

**Stop conditions:**

- Source access fails for a critical protocol.
- Findings show the core thesis is infeasible.
- Tool/time cap reached.

## Loop 2: MVP registry object and static repo page prototype

**Goal:** Prove a decentralized project identity can be represented and rendered.

**Tasks:**

- Create `schemas/project-registry.schema.json`.
- Create `fixtures/example-project.registry.json`.
- Create a local renderer script or static page.
- Validate the schema with a local test.

**Stop conditions:**

- No schema validator available and dependency install fails.
- Loop 1 recommends a different canonical object model.

## Loop 3: NIP-34 read/write spike

**Goal:** Test decentralized repo announcement mechanics locally/safely.

**Tasks:**

- Use test keys only.
- Use local/dev relay if available, otherwise prepare a dry-run payload.
- Create repo announcement event shape.
- Read/parse announcement back if local relay exists.

**Gate:**

Public relay publishing is now approved for this project only with disposable/project-scoped keys, documented storage locations, and prototype labeling. Use only test keys for local/dev relay or dry-run fixtures; never use production/private personal keys.

## Loop 4: Radicle local integration spike

**Goal:** Map Radicle's repository identity, delegates, issues, and patches into the local registry model without publishing.

**Tasks:**

- Install or locate Radicle tooling only through an approved safe path; do not run curl-pipe-shell installers.
- If the CLI is unavailable, inspect official source/manpage/examples and mark outputs as source-inspected rather than live-tested.
- Write `docs/radicle-mapping.md` mapping Radicle fields to `project-registry.schema.json`.
- Add a synthetic Radicle-backed registry fixture with fake public IDs only.
- Validate fixture JSON and run unit tests.

**Gate:**

No public seed publishing unless it is an accurate prototype-labeled project update covered by the public-build approval. No production/private keys, unsafe installs, contacting specific people outside public channels, or spending without explicit approval.

**Current result:**

Completed as a source-inspected local spike because `rad` was unavailable and the documented `curl https://radicle.dev/install | sh` path was not approved. Outputs are `docs/radicle-mapping.md`, `fixtures/radicle-backed-project.registry.json`, and expanded registry tests.

## Loop 5: Nostr local/dev relay or stronger dry-run collaboration fixtures

**Goal:** Demonstrate repository issue/patch announcement mechanics without using public relays.

**Tasks:**

- Prefer a free/safe local relay if available; publish only synthetic test-key events and read them back locally.
- If no local relay is feasible, expand NIP-34/NIP-35 dry-run fixtures for issue and patch collaboration events.
- Add parser/validation tests that prove the local registry can ingest or preserve the event shapes.
- Update `STATUS.md`, `.hermes/context.md`, and docs with verification evidence.

**Gate:**

Public relay publishing is allowed only with disposable/project-scoped keys and documented storage; otherwise keep dry-run fixtures and use GitHub issues/discussions as the public collaboration surface first. No production/private keys, unsupported public claims, paid services, or contacting specific people outside public channels.
