# Start Project Quickstart

This is the first user-facing path for starting a project on the current decentralized-forge alpha surface.

## One Command

From this repository, point at any local Git worktree:

```sh
python scripts/forge_registry.py start-project ../my-project --project-id my-project --project-name "My Project"
```

If the target repository has a `README.md`, that file is used as the first local artifact by default. To attach a specific artifact:

```sh
python scripts/forge_registry.py start-project ../my-project --artifact ../my-project/dist/my-project.tar.gz --project-id my-project --version 0.1.0-local --tag v0.1.0-local
```

## Outputs

The command writes:

- `fixtures/<project-id>.registry.json`
- `output/<project-id>.registry.summary.json`
- `output/<project-id>.registry.html`
- `output/<project-id>.registry.forge-app.html`
- `output/<project-id>.registry.start-project.json`
- refreshed `output/decentralized-forge-verification-bundle.zip`

The receipt JSON records the generated paths, copy/paste verification commands, and the next Radicle gate.

## Current Boundary

`start-project` starts the project on the local forge surface. It does not create a Radicle RID, publish protocol events, start public seeds, sign releases, pin storage, spend money, use wallets, or contact services. The next decentralized step is a Linux/Radicle genesis gate that creates and records a project RID as bounded live evidence.

## Verify

```sh
python scripts/forge_registry.py validate fixtures/<project-id>.registry.json
python scripts/forge_registry.py render fixtures/<project-id>.registry.json output/<project-id>.registry.html
python scripts/forge_registry.py verify-bundle output/decentralized-forge-verification-bundle.zip
python scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip
```

## Non-Claims

- This is not a hosted production forge.
- This is not a Radicle publication proof until the Radicle genesis gate runs.
- This is not durable storage, pinning, broad availability, censorship resistance, security, SLSA compliance, or production readiness.
