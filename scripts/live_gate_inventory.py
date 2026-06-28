#!/usr/bin/env python3
"""Inventory optional live-integration tooling without taking live actions."""

from __future__ import annotations

import argparse
import json
import platform
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TOOL_GROUPS = {
    "ipfs_storage": ["ipfs", "kubo", "ipfs-car", "car", "ipld", "cid", "ipget"],
    "nostr": ["nak", "nostril", "strfry", "nostr-rs-relay"],
    "radicle": ["rad"],
    "signing_provenance": ["cosign", "gitsign", "openssl"],
}

NEXT_GATES = {
    "ipfs_storage": "Explicit live-storage target required before daemon start, add, fetch, gateway, pinning, wallet, paid storage, or durability claims.",
    "nostr": "Disposable project-scoped key target required before any new publish; readback checks must stay low-volume and evidence-scoped.",
    "radicle": "Explicit target required before repeated or broader public-network checks, persistent seed operation, or stronger availability claims.",
    "signing_provenance": "Disposable or keyless test-signing target required before replacing synthetic provenance with verified signing evidence.",
}


def inventory() -> dict:
    groups = {}
    for group, commands in TOOL_GROUPS.items():
        found = {command: shutil.which(command) for command in commands}
        groups[group] = {
            "commands": found,
            "available_commands": sorted(command for command, path in found.items() if path),
            "missing_commands": sorted(command for command, path in found.items() if not path),
            "next_gate": NEXT_GATES[group],
        }

    return {
        "schema_version": "decentralized-forge.live-gate-inventory.v1",
        "created_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "host": {
            "system": platform.system(),
            "release": platform.release(),
            "python": platform.python_version(),
        },
        "scope": "local tool inventory only",
        "groups": groups,
        "actions_not_taken": [
            "no IPFS daemon was started",
            "no IPFS add/fetch/pin/gateway command was run",
            "no Nostr event was signed, published, or read back",
            "no Radicle node, seed, sync, publish, clone, or remote command was run",
            "no signing key, production/private personal key, wallet, paid infrastructure, direct outreach, or spending was used",
            "no durability, censorship-resistance, security, identity-trust, broad-availability, or production-readiness claim is made"
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional path to write inventory JSON")
    args = parser.parse_args(argv)

    payload = inventory()
    text = f"{json.dumps(payload, indent=2, sort_keys=True)}\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print(f"wrote live gate inventory: {args.output}")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
