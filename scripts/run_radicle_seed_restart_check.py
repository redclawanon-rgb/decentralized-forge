#!/usr/bin/env python3
"""Rehearse restartable retained-RID Radicle seed operation.

Loop 65 proved that a temporary follower seed can serve the retained RID to a
second fresh reader. This check advances the retained RID to the current source
commit, starts the retained seed, verifies a fresh direct-seed clone, stops the
seed, starts it again on the same local address, and verifies another fresh
direct-seed clone after restart.

The script intentionally stops the node at the end. It records a bounded
service rehearsal, not an always-on public seed claim.
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
SOURCE_EVIDENCE = ROOT / "evidence" / "radicle-independent-availability-check-2026-06-29.json"
EVIDENCE_JSON = ROOT / "evidence" / "radicle-seed-restart-check-2026-06-29.json"
EVIDENCE_MD = ROOT / "evidence" / "radicle-seed-restart-check-2026-06-29.md"
SEED_LISTEN_ADDR = os.environ.get("DF_RADICLE_SEED_RESTART_LISTEN", "127.0.0.1:8799")


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


def run_record(
    commands: list[dict],
    cmd: list[str],
    *,
    env=None,
    cwd=None,
    input_text=None,
    timeout=30,
    allow_fail=False,
    secrets_to_scrub=None,
) -> dict:
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


def start_seed(commands: list[dict], env: dict, target_rid: str, secrets_to_scrub: list[str], label: str) -> tuple[bool, str, bool]:
    start = run_record(
        commands,
        ["rad", "node", "start", "--", "--listen", SEED_LISTEN_ADDR],
        env=env,
        timeout=60,
        allow_fail=True,
        secrets_to_scrub=secrets_to_scrub,
    )
    started = start["returncode"] == 0
    time.sleep(3)
    status = run_record(commands, ["rad", "node", "status"], env=env, timeout=45, allow_fail=True, secrets_to_scrub=secrets_to_scrub)
    node_id = retained.first_nid(status["stdout"] + "\n" + status["stderr"])
    seed = run_record(
        commands,
        ["rad", "seed", target_rid, "--scope", "all", "--no-fetch"],
        env=env,
        timeout=90,
        allow_fail=True,
        secrets_to_scrub=secrets_to_scrub,
    )
    seed_succeeded = seed["returncode"] == 0 or "already" in (seed["stdout"] + seed["stderr"]).lower()
    commands.append(
        {
            "cmd": ["seed-restart-checkpoint", label],
            "cwd": None,
            "returncode": 0 if (started and seed_succeeded) else 1,
            "stdout": f"started={started} node_id={node_id} seed_succeeded={seed_succeeded}\n",
            "stderr": "",
            "duration_seconds": 0,
        }
    )
    return started, node_id, seed_succeeded


def fresh_reader_clone(
    commands: list[dict],
    base_env: dict,
    tmp: Path,
    alias: str,
    listen_addr: str,
    target_rid: str,
    seed_node_id: str,
    seed_addr: str,
    expected_commit: str,
    secrets_to_scrub: list[str],
) -> dict:
    passphrase = secrets.token_urlsafe(32)
    secrets_to_scrub.append(passphrase)
    reader_home = tmp / f"{alias}-rad-home"
    clone_parent = tmp / f"{alias}-clone-parent"
    clone_parent.mkdir(parents=True)
    clone_path = clone_parent / "decentralized-forge"
    env = base_env.copy()
    env["RAD_HOME"] = str(reader_home)
    env["RAD_PASSPHRASE"] = passphrase

    auth = run_record(
        commands,
        ["rad", "auth", "--alias", alias, "--stdin"],
        env=env,
        input_text=passphrase + "\n",
        timeout=60,
        allow_fail=True,
        secrets_to_scrub=secrets_to_scrub,
    )
    node_start = run_record(
        commands,
        ["rad", "node", "start", "--", "--listen", listen_addr],
        env=env,
        timeout=60,
        allow_fail=True,
        secrets_to_scrub=secrets_to_scrub,
    )
    time.sleep(6)
    status = run_record(commands, ["rad", "node", "status"], env=env, timeout=45, allow_fail=True, secrets_to_scrub=secrets_to_scrub)
    reader_node_id = retained.first_nid(status["stdout"] + "\n" + status["stderr"])
    connect = run_record(
        commands,
        ["rad", "node", "connect", f"{seed_node_id}@{seed_addr}", "--timeout", "30s"],
        env=env,
        timeout=45,
        allow_fail=True,
        secrets_to_scrub=secrets_to_scrub,
    )
    clone = run_record(
        commands,
        ["rad", "clone", "--timeout", "120s", "--seed", seed_node_id, target_rid, str(clone_path)],
        cwd=clone_parent,
        env=env,
        timeout=240,
        allow_fail=True,
        secrets_to_scrub=secrets_to_scrub,
    )
    clone_succeeded = clone["returncode"] == 0
    readback_commit = git_head(clone_path, commands) if clone_succeeded else ""
    stop = retained.run(["rad", "node", "stop"], env=env, timeout=30, allow_fail=True)

    return {
        "auth_succeeded": auth["returncode"] == 0,
        "node_started": node_start["returncode"] == 0,
        "node_id": reader_node_id,
        "connected_to_seed": connect["returncode"] == 0,
        "clone_succeeded": clone_succeeded,
        "readback_commit": readback_commit,
        "readback_matches_source": readback_commit == expected_commit,
        "node_stop": scrub_record(stop, secrets_to_scrub),
    }


def main() -> int:
    retained.REAL_PASS, retained_passphrase_created = retained.load_or_create_passphrase()
    source = json.loads(SOURCE_EVIDENCE.read_text(encoding="utf-8"))
    target_rid = source["target_rid"]
    prior_verified_commit = source["current_source_commit"]

    commands: list[dict] = []
    node_stop_records: list[dict] = []
    tmp = Path(tempfile.mkdtemp(prefix="df-radicle-seed-restart-"))
    secrets_to_scrub: list[str] = []

    maintainer_env = os.environ.copy()
    maintainer_env["PATH"] = f"{maintainer_env.get('RADICLE_BIN_DIR', Path.home() / '.radicle' / 'bin')}:{maintainer_env.get('PATH', '')}"
    maintainer_env["RAD_HOME"] = str(retained.RAD_HOME)
    maintainer_env["RAD_PASSPHRASE"] = retained.REAL_PASS

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

        initial_stop = retained.run(["rad", "node", "stop"], env=maintainer_env, timeout=30, allow_fail=True)
        node_stop_records.append(scrub_record(initial_stop, secrets_to_scrub))

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
        publish = run_record(commands, ["rad", "publish", target_rid], env=maintainer_env, timeout=120, allow_fail=True)
        publish_succeeded = publish["returncode"] == 0 or "already public" in (publish["stdout"] + publish["stderr"]).lower()

        first_seed_started, first_seed_node_id, first_seed_policy_succeeded = start_seed(
            commands, maintainer_env, target_rid, secrets_to_scrub, "first-start"
        )
        first_reader = fresh_reader_clone(
            commands,
            maintainer_env,
            tmp,
            "df-seed-restart-reader-a",
            "127.0.0.1:8800",
            target_rid,
            first_seed_node_id,
            SEED_LISTEN_ADDR,
            current_commit,
            secrets_to_scrub,
        )

        first_stop = retained.run(["rad", "node", "stop"], env=maintainer_env, timeout=30, allow_fail=True)
        first_stop_record = scrub_record(first_stop, secrets_to_scrub)
        node_stop_records.append(first_stop_record)
        stop_after_first_succeeded = first_stop["returncode"] == 0
        time.sleep(3)

        restart_seed_started, restart_seed_node_id, restart_seed_policy_succeeded = start_seed(
            commands, maintainer_env, target_rid, secrets_to_scrub, "restart"
        )
        second_reader = fresh_reader_clone(
            commands,
            maintainer_env,
            tmp,
            "df-seed-restart-reader-b",
            "127.0.0.1:8801",
            target_rid,
            restart_seed_node_id,
            SEED_LISTEN_ADDR,
            current_commit,
            secrets_to_scrub,
        )

        final_stop = retained.run(["rad", "node", "stop"], env=maintainer_env, timeout=30, allow_fail=True)
        final_stop_record = scrub_record(final_stop, secrets_to_scrub)
        node_stop_records.append(final_stop_record)
        final_stop_succeeded = final_stop["returncode"] == 0

        retained.save_state(
            {
                "rid": target_rid,
                "delegate_did": delegate_did,
                "retained_peer_id": retained_peer_id,
                "last_verified_commit": current_commit,
                "last_verified_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
        )

        same_seed_node_after_restart = bool(first_seed_node_id and first_seed_node_id == restart_seed_node_id == retained_peer_id)
        verification_passed = bool(
            retained_profile_available
            and same_retained_rid
            and current_extends_prior
            and worktree_matches_source
            and push_succeeded
            and publish_succeeded
            and first_seed_started
            and first_seed_policy_succeeded
            and first_reader["node_started"]
            and first_reader["connected_to_seed"]
            and first_reader["clone_succeeded"]
            and first_reader["readback_matches_source"]
            and stop_after_first_succeeded
            and restart_seed_started
            and restart_seed_policy_succeeded
            and same_seed_node_after_restart
            and second_reader["node_started"]
            and second_reader["connected_to_seed"]
            and second_reader["clone_succeeded"]
            and second_reader["readback_matches_source"]
            and final_stop_succeeded
        )

        evidence = {
            "schema_version": "decentralized-forge.radicle-seed-restart-check.v1",
            "loop": 66,
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "scope": "Restartable retained-RID Radicle seed rehearsal",
            "source_evidence": "evidence/radicle-independent-availability-check-2026-06-29.json",
            "target_rid": target_rid,
            "observed_rid": observed_rid,
            "same_retained_rid": same_retained_rid,
            "prior_verified_commit": prior_verified_commit,
            "current_source_commit": current_commit,
            "current_extends_prior_verified_commit": current_extends_prior,
            "advanced_from_prior_verified_commit": current_commit != prior_verified_commit and current_extends_prior,
            "state_root_shape": "<retained-state-root> (local host/WSL state; not committed; not bundled)",
            "reader_state_shape": "/tmp/df-radicle-seed-restart-* (removed)",
            "seed_listen_addr": SEED_LISTEN_ADDR,
            "seed_address_publicly_reachable": False,
            "separate_host_readback_observed": False,
            "secret_values_recorded": False,
            "retained_passphrase_file_created_this_run": retained_passphrase_created,
            "retained_profile_available": retained_profile_available,
            "delegate_did": delegate_did,
            "retained_peer_id": retained_peer_id,
            "first_seed_node_started": first_seed_started,
            "first_seed_node_id": first_seed_node_id,
            "first_seed_policy_succeeded": first_seed_policy_succeeded,
            "first_reader": first_reader,
            "stop_after_first_succeeded": stop_after_first_succeeded,
            "restart_seed_node_started": restart_seed_started,
            "restart_seed_node_id": restart_seed_node_id,
            "restart_seed_policy_succeeded": restart_seed_policy_succeeded,
            "same_seed_node_after_restart": same_seed_node_after_restart,
            "second_reader": second_reader,
            "final_stop_succeeded": final_stop_succeeded,
            "persistent_seed_service_left_running": False,
            "worktree_commit": worktree_commit,
            "worktree_matches_source": worktree_matches_source,
            "visibility": visibility_record["stdout"].strip(),
            "push_succeeded": push_succeeded,
            "publish_succeeded": publish_succeeded,
            "verification_passed": verification_passed,
            "commands": commands,
            "node_stop": node_stop_records,
            "actions_not_taken": [
                "no secret passphrase or Radicle key material was written to committed evidence",
                "reader temporary Radicle homes were removed after evidence capture",
                "no production/private personal keys were used",
                "no paid infrastructure, wallet, spending, or direct outreach was used",
                "no persistent public seed service was left running after verification",
                "no public firewall/router/NAT change was made",
                "no separate-host or separate-network readback was observed",
                "no permanent durability, censorship-resistance, security, global replication, identity-trust, or production-readiness claim is made",
                "no future default public-routing availability claim is made",
                "no full Radicle compatibility claim is made",
            ],
            "claim_boundary": "This records one local restart rehearsal for the retained Radicle seed: a fresh reader cloned before seed restart and another fresh reader cloned after the retained seed restarted on the same local address. It is not an always-on public seed, separate-network availability, durability, default public-routing, broad replication, security, identity-trust, or production-readiness guarantee.",
        }
        EVIDENCE_JSON.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

        EVIDENCE_MD.write_text(
            textwrap.dedent(
                f"""
                # Radicle seed restart check - 2026-06-29

                ## Scope

                Loop 66 checked whether the retained Radicle seed can be stopped, restarted on the same local address, and still serve the retained RID to fresh readers.

                ## Result

                - RID: `{target_rid}`
                - Prior verified commit: `{prior_verified_commit}`
                - Current source commit: `{current_commit}`
                - Seed listen address: `{SEED_LISTEN_ADDR}`
                - First fresh reader cloned before restart: `{first_reader["clone_succeeded"]}`
                - First reader readback commit: `{first_reader["readback_commit"]}`
                - First reader readback matched source: `{first_reader["readback_matches_source"]}`
                - Seed stop after first reader succeeded: `{stop_after_first_succeeded}`
                - Restarted seed node ID matched retained peer: `{same_seed_node_after_restart}`
                - Second fresh reader cloned after restart: `{second_reader["clone_succeeded"]}`
                - Second reader readback commit: `{second_reader["readback_commit"]}`
                - Second reader readback matched source: `{second_reader["readback_matches_source"]}`
                - Persistent service left running: `False`
                - Overall verification passed: `{verification_passed}`

                ## Evidence

                Machine-readable command evidence is in `evidence/radicle-seed-restart-check-2026-06-29.json`.

                ## Non-claims

                This does not prove permanent durability, censorship resistance, security, global replication, identity trust, production readiness, full Radicle compatibility, future default public-routing availability, public reachability, separate-network availability, or always-on seed operation. It records only this exact retained-RID local seed restart/readback rehearsal.
                """
            ).lstrip(),
            encoding="utf-8",
        )
        return 0 if verification_passed else 2
    finally:
        stop_node(maintainer_env)
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
