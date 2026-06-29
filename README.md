# Decentralized Forge

A research and prototype project for a GitHub-class decentralized forge.

## One-line thesis

Build a normal-feeling GitHub alternative whose authority is decentralized across Git, cryptographic identity, P2P/federated collaboration protocols, durable artifact storage, and signed build/release attestations.

## Starting question

Can modern decentralized protocols be combined to recreate GitHub's core features without central platform censorship?

## Initial scope

This repo starts as a research/spec/prototype workspace. The first milestone is not a production forge; it is a proof that a project can be:

- announced without GitHub,
- discovered without GitHub,
- cloned from one or more mirrors,
- discussed through decentralized issues,
- proposed against through decentralized patches/PRs,
- released with structured metadata, artifact hashes, and eventual signed attestations once verified.

## Current status

This repository is a **local registry/static renderer prototype** with a generated static workbench app, protocol-mapping fixtures, a first project-scoped Radicle repository smoke, fresh-state Radicle readback, update-continuity evidence, a retained project-scoped Radicle maintainer lane, retained same-RID update evidence, and narrow, evidence-backed live checks. It is public for collaboration, but it is not a production forge and does not claim durable storage, broad protocol availability, censorship resistance, security guarantees, or production readiness.

As of Loop 67, the project has local CAR/CID fixture verification, local Helia UnixFS/IPFS add-get evidence for the same fixture bytes, a bounded public gateway/pinning preflight, selected-relay Nostr repository-announcement plus issue/patch readback evidence, one disposable Radicle local/private replay, one disposable public Radicle seed/remote-clone smoke, a project-scoped Radicle repo smoke for commit `fd3f1898d81a4b00be9095c62e3c07fc1a792a95` at RID `rad:zWGy1Ssjb7tBbwDbdGLqeHCsUqwr`, a fresh temporary-profile Radicle clone/readback of that same RID and commit without reusing the original Loop 59 seed profile, a fresh-peer same-RID push of current commit `00404656bcb17ad1aab241fb0ab0dd60487d9699` whose default clone still read back the original delegate commit, a retained project-scoped Radicle maintainer lane at RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`, retained same-RID update evidence, an evidence-derived retained RID community direct-seed quickstart, an independent follower-seed readback of commit `7262f69b82e442263d6261414f6b771be04c6b6f`, a retained-seed restart/readback rehearsal of commit `4c8cd6183e2e12d1c62af7d2f013fb085b2d6bf8`, and a public VPS follower-seed readback of current commit `610fc3da9757d0cb123aa5976db552b991b766d4`. It also has hosted GitHub keyless artifact attestation evidence, a separate registry-shaped keyless-attestation import, evidence hash hardening, a local static workbench app, a deterministic portable verification bundle, a clean-room bundle consumer check, a bundle import/report command, a portable bundle review checklist, a release-note export for bundle handoff, and local registry import scaffolding. Those checks are deliberately scoped to the exact evidence files in this repo.

| Area | Current state | Not claimed |
|---|---|---|
| Registry/UI | Local JSON schema, fixtures, stdlib renderer, generated demo HTML, generated static workbench app, deterministic verification bundle | Production forge, hosted service, signed authority |
| Nostr NIP-34 | Dry-run repository/issue/patch/state fixtures, local stdlib parser/conformance checks, imported Loop 25 selected-relay repository-announcement readback, and Loop 43 disposable issue/patch selected-relay readback | Durability, global propagation, identity trust, full NIP-34/forge compatibility |
| Radicle | Source-inspected mapping, disposable local/private CLI replay evidence, one disposable public seed/remote-clone smoke for exact RID `rad:z2WtozFrCRhygh9CGzyUN57CN7Nwa`, current-host route probes, a project-scoped Radicle repo smoke for RID `rad:zWGy1Ssjb7tBbwDbdGLqeHCsUqwr`, one fresh temporary-profile readback of that RID at commit `fd3f1898d81a4b00be9095c62e3c07fc1a792a95`, one fresh-peer push of current commit `00404656bcb17ad1aab241fb0ab0dd60487d9699` where default readback remained on the original delegate branch, a retained project-scoped maintainer RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`, retained same-RID update evidence through commit `f800bae387f33452fdeb79ecf5c795d25f7246ac`, independent follower-seed readback of commit `7262f69b82e442263d6261414f6b771be04c6b6f`, retained-seed restart/readback rehearsal of commit `4c8cd6183e2e12d1c62af7d2f013fb085b2d6bf8`, public VPS follower-seed readback of current commit `610fc3da9757d0cb123aa5976db552b991b766d4`, and a read-only retained RID quickstart command | Permanent durability, future default public-routing availability, broad Radicle network availability, identity trust, production readiness |
| Artifacts | Local SHA-256, CIDv1 raw/base32-compatible metadata, lockfile-backed local CAR/CID readback evidence, project-scoped Helia local add/get readback evidence, and public gateway preflight with zero matching gateway readbacks observed | Public gateway availability, pinning, paid storage, Filecoin/Arweave durability |
| CI/provenance | GitHub Actions runs the local verification suite and generated keyless artifact attestation evidence in Loop 40; Loop 45 imports that evidence into a separate registry-shaped file | Registry fixture provenance replacement, SLSA compliance, supply-chain security guarantee |
| Verification labels | Top-level and NIP-34 adapter `verification_states[]` records identify local fixtures, source-inspected mappings, synthetic fixtures, live-unverified scopes, and narrow live-verified evidence, with rendered counts and claim-boundary summaries | Implicit trust, unsupported scope expansion, censorship-proof/durability/security guarantees |
| Live replay gates | Safe replay checklist advanced through Loop 35; standing approval covers free, disposable/project-scoped, low-volume, evidence-labeled live follow-up, including Loops 41-45 | Unbounded live testing, paid services, production/private personal keys, stronger unsupported claims |
| Public collaboration | GitHub issues/discussions for temporary coordination | Decentralized issue/patch federation running in production |

