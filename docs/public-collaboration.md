# Public collaboration surface

Loop 9 establishes GitHub as the temporary public collaboration surface for the decentralized-forge prototype while decentralized issue/patch federation remains fixture-backed.

## Current public home

- GitHub repo: <https://github.com/redclawanon-rgb/decentralized-forge>
- Visibility: public
- Issues: enabled
- Discussions: enabled
- Wiki: disabled
- License: MIT

## Public collaboration stance

This project should be described as:

- a research/prototype workspace;
- a decentralized forge experiment;
- a local registry/static renderer plus protocol-mapping fixture set;
- a place to discuss protocol adapters, project identity, artifact metadata, and provenance models.

Do not describe it as:

- production ready;
- secure, compliant, or SLSA verified;
- censorship-proof;
- live-verified on Nostr/Radicle/IPFS unless a future loop actually verifies that;
- a complete GitHub replacement.

## First public issue set

The initial public issues are bounded and collaboration-friendly:

1. Renderer UX: improve fixture/non-claim display — <https://github.com/redclawanon-rgb/decentralized-forge/issues/1>.
2. Nostr adapter: turn NIP-34 issue/patch dry-run events into parser/conformance tests — <https://github.com/redclawanon-rgb/decentralized-forge/issues/2>.
3. Radicle adapter: find a safe CLI verification path and replay in a temporary local `RAD_HOME` — <https://github.com/redclawanon-rgb/decentralized-forge/issues/3>.
4. Artifact metadata: separate local fixture, live-verified CID, pinned artifact, and durable paid-storage states — <https://github.com/redclawanon-rgb/decentralized-forge/issues/4>.
5. Provenance model: evolve fake local attestations toward optional real signing without claiming SLSA — <https://github.com/redclawanon-rgb/decentralized-forge/issues/5>.

These issues are temporary GitHub coordination scaffolding. They are not evidence that decentralized issue/patch federation is live.

## Draft public update

> Opened a public research/prototype repo for a decentralized GitHub-class forge: local project registry schema, static renderer, Nostr/Radicle mapping fixtures, local CID-compatible artifact metadata, and synthetic CI/provenance displays. This is not production-ready or live protocol verified yet; the goal is to make the seams explicit and invite focused protocol/UX collaboration. https://github.com/redclawanon-rgb/decentralized-forge

## Boundaries

- Public repo/issues/discussions are allowed for this project.
- Public posts are allowed only when accurate, non-spammy, and clearly prototype-labeled.
- Do not contact specific people directly without separate approval.
- Do not use production/private keys, paid services, wallets, or unsupported security/compliance claims.
