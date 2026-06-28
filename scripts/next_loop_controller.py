#!/usr/bin/env python3
"""Run the approval-bounded next-loop controller."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import live_gate_inventory

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "fixtures" / "next-loop-controller.json"


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def run_capture(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def git_value(*args: str) -> str:
    result = run_capture(["git", *args])
    if result.returncode:
        return "unknown"
    return result.stdout.strip()


def git_status_lines() -> list[str]:
    result = run_capture(["git", "status", "--short"])
    if result.returncode:
        return [f"git status failed: {result.stderr.strip()}"]
    return [line for line in result.stdout.splitlines() if line.strip()]


def load_config(path: Path) -> dict:
    config = json.loads(path.read_text(encoding="utf-8"))
    if config.get("schema_version") != "decentralized-forge.next-loop-controller.v1":
        raise ValueError(f"unsupported controller schema: {config.get('schema_version')}")
    if config.get("mode") != "approval-bounded":
        raise ValueError("controller mode must stay approval-bounded")
    if config.get("max_iterations_per_run") != 1:
        raise ValueError("controller is limited to one iteration per run")
    return config


def run_verification(skip_npm_ci: bool) -> dict:
    command = [sys.executable, "scripts/forge_registry.py", "verify-local"]
    if skip_npm_ci:
        command.append("--skip-npm-ci")

    print(f"+ {' '.join(command)}")
    result = subprocess.run(command, cwd=ROOT, text=True, check=False)
    return {
        "command": " ".join(command),
        "exit_code": result.returncode,
        "status": "passed" if result.returncode == 0 else "failed",
    }


def summarize_gates(inventory: dict, config: dict) -> list[str]:
    lines = []
    for group_name, group in sorted(inventory.get("groups", {}).items()):
        available = group.get("available_commands", [])
        available_text = ", ".join(available) if available else "none found"
        lines.append(f"- `{group_name}`: available tools: {available_text}; gate: {group.get('next_gate')}")

    lines.append("")
    lines.append("Blocked without explicit target:")
    for gate in config["blocked_without_explicit_target"]:
        lines.append(f"- `{gate['id']}`: {gate['requires']}")
    return lines


def build_report(config: dict, verification: dict | None, plan_only: bool, dirty_at_start: list[str]) -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    inventory = live_gate_inventory.inventory()
    head = git_value("rev-parse", "HEAD")
    branch = git_value("branch", "--show-current")
    origin = git_value("ls-remote", "origin", "refs/heads/main")
    status_after = git_status_lines()

    verification_status = "skipped (plan-only)" if plan_only else verification["status"]
    verification_command = "not run" if plan_only else verification["command"]
    verification_exit = "n/a" if plan_only else str(verification["exit_code"])

    lines = [
        "# Next Loop Controller Report",
        "",
        f"- Created UTC: `{now}`",
        f"- Mode: `{config['mode']}`",
        f"- Branch: `{branch}`",
        f"- Local HEAD: `{head}`",
        f"- Origin main: `{origin or 'unknown'}`",
        f"- Max iterations this run: `{config['max_iterations_per_run']}`",
        f"- Verification command: `{verification_command}`",
        f"- Verification status: `{verification_status}`",
        f"- Verification exit code: `{verification_exit}`",
        "",
        "## Worktree",
        "",
        "Start state:",
    ]
    if dirty_at_start:
        lines.extend(f"- `{line}`" for line in dirty_at_start)
    else:
        lines.append("- clean")

    lines.extend(["", "End state:"])
    if status_after:
        lines.extend(f"- `{line}`" for line in status_after)
    else:
        lines.append("- clean")

    lines.extend(
        [
            "",
            "## Safe Actions",
            "",
        ]
    )
    for action in config["approved_safe_actions"]:
        lines.append(f"- `{action}`")

    lines.extend(
        [
            "",
            "## Live Gates",
            "",
            *summarize_gates(inventory, config),
            "",
            "## Next Logical Step",
            "",
            "Keep looping through safe verification/reporting with this controller. Choose one explicit target before moving into live IPFS/storage, broader Radicle public-network checks, new Nostr publish/readback, signing/provenance, spending, direct outreach, or stronger claims.",
            "",
            "No live IPFS daemon/add/fetch/gateway/pinning, Nostr publish/readback, Radicle public-network action, signing action, wallet, paid infrastructure, production/private personal key use, direct outreach, or stronger durability/censorship/security/SLSA/production-readiness claim was performed by this controller.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path, report: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report, encoding="utf-8")
    print(f"wrote next-loop report: {relative(path)}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--check", action="store_true", help="Run safe verification and print the report")
    parser.add_argument("--write-report", action="store_true", help="Write the report path from controller config")
    parser.add_argument("--plan-only", action="store_true", help="Only render the next-loop plan; do not run verification")
    parser.add_argument("--skip-npm-ci", action="store_true", help="Use already-installed Node dependencies in the verifier")
    parser.add_argument("--allow-dirty", action="store_true", help="Continue when the worktree is already dirty")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not (args.check or args.write_report or args.plan_only):
        parser.error("choose --check, --write-report, or --plan-only")

    try:
        config = load_config(args.config)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"next-loop-controller error: {exc}", file=sys.stderr)
        return 2

    dirty_at_start = git_status_lines()
    if dirty_at_start and not args.allow_dirty:
        report = build_report(config, None, True, dirty_at_start)
        print(report, end="")
        print("next-loop-controller refused to run verification on a dirty worktree", file=sys.stderr)
        return 2

    verification = None
    if not args.plan_only:
        verification = run_verification(args.skip_npm_ci)

    report = build_report(config, verification, args.plan_only, dirty_at_start)
    if args.write_report:
        report_path = ROOT / config["report_path"]
        write_report(report_path, report)
    if args.check or args.plan_only:
        print(report, end="")

    if verification and verification["exit_code"]:
        return verification["exit_code"]
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
