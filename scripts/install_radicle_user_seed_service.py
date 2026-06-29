#!/usr/bin/env python3
"""Install a user-level systemd service for a Radicle follower seed.

The script is intended for Linux seed hosts. It reads an existing Radicle
passphrase file locally on the host, writes a private EnvironmentFile, installs
an LF-only user service, enables it, restarts it, and prints only non-secret
service state.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path


def run(cmd: list[str], *, check: bool = True, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=check, env=env, text=True)


def write_private(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    os.chmod(path, 0o600)


def service_text(args: argparse.Namespace, env_file: Path) -> str:
    return f"""[Unit]
Description={args.description}
Documentation={args.documentation}
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
Environment=RAD_HOME={args.rad_home}
Environment=PATH={args.bin_dir}:/usr/local/bin:/usr/bin:/bin
EnvironmentFile={env_file}
WorkingDirectory={args.working_directory}
ExecStartPre={args.bin_dir}/rad seed {args.rid} --scope all --no-fetch
ExecStart={args.bin_dir}/radicle-node --listen {args.listen} --force
Restart=always
RestartSec={args.restart_sec}
NoNewPrivileges=true

[Install]
WantedBy=default.target
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install a user systemd Radicle seed service")
    parser.add_argument("--service-name", default="decentralized-forge-radicle-seed.service")
    parser.add_argument("--description", default="Decentralized Forge public Radicle follower seed")
    parser.add_argument("--documentation", default="https://github.com/redclawanon-rgb/decentralized-forge")
    parser.add_argument("--rid", required=True)
    parser.add_argument("--rad-home", type=Path, required=True)
    parser.add_argument("--passphrase-file", type=Path, required=True)
    parser.add_argument("--listen", default="0.0.0.0:8776")
    parser.add_argument("--bin-dir", type=Path, default=Path.home() / ".local" / "bin")
    parser.add_argument("--working-directory", type=Path, required=True)
    parser.add_argument("--restart-sec", type=int, default=10)
    parser.add_argument("--settle-seconds", type=int, default=6)
    args = parser.parse_args(argv)

    if sys.platform.startswith("win"):
        raise SystemExit("This installer must run on the Linux seed host.")
    if not args.passphrase_file.is_file():
        raise SystemExit(f"missing passphrase file: {args.passphrase_file}")
    if not (args.bin_dir / "rad").is_file():
        raise SystemExit(f"missing rad binary: {args.bin_dir / 'rad'}")
    if not (args.bin_dir / "radicle-node").is_file():
        raise SystemExit(f"missing radicle-node binary: {args.bin_dir / 'radicle-node'}")

    passphrase = args.passphrase_file.read_text(encoding="utf-8").strip()
    if not passphrase:
        raise SystemExit("passphrase file was empty")

    systemd_user = Path.home() / ".config" / "systemd" / "user"
    service_path = systemd_user / args.service_name
    env_file = args.working_directory / "radicle-node.env"

    write_private(env_file, f"RAD_PASSPHRASE={passphrase}\n")
    write_private(service_path, service_text(args, env_file))

    run(["systemctl", "--user", "stop", args.service_name], check=False)
    run(["systemctl", "--user", "daemon-reload"])
    run(["systemctl", "--user", "reset-failed", args.service_name], check=False)
    run(["systemctl", "--user", "enable", args.service_name])
    run(["systemctl", "--user", "restart", args.service_name])
    time.sleep(args.settle_seconds)

    run(["systemctl", "--user", "--no-pager", "--full", "status", args.service_name], check=False)
    env = os.environ.copy()
    env["RAD_HOME"] = str(args.rad_home)
    env["PATH"] = f"{args.bin_dir}:{env.get('PATH', '')}"
    run([str(args.bin_dir / "rad"), "node", "status"], check=False, env=env)
    print(f"installed_user_service={args.service_name}")
    print(f"service_path={service_path}")
    print(f"env_file={env_file}")
    print("secret_values_printed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
