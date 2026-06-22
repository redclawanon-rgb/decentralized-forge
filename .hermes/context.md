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

## Hard boundaries / gates for the current autonomous loop

Eric's current standing approval for this all-night controller run is local/reversible only. Do **not** infer public-release approval from older or unverified notes.

Allowed without additional approval:

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
- Using production/private keys for protocol actions
- Contacting anyone
- Making unsupported security/compliance/privacy claims
- Claiming production readiness, censorship-proof guarantees, or live protocol verification that has not actually been tested
## Current loop state

Loops 1–3 are complete. Loop 4 (Radicle local integration spike) is complete as a **source-inspected local artifact**, not a live Radicle CLI run.

An unauthorized public GitHub remote/repo was created by an automation lane during this cron run despite the current hard boundary. Treat the public remote as an incident requiring Eric review before any further public action; do not push/post/publish or create additional public resources from this repo.

Loop 4 outputs:

- `docs/radicle-mapping.md`
- `fixtures/radicle-backed-project.registry.json`
- expanded `tests/test_registry_fixture.py`

Radicle caveat: `rad` was unavailable in the environment, and the documented `curl https://radicle.dev/install | sh` installer was not used. The mapping was derived from official source/manpage/examples in `/tmp/radicle-heartwood` at commit `90aaec1c9eee77a0beebece48f460c1424c1c8bd`. Do not claim live Radicle verification until an approved binary/install path is available and a temporary local `RAD_HOME` replay has been run.

## Current next recommended loop

**Loop 5: Nostr local/dev relay spike or stronger dry-run issue/patch fixtures.** Do not publish to public relays. If no local relay is feasible, strengthen NIP-34/NIP-35 issue/patch fixtures and parser tests as a dry-run artifact.