## Docs

- `.hermes/context.md` — durable project brain for agents
- `STATUS.md` — current loop, gates, and next actions
- `COMPLETION-CRITERIA.md` — Milestone 1 definition of done, verification commands, and gated completion lanes
- `RESEARCH.md` — source-grounded protocol research
- `PROTOCOL-MATRIX.md` — protocol fit/maturity comparison plus next-step decision matrix
- `SPEC-FIRST.md` — MVP product/specification
- `ARCHITECTURE.md` — proposed architecture, verification-state boundaries, and implementation decision matrix
- `AGENT-LOOPS.md` — autonomous loop definitions for overnight work
- `docs/nip34-event-shapes.md` — NIP-34 dry-run event shape notes
- `docs/radicle-mapping.md` — source-inspected Radicle-to-registry mapping, clearly marked not live-CLI verified
- `docs/artifact-metadata.md` — Loop 6 release artifact metadata, local CID fixture, and no-pinning/no-durability boundaries
- `docs/ci-provenance-model.md` — synthetic local CI/provenance model plus hosted keyless attestation boundary
- `docs/public-collaboration.md` — Loop 9 public collaboration stance, first issue set, and public update draft
- `docs/threat-model.md` — public threat model, what the prototype helps with, and explicit non-goals
- `docs/community-quickstart.md` — current community verification workflow and portable bundle review path
- `docs/radicle-persistent-seed-plan.md` — Loop 66-informed minimum service plan for a future persistent retained-RID seed
- `docs/radicle-retained-rid-quickstart.md` — retained Radicle RID direct-seed clone recipe derived from the strongest retained-RID evidence
- `docs/portable-bundle-review-checklist.md` — maintainer checklist for reviewing and describing the portable verification bundle without overclaiming
- `docs/live-adapter-replay-plan.md` — Loop 20 safe live-gated Radicle/Nostr replay prerequisites, evidence checklist, rollback, and non-claim gates
- `docs/live-completion-gates.md` — optional post-Milestone-1 live IPFS, Nostr, Radicle, and signing gates
- `docs/autonomy/README.md` — approval-bounded next-loop controller usage and automation limits
- `ROADMAP.md` — public prototype roadmap, verification-state labels, and collaboration tracks
- `schemas/project-registry.schema.json` — MVP project registry schema
- `fixtures/example-project.registry.json` — local-only demo project registry fixture
- `fixtures/portable-lab.registry.json` — second local-only registry fixture for non-demo CLI/export coverage
- `fixtures/onboarding-sample.registry.json` — committed output from the local onboarding command, generated from this repository with local-only artifact metadata
- `fixtures/onboarding-sample-artifact.txt` — local-only artifact used by the onboarding sample
- `fixtures/live-adapter-replay-checklist.json` — secret-free replay gate/checklist state advanced through Loop 35
- `fixtures/live-evidence-index.json` — secret-free index of Radicle, Nostr, IPFS/gateway, GitHub keyless attestation, local Helia, and registry-shaped import evidence plus explicit non-claims
- `schemas/live-evidence-index.schema.json` — live evidence index schema contract
- `evidence/github-keyless-attestation-2026-06-28.json` — Loop 40 hosted keyless artifact attestation evidence from GitHub Actions
- `evidence/helia-local-ipfs-add-get-2026-06-28.json` — Loop 41 project-scoped local Helia UnixFS/IPFS add-get evidence for the release artifact fixture
- `evidence/public-gateway-pinning-preflight-2026-06-28.json` — Loop 42 public gateway/pinning preflight with zero matching gateway readbacks and no pinning action
- `evidence/nostr-loop43-issue-patch-readback-2026-06-28.json` — Loop 43 disposable Nostr issue/patch selected-relay readback evidence
- `evidence/radicle-loop44-broader-check-2026-06-28.json` — Loop 44 current-host Radicle route probe and `rad` CLI blocker evidence
- `evidence/radicle-project-repo-smoke-2026-06-29.json` and `.md` — Loop 59 project-scoped Radicle repo smoke for RID `rad:zWGy1Ssjb7tBbwDbdGLqeHCsUqwr`
- `evidence/radicle-fresh-readback-check-2026-06-29.json` and `.md` — Loop 60 fresh temporary-profile Radicle readback check for RID `rad:zWGy1Ssjb7tBbwDbdGLqeHCsUqwr`
- `evidence/radicle-update-continuity-check-2026-06-29.json` and `.md` — Loop 61 same-RID update-continuity check showing fresh-peer publication but default readback still on the original delegate commit
- `evidence/radicle-retained-delegate-check-2026-06-29.json` and `.md` — Loop 62 retained project-scoped Radicle maintainer lane with fresh default and direct-seed readback of RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy`
- `evidence/radicle-retained-update-check-2026-06-29.json` and `.md` — Loop 63 retained same-RID update check advancing RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` to commit `f800bae387f33452fdeb79ecf5c795d25f7246ac` with direct-seed readback
- `evidence/radicle-independent-availability-check-2026-06-29.json` and `.md` — Loop 65 retained RID update to commit `7262f69b82e442263d6261414f6b771be04c6b6f` with independent follower-seed readback
- `evidence/radicle-seed-restart-check-2026-06-29.json` and `.md` — Loop 66 retained seed restart/readback rehearsal advancing RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` to commit `4c8cd6183e2e12d1c62af7d2f013fb085b2d6bf8`
- `evidence/radicle-vps-follower-public-readback-2026-06-29.json` and `.md` — Loop 67 public VPS follower-seed readback for retained RID `rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy` at commit `610fc3da9757d0cb123aa5976db552b991b766d4`
- `evidence/radicle-vps-follower-systemd-service-2026-06-29.json` and `.md` — Loop 68 enabled user-level `systemd` service for the public `openclaw` follower seed with post-restart readback
- `evidence/radicle-public-seed-health-check-2026-06-29.json` and `.md` — Loop 69 repeatable fresh-profile health check for the public Radicle seed
- `evidence/radicle-public-seed-update-propagation-2026-06-29.json` and `.md` — Loop 70 retained RID update propagation through the public `openclaw` follower seed to commit `64efbada294d4a57c014a27398b92e344c6d68aa`
- `docs/first-decentralized-repo-milestone.md` — first usable public Radicle direct-seed clone milestone and non-claims
- `fixtures/keyless-attestation.registry-verification.json` — Loop 45 registry-shaped keyless-attestation import kept outside project-registry fixtures
- `fixtures/local-release-artifact.txt` — local-only release artifact fixture with stdlib-tested SHA-256/CIDv1 metadata
- `fixtures/nostr-repo-state-status.json` — local-only `kind: 30618` repository state fixture generated from the recorded local Git HEAD at fixture creation time plus fixture-only synthetic status/check projections
- `fixtures/radicle-backed-project.registry.json` — synthetic local-only Radicle-backed registry fixture
- `scripts/nip34_adapter.py` — stdlib parser/export helper that round-trips dry-run NIP-34 repository, issue, patch, repository state, fixture-only status/check data, and local NIP-01 conformance metadata back to registry-shaped concepts without relay publishing
- `scripts/render_project_page.py` — stdlib renderer for static project pages, including verification-state labels, artifact availability, content-address, CI/provenance, substrate detail sections, optional local NIP-34 fixture adapter import/display, and optional live-evidence index display
- `scripts/render_forge_app.py` — stdlib generator for `output/forge-app.html`, a local static workbench over registry fixtures, evidence rows, selected-relay Nostr readback, and unsigned local Nostr issue/patch drafts
- `scripts/preflight_static_artifact.py` — stdlib preflight for generated static artifact freshness, expected local/synthetic boundary sections, optional NIP-34 fixture sections, optional live evidence index, and selected unsupported claim phrases
- `scripts/forge_registry.py` — reusable local CLI for local registry scaffolding, validation, rendering, workbench app generation, summaries, evidence-index hash checks, portable verification bundle export/verification/reporting/release-note export, retained Radicle quickstart output, and read-only doctor output
- `scripts/run_radicle_fresh_readback_check.py` — Docker/Linux-oriented fresh-state Radicle readback check for the recorded project RID without reusing the original seed profile
- `scripts/run_radicle_independent_availability_check.py` — host/WSL-oriented retained RID update plus independent follower-seed readback check
- `scripts/run_radicle_project_repo_smoke.py` — Docker/Linux-oriented bounded Radicle smoke that initializes the current checkout as a public Radicle repo from temporary state and records separate-profile clone/readback evidence
- `scripts/run_radicle_retained_delegate_check.py` — Docker/Linux-oriented retained-maintainer workflow that keeps project-scoped Radicle state under gitignored `.tmp/` and records fresh readback evidence without committing secrets
- `scripts/run_radicle_retained_update_check.py` — host/WSL-oriented retained same-RID update check that reuses local retained Radicle state without Docker
- `scripts/run_radicle_seed_restart_check.py` — host/WSL-oriented retained seed restart/readback rehearsal
- `scripts/install_radicle_user_seed_service.py` — Linux host helper for installing a user-level `systemd` Radicle follower seed service without printing secrets
- `scripts/check_public_radicle_seed.py` — fresh-profile public Radicle seed clone/readback health check
- `scripts/radicle_seed_host_control.py` — Linux host helper for starting/stopping a Radicle seed profile from a local passphrase file without printing secrets
- `scripts/run_radicle_update_continuity_check.py` — Docker/Linux-oriented same-RID update-continuity check for fresh-peer publication versus default delegate readback
- `output/demo-project.html` — generated demo project page
- `output/forge-app.html` — generated local static workbench app; it reads embedded committed fixture/evidence data and does not sign, fetch, open WebSockets, or publish protocol events
- `output/forge-app-with-onboarding-sample.html` — optional generated workbench app with the committed onboarding sample imported via `render-app --registry`
- `output/portable-lab.html` — generated second-fixture project page
- `output/onboarding-sample.registry.html` — generated committed onboarding sample page
- `output/*.summary.json` — deterministic machine-readable registry summaries
- `output/onboarding-sample.bundle-report.json` — committed JSON bundle report generated after the onboarding sample refresh
- `output/decentralized-forge-verification-bundle.zip` — deterministic portable bundle containing fixtures, schemas, source evidence, generated outputs, verifier scripts, and `verification-bundle.manifest.json`
- `tests/test_registry_fixture.py` — stdlib verification tests for the registry fixture and renderer

## Local prototype usage and verification

Regenerate the public demo artifact with every local fixture section enabled:

```sh
python3 scripts/render_project_page.py fixtures/example-project.registry.json output/demo-project.html \
  --nip34-repo-fixture fixtures/nostr-repo-announcement.json \
  --nip34-collaboration-fixture fixtures/nostr-collaboration-events.json \
  --nip34-state-status-fixture fixtures/nostr-repo-state-status.json \
  --live-evidence-index fixtures/live-evidence-index.json
```

Open the generated artifact locally in a browser:

```sh
python3 -m webbrowser output/demo-project.html
```

Regenerate and open the local static forge workbench:

```sh
python3 scripts/forge_registry.py render-app output/forge-app.html
python3 -m webbrowser output/forge-app.html
```

Render the same workbench with the committed onboarding sample imported:

```sh
python3 scripts/forge_registry.py render-app output/forge-app-with-onboarding-sample.html --registry fixtures/example-project.registry.json --registry fixtures/portable-lab.registry.json --registry fixtures/onboarding-sample.registry.json
python3 -m webbrowser output/forge-app-with-onboarding-sample.html
```

The workbench is a static local app over committed fixtures/evidence. Its Nostr draft screen creates unsigned local JSON only; it does not sign events, import private keys, fetch from relays, open WebSockets, or publish.
The Project set screen lists the embedded registry sources and output path, and shows a copyable `render-app --registry ...` command for recreating the current workbench.

Scaffold a starter registry fixture from a local Git worktree:

```sh
python3 scripts/forge_registry.py onboard-local-project ../some-local-repo path/to/artifact --project-id some-local-repo --version 0.1.0-local --tag v0.1.0-local
python3 scripts/forge_registry.py scaffold-registry ../some-local-repo fixtures/some-local-repo.registry.json
python3 scripts/forge_registry.py attach-local-artifact fixtures/some-local-repo.registry.json path/to/artifact --version 0.1.0-local --tag v0.1.0-local
python3 scripts/forge_registry.py validate fixtures/some-local-repo.registry.json
```

The onboarding command chains scaffold, local artifact attachment, validation, summary export, HTML rendering, and bundle/report refresh. The scaffold command reads local Git metadata only. It writes an unsigned local fixture with placeholder maintainer identity, file-based clone URL, absent artifact/provenance claims, and explicit non-claims. The local artifact attach command records exact file SHA-256, byte size, media type, `file://` URI, and local-only availability while preserving no-IPFS, no-pinning, no-signing, no-paid-storage, and no-durability boundaries. Review and replace the placeholder identity, then add protocol evidence only after it is separately verified.

Regenerate and verify the portable verification bundle:

```sh
python3 scripts/forge_registry.py export-bundle output/decentralized-forge-verification-bundle.zip
python3 scripts/forge_registry.py verify-bundle output/decentralized-forge-verification-bundle.zip
python3 scripts/forge_registry.py verify-bundle-cleanroom output/decentralized-forge-verification-bundle.zip
python3 scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip
python3 scripts/forge_registry.py export-bundle-release-note output/decentralized-forge-verification-bundle.zip
```

The bundle is deterministic and includes a manifest with payload sizes, SHA-256 hashes, evidence-index bindings, suggested verification commands, explicit non-claims, and the portable bundle review checklist. The clean-room verifier extracts the bundle to a temporary directory, copies the bundle into that extracted tree, and runs bundled checks from there rather than from the original checkout. The report command reads either the ZIP or an extracted bundle directory and summarizes project identity, evidence rows, non-claims, verification gaps, and suggested commands. The release-note export combines the bundle report, exact current commit SHA, bundle digest, checklist stop conditions, and non-claims into markdown for handoff. It is not a release-signing, durability, availability, security, or production-readiness proof.

Run the static artifact preflight before release-oriented edits, screenshots, pushes, or public updates:

```sh
python3 scripts/preflight_static_artifact.py
```

The preflight is stdlib-only. It checks that `output/demo-project.html` exists, is byte-for-byte current with the renderer plus all optional NIP-34 fixtures and the current live evidence index, includes expected local/synthetic/non-claim sections, includes the optional NIP-34 fixture adapter/state/status/conformance sections, includes the live evidence index section, and omits selected unsupported live-protocol/security/durability claim phrases.

Run read-only local readiness and evidence-index integrity checks:

```sh
npm run forge:doctor
npm run verify:evidence-index
```

The live evidence index records each source evidence file's canonical LF-normalized SHA-256 and byte size, so Windows and Linux checkouts verify the same committed evidence. Refresh those fields only after intentionally updating evidence files:

```sh
npm run refresh:evidence-hashes
```

Run the full local verification suite:

```sh
python3 -m json.tool schemas/project-registry.schema.json
python3 -m json.tool schemas/live-evidence-index.schema.json
python3 -m json.tool fixtures/example-project.registry.json
python3 -m json.tool fixtures/portable-lab.registry.json
python3 -m json.tool fixtures/radicle-backed-project.registry.json
python3 -m json.tool fixtures/onboarding-sample.registry.json
python3 -m json.tool fixtures/nostr-repo-announcement.json
python3 -m json.tool fixtures/nostr-collaboration-events.json
python3 -m json.tool fixtures/nostr-repo-state-status.json
python3 -m json.tool fixtures/live-adapter-replay-checklist.json
python3 -m json.tool fixtures/live-evidence-index.json
python3 -m json.tool fixtures/keyless-attestation.registry-verification.json
python3 scripts/nip34_adapter.py fixtures/nostr-repo-announcement.json fixtures/nostr-collaboration-events.json fixtures/nostr-repo-state-status.json
python3 scripts/preflight_static_artifact.py
python3 scripts/forge_registry.py validate-evidence-index fixtures/live-evidence-index.json
python3 scripts/forge_registry.py refresh-evidence-hashes fixtures/live-evidence-index.json --check
python3 scripts/forge_registry.py doctor --json
python3 scripts/forge_registry.py validate fixtures/example-project.registry.json fixtures/portable-lab.registry.json fixtures/onboarding-sample.registry.json
python3 scripts/forge_registry.py render fixtures/portable-lab.registry.json output/portable-lab.html
python3 scripts/forge_registry.py render-app output/forge-app.html
python3 scripts/forge_registry.py render-app output/forge-app-with-onboarding-sample.html --registry fixtures/example-project.registry.json --registry fixtures/portable-lab.registry.json --registry fixtures/onboarding-sample.registry.json
python3 scripts/forge_registry.py export-summary fixtures/example-project.registry.json output/demo-project.summary.json
python3 scripts/forge_registry.py export-summary fixtures/portable-lab.registry.json output/portable-lab.summary.json
python3 scripts/forge_registry.py export-bundle output/decentralized-forge-verification-bundle.zip
python3 scripts/forge_registry.py verify-bundle output/decentralized-forge-verification-bundle.zip
python3 scripts/forge_registry.py verify-bundle-cleanroom output/decentralized-forge-verification-bundle.zip
python3 scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip --json
python3 scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip --json --output output/onboarding-sample.bundle-report.json
python3 scripts/forge_registry.py export-bundle-release-note output/decentralized-forge-verification-bundle.zip
python3 scripts/forge_registry.py radicle-retained-quickstart
python3 scripts/live_gate_inventory.py
python3 -m unittest discover -s tests
npm run verify:car-cid
npm run verify:helia
```

To continue safe housekeeping without re-deciding the same next step each time:

```sh
npm run next:loop
```

This writes `docs/autonomy/next-loop-report.md` after running the safe verifier. The matching manual GitHub Actions workflow is `next-loop-controller`; it runs the same controller in check mode and does not commit, push, publish, sign, spend, or perform live protocol actions.

The prototype is evidence-scoped: it does not run a public federation actor, spend money, use production/private personal keys, or claim production readiness. Top-level `verification_states[]` records make each scope's evidence and claim boundary explicit. CI/provenance fields and renderer sections remain synthetic/local display data unless separately verified. The NIP-34 adapter parses local dry-run fixtures and separately imports recorded selected-relay readback evidence; rendering and tests do not publish relay events. Release artifact metadata includes local hashes, CID-compatible identifiers, a local CAR/CID readback fixture, a local Helia add/get readback fixture, and a public gateway preflight that observed no successful readback; it is not pinned, uploaded to paid storage, wallet-backed, paid-storage-backed, or durable-storage verified.

The renderer summarizes both registry-level and adapter-level verification rows: total row counts, live-verified false/true counts, synthetic false/true counts, state chips, grouped rows by state, and claim-boundary summaries. It also displays a concise conformance summary without dumping full serialized event payloads by default. Further public gateway checks, pinning, paid storage, broader/repeated Radicle public-network testing, or stronger durability/censorship/security/production claims require separate evidence and approval.
