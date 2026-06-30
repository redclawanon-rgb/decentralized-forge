#!/usr/bin/env python3
"""Run a bounded start-project to Radicle genesis/readback gate.

This creates a fresh sample Git project, starts it on the local forge surface,
then initializes that same project as a disposable public Radicle repository and
clones it back from a separate temporary Radicle profile.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import textwrap
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import forge_registry

DEFAULT_EVIDENCE_JSON = ROOT / "evidence" / "radicle-start-project-genesis-2026-06-30.json"
DEFAULT_EVIDENCE_MD = ROOT / "evidence" / "radicle-start-project-genesis-2026-06-30.md"
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
        "cmd": [str(part) for part in cmd],
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


def free_local_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def make_env(rad_home: Path) -> dict:
    env = os.environ.copy()
    bin_dir = env.get("RADICLE_BIN_DIR", str(Path.home() / ".radicle" / "bin"))
    env["PATH"] = f"{bin_dir}:{env.get('PATH', '')}"
    env["RAD_HOME"] = str(rad_home)
    env["RAD_PASSPHRASE"] = REAL_PASS
    return env


def create_sample_project(project: Path, commands: list[dict]) -> None:
    project.mkdir(parents=True)
    commands.append(run(["git", "init", "-b", "main"], cwd=project, timeout=60))
    (project / "README.md").write_text(
        "# Started Forge Sample\n\n"
        "A fresh project used to prove the start-project to Radicle genesis path.\n",
        encoding="utf-8",
    )
    (project / "src").mkdir()
    (project / "src" / "hello.txt").write_text("hello decentralized forge\n", encoding="utf-8")
    commands.append(run(["git", "add", "README.md", "src/hello.txt"], cwd=project))
    commands.append(
        run(
            [
                "git",
                "-c",
                "user.name=Started Project Fixture",
                "-c",
                "user.email=started-project@example.invalid",
                "commit",
                "-m",
                "Initial started forge sample",
            ],
            cwd=project,
            timeout=60,
        )
    )


def artifact_for_temp_repo(source_repo: Path, temp_repo: Path, artifact: Path | None) -> Path | None:
    if artifact is None:
        return None
    resolved_artifact = artifact.resolve()
    try:
        relative_artifact = resolved_artifact.relative_to(source_repo.resolve())
    except ValueError:
        return resolved_artifact
    return temp_repo / relative_artifact


def run_gate(
    evidence_json: Path,
    evidence_md: Path,
    *,
    repository: Path | None = None,
    artifact: Path | None = None,
    project_id: str | None = None,
    project_name: str | None = None,
    description: str | None = None,
    version: str = "0.1.0-local",
    tag: str | None = None,
) -> int:
    tmp = Path(tempfile.mkdtemp(prefix="df-started-project-radicle-genesis-"))
    commands: list[dict] = []
    node_stop_records: list[dict] = []
    try:
        sample_mode = repository is None
        if sample_mode:
            project = tmp / "started-forge-sample"
            create_sample_project(project, commands)
            resolved_project_id = project_id or "started-forge-sample"
            resolved_project_name = project_name or "Started Forge Sample"
            resolved_description = description
            readback_phrase = "start-project to Radicle genesis path"
            artifact_path = None
        else:
            source_metadata = forge_registry.local_repo_metadata(repository)
            source_repo = source_metadata["root"]
            resolved_project_id = forge_registry.slugify_project_id(project_id or source_metadata["repo_name"])
            resolved_project_name = project_name or forge_registry.title_from_project_id(resolved_project_id)
            resolved_description = description
            project = tmp / f"{resolved_project_id}-source"
            commands.append(run(["git", "clone", "--no-hardlinks", str(source_repo), str(project)], timeout=90))
            if source_metadata["branch"]:
                commands.append(run(["git", "checkout", source_metadata["branch"]], cwd=project, timeout=60, allow_fail=True))
            artifact_path = artifact_for_temp_repo(source_repo, project, artifact)
            readback_phrase = None

        output = tmp / "forge-output"
        output.mkdir()
        seed_rad_home = tmp / "seed-rad-home"
        clone_rad_home = tmp / "clone-rad-home"
        clone_parent = tmp / "clone-parent"
        clone_parent.mkdir()
        bundle_path = output / f"{resolved_project_id}.verification-bundle.zip"
        report_path = output / f"{resolved_project_id}.bundle-report.json"
        registry_path = output / f"{resolved_project_id}.registry.json"
        summary_path = output / f"{resolved_project_id}.summary.json"
        html_path = output / f"{resolved_project_id}.html"
        workbench_path = output / f"{resolved_project_id}.forge-app.html"
        receipt_path = output / f"{resolved_project_id}.start-project.json"

        project_commit_record = run(["git", "rev-parse", "HEAD"], cwd=project)
        project_commit = project_commit_record["stdout"].strip()
        commands.append(project_commit_record)
        if not sample_mode and project_commit != source_metadata["head"]:
            raise RuntimeError(
                f"temporary clone HEAD {project_commit} does not match source HEAD {source_metadata['head']}"
            )

        start_result = forge_registry.start_project(
            project,
            artifact_path,
            registry_output=registry_path,
            summary_output=summary_path,
            html_output=html_path,
            app_output=workbench_path,
            receipt_output=receipt_path,
            bundle_output=bundle_path,
            report_json_output=report_path,
            project_id=resolved_project_id,
            project_name=resolved_project_name,
            description=resolved_description,
            version=version,
            tag=tag or version,
            timestamp="2026-06-30T00:00:00Z",
        )
        registry = start_result["registry"]
        receipt = start_result["receipt"]
        artifact = registry["releases"][0]["artifacts"][0]
        start_project_completed = all(path.is_file() for path in [registry_path, summary_path, html_path, workbench_path, receipt_path, bundle_path, report_path])
        bundle_valid = bool(start_result["bundle_report"]["verification"]["valid"])

        env = make_env(seed_rad_home)
        clone_env = make_env(clone_rad_home)
        commands.append(run(["rad", "--version"], env=env, timeout=30))
        commands.append(run(["radicle-node", "--version"], env=env, timeout=30))
        commands.append(run(["rad", "auth", "--alias", "started-project-genesis", "--stdin"], env=env, input_text=REAL_PASS + "\n", timeout=60))
        commands.append(
            run(
                [
                    "rad",
                    "init",
                    "--name",
                    registry["project"]["id"],
                    "--description",
                    registry["project"]["description"],
                    "--default-branch",
                    registry["project"]["default_branch"],
                    "--public",
                    "--no-confirm",
                    "--no-seed",
                    str(project),
                ],
                env=env,
                timeout=60,
            )
        )
        rid = run(["rad", "inspect", "--rid", str(project)], env=env)
        identity = run(["rad", "inspect", "--identity", str(project)], env=env)
        refs = run(["rad", "inspect", "--refs", str(project)], env=env)
        visibility = run(["rad", "inspect", "--visibility", str(project)], env=env)
        commands.extend([rid, identity, refs, visibility])
        rid_value = rid["stdout"].strip()

        seed_port = free_local_port()
        clone_port = free_local_port()
        node_start = run(["rad", "node", "start", "--", "--listen", f"127.0.0.1:{seed_port}"], env=env, timeout=60, allow_fail=True)
        commands.append(node_start)
        node_started = node_start["returncode"] == 0
        time.sleep(2)
        node_status = run(["rad", "node", "status"], env=env, timeout=30, allow_fail=True)
        commands.append(node_status)
        seed_nid = first_nid(node_status["stdout"])

        publish = run(["rad", "publish", rid_value], env=env, timeout=90, allow_fail=True)
        seed = run(["rad", "seed", rid_value, "--no-fetch"], env=env, timeout=60, allow_fail=True)
        sync = run(["rad", "sync", "--announce", rid_value], env=env, timeout=90, allow_fail=True)
        commands.extend([publish, seed, sync])
        publish_succeeded = publish["returncode"] == 0 or "already public" in (publish["stdout"] + publish["stderr"]).lower()
        seed_succeeded = seed["returncode"] == 0
        sync_succeeded = sync["returncode"] == 0

        clone_auth = run(["rad", "auth", "--alias", "started-project-reader", "--stdin"], env=clone_env, input_text=REAL_PASS + "\n", timeout=60, allow_fail=True)
        clone_node_start = run(["rad", "node", "start", "--", "--listen", f"127.0.0.1:{clone_port}"], env=clone_env, timeout=60, allow_fail=True)
        commands.extend([clone_auth, clone_node_start])
        clone_node_started = clone_node_start["returncode"] == 0
        time.sleep(2)

        clone_connect = None
        if seed_nid:
            clone_connect = run(["rad", "node", "connect", f"{seed_nid}@127.0.0.1:{seed_port}"], env=clone_env, timeout=30, allow_fail=True)
            commands.append(clone_connect)

        clone_target = clone_parent / f"{resolved_project_id}-clone"
        clone_cmd = ["rad", "clone", "--timeout", "30s"]
        if seed_nid:
            clone_cmd.extend(["--seed", seed_nid])
        clone_cmd.extend([rid_value, str(clone_target)])
        clone = run(clone_cmd, cwd=clone_parent, env=clone_env, timeout=150, allow_fail=True)
        commands.append(clone)
        clone_succeeded = clone["returncode"] == 0

        clone_commit = ""
        readme_matches = False
        if clone_succeeded:
            clone_commit_record = run(["git", "rev-parse", "HEAD"], cwd=clone_target, allow_fail=True)
            commands.append(clone_commit_record)
            clone_commit = clone_commit_record["stdout"].strip()
            readme_matches = (
                clone_commit == project_commit
                and (
                    readback_phrase is None
                    or (
                        (clone_target / "README.md").is_file()
                        and readback_phrase in (clone_target / "README.md").read_text(encoding="utf-8")
                    )
                )
            )

        node_stop_records.append(run(["rad", "node", "stop"], env=env, timeout=30, allow_fail=True))
        node_stop_records.append(run(["rad", "node", "stop"], env=clone_env, timeout=30, allow_fail=True))

        verification_passed = bool(
            start_project_completed
            and bundle_valid
            and project_commit
            and rid_value.startswith("rad:z")
            and visibility["stdout"].strip() == "public"
            and node_started
            and publish_succeeded
            and seed_succeeded
            and sync_succeeded
            and clone_node_started
            and bool(clone_connect and clone_connect["returncode"] == 0)
            and clone_succeeded
            and readme_matches
        )
        evidence = {
            "schema_version": "decentralized-forge.started-project-radicle-genesis.v1",
            "loop": 96,
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "scope": "Fresh project start-project plus disposable Radicle genesis/readback gate",
            "permission": "User approved continuing toward a public-ready product; actions stayed disposable, project-scoped, and evidence-labeled.",
            "temp_state_root_shape": "/tmp/df-started-project-radicle-genesis-* (removed after evidence capture)",
            "project_source_shape": "/tmp/df-started-project-radicle-genesis-*/<project-id>-source or started-forge-sample (removed)",
            "rad_home_shape": "/tmp/df-started-project-radicle-genesis-*/seed-rad-home (removed)",
            "clone_rad_home_shape": "/tmp/df-started-project-radicle-genesis-*/clone-rad-home (removed)",
            "source_mode": "generated sample project" if sample_mode else "temporary clone of provided Git repository",
            "start_project": {
                "project_id": registry["project"]["id"],
                "project_name": registry["project"]["name"],
                "default_branch": registry["project"]["default_branch"],
                "artifact_name": artifact["name"],
                "artifact_sha256": artifact["sha256"],
                "receipt_schema": receipt["schema_version"],
                "receipt_radicle_next_gate_status": receipt["radicle_next_gate"]["status"],
                "registry_path_shape": f"/tmp/df-started-project-radicle-genesis-*/forge-output/{resolved_project_id}.registry.json",
                "workbench_path_shape": f"/tmp/df-started-project-radicle-genesis-*/forge-output/{resolved_project_id}.forge-app.html",
                "receipt_path_shape": f"/tmp/df-started-project-radicle-genesis-*/forge-output/{resolved_project_id}.start-project.json",
                "bundle_path_shape": f"/tmp/df-started-project-radicle-genesis-*/forge-output/{resolved_project_id}.verification-bundle.zip",
                "start_project_completed": start_project_completed,
                "bundle_valid": bundle_valid,
            },
            "radicle": {
                "rid": rid_value,
                "visibility": visibility["stdout"].strip(),
                "seed_node_id": seed_nid,
                "project_git_commit": project_commit,
                "clone_commit": clone_commit,
                "node_started": node_started,
                "publish_succeeded": publish_succeeded,
                "seed_succeeded": seed_succeeded,
                "sync_succeeded": sync_succeeded,
                "clone_node_started": clone_node_started,
                "clone_node_connected_to_seed": bool(clone_connect and clone_connect["returncode"] == 0),
                "remote_clone_succeeded": clone_succeeded,
                "readback_commit_matches_project": readme_matches,
            },
            "start_project_radicle_gate_executed_separately": True,
            "verification_passed": verification_passed,
            "commands": commands,
            "node_stop": node_stop_records,
            "actions_not_taken": [
                "no production/private personal keys were used",
                "no persistent Radicle home, project repository, or seed state was kept",
                "no paid infrastructure, wallet, spending, or direct outreach was used",
                "no durable storage, pinning, or broad availability claim is made",
                "no censorship resistance, security, identity-trust, SLSA, or production readiness claim is made",
                "no full Radicle or forge compatibility claim is made beyond this exact bounded sample path",
            ],
            "claim_boundary": "This proves only that one Git project completed the local start-project path and then received a disposable public Radicle RID that a separate temporary Radicle profile cloned/read back during this run.",
        }
        evidence_json.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
        evidence_md.write_text(
            textwrap.dedent(
                f"""
                # Started Project Radicle Genesis - 2026-06-30

                ## Scope

                Loop 96 ran the `start-project` alpha path, then separately initialized the same project as a disposable public Radicle repository.

                ## Result

                - Project: `{resolved_project_id}`
                - RID: `{rid_value}`
                - Project commit: `{project_commit}`
                - Clone commit: `{clone_commit}`
                - Visibility: `{visibility['stdout'].strip()}`
                - Start-project completed: `{start_project_completed}`
                - Bundle valid: `{bundle_valid}`
                - Separate temporary-profile clone succeeded: `{clone_succeeded}`
                - Readback commit matched project: `{readme_matches}`
                - Overall verification passed: `{verification_passed}`

                ## Evidence

                Machine-readable command evidence is in `evidence/radicle-start-project-genesis-2026-06-30.json`.

                ## Non-Claims

                This does not prove durable storage, censorship resistance, security, identity trust, SLSA compliance, production readiness, full Radicle compatibility, full forge compatibility, global replication, or long-term availability. It records only the exact bounded sample path above.
                """
            ).lstrip(),
            encoding="utf-8",
        )
        return 0 if verification_passed else 2
    finally:
        for home_name in ("seed-rad-home", "clone-rad-home"):
            try:
                stop_env = make_env(tmp / home_name)
                subprocess.run(["rad", "node", "stop"], env=stop_env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
            except Exception:
                pass
        shutil.rmtree(tmp, ignore_errors=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, help="Existing Git worktree to prove; omitted means create the built-in sample project")
    parser.add_argument("--artifact", type=Path, help="Artifact to attach during start-project; defaults to repository README.md")
    parser.add_argument("--project-id", help="Project id to use for start-project and Radicle metadata")
    parser.add_argument("--project-name", help="Project name to use for start-project and Radicle metadata")
    parser.add_argument("--description", help="Project description to use for start-project and Radicle metadata")
    parser.add_argument("--version", default="0.1.0-local", help="Release version for start-project")
    parser.add_argument("--tag", help="Release tag for start-project; defaults to --version")
    parser.add_argument("--output", type=Path, default=DEFAULT_EVIDENCE_JSON, help="Evidence JSON to write")
    parser.add_argument("--markdown", type=Path, default=DEFAULT_EVIDENCE_MD, help="Evidence Markdown summary to write")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.repository is not None and (args.output == DEFAULT_EVIDENCE_JSON or args.markdown == DEFAULT_EVIDENCE_MD):
        print(
            "project-specific Radicle genesis runs need --output and --markdown so they do not overwrite committed sample evidence",
            file=sys.stderr,
        )
        return 2
    return run_gate(
        args.output,
        args.markdown,
        repository=args.repository,
        artifact=args.artifact,
        project_id=args.project_id,
        project_name=args.project_name,
        description=args.description,
        version=args.version,
        tag=args.tag,
    )


if __name__ == "__main__":
    raise SystemExit(main())
