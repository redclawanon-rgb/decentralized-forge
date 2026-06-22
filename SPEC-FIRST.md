# Spec First: Decentralized Forge MVP

## Goal

Create a GitHub-like decentralized forge MVP that proves a project can exist, be discovered, be cloned, receive issues/patches, and publish releases without GitHub as the authority.

## MVP user stories

### Maintainer

- As a maintainer, I can import an existing Git repo.
- As a maintainer, I can publish a signed/structured project identity.
- As a maintainer, I can list multiple clone/mirror URLs.
- As a maintainer, I can receive and respond to issues.
- As a maintainer, I can receive patch/PR proposals.
- As a maintainer, I can publish signed release metadata with artifact hashes.

### Contributor

- As a contributor, I can discover the canonical project identity without a GitHub account.
- As a contributor, I can clone the project from at least one available mirror.
- As a contributor, I can open an issue.
- As a contributor, I can comment on an issue.
- As a contributor, I can submit a patch or PR-like proposal.

### Reader/user

- As a reader, I can view README, clone instructions, maintainers, latest release, and active issues in a familiar web UI.

## MVP features

- Project registry object
- Repo browser backed by Git clone/mirror
- Issue list/detail/create/comment/close
- Patch/PR list/detail/comment/status
- Release metadata with signed tag/hash and optional IPFS CID
- Local static/demo UI

## Explicit non-goals

- Private repos
- Paid hosting
- Full CI/CD system
- Full package registry
- Full GitHub org/team model
- Global code search
- Public protocol publishing without approval

## Minimum proof

The MVP works when all of these are true locally:

1. A sample repo has a signed/structured project registry object.
2. The project page renders from the registry plus Git metadata.
3. An issue object can be created/listed/rendered.
4. A patch/PR object can be created/listed/rendered.
5. Release metadata includes verifiable hashes/signature placeholders.
6. The docs explain which decentralized substrate each object could publish to.

## Loop 2 acceptance criteria: registry and static project page

The next local prototype is accepted only when all criteria below pass without network, private keys, paid services, or public publishing.

### Registry schema

- `schemas/project-registry.schema.json` exists and is valid JSON.
- The schema declares a stable object type such as `decentralized-forge.project-registry.v1`.
- Required fields include:
  - `schema_version`
  - `project.id`
  - `project.name`
  - `project.description`
  - `project.default_branch`
  - at least one `maintainers[]` item
  - at least one `clone_urls[]` item
  - `created_at`
  - `updated_at`
- Maintainer entries include an identifier type (`nostr`, `radicle`, `did`, `ssh`, or `other`) and a public identifier string.
- Clone URL entries include a transport type (`git`, `https`, `ssh`, `radicle`, `nostr`, or `other`) and URL.
- Release entries can include artifact hashes, optional CID/URI, and signature/attestation placeholders.

### Fixture

- `fixtures/example-project.registry.json` exists and is valid JSON.
- The fixture validates against the repository's own stdlib validation test.
- The fixture includes at least:
  - one local clone URL,
  - one maintainer,
  - one issue summary,
  - one patch/PR summary,
  - one release with a SHA-256 hash placeholder or real hash,
  - substrate hints for NIP-34, Radicle, ForgeFed, IPFS, and Sigstore/SLSA.

### Renderer

- `scripts/render_project_page.py` uses Python standard library only.
- It accepts an input registry path and output path.
- It renders a deterministic `output/demo-project.html` or `output/demo-project.md`.
- The rendered page includes project name, description, maintainers, clone URLs, release metadata, issue summaries, patch summaries, and protocol/substrate hints.
- It fails with a non-zero exit code and clear message for invalid/missing required fields.

### Tests and verification

- `tests/test_registry_fixture.py` uses stdlib `unittest` only.
- Tests check JSON parsing, required fields, fixture/schema alignment for the MVP subset, and renderer output.
- Verification commands pass locally:
  - `python3 -m unittest discover -s tests`
  - `python3 scripts/render_project_page.py fixtures/example-project.registry.json output/demo-project.html`
  - `git status --short`

## Loop 3 dry-run acceptance criteria: NIP-34 fixtures

- `docs/nip34-event-shapes.md` documents local-only repository announcement and related event shape mapping.
- `fixtures/nostr-repo-announcement.json` contains a valid unsigned/synthetic NIP-34-style `kind: 30617` event body fixture.
- No event is signed with a private key.
- No event is published to public relays.
- The fixture maps cleanly back to the project registry's project id, name, clone URLs, maintainers, and relay hints.
