# Loop 70: Public Seed Update Propagation

Loop 70 proved that the first public Radicle direct-seed path can move forward,
not just serve the original snapshot.

The retained RID stayed the same:

```text
rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy
```

It advanced from:

```text
610fc3da9757d0cb123aa5976db552b991b766d4
```

to:

```text
64efbada294d4a57c014a27398b92e344c6d68aa
```

The `openclaw` VPS follower synced that update through a temporary bridge to the
retained maintainer seed. The bridge was stopped afterward, and the retained
maintainer seed on `ubuntu-work` was stopped afterward.

After that shutdown, a fresh reader on `ubuntu-work` connected to the public VPS
seed:

```text
z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776
```

and cloned the updated commit from the public seed.

This proves one manual update propagation through the public follower seed. It
does not prove automatic future propagation, permanent durability, global
replication, security, identity trust, default public routing, or production
readiness.
