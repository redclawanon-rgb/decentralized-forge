#!/usr/bin/env python3
"""Run a bounded Radicle smoke for the current decentralized-forge repo.

The script uses only temporary Radicle homes and a temporary Git clone of this
checkout. It records exact command evidence without preserving private key
material or claiming durability, broad availability, security, or production
readiness.
"""

from __future__ import annotations

import json
import os
import re
import secrets
import shutil
import subprocess
import tempfile
import textwrap
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_JSON = ROOT / "evidence" / "radicle-project-repo-smoke-2026-06-29.json"
EVIDENCE_MD = ROOT / "evidence" / "radicle-project-repo-smoke-2026-06-29.md"

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
        "stdout": stdout[-8000:],
        "stderr": stderr[-8000:],
        "duration_seconds": round(time.time() - started, 3),
    }
    if result.returncode != 0 and not allow_fail:
        raise RuntimeError(json.dumps(record, indent=2))
    return record


def first_nid(text: str) -> str:
    match = re.search(r"\bz6[0-9A-Za-z]{20,}\b", text)
    return match.group(0) if match else ""


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="df-radicle-project-smoke-"))
    commands = []
    node_stop_records = []
    try:
        rad_home = tmp / "seed-rad-home"
        clone_home = tmp / "clone-rad-home"
        seed_repo = tmp / "decentralized-forge-seed"
        clone_parent = tmp / "clone-parent"
        clone_parent.mkdir(parents=True)

        env = os.environ.copy()
        env["PATH"] = f"{env.get('RADICLE_BIN_DIR', Path.home() / '.radicle' / 'bin')}:{env.get('PATH', '')}"
        env["RAD_HOME"] = str(rad_home)
        env["RAD_PASSPHRASE"] = REAL_PASS

        commands.append(run(["rad", "--version"], env=env))
        commands.append(run(["radicle-node", "--version"], env=env))
        source_commit_record = run(["git", "-c", f"safe.directory={ROOT}", "rev-parse", "HEAD"], cwd=ROOT)
        source_commit = source_commit_record["stdout"].strip()
        commands.append(source_commit_record)
        commands.append(
            run(
                [
                    "git",
                    "-c",
                    f"safe.directory={ROOT}",
                    "clone",
                    "--no-hardlinks",
                    str(ROOT),
                    str(seed_repo),
                ],
                timeout=60,
            )
        )
        seed_commit_record = run(["git", "rev-parse", "HEAD"], cwd=seed_repo)
        seed_commit = seed_commit_record["stdout"].strip()
        commands.append(seed_commit_record)

        commands.append(
            run(
                ["rad", "auth", "--alias", "df-project-smoke", "--stdin"],
                env=env,
                input_text=REAL_PASS + "\n",
                timeout=60,
            )
        )
        commands.append(
            run(
                [
                    "rad",
                    "init",
                    "--name",
                    "decentralized-forge",
                    "--description",
                    "Decentralized Forge prototype repository smoke; evidence-scoped, no durability/security/production claims.",
                    "--default-branch",
                    "main",
                    "--public",
                    "--no-confirm",
                    "--no-seed",
                    str(seed_repo),
                ],
                env=env,
                timeout=60,
            )
        )
        rid = run(["rad", "inspect", "--rid", str(seed_repo)], env=env)
        identity = run(["rad", "inspect", "--identity", str(seed_repo)], env=env)
        refs = run(["rad", "inspect", "--refs", str(seed_repo)], env=env)
        visibility = run(["rad", "inspect", "--visibility", str(seed_repo)], env=env)
        commands.extend([rid, identity, refs, visibility])
        rid_value = rid["stdout"].strip()

        node_start = run(["rad", "node", "start", "--", "--listen", "127.0.0.1:8776"], env=env, timeout=60, allow_fail=True)
        commands.append(node_start)
        node_started = node_start["returncode"] == 0
        time.sleep(2)
        node_status = run(["rad", "node", "status"], env=env, timeout=30, allow_fail=True)
        commands.append(node_status)
        seed_nid = first_nid(node_status["stdout"])

        publish = run(["rad", "publish", rid_value], env=env, timeout=90, allow_fail=True)
        commands.append(publish)
        publish_succeeded = publish["returncode"] == 0 or "already public" in (publish["stdout"] + publish["stderr"]).lower()

        seed = run(["rad", "seed", rid_value, "--no-fetch"], env=env, timeout=60, allow_fail=True)
        commands.append(seed)
        seed_succeeded = seed["returncode"] == 0

        sync = run(["rad", "sync", "--announce", rid_value], env=env, timeout=90, allow_fail=True)
        commands.append(sync)
        sync_succeeded = sync["returncode"] == 0

        clone_env = env.copy()
        clone_env["RAD_HOME"] = str(clone_home)
        clone_auth = run(
            ["rad", "auth", "--alias", "df-project-clone", "--stdin"],
            env=clone_env,
            input_text=REAL_PASS + "\n",
            timeout=60,
            allow_fail=True,
        )
        commands.append(clone_auth)
        clone_node_start = run(["rad", "node", "start", "--", "--listen", "127.0.0.1:8777"], env=clone_env, timeout=60, allow_fail=True)
        commands.append(clone_node_start)
        clone_node_started = clone_node_start["returncode"] == 0
        time.sleep(2)
        clone_connect = None
        if seed_nid:
            clone_connect = run(["rad", "node", "connect", f"{seed_nid}@127.0.0.1:8776"], env=clone_env, timeout=30, allow_fail=True)
            commands.append(clone_connect)

        clone_cmd = ["rad", "clone", "--timeout", "30s"]
        if seed_nid:
            clone_cmd.extend(["--seed", seed_nid])
        clone_cmd.extend([rid_value, str(clone_parent / "decentralized-forge-clone")])
        clone = run(clone_cmd, cwd=clone_parent, env=clone_env, timeout=150, allow_fail=True)
        commands.append(clone)
        clone_succeeded = clone["returncode"] == 0

        clone_commit = ""
        readback_matches = False
        if clone_succeeded:
            cloned_repo = clone_parent / "decentralized-forge-clone"
            clone_commit_record = run(["git", "rev-parse", "HEAD"], cwd=cloned_repo, allow_fail=True)
            commands.append(clone_commit_record)
            clone_commit = clone_commit_record["stdout"].strip()
            readback_matches = clone_commit == source_commit and (cloned_repo / "README.md").exists()

        node_stop_records.append(run(["rad", "node", "stop"], env=env, timeout=30, allow_fail=True))
        node_stop_records.append(run(["rad", "node", "stop"], env=clone_env, timeout=30, allow_fail=True))

        verification_passed = bool(
            source_commit
            and seed_commit == source_commit
            and rid_value.startswith("rad:z")
            and node_started
            and publish_succeeded
            and seed_succeeded
            and sync_succeeded
            and clone_node_started
            and clone_succeeded
            and readback_matches
        )
        evidence = {
            "schema_version": "decentralized-forge.radicle-project-repo-smoke.v1",
            "loop": 59,
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "scope": "Project-scoped Radicle repository smoke for decentralized-forge",
            "permission": "User approved continuing toward the first decentralized repo; actions stayed disposable, project-scoped, and evidence-labeled.",
            "temp_state_root_shape": "/tmp/df-radicle-project-smoke-* (removed after evidence capture)",
            "rad_home_shape": "/tmp/df-radicle-project-smoke-*/seed-rad-home (removed)",
            "clone_rad_home_shape": "/tmp/df-radicle-project-smoke-*/clone-rad-home (removed)",
            "source_repo": "current decentralized-forge checkout",
            "source_commit": source_commit,
            "seed_repo_commit": seed_commit,
            "rid": rid_value,
            "visibility": visibility["stdout"].strip(),
            "seed_node_id": seed_nid,
            "clone_commit": clone_commit,
            "node_started": node_started,
            "publish_succeeded": publish_succeeded,
            "seed_succeeded": seed_succeeded,
            "sync_succeeded": sync_succeeded,
            "clone_node_started": clone_node_started,
            "clone_node_connected_to_seed": bool(clone_connect and clone_connect["returncode"] == 0),
            "remote_clone_succeeded": clone_succeeded,
            "readback_commit_matches_source": readback_matches,
            "verification_passed": verification_passed,
            "commands": commands,
            "node_stop": node_stop_records,
            "actions_not_taken": [
                "no production/private personal keys were used",
                "no persistent Radicle home or seed state was kept",
                "no paid infrastructure, wallet, spending, or direct outreach was used",
                "no durability, censorship-resistance, security, global replication, identity-trust, or production-readiness claim is made",
                "no broad Radicle network availability claim is made beyond this exact bounded smoke evidence",
            ],
            "claim_boundary": "This proves only that the current decentralized-forge commit was initialized as a public Radicle repository, seeded from disposable temporary state, and cloned/read back by a separate temporary Radicle profile during this run.",
        }
        EVIDENCE_JSON.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
        EVIDENCE_MD.write_text(
            textwrap.dedent(
                f"""
                # Radicle project repository smoke - 2026-06-29

                ## Scope

                Loop 59 created a project-scoped public Radicle repository from the current decentralized-forge checkout using temporary Radicle homes only. The seed and clone profiles were removed after evidence capture.

                ## Result

                - RID: `{rid_value}`
                - Source commit: `{source_commit}`
                - Clone commit: `{clone_commit}`
                - Visibility: `{visibility['stdout'].strip()}`
                - Node started: `{node_started}`
                - Publish succeeded: `{publish_succeeded}`
                - Seed succeeded: `{seed_succeeded}`
                - Sync/announce command succeeded: `{sync_succeeded}`
                - Separate temporary-profile clone succeeded: `{clone_succeeded}`
                - Readback commit matched source: `{readback_matches}`
                - Overall verification passed: `{verification_passed}`

                ## Evidence

                Machine-readable command evidence is in `evidence/radicle-project-repo-smoke-2026-06-29.json`.

                ## Non-claims

                This does not prove durability, censorship resistance, security, global replication, identity trust, production readiness, full Radicle compatibility, or long-term availability. It records only the exact project-scoped Radicle smoke behavior above.
                """
            ).lstrip(),
            encoding="utf-8",
        )
        return 0 if verification_passed else 2
    finally:
        for home_name in ("seed-rad-home", "clone-rad-home"):
            try:
                stop_env = os.environ.copy()
                stop_env["PATH"] = f"{stop_env.get('RADICLE_BIN_DIR', Path.home() / '.radicle' / 'bin')}:{stop_env.get('PATH', '')}"
                stop_env["RAD_HOME"] = str(tmp / home_name)
                subprocess.run(["rad", "node", "stop"], env=stop_env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
            except Exception:
                pass
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
