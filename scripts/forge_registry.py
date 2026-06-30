#!/usr/bin/env python3
"""Local CLI for decentralized-forge registry fixtures."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import shutil
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter
from datetime import datetime, timezone
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
DEFAULT_BUNDLE_REVIEW_CHECKLIST = ROOT / "docs" / "portable-bundle-review-checklist.md"
DEFAULT_PUBLIC_SEED_STATUS_OUTPUT = ROOT / "output" / "public-seed-status.json"
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


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stable_json_bytes(payload: object) -> bytes:
    return f"{json.dumps(payload, indent=2, sort_keys=True)}\n".encode("utf-8")


def canonical_evidence_bytes(path: Path) -> bytes:
    """Return cross-platform evidence bytes with text line endings normalized."""
    return path.read_bytes().replace(b"\r\n", b"\n")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(canonical_evidence_bytes(path)).hexdigest()


def raw_sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def live_evidence_entry(entry_id: str, index_path: Path = DEFAULT_LIVE_EVIDENCE_INDEX) -> dict:
    index = json.loads(index_path.read_text(encoding="utf-8"))
    if not isinstance(index, dict) or not isinstance(index.get("evidence"), list):
        raise ValueError("live evidence index must be an object with evidence[]")
    for item in index["evidence"]:
        if isinstance(item, dict) and item.get("id") == entry_id:
            return item
    raise ValueError(f"live evidence entry not found: {entry_id}")


def retained_radicle_quickstart_model(index_path: Path = DEFAULT_LIVE_EVIDENCE_INDEX) -> dict:
    try:
        entry = live_evidence_entry("loop75-radicle-public-seed-update-d596024", index_path)
    except ValueError:
        try:
            entry = live_evidence_entry("loop72-radicle-public-seed-update-ef16e2a", index_path)
        except ValueError:
            try:
                entry = live_evidence_entry("loop70-radicle-public-seed-update-propagation", index_path)
            except ValueError:
                try:
                    entry = live_evidence_entry("loop67-radicle-vps-follower-public-readback", index_path)
                except ValueError:
                    try:
                        entry = live_evidence_entry("loop66-radicle-seed-restart-check", index_path)
                    except ValueError:
                        try:
                            entry = live_evidence_entry("loop65-radicle-independent-availability-check", index_path)
                        except ValueError:
                            entry = live_evidence_entry("loop63-radicle-retained-update-check", index_path)
    public = entry.get("public_identifiers")
    if not isinstance(public, dict):
        raise ValueError(f"{entry.get('id', 'retained Radicle evidence')} missing public_identifiers")

    is_public_vps_seed = entry.get("id") in {
        "loop67-radicle-vps-follower-public-readback",
        "loop70-radicle-public-seed-update-propagation",
        "loop72-radicle-public-seed-update-ef16e2a",
        "loop75-radicle-public-seed-update-d596024",
    }
    is_public_vps_update = entry.get("id") in {
        "loop70-radicle-public-seed-update-propagation",
        "loop72-radicle-public-seed-update-ef16e2a",
        "loop75-radicle-public-seed-update-d596024",
    }
    is_two_public_seed_update = entry.get("id") == "loop75-radicle-public-seed-update-d596024"
    is_independent_availability = entry.get("id") == "loop65-radicle-independent-availability-check"
    is_seed_restart = entry.get("id") == "loop66-radicle-seed-restart-check"
    required = ["rid", "current_source_commit", "retained_state_committed", "secret_values_recorded"]
    if is_public_vps_seed:
        required.extend(["vps_seed_address", "fresh_reader_readback_commit", "fresh_reader_readback_matches_expected", "public_seed_address_reachable"])
    elif is_seed_restart:
        required.extend(["second_reader_readback_commit", "second_reader_readback_matches_source", "same_seed_node_after_restart"])
    elif is_independent_availability:
        required.extend(["reader_b_readback_commit", "reader_b_readback_matches_source", "follower_seed_succeeded"])
    else:
        required.extend(["direct_seed_readback_commit", "direct_seed_readback_matches_source", "default_readback_matches_source"])
    missing = [key for key in required if key not in public]
    if missing:
        raise ValueError(f"{entry['id']} retained Radicle evidence missing fields: {', '.join(missing)}")
    if is_public_vps_seed:
        readback_key = "fresh_reader_readback_commit"
        matches_key = "fresh_reader_readback_matches_expected"
    elif is_seed_restart:
        readback_key = "second_reader_readback_commit"
        matches_key = "second_reader_readback_matches_source"
    elif is_independent_availability:
        readback_key = "reader_b_readback_commit"
        matches_key = "reader_b_readback_matches_source"
    else:
        readback_key = "direct_seed_readback_commit"
        matches_key = "direct_seed_readback_matches_source"
    if public[readback_key] != public["current_source_commit"]:
        raise ValueError(f"{entry['id']} readback commit does not match current source commit")
    if public[matches_key] is not True:
        raise ValueError(f"{entry['id']} readback did not match source")
    if is_public_vps_seed and public["public_seed_address_reachable"] is not True:
        raise ValueError(f"{entry['id']} public VPS seed address was not reachable")
    if is_seed_restart and public["same_seed_node_after_restart"] is not True:
        raise ValueError("loop66 seed restart did not preserve the retained seed node identity")
    if is_independent_availability and public["follower_seed_succeeded"] is not True:
        raise ValueError("loop65 follower seed did not succeed")
    if public["retained_state_committed"] is not False or public["secret_values_recorded"] is not False:
        raise ValueError(f"{entry['id']} retained Radicle evidence is not secret-free")
    if is_two_public_seed_update:
        availability_mode = "two public follower-seed update readback"
    elif is_public_vps_update:
        availability_mode = "public VPS follower-seed update readback"
    elif is_public_vps_seed:
        availability_mode = "public VPS follower-seed readback"
    elif is_seed_restart:
        availability_mode = "local seed restart readback"
    elif is_independent_availability:
        availability_mode = "independent follower-seed readback"
    else:
        availability_mode = "maintainer direct-seed readback"

    return {
        "schema_version": "decentralized-forge.radicle-retained-quickstart.v1",
        "source_evidence_id": entry["id"],
        "source_evidence_file": entry["evidence_file"],
        "rid": public["rid"],
        "expected_commit": public["current_source_commit"],
        "readback_commit": public[readback_key],
        "availability_mode": availability_mode,
        "follower_seed_succeeded": bool(public.get("follower_seed_succeeded", public.get("vps_seed_left_running", False))),
        "seed_restart_verified": bool(public.get("same_seed_node_after_restart", False)),
        "persistent_seed_service_left_running": bool(public.get("persistent_seed_service_left_running", public.get("vps_seed_left_running", False))),
        "seed_address_publicly_reachable": bool(public.get("public_seed_address_reachable", public.get("seed_address_publicly_reachable", False))),
        "default_public_routing_observed": bool(public.get("default_readback_matches_source", False)),
        "retained_state_committed": public["retained_state_committed"],
        "secret_values_recorded": public["secret_values_recorded"],
        "seed_peer_hint": public.get("vps_seed_address", "<seed-peer-id>@<reachable-host>:<port>"),
        "public_seeds": [
            {
                "id": "primary",
                "address": public.get("primary_public_seed_address", public.get("vps_seed_address", "<seed-peer-id>@<reachable-host>:<port>")),
                "node_id": public.get("primary_public_seed_node_id", public.get("vps_seed_node_id", "<seed-peer-id>")),
                "role": "primary public follower seed",
            },
            *(
                [
                    {
                        "id": "second",
                        "address": public["second_public_seed_address"],
                        "node_id": public.get("second_public_seed_node_id", public["second_public_seed_address"].split("@", 1)[0]),
                        "role": "second public follower seed via openclaw relay to ubuntu-work",
                    }
                ]
                if public.get("second_public_seed_address")
                else []
            ),
        ],
        "commands": [
            "rad auth --alias decentralized-forge-reader --stdin",
            "rad node start",
            f"rad node connect {public.get('vps_seed_address', '<seed-peer-id>@<reachable-host>:<port>')} --timeout 30s",
            f"rad clone --timeout 120s --seed {public.get('vps_seed_node_id', '<seed-peer-id>')} {public['rid']} decentralized-forge",
            "cd decentralized-forge",
            "git rev-parse HEAD",
        ],
        "expected_verification": [
            f"git rev-parse HEAD prints {public['current_source_commit']}",
            f"A mismatch means the clone did not reproduce the {entry['id']} readback claim.",
        ],
        "non_claims": [
            "not a default public-routing claim",
            "not a durability guarantee",
            "not proof of broad Radicle network availability",
            "not proof of censorship resistance",
            "not proof of identity trust",
            "not a security guarantee",
            "not production readiness",
            "not a committed secret or key backup",
            *(["not proof of automatic future update propagation"] if is_public_vps_update else []),
            *(
                ["not maintainer key material on the VPS"]
                if is_public_vps_seed
                else ["not a persistent public seed service claim"]
            ),
        ],
    }


def format_retained_radicle_quickstart(model: dict) -> str:
    lines = [
        "Retained Radicle direct-seed quickstart",
        "",
        f"- source evidence: `{model['source_evidence_file']}`",
        f"- RID: `{model['rid']}`",
        f"- expected commit: `{model['expected_commit']}`",
        f"- availability mode: `{model['availability_mode']}`",
        f"- follower seed succeeded in evidence: `{str(model['follower_seed_succeeded']).lower()}`",
        f"- seed restart verified in evidence: `{str(model['seed_restart_verified']).lower()}`",
        f"- public seed address observed: `{str(model['seed_address_publicly_reachable']).lower()}`",
        f"- persistent seed service left running: `{str(model['persistent_seed_service_left_running']).lower()}`",
        f"- default public routing observed: `{str(model['default_public_routing_observed']).lower()}`",
        f"- seed address needed: `{model['seed_peer_hint']}`",
        "",
        "This is a direct-seed path. A maintainer or follower seed operator must run a reachable Radicle node for this RID and share the peer address for the current session.",
        "",
        "Reader commands:",
        "",
        "```sh",
        *model["commands"],
        "```",
        "",
        "Expected verification:",
    ]
    lines.extend(f"- {item}" for item in model["expected_verification"])
    lines.extend(["", "Non-claims:"])
    lines.extend(f"- {item}" for item in model["non_claims"])
    return "\n".join(lines)


def first_public_clone_plan(args: argparse.Namespace) -> dict:
    model = retained_radicle_quickstart_model(args.index)
    seeds = {seed["id"]: seed for seed in model["public_seeds"]}
    if args.seed not in seeds:
        raise ValueError(f"seed {args.seed!r} is not available in retained Radicle evidence")
    seed = seeds[args.seed]
    return {
        "schema_version": "decentralized-forge.first-public-clone-verifier.v1",
        "created_utc": now_utc(),
        "mode": "plan" if args.plan_only else "live",
        "live_actions_executed": False,
        "source_evidence_id": model["source_evidence_id"],
        "source_evidence_file": model["source_evidence_file"],
        "rid": model["rid"],
        "expected_commit": model["expected_commit"],
        "seed": seed,
        "command": [
            sys.executable,
            "scripts/check_public_radicle_seed.py",
            "--seed",
            seed["address"],
            "--rid",
            model["rid"],
            "--expected-commit",
            model["expected_commit"],
        ],
        "expected_verification": f"git rev-parse HEAD prints {model['expected_commit']}",
        "secret_values_recorded": False,
        "non_claims": [
            "not a default public-routing claim",
            "not a durability guarantee",
            "not proof of automatic future update propagation",
            "not proof of broad Radicle network availability",
            "not proof of censorship resistance",
            "not proof of identity trust",
            "not a security guarantee",
            "not production readiness",
        ],
    }


def format_first_public_clone_result(result: dict) -> str:
    seed = result["seed"]
    lines = [
        "First public Radicle clone verifier",
        "",
        f"- mode: `{result['mode']}`",
        f"- source evidence: `{result['source_evidence_file']}`",
        f"- RID: `{result['rid']}`",
        f"- seed: `{seed['address']}`",
        f"- expected commit: `{result['expected_commit']}`",
    ]
    if result["mode"] == "plan":
        lines.extend(
            [
                "- live actions executed: `false`",
                "",
                "Planned command:",
                "",
                "```sh",
                " ".join(result["command"]),
                "```",
            ]
        )
    else:
        lines.extend(
            [
                f"- verification passed: `{str(result.get('verification_passed', False)).lower()}`",
                f"- readback commit: `{result.get('readback_commit', '')}`",
                f"- checker exit code: `{result.get('checker_exit_code')}`",
            ]
        )
    lines.extend(["", "Non-claims:"])
    lines.extend(f"- {item}" for item in result["non_claims"])
    return "\n".join(lines)


def public_seed_status_model(index_path: Path = DEFAULT_LIVE_EVIDENCE_INDEX) -> dict:
    quickstart = retained_radicle_quickstart_model(index_path)
    index = json.loads(index_path.read_text(encoding="utf-8"))
    clone_entries = {}
    for item in index.get("evidence", []):
        if not isinstance(item, dict) or item.get("protocol") != "radicle":
            continue
        public = item.get("public_identifiers", {})
        if not isinstance(public, dict):
            continue
        seed_id = public.get("seed_id")
        if seed_id not in {"primary", "second"}:
            continue
        if public.get("rid") != quickstart["rid"] or public.get("current_source_commit") != quickstart["expected_commit"]:
            continue
        if public.get("readback_matches_expected") is not True:
            continue
        scope = str(item.get("scope", ""))
        if "first_public_clone" not in scope:
            continue
        previous = clone_entries.get(seed_id)
        if previous is None or str(item.get("id", "")) > str(previous.get("id", "")):
            clone_entries[seed_id] = item

    seeds = []
    for seed in quickstart["public_seeds"]:
        entry = clone_entries.get(seed["id"], {})
        public = entry.get("public_identifiers", {}) if isinstance(entry, dict) else {}
        seeds.append(
            {
                "id": seed["id"],
                "role": seed["role"],
                "address": seed["address"],
                "node_id": seed["node_id"],
                "latest_evidence_id": entry.get("id"),
                "latest_evidence_file": entry.get("evidence_file"),
                "latest_state": entry.get("state"),
                "verified_at": entry.get("verified_at"),
                "verification_passed": public.get("readback_matches_expected") is True,
                "connected_to_seed": public.get("connected_to_seed") is True,
                "clone_succeeded": public.get("clone_succeeded") is True,
                "readback_commit": public.get("readback_commit"),
                "readback_matches_expected": public.get("readback_matches_expected") is True,
                "fresh_reader_environment": public.get("fresh_reader_environment"),
            }
        )

    return {
        "schema_version": "decentralized-forge.public-seed-status.v1",
        "source_index": relative(index_path),
        "source_index_loop": index.get("loop"),
        "source_evidence_id": quickstart["source_evidence_id"],
        "source_evidence_file": quickstart["source_evidence_file"],
        "rid": quickstart["rid"],
        "expected_commit": quickstart["expected_commit"],
        "status": "passing" if seeds and all(seed["readback_matches_expected"] for seed in seeds) else "attention-needed",
        "seed_count": len(seeds),
        "seeds": seeds,
        "recommended_commands": [
            "python scripts/forge_registry.py verify-first-public-clone --plan-only",
            "python scripts/forge_registry.py verify-first-public-clone --json",
            "python scripts/forge_registry.py verify-first-public-clone --seed second --json",
            "python scripts/forge_registry.py public-seed-status output/public-seed-status.json",
            "python scripts/run_first_public_clone_rehearsal.py",
        ],
        "non_claims": [
            "not an uptime or SLA claim",
            "not proof of automatic repair",
            "not proof of automatic future update propagation",
            "not a default public-routing claim",
            "not a durability guarantee",
            "not proof of independent provider or network availability",
            "not a security guarantee",
            "not production readiness",
        ],
    }


def command_public_seed_status(args: argparse.Namespace) -> int:
    status = public_seed_status_model(args.index)
    output = json.dumps(status, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(f"{output}\n", encoding="utf-8", newline="\n")
        print(f"wrote public seed status: {relative(args.output)}")
    else:
        print(output)
    return 0 if status["status"] == "passing" else 1


def slugify_project_id(value: str) -> str:
    slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in value).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "local-import"


def title_from_project_id(value: str) -> str:
    return " ".join(part.capitalize() for part in value.replace("_", "-").split("-") if part) or "Local Import"


def local_file_uri(path: Path) -> str:
    resolved = path.resolve()
    try:
        return f"file://{resolved.relative_to(ROOT).as_posix()}"
    except ValueError:
        return resolved.as_uri()


def git_value_at(cwd: Path, *args: str) -> str | None:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def local_repo_metadata(repo_path: Path) -> dict:
    repo = repo_path.resolve()
    if not repo.is_dir():
        raise ValueError(f"repository path is not a directory: {repo_path}")
    worktree = git_value_at(repo, "rev-parse", "--show-toplevel")
    if not worktree:
        raise ValueError(f"repository path is not inside a Git worktree: {repo_path}")
    root = Path(worktree).resolve()
    head = git_value_at(root, "rev-parse", "HEAD") or "0" * 40
    branch = git_value_at(root, "branch", "--show-current") or "main"
    committed_at = git_value_at(root, "log", "-1", "--format=%cI") or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    repo_name = root.name
    return {
        "root": root,
        "head": head,
        "branch": branch,
        "committed_at": committed_at,
        "repo_name": repo_name,
    }


def scaffold_registry_from_repo(
    repo_path: Path,
    *,
    project_id: str | None = None,
    name: str | None = None,
    description: str | None = None,
) -> dict:
    metadata = local_repo_metadata(repo_path)
    inferred_id = slugify_project_id(project_id or metadata["repo_name"])
    project_name = name or title_from_project_id(inferred_id)
    project_description = description or (
        f"Local-only registry scaffold for {project_name}. Generated from a local Git worktree without live protocol publication."
    )
    repo_uri = local_file_uri(metadata["root"])
    timestamp = metadata["committed_at"]
    head = metadata["head"]
    branch = metadata["branch"]

    return {
        "schema_version": "decentralized-forge.project-registry.v1",
        "project": {
            "id": inferred_id,
            "name": project_name,
            "description": project_description,
            "default_branch": branch,
            "web_urls": [],
        },
        "maintainers": [
            {
                "name": "Local Import Maintainer Placeholder",
                "id_type": "other",
                "public_id": "local-import-placeholder",
                "role": "maintainer-placeholder",
            }
        ],
        "clone_urls": [
            {
                "transport": "git",
                "url": repo_uri,
                "primary": True,
            }
        ],
        "issues": [],
        "patches": [],
        "releases": [],
        "substrates": {
            "forgefed": {
                "status": "not-configured-local-import",
            },
            "ipfs": {
                "artifact_cids": [],
                "cid_status": "no-artifact-cid",
                "pinning_status": "not-pinned",
                "live_ipfs_verified": False,
                "paid_storage": False,
                "durability_claim": False,
            },
            "sigstore_slsa": {
                "release_signature_status": "absent",
                "provenance_status": "absent",
                "real_sigstore_verified": False,
                "real_cosign_verified": False,
                "real_in_toto_verified": False,
                "slsa_level_claimed": False,
                "rekor_uploaded": False,
                "private_keys_used": False,
                "production_claim": "none",
            },
        },
        "verification_states": [
            {
                "scope": "registry.local_import_scaffold",
                "state": "local-fixture",
                "evidence": f"Generated from local Git worktree {repo_uri} at commit {head}.",
                "live_verified": False,
                "synthetic": False,
                "claim_boundary": "Local registry scaffold only; no live protocol publication, signing, durable storage, hosted service, or production readiness claim.",
                "last_checked_at": timestamp,
                "notes": "Replace placeholder maintainer identity, add artifacts/evidence, and rerun validation before sharing.",
            }
        ],
        "signature": {
            "status": "unsigned-fixture",
            "algorithm": "none",
            "value": "",
        },
        "created_at": timestamp,
        "updated_at": timestamp,
    }


def scaffold_registry_guidance(output: Path) -> list[str]:
    rel = relative(output)
    return [
        f"python scripts/forge_registry.py validate {rel}",
        f"python scripts/forge_registry.py attach-local-artifact {rel} path/to/artifact --version 0.1.0-local --tag v0.1.0-local",
        f"python scripts/forge_registry.py export-summary {rel} output/{output.stem}.summary.json",
        f"python scripts/forge_registry.py render {rel} output/{output.stem}.html",
        "Review placeholder maintainer identity before sharing.",
        "Add protocol mappings only when separately verified.",
        "Do not claim signing, durability, broad availability, censorship resistance, security, SLSA compliance, or production readiness from this scaffold.",
    ]


def media_type_for_artifact(path: Path, explicit_media_type: str | None = None) -> str:
    if explicit_media_type:
        return explicit_media_type
    if path.suffix.lower() in {".md", ".markdown"}:
        return "text/markdown"
    guessed_media_type, _encoding = mimetypes.guess_type(path.name)
    return guessed_media_type or "application/octet-stream"


def artifact_file_uri(path: Path) -> str:
    return local_file_uri(path)


def local_artifact_metadata(path: Path, *, name: str | None = None, media_type: str | None = None) -> dict:
    if not path.is_file():
        raise ValueError(f"artifact path is not a file: {path}")
    digest = raw_sha256_file(path)
    return {
        "name": name or path.name,
        "media_type": media_type_for_artifact(path, media_type),
        "size_bytes": path.stat().st_size,
        "sha256": digest,
        "hashes": {
            "sha256": digest,
        },
        "uri": artifact_file_uri(path),
        "availability": {
            "local_fixture": True,
            "pinned": False,
            "live_ipfs_verified": False,
            "paid_storage": False,
            "durability_claim": False,
            "notes": "Local file metadata only; no IPFS add, fetch, pin, gateway readback, paid storage, wallet, signing, or durability claim.",
        },
        "signature": "unsigned-local-artifact-metadata",
        "attestation": "absent",
    }


def attach_local_artifact_to_registry(
    registry_path: Path,
    artifact_path: Path,
    *,
    version: str,
    tag: str | None = None,
    name: str | None = None,
    media_type: str | None = None,
    timestamp: str | None = None,
) -> dict:
    registry = render_project_page.load_registry(registry_path)
    attached_at = timestamp or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    release_tag = tag or version
    artifact = local_artifact_metadata(artifact_path, name=name, media_type=media_type)
    releases = registry.setdefault("releases", [])
    release = next(
        (
            item
            for item in releases
            if isinstance(item, dict) and item.get("version") == version and item.get("tag") == release_tag
        ),
        None,
    )
    if release is None:
        release = {"version": version, "tag": release_tag, "artifacts": []}
        releases.append(release)
    release_artifacts = [item for item in release.get("artifacts", []) if item.get("name") != artifact["name"]]
    release_artifacts.append(artifact)
    release["artifacts"] = release_artifacts

    substrates = registry.setdefault("substrates", {})
    ipfs = substrates.setdefault("ipfs", {})
    ipfs["artifact_cids"] = [cid for cid in ipfs.get("artifact_cids", []) if cid]
    ipfs.setdefault("cid_status", "no-artifact-cid")
    ipfs["pinning_status"] = "not-pinned"
    ipfs["live_ipfs_verified"] = False
    ipfs["paid_storage"] = False
    ipfs["durability_claim"] = False

    sigstore_slsa = substrates.setdefault("sigstore_slsa", {})
    sigstore_slsa.setdefault("release_signature_status", "absent")
    sigstore_slsa.setdefault("provenance_status", "absent")
    sigstore_slsa["private_keys_used"] = False
    sigstore_slsa["slsa_level_claimed"] = False
    sigstore_slsa.setdefault("production_claim", "none")

    state = {
        "scope": "registry.local_artifact_metadata",
        "state": "local-fixture",
        "evidence": f"Attached local artifact metadata for {artifact['name']} at {artifact['uri']} with sha256 {artifact['sha256']}.",
        "live_verified": False,
        "synthetic": False,
        "claim_boundary": "Local file metadata only; no IPFS add, fetch, pin, gateway readback, paid storage, wallet, signing, durable storage, or production readiness claim.",
        "last_checked_at": attached_at,
        "notes": "Artifact bytes were hashed locally and referenced with a file URI; availability beyond this local file was not verified.",
    }
    states = [
        item
        for item in registry.get("verification_states", [])
        if not (
            isinstance(item, dict)
            and item.get("scope") == state["scope"]
            and artifact["name"] in item.get("evidence", "")
        )
    ]
    states.append(state)
    registry["verification_states"] = states
    registry["updated_at"] = attached_at
    render_project_page.validate_registry(registry)
    return registry


def attach_local_artifact_guidance(registry_path: Path) -> list[str]:
    rel = relative(registry_path)
    stem = registry_path.stem
    return [
        f"python scripts/forge_registry.py validate {rel}",
        f"python scripts/forge_registry.py export-summary {rel} output/{stem}.summary.json",
        f"python scripts/forge_registry.py render {rel} output/{stem}.html",
        "Treat the attached artifact as local metadata only until IPFS readback, pinning, signing, provenance, and release availability are separately verified.",
    ]


def next_collaboration_id(prefix: str, records: list[dict]) -> str:
    existing = {item.get("id") for item in records if isinstance(item, dict)}
    index = 1
    while f"{prefix}-{index}" in existing:
        index += 1
    return f"{prefix}-{index}"


def apply_local_collaboration_record(
    registry_path: Path,
    *,
    kind: str,
    title: str,
    summary: str = "",
    status: str | None = None,
    record_id: str | None = None,
    author: str | None = None,
    timestamp: str | None = None,
) -> dict:
    if kind not in {"issue", "patch"}:
        raise ValueError(f"unsupported collaboration kind: {kind}")
    if not title.strip():
        raise ValueError("collaboration title cannot be empty")

    registry = render_project_page.load_registry(registry_path)
    updated_at = timestamp or now_utc()
    collection_name = "issues" if kind == "issue" else "patches"
    prefix = "issue" if kind == "issue" else "patch"
    default_status = "open" if kind == "issue" else "proposed"
    allowed_statuses = {"open", "closed"} if kind == "issue" else {"proposed", "review", "accepted", "rejected", "merged"}
    resolved_status = status or default_status
    if resolved_status not in allowed_statuses:
        raise ValueError(f"unsupported {kind} status {resolved_status!r}; expected one of {sorted(allowed_statuses)}")

    records = registry.setdefault(collection_name, [])
    resolved_id = record_id or next_collaboration_id(prefix, records)
    record = {
        "id": resolved_id,
        "title": title.strip(),
        "status": resolved_status,
    }
    if author:
        record["author"] = author
    if summary:
        record["summary"] = summary
    records = [item for item in records if not (isinstance(item, dict) and item.get("id") == resolved_id)]
    records.append(record)
    registry[collection_name] = records

    scope = f"registry.local_collaboration.{kind}.{resolved_id}"
    state = {
        "scope": scope,
        "state": "local-fixture",
        "evidence": f"Recorded local {kind} {resolved_id} in {relative(registry_path)} with status {resolved_status}.",
        "live_verified": False,
        "synthetic": False,
        "claim_boundary": "Local registry collaboration record only; no Nostr publish/readback, Radicle patch submission, signing, relay delivery, hosted service, or production readiness claim.",
        "last_checked_at": updated_at,
        "notes": "Use the Nostr draft or selected-relay replay gate when live decentralized collaboration evidence is required.",
    }
    states = [
        item
        for item in registry.get("verification_states", [])
        if not (isinstance(item, dict) and item.get("scope") == scope)
    ]
    states.append(state)
    registry["verification_states"] = states
    registry["updated_at"] = updated_at
    render_project_page.validate_registry(registry)
    return registry


def parse_created_at(value: str | None = None) -> int:
    if value is None:
        return int(datetime.now(timezone.utc).timestamp())
    try:
        return int(value)
    except ValueError:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return int(parsed.timestamp())


def collaboration_record(registry: dict, *, kind: str, record_id: str) -> dict:
    collection = "issues" if kind == "issue" else "patches"
    for item in registry.get(collection, []):
        if isinstance(item, dict) and item.get("id") == record_id:
            return item
    raise ValueError(f"{kind} record not found: {record_id}")


def default_nostr_draft_paths(registry: dict, *, kind: str, record_id: str) -> tuple[Path, Path]:
    project_id = slugify_project_id(registry["project"]["id"])
    record_slug = slugify_project_id(record_id)
    stem = f"{project_id}.{kind}.{record_slug}.nostr-draft"
    return ROOT / "output" / f"{stem}.json", ROOT / "output" / f"{stem}.md"


def default_nostr_replay_paths(registry: dict) -> tuple[Path, Path]:
    project_id = slugify_project_id(registry["project"]["id"])
    return (
        ROOT / "output" / f"{project_id}.nostr-draft-readback-plan.json",
        ROOT / "evidence" / f"{project_id}.nostr-draft-collaboration-readback.json",
    )


def nostr_draft_export_command(registry_path: Path, registry: dict, *, kind: str, record_id: str) -> str:
    output_path, markdown_path = default_nostr_draft_paths(registry, kind=kind, record_id=record_id)
    return format_command(
        [
            "python",
            "scripts/forge_registry.py",
            "export-nostr-draft",
            relative(registry_path),
            kind,
            record_id,
            "--output",
            relative(output_path),
            "--markdown",
            relative(markdown_path),
        ]
    )


def nostr_replay_command(registry: dict, *, issue_id: str, patch_id: str, plan_only: bool) -> str:
    issue_draft, _issue_markdown = default_nostr_draft_paths(registry, kind="issue", record_id=issue_id)
    patch_draft, _patch_markdown = default_nostr_draft_paths(registry, kind="patch", record_id=patch_id)
    plan_path, evidence_path = default_nostr_replay_paths(registry)
    parts = [
        "node",
        "scripts/run_nostr_issue_patch_readback.mjs",
    ]
    if plan_only:
        parts.append("--plan-only")
    parts.extend(
        [
            "--draft",
            relative(issue_draft),
            "--draft",
            relative(patch_draft),
            "--output",
            relative(plan_path if plan_only else evidence_path),
        ]
    )
    return format_command(parts)


def collaboration_next_gate(
    registry_path: Path,
    registry: dict,
    *,
    issue_id: str | None = None,
    patch_id: str | None = None,
) -> dict:
    issues = [item for item in registry.get("issues", []) if isinstance(item, dict)]
    patches = [item for item in registry.get("patches", []) if isinstance(item, dict)]
    resolved_issue_id = issue_id or (issues[0]["id"] if issues else next_collaboration_id("issue", issues))
    resolved_patch_id = patch_id or (patches[0]["id"] if patches else next_collaboration_id("patch", patches))
    plan_path, evidence_path = default_nostr_replay_paths(registry)
    return {
        "status": "local-records-ready" if issues and patches else "local-records-needed",
        "issue_id": resolved_issue_id,
        "patch_id": resolved_patch_id,
        "add_issue_command": format_command(
            [
                "python",
                "scripts/forge_registry.py",
                "add-issue",
                relative(registry_path),
                "--id",
                resolved_issue_id,
                "--title",
                "Document first contributor task",
                "--summary",
                "Track the first project task.",
            ]
        ),
        "add_patch_command": format_command(
            [
                "python",
                "scripts/forge_registry.py",
                "add-patch",
                relative(registry_path),
                "--id",
                resolved_patch_id,
                "--title",
                "Add first patch proposal",
                "--summary",
                "Describe the first proposed change.",
            ]
        ),
        "export_issue_draft_command": nostr_draft_export_command(
            registry_path,
            registry,
            kind="issue",
            record_id=resolved_issue_id,
        ),
        "export_patch_draft_command": nostr_draft_export_command(
            registry_path,
            registry,
            kind="patch",
            record_id=resolved_patch_id,
        ),
        "plan_replay_command": nostr_replay_command(
            registry,
            issue_id=resolved_issue_id,
            patch_id=resolved_patch_id,
            plan_only=True,
        ),
        "live_replay_command": nostr_replay_command(
            registry,
            issue_id=resolved_issue_id,
            patch_id=resolved_patch_id,
            plan_only=False,
        ),
        "plan_output": relative(plan_path),
        "live_evidence_output": relative(evidence_path),
        "non_claims": [
            "add-issue and add-patch create local registry records only",
            "export-nostr-draft creates unsigned draft payloads only",
            "plan replay does not sign, publish, fetch, or read back from relays",
            "live replay uses disposable generated key material and selected-relay readback only",
            "not durability, global propagation, identity trust, security, full NIP-34/forge compatibility, or production readiness",
        ],
    }


def export_nostr_collaboration_draft(
    registry_path: Path,
    *,
    kind: str,
    record_id: str,
    output_path: Path | None = None,
    markdown_path: Path | None = None,
    pubkey: str = "0" * 64,
    created_at: str | None = None,
    relays: list[str] | None = None,
) -> dict:
    if kind not in {"issue", "patch"}:
        raise ValueError(f"unsupported collaboration kind: {kind}")
    registry = render_project_page.load_registry(registry_path)
    record = collaboration_record(registry, kind=kind, record_id=record_id)
    default_output, default_markdown = default_nostr_draft_paths(registry, kind=kind, record_id=record_id)
    output_path = output_path or default_output
    markdown_path = markdown_path or (output_path.with_suffix(".md") if output_path != default_output else default_markdown)
    created_at_int = parse_created_at(created_at)
    nip34 = registry.get("substrates", {}).get("nip34", {})
    repo_id = nip34.get("repo_id_tag") or registry["project"]["id"]
    relay_hints = list(dict.fromkeys([*(nip34.get("relay_hints", []) or []), *(relays or [])]))
    repository_address = f"{nip34_adapter.REPOSITORY_KIND}:{pubkey}:{repo_id}"
    event = {
        "pubkey": pubkey,
        "created_at": created_at_int,
        "kind": nip34_adapter.ISSUE_KIND if kind == "issue" else nip34_adapter.PATCH_KIND,
        "tags": [
            ["a", repository_address, "", "root"],
            ["subject", record["title"]],
            ["status", record["status"]],
            ["t", registry["project"]["id"]],
            ["client", "decentralized-forge-cli"],
        ],
        "content": record.get("summary", ""),
    }
    for relay in relay_hints:
        event["tags"].append(["relays", relay])
    conformance = nip34_adapter.conformance_report(event, label=f"{registry['project']['id']}.{kind}.{record_id}")
    draft = {
        "schema_version": "decentralized-forge.nostr-collaboration-draft.v1",
        "source_registry": relative(registry_path),
        "source_record": {
            "type": kind,
            "id": record_id,
            "title": record["title"],
            "status": record["status"],
            "author": record.get("author", ""),
        },
        "project": {
            "id": registry["project"]["id"],
            "name": registry["project"]["name"],
        },
        "repository_address": repository_address,
        "relay_hints": relay_hints,
        "event": event,
        "event_conformance": conformance,
        "live_replay_gate": {
            "status": "not-run-by-export",
            "current_fixture_command": "npm run live:nostr-issue-patch",
            "boundary": "The current live script proves the committed fixture issue/patch path; this project-specific draft must be signed with a disposable project-scoped key and read back from selected relays before any live collaboration claim.",
        },
        "non_claims": [
            "unsigned draft only",
            "not signed",
            "not published",
            "no relay readback",
            "not a Radicle patch submission",
            "not a hosted collaboration service",
            "not durable storage",
            "not production readiness",
        ],
    }
    write_json(output_path, draft)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(format_nostr_collaboration_draft_markdown(draft, output_path), encoding="utf-8", newline="\n")
    return draft


def format_nostr_collaboration_draft_markdown(draft: dict, output_path: Path) -> str:
    record = draft["source_record"]
    lines = [
        f"# Nostr {record['type'].title()} Draft",
        "",
        f"- Project: `{draft['project']['id']}`",
        f"- Record: `{record['id']}`",
        f"- Draft JSON: `{relative(output_path)}`",
        f"- Event kind: `{draft['event']['kind']}`",
        f"- Possible event id: `{draft['event_conformance'].get('possible_event_id') or 'not computed'}`",
        f"- Repository address: `{draft['repository_address']}`",
        "",
        "## Boundary",
        "",
        draft["live_replay_gate"]["boundary"],
        "",
        "## Non-Claims",
        "",
        *[f"- {item}" for item in draft["non_claims"]],
        "",
    ]
    return "\n".join(lines)


def refresh_registry_outputs(
    registry_path: Path,
    *,
    summary_output: Path | None = None,
    html_output: Path | None = None,
    workbench_output: Path | None = None,
    bundle_output: Path = DEFAULT_BUNDLE_OUTPUT,
    report_json_output: Path | None = None,
) -> dict:
    stem = registry_path.stem
    summary_path = summary_output or ROOT / "output" / f"{stem}.summary.json"
    html_path = html_output or ROOT / "output" / f"{stem}.html"
    workbench_path = workbench_output or ROOT / "output" / f"{stem}.forge-app.html"
    registry = render_project_page.load_registry(registry_path)
    render_project_page.main([str(registry_path), str(html_path)])
    write_json(summary_path, registry_summary(registry, registry_path))

    render_args = [str(workbench_path)]
    for candidate in [
        ROOT / "fixtures" / "example-project.registry.json",
        ROOT / "fixtures" / "portable-lab.registry.json",
        ROOT / "fixtures" / "onboarding-sample.registry.json",
        registry_path,
    ]:
        if candidate.is_file():
            render_args.extend(["--registry", str(candidate)])
    render_exit = render_forge_app.main(render_args)
    if render_exit:
        raise ValueError(f"workbench render failed for registry: {registry_path}")

    manifest = create_verification_bundle(bundle_output)
    errors = verify_verification_bundle(bundle_output)
    if errors:
        raise ValueError(f"verification bundle failed after registry refresh: {'; '.join(errors)}")
    report = bundle_report(bundle_output)
    if report_json_output is not None:
        write_json(report_json_output, report)
    return {
        "summary": summary_path,
        "html": html_path,
        "workbench": workbench_path,
        "bundle": bundle_output,
        "report_json": report_json_output,
        "bundle_manifest": manifest,
        "bundle_report": report,
    }


def apply_radicle_genesis_to_registry(
    registry_path: Path,
    evidence_path: Path,
    *,
    timestamp: str | None = None,
) -> dict:
    registry = render_project_page.load_registry(registry_path)
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    if evidence.get("schema_version") != "decentralized-forge.started-project-radicle-genesis.v1":
        raise ValueError(f"unsupported Radicle genesis evidence schema: {evidence_path}")
    if evidence.get("verification_passed") is not True:
        raise ValueError(f"Radicle genesis evidence did not pass verification: {evidence_path}")

    project = evidence.get("start_project", {})
    radicle = evidence.get("radicle", {})
    rid = radicle.get("rid")
    if not isinstance(rid, str) or not rid.startswith("rad:z"):
        raise ValueError(f"Radicle genesis evidence missing RID: {evidence_path}")
    if project.get("project_id") and project.get("project_id") != registry["project"]["id"]:
        raise ValueError(
            f"Radicle genesis project id {project.get('project_id')} does not match registry {registry['project']['id']}"
        )

    checked_at = timestamp or evidence.get("created_utc") or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    source_commit = radicle.get("project_git_commit", "")
    clone_commit = radicle.get("clone_commit", "")
    readback_matches = bool(radicle.get("readback_commit_matches_project"))

    substrates = registry.setdefault("substrates", {})
    substrates["radicle"] = {
        "rid": rid,
        "visibility": radicle.get("visibility", "unknown"),
        "seed_node_id": radicle.get("seed_node_id", ""),
        "genesis_status": "verified-disposable-genesis-readback",
        "project_git_commit": source_commit,
        "clone_commit": clone_commit,
        "readback_commit_matches_project": readback_matches,
        "remote_clone_succeeded": bool(radicle.get("remote_clone_succeeded")),
        "evidence_file": relative(evidence_path),
        "evidence_schema": evidence["schema_version"],
        "persistent_seed": False,
        "durability_claim": False,
        "default_public_routing_claim": False,
        "production_readiness_claim": False,
        "notes": "Project-specific Radicle RID was created and read back with disposable temporary state; no persistent seed or durability claim.",
    }

    clone_urls = [
        item
        for item in registry.get("clone_urls", [])
        if not (isinstance(item, dict) and item.get("transport") == "radicle")
    ]
    clone_urls.append({"transport": "radicle", "url": rid, "primary": False})
    registry["clone_urls"] = clone_urls

    state = {
        "scope": "registry.radicle_genesis_readback",
        "state": "live-verified",
        "evidence": f"Radicle RID {rid} was created for this project and cloned/read back at commit {clone_commit}; evidence {relative(evidence_path)}.",
        "live_verified": True,
        "synthetic": False,
        "claim_boundary": "Project-specific disposable Radicle genesis/readback only; no persistent seed, default public routing, durable storage, broad availability, security, SLSA compliance, or production readiness claim.",
        "last_checked_at": checked_at,
        "notes": "The RID is a recorded decentralized repository identity for this project. Availability beyond the bounded clone/readback evidence is not claimed.",
    }
    states = [
        item
        for item in registry.get("verification_states", [])
        if not (isinstance(item, dict) and item.get("scope") == state["scope"])
    ]
    states.append(state)
    registry["verification_states"] = states
    registry["updated_at"] = checked_at
    render_project_page.validate_registry(registry)
    return registry


def default_onboarding_registry_path(repo_path: Path, project_id: str | None = None) -> Path:
    metadata = local_repo_metadata(repo_path)
    slug = slugify_project_id(project_id or metadata["repo_name"])
    return ROOT / "fixtures" / f"{slug}.registry.json"


def onboard_local_project(
    repo_path: Path,
    artifact_path: Path,
    *,
    registry_output: Path | None = None,
    summary_output: Path | None = None,
    html_output: Path | None = None,
    bundle_output: Path = DEFAULT_BUNDLE_OUTPUT,
    report_json_output: Path | None = None,
    project_id: str | None = None,
    project_name: str | None = None,
    description: str | None = None,
    version: str = "0.0.0-local",
    tag: str | None = None,
    artifact_name: str | None = None,
    media_type: str | None = None,
    timestamp: str | None = None,
) -> dict:
    registry_path = registry_output or default_onboarding_registry_path(repo_path, project_id)
    stem = registry_path.stem
    summary_path = summary_output or ROOT / "output" / f"{stem}.summary.json"
    html_path = html_output or ROOT / "output" / f"{stem}.html"

    registry = scaffold_registry_from_repo(
        repo_path,
        project_id=project_id,
        name=project_name,
        description=description,
    )
    write_json(registry_path, registry)

    registry = attach_local_artifact_to_registry(
        registry_path,
        artifact_path,
        version=version,
        tag=tag,
        name=artifact_name,
        media_type=media_type,
        timestamp=timestamp,
    )
    write_json(registry_path, registry)
    validated_registry = render_project_page.load_registry(registry_path)
    write_json(summary_path, registry_summary(validated_registry, registry_path))

    render_exit = render_project_page.main([str(registry_path), str(html_path)])
    if render_exit:
        raise ValueError(f"render failed for onboarded registry: {registry_path}")

    manifest = create_verification_bundle(bundle_output)
    bundle_errors = verify_verification_bundle(bundle_output)
    if bundle_errors:
        raise ValueError(f"onboarding bundle verification failed: {'; '.join(bundle_errors)}")
    report = bundle_report(bundle_output)
    if report_json_output is not None:
        write_json(report_json_output, report)

    return {
        "registry": validated_registry,
        "paths": {
            "registry": registry_path,
            "summary": summary_path,
            "html": html_path,
            "bundle": bundle_output,
            "report_json": report_json_output,
        },
        "bundle_manifest": manifest,
        "bundle_report": report,
        "non_claims": [
            "local onboarding does not publish protocol events",
            "local onboarding does not sign events or use private keys",
            "local onboarding does not add, fetch, or pin IPFS content",
            "local onboarding does not claim durability, censorship resistance, broad availability, security, SLSA compliance, or production readiness",
        ],
    }


def default_start_artifact(repo_path: Path, artifact_path: Path | None) -> Path:
    if artifact_path is not None:
        return artifact_path
    readme = repo_path / "README.md"
    if readme.is_file():
        return readme
    raise ValueError("start-project needs --artifact when the repository has no README.md")


def radicle_genesis_output_paths(project_id: str) -> tuple[Path, Path]:
    slug = slugify_project_id(project_id)
    return (
        ROOT / "output" / f"{slug}.radicle-genesis.json",
        ROOT / "output" / f"{slug}.radicle-genesis.md",
    )


def radicle_genesis_command_parts(
    repo_path: Path,
    *,
    project_id: str,
    project_name: str,
    artifact_path: Path | None = None,
    evidence_output: Path | None = None,
    markdown_output: Path | None = None,
) -> list[str]:
    evidence, markdown = radicle_genesis_output_paths(project_id)
    evidence = evidence_output or evidence
    markdown = markdown_output or markdown
    command = [
        "python",
        "scripts/run_started_project_radicle_genesis.py",
        "--repository",
        relative(repo_path),
        "--project-id",
        project_id,
        "--project-name",
        project_name,
        "--output",
        relative(evidence),
        "--markdown",
        relative(markdown),
    ]
    if artifact_path is not None:
        command.extend(["--artifact", relative(artifact_path)])
    return command


def format_command(parts: list[str]) -> str:
    return " ".join(json.dumps(part) if any(ch.isspace() for ch in part) else part for part in parts)


def start_project_receipt(
    result: dict,
    *,
    repo_path: Path,
    app_output: Path,
    artifact_path: Path,
    radicle_evidence_output: Path | None = None,
    radicle_markdown_output: Path | None = None,
) -> dict:
    registry = result["registry"]
    paths = result["paths"]
    project_id = registry["project"]["id"]
    project_name = registry["project"]["name"]
    radicle_command_parts = radicle_genesis_command_parts(
        repo_path,
        project_id=project_id,
        project_name=project_name,
        artifact_path=artifact_path,
        evidence_output=radicle_evidence_output,
        markdown_output=radicle_markdown_output,
    )
    radicle_evidence, radicle_markdown = radicle_genesis_output_paths(project_id)
    radicle_evidence = radicle_evidence_output or radicle_evidence
    radicle_markdown = radicle_markdown_output or radicle_markdown
    collaboration_gate = collaboration_next_gate(paths["registry"], registry)
    return {
        "schema_version": "decentralized-forge.start-project-receipt.v1",
        "project": {
            "id": project_id,
            "name": project_name,
            "default_branch": registry["project"]["default_branch"],
        },
        "outputs": {
            "registry": relative(paths["registry"]),
            "summary": relative(paths["summary"]),
            "html": relative(paths["html"]),
            "workbench": relative(app_output),
            "bundle": relative(paths["bundle"]),
            "report_json": relative(paths["report_json"]) if paths["report_json"] is not None else None,
            "artifact": relative(artifact_path),
            "radicle_genesis_json": relative(radicle_evidence),
            "radicle_genesis_markdown": relative(radicle_markdown),
        },
        "next_commands": [
            f"python scripts/forge_registry.py validate {relative(paths['registry'])}",
            f"python scripts/forge_registry.py render {relative(paths['registry'])} {relative(paths['html'])}",
            f"python scripts/forge_registry.py render-app {relative(app_output)} --registry fixtures/example-project.registry.json --registry fixtures/portable-lab.registry.json --registry fixtures/onboarding-sample.registry.json --registry {relative(paths['registry'])}",
            collaboration_gate["add_issue_command"],
            collaboration_gate["add_patch_command"],
            collaboration_gate["export_issue_draft_command"],
            collaboration_gate["export_patch_draft_command"],
            collaboration_gate["plan_replay_command"],
            collaboration_gate["live_replay_command"],
            format_command(radicle_command_parts),
            "python scripts/forge_registry.py export-bundle output/decentralized-forge-verification-bundle.zip",
            "python scripts/forge_registry.py verify-bundle output/decentralized-forge-verification-bundle.zip",
        ],
        "collaboration_next_gate": collaboration_gate,
        "radicle_next_gate": {
            "status": "not-started-by-start-project",
            "summary": "Create a project Radicle RID only after a Linux host with Radicle CLI is selected and the run is recorded as bounded live evidence.",
            "command": format_command(radicle_command_parts),
            "evidence_json": relative(radicle_evidence),
            "evidence_markdown": relative(radicle_markdown),
            "non_claims": [
                "start-project does not create a Radicle RID",
                "start-project does not publish protocol events",
                "start-project does not start public seeds or background services",
                "start-project does not use private keys, wallets, paid services, or direct outreach",
                "start-project does not claim durability, censorship resistance, broad availability, security, SLSA compliance, or production readiness",
            ],
        },
        "non_claims": result["non_claims"],
    }


def start_project(
    repo_path: Path,
    artifact_path: Path | None,
    *,
    registry_output: Path | None = None,
    summary_output: Path | None = None,
    html_output: Path | None = None,
    app_output: Path | None = None,
    receipt_output: Path | None = None,
    bundle_output: Path = DEFAULT_BUNDLE_OUTPUT,
    report_json_output: Path | None = None,
    project_id: str | None = None,
    project_name: str | None = None,
    description: str | None = None,
    version: str = "0.1.0-local",
    tag: str | None = None,
    artifact_name: str | None = None,
    media_type: str | None = None,
    timestamp: str | None = None,
    radicle_evidence_output: Path | None = None,
    radicle_markdown_output: Path | None = None,
) -> dict:
    artifact = default_start_artifact(repo_path, artifact_path)
    result = onboard_local_project(
        repo_path,
        artifact,
        registry_output=registry_output,
        summary_output=summary_output,
        html_output=html_output,
        bundle_output=bundle_output,
        report_json_output=report_json_output,
        project_id=project_id,
        project_name=project_name,
        description=description,
        version=version,
        tag=tag,
        artifact_name=artifact_name,
        media_type=media_type,
        timestamp=timestamp,
    )
    registry_path = result["paths"]["registry"]
    stem = registry_path.stem
    workbench_path = app_output or ROOT / "output" / f"{stem}.forge-app.html"
    render_args = [str(workbench_path)]
    for registry in [
        ROOT / "fixtures" / "example-project.registry.json",
        ROOT / "fixtures" / "portable-lab.registry.json",
        ROOT / "fixtures" / "onboarding-sample.registry.json",
        registry_path,
    ]:
        if registry.is_file():
            render_args.extend(["--registry", str(registry)])
    render_exit = render_forge_app.main(render_args)
    if render_exit:
        raise ValueError(f"workbench render failed for started project: {registry_path}")

    receipt = start_project_receipt(
        result,
        repo_path=repo_path,
        app_output=workbench_path,
        artifact_path=artifact,
        radicle_evidence_output=radicle_evidence_output,
        radicle_markdown_output=radicle_markdown_output,
    )
    receipt_path = receipt_output or ROOT / "output" / f"{stem}.start-project.json"
    write_json(receipt_path, receipt)
    return {
        **result,
        "artifact": artifact,
        "app_output": workbench_path,
        "receipt": receipt,
        "receipt_output": receipt_path,
    }


def refresh_started_project_outputs(result: dict) -> dict:
    paths = result["paths"]
    registry_path = paths["registry"]
    render_project_page.main([str(registry_path), str(paths["html"])])
    write_json(paths["summary"], registry_summary(render_project_page.load_registry(registry_path), registry_path))

    render_args = [str(result["app_output"])]
    for registry in [
        ROOT / "fixtures" / "example-project.registry.json",
        ROOT / "fixtures" / "portable-lab.registry.json",
        ROOT / "fixtures" / "onboarding-sample.registry.json",
        registry_path,
    ]:
        if registry.is_file():
            render_args.extend(["--registry", str(registry)])
    render_exit = render_forge_app.main(render_args)
    if render_exit:
        raise ValueError(f"workbench render failed for started project: {registry_path}")
    manifest = create_verification_bundle(paths["bundle"])
    errors = verify_verification_bundle(paths["bundle"])
    if errors:
        raise ValueError(f"verification bundle failed after Radicle genesis: {'; '.join(errors)}")
    report = bundle_report(paths["bundle"])
    if paths["report_json"] is not None:
        write_json(paths["report_json"], report)
    result["bundle_manifest"] = manifest
    result["bundle_report"] = report
    return result


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
    for pattern in [
        "schemas/*.json",
        "fixtures/*.json",
        "fixtures/*.txt",
        "evidence/*",
        "output/*.html",
        "output/*.summary.json",
        "output/*.start-project.json",
        "output/*.nostr-draft.json",
        "output/*.nostr-draft.md",
    ]:
        paths.update(path for path in ROOT.glob(pattern) if path.is_file())

    for relative_path in [
        "README.md",
        "STATUS.md",
        "COMPLETION-CRITERIA.md",
        "AGENT-LOOPS.md",
        "docs/threat-model.md",
        "docs/community-quickstart.md",
        "docs/first-decentralized-repo-milestone.md",
        "docs/first-public-clone-outside-reader-rehearsal.md",
        "docs/first-public-clone-rc-plan.md",
        "docs/live-completion-gates.md",
        "docs/post-alpha-hardening-plan.md",
        "docs/product-finish-plan.md",
        "docs/radicle-persistent-seed-plan.md",
        "docs/radicle-retained-rid-quickstart.md",
        "docs/start-project-quickstart.md",
        relative(DEFAULT_BUNDLE_REVIEW_CHECKLIST),
        "package.json",
        "package-lock.json",
        "scripts/forge_registry.py",
        "scripts/render_project_page.py",
        "scripts/render_forge_app.py",
        "scripts/nip34_adapter.py",
        "scripts/preflight_static_artifact.py",
        "scripts/run_nostr_issue_patch_readback.mjs",
        "scripts/bootstrap_radicle_follower_seed.py",
        "scripts/check_public_radicle_seed.py",
        "scripts/run_first_public_clone_rehearsal.py",
        "scripts/refresh_radicle_follower_seed.py",
        "scripts/install_radicle_health_timer.py",
        "scripts/install_tcp_relay_user_service.py",
        "scripts/install_radicle_user_seed_service.py",
        "scripts/radicle_seed_host_control.py",
        "scripts/run_radicle_fresh_readback_check.py",
        "scripts/run_radicle_independent_availability_check.py",
        "scripts/run_radicle_project_repo_smoke.py",
        "scripts/run_started_project_radicle_genesis.py",
        "scripts/run_radicle_retained_delegate_check.py",
        "scripts/run_radicle_retained_update_check.py",
        "scripts/run_radicle_seed_restart_check.py",
        "scripts/run_radicle_update_continuity_check.py",
        "scripts/verify_car_cid_fixture.mjs",
        "scripts/verify_helia_fixture.mjs",
        "output/forge-app.html",
        relative(DEFAULT_PUBLIC_SEED_STATUS_OUTPUT),
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
    onboarding_registry = ROOT / "fixtures" / "onboarding-sample.registry.json"
    if onboarding_registry.is_file():
        render_forge_app.main(
            [
                str(ROOT / "output" / "forge-app-with-onboarding-sample.html"),
                "--registry",
                str(ROOT / "fixtures" / "example-project.registry.json"),
                "--registry",
                str(ROOT / "fixtures" / "portable-lab.registry.json"),
                "--registry",
                str(onboarding_registry),
            ]
        )
    for registry_path, summary_path in [
        (ROOT / "fixtures" / "example-project.registry.json", ROOT / "output" / "demo-project.summary.json"),
        (ROOT / "fixtures" / "portable-lab.registry.json", ROOT / "output" / "portable-lab.summary.json"),
    ]:
        registry = render_project_page.load_registry(registry_path)
        write_json(summary_path, registry_summary(registry, registry_path))
    if onboarding_registry.is_file():
        render_project_page.main([str(onboarding_registry), str(ROOT / "output" / "onboarding-sample.registry.html")])
        registry = render_project_page.load_registry(onboarding_registry)
        write_json(ROOT / "output" / "onboarding-sample.registry.summary.json", registry_summary(registry, onboarding_registry))
    export_nostr_collaboration_draft(
        ROOT / "fixtures" / "example-project.registry.json",
        kind="issue",
        record_id="ISSUE-1",
        output_path=ROOT / "output" / "demo-project.issue.issue-1.nostr-draft.json",
        markdown_path=ROOT / "output" / "demo-project.issue.issue-1.nostr-draft.md",
        created_at="2026-06-30T00:10:00Z",
    )
    export_nostr_collaboration_draft(
        ROOT / "fixtures" / "example-project.registry.json",
        kind="patch",
        record_id="PATCH-1",
        output_path=ROOT / "output" / "demo-project.patch.patch-1.nostr-draft.json",
        markdown_path=ROOT / "output" / "demo-project.patch.patch-1.nostr-draft.md",
        created_at="2026-06-30T00:11:00Z",
    )
    write_json(DEFAULT_PUBLIC_SEED_STATUS_OUTPUT, public_seed_status_model())


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
            "python scripts/forge_registry.py verify-bundle-cleanroom output/decentralized-forge-verification-bundle.zip",
            "python scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip",
            "python scripts/forge_registry.py export-bundle-release-note output/decentralized-forge-verification-bundle.zip",
            "python scripts/forge_registry.py radicle-retained-quickstart",
            "python scripts/forge_registry.py verify-first-public-clone --plan-only",
            "python scripts/forge_registry.py public-seed-status output/public-seed-status.json",
            "python scripts/forge_registry.py export-nostr-draft fixtures/example-project.registry.json issue ISSUE-1 --created-at 2026-06-30T00:10:00Z",
            "node scripts/run_nostr_issue_patch_readback.mjs --plan-only --draft output/demo-project.issue.issue-1.nostr-draft.json --draft output/demo-project.patch.patch-1.nostr-draft.json",
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
                "output/public-seed-status.json",
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


def safe_extract_bundle(bundle_path: Path, destination: Path) -> list[str]:
    errors: list[str] = []
    try:
        with zipfile.ZipFile(bundle_path, "r") as archive:
            seen: set[str] = set()
            destination_root = destination.resolve()
            for info in archive.infolist():
                name = info.filename
                if not name or name.endswith("/"):
                    continue
                if name in seen:
                    errors.append(f"duplicate zip entry: {name}")
                    continue
                seen.add(name)
                if "\\" in name:
                    errors.append(f"zip entry must use forward slashes: {name}")
                    continue
                path = Path(name)
                if path.is_absolute() or ".." in path.parts:
                    errors.append(f"zip entry escapes bundle root: {name}")
                    continue
                target = (destination_root / path).resolve()
                try:
                    target.relative_to(destination_root)
                except ValueError:
                    errors.append(f"zip entry escapes bundle root: {name}")
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.read(info))
    except (OSError, zipfile.BadZipFile) as exc:
        return [f"cannot extract bundle: {exc}"]
    return errors


def run_cleanroom_command(command: list[str], cwd: Path) -> list[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode == 0:
        return []
    output = "\n".join(part for part in [result.stdout.strip(), result.stderr.strip()] if part)
    return [f"cleanroom command failed ({' '.join(command)}): {output}"]


def verify_verification_bundle_cleanroom(bundle_path: Path) -> list[str]:
    errors = verify_verification_bundle(bundle_path)
    if errors:
        return errors

    with tempfile.TemporaryDirectory(prefix="df-bundle-cleanroom-") as tmpdir:
        cleanroom = Path(tmpdir)
        errors = safe_extract_bundle(bundle_path, cleanroom)
        if errors:
            return errors

        copied_bundle = cleanroom / "output" / "decentralized-forge-verification-bundle.zip"
        copied_bundle.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(bundle_path, copied_bundle)

        manifest_path = cleanroom / DEFAULT_BUNDLE_MANIFEST_PATH
        if not manifest_path.is_file():
            return [f"cleanroom missing {DEFAULT_BUNDLE_MANIFEST_PATH}"]
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return [f"cleanroom cannot read manifest: {exc}"]

        suggested = manifest.get("suggested_verification_commands")
        if not isinstance(suggested, list):
            return ["cleanroom manifest suggested_verification_commands must be an array"]
        for expected in [
            "python scripts/forge_registry.py verify-bundle output/decentralized-forge-verification-bundle.zip",
            "python scripts/forge_registry.py verify-bundle-cleanroom output/decentralized-forge-verification-bundle.zip",
        ]:
            if expected not in suggested:
                errors.append(f"cleanroom manifest missing suggested command: {expected}")

        commands = [
            [sys.executable, "-m", "json.tool", DEFAULT_BUNDLE_MANIFEST_PATH],
            [sys.executable, "scripts/forge_registry.py", "verify-bundle", "output/decentralized-forge-verification-bundle.zip"],
            [sys.executable, "scripts/forge_registry.py", "validate-evidence-index", "fixtures/live-evidence-index.json"],
            [sys.executable, "scripts/preflight_static_artifact.py"],
        ]
        for command in commands:
            errors.extend(run_cleanroom_command(command, cleanroom))
    return errors


def bundle_source_type(source: Path) -> str:
    return "directory" if source.is_dir() else "zip"


def read_bundle_source_bytes(source: Path, bundle_path: str) -> bytes:
    path = Path(bundle_path)
    if path.is_absolute() or ".." in path.parts or "\\" in bundle_path:
        raise ValueError(f"invalid bundle path: {bundle_path}")
    if source.is_dir():
        source_root = source.resolve()
        target = (source_root / path).resolve()
        try:
            target.relative_to(source_root)
        except ValueError as exc:
            raise ValueError(f"bundle path escapes source root: {bundle_path}") from exc
        return target.read_bytes()
    with zipfile.ZipFile(source, "r") as archive:
        return archive.read(bundle_path)


def read_bundle_source_json(source: Path, bundle_path: str) -> dict:
    payload = json.loads(read_bundle_source_bytes(source, bundle_path).decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{bundle_path} must contain a JSON object")
    return payload


def verify_bundle_source(source: Path) -> list[str]:
    if source.is_dir():
        manifest_path = source / DEFAULT_BUNDLE_MANIFEST_PATH
        if not manifest_path.is_file():
            return [f"missing {DEFAULT_BUNDLE_MANIFEST_PATH}"]
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return [f"cannot verify extracted bundle: {exc}"]
        errors: list[str] = []
        if manifest.get("schema_version") != "decentralized-forge.verification-bundle.v1":
            errors.append("unsupported verification bundle schema_version")
        if manifest.get("scope") != "portable local verification package; no live protocol actions, signing, spending, or publishing":
            errors.append("unexpected verification bundle scope")
        files = manifest.get("files")
        if not isinstance(files, list) or not files:
            return ["manifest.files must be a non-empty array"]
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
            if item.get("role") != bundle_role(rel):
                errors.append(f"{prefix}.role does not match expected role")
            try:
                data = read_bundle_source_bytes(source, rel)
            except (KeyError, OSError, ValueError) as exc:
                errors.append(f"{prefix}.path missing from extracted bundle: {rel} ({exc})")
                continue
            if item.get("size_bytes") != len(data):
                errors.append(f"{prefix}.size_bytes does not match {rel}")
            if item.get("sha256") != hashlib.sha256(data).hexdigest():
                errors.append(f"{prefix}.sha256 does not match {rel}")
        evidence_index = manifest.get("evidence_index")
        if not isinstance(evidence_index, dict):
            errors.append("manifest.evidence_index must be an object")
        else:
            entries = evidence_index.get("entries", [])
            if evidence_index.get("entry_count") != len(entries):
                errors.append("manifest.evidence_index.entry_count does not match entries length")
            for offset, item in enumerate(entries):
                prefix = f"evidence_index.entries[{offset}]"
                evidence_file = item.get("evidence_file") if isinstance(item, dict) else None
                if not isinstance(evidence_file, str):
                    errors.append(f"{prefix}.evidence_file is required")
                    continue
                try:
                    data = read_bundle_source_bytes(source, evidence_file).replace(b"\r\n", b"\n")
                except (KeyError, OSError, ValueError) as exc:
                    errors.append(f"{prefix}.evidence_file missing from extracted bundle: {evidence_file} ({exc})")
                    continue
                if item.get("evidence_sha256") != hashlib.sha256(data).hexdigest():
                    errors.append(f"{prefix}.evidence_sha256 does not match bundled evidence")
                if item.get("evidence_size_bytes") != len(data):
                    errors.append(f"{prefix}.evidence_size_bytes does not match bundled evidence")
        return errors
    return verify_verification_bundle(source)


def bundle_report(source: Path) -> dict:
    errors = verify_bundle_source(source)
    manifest = read_bundle_source_json(source, DEFAULT_BUNDLE_MANIFEST_PATH)
    files = manifest.get("files", [])
    file_roles = Counter(item.get("role", "unknown") for item in files if isinstance(item, dict))

    projects = []
    for item in files:
        if not isinstance(item, dict):
            continue
        rel = item.get("path")
        if not isinstance(rel, str) or not rel.startswith("fixtures/") or not rel.endswith(".registry.json"):
            continue
        registry = read_bundle_source_json(source, rel)
        if registry.get("schema_version") != "decentralized-forge.project-registry.v1":
            continue
        projects.append(registry_summary(registry, Path(rel)))

    evidence_index_path = manifest.get("evidence_index", {}).get("path", relative(DEFAULT_LIVE_EVIDENCE_INDEX))
    evidence_index = read_bundle_source_json(source, evidence_index_path)
    evidence_entries = evidence_index.get("evidence", [])
    if not isinstance(evidence_entries, list):
        evidence_entries = []
    protocols = Counter(item.get("protocol", "unknown") for item in evidence_entries if isinstance(item, dict))
    states = Counter(item.get("state", "unknown") for item in evidence_entries if isinstance(item, dict))

    evidence_summary_entries = []
    first_public_clone_entries = []
    for item in evidence_entries:
        if not isinstance(item, dict):
            continue
        public = item.get("public_identifiers", {})
        if isinstance(public, dict) and str(item.get("scope", "")).startswith("radicle.first_public_clone_rc."):
            first_public_clone_entries.append(
                {
                    "id": item.get("id"),
                    "state": item.get("state"),
                    "evidence_file": item.get("evidence_file"),
                    "rid": public.get("rid"),
                    "expected_commit": public.get("current_source_commit"),
                    "seed_id": public.get("seed_id"),
                    "seed_address": public.get("seed_address"),
                    "readback_commit": public.get("readback_commit"),
                    "readback_matches_expected": public.get("readback_matches_expected"),
                    "verifier_command": public.get("verifier_command"),
                    "fresh_reader_environment": public.get("fresh_reader_environment"),
                }
            )
        evidence_summary_entries.append(
            {
                "id": item.get("id"),
                "protocol": item.get("protocol"),
                "state": item.get("state"),
                "scope": item.get("scope"),
                "evidence_file": item.get("evidence_file"),
                "verification_summary": item.get("verification_summary"),
                "live_network_action": item.get("live_network_action"),
                "selected_relay_readback_verified": item.get("selected_relay_readback_verified"),
                "synthetic": item.get("synthetic"),
            }
        )

    public_seed_status = None
    public_seed_status_path = relative(DEFAULT_PUBLIC_SEED_STATUS_OUTPUT)
    if public_seed_status_path in {item.get("path") for item in files if isinstance(item, dict)}:
        try:
            public_seed_status = read_bundle_source_json(source, public_seed_status_path)
        except (OSError, json.JSONDecodeError, UnicodeDecodeError):
            public_seed_status = None

    verification_gaps = [
        "Durable storage, pinning, and broad availability remain unverified unless supported by a future evidence row.",
        "Censorship resistance, identity trust, production readiness, and security guarantees remain outside the bundle claim boundary.",
        "Live protocol checks are evidence-scoped to the recorded files and do not imply full NIP-34, Radicle, IPFS, or forge compatibility.",
        "The report is a local import/readback summary only; it does not sign, publish, fetch, pin, start daemons, spend money, or contact paid services.",
    ]

    return {
        "schema_version": "decentralized-forge.bundle-report.v1",
        "source": relative(source),
        "source_type": bundle_source_type(source),
        "verification": {
            "valid": not errors,
            "errors": errors,
        },
        "bundle": {
            "schema_version": manifest.get("schema_version"),
            "name": manifest.get("bundle_name"),
            "scope": manifest.get("scope"),
            "file_count": manifest.get("file_count"),
            "role_counts": dict(sorted(file_roles.items())),
            "suggested_verification_commands": manifest.get("suggested_verification_commands", []),
        },
        "projects": projects,
        "evidence": {
            "index_path": evidence_index_path,
            "entry_count": len(evidence_summary_entries),
            "protocol_counts": dict(sorted(protocols.items())),
            "state_counts": dict(sorted(states.items())),
            "live_network_action_count": sum(1 for item in evidence_entries if isinstance(item, dict) and item.get("live_network_action") is True),
            "selected_relay_readback_count": sum(
                1 for item in evidence_entries if isinstance(item, dict) and item.get("selected_relay_readback_verified") is True
            ),
            "synthetic_count": sum(1 for item in evidence_entries if isinstance(item, dict) and item.get("synthetic") is True),
            "entries": evidence_summary_entries,
        },
        "first_public_clone": {
            "entry_count": len(first_public_clone_entries),
            "rid": first_public_clone_entries[0]["rid"] if first_public_clone_entries else None,
            "expected_commit": first_public_clone_entries[0]["expected_commit"] if first_public_clone_entries else None,
            "entries": first_public_clone_entries,
            "claim_boundary": (
                "Fresh reader public direct-seed clone evidence only; not a durability, default-routing, "
                "independent-provider, security, identity-trust, or production-readiness claim."
            ),
        },
        "public_seed_status": {
            "path": public_seed_status_path,
            "available": isinstance(public_seed_status, dict),
            "status": public_seed_status.get("status") if isinstance(public_seed_status, dict) else None,
            "rid": public_seed_status.get("rid") if isinstance(public_seed_status, dict) else None,
            "expected_commit": public_seed_status.get("expected_commit") if isinstance(public_seed_status, dict) else None,
            "seed_count": public_seed_status.get("seed_count") if isinstance(public_seed_status, dict) else 0,
            "seeds": [
                {
                    "id": seed.get("id"),
                    "address": seed.get("address"),
                    "latest_state": seed.get("latest_state"),
                    "readback_commit": seed.get("readback_commit"),
                    "readback_matches_expected": seed.get("readback_matches_expected"),
                    "latest_evidence_file": seed.get("latest_evidence_file"),
                }
                for seed in public_seed_status.get("seeds", [])
                if isinstance(seed, dict)
            ]
            if isinstance(public_seed_status, dict)
            else [],
            "claim_boundary": (
                "Machine-readable status over committed public direct-seed readback evidence only; "
                "not uptime, durability, automatic repair, security, or production readiness."
            ),
        },
        "non_claims": manifest.get("non_claims", []),
        "verification_gaps": verification_gaps,
    }


def format_bundle_report(report: dict) -> str:
    lines = [
        "Decentralized Forge bundle report",
        f"- source: {report['source']} ({report['source_type']})",
        f"- verification: {'valid' if report['verification']['valid'] else 'invalid'}",
        f"- files: {report['bundle']['file_count']}",
    ]
    role_counts = report["bundle"]["role_counts"]
    if role_counts:
        lines.append(f"- roles: {', '.join(f'{role}={count}' for role, count in role_counts.items())}")

    lines.append("")
    lines.append("Projects")
    for project in report["projects"]:
        counts = project["counts"]
        verification = project["verification"]
        lines.append(
            f"- {project['project']['id']}: {project['project']['name']} "
            f"(maintainers={counts['maintainers']}, clone_urls={counts['clone_urls']}, "
            f"issues={counts['issues']}, patches={counts['patches']}, releases={counts['releases']}, "
            f"verification_states={verification['total']})"
        )

    evidence = report["evidence"]
    lines.append("")
    lines.append("Evidence")
    lines.append(
        f"- entries: {evidence['entry_count']}; protocols: "
        f"{', '.join(f'{key}={value}' for key, value in evidence['protocol_counts'].items())}"
    )
    lines.append(
        f"- live_network_action={evidence['live_network_action_count']}; "
        f"selected_relay_readback={evidence['selected_relay_readback_count']}; synthetic={evidence['synthetic_count']}"
    )

    public_clone = report.get("first_public_clone", {})
    if public_clone.get("entry_count"):
        lines.append("")
        lines.append("First public clone RC")
        lines.append(f"- rid: {public_clone['rid']}")
        lines.append(f"- expected_commit: {public_clone['expected_commit']}")
        for entry in public_clone["entries"]:
            lines.append(
                f"- {entry['seed_id']}: {entry['seed_address']} -> {entry['readback_commit']} "
                f"({entry['state']}; {entry['evidence_file']})"
            )
        lines.append(f"- boundary: {public_clone['claim_boundary']}")

    public_seed = report.get("public_seed_status", {})
    if public_seed.get("available"):
        lines.append("")
        lines.append("Public seed status")
        lines.append(f"- status: {public_seed['status']}")
        lines.append(f"- path: {public_seed['path']}")
        lines.append(f"- rid: {public_seed['rid']}")
        lines.append(f"- expected_commit: {public_seed['expected_commit']}")
        for seed in public_seed["seeds"]:
            lines.append(
                f"- {seed['id']}: {seed['address']} -> {seed['readback_commit']} "
                f"(matches_expected={str(seed['readback_matches_expected']).lower()}; {seed['latest_evidence_file']})"
            )
        lines.append(f"- boundary: {public_seed['claim_boundary']}")

    lines.append("")
    lines.append("Non-claims")
    for item in report["non_claims"]:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("Verification gaps")
    for item in report["verification_gaps"]:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("Suggested commands")
    for item in report["bundle"]["suggested_verification_commands"]:
        lines.append(f"- {item}")
    return "\n".join(lines)


def git_output(args: list[str]) -> str | None:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def git_commit_sha() -> str:
    return git_output(["rev-parse", "HEAD"]) or "unknown"


def git_worktree_clean() -> bool | None:
    status = git_output(["status", "--porcelain"])
    if status is None:
        return None
    return status == ""


def extract_checklist_stop_conditions(checklist_path: Path = DEFAULT_BUNDLE_REVIEW_CHECKLIST) -> list[str]:
    text = checklist_path.read_text(encoding="utf-8")
    marker = "## Stop Conditions"
    if marker not in text:
        return []
    stop_section = text.split(marker, 1)[1].split("\n## ", 1)[0]
    return [line.removeprefix("- ").strip() for line in stop_section.splitlines() if line.startswith("- ")]


def format_bundle_release_note(bundle_path: Path = DEFAULT_BUNDLE_OUTPUT, checklist_path: Path = DEFAULT_BUNDLE_REVIEW_CHECKLIST) -> str:
    report = bundle_report(bundle_path)
    bundle_bytes = bundle_path.read_bytes()
    stop_conditions = extract_checklist_stop_conditions(checklist_path)
    commit = git_commit_sha()
    clean = git_worktree_clean()
    clean_label = "unknown" if clean is None else str(clean).lower()

    lines = [
        "# Decentralized Forge Portable Bundle Release Note",
        "",
        f"- commit: `{commit}`",
        f"- bundle: `{relative(bundle_path)}`",
        f"- bundle_sha256: `{hashlib.sha256(bundle_bytes).hexdigest()}`",
        f"- bundle_size_bytes: `{len(bundle_bytes)}`",
        f"- verification: `{'valid' if report['verification']['valid'] else 'invalid'}`",
        f"- working_tree_clean_at_export: `{clean_label}`",
        "",
        "## Scope",
        "",
        "This is a local verification package over committed fixtures, generated outputs, source evidence files, and verifier scripts. It is not a production forge, signed release, durability proof, broad availability proof, censorship-resistance proof, security guarantee, or SLSA compliance claim.",
        "",
        "## Bundle Summary",
        "",
        f"- files: `{report['bundle']['file_count']}`",
        f"- roles: {', '.join(f'`{role}={count}`' for role, count in report['bundle']['role_counts'].items())}",
        f"- evidence_entries: `{report['evidence']['entry_count']}`",
        f"- live_network_action_entries: `{report['evidence']['live_network_action_count']}`",
        f"- selected_relay_readback_entries: `{report['evidence']['selected_relay_readback_count']}`",
        "",
    ]

    public_clone = report.get("first_public_clone", {})
    lines.extend(["## First Public Clone RC", ""])
    if public_clone.get("entry_count"):
        lines.append(f"- rid: `{public_clone['rid']}`")
        lines.append(f"- expected_commit: `{public_clone['expected_commit']}`")
        for entry in public_clone["entries"]:
            lines.append(
                f"- `{entry['seed_id']}`: `{entry['seed_address']}` -> `{entry['readback_commit']}` "
                f"via `{entry['evidence_file']}`"
            )
        lines.append(f"- boundary: {public_clone['claim_boundary']}")
    else:
        lines.append("- no first public clone RC evidence found in the bundle report")

    public_seed = report.get("public_seed_status", {})
    lines.extend(["", "## Public Seed Status", ""])
    if public_seed.get("available"):
        lines.append(f"- status: `{public_seed['status']}`")
        lines.append(f"- status_artifact: `{public_seed['path']}`")
        lines.append(f"- rid: `{public_seed['rid']}`")
        lines.append(f"- expected_commit: `{public_seed['expected_commit']}`")
        for seed in public_seed["seeds"]:
            lines.append(
                f"- `{seed['id']}`: `{seed['address']}` -> `{seed['readback_commit']}` "
                f"via `{seed['latest_evidence_file']}`"
            )
        lines.append(f"- boundary: {public_seed['claim_boundary']}")
    else:
        lines.append("- no public seed status artifact found in the bundle report")

    lines.extend(["", "## Projects", ""])

    for project in report["projects"]:
        counts = project["counts"]
        lines.append(
            f"- `{project['project']['id']}`: {project['project']['name']} "
            f"(issues={counts['issues']}, patches={counts['patches']}, releases={counts['releases']}, "
            f"verification_states={project['verification']['total']})"
        )

    lines.extend(["", "## Required Verification Commands", ""])
    for command in report["bundle"]["suggested_verification_commands"]:
        lines.append(f"- `{command}`")
    lines.append(f"- `python scripts/forge_registry.py export-bundle {relative(bundle_path)}`")
    lines.append(f"- `python scripts/forge_registry.py report-bundle {relative(bundle_path)} --json`")

    lines.extend(["", "## Non-Claims", ""])
    for item in report["non_claims"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Verification Gaps", ""])
    for item in report["verification_gaps"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Stop Conditions", ""])
    for item in stop_conditions:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Attachments",
            "",
            f"- `{relative(bundle_path)}`",
            f"- `docs/portable-bundle-review-checklist.md`",
            "- this release note, generated after the target commit exists",
            "",
        ]
    )
    return "\n".join(lines)


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


def command_scaffold_registry(args: argparse.Namespace) -> int:
    registry = scaffold_registry_from_repo(
        args.repository,
        project_id=args.project_id,
        name=args.name,
        description=args.description,
    )
    write_json(args.output, registry)
    render_project_page.load_registry(args.output)
    print(f"wrote registry scaffold: {relative(args.output)}")
    print("- scope: local Git worktree import only; no live protocol publication, signing, or durability claim")
    print("- next steps:")
    for item in scaffold_registry_guidance(args.output):
        print(f"  - {item}")
    return 0


def command_attach_local_artifact(args: argparse.Namespace) -> int:
    registry = attach_local_artifact_to_registry(
        args.registry,
        args.artifact,
        version=args.version,
        tag=args.tag,
        name=args.name,
        media_type=args.media_type,
        timestamp=args.timestamp,
    )
    write_json(args.registry, registry)
    render_project_page.load_registry(args.registry)
    print(f"attached local artifact metadata: {relative(args.artifact)} -> {relative(args.registry)}")
    print("- scope: local file metadata only; no IPFS add/fetch/pin, signing, paid storage, or durability claim")
    print("- next steps:")
    for item in attach_local_artifact_guidance(args.registry):
        print(f"  - {item}")
    return 0


def command_add_collaboration_record(args: argparse.Namespace) -> int:
    registry = apply_local_collaboration_record(
        args.registry,
        kind=args.kind,
        title=args.title,
        summary=args.summary or "",
        status=args.status,
        record_id=args.id,
        author=args.author,
        timestamp=args.timestamp,
    )
    write_json(args.registry, registry)
    collection_name = "issues" if args.kind == "issue" else "patches"
    record = registry[collection_name][-1]
    if args.kind == "issue":
        collaboration_gate = collaboration_next_gate(args.registry, registry, issue_id=record["id"])
    else:
        collaboration_gate = collaboration_next_gate(args.registry, registry, patch_id=record["id"])
    print(f"recorded local {args.kind}: {record['id']} -> {relative(args.registry)}")
    print("- scope: local registry collaboration record only; no publish, signing, relay delivery, or production claim")
    print("- collaboration next gate:")
    print(f"  - {collaboration_gate[f'export_{args.kind}_draft_command']}")
    if collaboration_gate["status"] != "local-records-ready":
        counterpart = "patch" if args.kind == "issue" else "issue"
        print(f"  - add the first {counterpart} record before running the issue+patch replay plan")
    print(f"  - {collaboration_gate['plan_replay_command']}")
    print(f"  - {collaboration_gate['live_replay_command']}")
    if args.no_refresh:
        print("- refresh skipped")
        print(f"  - python scripts/forge_registry.py render {relative(args.registry)} output/{args.registry.stem}.html")
        print(f"  - python scripts/forge_registry.py render-app output/{args.registry.stem}.forge-app.html --registry {relative(args.registry)}")
        return 0

    refreshed = refresh_registry_outputs(
        args.registry,
        summary_output=args.summary_output,
        html_output=args.html,
        workbench_output=args.workbench,
        bundle_output=args.bundle,
        report_json_output=args.report_json,
    )
    print(f"- summary: {relative(refreshed['summary'])}")
    print(f"- html: {relative(refreshed['html'])}")
    print(f"- workbench: {relative(refreshed['workbench'])}")
    print(f"- bundle: {relative(refreshed['bundle'])}")
    if refreshed["report_json"] is not None:
        print(f"- report_json: {relative(refreshed['report_json'])}")
    print(f"- bundle_valid: {str(refreshed['bundle_report']['verification']['valid']).lower()}")
    print("- next gate: export Nostr drafts, review the replay plan, then run bounded selected-relay replay only when live decentralized collaboration evidence is required")
    return 0


def command_export_nostr_draft(args: argparse.Namespace) -> int:
    draft = export_nostr_collaboration_draft(
        args.registry,
        kind=args.kind,
        record_id=args.record_id,
        output_path=args.output,
        markdown_path=args.markdown,
        pubkey=args.pubkey,
        created_at=args.created_at,
        relays=args.relay,
    )
    output_path = args.output or default_nostr_draft_paths(
        render_project_page.load_registry(args.registry),
        kind=args.kind,
        record_id=args.record_id,
    )[0]
    markdown_path = args.markdown or output_path.with_suffix(".md")
    print(f"wrote Nostr {args.kind} draft: {relative(output_path)}")
    print(f"- markdown: {relative(markdown_path)}")
    print(f"- kind: {draft['event']['kind']}")
    print(f"- possible_event_id: {draft['event_conformance'].get('possible_event_id') or 'not computed'}")
    print("- scope: unsigned local NIP-34-shaped draft only; no signing, publish, relay readback, or production claim")
    print(f"- live gate: {draft['live_replay_gate']['boundary']}")
    return 0


def command_onboard_local_project(args: argparse.Namespace) -> int:
    result = onboard_local_project(
        args.repository,
        args.artifact,
        registry_output=args.registry,
        summary_output=args.summary,
        html_output=args.html,
        bundle_output=args.bundle,
        report_json_output=args.report_json,
        project_id=args.project_id,
        project_name=args.project_name,
        description=args.description,
        version=args.version,
        tag=args.tag,
        artifact_name=args.artifact_name,
        media_type=args.media_type,
        timestamp=args.timestamp,
    )
    paths = result["paths"]
    report = result["bundle_report"]
    registry = result["registry"]
    print(f"onboarded local project: {registry['project']['id']}")
    print("- scope: local scaffold, local artifact metadata, local render, and local bundle/report refresh only")
    print(f"- registry: {relative(paths['registry'])}")
    print(f"- summary: {relative(paths['summary'])}")
    print(f"- html: {relative(paths['html'])}")
    print(f"- bundle: {relative(paths['bundle'])}")
    if paths["report_json"] is not None:
        print(f"- report_json: {relative(paths['report_json'])}")
    print(f"- bundle_valid: {str(report['verification']['valid']).lower()}")
    print(f"- bundle_files: {report['bundle']['file_count']}")
    print("- non-claims:")
    for item in result["non_claims"]:
        print(f"  - {item}")
    return 0


def command_start_project(args: argparse.Namespace) -> int:
    result = start_project(
        args.repository,
        args.artifact,
        registry_output=args.registry,
        summary_output=args.summary,
        html_output=args.html,
        app_output=args.workbench,
        receipt_output=args.receipt,
        bundle_output=args.bundle,
        report_json_output=args.report_json,
        project_id=args.project_id,
        project_name=args.project_name,
        description=args.description,
        version=args.version,
        tag=args.tag,
        artifact_name=args.artifact_name,
        media_type=args.media_type,
        timestamp=args.timestamp,
        radicle_evidence_output=args.radicle_evidence,
        radicle_markdown_output=args.radicle_markdown,
    )
    registry = result["registry"]
    paths = result["paths"]
    report = result["bundle_report"]
    print(f"started project: {registry['project']['id']}")
    print("- scope: local project registry, local artifact metadata, rendered project page, workbench entry, and verification bundle")
    print(f"- registry: {relative(paths['registry'])}")
    print(f"- summary: {relative(paths['summary'])}")
    print(f"- html: {relative(paths['html'])}")
    print(f"- workbench: {relative(result['app_output'])}")
    print(f"- receipt: {relative(result['receipt_output'])}")
    print(f"- bundle: {relative(paths['bundle'])}")
    print(f"- bundle_valid: {str(report['verification']['valid']).lower()}")
    print("- next commands:")
    for item in result["receipt"]["next_commands"]:
        print(f"  - {item}")
    print("- radicle next gate:")
    print(f"  - {result['receipt']['radicle_next_gate']['summary']}")
    print(f"  - {result['receipt']['radicle_next_gate']['command']}")
    if args.run_radicle_genesis:
        run_command = radicle_genesis_command_parts(
            args.repository,
            project_id=registry["project"]["id"],
            project_name=registry["project"]["name"],
            artifact_path=result["artifact"],
            evidence_output=args.radicle_evidence,
            markdown_output=args.radicle_markdown,
        )
        run_command[0] = sys.executable
        completed = subprocess.run(run_command, cwd=ROOT, check=False)
        if completed.returncode != 0:
            print(f"- radicle genesis failed: exit {completed.returncode}")
            return completed.returncode
        evidence_path, _markdown_path = radicle_genesis_output_paths(registry["project"]["id"])
        evidence_path = args.radicle_evidence or evidence_path
        registry = apply_radicle_genesis_to_registry(paths["registry"], evidence_path)
        write_json(paths["registry"], registry)
        result["registry"] = registry
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        result["receipt"]["radicle_next_gate"]["status"] = "completed-by-run-radicle-genesis"
        result["receipt"]["radicle_next_gate"]["rid"] = evidence["radicle"]["rid"]
        result["receipt"]["radicle_next_gate"]["readback_commit"] = evidence["radicle"]["clone_commit"]
        result["receipt"]["radicle_result"] = {
            "status": "verified-disposable-genesis-readback",
            "rid": evidence["radicle"]["rid"],
            "project_git_commit": evidence["radicle"]["project_git_commit"],
            "clone_commit": evidence["radicle"]["clone_commit"],
            "readback_commit_matches_project": evidence["radicle"]["readback_commit_matches_project"],
            "evidence_json": relative(evidence_path),
            "non_claims": [
                "not a persistent public seed",
                "not a default public-routing claim",
                "not a durability guarantee",
                "not proof of broad availability",
                "not production readiness",
            ],
        }
        write_json(result["receipt_output"], result["receipt"])
        refresh_started_project_outputs(result)
        print("- radicle genesis: completed")
        print(f"  - rid: {evidence['radicle']['rid']}")
        print(f"  - readback_commit: {evidence['radicle']['clone_commit']}")
    print("- non-claims:")
    for item in result["receipt"]["radicle_next_gate"]["non_claims"]:
        print(f"  - {item}")
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


def command_verify_bundle_cleanroom(args: argparse.Namespace) -> int:
    errors = verify_verification_bundle_cleanroom(args.bundle)
    if errors:
        for error in errors:
            print(f"cleanroom bundle verification error: {error}", file=sys.stderr)
        return 1
    print(f"valid cleanroom verification bundle: {relative(args.bundle)}")
    return 0


def command_report_bundle(args: argparse.Namespace) -> int:
    report = bundle_report(args.source)
    output = json.dumps(report, indent=2, sort_keys=True) if args.json else format_bundle_report(report)
    if args.output is None:
        print(output)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(f"{output}\n", encoding="utf-8", newline="\n")
        print(f"wrote bundle report: {relative(args.output)}")
    return 0 if report["verification"]["valid"] else 1


def command_export_bundle_release_note(args: argparse.Namespace) -> int:
    note = format_bundle_release_note(args.bundle)
    if args.output is None:
        print(note)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(f"{note}\n", encoding="utf-8", newline="\n")
        print(f"wrote bundle release note: {relative(args.output)}")
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


def command_radicle_retained_quickstart(args: argparse.Namespace) -> int:
    model = retained_radicle_quickstart_model(args.index)
    output = json.dumps(model, indent=2, sort_keys=True) if args.json else format_retained_radicle_quickstart(model)
    if args.output is None:
        print(output)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(f"{output}\n", encoding="utf-8", newline="\n")
        print(f"wrote retained Radicle quickstart: {relative(args.output)}")
    return 0


def command_verify_first_public_clone(args: argparse.Namespace) -> int:
    result = first_public_clone_plan(args)
    if not args.plan_only:
        with tempfile.TemporaryDirectory(prefix="df-first-public-clone-") as tmpdir:
            checker_output = Path(tmpdir) / "check.json"
            command = [
                *result["command"],
                "--output",
                str(checker_output),
                "--connect-timeout",
                args.connect_timeout,
                "--clone-timeout",
                args.clone_timeout,
            ]
            if args.bin_dir:
                command.extend(["--bin-dir", str(args.bin_dir)])
            if args.keep_temp:
                command.append("--keep-temp")
            completed = subprocess.run(
                command,
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            checker = json.loads(checker_output.read_text(encoding="utf-8")) if checker_output.is_file() else {}
            result.update(
                {
                    "mode": "live",
                    "live_actions_executed": True,
                    "command": command,
                    "checker_exit_code": completed.returncode,
                    "checker_stdout": completed.stdout,
                    "checker_stderr": completed.stderr,
                    "checker": checker,
                    "readback_commit": checker.get("readback_commit", ""),
                    "verification_passed": completed.returncode == 0 and checker.get("verification_passed") is True,
                }
            )
    output = json.dumps(result, indent=2, sort_keys=True) if args.json else format_first_public_clone_result(result)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(f"{json.dumps(result, indent=2, sort_keys=True)}\n", encoding="utf-8", newline="\n")
        print(f"wrote first public clone verification: {relative(args.output)}")
        if not args.json:
            print(format_first_public_clone_result(result))
    else:
        print(output)
    return 0 if result["mode"] == "plan" or result.get("verification_passed") else 1


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
        [sys.executable, "-m", "json.tool", "fixtures/onboarding-sample.registry.json"],
        [sys.executable, "-m", "json.tool", "fixtures/nostr-repo-announcement.json"],
        [sys.executable, "-m", "json.tool", "fixtures/nostr-collaboration-events.json"],
        [sys.executable, "-m", "json.tool", "fixtures/nostr-repo-state-status.json"],
        [sys.executable, "-m", "json.tool", "fixtures/live-adapter-replay-checklist.json"],
        [sys.executable, "-m", "json.tool", "fixtures/live-evidence-index.json"],
        [sys.executable, "-m", "json.tool", "fixtures/keyless-attestation.registry-verification.json"],
        [sys.executable, "-m", "py_compile", "scripts/run_radicle_fresh_readback_check.py"],
        [sys.executable, "-m", "py_compile", "scripts/run_radicle_independent_availability_check.py"],
        [sys.executable, "-m", "py_compile", "scripts/run_radicle_project_repo_smoke.py"],
        [sys.executable, "-m", "py_compile", "scripts/run_radicle_retained_delegate_check.py"],
        [sys.executable, "-m", "py_compile", "scripts/run_radicle_retained_update_check.py"],
        [sys.executable, "-m", "py_compile", "scripts/run_radicle_seed_restart_check.py"],
        [sys.executable, "-m", "py_compile", "scripts/run_radicle_update_continuity_check.py"],
        [sys.executable, "-m", "py_compile", "scripts/bootstrap_radicle_follower_seed.py"],
        [sys.executable, "-m", "py_compile", "scripts/check_public_radicle_seed.py"],
        [sys.executable, "-m", "py_compile", "scripts/refresh_radicle_follower_seed.py"],
        [sys.executable, "-m", "py_compile", "scripts/install_radicle_health_timer.py"],
        [sys.executable, "-m", "py_compile", "scripts/install_tcp_relay_user_service.py"],
        [sys.executable, "-m", "py_compile", "scripts/install_radicle_user_seed_service.py"],
        [sys.executable, "-m", "py_compile", "scripts/radicle_seed_host_control.py"],
        [sys.executable, "-m", "py_compile", "scripts/run_first_public_clone_rehearsal.py"],
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
        [sys.executable, "scripts/forge_registry.py", "radicle-retained-quickstart"],
        [sys.executable, "scripts/forge_registry.py", "verify-first-public-clone", "--plan-only", "--json"],
        [sys.executable, "scripts/forge_registry.py", "public-seed-status", "output/public-seed-status.json"],
        [
            sys.executable,
            "scripts/forge_registry.py",
            "export-nostr-draft",
            "fixtures/example-project.registry.json",
            "issue",
            "ISSUE-1",
            "--output",
            "output/demo-project.issue.issue-1.nostr-draft.json",
            "--markdown",
            "output/demo-project.issue.issue-1.nostr-draft.md",
            "--created-at",
            "2026-06-30T00:10:00Z",
        ],
        [
            sys.executable,
            "scripts/forge_registry.py",
            "export-nostr-draft",
            "fixtures/example-project.registry.json",
            "patch",
            "PATCH-1",
            "--output",
            "output/demo-project.patch.patch-1.nostr-draft.json",
            "--markdown",
            "output/demo-project.patch.patch-1.nostr-draft.md",
            "--created-at",
            "2026-06-30T00:11:00Z",
        ],
        ["node", "--check", "scripts/run_nostr_issue_patch_readback.mjs"],
        [
            "node",
            "scripts/run_nostr_issue_patch_readback.mjs",
            "--plan-only",
            "--draft",
            "output/demo-project.issue.issue-1.nostr-draft.json",
            "--draft",
            "output/demo-project.patch.patch-1.nostr-draft.json",
            "--created-at",
            "1782778800",
        ],
        [sys.executable, "scripts/forge_registry.py", "doctor", "--json"],
        [
            sys.executable,
            "scripts/forge_registry.py",
            "validate",
            "fixtures/example-project.registry.json",
            "fixtures/portable-lab.registry.json",
            "fixtures/onboarding-sample.registry.json",
        ],
        [sys.executable, "scripts/forge_registry.py", "render", "fixtures/portable-lab.registry.json", "output/portable-lab.html"],
        [sys.executable, "scripts/forge_registry.py", "render-app", "output/forge-app.html"],
        [
            sys.executable,
            "scripts/forge_registry.py",
            "render-app",
            "output/forge-app-with-onboarding-sample.html",
            "--registry",
            "fixtures/example-project.registry.json",
            "--registry",
            "fixtures/portable-lab.registry.json",
            "--registry",
            "fixtures/onboarding-sample.registry.json",
        ],
        [sys.executable, "scripts/forge_registry.py", "export-summary", "fixtures/example-project.registry.json", "output/demo-project.summary.json"],
        [sys.executable, "scripts/forge_registry.py", "export-summary", "fixtures/portable-lab.registry.json", "output/portable-lab.summary.json"],
        [sys.executable, "scripts/forge_registry.py", "export-bundle", "output/decentralized-forge-verification-bundle.zip"],
        [sys.executable, "scripts/forge_registry.py", "verify-bundle", "output/decentralized-forge-verification-bundle.zip"],
        [sys.executable, "scripts/forge_registry.py", "verify-bundle-cleanroom", "output/decentralized-forge-verification-bundle.zip"],
        [sys.executable, "scripts/forge_registry.py", "report-bundle", "output/decentralized-forge-verification-bundle.zip", "--json"],
        [
            sys.executable,
            "scripts/forge_registry.py",
            "report-bundle",
            "output/decentralized-forge-verification-bundle.zip",
            "--json",
            "--output",
            "output/onboarding-sample.bundle-report.json",
        ],
        [sys.executable, "scripts/forge_registry.py", "export-bundle-release-note", "output/decentralized-forge-verification-bundle.zip"],
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

    scaffold_registry = subparsers.add_parser("scaffold-registry", help="Create a local-only registry fixture from a Git worktree")
    scaffold_registry.add_argument("repository", type=Path, help="Local Git worktree to scaffold")
    scaffold_registry.add_argument("output", type=Path, help="Registry fixture JSON to write")
    scaffold_registry.add_argument("--project-id", help="Override the generated project id")
    scaffold_registry.add_argument("--name", help="Override the generated project name")
    scaffold_registry.add_argument("--description", help="Override the generated project description")
    scaffold_registry.set_defaults(func=command_scaffold_registry)

    attach_local_artifact = subparsers.add_parser(
        "attach-local-artifact",
        help="Attach local-only file artifact metadata to a registry fixture",
    )
    attach_local_artifact.add_argument("registry", type=Path, help="Registry fixture JSON to update in place")
    attach_local_artifact.add_argument("artifact", type=Path, help="Local artifact file to hash and reference")
    attach_local_artifact.add_argument("--version", default="0.0.0-local", help="Release version to create or update")
    attach_local_artifact.add_argument("--tag", help="Release tag; defaults to --version")
    attach_local_artifact.add_argument("--name", help="Artifact display name; defaults to the file name")
    attach_local_artifact.add_argument("--media-type", help="Override guessed media type")
    attach_local_artifact.add_argument("--timestamp", help="Override updated_at and verification timestamp")
    attach_local_artifact.set_defaults(func=command_attach_local_artifact)

    def add_collaboration_parser(name: str, kind: str, help_text: str, status_choices: list[str]) -> None:
        collab = subparsers.add_parser(name, help=help_text)
        collab.add_argument("registry", type=Path, help="Registry fixture JSON to update in place")
        collab.add_argument("--id", help=f"Record id; defaults to the next {kind}-N id")
        collab.add_argument("--title", required=True, help="Issue or patch title")
        collab.add_argument("--summary", default="", help="Short issue/patch summary")
        collab.add_argument("--author", help="Optional author display name or public id")
        collab.add_argument("--status", choices=status_choices, help="Record status; defaults to open for issues and proposed for patches")
        collab.add_argument("--timestamp", help="Override updated_at and verification timestamp")
        collab.add_argument("--summary-output", type=Path, help="Summary JSON to refresh; defaults to output/<registry-stem>.summary.json")
        collab.add_argument("--html", type=Path, help="Rendered HTML to refresh; defaults to output/<registry-stem>.html")
        collab.add_argument("--workbench", type=Path, help="Workbench HTML to refresh; defaults to output/<registry-stem>.forge-app.html")
        collab.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE_OUTPUT, help="Verification bundle to refresh")
        collab.add_argument("--report-json", type=Path, help="Optional bundle report JSON to write after refresh")
        collab.add_argument("--no-refresh", action="store_true", help="Only update the registry; skip summary/page/workbench/bundle refresh")
        collab.set_defaults(func=command_add_collaboration_record, kind=kind)

    add_collaboration_parser(
        "add-issue",
        "issue",
        "Add or update a local issue record in a registry fixture",
        ["open", "closed"],
    )
    add_collaboration_parser(
        "add-patch",
        "patch",
        "Add or update a local patch/PR-like record in a registry fixture",
        ["proposed", "review", "accepted", "rejected", "merged"],
    )

    nostr_draft = subparsers.add_parser(
        "export-nostr-draft",
        help="Export a registry issue or patch as an unsigned NIP-34-shaped draft",
    )
    nostr_draft.add_argument("registry", type=Path, help="Registry fixture JSON to read")
    nostr_draft.add_argument("kind", choices=["issue", "patch"], help="Collaboration record type")
    nostr_draft.add_argument("record_id", help="Issue or patch id to export")
    nostr_draft.add_argument("--output", type=Path, help="Draft JSON path; defaults to output/<project>.<kind>.<id>.nostr-draft.json")
    nostr_draft.add_argument("--markdown", type=Path, help="Markdown handoff path; defaults beside the draft JSON")
    nostr_draft.add_argument("--pubkey", default="0" * 64, help="Draft pubkey; defaults to an obvious placeholder key")
    nostr_draft.add_argument("--created-at", help="Draft created_at as Unix seconds or ISO-8601; defaults to current time")
    nostr_draft.add_argument("--relay", action="append", default=[], help="Relay hint to include; may be repeated")
    nostr_draft.set_defaults(func=command_export_nostr_draft)

    onboard = subparsers.add_parser(
        "onboard-local-project",
        help="Scaffold, attach a local artifact, validate, render, and refresh bundle/report outputs",
    )
    onboard.add_argument("repository", type=Path, help="Local Git worktree to onboard")
    onboard.add_argument("artifact", type=Path, help="Local artifact file to hash and reference")
    onboard.add_argument("--registry", type=Path, help="Registry fixture JSON to write; defaults to fixtures/<project-id>.registry.json")
    onboard.add_argument("--summary", type=Path, help="Summary JSON to write; defaults to output/<registry-stem>.summary.json")
    onboard.add_argument("--html", type=Path, help="Rendered HTML to write; defaults to output/<registry-stem>.html")
    onboard.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE_OUTPUT, help="Verification bundle to refresh")
    onboard.add_argument("--report-json", type=Path, help="Optional bundle report JSON to write after refresh")
    onboard.add_argument("--project-id", help="Override the generated project id")
    onboard.add_argument("--project-name", help="Override the generated project name")
    onboard.add_argument("--description", help="Override the generated project description")
    onboard.add_argument("--version", default="0.0.0-local", help="Release version to create or update")
    onboard.add_argument("--tag", help="Release tag; defaults to --version")
    onboard.add_argument("--artifact-name", help="Artifact display name; defaults to the file name")
    onboard.add_argument("--media-type", help="Override guessed media type")
    onboard.add_argument("--timestamp", help="Override artifact verification timestamp")
    onboard.set_defaults(func=command_onboard_local_project)

    start_project_parser = subparsers.add_parser(
        "start-project",
        help="Start a project on the local forge surface with registry, artifact metadata, page, workbench, receipt, and bundle",
    )
    start_project_parser.add_argument("repository", type=Path, help="Local Git worktree to start on the forge")
    start_project_parser.add_argument("--artifact", type=Path, help="Local artifact file to hash and reference; defaults to repository README.md")
    start_project_parser.add_argument("--registry", type=Path, help="Registry fixture JSON to write; defaults to fixtures/<project-id>.registry.json")
    start_project_parser.add_argument("--summary", type=Path, help="Summary JSON to write; defaults to output/<registry-stem>.summary.json")
    start_project_parser.add_argument("--html", type=Path, help="Rendered HTML to write; defaults to output/<registry-stem>.html")
    start_project_parser.add_argument("--workbench", type=Path, help="Workbench HTML to write; defaults to output/<registry-stem>.forge-app.html")
    start_project_parser.add_argument("--receipt", type=Path, help="Start-project receipt JSON to write; defaults to output/<registry-stem>.start-project.json")
    start_project_parser.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE_OUTPUT, help="Verification bundle to refresh")
    start_project_parser.add_argument("--report-json", type=Path, help="Optional bundle report JSON to write after refresh")
    start_project_parser.add_argument("--project-id", help="Override the generated project id")
    start_project_parser.add_argument("--project-name", help="Override the generated project name")
    start_project_parser.add_argument("--description", help="Override the generated project description")
    start_project_parser.add_argument("--version", default="0.1.0-local", help="Release version to create or update")
    start_project_parser.add_argument("--tag", help="Release tag; defaults to --version")
    start_project_parser.add_argument("--artifact-name", help="Artifact display name; defaults to the file name")
    start_project_parser.add_argument("--media-type", help="Override guessed media type")
    start_project_parser.add_argument("--timestamp", help="Override artifact verification timestamp")
    start_project_parser.add_argument("--radicle-evidence", type=Path, help="Radicle genesis evidence JSON path for the emitted or executed next gate")
    start_project_parser.add_argument("--radicle-markdown", type=Path, help="Radicle genesis Markdown evidence path for the emitted or executed next gate")
    start_project_parser.add_argument("--run-radicle-genesis", action="store_true", help="Run the emitted bounded Radicle genesis gate after start-project")
    start_project_parser.set_defaults(func=command_start_project)

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

    verify_bundle_cleanroom = subparsers.add_parser(
        "verify-bundle-cleanroom",
        help="Extract a portable verification bundle into a temporary clean-room tree and run bundled checks",
    )
    verify_bundle_cleanroom.add_argument("bundle", type=Path, nargs="?", default=DEFAULT_BUNDLE_OUTPUT)
    verify_bundle_cleanroom.set_defaults(func=command_verify_bundle_cleanroom)

    report_bundle = subparsers.add_parser("report-bundle", help="Summarize a portable bundle ZIP or extracted bundle directory")
    report_bundle.add_argument("source", type=Path, nargs="?", default=DEFAULT_BUNDLE_OUTPUT)
    report_bundle.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    report_bundle.add_argument("--output", type=Path, help="Write the report to a file instead of stdout")
    report_bundle.set_defaults(func=command_report_bundle)

    export_bundle_release_note = subparsers.add_parser(
        "export-bundle-release-note",
        help="Emit a release-facing markdown note for a portable verification bundle",
    )
    export_bundle_release_note.add_argument("bundle", type=Path, nargs="?", default=DEFAULT_BUNDLE_OUTPUT)
    export_bundle_release_note.add_argument("output", type=Path, nargs="?", default=None)
    export_bundle_release_note.set_defaults(func=command_export_bundle_release_note)

    evidence_index = subparsers.add_parser("validate-evidence-index", help="Validate live evidence index paths, hashes, and claim boundaries")
    evidence_index.add_argument("index", type=Path, nargs="?", default=DEFAULT_LIVE_EVIDENCE_INDEX)
    evidence_index.set_defaults(func=command_validate_evidence_index)

    refresh_hashes = subparsers.add_parser("refresh-evidence-hashes", help="Add or check evidence file SHA-256 and size metadata")
    refresh_hashes.add_argument("index", type=Path, nargs="?", default=DEFAULT_LIVE_EVIDENCE_INDEX)
    refresh_hashes.add_argument("--check", action="store_true", help="Fail if committed hash metadata is stale")
    refresh_hashes.set_defaults(func=command_refresh_evidence_hashes)

    radicle_retained = subparsers.add_parser(
        "radicle-retained-quickstart",
        help="Print the evidence-bounded retained Radicle direct-seed clone recipe",
    )
    radicle_retained.add_argument("output", type=Path, nargs="?", default=None, help="Optional file to write")
    radicle_retained.add_argument("--index", type=Path, default=DEFAULT_LIVE_EVIDENCE_INDEX, help="Live evidence index to read")
    radicle_retained.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    radicle_retained.set_defaults(func=command_radicle_retained_quickstart)

    first_public_clone = subparsers.add_parser(
        "verify-first-public-clone",
        help="Verify or plan the current retained RID public direct-seed clone path",
    )
    first_public_clone.add_argument("--index", type=Path, default=DEFAULT_LIVE_EVIDENCE_INDEX, help="Live evidence index to read")
    first_public_clone.add_argument("--seed", choices=["primary", "second"], default="primary", help="Public seed path to verify")
    first_public_clone.add_argument("--plan-only", action="store_true", help="Print the bounded verification plan without running Radicle")
    first_public_clone.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    first_public_clone.add_argument("--output", type=Path, help="Write machine-readable result JSON")
    first_public_clone.add_argument("--bin-dir", type=Path, help="Directory containing rad/radicle-node")
    first_public_clone.add_argument("--keep-temp", action="store_true", help="Preserve checker temporary state in live mode")
    first_public_clone.add_argument("--connect-timeout", default="30s")
    first_public_clone.add_argument("--clone-timeout", default="180s")
    first_public_clone.set_defaults(func=command_verify_first_public_clone)

    public_seed_status = subparsers.add_parser(
        "public-seed-status",
        help="Emit current public seed status from committed first-public-clone evidence",
    )
    public_seed_status.add_argument("output", type=Path, nargs="?", default=None, help="Optional JSON file to write")
    public_seed_status.add_argument("--index", type=Path, default=DEFAULT_LIVE_EVIDENCE_INDEX, help="Live evidence index to read")
    public_seed_status.set_defaults(func=command_public_seed_status)

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
