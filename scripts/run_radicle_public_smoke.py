#!/usr/bin/env python3
"""Run one disposable Permission-G Radicle public seed/clone smoke.

This script is intentionally project-scoped and evidence-oriented. It uses only
/tmp disposable state, never prints the disposable passphrase, and records a
bounded JSON/Markdown result under evidence/.
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
EVIDENCE_JSON = ROOT / "evidence" / "radicle-public-network-smoke-2026-06-22.json"
EVIDENCE_MD = ROOT / "evidence" / "radicle-public-network-smoke-2026-06-22.md"

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
        "stdout": stdout[-6000:],
        "stderr": stderr[-6000:],
        "duration_seconds": round(time.time() - started, 3),
    }
    if result.returncode != 0 and not allow_fail:
        raise RuntimeError(json.dumps(record, indent=2))
    return record


def main():
    tmp = Path(tempfile.mkdtemp(prefix="df-radicle-public-smoke-"))
    node_stop_records = []
    commands = []
    cleanup_removed = False
    try:
        rad_home = tmp / "rad-home"
        repo = tmp / "seed-repo"
        clone_home = tmp / "clone-rad-home"
        clone_parent = tmp / "clone-parent"
        clone_parent.mkdir(parents=True)
        env = os.environ.copy()
        env["PATH"] = f"{Path.home() / '.local/bin'}:{env.get('PATH','')}"
        env["RAD_HOME"] = str(rad_home)
        env["RAD_PASSPHRASE"] = REAL_PASS

        commands.append(run(["bash", "-lc", "command -v rad"], env=env, allow_fail=True))
        commands.append(run(["rad", "--version"], env=env))
        commands.append(run(["git", "init", "-b", "master", str(repo)]))
        readme = repo / "README.md"
        readme.write_text(
            "# Decentralized Forge disposable Radicle public smoke\n\n"
            "This repository is a disposable prototype/research smoke fixture created by Harry on 2026-06-22.\n"
            "It is not production infrastructure and does not claim durability, censorship resistance, security, or availability.\n",
            encoding="utf-8",
        )
        commands.append(run(["git", "add", "README.md"], cwd=repo))
        commands.append(run(["git", "-c", "user.name=Harry Radicle Smoke", "-c", "user.email=harry@example.invalid", "commit", "-m", "docs: disposable radicle public smoke fixture"], cwd=repo))
        git_commit = commands[-1]["stdout"].strip().splitlines()[-1] if commands[-1]["stdout"].strip() else ""

        commands.append(run(["rad", "auth", "--alias", "decentralized-forge-public-smoke", "--stdin"], env=env, input_text=REAL_PASS + "\n", timeout=60))
        commands.append(run([
            "rad", "init",
            "--name", "decentralized-forge-public-smoke-2026-06-22",
            "--description", "Disposable Decentralized Forge prototype/research public Radicle smoke; no durability/security/production claims.",
            "--default-branch", "master",
            "--public",
            "--no-confirm",
            "--no-seed",
            str(repo),
        ], env=env, timeout=60))
        rid = run(["rad", "inspect", "--rid", str(repo)], env=env)
        identity = run(["rad", "inspect", "--identity", str(repo)], env=env)
        refs = run(["rad", "inspect", "--refs", str(repo)], env=env)
        visibility = run(["rad", "inspect", "--visibility", str(repo)], env=env)
        commands.extend([rid, identity, refs, visibility])
        rid_value = rid["stdout"].strip()

        # Start the node as a daemon in the temporary RAD_HOME. Bind localhost only:
        # this smoke tests publish/seed/clone through local node plumbing without
        # exposing a public listening socket or contacting named people.
        commands.append(run(["rad", "node", "start", "--", "--listen", "127.0.0.1:8776"], env=env, timeout=60, allow_fail=True))
        node_started = commands[-1]["returncode"] == 0
        time.sleep(2)
        node_status = run(["rad", "node", "status"], env=env, timeout=30, allow_fail=True)
        commands.append(node_status)

        publish = run(["rad", "publish", rid_value], env=env, timeout=90, allow_fail=True)
        commands.append(publish)
        publish_succeeded = publish["returncode"] == 0 or "repository is already public" in publish["stdout"].lower()

        seed = run(["rad", "seed", rid_value, "--no-fetch"], env=env, timeout=60, allow_fail=True)
        commands.append(seed)
        seed_succeeded = seed["returncode"] == 0

        sync = run(["rad", "sync", "--announce", rid_value], env=env, timeout=90, allow_fail=True)
        commands.append(sync)
        sync_succeeded = sync["returncode"] == 0

        clone_env = env.copy()
        clone_env["RAD_HOME"] = str(clone_home)
        clone_auth = run(["rad", "auth", "--alias", "df-public-smoke-clone", "--stdin"], env=clone_env, input_text=REAL_PASS + "\n", timeout=60, allow_fail=True)
        commands.append(clone_auth)
        clone_node_start = run(["rad", "node", "start", "--", "--listen", "127.0.0.1:8777"], env=clone_env, timeout=60, allow_fail=True)
        commands.append(clone_node_start)
        time.sleep(2)
        clone_node_started = clone_node_start["returncode"] == 0
        clone_connect = None
        # Try explicit local path first is not a network proof, so do not use it.
        # For the separate temporary profile, connect to the disposable seed over localhost
        # and then use the seed NID accepted by `rad clone --seed`.
        seed_nid = ""
        for line in node_status["stdout"].splitlines():
            if "Node ID" in line or "Node" in line and "z6" in line:
                for part in line.replace(":", " ").split():
                    if part.startswith("z6"):
                        seed_nid = part
                        break
            if seed_nid:
                break
        if seed_nid:
            clone_connect = run(["rad", "node", "connect", f"{seed_nid}@127.0.0.1:8776"], env=clone_env, timeout=30, allow_fail=True)
            commands.append(clone_connect)
        clone_cmd = ["rad", "clone", "--timeout", "20s"]
        if seed_nid:
            clone_cmd.extend(["--seed", seed_nid])
        clone_cmd.extend([rid_value, str(clone_parent / "cloned-repo")])
        clone = run(clone_cmd, cwd=clone_parent, env=clone_env, timeout=120, allow_fail=True)
        commands.append(clone)
        clone_succeeded = clone["returncode"] == 0

        readback = None
        readme_matches = False
        if clone_succeeded:
            candidates = list(clone_parent.glob("*/README.md"))
            if candidates:
                readback = candidates[0].read_text(encoding="utf-8")
                readme_matches = "disposable prototype/research smoke fixture" in readback

        node_stop_records.append(run(["rad", "node", "stop"], env=env, timeout=30, allow_fail=True))
        node_stop_records.append(run(["rad", "node", "stop"], env=clone_env, timeout=30, allow_fail=True))

        verification_passed = bool(node_started and publish_succeeded and seed_succeeded and sync_succeeded and clone_node_started and clone_succeeded and readme_matches)
        evidence = {
            "schema_version": "decentralized-forge.radicle-public-network-smoke.v1",
            "loop": 34,
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "scope": "Permission G disposable public Radicle seed/remote-clone smoke",
            "permission": "Permission G approved 2026-06-22 for one disposable public Radicle seed/remote-clone smoke using only disposable/project-scoped state.",
            "temp_state_root_shape": "/tmp/df-radicle-public-smoke-* (removed after evidence capture)",
            "rad_home_shape": "/tmp/df-radicle-public-smoke-*/rad-home (removed)",
            "clone_rad_home_shape": "/tmp/df-radicle-public-smoke-*/clone-rad-home (removed)",
            "rid": rid_value,
            "visibility": visibility["stdout"].strip(),
            "disposable_git_commit_summary": git_commit,
            "node_started": node_started,
            "node_status_returncode": node_status["returncode"],
            "publish_succeeded": publish_succeeded,
            "seed_succeeded": seed_succeeded,
            "sync_succeeded": sync_succeeded,
            "clone_node_started": clone_node_started,
            "clone_node_connected_to_seed": bool(clone_connect and clone_connect["returncode"] == 0),
            "remote_clone_succeeded": clone_succeeded,
            "readme_readback_matches": readme_matches,
            "verification_passed": verification_passed,
            "commands": commands,
            "node_stop": node_stop_records,
            "actions_not_taken": [
                "no production/private personal keys were used",
                "no paid infrastructure or spending was used",
                "no direct outreach or named peer targeting was used",
                "no durability, censorship-resistance, security, global replication, identity-trust, or production-readiness claim is made",
                "no broad Radicle network availability claim is made beyond this exact bounded smoke evidence"
            ],
            "claim_boundary": "This is a disposable prototype Radicle smoke only. It proves only the exact command outcomes recorded here at this time."
        }
        EVIDENCE_JSON.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
        EVIDENCE_MD.write_text(textwrap.dedent(f"""
            # Radicle public-network smoke — 2026-06-22

            ## Scope

            Loop 34 ran under Permission G for one disposable public Radicle seed/remote-clone smoke. It used temporary `/tmp/df-radicle-public-smoke-*` state only, with no production/private personal keys, no paid infrastructure, no spending, and no direct outreach.

            ## Result

            - RID: `{rid_value}`
            - Visibility: `{visibility['stdout'].strip()}`
            - Node started: `{node_started}`
            - Publish succeeded: `{publish_succeeded}`
            - Seed succeeded: `{seed_succeeded}`
            - Sync/announce command succeeded: `{sync_succeeded}`
            - Separate temporary-state `rad clone` succeeded: `{clone_succeeded}`
            - README readback matched disposable fixture text: `{readme_matches}`
            - Overall verification passed: `{verification_passed}`

            ## Evidence

            Machine-readable command evidence is in `evidence/radicle-public-network-smoke-2026-06-22.json`.

            ## Non-claims

            This does not prove durability, censorship resistance, security, global replication, identity trust, production readiness, full Radicle compatibility, or long-term availability. It records only the exact disposable smoke behavior above.
        """).lstrip(), encoding="utf-8")
        if not verification_passed:
            return 2
        return 0
    finally:
        try:
            env = os.environ.copy()
            env["RAD_HOME"] = str(tmp / "rad-home")
            env["PATH"] = f"{Path.home() / '.local/bin'}:{env.get('PATH','')}"
            subprocess.run(["rad", "node", "stop"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
        except Exception:
            pass
        shutil.rmtree(tmp, ignore_errors=True)
        cleanup_removed = True


if __name__ == "__main__":
    raise SystemExit(main())
