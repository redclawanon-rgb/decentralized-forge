# Product Finish Plan

This plan moves `decentralized-forge` from a public-clone release candidate to
a usable alpha product: a technical user can discover the project, clone it
without GitHub as the authority, verify the exact commit, inspect a portable
evidence bundle, and exercise at least one decentralized collaboration path.

## Target Outcome

```text
v0.1.0-alpha is usable when a new technical user can:
1. find the public clone instructions,
2. clone the retained Radicle RID from a published direct-seed address,
3. verify the expected HEAD,
4. inspect the release-candidate bundle/report,
5. see live seed status,
6. submit or inspect one decentralized issue/patch-shaped collaboration path,
7. understand the non-claims without reading the full project history.
```

This target does not require production hosting, paid storage, wallets,
production/private personal keys, default public Radicle routing, permanent
durability, censorship resistance, security guarantees, SLSA compliance, or
production readiness.

## Current Baseline

- Retained RID: `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`
- Expected commit: `d596024dac0d90605d4f103d567e5851771be5a8`
- Primary public seed: `z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776`
- Second public seed: `z6MksRdjzuN2VYV4HTXdVSchitJ8Bq1zbx8WhBb3KhyfSm6A@187.77.19.162:8877`
- Fresh public clone evidence:
  - `evidence/radicle-first-public-clone-primary-d596024-2026-06-30.json`
  - `evidence/radicle-first-public-clone-second-d596024-2026-06-30.json`
- Portable bundle SHA-256 from the first public clone RC:
  `9c740f82324da14de34c01d236ea01d63550525b6ddcc0adcbd6908a54f9b3c5`

## Definition Of Done

- A release-candidate handoff exists with exact RID, seed addresses, expected
  commit, bundle digest, verifier command, and non-claims.
- A third-party or outside-reader clone rehearsal is recorded, or the blocker is
  documented with a copy/paste script for the user to run.
- The README first screen prioritizes "clone", "verify", "inspect bundle", and
  "known limits" over historical detail.
- A generated public seed status artifact summarizes latest known seed health
  for both public seed addresses.
- At least one decentralized collaboration path is usable enough for an alpha:
  selected-relay Nostr issue/patch publish/readback, Radicle patch workflow, or
  a clearly bounded dry-run plus evidence-backed next command.
- The portable bundle/report/release note include the user-facing clone path,
  seed status, collaboration status, and non-claims.
- CI is green on `main`.

## Phases

### Phase 1: Public Alpha Handoff

Turn the current RC evidence into a release-like handoff:

- finalize `docs/public-update-drafts/2026-06-30-first-public-clone-rc.md`;
- decide whether to publish as a GitHub draft release, tag, or release-note
  document only;
- ensure the release text points at the Radicle clone verifier first, not at
  GitHub as the source of authority;
- keep bundle verification and non-claims attached to the handoff.

### Phase 2: Outside Reader Rehearsal

Run or prepare a clone rehearsal outside the seed/service path:

- preferred: a third-party machine or the user's separate Linux/VPS path runs
  `python scripts/forge_registry.py verify-first-public-clone --json`;
- fallback: produce a copy/paste rehearsal script and evidence template when
  an outside machine is not available inside the autonomous run;
- import successful evidence into `fixtures/live-evidence-index.json`.

### Phase 3: Public Product Surface

Make the first screen usable:

- compress README history behind links;
- put the Radicle clone verifier, bundle verification, seed status, and
  non-claims above the long evidence catalog;
- make `docs/community-quickstart.md` the canonical "new user" path.

### Phase 4: Seed Status Artifact

Generate an inspectable status artifact from committed evidence:

- `output/public-seed-status.json` for machines;
- optional `output/public-seed-status.html` for readers;
- include seed address, RID, expected commit, latest evidence file, pass/fail,
  checked time, and claim boundary;
- do not claim uptime, SLA, automatic repair, default routing, or durability.

### Phase 5: First Decentralized Collaboration Path

Choose the fastest alpha path that proves collaboration intent:

- first choice: Nostr selected-relay issue/patch publish/readback using
  disposable project-scoped keys and existing NIP-34 adapter concepts;
- second choice: Radicle patch workflow if the CLI path is already available on
  Linux and does not require maintainer secrets;
- fallback: one-command unsigned draft/export path with a clear live replay gate.

### Phase 6: Release Candidate Freeze

Freeze the alpha candidate:

- regenerate bundle/report/release note;
- run `verify-local --skip-npm-ci`;
- push and require CI green;
- update `STATUS.md` with the exact release commit and remaining non-blocking
  post-alpha gates.

## Autonomous Loop Sequence

The controller may execute these loops in order without asking for another
"continue" as long as each loop stays within `fixtures/next-loop-controller.json`
approval boundaries.

### Loop 83: Alpha Release Handoff

**Goal:** Convert the current first-public-clone RC into a release-facing
handoff.

