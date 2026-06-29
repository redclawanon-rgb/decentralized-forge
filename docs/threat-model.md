# Threat Model

Decentralized Forge is an evidence and publication-metadata tool for projects that want their knowledge to survive platform churn, link rot, and unilateral removal better than a single hosted page or repository can.

It is not a magic censorship-proof system. The project should earn trust by recording exactly what was verified, preserving the raw evidence, and refusing to upgrade narrow observations into broad guarantees.

## Assets

- Project registry metadata: project identity, maintainers, clone URLs, issues, patches, releases, and verification states.
- Release artifacts: file bytes, SHA-256 hashes, CID-compatible identifiers, CAR/CID evidence, local Helia add/get evidence, and optional future storage evidence.
- Collaboration records: NIP-34-shaped repository, issue, patch, and repository-state events.
- Provenance records: CI runs, artifact attestations, and registry-shaped import rows.
- Rendered reports: static HTML and summaries that a reader can inspect without running a service.

## Adversaries

- A centralized platform removes a repository, issue, release, or account.
- A gateway, relay, mirror, or public node withholds or drops content.
- A malicious publisher changes an artifact while keeping confusing metadata.
- A confused maintainer overstates what the evidence proves.
- A user mistakes a local fixture, dry-run event, selected-relay readback, or hosted attestation for a broad durability or security guarantee.

## Helps With

- Tamper evidence: artifact hashes and evidence-file hashes make silent mutation easier to detect.
- Link rot: multiple transport hints and static reports give readers more than one path to inspect project state.
- Platform removal: registry and evidence files can be copied, mirrored, rendered, and verified outside a single forge.
- Claim discipline: verification states and non-claims keep local, synthetic, selected-relay, public-gateway, and hosted-attestation evidence separate.
- Reproducibility: CI and local commands can regenerate summaries and static reports from committed fixtures.

## Does Not Yet Solve

- Global network blocking or country-scale censorship.
- Durable IPFS/Filecoin/Arweave persistence.
- Broad Radicle network availability.
- Nostr relay durability, global propagation, or Sybil resistance.
- Maintainer identity trust beyond recorded identifiers and signatures/attestations that are explicitly verified.
- Malicious content moderation, takedown response, abuse handling, or legal process.
- Production supply-chain security or SLSA compliance.

## Trust Rules

1. A claim is valid only when a committed evidence row states that exact scope.
2. A transport observation is not a durability guarantee.
3. A selected relay readback is not global propagation.
4. A public gateway timeout is still useful evidence, but it is not proof that the CID is unavailable everywhere.
5. A hosted keyless attestation proves the hosted workflow produced an attestation for the listed subjects; it is not a general supply-chain security guarantee.
6. Disposable keys are acceptable for protocol testing; production/private personal keys are not used by default.
7. Paid storage, wallets, direct outreach, persistent public seed services, and stronger security/censorship claims require separate explicit approval and evidence.

## Near-Term Hardening Priorities

- Keep evidence rows hash-linked to their source files.
- Add importer commands that create verification bundles from external projects.
- Add deterministic bundle export for registry JSON, evidence files, summaries, and rendered reports.
- Add optional transport adapters without changing the claim model.
- Build public verification instructions that assume no prior trust in the original host.
