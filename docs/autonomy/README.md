# Autonomy Controller

`scripts/next_loop_controller.py` is the approval-bounded loop entry point for continuing safe project work without re-deciding the same housekeeping steps.

It may:

- check that the worktree starts clean;
- run the documented local verification suite;
- inventory live-gate tooling without live actions;
- draft a next-loop report.

As of the 2026-06-28 user chat approval recorded in `fixtures/next-loop-controller.json`, live IPFS, Radicle, Nostr, and signing/provenance actions are approved when they stay free, disposable or project-scoped, low-volume, secret-free, and evidence-labeled.

It must not perform spending, wallet use, paid infrastructure, production/private personal key use, direct outreach, persistent public seed/background service operation, or stronger durability/censorship/security/SLSA/production-readiness claims without separate approval.

Run locally:

```sh
npm run next:loop
```

Run a non-writing CI-style check after dependencies are installed:

```sh
python scripts/next_loop_controller.py --check --skip-npm-ci
```

The controller config is `fixtures/next-loop-controller.json`. The local report path is `docs/autonomy/next-loop-report.md`.

## Product Finish Alpha

The active autonomous goal is `product-finish-alpha`, backed by `docs/product-finish-plan.md`.

The controller may continue through Loops 83-88 without another "continue" prompt when each loop stays inside the recorded approval boundaries and passes its verification gates:

- Loop 83: alpha release handoff.
- Loop 84: outside-reader clone rehearsal.
- Loop 85: first-screen product surface.
- Loop 86: public seed status artifact.
- Loop 87: decentralized collaboration alpha path.
- Loop 88: alpha freeze and CI gate.

It still stops before spending, wallets, paid infrastructure, production/private personal key use, direct outreach, new persistent public services, release tags/GitHub Releases/public announcements, or stronger durability/censorship/security/SLSA/production-readiness claims unless separate approval is recorded.
