#!/usr/bin/env python3
"""Plan or run an outside-reader rehearsal for the public Radicle clone path."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import forge_registry


def seed_ids(selection: str) -> list[str]:
    if selection == "both":
        return ["primary", "second"]
    return [selection]


def planned_output(output_dir: Path, seed: str) -> Path:
    return output_dir / f"radicle-first-public-clone-outside-reader-{seed}-YYYY-MM-DD.json"


def build_rehearsal_plan(args: argparse.Namespace) -> dict:
    status = forge_registry.public_seed_status_model(args.index)
    commands = []
    for seed in seed_ids(args.seed):
        command = [
            "python",
            "scripts/forge_registry.py",
            "verify-first-public-clone",
            "--seed",
            seed,
            "--json",
            "--output",
            str(planned_output(args.output_dir, seed)),
            "--connect-timeout",
            args.connect_timeout,
            "--clone-timeout",
            args.clone_timeout,
        ]
        if args.bin_dir:
            command.extend(["--bin-dir", str(args.bin_dir)])
        commands.append({"seed": seed, "command": command, "output": str(planned_output(args.output_dir, seed))})

    return {
        "schema_version": "decentralized-forge.first-public-clone-outside-reader-rehearsal.v1",
        "mode": "execute" if args.execute else "plan",
        "live_actions_executed": False,
        "rid": status["rid"],
        "expected_commit": status["expected_commit"],
        "current_public_seed_status": status["status"],
        "selected_seeds": seed_ids(args.seed),
        "commands": commands,
        "outside_reader_requirements": [
            "Linux or another environment with Radicle CLI available",
            "network reachability to the selected public seed address",
            "a checkout of this repository at the commit being rehearsed",
            "no maintainer Radicle state or private key material copied into the reader environment",
        ],
        "non_claims": [
            "plan mode does not contact public seeds",
            "execute mode only verifies the selected direct-seed readback",
            "not a durability or uptime claim",
            "not proof of default public routing",
            "not proof of automatic future update propagation",
            "not a security guarantee",
            "not production readiness",
        ],
    }


def execute_rehearsal(plan: dict, cwd: Path) -> dict:
    results = []
    for item in plan["commands"]:
        output = Path(item["output"])
        output.parent.mkdir(parents=True, exist_ok=True)
        completed = subprocess.run(
            item["command"],
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        result = {
            "seed": item["seed"],
            "command": item["command"],
            "exit_code": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "output": item["output"],
        }
        if output.is_file():
            try:
                result["verification"] = json.loads(output.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                result["verification_error"] = str(exc)
        results.append(result)

    plan = dict(plan)
    plan["mode"] = "execute"
    plan["live_actions_executed"] = True
    plan["results"] = results
    plan["verification_passed"] = bool(results) and all(
        result["exit_code"] == 0 and result.get("verification", {}).get("verification_passed") is True
        for result in results
    )
    return plan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", choices=["primary", "second", "both"], default="both")
    parser.add_argument("--output-dir", type=Path, default=Path("evidence"))
    parser.add_argument("--execute", action="store_true", help="Run live first-public-clone checks instead of only printing the plan")
    parser.add_argument("--index", type=Path, default=forge_registry.DEFAULT_LIVE_EVIDENCE_INDEX)
    parser.add_argument("--bin-dir", type=Path, help="Directory containing rad/radicle-node for execute mode")
    parser.add_argument("--connect-timeout", default="30s")
    parser.add_argument("--clone-timeout", default="180s")
    parser.add_argument("--output", type=Path, help="Optional JSON file for the rehearsal plan or result")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    plan = build_rehearsal_plan(args)
    result = execute_rehearsal(plan, ROOT) if args.execute else plan
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(f"{text}\n", encoding="utf-8", newline="\n")
    else:
        print(text)
    return 0 if not args.execute or result.get("verification_passed") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
