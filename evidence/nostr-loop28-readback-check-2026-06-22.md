# Nostr Loop 28 readback persistence/divergence check

Created UTC: `2026-06-22T18:32:38.019783+00:00`

## Scope

Loop 28 re-read the Loop 25 prototype/research NIP-34 event by event ID. Permission E allowed low-volume extra relay readback checks using the disposable project key boundary; this loop did not publish any new event and did not read or print secret key material.

## Event

- Event ID: `4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba`
- Input event: `evidence/nostr-loop24-signed-event-preview-2026-06-22.json`
- Original selected relays from Loop 25: `wss://relay.damus.io`, `wss://nos.lol`

## Results

| Relay | Source | Returned matching event | Fields match preview | `nak verify` | Notes |
| --- | --- | --- | --- | --- | --- |
| `wss://relay.damus.io` | loop25-selected | `True` | `True` | pass | matching event returned and verified |
| `wss://nos.lol` | loop25-selected | `True` | `True` | pass | matching event returned and verified |
| `wss://relay.primal.net` | permission-e-extra-readback-only | `True` | `True` | pass | matching event returned and verified |
| `wss://nostr.wine` | permission-e-extra-readback-only | `False` | `False` | not run | no matching event returned during this check |

## Outcome

- Matched relays: `['wss://relay.damus.io', 'wss://nos.lol', 'wss://relay.primal.net']`
- Verified relays: `['wss://relay.damus.io', 'wss://nos.lol', 'wss://relay.primal.net']`
- The two Loop 25 selected relays still returned the exact event and passed `nak verify` during this check.
- Extra readback-only relays that did not return the event in this check: `['wss://nostr.wine']`.

## Non-claims

- readback persistence on selected relays is not a durability guarantee
- extra relay non-readback is not proof of absence from the wider Nostr network
- not proof of global propagation
- not proof of censorship resistance
- not proof of identity trust
- not production readiness
- not full NIP-34 or forge protocol compatibility

## Actions not taken

- no new Nostr event was published
- no secret key material was read or printed
- no paid/authenticated relay was used
- no production/private personal key was used
- no Radicle public-network action was taken

