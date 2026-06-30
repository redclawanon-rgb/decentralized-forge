#!/usr/bin/env python3
"""Refresh a persistent Radicle follower seed cache from a trusted source seed.

This helper is for follower seed hosts that already have a Radicle identity and
service wrapper. It preserves follower key material, backs up stale cache state,
clones a retained RID from an explicit source seed, verifies the readback commit,
and restores the follower seed policy. Dry-run mode is safe on any platform and
prints a bounded plan without touching local state or running commands.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def timestamp_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def parse_seed_node_id(seed: str) -> str:
    if "@" not in seed:
        raise ValueError("--source-seed must be '<node-id>@<host>:<port>'")
    node_id, _address = seed.split("@", 1)
    if not node_id:
        raise ValueError("source seed address is missing node id")
    return node_id


def rid_storage_name(rid: str) -> str:
    if not rid.startswith("rad:"):
        raise ValueError("--rid must start with 'rad:'")
    storage_name = rid.removeprefix("rad:")
    if not storage_name:
        raise ValueError("--rid is missing storage id after 'rad:'")
    return storage_name


def clone_command(args: argparse.Namespace, source_node_id: str, readback_path: Path) -> list[str]:
    return [
        "rad",
        "clone",
        "--timeout",
        args.clone_timeout,
        "--seed",
        source_node_id,
        "--signed-refs-feature-level",
        args.signed_refs_feature_level,
        args.rid,
        str(readback_path),
    ]


def seed_command(args: argparse.Namespace) -> list[str]:
    return ["rad", "seed", args.rid, "--scope", "all", "--no-fetch"]


def build_paths(args: argparse.Namespace) -> dict[str, Path]:
    state_dir = args.state_dir
    rad_home = state_dir / "rad-home"
    readback_path = state_dir / "readback" / "decentralized-forge"
    backups = state_dir / "backups"
    rid_storage = rad_home / "storage" / rid_storage_name(args.rid)
    slug = f"{rid_storage_name(args.rid)}-{timestamp_slug()}"
    return {
        "state_dir": state_dir,
        "rad_home": rad_home,
        "passphrase_file": state_dir / "follower.passphrase",
        "readback_path": readback_path,
        "readback_parent": readback_path.parent,
        "backups": backups,
        "storage": rid_storage,
        "storage_backup": backups / f"refresh-storage-{slug}",
        "rad_home_backup": backups / f"refresh-rad-home-{slug}",
    }


def dry_run_plan(args: argparse.Namespace, source_node_id: str, paths: dict[str, Path]) -> dict:
    return {
        "schema_version": "decentralized-forge.radicle-follower-refresh-plan.v1",
        "created_utc": now_utc(),
        "host": socket.gethostname(),
        "dry_run": True,
        "live_actions_executed": False,
        "mode_requested": args.mode,
        "rid": args.rid,
        "source_seed": args.source_seed,
        "source_seed_node_id": source_node_id,
        "expected_commit": args.expected_commit,
        "state_dir": str(paths["state_dir"]),
        "rad_home": str(paths["rad_home"]),
        "listen": args.listen,
        "service": args.service,
        "would_stop_service": bool(args.service),
        "would_stop_existing_node": True,
        "would_backup_storage": args.mode in {"auto", "storage"},
        "storage_path": str(paths["storage"]),
        "storage_backup_path": str(paths["storage_backup"]),
        "would_backup_rad_home": args.mode in {"auto", "rad-home"},
        "rad_home_backup_path": str(paths["rad_home_backup"]),
        "would_preserve_keys_and_config": args.mode in {"auto", "rad-home"},
        "would_remove_readback_path": str(paths["readback_path"]),
        "start_command": ["rad", "node", "start", "--", "--listen", args.listen],
        "connect_command": ["rad", "node", "connect", args.source_seed, "--timeout", args.connect_timeout],
        "clone_command": clone_command(args, source_node_id, paths["readback_path"]),
        "seed_command": seed_command(args),
        "would_restart_service": bool(args.service),
        "secret_values_recorded": False,
    }


def run(
    cmd: list[str],
    *,
    commands: list[dict],
    env: dict[str, str],
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


def ensure_rad_home_under_state(rad_home: Path, state_dir: Path) -> None:
    if rad_home.resolve().parent != state_dir.resolve():
        raise ValueError(f"rad-home must be directly under state-dir: {rad_home}")


def backup_storage(paths: dict[str, Path]) -> Path | None:
    storage = paths["storage"]
    if not storage.exists():
        return None
    if storage.resolve().parent != (paths["rad_home"] / "storage").resolve():
        raise ValueError(f"RID storage parent mismatch: {storage}")
    paths["backups"].mkdir(parents=True, exist_ok=True)
    shutil.move(str(storage), str(paths["storage_backup"]))
    return paths["storage_backup"]


def backup_rad_home_preserving_identity(paths: dict[str, Path]) -> tuple[Path, bool, bool]:
    rad_home = paths["rad_home"]
    ensure_rad_home_under_state(rad_home, paths["state_dir"])
    keys = rad_home / "keys"
    config = rad_home / "config.json"
    if not keys.exists():
        raise ValueError(f"refusing rad-home refresh because keys are missing: {keys}")
    if not config.is_file():
        raise ValueError(f"refusing rad-home refresh because config.json is missing: {config}")
    paths["backups"].mkdir(parents=True, exist_ok=True)
    shutil.move(str(rad_home), str(paths["rad_home_backup"]))
    rad_home.mkdir(parents=True, exist_ok=True)
    shutil.copytree(paths["rad_home_backup"] / "keys", rad_home / "keys")
    shutil.copy2(paths["rad_home_backup"] / "config.json", rad_home / "config.json")
    return paths["rad_home_backup"], True, True


def remove_readback(paths: dict[str, Path]) -> None:
    readback_path = paths["readback_path"]
    if readback_path.exists():
        shutil.rmtree(readback_path)
    paths["readback_parent"].mkdir(parents=True, exist_ok=True)


def refresh_once(
    args: argparse.Namespace,
    *,
    source_node_id: str,
    paths: dict[str, Path],
    env: dict[str, str],
    commands: list[dict],
    passphrase: str,
) -> str:
    remove_readback(paths)
    run(["rad", "node", "start", "--", "--listen", args.listen], commands=commands, env=env, timeout=60, secrets_to_scrub=[passphrase])
    time.sleep(args.settle_seconds)
    run(
        ["rad", "node", "connect", args.source_seed, "--timeout", args.connect_timeout],
        commands=commands,
        env=env,
        timeout=60,
        secrets_to_scrub=[passphrase],
    )
    run(
        clone_command(args, source_node_id, paths["readback_path"]),
        commands=commands,
        cwd=paths["readback_parent"],
        env=env,
        timeout=args.clone_timeout_seconds,
        secrets_to_scrub=[passphrase],
    )
    head = run(["git", "rev-parse", "HEAD"], commands=commands, cwd=paths["readback_path"], env=env, timeout=30)
    readback_commit = head["stdout"].strip()
    run(seed_command(args), commands=commands, env=env, timeout=60, secrets_to_scrub=[passphrase])
    run(["rad", "node", "stop"], commands=commands, env=env, timeout=30, allow_fail=True, secrets_to_scrub=[passphrase])
    return readback_commit


def service_command(action: str, service: str) -> list[str]:
    return ["systemctl", "--user", action, service]


def write_output(args: argparse.Namespace, payload: dict) -> None:
    output = json.dumps(payload, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + "\n", encoding="utf-8")
    print(output)


def live_refresh(args: argparse.Namespace, source_node_id: str, paths: dict[str, Path]) -> tuple[int, dict]:
    if sys.platform.startswith("win"):
        raise SystemExit("Live follower refresh must run on the Linux follower seed host. Use --dry-run for a local plan.")
    if not paths["passphrase_file"].is_file():
        raise SystemExit(f"missing follower passphrase file: {paths['passphrase_file']}")

    passphrase = paths["passphrase_file"].read_text(encoding="utf-8").strip()
    if not passphrase:
        raise SystemExit(f"passphrase file is empty: {paths['passphrase_file']}")

    env = os.environ.copy()
    if args.bin_dir:
        env["PATH"] = f"{args.bin_dir}:{env.get('PATH', '')}"
    env["RAD_HOME"] = str(paths["rad_home"])
    env["RAD_PASSPHRASE"] = passphrase

    commands: list[dict] = []
    result = {
        "schema_version": "decentralized-forge.radicle-follower-refresh.v1",
        "created_utc": now_utc(),
        "host": socket.gethostname(),
        "dry_run": False,
        "live_actions_executed": True,
        "mode_requested": args.mode,
        "mode_used": "",
        "rid": args.rid,
        "source_seed": args.source_seed,
        "source_seed_node_id": source_node_id,
        "expected_commit": args.expected_commit,
        "state_dir": str(paths["state_dir"]),
        "rad_home": str(paths["rad_home"]),
        "listen": args.listen,
        "service": args.service,
        "storage_backup_path": None,
        "rad_home_backup_path": None,
        "keys_preserved": False,
        "config_preserved": False,
        "readback_commit": "",
        "readback_matches_expected": False,
        "service_active_after_refresh": None,
        "secret_values_recorded": False,
    }

    try:
        run(["rad", "--version"], commands=commands, env=env, timeout=30)
        run(["radicle-node", "--version"], commands=commands, env=env, timeout=30)
        if args.service:
            run(service_command("stop", args.service), commands=commands, env=env, timeout=60, allow_fail=True, secrets_to_scrub=[passphrase])
        run(["rad", "node", "stop"], commands=commands, env=env, timeout=30, allow_fail=True, secrets_to_scrub=[passphrase])

        if args.mode in {"auto", "storage"}:
            result["mode_used"] = "storage"
            storage_backup = backup_storage(paths)
            result["storage_backup_path"] = str(storage_backup) if storage_backup else None
            readback_commit = refresh_once(
                args,
                source_node_id=source_node_id,
                paths=paths,
                env=env,
                commands=commands,
                passphrase=passphrase,
            )
            result["readback_commit"] = readback_commit
            result["readback_matches_expected"] = readback_commit == args.expected_commit

        if args.mode == "rad-home" or (args.mode == "auto" and not result["readback_matches_expected"]):
            result["mode_used"] = "rad-home"
            run(["rad", "node", "stop"], commands=commands, env=env, timeout=30, allow_fail=True, secrets_to_scrub=[passphrase])
            rad_home_backup, keys_preserved, config_preserved = backup_rad_home_preserving_identity(paths)
            result["rad_home_backup_path"] = str(rad_home_backup)
            result["keys_preserved"] = keys_preserved
            result["config_preserved"] = config_preserved
            readback_commit = refresh_once(
                args,
                source_node_id=source_node_id,
                paths=paths,
                env=env,
                commands=commands,
                passphrase=passphrase,
            )
            result["readback_commit"] = readback_commit
            result["readback_matches_expected"] = readback_commit == args.expected_commit

        return_code = 0 if result["readback_matches_expected"] else 1
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
        return_code = 1
    finally:
        run(["rad", "node", "stop"], commands=commands, env=env, timeout=30, allow_fail=True, secrets_to_scrub=[passphrase])
        if args.service:
            run(service_command("start", args.service), commands=commands, env=env, timeout=60, allow_fail=True, secrets_to_scrub=[passphrase])
            active = run(service_command("is-active", args.service), commands=commands, env=env, timeout=30, allow_fail=True, secrets_to_scrub=[passphrase])
            result["service_active_after_refresh"] = active["stdout"].strip() == "active"
        result["commands"] = commands

    return return_code, result


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("value must be positive")
    return parsed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Refresh a Radicle follower seed cache from an explicit source seed")
    parser.add_argument("--rid", required=True)
    parser.add_argument("--source-seed", required=True, help="Trusted source seed as '<node-id>@<host>:<port>'")
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--listen", required=True)
    parser.add_argument("--service", help="Optional systemd --user service to stop before refresh and restart afterward")
    parser.add_argument("--mode", choices=["auto", "storage", "rad-home"], default="auto")
    parser.add_argument("--signed-refs-feature-level", default="root")
    parser.add_argument("--bin-dir", type=Path, default=Path(os.environ.get("RADICLE_BIN_DIR", "")) if os.environ.get("RADICLE_BIN_DIR") else None)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--connect-timeout", default="30s")
    parser.add_argument("--clone-timeout", default="180s")
    parser.add_argument("--clone-timeout-seconds", type=positive_int, default=240)
    parser.add_argument("--settle-seconds", type=positive_int, default=5)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    source_node_id = parse_seed_node_id(args.source_seed)
    paths = build_paths(args)

    if args.dry_run:
        plan = dry_run_plan(args, source_node_id, paths)
        write_output(args, plan)
        return 0

    return_code, result = live_refresh(args, source_node_id, paths)
    write_output(args, result)
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
