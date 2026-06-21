# Agent Loops

This file turns the broad mission into bounded, verifiable loops.

## Loop design rules

Inspired by Eric's X bookmark signal around loop engineering, subagents, scoping, and verification:

1. Every loop has a named deliverable.
2. Every loop has gates and stop conditions.
3. Every loop writes/updates docs before moving on.
4. Every subagent result is parent-verified with files, source links, tests, or git state.
5. A loop can continue overnight only if it is local, reversible, and bounded.
6. Public actions are hard gates.

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

Do not publish to public relays without Eric approval.

## Loop 4: Issue/patch collaboration spike

**Goal:** Demonstrate issue/comment/patch objects independent from GitHub.

**Gate:**

Local/dev relay or dry-run fixture only unless Eric approves public relay usage.
