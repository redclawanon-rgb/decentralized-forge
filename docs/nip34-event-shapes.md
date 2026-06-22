# NIP-34 Event Shapes Dry Run

Retrieval/source basis: Nostr NIP-01 and NIP-34, https://github.com/nostr-protocol/nips/blob/master/01.md and https://github.com/nostr-protocol/nips/blob/master/34.md, source-inspected 2026-06-22.

This document maps the local project registry fixture to NIP-34-style event bodies. It is a **dry run only**:

- No private keys are used.
- No event IDs/signatures are real.
- No event is published to public relays.
- Relay URLs in fixtures are examples/hints only.

Loop 11 adds a stdlib-only local parser/export seam in `scripts/nip34_adapter.py`. The adapter reads the repository announcement and collaboration fixtures and round-trips them back into registry-shaped concepts for tests and future UI integration. Loop 12 wires that adapter into the static renderer through paired optional fixture arguments. Loop 13 adds a local repository state/status fixture generated from the recorded local Git HEAD at fixture creation time; later commits may make that recorded SHA an ancestor rather than current `HEAD`. Loop 14 adds local NIP-01 event-shape/conformance metadata reports for those dry-run events, including compact serialized payloads and possible reference event IDs when the fixture shape permits them. None of these paths replace fixture IDs, sign events, verify keys, connect to relays, fetch relay state, or publish anything.

Loop 5 local relay/tool check:

- Checked `nak`, `nostril`, `strfry`, and `nostr-rs-relay` with `command -v` in this environment.
- None were installed or immediately usable.
- No unsafe curl-pipe-shell installer, paid service, production key, or public relay was used.
- The implementation therefore took the dry-run fixture fallback path.

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

Loop 13 adds `fixtures/nostr-repo-state-status.json` with a dry-run repository state event generated from `git rev-parse HEAD` in this repository at fixture creation time. In this fixture, the recorded source commit is `32f88a7a42498328a515e4763e28d84216420a98`; after subsequent commits, it is expected to be an ancestor rather than the current `HEAD`.

```json
{
  "kind": 30618,
  "content": "",
  "tags": [
    ["d", "demo-project"],
    ["HEAD", "ref: refs/heads/main"],
    ["refs/heads/main", "32f88a7a42498328a515e4763e28d84216420a98"],
    ["a", "30617:0000000000000000000000000000000000000000000000000000000000000000:demo-project"]
  ]
}
```

Acceptance gate: generate this only from an actual local Git commit SHA. The fixture keeps obvious placeholder `id`, `sig`, and `pubkey` values and records `published: false` through the adapter output. It is local state-shape evidence only, not a relay-published repository state.

`scripts/nip34_adapter.py` maps the fixture to:

- `repository_state.kind` = `30618`
- `repository_state.repo_id_tag` from the `d` tag
- `repository_state.head`, `head_ref`, and `head_commit` from the `HEAD` and ref tags
- `repository_state.refs` as a local map of Git refs to commit SHAs
- `dry_run.repository_state_event` with placeholder id/signature/pubkey and `published: false`

## Issues

NIP-34 includes issue-shaped events for repository collaboration. MVP mapping:

| Registry field | Event mapping |
|---|---|
| `issues[].id` | local display id; event id after signing/publishing in real use |
| `issues[].title` | subject/title tag or first-line content in future fixture |
| `issues[].summary` | event `content` |
| `issues[].status` | status tag or project-local curation state |
| repository link | `a` tag pointing to `30617:<repo-owner-pubkey>:demo-project` |

Dry-run rule: issue fixtures can be generated locally, but must not be relayed without approved disposable/project-scoped keys and explicit relay selection. Loop 5 adds `fixtures/nostr-collaboration-events.json` with a synthetic `kind: 1621` issue event mapped from `fixtures/example-project.registry.json`.

Observed local fixture semantics:

- The issue event links to the repository announcement through an `a` tag (`30617:<synthetic-owner-pubkey>:demo-project`).
- The issue title is preserved in a `subject` tag.
- The registry issue summary is preserved in Markdown `content`.
- The local registry status is preserved as a fixture-only `status` tag so parser tests can round-trip it; this is not a claim that every relay/client will interpret that tag.
- The event has obvious placeholder `id`/`sig` strings and a repeated-hex synthetic pubkey. It is intentionally unusable as a signed public event.
- `scripts/nip34_adapter.py` maps `kind: 1621` events back to registry-like issue records using the `subject` tag as `title`, the fixture-only `status` tag as `status`, and the first Markdown paragraph in `content` as `summary`, while preserving full `content`, source event kind, repository address, and dry-run placeholders.

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

Loop 5 adds a synthetic `kind: 1617` patch event in `fixtures/nostr-collaboration-events.json`:

- The patch/proposal links to the same repository announcement via an `a` tag.
- The patch title is preserved in a `subject` tag.
- The registry patch summary appears in a minimal `git format-patch`-shaped content body.
- The example diff is deliberately tiny and synthetic; it is parser/shape evidence, not a proposed repository change to apply.
- `id`, `sig`, and `pubkey` remain dry-run placeholders; no signature validity or relay acceptance is claimed.
- `scripts/nip34_adapter.py` maps `kind: 1617` events back to registry-like patch records using the `subject` tag as `title`, the fixture-only `status` tag as `status`, the first body paragraph after the mail-style patch headers as `summary`, and the full `git format-patch`-shaped body as `content`.

## Local adapter verification

The Loop 11 helper accepts the two dry-run fixture JSON objects (or paths via its CLI) and exports:

