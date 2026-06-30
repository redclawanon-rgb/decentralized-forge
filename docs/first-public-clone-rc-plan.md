# First Public Clone RC Plan

This plan turns the current retained-RID/public-seed evidence into the first user-facing release candidate: a technical user can find the project, clone it from Radicle through a published seed, verify the exact commit, and understand the claim boundary without asking the maintainer for extra context.

## Target Outcome

```text
v0.1.0-alpha can honestly claim: a user can clone decentralized-forge from a published Radicle direct-seed address and verify that HEAD equals the expected retained-RID commit.
```

The release candidate must not claim permanent durability, censorship resistance, global replication, default public routing, identity trust, security, SLSA compliance, or production readiness unless separate evidence is added for those exact claims.

## Definition Of Done

- README and quickstart lead with the current retained RID, public seed addresses, expected commit, and exact clone/verify commands.
- A single verifier command can perform the fresh-profile public seed clone/readback check and emit both human-readable status and JSON evidence.
- At least one fresh Linux environment outside the seed service path runs the verifier successfully against the primary public seed.
- The second public seed path is either verified at the current expected commit or explicitly marked as secondary/relay-backed with latest evidence.
- Public seed status is visible from docs and generated bundle/report output.
- The portable verification bundle includes the verifier, docs, latest evidence, and non-claims.
- CI passes on `main`.

## Autonomous Loop Sequence

The controller may execute these loops in order without asking for "continue" after each loop, as long as each loop stays inside the approved boundaries recorded in `fixtures/next-loop-controller.json`.

### Loop 77: Public Clone Surface Audit

**Goal:** Make the user-facing public clone path current and obvious.

**Actions:**

- Update `README.md`, `docs/community-quickstart.md`, `docs/first-decentralized-repo-milestone.md`, and `docs/radicle-retained-rid-quickstart.md` so they consistently point at the Loop 75 retained RID commit `d596024dac0d90605d4f103d567e5851771be5a8`.
- Add a compact seed status table: primary public seed, second public seed, expected commit, latest evidence files, and known non-claims.
- Keep the primary user command path direct-seed based; do not imply default public routing.

**Verification:**

- Unit tests for the docs/model expectations.
- `python scripts/forge_registry.py radicle-retained-quickstart`
- `python scripts/forge_registry.py verify-local --skip-npm-ci`

**Stop conditions:**

- Evidence index cannot identify the latest retained RID row.
- A doc edit would require claiming durability, security, default routing, or production readiness.

### Loop 78: First Public Clone Verifier Command

**Goal:** Give users one command that verifies the first decentralized repo clone path.

**Actions:**

- Add a `verify-first-public-clone` CLI surface that wraps `scripts/check_public_radicle_seed.py` with the current RID, seed, and expected commit from the evidence model.
- Emit JSON evidence plus a concise pass/fail text summary.
- Add tests proving the command is secret-free, bounded, and uses the latest evidence row.
- Include the command in the verification bundle suggested commands or quickstart output when appropriate.

**Verification:**

- Focused tests for default model selection and dry/plan behavior if live Radicle is unavailable.
- Full local verification suite.

**Stop conditions:**

- The command would need retained maintainer secret state.
- The command cannot run without starting a disposable reader node.

### Loop 79: Fresh Linux Public Clone Proof

**Goal:** Prove the public docs and verifier work from a fresh Linux reader environment.

**Actions:**

- Run the verifier from a fresh Linux environment against the primary public seed.
- Prefer `ubuntu-work` or a clean Linux container/VM with project-scoped temporary Radicle state.
- Record secret-free evidence under `evidence/`.
- If low-risk and available, also verify the second public seed path.

**Verification:**

- Evidence JSON validates and is imported into `fixtures/live-evidence-index.json`.
- Fresh clone HEAD equals the expected retained RID commit.
- Maintainer seed is not left running.

**Stop conditions:**

- Public seed is unreachable.
- Clone returns a stale commit.
- The check requires production/private personal keys, paid infrastructure, direct outreach, or broader claims.

### Loop 80: Product Surface RC Polish

**Goal:** Make the release candidate understandable without reading the whole evidence history.

**Actions:**

- Add a "First public clone RC" section to README and generated reports.
- Ensure `output/forge-app.html` or bundle report exposes the current Radicle seed status at a glance.
- Tighten `COMPLETION-CRITERIA.md` around what is complete for v0.1.0-alpha versus what remains future work.

**Verification:**

- Renderer/static artifact tests.
- Bundle report tests.
- Full local verification suite.

**Stop conditions:**

- UI/report text starts implying production readiness, security guarantees, durability, or censorship resistance.

### Loop 81: Release Candidate Package

**Goal:** Produce a shareable RC package from committed artifacts.

**Actions:**

- Refresh the portable verification bundle and release-note export.
- Add a release-candidate note or update `docs/public-update-drafts/` with exact commit, bundle SHA-256, seed addresses, verifier command, and non-claims.
- Push only after local verification and CI pass.

**Verification:**

- `verify-bundle`
- `verify-bundle-cleanroom`
- `report-bundle --json`
- GitHub Actions green on `main`.

**Stop conditions:**

- The working tree is dirty after regeneration.
- CI fails.
- Publishing would require unsupported claims or a GitHub Release/tag decision not already covered by the release-candidate plan.

### Loop 82: Availability Hardening Backlog

**Goal:** Identify the next most valuable post-RC hardening work without blocking the first usable product.

**Actions:**

- Draft the next evidence gates for independent provider/network availability, seed backup drill, stale-cache automatic refresh, external monitor visibility, and third-party clone rehearsal.
- Keep these as backlog gates unless the RC clone path is already passing.

**Verification:**

- Documentation/test updates only.

**Stop conditions:**

- The backlog work starts displacing the public clone RC path.

## Autonomy Rules

- Continue from one loop to the next when tests pass, CI passes after pushes, and no stop condition is hit.
- Commit and push at coherent loop boundaries.
- Prefer local tests before live checks.
- Use existing public seeds and project-scoped temporary reader state; do not provision paid services.
- Stop and ask before spending, wallet use, production/private personal keys, direct outreach, new persistent public services, or stronger durability/censorship/security/SLSA/production-readiness claims.
