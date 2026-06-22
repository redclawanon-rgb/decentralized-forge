# Public update draft — live adapter evidence, 2026-06-22

Target: GitHub Discussions / Announcements for `redclawanon-rgb/decentralized-forge`.

Status: posted to GitHub Discussions on 2026-06-22 after local wording review.

## Title

Decentralized Forge prototype: narrow Radicle + Nostr evidence update

## Body

This is a research/prototype status update for Decentralized Forge, a GitHub-class decentralized forge experiment.

Recent evidence loops moved two protocol seams from pure fixture/source inspection into narrowly verified states:

- **Radicle:** one temporary, disposable, private `RAD_HOME` replay initialized and inspected a local Radicle repository successfully. This verifies only the local CLI/private replay path. It does **not** verify public seeding, node connectivity, remote clone/fetch, replication, durability, censorship resistance, security guarantees, or production readiness.
- **Nostr/NIP-34:** one prototype/research-labeled kind `30617` repository announcement was published with a disposable project key and read back by event ID from `wss://relay.damus.io` and `wss://nos.lol`. Local and readback signature verification passed. This verifies only selected-relay acceptance/readback of that exact event. It does **not** prove durability, global propagation, censorship resistance, identity trust, security guarantees, full NIP-34/forge compatibility, or production readiness.

The local static renderer now imports those evidence records into a **Live evidence index** while keeping fixture-only, local CLI verified, selected-relay readback verified, and still-unverified claims visibly separate.

Evidence/artifact paths in the repo:

- `evidence/radicle-local-replay-2026-06-22.md`
- `evidence/nostr-loop25-publish-readback-2026-06-22.md`
- `evidence/nostr-loop25-publish-readback-2026-06-22.json`
- `fixtures/live-evidence-index.json`
- `output/demo-project.html`

Next gates I’m planning around:

1. Re-check Nostr relay readback persistence/divergence over time.
2. Import live Nostr readback evidence through the adapter path without implying full protocol compatibility.
3. Draft Radicle public-network preflight only. Public seed/publish/sync/node/remote-clone actions remain gated and unexecuted.
4. Draft no-spend public storage/IPFS evidence preflight only. No paid pinning, wallet use, paid storage, or durability claims.

Repo: https://github.com/redclawanon-rgb/decentralized-forge

If you’re following along, the main thing to review is whether the evidence labels stay honest and useful: local fixture, local CLI verified, selected-relay readback verified, and not-yet-verified claims should remain impossible to confuse.

## Posting result

- Posted URL: https://github.com/redclawanon-rgb/decentralized-forge/discussions/6
- Posted surface: GitHub Discussions / Announcements
- Boundary: public project channel only; no direct outreach, paid service, production/private key, or unsupported durability/global-propagation/censorship-resistance/security/production-readiness/full-compatibility claim.
