# Nostr relay publish/readback plan

Created: 2026-06-22
Loop: 24 — relay selection and event payload review

This plan prepares Loop 25 publication/readback only. The signed event preview exists locally, verifies with `nak verify`, and has **not** been published to any relay as part of Loop 24.

## Selected relays

Primary targets for Loop 25:

1. `wss://relay.damus.io`
   - NIP-11 info retrieved with `~/.local/bin/nak relay wss://relay.damus.io` on 2026-06-22.
   - Software: `git+https://github.com/hoytech/strfry.git`.
   - Reported limitations: `auth_required: false`, `payment_required: false`, `restricted_writes: false`, `max_message_length: 1000000`, `max_subscriptions: 200`, `max_limit: 500`.
   - Supported NIPs include 1 and 11. NIP-34 is not advertised in the relay info, but NIP-34 events are normal Nostr events; Loop 25 will treat acceptance/readback only as relay-level event acceptance, not full forge-protocol compatibility.

2. `wss://nos.lol`
   - NIP-11 info retrieved with `~/.local/bin/nak relay wss://nos.lol` on 2026-06-22.
   - Description: generally accepts notes, except spammy ones.
   - Software: `git+https://github.com/hoytech/strfry.git`.
   - Reported limitations: `auth_required: false`, `payment_required: false`, `restricted_writes: false`, `max_message_length: 131072`, `max_subscriptions: 20`, `max_limit: 500`.
   - Supported NIPs include 1 and 11. Same NIP-34 boundary applies.

Both relays are free/public relay targets from the local NIP-11 check. No paid infrastructure, production credentials, direct outreach, or relay account setup is required.

## Disposable key boundary

Use only the disposable project-scoped key stored outside the repo:

- Secret storage path: `~/.hermes/keys/decentralized-forge/nostr-project.nsec`
- Permissions previously recorded: `0600`
- Public key hex: `6669423ee76d9d5adc8e81df79286c2569edbe5ab84f3e35043db71a54eff5c8`
- Public key npub: `npub1ve55y0h8dkw44hyws80hj2rvy457m0j6hp8nudgy8km354807hyqp97suy`

Do not print, commit, or log the secret key value.

## Event selected for Loop 25

Event kind: `30617` (NIP-34 repository announcement)

Signed local preview:

- File: `evidence/nostr-loop24-signed-event-preview-2026-06-22.json`
- Event ID: `4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba`
- Pubkey: `6669423ee76d9d5adc8e81df79286c2569edbe5ab84f3e35043db71a54eff5c8`
- Created at: `1782142614`
- Local verification: `~/.local/bin/nak verify < evidence/nostr-loop24-signed-event-preview-2026-06-22.json` exited 0.
- Publication state: not published in Loop 24.

Unsigned payload preview:

- File: `evidence/nostr-loop24-unsigned-payload-2026-06-22.json`

## Exact content boundary

The event content is deliberately prototype/research-labeled:

> Decentralized Forge prototype/research relay test. This event announces a local/static prototype and live-adapter evidence paths only. It does not claim production readiness, durability, censorship resistance, global propagation, identity trust, security guarantees, or full protocol compatibility.

Tags include:

- `d=decentralized-forge-live-adapter-prototype-2026-06-22`
- `name=Decentralized Forge prototype live-adapter test`
- `description=Prototype/research NIP-34 repository announcement for Decentralized Forge live-adapter publish/readback verification.`
- `web=https://github.com/redclawanon-rgb/decentralized-forge`
- `clone=https://github.com/redclawanon-rgb/decentralized-forge.git`
- `relays=wss://relay.damus.io`
- `relays=wss://nos.lol`
- `t=decentralized-forge`, `t=prototype`, `t=research`, `t=live-adapter-test`

## Loop 25 publish/readback commands

Only run these under the already-granted Permission B and still preserve all boundaries:

```sh
# Verify the local signed preview before publication.
~/.local/bin/nak verify < evidence/nostr-loop24-signed-event-preview-2026-06-22.json

# Publish the exact pre-reviewed event. Do not regenerate content unless docs/evidence are updated first.
~/.local/bin/nak event wss://relay.damus.io < evidence/nostr-loop24-signed-event-preview-2026-06-22.json
~/.local/bin/nak event wss://nos.lol < evidence/nostr-loop24-signed-event-preview-2026-06-22.json

# Read back by ID from the selected relays.
~/.local/bin/nak req -i 4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba wss://relay.damus.io
~/.local/bin/nak req -i 4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba wss://nos.lol
```

Loop 25 should capture publish responses and readback JSON in secret-free evidence. It should verify returned event ID, pubkey, kind, tags, content, and signature with `nak verify`.

## Loop 25 outcome

Loop 25 completed on 2026-06-22 under Permission B.

- Published/read back exact event ID: `4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba`.
- Relays with publish success and verified readback: `wss://relay.damus.io`, `wss://nos.lol`.
- Evidence: `evidence/nostr-loop25-publish-readback-2026-06-22.md` and `evidence/nostr-loop25-publish-readback-2026-06-22.json`.
- Local and readback `nak verify` checks exited 0.

## Non-claims

Successful Loop 25 publish/readback shows only that the two selected public relays accepted and returned the exact event. It must not be described as proof of durability, global propagation, censorship resistance, identity trust, security, production readiness, or full NIP-34/forge compatibility.
