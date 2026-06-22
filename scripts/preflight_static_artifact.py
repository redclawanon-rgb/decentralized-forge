#!/usr/bin/env python3
"""Preflight checks for the generated static demo artifact.

This script is intentionally stdlib-only. It verifies that output/demo-project.html
exists, is byte-for-byte current with the renderer and local fixtures, contains the
expected local/synthetic boundary sections, and does not contain selected
unsupported claim phrases.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "output" / "demo-project.html"
RENDERER = ROOT / "scripts" / "render_project_page.py"
REGISTRY_FIXTURE = ROOT / "fixtures" / "example-project.registry.json"
NIP34_REPO_FIXTURE = ROOT / "fixtures" / "nostr-repo-announcement.json"
NIP34_COLLAB_FIXTURE = ROOT / "fixtures" / "nostr-collaboration-events.json"
NIP34_STATE_STATUS_FIXTURE = ROOT / "fixtures" / "nostr-repo-state-status.json"

RENDER_COMMAND = [
    sys.executable,
    str(RENDERER),
    str(REGISTRY_FIXTURE),
    "{output}",
    "--nip34-repo-fixture",
    str(NIP34_REPO_FIXTURE),
    "--nip34-collaboration-fixture",
    str(NIP34_COLLAB_FIXTURE),
    "--nip34-state-status-fixture",
    str(NIP34_STATE_STATUS_FIXTURE),
]

REQUIRED_PHRASES = [
    "Prototype boundary",
    "does not claim production readiness",
    "Verification states",
    "Registry verification states summary",
    "Live-verified row count</dt><dd><code>0</code></dd>",
    "NIP-34 fixture adapter",
    "No relay publishing, signing, fixture ID replacement, relay fetching, or live verification is performed or claimed",
    "Adapter verification states summary",
    "Local NIP-34 conformance summary",
    "Possible event ID (local reference only)",
    "Repository state fixture",
    "Fixture-only status/check projections",
]

# Phrases below would be over-claims if they appeared in the generated artifact.
# Deliberately avoid negated phrases that the renderer uses for boundary wording,
# such as "does not claim production readiness" or "No SLSA level claimed".
FORBIDDEN_PHRASES = [
    "production-ready decentralized forge",
    "censorship proof",
    "censorship-proof guarantee",
    "relay-accepted live event",
    "signed release verified by sigstore",
    "slsa compliant",
    "durably stored on ipfs",
    "pinned and available on ipfs",
]


def render_to(path: Path) -> subprocess.CompletedProcess[str]:
    command = [part.format(output=str(path)) for part in RENDER_COMMAND]
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def check_static_artifact(output_path: Path = DEFAULT_OUTPUT) -> list[str]:
    """Return a list of preflight failure messages for output_path."""
    failures: list[str] = []

    if not output_path.is_file():
        return [f"missing generated artifact: {output_path}"]

    html = output_path.read_text(encoding="utf-8")

    for phrase in REQUIRED_PHRASES:
        if phrase not in html:
            failures.append(f"required phrase missing from artifact: {phrase}")

    lower_html = html.lower()
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in lower_html:
            failures.append(f"unsupported claim phrase present in artifact: {phrase}")

    with tempfile.TemporaryDirectory() as tmpdir:
        regenerated = Path(tmpdir) / "demo-project.html"
        result = render_to(regenerated)
        if result.returncode != 0:
            failures.append(
                "renderer command failed while checking freshness: "
                f"exit={result.returncode}; stderr={result.stderr.strip()}"
            )
        elif regenerated.read_text(encoding="utf-8") != html:
            failures.append(
                "generated artifact is stale: rerun scripts/render_project_page.py "
                "with all optional NIP-34 fixtures"
            )

    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Preflight output/demo-project.html before public release/push.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="generated HTML artifact to check (default: output/demo-project.html)",
    )
    args = parser.parse_args(argv)

    failures = check_static_artifact(Path(args.output).resolve())
    if failures:
        print("Static artifact preflight failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Static artifact preflight passed: {Path(args.output)}")
    print("- artifact exists and matches regenerated renderer output")
    print("- required local/synthetic/non-claim sections are present")
    print("- selected unsupported live/protocol/security/durability claim phrases are absent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