**Actions:**

- Review and tighten the public update draft.
- Add or update release-note text with exact RID, seed addresses, verifier
  command, bundle digest, and non-claims.
- Decide whether the current repo should create a GitHub draft release or stop
  at a committed release-note draft; do not create a tag unless the release gate
  explicitly says to.

**Verification:**

- `python scripts/forge_registry.py export-bundle-release-note output/decentralized-forge-verification-bundle.zip`
- focused tests around bundle release-note and public update text.

**Stop Conditions:**

- A tag, GitHub Release, or public post would require a user-facing product
  decision not already encoded in docs. Treat release tags/GitHub Releases/public announcements as separately approved release actions.
- Release text starts implying durability, security, censorship resistance,
  default routing, SLSA compliance, or production readiness.

### Loop 84: Outside Reader Clone Rehearsal

**Goal:** Prove or package the next outside-reader clone check.

**Actions:**

- Prefer running the public clone verifier from an outside machine/path not used
  as a seed service.
- If an outside run is not accessible autonomously, create
  `scripts/run_first_public_clone_rehearsal.py` or a shell-friendly command file
  that the user can paste on Linux, plus an evidence template.
- Import successful proof into the live evidence index when available.

**Verification:**

- Fresh clone HEAD equals `d596024dac0d90605d4f103d567e5851771be5a8`, or the
  blocker is explicitly recorded with exact next command.
- Evidence remains secret-free.

**Stop Conditions:**

- The check requires production/private personal keys, paid infrastructure,
  direct outreach, or broader claims.
- Public seed returns a stale commit or is unreachable.

### Loop 85: First-Screen Product Surface

**Goal:** Make the repo usable without reading the whole evidence history.

**Actions:**

- Restructure README top sections around clone, verify, inspect bundle, and
  limits.
- Move historical evidence catalog behind a "details" section or separate doc
  link when possible.
- Update `docs/community-quickstart.md` as the canonical new-user path.

**Verification:**

- Docs tests assert the clone/verify/bundle/non-claim path appears before the
  long evidence catalog.
- `python scripts/forge_registry.py verify-local --skip-npm-ci`

**Stop Conditions:**

- Edits remove evidence traceability or soften non-claims.

### Loop 86: Public Seed Status Artifact

**Goal:** Give users a quick status artifact for the public seed paths.

**Actions:**

- Add a generator command for `output/public-seed-status.json`.
- Optionally render `output/public-seed-status.html`.
- Include both public seed addresses, current RID, expected commit, latest
  evidence files, pass/fail booleans, and non-claims.
- Include the artifact in the portable bundle.

**Verification:**

- JSON validates.
- Bundle report surfaces status artifact path.
- Tests assert no uptime/SLA/durability/security overclaims.

**Stop Conditions:**

- Status text implies live monitoring, SLA, automatic repair, or durability
  without matching evidence.

### Loop 87: Decentralized Collaboration Alpha Path

**Goal:** Add the first usable issue/patch collaboration path beyond clone.

**Actions:**

- Prefer a Nostr selected-relay issue/patch publish/readback rehearsal with a
  disposable project-scoped key and low-volume selected relays.
- Reuse existing NIP-34 adapter concepts and live evidence index structure.
- If live relay publish is blocked, add the exact one-command draft/export path
  and a live replay gate.

**Verification:**

- Published/readback events verify locally and from selected relays, or fallback
  draft artifacts validate and clearly say "not live-published".
- Evidence imports into `fixtures/live-evidence-index.json`.

**Stop Conditions:**

- Relay auth/payment is required.
- A production/private personal key would be needed.
- Claims would exceed selected-relay readback evidence.

### Loop 88: Alpha Freeze And CI Gate

**Goal:** Produce the final v0.1.0-alpha candidate package.

**Actions:**

- Regenerate bundle, reports, status artifacts, and release note.
- Run full local verification with existing dependencies.
- Commit, push, and verify GitHub Actions.
- Update `STATUS.md` with release-candidate commit and next post-alpha gates.

**Verification:**

- `python scripts/forge_registry.py verify-local --skip-npm-ci`
- `python scripts/forge_registry.py verify-bundle output/decentralized-forge-verification-bundle.zip`
- `python scripts/forge_registry.py verify-bundle-cleanroom output/decentralized-forge-verification-bundle.zip`
- GitHub Actions green on `main`.

**Stop Conditions:**

- Working tree is dirty after regeneration.
- CI fails.
- A release action would require a tag/GitHub Release/public announcement
  decision not already approved.

## Post-Alpha Gates

These are valuable, but not required before v0.1.0-alpha:

- independent provider/network seed availability;
- seed backup and restore drill;
- automatic stale-cache refresh;
- public monitor/status publishing;
- full Radicle patch workflow;
- real signed release/provenance verification;
- durable storage/pinning with explicit cost/key approval.
