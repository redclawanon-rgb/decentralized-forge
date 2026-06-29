#!/usr/bin/env python3
"""Check whether a second independent Radicle profile can serve the retained RID.

Loop 63 proved retained maintainer direct-seed readback for one updated commit.
This loop advances the same retained RID to the current checkout, then uses two
fresh Radicle profiles: reader A clones from the retained maintainer seed and
seeds the RID, while reader B clones from reader A. That is still not durable
availability, but it is a materially stronger usability signal than a single
maintainer-only direct-seed clone.
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

import run_radicle_retained_delegate_check as retained

ROOT = Path(__file__).resolve().parents[1]
SOURCE_EVIDENCE = ROOT / "evidence" / "radicle-retained-update-check-2026-06-29.json"
EVIDENCE_JSON = ROOT / "evidence" / "radicle-independent-availability-check-2026-06-29.json"
EVIDENCE_MD = ROOT / "evidence" / "radicle-independent-availability-check-2026-06-29.md"


def scrub_record(record: dict, extra_secrets: list[str]) -> dict:
    scrubbed = json.loads(json.dumps(record))
    for key in ("stdout", "stderr", "cwd"):
        value = scrubbed.get(key)
        if isinstance(value, str):
            for secret in extra_secrets:
                if secret:
                    value = value.replace(secret, "<redacted local reader passphrase>")
            scrubbed[key] = value
    return scrubbed


def run_record(commands: list[dict], cmd: list[str], *, env=None, cwd=None, input_text=None, timeout=30, allow_fail=False, secrets_to_scrub=None) -> dict:
    record = retained.run(cmd, env=env, cwd=cwd, input_text=input_text, timeout=timeout, allow_fail=allow_fail)
    record = scrub_record(record, secrets_to_scrub or [])
    commands.append(record)
    return record


def stop_node(env: dict) -> None:
    try:
        subprocess.run(["rad", "node", "stop"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
    except Exception:
        pass


def git_head(path: Path, commands: list[dict]) -> str:
    record = run_record(commands, ["git", "rev-parse", "HEAD"], cwd=path, allow_fail=True)
    return record["stdout"].strip() if record["returncode"] == 0 else ""


def main() -> int:
    retained.REAL_PASS, retained_passphrase_created = retained.load_or_create_passphrase()
    source = json.loads(SOURCE_EVIDENCE.read_text(encoding="utf-8"))
    target_rid = source["target_rid"]
    prior_verified_commit = source["current_source_commit"]

    commands: list[dict] = []
    node_stop_records: list[dict] = []
    tmp = Path(tempfile.mkdtemp(prefix="df-radicle-independent-availability-"))
    reader_a_pass = secrets.token_urlsafe(32)
    reader_b_pass = secrets.token_urlsafe(32)
    secrets_to_scrub = [reader_a_pass, reader_b_pass]

    maintainer_env = os.environ.copy()
    maintainer_env["PATH"] = f"{maintainer_env.get('RADICLE_BIN_DIR', Path.home() / '.radicle' / 'bin')}:{maintainer_env.get('PATH', '')}"
    maintainer_env["RAD_HOME"] = str(retained.RAD_HOME)
    maintainer_env["RAD_PASSPHRASE"] = retained.REAL_PASS

    reader_a_home = tmp / "reader-a-rad-home"
    reader_b_home = tmp / "reader-b-rad-home"
    reader_a_parent = tmp / "reader-a-clone-parent"
    reader_b_parent = tmp / "reader-b-clone-parent"
    reader_a_clone = reader_a_parent / "decentralized-forge-reader-a"
    reader_b_clone = reader_b_parent / "decentralized-forge-reader-b"
    reader_a_parent.mkdir(parents=True)
    reader_b_parent.mkdir(parents=True)

    reader_a_env = maintainer_env.copy()
    reader_a_env["RAD_HOME"] = str(reader_a_home)
    reader_a_env["RAD_PASSPHRASE"] = reader_a_pass
    reader_b_env = maintainer_env.copy()
    reader_b_env["RAD_HOME"] = str(reader_b_home)
    reader_b_env["RAD_PASSPHRASE"] = reader_b_pass

    try:
        run_record(commands, ["rad", "--version"], env=maintainer_env)
        run_record(commands, ["radicle-node", "--version"], env=maintainer_env)
        current_record = run_record(
            commands,
            ["git", "-c", f"safe.directory={ROOT}", "rev-parse", "HEAD"],
            cwd=ROOT,
        )
        current_commit = current_record["stdout"].strip()
        ancestor = run_record(
            commands,
            ["git", "-c", f"safe.directory={ROOT}", "merge-base", "--is-ancestor", prior_verified_commit, current_commit],
            cwd=ROOT,
            allow_fail=True,
        )
        current_extends_prior = ancestor["returncode"] == 0

        self_record = run_record(commands, ["rad", "self"], env=maintainer_env, timeout=45, allow_fail=True)
        retained_profile_available = self_record["returncode"] == 0
        retained_peer_id = retained.first_nid(self_record["stdout"] + "\n" + self_record["stderr"])

        worktree_matches_source, worktree_commit = retained.ensure_worktree(commands, current_commit)
        rid_record = run_record(commands, ["rad", "inspect", "--rid", str(retained.WORKTREE)], env=maintainer_env)
        identity_record = run_record(commands, ["rad", "inspect", "--identity", str(retained.WORKTREE)], env=maintainer_env)
        visibility_record = run_record(commands, ["rad", "inspect", "--visibility", str(retained.WORKTREE)], env=maintainer_env)
        observed_rid = rid_record["stdout"].strip()
        delegate_did = retained.first_did(identity_record["stdout"])
        same_retained_rid = observed_rid == target_rid

        push = run_record(commands, ["git", "push", "rad", "main"], cwd=retained.WORKTREE, env=maintainer_env, timeout=180, allow_fail=True)
        push_succeeded = push["returncode"] == 0

        maintainer_node_start = run_record(
            commands,
            ["rad", "node", "start", "--", "--listen", "127.0.0.1:8796"],
            env=maintainer_env,
            timeout=60,
            allow_fail=True,
        )
        maintainer_node_started = maintainer_node_start["returncode"] == 0
        time.sleep(3)
        maintainer_node_status = run_record(commands, ["rad", "node", "status"], env=maintainer_env, timeout=45, allow_fail=True)
        maintainer_node_id = retained.first_nid(maintainer_node_status["stdout"] + "\n" + maintainer_node_status["stderr"])

        publish = run_record(commands, ["rad", "publish", target_rid], env=maintainer_env, timeout=120, allow_fail=True)
        publish_succeeded = publish["returncode"] == 0 or "already public" in (publish["stdout"] + publish["stderr"]).lower()
        maintainer_seed = run_record(commands, ["rad", "seed", target_rid, "--scope", "all", "--no-fetch"], env=maintainer_env, timeout=90, allow_fail=True)
        maintainer_seed_succeeded = maintainer_seed["returncode"] == 0 or "already" in (maintainer_seed["stdout"] + maintainer_seed["stderr"]).lower()
        maintainer_sync = run_record(
            commands,
            ["rad", "sync", "--announce", "--timeout", "60s", "--replicas", "1", target_rid],
            env=maintainer_env,
            timeout=150,
            allow_fail=True,
        )
        maintainer_sync_succeeded = maintainer_sync["returncode"] == 0 and "error:" not in (
            maintainer_sync["stdout"] + maintainer_sync["stderr"]
        ).lower()

        run_record(
            commands,
            ["rad", "auth", "--alias", "df-independent-reader-a", "--stdin"],
            env=reader_a_env,
            input_text=reader_a_pass + "\n",
            timeout=60,
            allow_fail=True,
            secrets_to_scrub=secrets_to_scrub,
        )
        reader_a_node_start = run_record(
            commands,
            ["rad", "node", "start", "--", "--listen", "127.0.0.1:8797"],
            env=reader_a_env,
            timeout=60,
            allow_fail=True,
            secrets_to_scrub=secrets_to_scrub,
        )
        reader_a_node_started = reader_a_node_start["returncode"] == 0
        time.sleep(8)
        reader_a_status = run_record(commands, ["rad", "node", "status"], env=reader_a_env, timeout=45, allow_fail=True, secrets_to_scrub=secrets_to_scrub)
        reader_a_node_id = retained.first_nid(reader_a_status["stdout"] + "\n" + reader_a_status["stderr"])
        reader_a_connect = run_record(
            commands,
            ["rad", "node", "connect", f"{maintainer_node_id}@127.0.0.1:8796", "--timeout", "30s"],
            env=reader_a_env,
            timeout=45,
            allow_fail=True,
            secrets_to_scrub=secrets_to_scrub,
        )
        reader_a_connected_to_maintainer = reader_a_connect["returncode"] == 0
        reader_a_direct_clone = run_record(
            commands,
            ["rad", "clone", "--timeout", "120s", "--seed", maintainer_node_id, target_rid, str(reader_a_clone)],
            cwd=reader_a_parent,
            env=reader_a_env,
            timeout=240,
            allow_fail=True,
            secrets_to_scrub=secrets_to_scrub,
        )
        reader_a_clone_succeeded = reader_a_direct_clone["returncode"] == 0
        reader_a_commit = git_head(reader_a_clone, commands) if reader_a_clone_succeeded else ""
        reader_a_matches_source = reader_a_commit == current_commit

        follower_seed = run_record(commands, ["rad", "seed", target_rid, "--scope", "all", "--no-fetch"], env=reader_a_env, timeout=90, allow_fail=True, secrets_to_scrub=secrets_to_scrub)
        follower_seed_succeeded = follower_seed["returncode"] == 0 or "already" in (follower_seed["stdout"] + follower_seed["stderr"]).lower()
        follower_sync = run_record(
            commands,
            ["rad", "sync", "--announce", "--timeout", "60s", "--replicas", "1", target_rid],
            env=reader_a_env,
            timeout=150,
            allow_fail=True,
            secrets_to_scrub=secrets_to_scrub,
        )
        follower_sync_succeeded = follower_sync["returncode"] == 0 and "error:" not in (
            follower_sync["stdout"] + follower_sync["stderr"]
        ).lower()

        run_record(
            commands,
            ["rad", "auth", "--alias", "df-independent-reader-b", "--stdin"],
            env=reader_b_env,
            input_text=reader_b_pass + "\n",
            timeout=60,
            allow_fail=True,
            secrets_to_scrub=secrets_to_scrub,
        )
        reader_b_node_start = run_record(
            commands,
            ["rad", "node", "start", "--", "--listen", "127.0.0.1:8798"],
            env=reader_b_env,
            timeout=60,
            allow_fail=True,
            secrets_to_scrub=secrets_to_scrub,
        )
        reader_b_node_started = reader_b_node_start["returncode"] == 0
        time.sleep(8)
        run_record(commands, ["rad", "node", "status"], env=reader_b_env, timeout=45, allow_fail=True, secrets_to_scrub=secrets_to_scrub)
        reader_b_connect = run_record(
            commands,
            ["rad", "node", "connect", f"{reader_a_node_id}@127.0.0.1:8797", "--timeout", "30s"],
            env=reader_b_env,
            timeout=45,
            allow_fail=True,
            secrets_to_scrub=secrets_to_scrub,
        )
        reader_b_connected_to_follower = reader_b_connect["returncode"] == 0
        reader_b_clone_record = run_record(
            commands,
            ["rad", "clone", "--timeout", "120s", "--seed", reader_a_node_id, target_rid, str(reader_b_clone)],
            cwd=reader_b_parent,
            env=reader_b_env,
            timeout=240,
            allow_fail=True,
            secrets_to_scrub=secrets_to_scrub,
        )
        reader_b_clone_succeeded = reader_b_clone_record["returncode"] == 0
        reader_b_commit = git_head(reader_b_clone, commands) if reader_b_clone_succeeded else ""
        reader_b_matches_source = reader_b_commit == current_commit

        for env in (reader_b_env, reader_a_env, maintainer_env):
            stop = retained.run(["rad", "node", "stop"], env=env, timeout=30, allow_fail=True)
            node_stop_records.append(scrub_record(stop, secrets_to_scrub))

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
            and current_extends_prior
            and worktree_matches_source
            and push_succeeded
            and maintainer_node_started
            and publish_succeeded
            and maintainer_seed_succeeded
            and reader_a_node_started
            and reader_a_connected_to_maintainer
            and reader_a_clone_succeeded
            and reader_a_matches_source
            and follower_seed_succeeded
            and reader_b_node_started
            and reader_b_connected_to_follower
            and reader_b_clone_succeeded
            and reader_b_matches_source
        )

        evidence = {
            "schema_version": "decentralized-forge.radicle-independent-availability-check.v1",
            "loop": 65,
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "scope": "Independent follower-seed readback for retained project Radicle RID",
            "source_evidence": "evidence/radicle-retained-update-check-2026-06-29.json",
            "target_rid": target_rid,
            "observed_rid": observed_rid,
            "same_retained_rid": same_retained_rid,
            "prior_verified_commit": prior_verified_commit,
            "current_source_commit": current_commit,
            "current_extends_prior_verified_commit": current_extends_prior,
            "advanced_from_prior_verified_commit": current_commit != prior_verified_commit and current_extends_prior,
            "state_root_shape": "<retained-state-root> (local host/WSL state; not committed; not bundled)",
            "reader_state_shape": "/tmp/df-radicle-independent-availability-* (removed)",
            "secret_values_recorded": False,
            "retained_passphrase_file_created_this_run": retained_passphrase_created,
            "retained_profile_available": retained_profile_available,
            "delegate_did": delegate_did,
            "retained_peer_id": retained_peer_id,
            "retained_node_id": maintainer_node_id,
            "worktree_commit": worktree_commit,
            "worktree_matches_source": worktree_matches_source,
            "visibility": visibility_record["stdout"].strip(),
            "push_succeeded": push_succeeded,
            "maintainer_node_started": maintainer_node_started,
            "publish_succeeded": publish_succeeded,
            "maintainer_seed_succeeded": maintainer_seed_succeeded,
            "maintainer_sync_succeeded": maintainer_sync_succeeded,
            "reader_a_node_started": reader_a_node_started,
            "reader_a_node_id": reader_a_node_id,
            "reader_a_connected_to_maintainer": reader_a_connected_to_maintainer,
            "reader_a_clone_succeeded": reader_a_clone_succeeded,
            "reader_a_readback_commit": reader_a_commit,
            "reader_a_readback_matches_source": reader_a_matches_source,
            "follower_seed_succeeded": follower_seed_succeeded,
            "follower_sync_succeeded": follower_sync_succeeded,
            "reader_b_node_started": reader_b_node_started,
            "reader_b_connected_to_follower": reader_b_connected_to_follower,
            "reader_b_clone_succeeded": reader_b_clone_succeeded,
            "reader_b_readback_commit": reader_b_commit,
            "reader_b_readback_matches_source": reader_b_matches_source,
            "verification_passed": verification_passed,
            "commands": commands,
            "node_stop": node_stop_records,
            "actions_not_taken": [
                "no secret passphrase or Radicle key material was written to committed evidence",
                "reader temporary Radicle homes were removed after evidence capture",
                "no production/private personal keys were used",
                "no paid infrastructure, wallet, spending, or direct outreach was used",
                "no persistent public seed service was kept running after verification",
                "no permanent durability, censorship-resistance, security, global replication, identity-trust, or production-readiness claim is made",
                "no future default public-routing availability claim is made",
                "no full Radicle compatibility claim is made",
            ],
            "claim_boundary": "This records one retained-RID update to the current source commit plus two independent temporary reader profiles: reader A cloned from the retained maintainer seed and then served as a follower seed for reader B. It is not a durability, default public-routing, broad replication, security, identity-trust, or production-readiness guarantee.",
        }
        EVIDENCE_JSON.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

        EVIDENCE_MD.write_text(
            textwrap.dedent(
                f"""
                # Radicle independent availability check - 2026-06-29

                ## Scope

                Loop 65 checked whether the retained Radicle RID could be advanced to the current Git commit and then read back through an independent follower seed.

                ## Result

                - RID: `{target_rid}`
                - Prior verified commit: `{prior_verified_commit}`
                - Current source commit: `{current_commit}`
                - Same retained RID observed: `{same_retained_rid}`
                - Reader A cloned from maintainer seed: `{reader_a_clone_succeeded}`
                - Reader A readback commit: `{reader_a_commit}`
                - Reader A readback matched source: `{reader_a_matches_source}`
                - Reader A follower seed succeeded: `{follower_seed_succeeded}`
                - Reader B connected to follower: `{reader_b_connected_to_follower}`
                - Reader B cloned from follower seed: `{reader_b_clone_succeeded}`
                - Reader B readback commit: `{reader_b_commit}`
                - Reader B readback matched source: `{reader_b_matches_source}`
                - Overall verification passed: `{verification_passed}`

                ## Evidence

                Machine-readable command evidence is in `evidence/radicle-independent-availability-check-2026-06-29.json`.

                ## Non-claims

                This does not prove permanent durability, censorship resistance, security, global replication, identity trust, production readiness, full Radicle compatibility, future default public-routing availability, persistent public seed operation, or general Radicle availability. It records only this exact retained-RID update and independent follower-seed readback attempt.
                """
            ).lstrip(),
            encoding="utf-8",
        )
        return 0 if verification_passed else 2
    finally:
        for env in (reader_b_env, reader_a_env, maintainer_env):
            stop_node(env)
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
