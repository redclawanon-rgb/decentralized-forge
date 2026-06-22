# Nostr Loop 25 publish/readback evidence

Created UTC: `2026-06-22T16:03:48.223066+00:00`

## Event

- Input: `evidence/nostr-loop24-signed-event-preview-2026-06-22.json`
- Kind: `30617`
- Event ID: `4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba`
- Public key: `6669423ee76d9d5adc8e81df79286c2569edbe5ab84f3e35043db71a54eff5c8`
- Secret key material: not present; the disposable project secret remains outside the repo at the documented key path.

## Local verification

- `nak verify < evidence/nostr-loop24-signed-event-preview-2026-06-22.json` exit code: `0`

## Publish results

### wss://relay.damus.io

- Exit code: `0`
- Stdout:
```
{"kind":30617,"id":"4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba","pubkey":"6669423ee76d9d5adc8e81df79286c2569edbe5ab84f3e35043db71a54eff5c8","created_at":1782142614,"tags":[["d","decentralized-forge-live-adapter-prototype-2026-06-22"],["name","Decentralized Forge prototype live-adapter test"],["description","Prototype/research NIP-34 repository announcement for Decentralized Forge live-adapter publish/readback verification."],["web","https://github.com/redclawanon-rgb/decentralized-forge"],["clone","https://github.com/redclawanon-rgb/decentralized-forge.git"],["relays","wss://relay.damus.io"],["relays","wss://nos.lol"],["t","decentralized-forge"],["t","prototype"],["t","research"],["t","live-adapter-test"]],"content":"Decentralized Forge prototype/research relay test. This event announces a local/static prototype and live-adapter evidence paths only. It does not claim production readiness, durability, censorship resistance, global propagation, identity trust, security guarantees, or full protocol compatibility.","sig":"109b5458e25a36c84ef633480d20c179b58f0a6a3df9576304577fc15ae44edc9f4e06f03c956ef0aa0828d75b6dabeb55fb7c9e3ebe03689c828df2753847c3"}
```
- Stderr:
```
connecting to relay.damus.io... ok.
publishing to relay.damus.io... success.
```

### wss://nos.lol

- Exit code: `0`
- Stdout:
```
{"kind":30617,"id":"4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba","pubkey":"6669423ee76d9d5adc8e81df79286c2569edbe5ab84f3e35043db71a54eff5c8","created_at":1782142614,"tags":[["d","decentralized-forge-live-adapter-prototype-2026-06-22"],["name","Decentralized Forge prototype live-adapter test"],["description","Prototype/research NIP-34 repository announcement for Decentralized Forge live-adapter publish/readback verification."],["web","https://github.com/redclawanon-rgb/decentralized-forge"],["clone","https://github.com/redclawanon-rgb/decentralized-forge.git"],["relays","wss://relay.damus.io"],["relays","wss://nos.lol"],["t","decentralized-forge"],["t","prototype"],["t","research"],["t","live-adapter-test"]],"content":"Decentralized Forge prototype/research relay test. This event announces a local/static prototype and live-adapter evidence paths only. It does not claim production readiness, durability, censorship resistance, global propagation, identity trust, security guarantees, or full protocol compatibility.","sig":"109b5458e25a36c84ef633480d20c179b58f0a6a3df9576304577fc15ae44edc9f4e06f03c956ef0aa0828d75b6dabeb55fb7c9e3ebe03689c828df2753847c3"}
```
- Stderr:
```
connecting to nos.lol... ok.
publishing to nos.lol... success.
```

## Readback results

### wss://relay.damus.io

- Exit code: `0`
- Matched event ID: `True`
- Readback fields match signed preview: `True`
- `nak verify` on readback event exit code: `0`
- Readback event JSON:
```json
{
  "content": "Decentralized Forge prototype/research relay test. This event announces a local/static prototype and live-adapter evidence paths only. It does not claim production readiness, durability, censorship resistance, global propagation, identity trust, security guarantees, or full protocol compatibility.",
  "created_at": 1782142614,
  "id": "4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba",
  "kind": 30617,
  "pubkey": "6669423ee76d9d5adc8e81df79286c2569edbe5ab84f3e35043db71a54eff5c8",
  "sig": "109b5458e25a36c84ef633480d20c179b58f0a6a3df9576304577fc15ae44edc9f4e06f03c956ef0aa0828d75b6dabeb55fb7c9e3ebe03689c828df2753847c3",
  "tags": [
    [
      "d",
      "decentralized-forge-live-adapter-prototype-2026-06-22"
    ],
    [
      "name",
      "Decentralized Forge prototype live-adapter test"
    ],
    [
      "description",
      "Prototype/research NIP-34 repository announcement for Decentralized Forge live-adapter publish/readback verification."
    ],
    [
      "web",
      "https://github.com/redclawanon-rgb/decentralized-forge"
    ],
    [
      "clone",
      "https://github.com/redclawanon-rgb/decentralized-forge.git"
    ],
    [
      "relays",
      "wss://relay.damus.io"
    ],
    [
      "relays",
      "wss://nos.lol"
    ],
    [
      "t",
      "decentralized-forge"
    ],
    [
      "t",
      "prototype"
    ],
    [
      "t",
      "research"
    ],
    [
      "t",
      "live-adapter-test"
    ]
  ]
}
```
- Raw stderr:
```
connecting to relay.damus.io... ok.
```

### wss://nos.lol

- Exit code: `0`
- Matched event ID: `True`
- Readback fields match signed preview: `True`
- `nak verify` on readback event exit code: `0`
- Readback event JSON:
```json
{
  "content": "Decentralized Forge prototype/research relay test. This event announces a local/static prototype and live-adapter evidence paths only. It does not claim production readiness, durability, censorship resistance, global propagation, identity trust, security guarantees, or full protocol compatibility.",
  "created_at": 1782142614,
  "id": "4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba",
  "kind": 30617,
  "pubkey": "6669423ee76d9d5adc8e81df79286c2569edbe5ab84f3e35043db71a54eff5c8",
  "sig": "109b5458e25a36c84ef633480d20c179b58f0a6a3df9576304577fc15ae44edc9f4e06f03c956ef0aa0828d75b6dabeb55fb7c9e3ebe03689c828df2753847c3",
  "tags": [
    [
      "d",
      "decentralized-forge-live-adapter-prototype-2026-06-22"
    ],
    [
      "name",
      "Decentralized Forge prototype live-adapter test"
    ],
    [
      "description",
      "Prototype/research NIP-34 repository announcement for Decentralized Forge live-adapter publish/readback verification."
    ],
    [
      "web",
      "https://github.com/redclawanon-rgb/decentralized-forge"
    ],
    [
      "clone",
      "https://github.com/redclawanon-rgb/decentralized-forge.git"
    ],
    [
      "relays",
      "wss://relay.damus.io"
    ],
    [
      "relays",
      "wss://nos.lol"
    ],
    [
      "t",
      "decentralized-forge"
    ],
    [
      "t",
      "prototype"
    ],
    [
      "t",
      "research"
    ],
    [
      "t",
      "live-adapter-test"
    ]
  ]
}
```
- Raw stderr:
```
connecting to nos.lol... ok.
```

## Outcome

- Relays with publish command exit 0: `['wss://relay.damus.io', 'wss://nos.lol']`
- Relays with verified readback: `['wss://relay.damus.io', 'wss://nos.lol']`

## Non-claims

- relay acceptance/readback is not a durability guarantee
- not proof of global propagation
- not proof of censorship resistance
- not proof of identity trust
- not production readiness
- not full NIP-34 or forge protocol compatibility
