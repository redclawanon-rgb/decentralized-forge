# NIP-34 Event Shapes Dry Run

Retrieval/source basis: Nostr NIP-34, https://github.com/nostr-protocol/nips/blob/master/34.md, retrieved 2026-06-22.

This document maps the local project registry fixture to NIP-34-style event bodies. It is a **dry run only**:

- No private keys are used.
- No event IDs/signatures are real.
- No event is published to public relays.
- Relay URLs in fixtures are examples/hints only.

## Repository announcement: `kind: 30617`

NIP-34 defines repository announcements as addressable events. The MVP registry maps to a synthetic `kind: 30617` body in `fixtures/nostr-repo-announcement.json`.

| NIP-34 tag | Registry source | Demo value |
|---|---|---|
| `['d', '<repo-id>']` | `project.id` | `demo-project` |
| `['name', '<name>']` | `project.name` | `Demo Decentralized Forge Project` |
| `['description', '<description>']` | `project.description` | local fixture description |
| `['web', '<url>']` | `project.web_urls[]` | `file://output/demo-project.html` |
| `['clone', '<url>']` | `clone_urls[].url` | local file URL, nostr URL, Radicle placeholder |
| `['relays', '<relay-url>']` | `substrates.nip34.relay_hints[]` | `wss://relay.example.invalid` |
| `['maintainers', '<pubkey>']` | Nostr maintainer public id | synthetic fixture npub |
| `['t', '<topic>']` | registry/project topics | `decentralized-forge`, `demo`, `local-only` |

## Repository state announcement: `kind: 30618`

Later fixture target. This should map Git refs to event tags:

```json
{
  "kind": 30618,
  "content": "",
  "tags": [
    ["d", "demo-project"],
    ["HEAD", "ref: refs/heads/main"],
    ["refs/heads/main", "<commit-sha>"]
  ]
}
```

Acceptance gate: generate this only from an actual local Git commit SHA.

## Issues

NIP-34 includes issue-shaped events for repository collaboration. MVP mapping:

| Registry field | Event mapping |
|---|---|
| `issues[].id` | local display id; event id after signing/publishing in real use |
| `issues[].title` | subject/title tag or first-line content in future fixture |
| `issues[].summary` | event `content` |
| `issues[].status` | status tag or project-local curation state |
| repository link | `a` tag pointing to `30617:<repo-owner-pubkey>:demo-project` |

Dry-run rule: issue fixtures can be generated locally later, but must not be relayed without approval.

## Patches / PRs

NIP-34 patch events can contain `git format-patch` output. MVP mapping:

| Registry field | Event mapping |
|---|---|
| `patches[].id` | local display id; event id after signing/publishing in real use |
| `patches[].title` | patch subject/title |
| `patches[].summary` | cover letter or summary text |
| `patches[].status` | local status/status-event mapping |
| repository link | `a` tag pointing to `30617:<repo-owner-pubkey>:demo-project` |

For large PR-like contributions, prefer branch/remote references rather than embedding huge patch content.

## Status/check events

The local registry can later model patch checks/statuses. Candidate fields:

- `target_patch_id`
- `state`: pending/success/failure/error
- `description`
- `log_uri`
- `attestation_uri`

## Open decisions before public NIP-34 publishing

1. Which Nostr key controls the canonical repository announcement?
2. Which relays are monitored, and what is the anti-spam/curation policy?
3. Is `npub` or raw hex public key stored in registry fixtures? NIP events use hex pubkeys; human docs often use `npub`.
4. How are maintainer rotations represented across registry signatures, NIP-34 tags, and other substrates?
5. What local cache/export format preserves events if relays drop data?
