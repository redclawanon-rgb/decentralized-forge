#!/usr/bin/env python3
"""Start, stop, or inspect a Radicle seed on a Linux host without printing secrets."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path


def env_for(args: argparse.Namespace) -> dict[str, str]:
    if not args.passphrase_file.is_file():
        raise SystemExit(f"missing passphrase file: {args.passphrase_file}")
    env = os.environ.copy()
    env["RAD_HOME"] = str(args.rad_home)
    env["RAD_PASSPHRASE"] = args.passphrase_file.read_text(encoding="utf-8").strip()
    env["PATH"] = f"{args.bin_dir}:{env.get('PATH', '')}"
    return env


def run(cmd: list[str], env: dict[str, str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, env=env, check=check, text=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Control a local Radicle seed host profile")
    parser.add_argument("action", choices=["start", "stop", "status"])
    parser.add_argument("--rid", required=True)
    parser.add_argument("--rad-home", type=Path, required=True)
    parser.add_argument("--passphrase-file", type=Path, required=True)
    parser.add_argument("--bin-dir", type=Path, default=Path.home() / ".local" / "bin")
    parser.add_argument("--listen", default="127.0.0.1:8799")
    parser.add_argument("--settle-seconds", type=int, default=5)
    args = parser.parse_args(argv)

    if sys.platform.startswith("win"):
        raise SystemExit("This helper must run on the Linux seed host.")

    env = env_for(args)
    if args.action == "stop":
        run(["rad", "node", "stop"], env, check=False)
        return 0
    if args.action == "start":
        run(["rad", "node", "stop"], env, check=False)
        run(["rad", "node", "start", "--", "--listen", args.listen], env)
        time.sleep(args.settle_seconds)
        run(["rad", "seed", args.rid, "--scope", "all", "--no-fetch"], env)
    run(["rad", "node", "status"], env, check=False)
    print("secret_values_printed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
