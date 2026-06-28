# Autonomy Controller

`scripts/next_loop_controller.py` is the approval-bounded loop entry point for continuing safe project work without re-deciding the same housekeeping steps.

It may:

- check that the worktree starts clean;
- run the documented local verification suite;
- inventory live-gate tooling without live actions;
- draft a next-loop report.

It must not perform live IPFS daemon/add/fetch/gateway/pinning work, new Nostr publish/readback work, broader Radicle public-network checks, signing/provenance actions, spending, wallet use, paid infrastructure, production/private personal key use, direct outreach, or stronger durability/censorship/security/SLSA/production-readiness claims without a separate explicit target.

Run locally:

```sh
npm run next:loop
```

Run a non-writing CI-style check after dependencies are installed:

```sh
python scripts/next_loop_controller.py --check --skip-npm-ci
```

The controller config is `fixtures/next-loop-controller.json`. The local report path is `docs/autonomy/next-loop-report.md`.
