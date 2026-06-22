# Public Release Preflight

## Status

Eric explicitly approved building this project in public on 2026-06-21 via Telegram.

Public GitHub repo has been created and verified:

- URL: `https://github.com/redclawanon-rgb/decentralized-forge`
- Visibility: PUBLIC
- Default branch: `main`
- Issues: enabled
- Discussions: enabled
- Wiki: disabled
- First verified remote/local match: `7941b9ee4558b644a01d63c481b2b09cca91a9e5`

Approved public actions:

- public publishing
- pushing to remote repos
- posting to Nostr/X/GitHub/etc.
- creating public accounts/projects

Still gated:

- spending money
- provisioning paid infrastructure
- using production/private personal keys for protocol actions
- making unsupported security/compliance/privacy claims
- claiming production readiness, censorship-proof guarantees, or live protocol verification that has not actually been tested
- directly contacting specific people outside public project channels unless separately approved

## First public target

- Platform: GitHub
- Owner: `redclawanon-rgb`
- Repo name: `decentralized-forge`
- Visibility: public
- Default branch: `main`
- Issues: enabled
- Discussions: enabled
- Wiki: disabled
- License: MIT unless Eric later chooses another license

## Pre-push hygiene checklist

- [x] `gh auth status` checked without printing secret values manually.
- [x] Local tests pass: `python3 -m unittest discover -s tests`.
- [x] Public-facing docs scanned for raw secrets/private keys.
- [x] Public-facing docs avoid claiming production security, live Radicle/Nostr verification, censorship-proof guarantees, or finished GitHub replacement status.
- [x] Add/confirm `LICENSE` before inviting contributors.
- [x] Create public GitHub repo and push once tree is clean.
- [x] Read back GitHub repo URL/settings.
- [x] Update `STATUS.md` and `.hermes/context.md` with verified public URL.

## Public non-claim wording

Use phrasing like:

- "research/prototype"
- "decentralized forge experiment"
- "local fixtures and mappings"
- "source-inspected Radicle mapping"
- "dry-run NIP-34 shapes"

Avoid phrasing like:

- "censorship-proof"
- "production-ready"
- "secure"
- "verified on public relays"
- "live Radicle integration"
- "GitHub replacement is complete"

## Stop criteria

Stop before additional public push/post if:

- tests fail,
- secret scan finds likely real credentials,
- docs overclaim security/production readiness,
- repo creation or push fails in a way that risks duplicate repos,
- paid services/wallets/production keys would be required.