- `project.id`, `project.name`, `project.description`, and `project.web_urls` from `kind: 30617` tags.
- `clone_urls[]` from `clone` tags with local transport inference (`file://` as `git`, `nostr://` as `nostr`, `rad:` as `radicle`).
- Nostr maintainers from `maintainers` tags.
- `substrates.nip34` repository kind, repo id tag, relay hints, topics, and the explicit `dry-run-only` publish status.
- `issues[]` and `patches[]` from `kind: 1621` and `kind: 1617` events.
- `dry_run` metadata preserving fixture notices, placeholder IDs/signatures, relay-tool fallback state, synthetic key policy, NIP-35 boundary, and `published: false` for each event.
- `dry_run.conformance.reports[]` for the repository announcement, issue, patch, and repository state fixtures.

This is conformance/round-trip evidence for local fixtures only. It is not a live Nostr adapter and does not claim relay read/write compatibility.

## Loop 14 local NIP-01 conformance metadata

NIP-01 defines the event fields `id`, `pubkey`, `created_at`, `kind`, `tags`, `content`, and `sig`; it defines event IDs as the SHA-256 hash of the UTF-8 JSON serialization of `[0,pubkey,created_at,kind,tags,content]` with no whitespace. NIP-34 uses `kind: 30617` for repository announcements, `kind: 30618` for repository state, `kind: 1621` for issues, and `kind: 1617` for patches.

Loop 14 implements only local metadata checks:

- Required event fields checked: `pubkey`, `created_at`, `kind`, `tags`, and `content`.
- Shape checks: `kind` and `created_at` are exact JSON-style integers (Python bools are rejected), `content` is a string, and every tag is an array of strings.
- Fixture pubkeys must be 64 lowercase hex or this project's obvious repeated-digit synthetic fixture values.
- Placeholder `id` and `sig` strings are accepted and reported as placeholders because the fixtures are dry-run only.
- `event_id_computed: false`, `signed: false`, and `published: false` remain explicit even when a `possible_event_id` reference hash is included.
- `serialized_event_payload` and `possible_event_id` are local references only; they do not replace fixture `id` values and are not proof of signing or relay acceptance.

## Local renderer/import surface

Loop 12 extends `scripts/render_project_page.py` with paired optional arguments:

```sh
python3 scripts/render_project_page.py fixtures/example-project.registry.json output/demo-project.html \
  --nip34-repo-fixture fixtures/nostr-repo-announcement.json \
  --nip34-collaboration-fixture fixtures/nostr-collaboration-events.json \
  --nip34-state-status-fixture fixtures/nostr-repo-state-status.json
```

When the repository and collaboration arguments are provided, the renderer imports the fixture pair through `scripts/nip34_adapter.py` and adds a **NIP-34 fixture adapter** section to the generated HTML. Loop 13's optional state/status argument extends that section with the `kind: 30618` state, HEAD ref/commit, local refs, fixture-only status/check projections, and explicit state/status non-claims. The section displays repository id/name/kind, relay hints, dry-run publish status, imported issue and patch counts/titles/statuses/summaries/source kinds, placeholder event IDs/signatures, relay-tool fallback, synthetic key policy, NIP-35 boundary fields, and repository state/status dry-run fields.

The arguments must be provided together so the renderer cannot accidentally display a partial repository or collaboration import. The output is labeled as local parser/conformance data and explicitly states that no relay publishing, signing, fixture ID replacement, relay fetching, or live verification is performed or claimed. Any `possible_event_id` values are local reference hashes only, not signed or relay-accepted event ID claims.

## NIP-35 boundary

NIP-35 defines torrent index/comment events (`kind: 2003` and `kind: 2004`), not repository issues or patches. Loop 5 therefore records a `nip35_boundary` object in the collaboration fixture instead of inventing NIP-35 issue/patch semantics.

Loop 6 keeps artifact distribution metadata in the project registry instead of inventing NIP-35 release semantics. `docs/artifact-metadata.md` documents the local CID-compatible fixture. No paid pinning/storage, wallet, Filecoin/Arweave spend, live IPFS verification, or durability claim was made.

## Status/check events

Loop 13 also records fixture-only status/check projections in `fixtures/nostr-repo-state-status.json`. They are deliberately **not** claimed as standardized/live NIP status behavior; they preserve the existing synthetic CI/provenance names and conclusions while tying them to the local repository state commit.

Current local fields:

- `source_ci_check_id`: existing registry synthetic CI check id (`local-fake-ci-001`, `local-fake-ci-002`)
- `target_type`: `repository_state`
- `target_ref`: `refs/heads/main`
- `target_commit`: the same recorded local Git SHA used in the `kind: 30618` event
- `provider`: `local-fixture-projection`
- `status`/`conclusion`: copied as local fixture display fields
- `synthetic: true` and `published: false`

The fixture has explicit non-claims for no relay publish/fetch, no fixture ID replacement, no signing/private keys, no public CI status creation, and no live NIP status semantics claim. Local `possible_event_id` reference hashes, when present in conformance reports, are not signed or relay-accepted event IDs.

## Open decisions before public NIP-34 publishing

1. Which Nostr key controls the canonical repository announcement?
2. Which relays are monitored, and what is the anti-spam/curation policy?
3. Is `npub` or raw hex public key stored in registry fixtures? NIP events use hex pubkeys; human docs often use `npub`.
4. How are maintainer rotations represented across registry signatures, NIP-34 tags, and other substrates?
5. What local cache/export format preserves events if relays drop data?
