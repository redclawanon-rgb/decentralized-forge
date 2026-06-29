#!/usr/bin/env python3
"""Check a public Radicle seed by cloning a RID from a fresh local profile."""

from __future__ import annotations

import argparse
import json
import os
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def free_local_listen() -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return f"127.0.0.1:{sock.getsockname()[1]}"


def run(
    cmd: list[str],
    *,
    commands: list[dict],
    env: dict[str, str] | None = None,
    cwd: Path | None = None,
    input_text: str | None = None,
    timeout: int = 60,
    allow_fail: bool = False,
    secrets_to_scrub: list[str] | None = None,
) -> dict:
    start = time.monotonic()
    completed = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        input=input_text,
        text=True,
        capture_output=True,
        timeout=timeout,
    )
    record = {
        "cmd": cmd,
        "cwd": str(cwd) if cwd else None,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "duration_seconds": round(time.monotonic() - start, 3),
    }
    for secret in secrets_to_scrub or []:
        if secret:
            record["stdout"] = record["stdout"].replace(secret, "<redacted passphrase>")
            record["stderr"] = record["stderr"].replace(secret, "<redacted passphrase>")
    commands.append(record)
    if completed.returncode != 0 and not allow_fail:
        raise subprocess.CalledProcessError(completed.returncode, cmd, completed.stdout, completed.stderr)
    return record


def git_head(path: Path, commands: list[dict]) -> str:
    record = run(["git", "rev-parse", "HEAD"], cwd=path, commands=commands, timeout=30, allow_fail=True)
    return record["stdout"].strip() if record["returncode"] == 0 else ""


def parse_seed(seed: str, explicit_node_id: str | None) -> tuple[str, str]:
    if explicit_node_id:
        return explicit_node_id, seed
    if "@" not in seed:
        raise ValueError("--seed-node-id is required when --seed does not include '<node-id>@'")
    node_id, _host = seed.split("@", 1)
    if not node_id:
        raise ValueError("seed address is missing node id")
    return node_id, seed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fresh-profile public Radicle seed clone/readback check")
    parser.add_argument("--seed", required=True, help="Seed address, usually '<node-id>@<host>:<port>'")
    parser.add_argument("--seed-node-id")
    parser.add_argument("--rid", required=True)
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--alias", default="df-public-seed-reader")
    parser.add_argument("--clone-name", default="decentralized-forge")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--bin-dir", type=Path, default=Path(os.environ.get("RADICLE_BIN_DIR", "")) if os.environ.get("RADICLE_BIN_DIR") else None)
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--connect-timeout", default="30s")
    parser.add_argument("--clone-timeout", default="180s")
    args = parser.parse_args(argv)

    seed_node_id, seed_address = parse_seed(args.seed, args.seed_node_id)
    tmp = Path(tempfile.mkdtemp(prefix="df-public-radicle-seed-check-"))
    commands: list[dict] = []
    passphrase = secrets.token_urlsafe(32)
    env = os.environ.copy()
    if args.bin_dir:
        env["PATH"] = f"{args.bin_dir}:{env.get('PATH', '')}"
    env["RAD_HOME"] = str(tmp / "rad-home")
    env["RAD_PASSPHRASE"] = passphrase
    listen = free_local_listen()
    clone_parent = tmp / "clone-parent"
    clone_parent.mkdir(parents=True)
    clone_path = clone_parent / args.clone_name
    node_stop_record: dict | None = None

    result = {
        "schema_version": "decentralized-forge.public-radicle-seed-health-check.v1",
        "created_utc": now_utc(),
        "host": socket.gethostname(),
        "seed": seed_address,
        "seed_node_id": seed_node_id,
        "rid": args.rid,
        "expected_commit": args.expected_commit,
        "temp_state": str(tmp) if args.keep_temp else "removed",
        "secret_values_recorded": False,
        "claim_boundary": (
            "Fresh local Radicle profile connected to one explicit seed, cloned one RID, "
            "and compared git HEAD to the expected commit. This is not a durability, "
            "default public-routing, security, identity-trust, or production-readiness claim."
        ),
    }

    try:
        run(["rad", "--version"], commands=commands, env=env)
        run(["radicle-node", "--version"], commands=commands, env=env)
        auth = run(
            ["rad", "auth", "--alias", args.alias, "--stdin"],
            commands=commands,
            env=env,
            input_text=passphrase + "\n",
            timeout=60,
            allow_fail=True,
            secrets_to_scrub=[passphrase],
        )
        node_start = run(
            ["rad", "node", "start", "--", "--listen", listen],
            commands=commands,
            env=env,
            timeout=60,
            allow_fail=True,
            secrets_to_scrub=[passphrase],
        )
        time.sleep(5)
        connect = run(
            ["rad", "node", "connect", seed_address, "--timeout", args.connect_timeout],
            commands=commands,
            env=env,
            timeout=60,
            allow_fail=True,
            secrets_to_scrub=[passphrase],
        )
        clone = run(
            ["rad", "clone", "--timeout", args.clone_timeout, "--seed", seed_node_id, args.rid, str(clone_path)],
            commands=commands,
            cwd=clone_parent,
            env=env,
            timeout=240,
            allow_fail=True,
            secrets_to_scrub=[passphrase],
        )
        readback_commit = git_head(clone_path, commands) if clone["returncode"] == 0 else ""
        result.update(
            {
                "auth_succeeded": auth["returncode"] == 0,
                "node_started": node_start["returncode"] == 0,
                "connected_to_seed": connect["returncode"] == 0,
                "clone_succeeded": clone["returncode"] == 0,
                "readback_commit": readback_commit,
                "readback_matches_expected": readback_commit == args.expected_commit,
                "verification_passed": readback_commit == args.expected_commit,
            }
        )
    finally:
        node_stop = subprocess.run(["rad", "node", "stop"], env=env, text=True, capture_output=True, timeout=30)
        node_stop_record = {
            "cmd": ["rad", "node", "stop"],
            "returncode": node_stop.returncode,
            "stdout": node_stop.stdout.replace(passphrase, "<redacted passphrase>"),
            "stderr": node_stop.stderr.replace(passphrase, "<redacted passphrase>"),
        }
        if not args.keep_temp:
            shutil.rmtree(tmp, ignore_errors=True)

    result["commands"] = commands
    result["node_stop"] = node_stop_record
    output = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
    print(output)
    return 0 if result.get("verification_passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
