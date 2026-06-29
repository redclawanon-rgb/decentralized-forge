# Loop 71: External Public Seed Health Timer

`ubuntu-work` now runs a user-level `systemd` timer:

```text
decentralized-forge-radicle-healthcheck.timer
```

The timer triggers:

```text
decentralized-forge-radicle-healthcheck.service
```

which runs `scripts/check_public_radicle_seed.py` against the public `openclaw`
seed and writes:

```text
~/.local/state/decentralized-forge/radicle-health/latest.json
```

The first forced run succeeded and read back:

```text
ef16e2ad39d3e13bdcc9d454443c5bbb17733c68
```

This improves operational confidence because the public seed is now checked from
outside the VPS on a schedule. It does not prove durability, automatic repair,
security, identity trust, default public routing, or production readiness.
