#!/usr/bin/env python3
"""Advance the retained Radicle RID to the current Git commit.

Loop 62 proved a retained project-scoped maintainer lane. This script reuses
that gitignored maintainer state, moves the same RID to the current checkout,
and records whether fresh readback observes the new commit.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import textwrap
import time
from pathlib import Path

import run_radicle_retained_delegate_check as retained

ROOT = Path(__file__).resolve().parents[1]
SOURCE_EVIDENCE = ROOT / "evidence" / "radicle-retained-delegate-check-2026-06-29.json"
EVIDENCE_JSON = ROOT / "evidence" / "radicle-retained-update-check-2026-06-29.json"
EVIDENCE_MD = ROOT / "evidence" / "radicle-retained-update-check-2026-06-29.md"


def command_blob(commands: list[dict]) -> str:
    return "\n".join(
        " ".join(str(part) for part in command.get("cmd", [])) + "\n" + command.get("stdout", "") + "\n" + command.get("stderr", "")
        for command in commands
    ).lower()


def main() -> int:
    retained.REAL_PASS, passphrase_created = retained.load_or_create_passphrase()
    source = json.loads(SOURCE_EVIDENCE.read_text(encoding="utf-8"))
    target_rid = source["rid"]
    prior_commit = source["source_commit"]
    prior_default_readback_commit = source["readback_commit"]

    commands = []
    node_stop_records = []
    readback_tmp = Path(tempfile.mkdtemp(prefix="df-radicle-retained-update-readback-"))
    try:
        env = os.environ.copy()
        env["PATH"] = f"{env.get('RADICLE_BIN_DIR', Path.home() / '.radicle' / 'bin')}:{env.get('PATH', '')}"
        env["RAD_HOME"] = str(retained.RAD_HOME)
        env["RAD_PASSPHRASE"] = retained.REAL_PASS

        commands.append(retained.run(["rad", "--version"], env=env))
        commands.append(retained.run(["radicle-node", "--version"], env=env))
        current_commit_record = retained.run(["git", "-c", f"safe.directory={ROOT}", "rev-parse", "HEAD"], cwd=ROOT)
        commands.append(current_commit_record)
        current_commit = current_commit_record["stdout"].strip()
        ancestor = retained.run(
            ["git", "-c", f"safe.directory={ROOT}", "merge-base", "--is-ancestor", prior_commit, current_commit],
            cwd=ROOT,
            allow_fail=True,
        )
        commands.append(ancestor)
        current_extends_prior = ancestor["returncode"] == 0

        self_record = retained.run(["rad", "self"], env=env, timeout=45, allow_fail=True)
        commands.append(self_record)
        retained_profile_available = self_record["returncode"] == 0
        retained_peer_id = retained.first_nid(self_record["stdout"] + "\n" + self_record["stderr"])

        worktree_matches_source, worktree_commit = retained.ensure_worktree(commands, current_commit)
        rid_record = retained.run(["rad", "inspect", "--rid", str(retained.WORKTREE)], env=env)
        identity_record = retained.run(["rad", "inspect", "--identity", str(retained.WORKTREE)], env=env)
        refs_record = retained.run(["rad", "inspect", "--refs", str(retained.WORKTREE)], env=env)
        visibility_record = retained.run(["rad", "inspect", "--visibility", str(retained.WORKTREE)], env=env)
        commands.extend([rid_record, identity_record, refs_record, visibility_record])
        observed_rid = rid_record["stdout"].strip()
        delegate_did = retained.first_did(identity_record["stdout"])
        same_retained_rid = observed_rid == target_rid

        push_record = retained.run(["git", "push", "rad", "main"], cwd=retained.WORKTREE, env=env, timeout=180, allow_fail=True)
        commands.append(push_record)
        push_succeeded = push_record["returncode"] == 0

        node_start = retained.run(["rad", "node", "start", "--", "--listen", "127.0.0.1:8791"], env=env, timeout=60, allow_fail=True)
        commands.append(node_start)
        node_started = node_start["returncode"] == 0
        time.sleep(3)
        node_status = retained.run(["rad", "node", "status"], env=env, timeout=45, allow_fail=True)
        commands.append(node_status)
        retained_node_id = retained.first_nid(node_status["stdout"] + "\n" + node_status["stderr"])

        publish = retained.run(["rad", "publish", target_rid], env=env, timeout=120, allow_fail=True)
        commands.append(publish)
        publish_succeeded = publish["returncode"] == 0 or "already public" in (publish["stdout"] + publish["stderr"]).lower()

        seed = retained.run(["rad", "seed", target_rid, "--scope", "all", "--no-fetch"], env=env, timeout=90, allow_fail=True)
        commands.append(seed)
        seed_succeeded = seed["returncode"] == 0 or "already" in (seed["stdout"] + seed["stderr"]).lower()

        inventory_sync = retained.run(["rad", "sync", "--inventory"], env=env, timeout=120, allow_fail=True)
        commands.append(inventory_sync)
        inventory_sync_succeeded = inventory_sync["returncode"] == 0 and "error:" not in (
            inventory_sync["stdout"] + inventory_sync["stderr"]
        ).lower()

        sync = retained.run(
            ["rad", "sync", "--announce", "--timeout", "60s", "--replicas", "1", target_rid],
            env=env,
            timeout=150,
            allow_fail=True,
        )
        commands.append(sync)
        sync_succeeded = sync["returncode"] == 0 and "error:" not in (sync["stdout"] + sync["stderr"]).lower()

        time.sleep(15)
        readback_home = readback_tmp / "fresh-update-readback-rad-home"
        readback_parent = readback_tmp / "clone-parent"
        readback_parent.mkdir(parents=True)
        readback_path = readback_parent / "decentralized-forge-retained-update-default-readback"
        direct_readback_path = readback_parent / "decentralized-forge-retained-update-direct-readback"
        readback_env = env.copy()
        readback_env["RAD_HOME"] = str(readback_home)

        commands.append(
            retained.run(
                ["rad", "auth", "--alias", "df-retained-update-readback", "--stdin"],
                env=readback_env,
                input_text=retained.REAL_PASS + "\n",
                timeout=60,
                allow_fail=True,
            )
        )
        readback_node_start = retained.run(
            ["rad", "node", "start", "--", "--listen", "127.0.0.1:8792"],
            env=readback_env,
            timeout=60,
            allow_fail=True,
        )
        commands.append(readback_node_start)
        readback_node_started = readback_node_start["returncode"] == 0
        time.sleep(12)
        commands.append(retained.run(["rad", "node", "status"], env=readback_env, timeout=45, allow_fail=True))

        readback_clone = retained.run(
            ["rad", "clone", "--timeout", "120s", target_rid, str(readback_path)],
            cwd=readback_parent,
            env=readback_env,
            timeout=240,
            allow_fail=True,
        )
        commands.append(readback_clone)
        readback_clone_succeeded = readback_clone["returncode"] == 0
        readback_commit = ""
        readback_branches_output = ""
        if readback_clone_succeeded:
            readback_branches = retained.run(["git", "branch", "-a", "-vv"], cwd=readback_path, allow_fail=True)
            readback_commit_record = retained.run(["git", "rev-parse", "HEAD"], cwd=readback_path, allow_fail=True)
            commands.extend([readback_branches, readback_commit_record])
            readback_branches_output = readback_branches["stdout"]
            readback_commit = readback_commit_record["stdout"].strip()

        direct_connect_succeeded = False
        direct_seed_clone_succeeded = False
        direct_seed_readback_commit = ""
        direct_seed_readback_branches_output = ""
        direct_seed_readback_matches_source = False
        if retained_node_id:
            direct_connect = retained.run(
                ["rad", "node", "connect", f"{retained_node_id}@127.0.0.1:8791", "--timeout", "30s"],
                env=readback_env,
                timeout=45,
                allow_fail=True,
            )
            commands.append(direct_connect)
            direct_connect_succeeded = direct_connect["returncode"] == 0
            direct_clone = retained.run(
                ["rad", "clone", "--timeout", "120s", "--seed", retained_node_id, target_rid, str(direct_readback_path)],
                cwd=readback_parent,
                env=readback_env,
                timeout=240,
                allow_fail=True,
            )
            commands.append(direct_clone)
            direct_seed_clone_succeeded = direct_clone["returncode"] == 0
            if direct_seed_clone_succeeded:
                direct_branches = retained.run(["git", "branch", "-a", "-vv"], cwd=direct_readback_path, allow_fail=True)
                direct_commit = retained.run(["git", "rev-parse", "HEAD"], cwd=direct_readback_path, allow_fail=True)
                commands.extend([direct_branches, direct_commit])
                direct_seed_readback_branches_output = direct_branches["stdout"]
                direct_seed_readback_commit = direct_commit["stdout"].strip()
                direct_seed_readback_matches_source = direct_seed_readback_commit == current_commit

        node_stop_records.append(retained.run(["rad", "node", "stop"], env=readback_env, timeout=30, allow_fail=True))
        node_stop_records.append(retained.run(["rad", "node", "stop"], env=env, timeout=30, allow_fail=True))

        default_readback_matches_source = readback_commit == current_commit
        advanced_from_prior = current_commit != prior_commit and current_extends_prior
        retained.save_state(
            {
                "rid": target_rid,
                "delegate_did": delegate_did,
                "retained_peer_id": retained_peer_id,
                "last_verified_commit": current_commit,
                "last_verified_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
        )

        verification_passed = bool(
            retained_profile_available
            and same_retained_rid
            and advanced_from_prior
            and worktree_matches_source
            and push_succeeded
            and node_started
            and publish_succeeded
            and seed_succeeded
            and readback_node_started
            and (
                (readback_clone_succeeded and default_readback_matches_source)
                or (direct_seed_clone_succeeded and direct_seed_readback_matches_source)
            )
        )
        evidence = {
            "schema_version": "decentralized-forge.radicle-retained-update-check.v1",
            "loop": 63,
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "scope": "Same-RID update through retained project-scoped Radicle maintainer state",
            "source_evidence": "evidence/radicle-retained-delegate-check-2026-06-29.json",
            "target_rid": target_rid,
            "observed_rid": observed_rid,
            "same_retained_rid": same_retained_rid,
            "prior_recorded_commit": prior_commit,
            "prior_default_readback_commit": prior_default_readback_commit,
            "current_source_commit": current_commit,
            "current_extends_prior_recorded_commit": current_extends_prior,
            "advanced_from_prior_recorded_commit": advanced_from_prior,
            "state_root_shape": "<retained-state-root> (local host/WSL state; not committed; not bundled)",
            "secret_values_recorded": False,
            "passphrase_file_created_this_run": passphrase_created,
            "retained_profile_available": retained_profile_available,
            "delegate_did": delegate_did,
            "retained_peer_id": retained_peer_id,
            "retained_node_id": retained_node_id,
            "worktree_commit": worktree_commit,
            "worktree_matches_source": worktree_matches_source,
            "visibility": visibility_record["stdout"].strip(),
            "push_succeeded": push_succeeded,
            "node_started": node_started,
            "publish_succeeded": publish_succeeded,
            "seed_succeeded": seed_succeeded,
            "inventory_sync_succeeded": inventory_sync_succeeded,
            "sync_succeeded": sync_succeeded,
            "readback_node_started": readback_node_started,
            "readback_clone_succeeded": readback_clone_succeeded,
            "readback_commit": readback_commit,
            "readback_branches_output": readback_branches_output,
            "default_readback_matches_source": default_readback_matches_source,
            "direct_seed_node_connect_succeeded": direct_connect_succeeded,
            "direct_seed_clone_succeeded": direct_seed_clone_succeeded,
            "direct_seed_readback_commit": direct_seed_readback_commit,
            "direct_seed_readback_branches_output": direct_seed_readback_branches_output,
            "direct_seed_readback_matches_source": direct_seed_readback_matches_source,
            "verification_passed": verification_passed,
            "commands": commands,
            "node_stop": node_stop_records,
            "actions_not_taken": [
                "no secret passphrase or Radicle key material was written to committed evidence",
                "no production/private personal keys were used",
                "no paid infrastructure, wallet, spending, or direct outreach was used",
                "no persistent public seed service was kept running after verification",
                "no permanent durability, censorship-resistance, security, global replication, identity-trust, or production-readiness claim is made",
                "no future default public-routing availability claim is made",
                "no full Radicle compatibility claim is made",
            ],
            "claim_boundary": "This records one retained-RID update: gitignored project-scoped Radicle maintainer state advanced the same RID from the prior recorded commit to the current source commit, and a separate fresh profile read back the current commit. It is not a durability, broad replication, security, identity-trust, or production-readiness guarantee.",
        }
        EVIDENCE_JSON.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

        EVIDENCE_MD.write_text(
            textwrap.dedent(
                f"""
                # Radicle retained update check - 2026-06-29

                ## Scope

                Loop 63 checked whether retained project-scoped Radicle maintainer state could advance the same RID from the Loop 62 commit to the current Git commit.

                ## Result

                - RID: `{target_rid}`
                - Prior recorded commit: `{prior_commit}`
                - Current source commit: `{current_commit}`
                - Advanced from prior commit: `{advanced_from_prior}`
                - Same retained RID observed: `{same_retained_rid}`
                - Retained profile available: `{retained_profile_available}`
                - Worktree matched source: `{worktree_matches_source}`
                - Push succeeded: `{push_succeeded}`
                - Inventory sync succeeded: `{inventory_sync_succeeded}`
                - Sync/announce succeeded: `{sync_succeeded}`
                - Fresh default clone succeeded: `{readback_clone_succeeded}`
                - Fresh default clone commit: `{readback_commit}`
                - Default readback matched source: `{default_readback_matches_source}`
                - Direct seed clone succeeded: `{direct_seed_clone_succeeded}`
                - Direct seed clone commit: `{direct_seed_readback_commit}`
                - Direct seed readback matched source: `{direct_seed_readback_matches_source}`
                - Overall verification passed: `{verification_passed}`

                ## Evidence

                Machine-readable command evidence is in `evidence/radicle-retained-update-check-2026-06-29.json`.

                ## Non-claims

                This does not prove permanent durability, censorship resistance, security, global replication, identity trust, production readiness, full Radicle compatibility, future default public-routing availability, or general Radicle availability. It records only this exact retained-RID update and fresh readback attempt.
                """
            ).lstrip(),
            encoding="utf-8",
        )
        return 0 if verification_passed else 2
    finally:
        for rad_home in (readback_tmp / "fresh-update-readback-rad-home", retained.RAD_HOME):
            try:
                stop_env = os.environ.copy()
                stop_env["PATH"] = f"{stop_env.get('RADICLE_BIN_DIR', Path.home() / '.radicle' / 'bin')}:{stop_env.get('PATH', '')}"
                stop_env["RAD_HOME"] = str(rad_home)
                stop_env["RAD_PASSPHRASE"] = retained.REAL_PASS
                subprocess.run(["rad", "node", "stop"], env=stop_env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
            except Exception:
                pass
        shutil.rmtree(readback_tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
