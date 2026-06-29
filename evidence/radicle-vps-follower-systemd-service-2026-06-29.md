# Loop 68: VPS Follower Seed Systemd Service

`openclaw` now runs the public Radicle follower seed as an enabled user-level
`systemd` service:

```text
decentralized-forge-radicle-seed.service
```

The service runs:

```text
radicle-node --listen 0.0.0.0:8776 --force
```

It keeps the existing follower state at `~/df-rad-follower/rad-home`, uses a
private `0600` EnvironmentFile for the follower passphrase, and does not copy
retained maintainer key material to the VPS.

After an explicit service restart, a fresh reader on `ubuntu-work` connected to
`z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776`,
cloned `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`, and verified HEAD at
`610fc3da9757d0cb123aa5976db552b991b766d4`.

This proves a restart-safe user service plus post-restart public direct-seed
readback. It does not prove permanent durability, security, identity trust,
censorship resistance, global replication, default public routing, or production
readiness.
