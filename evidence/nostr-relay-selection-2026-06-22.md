# Nostr relay selection evidence

Date: 2026-06-22
Loop: 24 — Nostr relay selection and event payload review

## Scope

This loop selected relays, reviewed NIP-11 relay info where discoverable, drafted the exact prototype-labeled NIP-34 repository announcement payload, signed it locally with the disposable project key, and verified the signature locally.

No relay publication or readback happened in Loop 24.

## Commands run

- `~/.local/bin/nak relay wss://relay.damus.io`
- `~/.local/bin/nak relay wss://nos.lol`
- `~/.local/bin/nak event --force-sign < /tmp/df-loop24-payload.json > evidence/nostr-loop24-signed-event-preview-2026-06-22.json` with `NOSTR_SECRET_KEY` loaded from `~/.hermes/keys/decentralized-forge/nostr-project.nsec`.
- `~/.local/bin/nak verify < evidence/nostr-loop24-signed-event-preview-2026-06-22.json`
- `python3 -m json.tool evidence/nostr-loop24-signed-event-preview-2026-06-22.json`

The secret key value was not printed, recorded, or committed.

## Relay candidates selected

### `wss://relay.damus.io`

NIP-11 info was reachable through `nak relay`.

Relevant relay info:

- Name: `damus.io`
- Description: `Damus strfry relay`
- Software: `git+https://github.com/hoytech/strfry.git`
- Version: `1.1.0-1-g691a533f11eb`
- Supported NIPs: `1, 2, 4, 9, 11, 28, 40, 45, 70, 77`
- Limitations:
  - `max_message_length: 1000000`
  - `max_subscriptions: 200`
  - `max_limit: 500`
  - `auth_required: false`
  - `payment_required: false`
  - `restricted_writes: false`

Notes: no payment/auth requirement is advertised. NIP-34 is not listed, so any Loop 25 acceptance/readback is only relay-level event acceptance, not a claim of NIP-34-specific forge compatibility.

### `wss://nos.lol`

NIP-11 info was reachable through `nak relay`.

Relevant relay info:

- Name: `nos.lol`
- Description: `Generally accepts notes, except spammy ones.`
- Software: `git+https://github.com/hoytech/strfry.git`
- Version: `1.1.0`
- Supported NIPs: `1, 2, 4, 9, 11, 28, 40, 45, 70, 77`
- Limitations:
  - `max_message_length: 131072`
  - `max_subscriptions: 20`
  - `max_limit: 500`
  - `auth_required: false`
  - `payment_required: false`
  - `restricted_writes: false`

Notes: no payment/auth requirement is advertised. The relay description warns against spammy notes; Loop 25 should publish only this single prototype-labeled event and avoid repetition unless readback truly fails and the failure evidence supports one bounded retry.

## Event payload selected

- Kind: `30617` (NIP-34 repository announcement)
- Unsigned preview: `evidence/nostr-loop24-unsigned-payload-2026-06-22.json`
- Signed preview: `evidence/nostr-loop24-signed-event-preview-2026-06-22.json`
- Event ID: `4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba`
- Pubkey: `6669423ee76d9d5adc8e81df79286c2569edbe5ab84f3e35043db71a54eff5c8`
- Created at: `1782142614`
- Relay tags: `wss://relay.damus.io`, `wss://nos.lol`
- Local verification: `nak verify` exited 0.

Event content:

> Decentralized Forge prototype/research relay test. This event announces a local/static prototype and live-adapter evidence paths only. It does not claim production readiness, durability, censorship resistance, global propagation, identity trust, security guarantees, or full protocol compatibility.

## Publication state

Not published in Loop 24.

Loop 25 may publish/read back this exact signed event under Permission B. Treat publication as public/irreversible and record relay URLs, publish responses, readback payloads, and verification results.

## Non-claims preserved

- No durability claim.
- No global propagation claim.
- No censorship-resistance claim.
- No identity-trust claim.
- No production-readiness claim.
- No full protocol-compatibility claim.
- No secret key material in this evidence.
