#!/usr/bin/env python3
"""Create or reuse a retained project-scoped Radicle maintainer lane.

This script is intentionally different from the earlier disposable Radicle
smokes: it keeps a project-scoped Radicle home and maintainer worktree under
the repo-local, gitignored `.tmp/radicle-retained-delegate` directory. The
retained state is needed to make future updates to the same RID possible, but
no secret values or key material are written to committed evidence.
"""

from __future__ import annotations

import json
import os
import re
import secrets
import shutil
import stat
import subprocess
import tempfile
import textwrap
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_ROOT = Path(os.environ.get("DF_RADICLE_RETAINED_STATE_ROOT", ROOT / ".tmp" / "radicle-retained-delegate"))
RAD_HOME = STATE_ROOT / "maintainer-rad-home"
WORKTREE = STATE_ROOT / "maintainer-worktree"
PASSPHRASE_FILE = STATE_ROOT / "maintainer.passphrase"
STATE_JSON = STATE_ROOT / "retained-delegate-state.json"
EVIDENCE_JSON = ROOT / "evidence" / "radicle-retained-delegate-check-2026-06-29.json"
EVIDENCE_MD = ROOT / "evidence" / "radicle-retained-delegate-check-2026-06-29.md"

PASS = "<redacted project-scoped passphrase>"
REAL_PASS = ""


