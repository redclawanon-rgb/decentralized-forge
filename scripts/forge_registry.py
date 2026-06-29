#!/usr/bin/env python3
"""Local CLI for decentralized-forge registry fixtures."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from collections import Counter
from pathlib import Path

import nip34_adapter
import preflight_static_artifact
import render_forge_app
import render_project_page

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_NIP34_REPO_FIXTURE = ROOT / "fixtures" / "nostr-repo-announcement.json"
DEFAULT_NIP34_COLLAB_FIXTURE = ROOT / "fixtures" / "nostr-collaboration-events.json"
DEFAULT_NIP34_STATE_STATUS_FIXTURE = ROOT / "fixtures" / "nostr-repo-state-status.json"
DEFAULT_NIP34_LIVE_READBACK_FIXTURE = ROOT / "fixtures" / "nostr-live-readback-events.json"
DEFAULT_LIVE_EVIDENCE_INDEX = ROOT / "fixtures" / "live-evidence-index.json"
DEFAULT_LIVE_EVIDENCE_SCHEMA = ROOT / "schemas" / "live-evidence-index.schema.json"
DEFAULT_BUNDLE_OUTPUT = ROOT / "output" / "decentralized-forge-verification-bundle.zip"
DEFAULT_BUNDLE_MANIFEST_PATH = "verification-bundle.manifest.json"
ZIP_FIXED_DATE_TIME = (2026, 1, 1, 0, 0, 0)

SECRET_MARKERS = ("nsec1", "-----begin", "private key:", "seed phrase:", "api_token")
FORBIDDEN_LIVE_CLAIM_MARKERS = (
    "censorship resistance verified",
    "censorship-proof",
    "durably stored",
    "pinned and available",
    "production ready",
    "production-ready",
    "security guarantee",
    "slsa compliant",
)


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def verification_summary(states: list[dict]) -> dict:
    state_counts = Counter(state.get("state", "unknown") for state in states if isinstance(state, dict))
    return {
        "total": sum(state_counts.values()),
        "by_state": dict(sorted(state_counts.items())),
        "live_verified": sum(1 for state in states if isinstance(state, dict) and state.get("live_verified") is True),
        "synthetic": sum(1 for state in states if isinstance(state, dict) and state.get("synthetic") is True),
    }


def registry_summary(registry: dict, source_path: Path) -> dict:
    issues = registry.get("issues", [])
    patches = registry.get("patches", [])
    releases = registry.get("releases", [])
    artifacts = [
        artifact
        for release in releases
        for artifact in release.get("artifacts", [])
        if isinstance(artifact, dict)
    ]
    return {
        "schema_version": "decentralized-forge.registry-summary.v1",
        "source": relative(source_path),
        "project": {
            "id": registry["project"]["id"],
            "name": registry["project"]["name"],
            "default_branch": registry["project"]["default_branch"],
        },
        "counts": {
            "maintainers": len(registry.get("maintainers", [])),
            "clone_urls": len(registry.get("clone_urls", [])),
            "issues": len(issues),
            "patches": len(patches),
            "releases": len(releases),
            "artifacts": len(artifacts),
            "ci_checks": len(registry.get("ci_checks", [])),
            "verification_states": len(registry.get("verification_states", [])),
        },
        "clone_transports": sorted(
            {clone.get("transport") for clone in registry.get("clone_urls", []) if clone.get("transport")}
        ),
        "release_versions": [release.get("version") for release in releases if release.get("version")],
        "artifact_names": [artifact.get("name") for artifact in artifacts if artifact.get("name")],
        "artifact_cids": sorted({artifact.get("cid") for artifact in artifacts if artifact.get("cid")}),
        "verification": verification_summary(registry.get("verification_states", [])),
        "non_claims": {
            "production_ready": False,
            "durable_storage_verified": False,
            "censorship_resistance_verified": False,
            "security_guarantee": False,
        },
    }


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(f"{json.dumps(payload, indent=2, sort_keys=True)}\n")


def stable_json_bytes(payload: object) -> bytes:
    return f"{json.dumps(payload, indent=2, sort_keys=True)}\n".encode("utf-8")


def canonical_evidence_bytes(path: Path) -> bytes:
    """Return cross-platform evidence bytes with text line endings normalized."""
    return path.read_bytes().replace(b"\r\n", b"\n")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(canonical_evidence_bytes(path)).hexdigest()


def bundle_file_bytes(path: Path) -> bytes:
    if path.suffix.lower() in {".car"}:
        return path.read_bytes()
    return path.read_bytes().replace(b"\r\n", b"\n")


def safe_repo_relative_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        raise ValueError(f"path must be repository-relative: {value}")
    resolved = (ROOT / path).resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f"path escapes repository root: {value}") from exc
    return resolved


def validate_live_evidence_index(index_path: Path = DEFAULT_LIVE_EVIDENCE_INDEX) -> list[str]:
    errors: list[str] = []
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read live evidence index: {exc}"]

    if not isinstance(index, dict):
        return ["live evidence index root must be an object"]
    if index.get("schema_version") != "decentralized-forge.live-evidence-index.v1":
        errors.append("unsupported live evidence index schema_version")

    policy = index.get("claim_policy")
    if not isinstance(policy, dict):
        errors.append("claim_policy must be an object")
    elif policy.get("contains_secret_values") is not False:
        errors.append("claim_policy.contains_secret_values must be false")

    evidence = index.get("evidence")
    if not isinstance(evidence, list):
        return errors + ["evidence must be an array"]

    seen_ids: set[str] = set()
    for offset, item in enumerate(evidence):
        prefix = f"evidence[{offset}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue

        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id:
            errors.append(f"{prefix}.id is required")
        elif item_id in seen_ids:
            errors.append(f"{prefix}.id duplicates {item_id}")
        else:
            seen_ids.add(item_id)

        for key in [
            "protocol",
            "scope",
            "state",
            "verified_at",
            "evidence_file",
            "evidence_sha256",
            "verification_summary",
            "non_claims",
        ]:
            if key not in item:
                errors.append(f"{prefix}.{key} is required")

        if not isinstance(item.get("non_claims"), list) or not item.get("non_claims"):
            errors.append(f"{prefix}.non_claims must be a non-empty array")

        for bool_key in ["live_network_action", "local_cli_verified", "selected_relay_readback_verified", "synthetic"]:
            if not isinstance(item.get(bool_key), bool):
                errors.append(f"{prefix}.{bool_key} must be a boolean")

        if item.get("selected_relay_readback_verified") and item.get("protocol") != "nostr":
            errors.append(f"{prefix}.selected_relay_readback_verified must be Nostr-scoped")

        evidence_file = item.get("evidence_file")
        if isinstance(evidence_file, str):
            try:
                evidence_path = safe_repo_relative_path(evidence_file)
            except ValueError as exc:
                errors.append(f"{prefix}.evidence_file invalid: {exc}")
                evidence_path = None
            if evidence_path is not None:
                if not evidence_path.is_file():
                    errors.append(f"{prefix}.evidence_file missing: {evidence_file}")
                else:
                    actual_sha256 = sha256_file(evidence_path)
                    actual_size = len(canonical_evidence_bytes(evidence_path))
                    if item.get("evidence_sha256") != actual_sha256:
                        errors.append(f"{prefix}.evidence_sha256 does not match {evidence_file}")
                    if item.get("evidence_size_bytes") != actual_size:
                        errors.append(f"{prefix}.evidence_size_bytes does not match {evidence_file}")

        blob = json.dumps(item, sort_keys=True).lower()
        for marker in SECRET_MARKERS:
            if marker in blob:
                errors.append(f"{prefix} contains secret marker {marker!r}")
        for marker in FORBIDDEN_LIVE_CLAIM_MARKERS:
            negated_forms = (f"not {marker}", f"not a {marker}", f"no {marker}")
            if marker in blob and not any(form in blob for form in negated_forms):
                errors.append(f"{prefix} contains unsupported claim marker {marker!r}")

    return errors


def refresh_live_evidence_hashes(index_path: Path = DEFAULT_LIVE_EVIDENCE_INDEX) -> dict:
    index = json.loads(index_path.read_text(encoding="utf-8"))
    if not isinstance(index, dict) or not isinstance(index.get("evidence"), list):
        raise ValueError("live evidence index must be an object with evidence[]")
    for item in index["evidence"]:
        if not isinstance(item, dict):
            raise ValueError("live evidence entries must be objects")
        evidence_path = safe_repo_relative_path(item["evidence_file"])
        if not evidence_path.is_file():
            raise ValueError(f"missing evidence file: {item['evidence_file']}")
        item["evidence_sha256"] = sha256_file(evidence_path)
        item["evidence_size_bytes"] = len(canonical_evidence_bytes(evidence_path))
    return index


def bundle_role(path: str) -> str:
    if path.startswith("schemas/"):
        return "schema"
    if path.startswith("fixtures/"):
        return "fixture"
    if path.startswith("evidence/"):
        return "source-evidence"
    if path.startswith("output/"):
        return "generated-output"
    if path.startswith("scripts/"):
        return "verifier-tooling"
    if path.startswith("docs/") or path in {"README.md", "STATUS.md", "COMPLETION-CRITERIA.md", "AGENT-LOOPS.md"}:
        return "documentation"
    return "supporting-file"


def collect_verification_bundle_paths() -> list[Path]:
    paths: set[Path] = set()
    for pattern in ["schemas/*.json", "fixtures/*.json", "fixtures/*.txt", "evidence/*"]:
        paths.update(path for path in ROOT.glob(pattern) if path.is_file())

    for relative_path in [
        "README.md",
        "STATUS.md",
        "COMPLETION-CRITERIA.md",
        "AGENT-LOOPS.md",
        "docs/threat-model.md",
        "docs/community-quickstart.md",
        "package.json",
        "package-lock.json",
        "scripts/forge_registry.py",
        "scripts/render_project_page.py",
        "scripts/render_forge_app.py",
        "scripts/nip34_adapter.py",
        "scripts/preflight_static_artifact.py",
        "scripts/verify_car_cid_fixture.mjs",
        "scripts/verify_helia_fixture.mjs",
        "output/demo-project.html",
        "output/portable-lab.html",
        "output/forge-app.html",
        "output/demo-project.summary.json",
        "output/portable-lab.summary.json",
    ]:
        path = ROOT / relative_path
        if path.is_file():
            paths.add(path)

    return sorted(paths, key=relative)


def regenerate_portable_outputs() -> None:
    render_project_page.main(
        [
            str(ROOT / "fixtures" / "example-project.registry.json"),
            str(ROOT / "output" / "demo-project.html"),
            "--nip34-repo-fixture",
            str(DEFAULT_NIP34_REPO_FIXTURE),
            "--nip34-collaboration-fixture",
            str(DEFAULT_NIP34_COLLAB_FIXTURE),
            "--nip34-state-status-fixture",
            str(DEFAULT_NIP34_STATE_STATUS_FIXTURE),
            "--nip34-live-readback-fixture",
            str(DEFAULT_NIP34_LIVE_READBACK_FIXTURE),
            "--live-evidence-index",
            str(DEFAULT_LIVE_EVIDENCE_INDEX),
        ]
    )
    render_project_page.main(
        [
            str(ROOT / "fixtures" / "portable-lab.registry.json"),
            str(ROOT / "output" / "portable-lab.html"),
        ]
    )
    render_forge_app.main([str(ROOT / "output" / "forge-app.html")])
    for registry_path, summary_path in [
        (ROOT / "fixtures" / "example-project.registry.json", ROOT / "output" / "demo-project.summary.json"),
        (ROOT / "fixtures" / "portable-lab.registry.json", ROOT / "output" / "portable-lab.summary.json"),
    ]:
        registry = render_project_page.load_registry(registry_path)
        write_json(summary_path, registry_summary(registry, registry_path))


def build_verification_bundle_manifest(paths: list[Path]) -> dict:
    files = []
    for path in paths:
        rel = relative(path)
        data = bundle_file_bytes(path)
        files.append(
            {
                "path": rel,
                "bundle_path": rel,
                "role": bundle_role(rel),
                "sha256": hashlib.sha256(data).hexdigest(),
                "size_bytes": len(data),
            }
        )

    live_evidence_index = json.loads(DEFAULT_LIVE_EVIDENCE_INDEX.read_text(encoding="utf-8"))
    indexed_evidence = []
    for item in live_evidence_index.get("evidence", []):
        if not isinstance(item, dict):
            continue
        evidence_file = item.get("evidence_file")
        indexed_evidence.append(
            {
                "id": item.get("id"),
                "protocol": item.get("protocol"),
                "state": item.get("state"),
                "evidence_file": evidence_file,
                "bundle_path": evidence_file,
                "evidence_sha256": item.get("evidence_sha256"),
                "evidence_size_bytes": item.get("evidence_size_bytes"),
            }
        )

    return {
        "schema_version": "decentralized-forge.verification-bundle.v1",
        "bundle_name": "decentralized-forge portable verification bundle",
        "scope": "portable local verification package; no live protocol actions, signing, spending, or publishing",
        "manifest_path": DEFAULT_BUNDLE_MANIFEST_PATH,
        "file_count": len(files),
        "files": files,
        "evidence_index": {
            "path": relative(DEFAULT_LIVE_EVIDENCE_INDEX),
            "schema_version": live_evidence_index.get("schema_version"),
            "entry_count": len(indexed_evidence),
            "entries": indexed_evidence,
        },
        "suggested_verification_commands": [
            "python scripts/forge_registry.py verify-bundle output/decentralized-forge-verification-bundle.zip",
            "python scripts/forge_registry.py verify-local --skip-npm-ci",
        ],
        "non_claims": [
            "bundle does not publish protocol events",
            "bundle does not sign events or use private keys",
            "bundle does not start daemons, spend money, use wallets, or contact paid services",
            "bundle does not claim durability, censorship resistance, broad availability, security, SLSA compliance, or production readiness",
        ],
    }


def write_deterministic_zip(output: Path, paths: list[Path], manifest: dict) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        for path in paths:
            rel = relative(path)
            info = zipfile.ZipInfo(rel, ZIP_FIXED_DATE_TIME)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o644 << 16
            archive.writestr(info, bundle_file_bytes(path))

        info = zipfile.ZipInfo(DEFAULT_BUNDLE_MANIFEST_PATH, ZIP_FIXED_DATE_TIME)
        info.create_system = 3
        info.compress_type = zipfile.ZIP_STORED
        info.external_attr = 0o644 << 16
        archive.writestr(info, stable_json_bytes(manifest))


def create_verification_bundle(output: Path = DEFAULT_BUNDLE_OUTPUT) -> dict:
    regenerate_portable_outputs()
    paths = collect_verification_bundle_paths()
    manifest = build_verification_bundle_manifest(paths)
    write_deterministic_zip(output, paths, manifest)
    return manifest


def verify_verification_bundle(bundle_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        with zipfile.ZipFile(bundle_path, "r") as archive:
            names = set(archive.namelist())
            if DEFAULT_BUNDLE_MANIFEST_PATH not in names:
                return [f"missing {DEFAULT_BUNDLE_MANIFEST_PATH}"]
            manifest = json.loads(archive.read(DEFAULT_BUNDLE_MANIFEST_PATH).decode("utf-8"))
            if manifest.get("schema_version") != "decentralized-forge.verification-bundle.v1":
                errors.append("unsupported verification bundle schema_version")
            if manifest.get("scope") != "portable local verification package; no live protocol actions, signing, spending, or publishing":
                errors.append("unexpected verification bundle scope")
            files = manifest.get("files")
            if not isinstance(files, list) or not files:
                return errors + ["manifest.files must be a non-empty array"]
            if manifest.get("file_count") != len(files):
                errors.append("manifest.file_count does not match files length")

            seen_paths: set[str] = set()
            for offset, item in enumerate(files):
                prefix = f"files[{offset}]"
                if not isinstance(item, dict):
                    errors.append(f"{prefix} must be an object")
                    continue
                rel = item.get("path")
                bundle_name = item.get("bundle_path")
                if not isinstance(rel, str) or not rel:
                    errors.append(f"{prefix}.path is required")
                    continue
                if rel in seen_paths:
                    errors.append(f"{prefix}.path duplicates {rel}")
                seen_paths.add(rel)
                if bundle_name != rel:
                    errors.append(f"{prefix}.bundle_path must match path")
                if rel not in names:
                    errors.append(f"{prefix}.path missing from zip: {rel}")
                    continue
                data = archive.read(rel)
                if item.get("size_bytes") != len(data):
                    errors.append(f"{prefix}.size_bytes does not match {rel}")
                if item.get("sha256") != hashlib.sha256(data).hexdigest():
                    errors.append(f"{prefix}.sha256 does not match {rel}")
                if item.get("role") != bundle_role(rel):
                    errors.append(f"{prefix}.role does not match expected role")

            for required in [
                "fixtures/example-project.registry.json",
                "fixtures/portable-lab.registry.json",
                "fixtures/live-evidence-index.json",
                "output/demo-project.html",
                "output/portable-lab.html",
                "output/forge-app.html",
                "output/demo-project.summary.json",
                "output/portable-lab.summary.json",
            ]:
                if required not in seen_paths:
                    errors.append(f"required payload missing from manifest: {required}")

            evidence_index = manifest.get("evidence_index")
            if not isinstance(evidence_index, dict):
                errors.append("manifest.evidence_index must be an object")
            else:
                entries = evidence_index.get("entries", [])
                if evidence_index.get("entry_count") != len(entries):
                    errors.append("manifest.evidence_index.entry_count does not match entries length")
                for offset, item in enumerate(entries):
                    prefix = f"evidence_index.entries[{offset}]"
                    evidence_file = item.get("evidence_file")
                    if evidence_file not in names:
                        errors.append(f"{prefix}.evidence_file missing from zip: {evidence_file}")
                        continue
                    data = archive.read(evidence_file)
                    canonical_data = data.replace(b"\r\n", b"\n")
                    if item.get("evidence_sha256") != hashlib.sha256(canonical_data).hexdigest():
                        errors.append(f"{prefix}.evidence_sha256 does not match bundled evidence")
                    if item.get("evidence_size_bytes") != len(canonical_data):
                        errors.append(f"{prefix}.evidence_size_bytes does not match bundled evidence")

            combined = json.dumps(manifest, sort_keys=True).lower()
            for marker in SECRET_MARKERS:
                if marker in combined:
                    errors.append(f"manifest contains secret marker {marker!r}")
            for phrase in ["does not publish protocol events", "does not sign events", "does not claim durability"]:
                if phrase not in combined:
                    errors.append(f"manifest missing non-claim phrase: {phrase}")
    except (OSError, zipfile.BadZipFile, json.JSONDecodeError, UnicodeDecodeError) as exc:
        return [f"cannot verify bundle: {exc}"]
    return errors


def command_validate(args: argparse.Namespace) -> int:
    for registry_path in args.registries:
        render_project_page.load_registry(registry_path)
        print(f"valid registry: {relative(registry_path)}")
    return 0


def command_render(args: argparse.Namespace) -> int:
    render_args = [str(args.registry), str(args.output)]
    if args.with_demo_fixtures:
        render_args.extend(
            [
                "--nip34-repo-fixture",
                str(DEFAULT_NIP34_REPO_FIXTURE),
                "--nip34-collaboration-fixture",
                str(DEFAULT_NIP34_COLLAB_FIXTURE),
                "--nip34-state-status-fixture",
                str(DEFAULT_NIP34_STATE_STATUS_FIXTURE),
                "--nip34-live-readback-fixture",
                str(DEFAULT_NIP34_LIVE_READBACK_FIXTURE),
                "--live-evidence-index",
                str(DEFAULT_LIVE_EVIDENCE_INDEX),
            ]
        )
    return render_project_page.main(render_args)


def command_export_summary(args: argparse.Namespace) -> int:
    registry = render_project_page.load_registry(args.registry)
    write_json(args.output, registry_summary(registry, args.registry))
    print(f"wrote summary: {relative(args.output)}")
    return 0


def command_render_app(args: argparse.Namespace) -> int:
    render_args = [str(args.output)]
    for registry in args.registries:
        render_args.extend(["--registry", str(registry)])
    return render_forge_app.main(render_args)


def command_export_bundle(args: argparse.Namespace) -> int:
    manifest = create_verification_bundle(args.output)
    print(f"wrote verification bundle: {relative(args.output)}")
    print(f"- manifest: {DEFAULT_BUNDLE_MANIFEST_PATH}")
    print(f"- files: {manifest['file_count']}")
    print(f"- evidence entries: {manifest['evidence_index']['entry_count']}")
    return 0


def command_verify_bundle(args: argparse.Namespace) -> int:
    errors = verify_verification_bundle(args.bundle)
    if errors:
        for error in errors:
            print(f"bundle verification error: {error}", file=sys.stderr)
        return 1
    print(f"valid verification bundle: {relative(args.bundle)}")
    return 0


def command_validate_evidence_index(args: argparse.Namespace) -> int:
    errors = validate_live_evidence_index(args.index)
    if errors:
        for error in errors:
            print(f"evidence index error: {error}", file=sys.stderr)
        return 1
    print(f"valid live evidence index: {relative(args.index)}")
    return 0


def command_refresh_evidence_hashes(args: argparse.Namespace) -> int:
    refreshed = refresh_live_evidence_hashes(args.index)
    if args.check:
        current = json.loads(args.index.read_text(encoding="utf-8"))
        if refreshed != current:
            print("live evidence index hashes are stale", file=sys.stderr)
            return 1
        print(f"live evidence index hashes are current: {relative(args.index)}")
        return 0
    args.index.write_text(f"{json.dumps(refreshed, indent=2)}\n", encoding="utf-8")
    errors = validate_live_evidence_index(args.index)
    if errors:
        for error in errors:
            print(f"evidence index error after refresh: {error}", file=sys.stderr)
        return 1
    print(f"refreshed live evidence index hashes: {relative(args.index)}")
    return 0


def doctor_report() -> dict:
    tools = {}
    for name in ["git", "node", "npm", "python", "rad", "nak"]:
        executable = shutil.which(name)
        if executable is None and sys.platform == "win32":
            executable = shutil.which(f"{name}.exe") or shutil.which(f"{name}.cmd")
        tools[name] = {"available": executable is not None, "path": executable}

    git_head = None
    git_branch = None
    git_clean = None
    if tools["git"]["available"]:
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        branch = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        git_head = head.stdout.strip() if head.returncode == 0 else None
        git_branch = branch.stdout.strip() if branch.returncode == 0 else None
        git_clean = status.returncode == 0 and status.stdout.strip() == ""

    evidence_errors = validate_live_evidence_index(DEFAULT_LIVE_EVIDENCE_INDEX)
    return {
        "schema_version": "decentralized-forge.doctor.v1",
        "scope": "local readiness only; no live protocol actions, signing, spending, or publishing",
        "python": sys.version.split()[0],
        "repository": {
            "root": relative(ROOT),
            "branch": git_branch,
            "head": git_head,
            "clean": git_clean,
        },
        "tools": tools,
        "checks": {
            "live_evidence_index_valid": not evidence_errors,
            "live_evidence_index_errors": evidence_errors,
            "radicle_broader_cli_blocked": not tools["rad"]["available"],
            "nostr_cli_optional_missing": not tools["nak"]["available"],
        },
        "non_claims": [
            "doctor does not publish protocol events",
            "doctor does not start daemons or persistent services",
            "doctor does not use private keys, wallets, paid services, or direct outreach",
            "doctor does not verify durability, broad availability, censorship resistance, security, SLSA compliance, or production readiness",
        ],
    }


def command_doctor(args: argparse.Namespace) -> int:
    report = doctor_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        repo = report["repository"]
        print("Decentralized Forge doctor")
        print(f"- scope: {report['scope']}")
        print(f"- branch: {repo['branch'] or 'unknown'}")
        print(f"- head: {repo['head'] or 'unknown'}")
        print(f"- clean worktree: {repo['clean']}")
        print(f"- live evidence index valid: {report['checks']['live_evidence_index_valid']}")
        for name, tool in report["tools"].items():
            print(f"- tool {name}: {'available' if tool['available'] else 'missing'}")
        for error in report["checks"]["live_evidence_index_errors"]:
            print(f"- evidence index error: {error}")
    return 0 if report["checks"]["live_evidence_index_valid"] else 1


def run_command(command: list[str]) -> int:
    print(f"+ {' '.join(command)}")
    result = subprocess.run(command, cwd=ROOT)
    return result.returncode


def npm_command(command: str) -> str:
    executable = shutil.which(command)
    if executable:
        return executable
    if sys.platform == "win32":
        executable = shutil.which(f"{command}.cmd")
        if executable:
            return executable
    return command


def command_verify_local(args: argparse.Namespace) -> int:
    commands = [
        [sys.executable, "-m", "json.tool", "schemas/project-registry.schema.json"],
        [sys.executable, "-m", "json.tool", "schemas/live-evidence-index.schema.json"],
        [sys.executable, "-m", "json.tool", "fixtures/example-project.registry.json"],
        [sys.executable, "-m", "json.tool", "fixtures/portable-lab.registry.json"],
        [sys.executable, "-m", "json.tool", "fixtures/radicle-backed-project.registry.json"],
        [sys.executable, "-m", "json.tool", "fixtures/nostr-repo-announcement.json"],
        [sys.executable, "-m", "json.tool", "fixtures/nostr-collaboration-events.json"],
        [sys.executable, "-m", "json.tool", "fixtures/nostr-repo-state-status.json"],
        [sys.executable, "-m", "json.tool", "fixtures/live-adapter-replay-checklist.json"],
        [sys.executable, "-m", "json.tool", "fixtures/live-evidence-index.json"],
        [sys.executable, "-m", "json.tool", "fixtures/keyless-attestation.registry-verification.json"],
        [
            sys.executable,
            "scripts/nip34_adapter.py",
            "fixtures/nostr-repo-announcement.json",
            "fixtures/nostr-collaboration-events.json",
            "fixtures/nostr-repo-state-status.json",
        ],
        [sys.executable, "scripts/preflight_static_artifact.py"],
        [sys.executable, "scripts/forge_registry.py", "validate-evidence-index", "fixtures/live-evidence-index.json"],
        [sys.executable, "scripts/forge_registry.py", "refresh-evidence-hashes", "fixtures/live-evidence-index.json", "--check"],
        [sys.executable, "scripts/forge_registry.py", "doctor", "--json"],
        [sys.executable, "scripts/forge_registry.py", "validate", "fixtures/example-project.registry.json", "fixtures/portable-lab.registry.json"],
        [sys.executable, "scripts/forge_registry.py", "render", "fixtures/portable-lab.registry.json", "output/portable-lab.html"],
        [sys.executable, "scripts/forge_registry.py", "render-app", "output/forge-app.html"],
        [sys.executable, "scripts/forge_registry.py", "export-summary", "fixtures/example-project.registry.json", "output/demo-project.summary.json"],
        [sys.executable, "scripts/forge_registry.py", "export-summary", "fixtures/portable-lab.registry.json", "output/portable-lab.summary.json"],
        [sys.executable, "scripts/forge_registry.py", "export-bundle", "output/decentralized-forge-verification-bundle.zip"],
        [sys.executable, "scripts/forge_registry.py", "verify-bundle", "output/decentralized-forge-verification-bundle.zip"],
        [sys.executable, "scripts/live_gate_inventory.py"],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
    ]
    if not args.skip_npm_ci:
        commands.append([npm_command("npm"), "ci"])
    commands.append([npm_command("npm"), "run", "verify:car-cid"])
    commands.append([npm_command("npm"), "run", "verify:helia"])

    for command in commands:
        exit_code = run_command(command)
        if exit_code:
            return exit_code

    failures = preflight_static_artifact.check_static_artifact()
    if failures:
        for failure in failures:
            print(f"preflight failure: {failure}", file=sys.stderr)
        return 1
    print("local verification passed")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate one or more registry fixtures")
    validate.add_argument("registries", type=Path, nargs="+")
    validate.set_defaults(func=command_validate)

    render = subparsers.add_parser("render", help="Render a registry fixture to static HTML")
    render.add_argument("registry", type=Path)
    render.add_argument("output", type=Path)
    render.add_argument(
        "--with-demo-fixtures",
        action="store_true",
        help="Include the repository's demo NIP-34 fixtures and live evidence index",
    )
    render.set_defaults(func=command_render)

    export_summary = subparsers.add_parser("export-summary", help="Export a deterministic registry summary JSON")
    export_summary.add_argument("registry", type=Path)
    export_summary.add_argument("output", type=Path)
    export_summary.set_defaults(func=command_export_summary)

    render_app = subparsers.add_parser("render-app", help="Render the static forge workbench app")
    render_app.add_argument("output", type=Path, nargs="?", default=render_forge_app.DEFAULT_OUTPUT)
    render_app.add_argument(
        "--registry",
        dest="registries",
        action="append",
        type=Path,
        default=[],
        help="Registry fixture to include; may be repeated",
    )
    render_app.set_defaults(func=command_render_app)

    export_bundle = subparsers.add_parser("export-bundle", help="Export a deterministic portable verification bundle")
    export_bundle.add_argument("output", type=Path, nargs="?", default=DEFAULT_BUNDLE_OUTPUT)
    export_bundle.set_defaults(func=command_export_bundle)

    verify_bundle = subparsers.add_parser("verify-bundle", help="Verify a portable verification bundle manifest and payload hashes")
    verify_bundle.add_argument("bundle", type=Path, nargs="?", default=DEFAULT_BUNDLE_OUTPUT)
    verify_bundle.set_defaults(func=command_verify_bundle)

    evidence_index = subparsers.add_parser("validate-evidence-index", help="Validate live evidence index paths, hashes, and claim boundaries")
    evidence_index.add_argument("index", type=Path, nargs="?", default=DEFAULT_LIVE_EVIDENCE_INDEX)
    evidence_index.set_defaults(func=command_validate_evidence_index)

    refresh_hashes = subparsers.add_parser("refresh-evidence-hashes", help="Add or check evidence file SHA-256 and size metadata")
    refresh_hashes.add_argument("index", type=Path, nargs="?", default=DEFAULT_LIVE_EVIDENCE_INDEX)
    refresh_hashes.add_argument("--check", action="store_true", help="Fail if committed hash metadata is stale")
    refresh_hashes.set_defaults(func=command_refresh_evidence_hashes)

    doctor = subparsers.add_parser("doctor", help="Report local tool and evidence readiness without live protocol actions")
    doctor.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    doctor.set_defaults(func=command_doctor)

    verify_local = subparsers.add_parser("verify-local", help="Run the documented local verification suite")
    verify_local.add_argument("--skip-npm-ci", action="store_true", help="Use already-installed Node dependencies")
    verify_local.set_defaults(func=command_verify_local)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (OSError, json.JSONDecodeError, render_project_page.RegistryError, ValueError) as exc:
        print(f"forge-registry error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
