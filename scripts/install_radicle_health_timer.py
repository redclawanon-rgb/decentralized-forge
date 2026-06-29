#!/usr/bin/env python3
"""Install a user systemd timer for public Radicle seed health checks."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=check, text=True)


def write_lf(path: Path, text: str, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    os.chmod(path, mode)


def service_text(args: argparse.Namespace, state_dir: Path) -> str:
    output = state_dir / "latest.json"
    return f"""[Unit]
Description=Decentralized Forge public Radicle seed health check
Documentation=https://github.com/redclawanon-rgb/decentralized-forge

[Service]
Type=oneshot
WorkingDirectory={args.checkout}
Environment=PATH={args.bin_dir}:/usr/local/bin:/usr/bin:/bin
Environment=RADICLE_BIN_DIR={args.bin_dir}
ExecStart={args.python} {args.checkout}/scripts/check_public_radicle_seed.py --seed {args.seed} --rid {args.rid} --expected-commit {args.expected_commit} --output {output}
"""


def timer_text(args: argparse.Namespace) -> str:
    return f"""[Unit]
Description=Run Decentralized Forge public Radicle seed health check
Documentation=https://github.com/redclawanon-rgb/decentralized-forge

[Timer]
OnBootSec={args.on_boot_sec}
OnUnitActiveSec={args.on_unit_active_sec}
Persistent=true
Unit={args.service_name}

[Install]
WantedBy=timers.target
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install a user systemd timer for Radicle public seed checks")
    parser.add_argument("--service-name", default="decentralized-forge-radicle-healthcheck.service")
    parser.add_argument("--timer-name", default="decentralized-forge-radicle-healthcheck.timer")
    parser.add_argument("--checkout", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path, default=Path.home() / ".local" / "state" / "decentralized-forge" / "radicle-health")
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--bin-dir", type=Path, default=Path.home() / ".local" / "bin")
    parser.add_argument("--seed", required=True)
    parser.add_argument("--rid", required=True)
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--on-boot-sec", default="2min")
    parser.add_argument("--on-unit-active-sec", default="15min")
    parser.add_argument("--run-now", action="store_true")
    args = parser.parse_args(argv)

    if sys.platform.startswith("win"):
        raise SystemExit("This installer must run on the Linux health-check host.")
    if not (args.checkout / "scripts" / "check_public_radicle_seed.py").is_file():
        raise SystemExit(f"missing health-check script in checkout: {args.checkout}")
    if not (args.bin_dir / "rad").is_file():
        raise SystemExit(f"missing rad binary: {args.bin_dir / 'rad'}")

    systemd_user = Path.home() / ".config" / "systemd" / "user"
    service_path = systemd_user / args.service_name
    timer_path = systemd_user / args.timer_name
    args.state_dir.mkdir(parents=True, exist_ok=True)

    write_lf(service_path, service_text(args, args.state_dir))
    write_lf(timer_path, timer_text(args))

    run(["systemctl", "--user", "daemon-reload"])
    run(["systemctl", "--user", "enable", "--now", args.timer_name])
    if args.run_now:
        run(["systemctl", "--user", "start", args.service_name])

    run(["systemctl", "--user", "--no-pager", "--full", "status", args.timer_name], check=False)
    run(["systemctl", "--user", "--no-pager", "--full", "status", args.service_name], check=False)
    latest = args.state_dir / "latest.json"
    print(f"installed_health_timer={args.timer_name}")
    print(f"health_service={args.service_name}")
    print(f"state_latest={latest}")
    print(f"latest_exists={str(latest.is_file()).lower()}")
    print("secret_values_printed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