def load_or_create_passphrase() -> tuple[str, bool]:
    STATE_ROOT.mkdir(parents=True, exist_ok=True)
    if PASSPHRASE_FILE.exists():
        return PASSPHRASE_FILE.read_text(encoding="utf-8").strip(), False
    value = secrets.token_urlsafe(32)
    PASSPHRASE_FILE.write_text(value + "\n", encoding="utf-8")
    try:
        PASSPHRASE_FILE.chmod(stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass
    return value, True


def redact(text: str) -> str:
    if REAL_PASS:
        text = text.replace(REAL_PASS, PASS)
    return text.replace(str(STATE_ROOT), "<retained-state-root>")


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
    record = {
        "cmd": cmd,
        "cwd": redact(str(cwd)) if cwd else None,
        "returncode": result.returncode,
        "stdout": redact(result.stdout)[-12000:],
        "stderr": redact(result.stderr)[-12000:],
        "duration_seconds": round(time.time() - started, 3),
    }
    if result.returncode != 0 and not allow_fail:
        raise RuntimeError(json.dumps(record, indent=2))
    return record


def first_nid(text: str) -> str:
    match = re.search(r"\bz6[0-9A-Za-z]{20,}\b", text)
    return match.group(0) if match else ""


def first_did(text: str) -> str:
    match = re.search(r"\bdid:key:z6[0-9A-Za-z]{20,}\b", text)
    return match.group(0) if match else ""


def load_state() -> dict:
    if not STATE_JSON.exists():
        return {}
    return json.loads(STATE_JSON.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    STATE_ROOT.mkdir(parents=True, exist_ok=True)
    public_state = {
        "schema_version": "decentralized-forge.radicle-retained-delegate-state.v1",
        "state_scope": ".tmp/radicle-retained-delegate; gitignored; not bundled",
        "contains_secret_values": False,
        **state,
    }
    STATE_JSON.write_text(json.dumps(public_state, indent=2) + "\n", encoding="utf-8")


def ensure_worktree(commands: list[dict], source_commit: str) -> tuple[bool, str]:
    if not WORKTREE.exists():
        commands.append(
            run(
                [
                    "git",
                    "-c",
                    f"safe.directory={ROOT}",
                    "clone",
                    "--no-hardlinks",
                    str(ROOT),
                    str(WORKTREE),
                ],
                timeout=90,
            )
        )
    else:
        commands.append(run(["git", "fetch", str(ROOT), source_commit], cwd=WORKTREE, timeout=90))
        commands.append(run(["git", "checkout", "-B", "main", "FETCH_HEAD"], cwd=WORKTREE, timeout=60))

    worktree_commit_record = run(["git", "rev-parse", "HEAD"], cwd=WORKTREE)
    commands.append(worktree_commit_record)
    worktree_commit = worktree_commit_record["stdout"].strip()
    return worktree_commit == source_commit, worktree_commit


def main() -> int:
    global REAL_PASS
    REAL_PASS, passphrase_created = load_or_create_passphrase()
    STATE_ROOT.mkdir(parents=True, exist_ok=True)

    commands = []
    node_stop_records = []
    readback_tmp = Path(tempfile.mkdtemp(prefix="df-radicle-retained-readback-"))
    try:
        env = os.environ.copy()
        env["PATH"] = f"{env.get('RADICLE_BIN_DIR', Path.home() / '.radicle' / 'bin')}:{env.get('PATH', '')}"
        env["RAD_HOME"] = str(RAD_HOME)
        env["RAD_PASSPHRASE"] = REAL_PASS

        commands.append(run(["rad", "--version"], env=env))
        commands.append(run(["radicle-node", "--version"], env=env))
        source_commit_record = run(["git", "-c", f"safe.directory={ROOT}", "rev-parse", "HEAD"], cwd=ROOT)
        commands.append(source_commit_record)
        source_commit = source_commit_record["stdout"].strip()

        self_before = run(["rad", "self"], env=env, timeout=45, allow_fail=True)
        commands.append(self_before)
        auth_created = False
        if self_before["returncode"] != 0:
            commands.append(
                run(
                    ["rad", "auth", "--alias", "df-retained-maintainer", "--stdin"],
                    env=env,
                    input_text=REAL_PASS + "\n",
                    timeout=60,
                )
            )
            auth_created = True

        self_after = run(["rad", "self"], env=env, timeout=45, allow_fail=True)
        commands.append(self_after)
        retained_peer_id = first_nid(self_after["stdout"] + "\n" + self_after["stderr"])

        worktree_matches_source, worktree_commit = ensure_worktree(commands, source_commit)
        prior_state = load_state()
        prior_rid = prior_state.get("rid", "")
        initialized_new_rid = False
        if not prior_rid:
            commands.append(
                run(
                    [
                        "rad",
                        "init",
                        "--name",
                        "decentralized-forge",
                        "--description",
                        "Decentralized Forge retained-maintainer Radicle repository; evidence-scoped, no durability/security/production claims.",
                        "--default-branch",
                        "main",
                        "--public",
                        "--no-confirm",
                        "--no-seed",
                        str(WORKTREE),
                    ],
                    env=env,
                    timeout=90,
                )
            )
            initialized_new_rid = True

        rid_record = run(["rad", "inspect", "--rid", str(WORKTREE)], env=env)
        identity_record = run(["rad", "inspect", "--identity", str(WORKTREE)], env=env)
        refs_record = run(["rad", "inspect", "--refs", str(WORKTREE)], env=env)
        visibility_record = run(["rad", "inspect", "--visibility", str(WORKTREE)], env=env)
        commands.extend([rid_record, identity_record, refs_record, visibility_record])
        rid = rid_record["stdout"].strip()
        delegate_did = first_did(identity_record["stdout"])

        push_record = run(["git", "push", "rad", "main"], cwd=WORKTREE, env=env, timeout=180, allow_fail=True)
        commands.append(push_record)
        push_succeeded = push_record["returncode"] == 0

        node_start = run(["rad", "node", "start", "--", "--listen", "127.0.0.1:8791"], env=env, timeout=60, allow_fail=True)
        commands.append(node_start)
        node_started = node_start["returncode"] == 0
        time.sleep(3)
        node_status = run(["rad", "node", "status"], env=env, timeout=45, allow_fail=True)
        commands.append(node_status)
        retained_node_id = first_nid(node_status["stdout"] + "\n" + node_status["stderr"])

        publish = run(["rad", "publish", rid], env=env, timeout=120, allow_fail=True)
        commands.append(publish)
        publish_succeeded = publish["returncode"] == 0 or "already public" in (publish["stdout"] + publish["stderr"]).lower()

        seed = run(["rad", "seed", rid, "--scope", "all", "--no-fetch"], env=env, timeout=90, allow_fail=True)
        commands.append(seed)
        seed_succeeded = seed["returncode"] == 0 or "already" in (seed["stdout"] + seed["stderr"]).lower()

        inventory_sync = run(["rad", "sync", "--inventory"], env=env, timeout=120, allow_fail=True)
        commands.append(inventory_sync)
        inventory_sync_succeeded = inventory_sync["returncode"] == 0 and "error:" not in (
            inventory_sync["stdout"] + inventory_sync["stderr"]
        ).lower()

        sync = run(["rad", "sync", "--announce", "--timeout", "60s", "--replicas", "1", rid], env=env, timeout=150, allow_fail=True)
        commands.append(sync)
        sync_succeeded = sync["returncode"] == 0 and "error:" not in (sync["stdout"] + sync["stderr"]).lower()

        time.sleep(15)
        readback_home = readback_tmp / "fresh-readback-rad-home"
        readback_parent = readback_tmp / "clone-parent"
        readback_parent.mkdir(parents=True)
        readback_path = readback_parent / "decentralized-forge-retained-default-readback"
        direct_readback_path = readback_parent / "decentralized-forge-retained-direct-readback"
        readback_env = env.copy()
        readback_env["RAD_HOME"] = str(readback_home)
        commands.append(
            run(
                ["rad", "auth", "--alias", "df-retained-readback", "--stdin"],
                env=readback_env,
                input_text=REAL_PASS + "\n",
                timeout=60,
                allow_fail=True,
            )
        )
        readback_node_start = run(
            ["rad", "node", "start", "--", "--listen", "127.0.0.1:8792"],
            env=readback_env,
            timeout=60,
            allow_fail=True,
        )
        commands.append(readback_node_start)
        readback_node_started = readback_node_start["returncode"] == 0
        time.sleep(12)
        commands.append(run(["rad", "node", "status"], env=readback_env, timeout=45, allow_fail=True))

        readback_clone = run(
            ["rad", "clone", "--timeout", "120s", rid, str(readback_path)],
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
            readback_branches = run(["git", "branch", "-a", "-vv"], cwd=readback_path, allow_fail=True)
            readback_commit_record = run(["git", "rev-parse", "HEAD"], cwd=readback_path, allow_fail=True)
            commands.extend([readback_branches, readback_commit_record])
            readback_branches_output = readback_branches["stdout"]
            readback_commit = readback_commit_record["stdout"].strip()

        direct_connect_succeeded = False
        direct_seed_clone_succeeded = False
        direct_seed_readback_commit = ""
        direct_seed_readback_branches_output = ""
        direct_seed_readback_matches_source = False
        if retained_node_id:
            direct_connect = run(
                ["rad", "node", "connect", f"{retained_node_id}@127.0.0.1:8791", "--timeout", "30s"],
                env=readback_env,
                timeout=45,
                allow_fail=True,
            )
            commands.append(direct_connect)
            direct_connect_succeeded = direct_connect["returncode"] == 0
            direct_clone = run(
                ["rad", "clone", "--timeout", "120s", "--seed", retained_node_id, rid, str(direct_readback_path)],
                cwd=readback_parent,
                env=readback_env,
                timeout=240,
                allow_fail=True,
            )
            commands.append(direct_clone)
            direct_seed_clone_succeeded = direct_clone["returncode"] == 0
            if direct_seed_clone_succeeded:
                direct_branches = run(["git", "branch", "-a", "-vv"], cwd=direct_readback_path, allow_fail=True)
                direct_commit = run(["git", "rev-parse", "HEAD"], cwd=direct_readback_path, allow_fail=True)
                commands.extend([direct_branches, direct_commit])
                direct_seed_readback_branches_output = direct_branches["stdout"]
                direct_seed_readback_commit = direct_commit["stdout"].strip()
                direct_seed_readback_matches_source = direct_seed_readback_commit == source_commit

        node_stop_records.append(run(["rad", "node", "stop"], env=readback_env, timeout=30, allow_fail=True))
        node_stop_records.append(run(["rad", "node", "stop"], env=env, timeout=30, allow_fail=True))

        default_readback_matches_source = readback_commit == source_commit
        retained_state_reused = bool(prior_rid and prior_rid == rid)
        save_state(
            {
                "rid": rid,
                "delegate_did": delegate_did,
                "retained_peer_id": retained_peer_id,
                "last_verified_commit": source_commit,
                "last_verified_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
        )

        verification_passed = bool(
            rid.startswith("rad:z")
            and worktree_matches_source
            and (push_succeeded or initialized_new_rid)
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
            "schema_version": "decentralized-forge.radicle-retained-delegate-check.v1",
            "loop": 62,
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "scope": "Retained project-scoped Radicle maintainer/delegate lane",
            "state_root_shape": ".tmp/radicle-retained-delegate (gitignored; not committed; not bundled)",
            "retained_rad_home_shape": ".tmp/radicle-retained-delegate/maintainer-rad-home",
            "retained_worktree_shape": ".tmp/radicle-retained-delegate/maintainer-worktree",
            "secret_values_recorded": False,
            "passphrase_file_created_this_run": passphrase_created,
            "auth_profile_created_this_run": auth_created,
            "initialized_new_rid": initialized_new_rid,
            "retained_state_reused": retained_state_reused,
            "prior_rid": prior_rid,
            "rid": rid,
            "delegate_did": delegate_did,
            "retained_peer_id": retained_peer_id,
            "retained_node_id": retained_node_id,
            "source_commit": source_commit,
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
            "claim_boundary": "This records one retained project-scoped maintainer lane: a gitignored Radicle maintainer state published the source commit to its RID and a separate fresh profile read it back. The evidence records whether default public-routing clone worked and whether explicit direct-seed fallback was needed. It is not a durability, broad replication, security, identity-trust, or production-readiness guarantee.",
        }
        EVIDENCE_JSON.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

        EVIDENCE_MD.write_text(
            textwrap.dedent(
                f"""
                # Radicle retained delegate check - 2026-06-29

                ## Scope

                Loop 62 created or reused a project-scoped retained Radicle maintainer lane under gitignored `.tmp/radicle-retained-delegate`.

                ## Result

                - RID: `{rid}`
                - Source commit: `{source_commit}`
                - Retained state reused: `{retained_state_reused}`
                - Initialized new RID: `{initialized_new_rid}`
                - Delegate DID: `{delegate_did}`
                - Retained peer ID: `{retained_peer_id}`
                - Worktree matched source: `{worktree_matches_source}`
                - Push succeeded: `{push_succeeded}`
                - Publish succeeded: `{publish_succeeded}`
                - Seed succeeded: `{seed_succeeded}`
                - Inventory sync succeeded: `{inventory_sync_succeeded}`
                - Sync/announce succeeded: `{sync_succeeded}`
                - Fresh default clone succeeded: `{readback_clone_succeeded}`
                - Fresh default clone commit: `{readback_commit}`
                - Default readback matched source: `{default_readback_matches_source}`
                - Direct seed node connect succeeded: `{direct_connect_succeeded}`
                - Direct seed clone succeeded: `{direct_seed_clone_succeeded}`
                - Direct seed clone commit: `{direct_seed_readback_commit}`
                - Direct seed readback matched source: `{direct_seed_readback_matches_source}`
                - Overall verification passed: `{verification_passed}`

                ## Evidence

                Machine-readable command evidence is in `evidence/radicle-retained-delegate-check-2026-06-29.json`.

                ## Non-claims

                This does not prove permanent durability, censorship resistance, security, global replication, identity trust, production readiness, full Radicle compatibility, future default public-routing availability, or general Radicle availability. It records only this exact retained-maintainer publish and fresh readback attempt.
                """
            ).lstrip(),
            encoding="utf-8",
        )
        return 0 if verification_passed else 2
    finally:
        for rad_home in (readback_tmp / "fresh-readback-rad-home", RAD_HOME):
            try:
                stop_env = os.environ.copy()
                stop_env["PATH"] = f"{stop_env.get('RADICLE_BIN_DIR', Path.home() / '.radicle' / 'bin')}:{stop_env.get('PATH', '')}"
                stop_env["RAD_HOME"] = str(rad_home)
                stop_env["RAD_PASSPHRASE"] = REAL_PASS
                subprocess.run(["rad", "node", "stop"], env=stop_env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
            except Exception:
                pass
        shutil.rmtree(readback_tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
