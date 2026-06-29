#!/usr/bin/env python3
"""Bootstrap a Radicle follower seed from an explicit source seed.

The script creates or reuses a local follower Radicle identity, starts a node on
the requested listen address, clones a RID from a source seed, verifies the
checkout commit, and sets the follower's seed policy to `all`. It does not need
the retained maintainer key material.
"""

from __future__ import annotations

import argparse
import json
import os
import secrets
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run(
    cmd: list[str],
    *,
    commands: list[dict],
    cwd: Path | None = None,
    env: dict[str, str],
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
        "duration_seconds": round(time.monotonic() - start, 3),
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }
    for secret in secrets_to_scrub or []:
        if secret:
            record["stdout"] = record["stdout"].replace(secret, "<redacted passphrase>")
            record["stderr"] = record["stderr"].replace(secret, "<redacted passphrase>")
    commands.append(record)
    if completed.returncode != 0 and not allow_fail:
        raise subprocess.CalledProcessError(completed.returncode, cmd, completed.stdout, completed.stderr)
    return record


def parse_seed_node_id(seed: str) -> str:
    if "@" not in seed:
        raise ValueError("--source-seed must be '<node-id>@<host>:<port>'")
    node_id, _address = seed.split("@", 1)
    if not node_id:
        raise ValueError("source seed address is missing node id")
    return node_id


def read_or_create_passphrase(path: Path) -> str:
    if path.exists():
        passphrase = path.read_text(encoding="utf-8").strip()
        if not passphrase:
            raise SystemExit(f"passphrase file is empty: {path}")
        return passphrase
    path.parent.mkdir(parents=True, exist_ok=True)
    passphrase = secrets.token_urlsafe(32)
    path.write_text(passphrase + "\n", encoding="utf-8", newline="\n")
    os.chmod(path, 0o600)
    return passphrase


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bootstrap a Radicle follower seed")
    parser.add_argument("--rid", required=True)
    parser.add_argument("--source-seed", required=True)
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--listen", required=True)
    parser.add_argument("--alias", default="df-radicle-follower-seed")
    parser.add_argument("--bin-dir", type=Path, default=Path(os.environ.get("RADICLE_BIN_DIR", "")) if os.environ.get("RADICLE_BIN_DIR") else None)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--leave-running", action="store_true")
    parser.add_argument("--connect-timeout", default="30s")
    parser.add_argument("--clone-timeout", default="180s")
    args = parser.parse_args(argv)

    if sys.platform.startswith("win"):
        raise SystemExit("This bootstrapper must run on the Linux follower seed host.")

    source_node_id = parse_seed_node_id(args.source_seed)
    state_dir = args.state_dir
    rad_home = state_dir / "rad-home"
    readback_parent = state_dir / "readback"
    readback_path = readback_parent / "decentralized-forge"
    passphrase_file = state_dir / "follower.passphrase"
    passphrase = read_or_create_passphrase(passphrase_file)

    env = os.environ.copy()
    if args.bin_dir:
        env["PATH"] = f"{args.bin_dir}:{env.get('PATH', '')}"
    env["RAD_HOME"] = str(rad_home)
    env["RAD_PASSPHRASE"] = passphrase

    commands: list[dict] = []
    result = {
        "schema_version": "decentralized-forge.radicle-follower-seed-bootstrap.v1",
        "created_utc": now_utc(),
        "rid": args.rid,
        "source_seed": args.source_seed,
        "expected_commit": args.expected_commit,
        "state_dir": str(state_dir),
        "rad_home": str(rad_home),
        "listen": args.listen,
        "left_running": args.leave_running,
        "secret_values_recorded": False,
    }

    try:
        run(["rad", "--version"], commands=commands, env=env)
        run(["radicle-node", "--version"], commands=commands, env=env)

        if not (rad_home / "keys").exists():
            run(
                ["rad", "auth", "--alias", args.alias, "--stdin"],
                commands=commands,
                env=env,
                input_text=passphrase + "\n",
                timeout=60,
                secrets_to_scrub=[passphrase],
            )

        run(["rad", "node", "stop"], commands=commands, env=env, timeout=30, allow_fail=True, secrets_to_scrub=[passphrase])
        run(["rad", "node", "start", "--", "--listen", args.listen], commands=commands, env=env, timeout=60, secrets_to_scrub=[passphrase])
        time.sleep(5)
        status = run(["rad", "node", "status"], commands=commands, env=env, timeout=60, allow_fail=True, secrets_to_scrub=[passphrase])
        node_id = ""
        marker = "Node ID "
        if marker in status["stdout"]:
            node_id = status["stdout"].split(marker, 1)[1].split(" ", 1)[0]

        run(
            ["rad", "node", "connect", args.source_seed, "--timeout", args.connect_timeout],
            commands=commands,
            env=env,
            timeout=60,
            secrets_to_scrub=[passphrase],
        )
        if readback_path.exists():
            shutil.rmtree(readback_path)
        readback_parent.mkdir(parents=True, exist_ok=True)
        run(
            ["rad", "clone", "--timeout", args.clone_timeout, "--seed", source_node_id, args.rid, str(readback_path)],
            commands=commands,
            cwd=readback_parent,
            env=env,
            timeout=240,
            secrets_to_scrub=[passphrase],
        )
        head = run(["git", "rev-parse", "HEAD"], commands=commands, cwd=readback_path, env=env, timeout=30)
        readback_commit = head["stdout"].strip()
        run(
            ["rad", "seed", args.rid, "--scope", "all", "--no-fetch"],
            commands=commands,
            env=env,
            timeout=60,
            secrets_to_scrub=[passphrase],
        )
        result.update(
            {
                "node_id": node_id,
                "readback_commit": readback_commit,
                "readback_matches_expected": readback_commit == args.expected_commit,
                "seed_policy_scope": "all",
            }
        )
        return_code = 0 if readback_commit == args.expected_commit else 1
    finally:
        if not args.leave_running:
            run(["rad", "node", "stop"], commands=commands, env=env, timeout=30, allow_fail=True, secrets_to_scrub=[passphrase])
        result["commands"] = commands
        output = json.dumps(result, indent=2, sort_keys=True)
        if args.output:
            args.output.write_text(output + "\n", encoding="utf-8")
        print(output)

    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
