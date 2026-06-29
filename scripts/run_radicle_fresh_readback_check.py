#!/usr/bin/env python3
"""Check whether the Loop 59 Radicle RID can be read from fresh state.

This is intentionally narrower than a durability guarantee. It uses a new
temporary RAD_HOME and does not connect to the original temporary localhost seed
node recorded in Loop 59. A successful run means only that this fresh run could
clone the recorded RID at the expected commit through Radicle's normal network
path.
"""

from __future__ import annotations

import json
import os
import secrets
import shutil
import subprocess
import tempfile
import textwrap
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_EVIDENCE = ROOT / "evidence" / "radicle-project-repo-smoke-2026-06-29.json"
EVIDENCE_JSON = ROOT / "evidence" / "radicle-fresh-readback-check-2026-06-29.json"
EVIDENCE_MD = ROOT / "evidence" / "radicle-fresh-readback-check-2026-06-29.md"

PASS = "<redacted disposable passphrase>"
REAL_PASS = secrets.token_urlsafe(32)


def run(cmd, cwd=None, env=None, input_text=None, timeout=30, allow_fail=False):
    started = time.time()
    result = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )
    stdout = result.stdout.replace(REAL_PASS, PASS)
    stderr = result.stderr.replace(REAL_PASS, PASS)
    record = {
        "cmd": cmd,
        "cwd": str(cwd) if cwd else None,
        "returncode": result.returncode,
        "stdout": stdout[-12000:],
        "stderr": stderr[-12000:],
        "duration_seconds": round(time.time() - started, 3),
    }
    if result.returncode != 0 and not allow_fail:
        raise RuntimeError(json.dumps(record, indent=2))
    return record


def main() -> int:
    source = json.loads(SOURCE_EVIDENCE.read_text(encoding="utf-8"))
    target_rid = source["rid"]
    expected_commit = source["source_commit"]
    original_seed_node_id = source.get("seed_node_id", "")

    tmp = Path(tempfile.mkdtemp(prefix="df-radicle-fresh-readback-"))
    commands = []
    node_stop_records = []
    try:
        rad_home = tmp / "fresh-rad-home"
        clone_parent = tmp / "clone-parent"
        clone_parent.mkdir(parents=True)
        clone_path = clone_parent / "decentralized-forge-fresh"

        env = os.environ.copy()
        env["PATH"] = f"{env.get('RADICLE_BIN_DIR', Path.home() / '.radicle' / 'bin')}:{env.get('PATH', '')}"
        env["RAD_HOME"] = str(rad_home)
        env["RAD_PASSPHRASE"] = REAL_PASS

        commands.append(run(["rad", "--version"], env=env))
        commands.append(run(["radicle-node", "--version"], env=env))
        commands.append(
            run(
                ["rad", "auth", "--alias", "df-project-fresh-readback", "--stdin"],
                env=env,
                input_text=REAL_PASS + "\n",
                timeout=60,
            )
        )
        node_start = run(["rad", "node", "start", "--", "--listen", "127.0.0.1:8788"], env=env, timeout=60, allow_fail=True)
        commands.append(node_start)
        node_started = node_start["returncode"] == 0
        time.sleep(12)
        node_status = run(["rad", "node", "status"], env=env, timeout=45, allow_fail=True)
        commands.append(node_status)

        clone = run(
            ["rad", "clone", "--timeout", "90s", target_rid, str(clone_path)],
            cwd=clone_parent,
            env=env,
            timeout=180,
            allow_fail=True,
        )
        commands.append(clone)
        clone_succeeded = clone["returncode"] == 0

        clone_commit = ""
        readback_matches = False
        if clone_succeeded:
            clone_commit_record = run(["git", "rev-parse", "HEAD"], cwd=clone_path, allow_fail=True)
            commands.append(clone_commit_record)
            clone_commit = clone_commit_record["stdout"].strip()
            readback_matches = clone_commit == expected_commit and (clone_path / "README.md").exists()

        node_stop_records.append(run(["rad", "node", "stop"], env=env, timeout=30, allow_fail=True))

        fresh_network_readback_observed = bool(node_started and clone_succeeded and readback_matches)
        evidence = {
            "schema_version": "decentralized-forge.radicle-fresh-readback-check.v1",
            "loop": 60,
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "scope": "Fresh-state Radicle readback check for the Loop 59 project RID",
            "source_evidence": "evidence/radicle-project-repo-smoke-2026-06-29.json",
            "target_rid": target_rid,
            "expected_commit": expected_commit,
            "original_seed_node_id": original_seed_node_id,
            "original_seed_profile_reused": False,
            "explicit_original_seed_used": False,
            "temp_state_root_shape": "/tmp/df-radicle-fresh-readback-* (removed after evidence capture)",
            "fresh_rad_home_shape": "/tmp/df-radicle-fresh-readback-*/fresh-rad-home (removed)",
            "node_started": node_started,
            "clone_succeeded": clone_succeeded,
            "clone_commit": clone_commit,
            "readback_commit_matches_expected": readback_matches,
            "fresh_network_readback_observed": fresh_network_readback_observed,
            "verification_passed": fresh_network_readback_observed,
            "commands": commands,
            "node_stop": node_stop_records,
            "actions_not_taken": [
                "no original Loop 59 RAD_HOME or seed repository was reused",
                "no explicit connection to the original Loop 59 seed node was requested",
                "no production/private personal keys were used",
                "no persistent Radicle home or seed state was kept",
                "no paid infrastructure, wallet, spending, or direct outreach was used",
                "no durability, censorship-resistance, security, global replication, identity-trust, or production-readiness claim is made",
            ],
            "claim_boundary": "This records whether one fresh temporary Radicle profile could clone the recorded Loop 59 RID through Radicle's normal network path at the expected commit. It is still not a durability, broad replication, security, identity-trust, or production-readiness guarantee.",
        }
        EVIDENCE_JSON.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
        EVIDENCE_MD.write_text(
            textwrap.dedent(
                f"""
                # Radicle fresh readback check - 2026-06-29

                ## Scope

                Loop 60 checked whether the Loop 59 project RID could be cloned from a brand-new temporary Radicle profile without reusing the original Loop 59 seed profile or explicitly connecting to its original seed node.

                ## Result

                - Target RID: `{target_rid}`
                - Expected commit: `{expected_commit}`
                - Clone commit: `{clone_commit}`
                - Original seed profile reused: `False`
                - Explicit original seed used: `False`
                - Node started: `{node_started}`
                - Clone succeeded: `{clone_succeeded}`
                - Readback commit matched expected: `{readback_matches}`
                - Fresh network readback observed: `{fresh_network_readback_observed}`

                ## Evidence

                Machine-readable command evidence is in `evidence/radicle-fresh-readback-check-2026-06-29.json`.

                ## Non-claims

                This does not prove durability, censorship resistance, security, global replication, identity trust, production readiness, full Radicle compatibility, or long-term availability. It records only this exact fresh-state readback attempt.
                """
            ).lstrip(),
            encoding="utf-8",
        )
        return 0 if fresh_network_readback_observed else 2
    finally:
        try:
            stop_env = os.environ.copy()
            stop_env["PATH"] = f"{stop_env.get('RADICLE_BIN_DIR', Path.home() / '.radicle' / 'bin')}:{stop_env.get('PATH', '')}"
            stop_env["RAD_HOME"] = str(tmp / "fresh-rad-home")
            subprocess.run(["rad", "node", "stop"], env=stop_env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
        except Exception:
            pass
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
