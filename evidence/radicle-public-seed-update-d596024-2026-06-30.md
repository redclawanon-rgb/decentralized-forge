# Loop 75 Radicle Public Seed Update

The retained RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` was advanced from `ef16e2ad39d3e13bdcc9d454443c5bbb17733c68` to `d596024dac0d90605d4f103d567e5851771be5a8`.

Both public seed addresses were verified by fresh-profile clone/readback after the temporary retained maintainer seed was stopped:

- Primary: `z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776` -> `d596024dac0d90605d4f103d567e5851771be5a8`
- Second: `z6MksRdjzuN2VYV4HTXdVSchitJ8Bq1zbx8WhBb3KhyfSm6A@187.77.19.162:8877` -> `d596024dac0d90605d4f103d567e5851771be5a8`

The follower refresh encountered stale persistent follower cache state. The `openclaw` RID storage was moved to a host-local backup and rebuilt from the trusted retained maintainer seed. The `ubuntu-work` mirror required a fresh `rad-home` while preserving `keys/` and `config.json`; its node ID remained `z6MksRdjzuN2VYV4HTXdVSchitJ8Bq1zbx8WhBb3KhyfSm6A`.

No retained maintainer key material was copied to public follower hosts. No committed evidence contains passphrases or Radicle key material. This is not proof of automatic future propagation, permanent durability, default public routing, security, identity trust, or production readiness.
