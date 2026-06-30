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
- `output/<project-id>.radicle-genesis.json` as the planned next-gate evidence path
- `output/<project-id>.radicle-genesis.md` as the planned next-gate summary path
- refreshed `output/decentralized-forge-verification-bundle.zip`

The receipt JSON records the generated paths, copy/paste verification commands, and a project-specific Radicle genesis command.

## Current Boundary

`start-project` starts the project on the local forge surface. It does not create a Radicle RID, publish protocol events, start public seeds, sign releases, pin storage, spend money, use wallets, or contact services. The next decentralized step is a Linux/Radicle genesis gate that creates and records a project RID as bounded live evidence.

The bounded sample gate is:

```sh
python scripts/run_started_project_radicle_genesis.py
```

The current sample evidence is `evidence/radicle-start-project-genesis-2026-06-30.json`. It proves one fresh sample project completed `start-project`, received a disposable public Radicle RID, and was cloned/read back from a separate temporary Radicle profile. It is not a persistent seed, durability, routing, or production-readiness proof.

For your project, run the command recorded in `output/<project-id>.registry.start-project.json` under `radicle_next_gate.command`. It has this shape:

```sh
python scripts/run_started_project_radicle_genesis.py --repository ../my-project --project-id my-project --project-name "My Project" --output output/my-project.radicle-genesis.json --markdown output/my-project.radicle-genesis.md
```

The project-specific gate works from a temporary clone of your Git repository, then creates a disposable public Radicle RID and verifies a separate temporary-profile clone/readback for the committed project state. To run that gate immediately after `start-project`, add:

```sh
python scripts/forge_registry.py start-project ../my-project --project-id my-project --project-name "My Project" --run-radicle-genesis
```

When `--run-radicle-genesis` succeeds, the command updates `fixtures/<project-id>.registry.json` with `substrates.radicle.rid`, adds a Radicle clone URL, records a live-verified `registry.radicle_genesis_readback` state, refreshes the rendered project page/workbench, and rebuilds the verification bundle.

## Add First Collaboration Records

After a project exists, add local alpha issue and patch/PR-like records to the same registry:

```sh
python scripts/forge_registry.py add-issue fixtures/<project-id>.registry.json --title "Document first contributor task" --summary "Track the first project task."
python scripts/forge_registry.py add-patch fixtures/<project-id>.registry.json --title "Add first patch proposal" --summary "Describe the first proposed change."
```

Each command updates the registry, refreshes the project page/workbench, rebuilds the verification bundle, and records a local-only collaboration verification state. This is the usable local collaboration path; use the workbench Nostr draft or selected-relay replay gate when live decentralized issue/patch evidence is required.

## Verify

```sh
python scripts/forge_registry.py validate fixtures/<project-id>.registry.json
python scripts/forge_registry.py render fixtures/<project-id>.registry.json output/<project-id>.registry.html
python scripts/forge_registry.py verify-bundle output/decentralized-forge-verification-bundle.zip
python scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip
```

## Non-Claims

- This is not a hosted production forge.
- This is not a Radicle publication proof for your project until the Radicle genesis gate runs for that project.
- Local `add-issue` and `add-patch` records are not Nostr publishes, selected-relay readbacks, Radicle patch submissions, signatures, or hosted collaboration services.
- This is not durable storage, pinning, broad availability, censorship resistance, security, SLSA compliance, or production readiness.
