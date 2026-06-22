# Radicle local integration mapping

Loop 4 maps Radicle's project, identity, issue, and patch concepts into `schemas/project-registry.schema.json` without installing the live CLI or publishing anything.

## Scope and verification status

- Status: **source-inspected local spike**.
- Live Radicle CLI verification: **not performed**. `rad` was not installed in this environment, and the unsafe `curl https://radicle.dev/install | sh` path was explicitly not used.
- Source evidence: official `radicle-heartwood` source cloned read-only at `/tmp/radicle-heartwood`, commit `90aaec1c9eee77a0beebece48f460c1424c1c8bd` (`CONTRIBUTING: Add section on issue labels`, 2026-06-01).
- No public publishing, account creation, production keys, or paid services were used.

## Source-inspected Radicle concepts

From `/tmp/radicle-heartwood/README.md`:

- Heartwood is a peer-to-peer code collaboration and publishing stack with a `rad` CLI and `radicle-node` network daemon.
- Binary installation is documented as `curl -sSf https://radicle.dev/install | sh`; this spike did **not** run that command.
- Source installation is documented with `cargo install --path ... --root ~/.radicle`; this spike did **not** perform an install.

From `/tmp/radicle-heartwood/rad.1.adoc`:

- `rad auth` creates a local cryptographic profile and DID under a Radicle home, defaulting to `~/.radicle`.
- `rad clone <rid>` clones by Repository Identifier (RID). RIDs are described as globally unique URNs identifying repositories on Radicle.
- `rad init` publishes an existing Git repository to local Radicle storage and creates a `rad` remote; replication by other nodes depends on network connections and tracking/trust policy.
- `rad .` displays the Repository ID from a repository root.
- `rad inspect --payload` shows the identity payload containing name, description, and default branch.

From `/tmp/radicle-heartwood/rad-id.1.adoc`:

- Each repository has an identity document containing metadata such as repository name, description, and delegates.
- The identity document is stored as Canonical JSON.
- Identity changes are versioned and require signatures by a quorum of delegates.
- `rad id update` can change delegates, threshold, visibility, access, and payload fields such as `xyz.radicle.project` name/description and `xyz.radicle.crefs` canonical reference rules.

From `/tmp/radicle-heartwood/crates/radicle-cli/examples/rad-issue.md` and `rad-issue-list.md`:

- `rad issue open --title ... --description ... --no-announce` creates an issue with an ID, author, and open status.
- `rad issue list` displays issue ID, title, author, labels, assignees, and opened time.
- `rad issue show <id>` displays issue details and comments.
- `rad issue assign`, `rad issue label`, `rad issue comment`, and `rad issue state --solved` support assignment, labels, comments, and closing/solving.

From `/tmp/radicle-heartwood/rad-patch.1.adoc`:

- `rad patch` manages changesets inside Radicle repositories.
- Opening a patch is normally done by pushing to `refs/patches` on the `rad` remote: `git push rad HEAD:refs/patches`.
- Patch state includes open, merged, archived, and draft list filters.
- `rad patch review`, `rad patch comment`, `rad patch checkout`, `rad patch set`, and `rad patch ready` support review, comments, branch checkout, upstream association, and draft/open transitions.
- Merging is performed with normal Git merge followed by `git push rad`, after which Radicle reports the patch merged.

## Mapping to `project-registry.schema.json`

| Registry field | Radicle source concept | Mapping rule for fixtures/prototypes |
| --- | --- | --- |
| `project.id` | RID from `rad .` or `rad init` output | Use the RID as the stable decentralized ID when the registry entry is Radicle-primary. For local-only synthetic fixtures, use a clearly fake `rad:z...` value and mark it unverified. |
| `project.name` | `xyz.radicle.project.name` identity payload | Copy from identity payload when available. |
| `project.description` | `xyz.radicle.project.description` identity payload | Copy from identity payload when available. |
| `project.default_branch` | identity payload default branch / canonical refs | Copy the default branch from identity payload or local Git config. Represent stricter canonical reference policy under `substrates.radicle.identity_payload.canonical_refs`. |
| `maintainers[]` | repository delegates | Represent each delegate as `id_type: "radicle"` with `public_id` set to its DID (`did:key:...`) or peer identity. Use `role: "delegate"` or similar. |
| `clone_urls[]` | RID and `rad` remote | Add a `transport: "radicle"` entry with `url` equal to the RID or `rad://...` remote URL if captured locally. Keep `git`, `https`, or `ssh` mirrors as additional clone options if present. |
| `issues[]` | Radicle issue COBs | Map issue ID/title/status/author/summary. Radicle `open` maps to registry `open`; Radicle solved/closed maps to registry `closed`. Preserve labels/assignees/comments under `substrates.radicle.issues` until the registry schema grows those fields. |
| `patches[]` | Radicle patch COBs and `refs/patches` | Map patch ID/title/status/author/summary. Radicle draft/open can map to `proposed` or `review`; merged maps to `merged`; archived/rejected maps to `rejected` when no better enum exists. Preserve revision IDs, base/head refs, and review details under `substrates.radicle.patches`. |
| `releases[]` | Git tags governed by canonical ref rules | Keep release metadata in the registry release object; optionally record Radicle canonical tag rules under `substrates.radicle.identity_payload.canonical_refs`. |
| `substrates.radicle.rid` | Repository Identifier | Store the RID used for Radicle clone/discovery. |
| `substrates.radicle.identity_payload` | Canonical JSON identity document | Store the inspected/projected subset needed by the aggregator: project payload, delegates, threshold, visibility, and canonical ref rules. |
| `substrates.radicle.local_verification` | Local execution evidence | Explicitly distinguish `source_inspected`, `cli_installed`, `live_cli_verified`, and `published`. For this spike: source inspected is true; CLI installed/live verified/published are false. |

## Fixture policy

`fixtures/radicle-backed-project.registry.json` is intentionally synthetic:

- fake RID and DIDs only;
- no private keys;
- no live Radicle home;
- no network node;
- no public seed/publish action;
- `substrates.radicle.local_verification.live_cli_verified` is `false`.

The fixture is useful for testing whether the registry shape can preserve Radicle-specific identity, delegate, issue, patch, and clone metadata. It is **not** evidence that the synthetic RID exists on the Radicle network.

## Next safe follow-up

When a safe Radicle binary is available through an approved channel, run a purely local profile using a temporary `RAD_HOME`, initialize a disposable Git repository, capture `rad .`, `rad inspect --payload`, local issue output, and local patch output, then replace the synthetic fixture with a generated fixture. Do not connect to public seeds or publish unless explicitly approved.
