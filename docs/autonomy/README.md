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

## First Public Clone RC

The active autonomous goal is `first-public-clone-rc`, backed by `docs/first-public-clone-rc-plan.md`.

The controller may continue through Loops 77-82 without another "continue" prompt when each loop stays inside the recorded approval boundaries and passes its verification gates:

- Loop 77: public clone surface audit.
- Loop 78: first public clone verifier command.
- Loop 79: fresh Linux public clone proof.
- Loop 80: product surface RC polish.
- Loop 81: release candidate package.
- Loop 82: availability hardening backlog.

It still stops before spending, wallets, paid infrastructure, production/private personal key use, direct outreach, new persistent public services, or stronger durability/censorship/security/SLSA/production-readiness claims unless separate approval is recorded.
