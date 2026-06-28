#!/usr/bin/env python3
"""Local CLI for decentralized-forge registry fixtures."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

import nip34_adapter
import preflight_static_artifact
import render_project_page

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_NIP34_REPO_FIXTURE = ROOT / "fixtures" / "nostr-repo-announcement.json"
DEFAULT_NIP34_COLLAB_FIXTURE = ROOT / "fixtures" / "nostr-collaboration-events.json"
DEFAULT_NIP34_STATE_STATUS_FIXTURE = ROOT / "fixtures" / "nostr-repo-state-status.json"
DEFAULT_NIP34_LIVE_READBACK_FIXTURE = ROOT / "fixtures" / "nostr-live-readback-events.json"
DEFAULT_LIVE_EVIDENCE_INDEX = ROOT / "fixtures" / "live-evidence-index.json"


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def verification_summary(states: list[dict]) -> dict:
    state_counts = Counter(state.get("state", "unknown") for state in states if isinstance(state, dict))
    return {
        "total": sum(state_counts.values()),
        "by_state": dict(sorted(state_counts.items())),
        "live_verified": sum(1 for state in states if isinstance(state, dict) and state.get("live_verified") is True),
        "synthetic": sum(1 for state in states if isinstance(state, dict) and state.get("synthetic") is True),
    }


def registry_summary(registry: dict, source_path: Path) -> dict:
    issues = registry.get("issues", [])
    patches = registry.get("patches", [])
    releases = registry.get("releases", [])
    artifacts = [
        artifact
        for release in releases
        for artifact in release.get("artifacts", [])
        if isinstance(artifact, dict)
    ]
    return {
        "schema_version": "decentralized-forge.registry-summary.v1",
        "source": relative(source_path),
        "project": {
            "id": registry["project"]["id"],
            "name": registry["project"]["name"],
            "default_branch": registry["project"]["default_branch"],
        },
        "counts": {
            "maintainers": len(registry.get("maintainers", [])),
            "clone_urls": len(registry.get("clone_urls", [])),
            "issues": len(issues),
            "patches": len(patches),
            "releases": len(releases),
            "artifacts": len(artifacts),
            "ci_checks": len(registry.get("ci_checks", [])),
            "verification_states": len(registry.get("verification_states", [])),
        },
        "clone_transports": sorted(
            {clone.get("transport") for clone in registry.get("clone_urls", []) if clone.get("transport")}
        ),
        "release_versions": [release.get("version") for release in releases if release.get("version")],
        "artifact_names": [artifact.get("name") for artifact in artifacts if artifact.get("name")],
        "artifact_cids": sorted({artifact.get("cid") for artifact in artifacts if artifact.get("cid")}),
        "verification": verification_summary(registry.get("verification_states", [])),
        "non_claims": {
            "production_ready": False,
            "durable_storage_verified": False,
            "censorship_resistance_verified": False,
            "security_guarantee": False,
        },
    }


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{json.dumps(payload, indent=2, sort_keys=True)}\n", encoding="utf-8")


def command_validate(args: argparse.Namespace) -> int:
    for registry_path in args.registries:
        render_project_page.load_registry(registry_path)
        print(f"valid registry: {relative(registry_path)}")
    return 0


def command_render(args: argparse.Namespace) -> int:
    render_args = [str(args.registry), str(args.output)]
    if args.with_demo_fixtures:
        render_args.extend(
            [
                "--nip34-repo-fixture",
                str(DEFAULT_NIP34_REPO_FIXTURE),
                "--nip34-collaboration-fixture",
                str(DEFAULT_NIP34_COLLAB_FIXTURE),
                "--nip34-state-status-fixture",
                str(DEFAULT_NIP34_STATE_STATUS_FIXTURE),
                "--nip34-live-readback-fixture",
                str(DEFAULT_NIP34_LIVE_READBACK_FIXTURE),
                "--live-evidence-index",
                str(DEFAULT_LIVE_EVIDENCE_INDEX),
            ]
        )
    return render_project_page.main(render_args)


def command_export_summary(args: argparse.Namespace) -> int:
    registry = render_project_page.load_registry(args.registry)
    write_json(args.output, registry_summary(registry, args.registry))
    print(f"wrote summary: {relative(args.output)}")
    return 0


def run_command(command: list[str]) -> int:
    print(f"+ {' '.join(command)}")
    result = subprocess.run(command, cwd=ROOT)
    return result.returncode


def npm_command(command: str) -> str:
    executable = shutil.which(command)
    if executable:
        return executable
    if sys.platform == "win32":
        executable = shutil.which(f"{command}.cmd")
        if executable:
            return executable
    return command


def command_verify_local(args: argparse.Namespace) -> int:
    commands = [
        [sys.executable, "-m", "json.tool", "schemas/project-registry.schema.json"],
        [sys.executable, "-m", "json.tool", "fixtures/example-project.registry.json"],
        [sys.executable, "-m", "json.tool", "fixtures/portable-lab.registry.json"],
        [sys.executable, "-m", "json.tool", "fixtures/radicle-backed-project.registry.json"],
        [sys.executable, "-m", "json.tool", "fixtures/nostr-repo-announcement.json"],
        [sys.executable, "-m", "json.tool", "fixtures/nostr-collaboration-events.json"],
        [sys.executable, "-m", "json.tool", "fixtures/nostr-repo-state-status.json"],
        [sys.executable, "-m", "json.tool", "fixtures/live-adapter-replay-checklist.json"],
        [sys.executable, "-m", "json.tool", "fixtures/live-evidence-index.json"],
        [
            sys.executable,
            "scripts/nip34_adapter.py",
            "fixtures/nostr-repo-announcement.json",
            "fixtures/nostr-collaboration-events.json",
            "fixtures/nostr-repo-state-status.json",
        ],
        [sys.executable, "scripts/preflight_static_artifact.py"],
        [sys.executable, "scripts/forge_registry.py", "validate", "fixtures/example-project.registry.json", "fixtures/portable-lab.registry.json"],
        [sys.executable, "scripts/forge_registry.py", "render", "fixtures/portable-lab.registry.json", "output/portable-lab.html"],
        [sys.executable, "scripts/forge_registry.py", "export-summary", "fixtures/example-project.registry.json", "output/demo-project.summary.json"],
        [sys.executable, "scripts/forge_registry.py", "export-summary", "fixtures/portable-lab.registry.json", "output/portable-lab.summary.json"],
        [sys.executable, "scripts/live_gate_inventory.py"],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
    ]
    if not args.skip_npm_ci:
        commands.append([npm_command("npm"), "ci"])
    commands.append([npm_command("npm"), "run", "verify:car-cid"])

    for command in commands:
        exit_code = run_command(command)
        if exit_code:
            return exit_code

    failures = preflight_static_artifact.check_static_artifact()
    if failures:
        for failure in failures:
            print(f"preflight failure: {failure}", file=sys.stderr)
        return 1
    print("local verification passed")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate one or more registry fixtures")
    validate.add_argument("registries", type=Path, nargs="+")
    validate.set_defaults(func=command_validate)

    render = subparsers.add_parser("render", help="Render a registry fixture to static HTML")
    render.add_argument("registry", type=Path)
    render.add_argument("output", type=Path)
    render.add_argument(
        "--with-demo-fixtures",
        action="store_true",
        help="Include the repository's demo NIP-34 fixtures and live evidence index",
    )
    render.set_defaults(func=command_render)

    export_summary = subparsers.add_parser("export-summary", help="Export a deterministic registry summary JSON")
    export_summary.add_argument("registry", type=Path)
    export_summary.add_argument("output", type=Path)
    export_summary.set_defaults(func=command_export_summary)

    verify_local = subparsers.add_parser("verify-local", help="Run the documented local verification suite")
    verify_local.add_argument("--skip-npm-ci", action="store_true", help="Use already-installed Node dependencies")
    verify_local.set_defaults(func=command_verify_local)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (OSError, json.JSONDecodeError, render_project_page.RegistryError, ValueError) as exc:
        print(f"forge-registry error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
