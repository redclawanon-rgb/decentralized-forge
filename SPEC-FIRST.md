# Spec First: Decentralized Forge MVP

## Goal

Create a GitHub-like decentralized forge MVP that proves a project can exist, be discovered, be cloned, receive issues/patches, and publish releases without GitHub as the authority.

## MVP user stories

### Maintainer

- As a maintainer, I can import an existing Git repo.
- As a maintainer, I can publish a signed project identity.
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
