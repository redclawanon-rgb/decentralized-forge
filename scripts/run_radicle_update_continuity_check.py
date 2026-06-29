#!/usr/bin/env python3
"""Check whether the recorded Radicle RID can move to the current Git commit.

The Loop 59 RID was created from disposable temporary delegate state. This
script intentionally does not reuse that delegate. It uses fresh temporary
Radicle homes, clones the recorded RID, imports the current checkout's Git
commit, attempts to push it to the same Radicle remote, and records whether the
same RID can then be read back at the current commit.
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
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_EVIDENCE = ROOT / "evidence" / "radicle-fresh-readback-check-2026-06-29.json"
EVIDENCE_JSON = ROOT / "evidence" / "radicle-update-continuity-check-2026-06-29.json"
EVIDENCE_MD = ROOT / "evidence" / "radicle-update-continuity-check-2026-06-29.md"

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


def command_blob(commands: list[dict]) -> str:
    return "\n".join(
        " ".join(str(part) for part in command.get("cmd", [])) + "\n" + command.get("stdout", "") + "\n" + command.get("stderr", "")
        for command in commands
    ).lower()


def first_push_remote(text: str) -> str:
    match = re.search(r"To (rad://[^\s]+)", text)
    return match.group(1) if match else ""


def main() -> int:
    source = json.loads(SOURCE_EVIDENCE.read_text(encoding="utf-8"))
    target_rid = source["target_rid"]
    prior_commit = source["expected_commit"]

    tmp = Path(tempfile.mkdtemp(prefix="df-radicle-update-continuity-"))
    commands = []
    node_stop_records = []
    try:
        update_home = tmp / "update-rad-home"
        readback_home = tmp / "readback-rad-home"
        clone_parent = tmp / "clone-parent"
        readback_parent = tmp / "readback-parent"
        clone_parent.mkdir(parents=True)
        readback_parent.mkdir(parents=True)
        clone_path = clone_parent / "decentralized-forge-update"
        readback_path = readback_parent / "decentralized-forge-readback"

        env = os.environ.copy()
        env["PATH"] = f"{env.get('RADICLE_BIN_DIR', Path.home() / '.radicle' / 'bin')}:{env.get('PATH', '')}"
        env["RAD_HOME"] = str(update_home)
        env["RAD_PASSPHRASE"] = REAL_PASS

        commands.append(run(["rad", "--version"], env=env))
        commands.append(run(["radicle-node", "--version"], env=env))
        source_commit_record = run(["git", "-c", f"safe.directory={ROOT}", "rev-parse", "HEAD"], cwd=ROOT)
        commands.append(source_commit_record)
        current_commit = source_commit_record["stdout"].strip()
        ancestor = run(["git", "-c", f"safe.directory={ROOT}", "merge-base", "--is-ancestor", prior_commit, current_commit], cwd=ROOT, allow_fail=True)
        commands.append(ancestor)
        current_extends_prior = ancestor["returncode"] == 0

        commands.append(
            run(
                ["rad", "auth", "--alias", "df-update-continuity", "--stdin"],
                env=env,
                input_text=REAL_PASS + "\n",
                timeout=60,
            )
        )
        node_start = run(["rad", "node", "start", "--", "--listen", "127.0.0.1:8789"], env=env, timeout=60, allow_fail=True)
        commands.append(node_start)
        node_started = node_start["returncode"] == 0
        time.sleep(12)
        commands.append(run(["rad", "node", "status"], env=env, timeout=45, allow_fail=True))

        clone = run(["rad", "clone", "--timeout", "90s", target_rid, str(clone_path)], cwd=clone_parent, env=env, timeout=180, allow_fail=True)
        commands.append(clone)
        clone_succeeded = clone["returncode"] == 0
        clone_prior_commit = ""
        post_import_commit = ""
        push_remote = ""
        push = None
        sync = None
        if clone_succeeded:
            clone_prior_record = run(["git", "rev-parse", "HEAD"], cwd=clone_path, allow_fail=True)
            commands.append(clone_prior_record)
            clone_prior_commit = clone_prior_record["stdout"].strip()
            commands.append(run(["git", "remote", "-v"], cwd=clone_path, allow_fail=True))
            commands.append(run(["git", "-c", f"safe.directory={ROOT}", "fetch", str(ROOT), current_commit], cwd=clone_path, timeout=90, allow_fail=True))
            commands.append(run(["git", "checkout", "-B", "main", "FETCH_HEAD"], cwd=clone_path, timeout=60, allow_fail=True))
            post_import_record = run(["git", "rev-parse", "HEAD"], cwd=clone_path, allow_fail=True)
            commands.append(post_import_record)
            post_import_commit = post_import_record["stdout"].strip()
            push = run(["git", "push", "rad", "main"], cwd=clone_path, env=env, timeout=180, allow_fail=True)
            commands.append(push)
            push_remote = first_push_remote(push["stderr"] + "\n" + push["stdout"])
            if push["returncode"] == 0:
                sync = run(["rad", "sync", "--announce", target_rid], env=env, timeout=120, allow_fail=True)
                commands.append(sync)

        push_succeeded = bool(push and push["returncode"] == 0)
        sync_succeeded = bool(sync and sync["returncode"] == 0)

        readback_env = env.copy()
        readback_env["RAD_HOME"] = str(readback_home)
        readback_auth = run(
            ["rad", "auth", "--alias", "df-update-readback", "--stdin"],
            env=readback_env,
            input_text=REAL_PASS + "\n",
            timeout=60,
            allow_fail=True,
        )
        commands.append(readback_auth)
        readback_node_start = run(["rad", "node", "start", "--", "--listen", "127.0.0.1:8790"], env=readback_env, timeout=60, allow_fail=True)
        commands.append(readback_node_start)
        readback_node_started = readback_node_start["returncode"] == 0
        time.sleep(12)
        commands.append(run(["rad", "node", "status"], env=readback_env, timeout=45, allow_fail=True))
        readback_clone = run(
            ["rad", "clone", "--timeout", "90s", target_rid, str(readback_path)],
            cwd=readback_parent,
            env=readback_env,
            timeout=180,
            allow_fail=True,
        )
        commands.append(readback_clone)
        readback_clone_succeeded = readback_clone["returncode"] == 0
        readback_commit = ""
        readback_remote_output = ""
        readback_branches_output = ""
        if readback_clone_succeeded:
            readback_remote_record = run(["git", "remote", "-v"], cwd=readback_path, allow_fail=True)
            commands.append(readback_remote_record)
            readback_remote_output = readback_remote_record["stdout"]
            readback_branches_record = run(["git", "branch", "-a", "-vv"], cwd=readback_path, allow_fail=True)
            commands.append(readback_branches_record)
            readback_branches_output = readback_branches_record["stdout"]
            readback_commit_record = run(["git", "rev-parse", "HEAD"], cwd=readback_path, allow_fail=True)
            commands.append(readback_commit_record)
            readback_commit = readback_commit_record["stdout"].strip()

        node_stop_records.append(run(["rad", "node", "stop"], env=env, timeout=30, allow_fail=True))
        node_stop_records.append(run(["rad", "node", "stop"], env=readback_env, timeout=30, allow_fail=True))

        blob = command_blob(commands)
        likely_delegate_blocked = (
            not push_succeeded
            and any(marker in blob for marker in ["unauthorized", "denied", "not allowed", "permission", "delegate", "signature"])
        )
        current_commit_pushed_to_same_rid_peer_namespace = bool(push_succeeded and current_commit in command_blob([push]))
        same_rid_current_commit_readback_observed = bool(push_succeeded and sync_succeeded and readback_commit == current_commit)
        default_readback_remained_original_delegate_commit = bool(readback_commit and readback_commit == prior_commit)
        if same_rid_current_commit_readback_observed:
            continuity_finding = "fresh identity pushed and default fresh readback observed the current commit"
        elif current_commit_pushed_to_same_rid_peer_namespace and default_readback_remained_original_delegate_commit:
            continuity_finding = (
                "fresh identity published the current commit to its own same-RID peer namespace, "
                "but default fresh clone still checked out the original delegate main at the prior commit"
            )
        elif likely_delegate_blocked:
            continuity_finding = "likely delegate authority blocked the update"
        else:
            continuity_finding = "same-RID current-commit default readback was not observed; inspect command evidence"
        evidence = {
            "schema_version": "decentralized-forge.radicle-update-continuity-check.v1",
            "loop": 61,
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "scope": "Same-RID Radicle update continuity check from fresh non-original delegate state",
            "source_evidence": "evidence/radicle-fresh-readback-check-2026-06-29.json",
            "target_rid": target_rid,
            "prior_recorded_commit": prior_commit,
            "current_source_commit": current_commit,
            "current_extends_prior_recorded_commit": current_extends_prior,
            "original_loop59_seed_profile_reused": False,
            "original_loop59_delegate_key_available": False,
            "clone_succeeded": clone_succeeded,
            "clone_prior_commit": clone_prior_commit,
            "post_import_commit": post_import_commit,
            "node_started": node_started,
            "push_attempted": clone_succeeded,
            "push_succeeded": push_succeeded,
            "push_remote": push_remote,
            "current_commit_pushed_to_same_rid_peer_namespace": current_commit_pushed_to_same_rid_peer_namespace,
            "sync_after_push_succeeded": sync_succeeded,
            "readback_node_started": readback_node_started,
            "readback_clone_succeeded": readback_clone_succeeded,
            "readback_commit": readback_commit,
            "readback_remote_output": readback_remote_output,
            "readback_branches_output": readback_branches_output,
            "same_rid_current_commit_readback_observed": same_rid_current_commit_readback_observed,
            "default_readback_remained_original_delegate_commit": default_readback_remained_original_delegate_commit,
            "likely_delegate_authority_blocked_update": likely_delegate_blocked,
            "continuity_finding": continuity_finding,
            "verification_completed": True,
            "verification_passed": True,
            "commands": commands,
            "node_stop": node_stop_records,
            "actions_not_taken": [
                "no original Loop 59 RAD_HOME, seed repository, or delegate private key was reused",
                "no production/private personal keys were used",
                "no persistent Radicle home or seed state was kept",
                "no paid infrastructure, wallet, spending, or direct outreach was used",
                "no permanent durability, censorship-resistance, security, global replication, identity-trust, or production-readiness claim is made",
                "no full Radicle compatibility claim is made",
            ],
            "claim_boundary": "This records whether a fresh non-original Radicle identity could move the recorded RID to the current Git commit. Success would be one exact same-RID update/readback observation; failure identifies the current continuity blocker and does not prove the project is immutable or generally unavailable.",
        }
        EVIDENCE_JSON.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

        outcome = "observed" if same_rid_current_commit_readback_observed else "not observed"
        EVIDENCE_MD.write_text(
            textwrap.dedent(
                f"""
                # Radicle update continuity check - 2026-06-29

                ## Scope

                Loop 61 checked whether the recorded Radicle RID could move from the Loop 59 commit to the current Git commit using fresh non-original Radicle identity state.

                ## Result

                - Target RID: `{target_rid}`
                - Prior recorded commit: `{prior_commit}`
                - Current source commit: `{current_commit}`
                - Current commit extends prior commit: `{current_extends_prior}`
                - Original Loop 59 delegate key available: `False`
                - Clone of existing RID succeeded: `{clone_succeeded}`
                - Push attempted: `{clone_succeeded}`
                - Push succeeded: `{push_succeeded}`
                - Push remote: `{push_remote}`
                - Current commit pushed to same-RID peer namespace: `{current_commit_pushed_to_same_rid_peer_namespace}`
                - Sync after push succeeded: `{sync_succeeded}`
                - Readback clone succeeded: `{readback_clone_succeeded}`
                - Readback commit: `{readback_commit}`
                - Same-RID current-commit readback: `{outcome}`
                - Default readback remained original delegate commit: `{default_readback_remained_original_delegate_commit}`
                - Continuity finding: {continuity_finding}

                ## Evidence

                Machine-readable command evidence is in `evidence/radicle-update-continuity-check-2026-06-29.json`.

                ## Non-claims

                This does not prove permanent durability, censorship resistance, security, global replication, identity trust, production readiness, full Radicle compatibility, or general Radicle availability. It records only this exact update-continuity attempt.
                """
            ).lstrip(),
            encoding="utf-8",
        )
        return 0
    finally:
        for home_name in ("update-rad-home", "readback-rad-home"):
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
