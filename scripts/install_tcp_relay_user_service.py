#!/usr/bin/env python3
"""Install a user-level systemd TCP relay service using socat.

This is used for evidence-scoped public ingress where the serving process lives
on another host reachable through a private network path. It writes only a
systemd user unit; it does not write secrets.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=check, text=True)


def service_text(args: argparse.Namespace, socat: str) -> str:
    return f"""[Unit]
Description={args.description}
Documentation={args.documentation}
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart={socat} TCP-LISTEN:{args.listen_port},fork,reuseaddr,bind={args.listen_host} TCP:{args.target_host}:{args.target_port}
Restart=always
RestartSec={args.restart_sec}
NoNewPrivileges=true

[Install]
WantedBy=default.target
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install a user systemd TCP relay service")
    parser.add_argument("--service-name", default="decentralized-forge-radicle-mirror-public-relay.service")
    parser.add_argument("--description", default="Decentralized Forge public TCP relay")
    parser.add_argument("--documentation", default="https://github.com/redclawanon-rgb/decentralized-forge")
    parser.add_argument("--listen-host", default="0.0.0.0")
    parser.add_argument("--listen-port", type=int, required=True)
    parser.add_argument("--target-host", required=True)
    parser.add_argument("--target-port", type=int, required=True)
    parser.add_argument("--restart-sec", type=int, default=10)
    parser.add_argument("--settle-seconds", type=int, default=3)
    args = parser.parse_args(argv)

    if sys.platform.startswith("win"):
        raise SystemExit("This installer must run on the Linux relay host.")
    socat = shutil.which("socat")
    if not socat:
        raise SystemExit("missing socat binary")

    systemd_user = Path.home() / ".config" / "systemd" / "user"
    service_path = systemd_user / args.service_name
    systemd_user.mkdir(parents=True, exist_ok=True)
    service_path.write_text(service_text(args, socat), encoding="utf-8", newline="\n")

    run(["systemctl", "--user", "stop", args.service_name], check=False)
    run(["systemctl", "--user", "daemon-reload"])
    run(["systemctl", "--user", "reset-failed", args.service_name], check=False)
    run(["systemctl", "--user", "enable", args.service_name])
    run(["systemctl", "--user", "restart", args.service_name])
    time.sleep(args.settle_seconds)

    run(["systemctl", "--user", "--no-pager", "--full", "status", args.service_name], check=False)
    print(f"installed_user_service={args.service_name}")
    print(f"service_path={service_path}")
    print(f"listen={args.listen_host}:{args.listen_port}")
    print(f"target={args.target_host}:{args.target_port}")
    print("secret_values_printed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
