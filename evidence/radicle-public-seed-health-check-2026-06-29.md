# Loop 69: Public Radicle Seed Health Check

`scripts/check_public_radicle_seed.py` is a repeatable health check for the
current public Radicle direct-seed path. It creates a fresh temporary Radicle
profile, starts a local reader node, connects to one explicit seed address,
clones one RID, checks `git rev-parse HEAD`, stops the reader node, and removes
temporary state by default.

Loop 69 ran the check from `ubuntu-work` against:

```text
z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776
```

It cloned:

```text
rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy
```

and read back:

```text
610fc3da9757d0cb123aa5976db552b991b766d4
```

The JSON evidence is
`evidence/radicle-public-seed-health-check-2026-06-29.json`.

This is a point-in-time direct-seed health check, not a durability, security,
identity-trust, censorship-resistance, default-routing, or production-readiness
claim.
