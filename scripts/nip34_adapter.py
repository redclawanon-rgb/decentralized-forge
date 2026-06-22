#!/usr/bin/env python3
"""Stdlib-only helpers for local NIP-34 fixture parsing.

This module intentionally parses existing dry-run fixtures only. It does not
sign events, replace fixture event ids, publish to relays, or verify relay state.
Loop 14 can compute local possible event-id references for conformance metadata
only; fixture ids/signatures remain dry-run placeholders.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

REPOSITORY_KIND = 30617
REPOSITORY_STATE_KIND = 30618
ISSUE_KIND = 1621
PATCH_KIND = 1617

LOWER_HEX_64_RE = re.compile(r"^[0-9a-f]{64}$")
SYNTHETIC_REPEATED_DIGIT_KEY_RE = re.compile(r"^([0-9])\1{63}$")


def is_lower_hex_pubkey(value: Any) -> bool:
    """Return whether *value* is a NIP-01-shaped 64-char lowercase hex pubkey."""
    return isinstance(value, str) and bool(LOWER_HEX_64_RE.fullmatch(value))


def is_fixture_synthetic_pubkey(value: Any) -> bool:
    """Return whether *value* is one of this project's obvious fixture keys."""
    return isinstance(value, str) and bool(SYNTHETIC_REPEATED_DIGIT_KEY_RE.fullmatch(value))


def validate_nip01_event_shape(event: dict[str, Any]) -> dict[str, Any]:
    """Validate local NIP-01 event shape without requiring real id/sig.

    Dry-run fixtures intentionally keep placeholder ids and signatures. This
    helper checks the fields needed to describe NIP-01/NIP-34 fixture shape and
    reports validation errors instead of signing, publishing, or mutating input.
    """
    errors: list[str] = []
    for field in ["pubkey", "created_at", "kind", "tags", "content"]:
        if field not in event:
            errors.append(f"missing required field: {field}")

    pubkey = event.get("pubkey")
    pubkey_is_lower_hex = is_lower_hex_pubkey(pubkey)
    pubkey_is_fixture_synthetic = is_fixture_synthetic_pubkey(pubkey)
    if "pubkey" in event and not (pubkey_is_lower_hex or pubkey_is_fixture_synthetic):
        errors.append("pubkey must be 64 lowercase hex or an obvious repeated-digit fixture key")

    created_at_is_int = type(event.get("created_at")) is int
    kind_is_int = type(event.get("kind")) is int

    if "created_at" in event and not created_at_is_int:
        errors.append("created_at must be an int")
    if "kind" in event and not kind_is_int:
        errors.append("kind must be an int")
    if "content" in event and not isinstance(event.get("content"), str):
        errors.append("content must be a string")

    tags = event.get("tags")
    tags_valid = isinstance(tags, list)
    if "tags" in event and not tags_valid:
        errors.append("tags must be a list")
    if isinstance(tags, list):
        for index, tag in enumerate(tags):
            if not isinstance(tag, list):
                errors.append(f"tags[{index}] must be a list")
                tags_valid = False
                continue
            if not all(isinstance(item, str) for item in tag):
                errors.append(f"tags[{index}] values must be strings")
                tags_valid = False

    required_shape_valid = not errors
    return {
        "required_fields_present": all(field in event for field in ["pubkey", "created_at", "kind", "tags", "content"]),
        "pubkey_is_lower_hex_64": pubkey_is_lower_hex,
        "pubkey_is_fixture_synthetic": pubkey_is_fixture_synthetic,
        "created_at_is_int": created_at_is_int,
        "kind_is_int": kind_is_int,
        "tags_are_arrays_of_strings": tags_valid,
        "content_is_string": isinstance(event.get("content"), str),
        "valid_for_local_fixture": required_shape_valid,
        "errors": errors,
    }


def nip01_serialized_event_payload(event: dict[str, Any]) -> str:
    """Return compact UTF-8 JSON serialization for NIP-01 event id input."""
    shape = validate_nip01_event_shape(event)
    if not shape["valid_for_local_fixture"] or not shape["pubkey_is_lower_hex_64"]:
        raise ValueError("event is not eligible for NIP-01 serialized id payload")
    payload = [
        0,
        event["pubkey"],
        event["created_at"],
        event["kind"],
        event["tags"],
        event["content"],
    ]
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def possible_event_id(event: dict[str, Any]) -> str | None:
    """Return local reference sha256 event id when fixture shape permits it."""
    try:
        serialized = nip01_serialized_event_payload(event)
    except ValueError:
        return None
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def conformance_report(event: dict[str, Any], *, label: str = "") -> dict[str, Any]:
    """Describe dry-run NIP-01/NIP-34 conformance metadata for one fixture event."""
    shape = validate_nip01_event_shape(event)
    serialized_payload = None
    computed_reference = None
    if shape["valid_for_local_fixture"] and shape["pubkey_is_lower_hex_64"]:
        serialized_payload = nip01_serialized_event_payload(event)
        computed_reference = hashlib.sha256(serialized_payload.encode("utf-8")).hexdigest()
    event_id = event.get("id", "")
    sig = event.get("sig", "")
    return {
        "label": label or event.get("fixture_name", ""),
        "kind": event.get("kind"),
        "nip34_kind_known": event.get("kind") in {REPOSITORY_KIND, REPOSITORY_STATE_KIND, ISSUE_KIND, PATCH_KIND},
        "shape": shape,
        "id_is_placeholder": isinstance(event_id, str) and event_id.startswith("dry-run-"),
        "sig_is_placeholder": isinstance(sig, str) and sig.startswith("dry-run-"),
        "event_id_computed": False,
        "signed": False,
        "published": False,
        "serialized_event_payload": serialized_payload,
        "possible_event_id": computed_reference,
    }


def load_json(path: str | Path) -> dict[str, Any]:
    """Load a JSON object from *path*."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object in {path}")
    return data


def tags_by_name(event: dict[str, Any]) -> dict[str, list[list[str]]]:
    """Group Nostr event tags by their first element.

    The fixture uses simple string tags. This helper validates enough shape for
    conformance tests while staying intentionally small and dependency-free.
    """
    grouped: dict[str, list[list[str]]] = {}
    tags = event.get("tags")
    if not isinstance(tags, list):
        raise ValueError("event tags must be a list")
    for tag in tags:
        if not isinstance(tag, list) or len(tag) < 2:
            raise ValueError(f"invalid NIP-34 tag shape: {tag!r}")
        name = tag[0]
        if not isinstance(name, str):
            raise ValueError(f"invalid NIP-34 tag name: {tag!r}")
        if not all(isinstance(item, str) for item in tag):
            raise ValueError(f"fixture tag values must be strings: {tag!r}")
        grouped.setdefault(name, []).append(tag)
    return grouped


def _single_value(tags: dict[str, list[list[str]]], name: str, *, required: bool = True) -> str | None:
    values = tags.get(name, [])
    if not values:
        if required:
            raise ValueError(f"missing required tag: {name}")
        return None
    return values[0][1]


def _clone_transport(url: str) -> str:
    if url.startswith("file://"):
        return "git"
    if url.startswith("nostr://"):
        return "nostr"
    if url.startswith("rad:"):
        return "radicle"
    if url.startswith("ssh://") or url.startswith("git@"):
        return "ssh"
    if url.startswith("https://"):
        return "https"
    if url.startswith("git://"):
        return "git"
    return "other"


def parse_repository_announcement(event: dict[str, Any]) -> dict[str, Any]:
    """Map a NIP-34 repository announcement fixture to registry concepts."""
    if event.get("kind") != REPOSITORY_KIND:
        raise ValueError(f"expected NIP-34 repository kind {REPOSITORY_KIND}")

    tags = tags_by_name(event)
    repo_id = _single_value(tags, "d")
    name = _single_value(tags, "name")
    description = _single_value(tags, "description", required=False) or ""
    web_urls = [tag[1] for tag in tags.get("web", [])]
    clone_urls = [
        {"transport": _clone_transport(tag[1]), "url": tag[1]}
        for tag in tags.get("clone", [])
    ]
    maintainers = [
        {"id_type": "nostr", "public_id": tag[1], "role": "maintainer"}
        for tag in tags.get("maintainers", [])
    ]
    relay_hints = [tag[1] for tag in tags.get("relays", [])]
    topics = [tag[1] for tag in tags.get("t", [])]

    return {
        "project": {
            "id": repo_id,
            "name": name,
            "description": description,
            "web_urls": web_urls,
        },
        "clone_urls": clone_urls,
        "maintainers": maintainers,
        "substrates": {
            "nip34": {
                "repository_kind": REPOSITORY_KIND,
                "repo_id_tag": repo_id,
                "relay_hints": relay_hints,
                "publish_status": "dry-run-only",
                "topics": topics,
            }
        },
        "dry_run": {
            "repository": {
                "notice": event.get("dry_run_notice", ""),
                "id": event.get("id", ""),
                "sig": event.get("sig", ""),
                "pubkey": event.get("pubkey", ""),
                "published": False,
            }
        },
    }


def _content_summary(content: str, *, kind: int | None = None) -> str:
    """Return the registry summary represented by event content.

    Issue fixtures use the first Markdown paragraph. Patch fixtures are shaped
    like `git format-patch`, so the summary is the first paragraph after the
    mail-style headers and blank separator.
    """
    paragraphs = [part.strip() for part in content.split("\n\n") if part.strip()]
    if not paragraphs:
        return ""
    if kind == PATCH_KIND and paragraphs[0].startswith("From ") and len(paragraphs) > 1:
        return paragraphs[1]
    return paragraphs[0]


def parse_collaboration_event(event: dict[str, Any], repo_address: str) -> tuple[str, dict[str, Any]]:
    """Map one NIP-34 issue/patch fixture event to a registry concept."""
    kind = event.get("kind")
    if kind not in {ISSUE_KIND, PATCH_KIND}:
        raise ValueError(f"unsupported collaboration event kind: {kind!r}")

    tags = tags_by_name(event)
    linked_repos = [tag[1] for tag in tags.get("a", [])]
    if repo_address not in linked_repos:
        raise ValueError(f"event does not reference repository address {repo_address!r}")

    content = event.get("content", "")
    if not isinstance(content, str):
        raise ValueError("event content must be a string")

    item = {
        "id": event.get("id", ""),
        "title": _single_value(tags, "subject") or "",
        "status": _single_value(tags, "status", required=False) or "unknown",
        "author": event.get("pubkey", ""),
        "summary": _content_summary(content, kind=kind),
        "content": content,
        "repository": repo_address,
        "source_event_kind": kind,
        "source_fixture_name": event.get("fixture_name", ""),
        "mapped_registry_path": event.get("mapped_registry_path", ""),
    }
    return ("issues" if kind == ISSUE_KIND else "patches", item)


def parse_collaboration_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    """Parse the local collaboration-events fixture."""
    repo_address = fixture.get("repo_address")
    if not isinstance(repo_address, str) or not repo_address:
        raise ValueError("collaboration fixture requires repo_address")

    issues: list[dict[str, Any]] = []
    patches: list[dict[str, Any]] = []
    dry_run_events: list[dict[str, Any]] = []

    events = fixture.get("events")
    if not isinstance(events, list):
        raise ValueError("collaboration fixture events must be a list")

    for event in events:
        if not isinstance(event, dict):
            raise ValueError("collaboration events must be objects")
        collection, item = parse_collaboration_event(event, repo_address)
        if collection == "issues":
            issues.append(item)
        else:
            patches.append(item)
        dry_run_events.append(
            {
                "kind": event.get("kind"),
                "id": event.get("id", ""),
                "sig": event.get("sig", ""),
                "pubkey": event.get("pubkey", ""),
                "published": False,
            }
        )

    return {
        "issues": issues,
        "patches": patches,
        "dry_run": {
            "collaboration": {
                "notice": fixture.get("dry_run_notice", ""),
                "relay_tool_check": fixture.get("relay_tool_check", {}),
                "synthetic_key_policy": fixture.get("synthetic_key_policy", {}),
                "nip35_boundary": fixture.get("nip35_boundary", {}),
            },
            "events": dry_run_events,
        },
    }


def parse_repository_state_event(event: dict[str, Any], repo_address: str | None = None) -> dict[str, Any]:
    """Map a local NIP-34 repository state fixture to registry concepts.

    This accepts only the dry-run fixture shape. It records refs and the HEAD
    symbolic ref but does not verify relay state, sign anything, or infer live
    NIP behavior beyond the tag values present in the JSON file.
    """
    if event.get("kind") != REPOSITORY_STATE_KIND:
        raise ValueError(f"expected NIP-34 repository state kind {REPOSITORY_STATE_KIND}")

    tags = tags_by_name(event)
    repo_id = _single_value(tags, "d")
    linked_repos = [tag[1] for tag in tags.get("a", [])]
    if repo_address and linked_repos and repo_address not in linked_repos:
        raise ValueError(f"state event does not reference repository address {repo_address!r}")

    refs: dict[str, str] = {}
    for tag_name, tag_values in tags.items():
        if tag_name.startswith("refs/"):
            refs[tag_name] = tag_values[0][1]

    head = _single_value(tags, "HEAD", required=False) or ""
    head_ref = head.removeprefix("ref: ") if head.startswith("ref: ") else head
    head_commit = refs.get(head_ref, "") if head_ref else ""

    return {
        "kind": REPOSITORY_STATE_KIND,
        "repo_id_tag": repo_id,
        "repository_address": linked_repos[0] if linked_repos else repo_address or "",
        "head": head,
        "head_ref": head_ref,
        "head_commit": head_commit,
        "refs": refs,
        "fixture_name": event.get("fixture_name", ""),
    }


def parse_state_status_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    """Parse the local repository state/status dry-run fixture."""
    state_event = fixture.get("repository_state_event")
    if not isinstance(state_event, dict):
        raise ValueError("state/status fixture requires repository_state_event")
    repo_address = fixture.get("repo_address")
    if repo_address is not None and not isinstance(repo_address, str):
        raise ValueError("repo_address must be a string when present")

    state = parse_repository_state_event(state_event, repo_address)
    source_git_head = fixture.get("source_git_head", "")
    if source_git_head and state["head_commit"] and source_git_head != state["head_commit"]:
        raise ValueError("source_git_head does not match repository state HEAD commit")

    checks = fixture.get("status_checks", [])
    if not isinstance(checks, list):
        raise ValueError("status_checks must be a list")
    parsed_checks: list[dict[str, Any]] = []
    for check in checks:
        if not isinstance(check, dict):
            raise ValueError("status check entries must be objects")
        target_commit = check.get("target_commit", "")
        target_ref = check.get("target_ref", "")
        if target_commit and state["head_commit"] and target_commit != state["head_commit"]:
            raise ValueError("status check target_commit does not match repository state HEAD commit")
        if target_ref and state["head_ref"] and target_ref != state["head_ref"]:
            raise ValueError("status check target_ref does not match repository state HEAD ref")
        parsed_checks.append(
            {
                "fixture_name": check.get("fixture_name", ""),
                "mapped_registry_path": check.get("mapped_registry_path", ""),
                "source_ci_check_id": check.get("source_ci_check_id", ""),
                "target_type": check.get("target_type", ""),
                "target_commit": target_commit,
                "target_ref": target_ref,
                "name": check.get("name", ""),
                "provider": check.get("provider", ""),
                "status": check.get("status", ""),
                "conclusion": check.get("conclusion", ""),
                "synthetic": bool(check.get("synthetic", False)),
                "published": bool(check.get("published", False)),
                "notes": check.get("notes", ""),
            }
        )

    return {
        "repository_state": state,
        "status_checks": parsed_checks,
        "dry_run": {
            "state_status": {
                "notice": fixture.get("dry_run_notice", ""),
                "source_git_head": source_git_head,
                "non_claims": fixture.get("non_claims", {}),
            },
            "repository_state_event": {
                "kind": state_event.get("kind"),
                "id": state_event.get("id", ""),
                "sig": state_event.get("sig", ""),
                "pubkey": state_event.get("pubkey", ""),
                "published": False,
            },
        },
    }


def export_fixture_pair(
    repo_event: dict[str, Any],
    collaboration_fixture: dict[str, Any],
    state_status_fixture: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Round-trip local NIP-34 fixtures back to registry-shaped concepts."""
    repo = parse_repository_announcement(repo_event)
    collaboration = parse_collaboration_fixture(collaboration_fixture)
    state_status = parse_state_status_fixture(state_status_fixture) if state_status_fixture else None

    exported = {
        "project": repo["project"],
        "maintainers": repo["maintainers"],
        "clone_urls": repo["clone_urls"],
        "issues": collaboration["issues"],
        "patches": collaboration["patches"],
        "substrates": repo["substrates"],
        "dry_run": {
            "repository": repo["dry_run"]["repository"],
            "collaboration": collaboration["dry_run"]["collaboration"],
            "events": collaboration["dry_run"]["events"],
            "conformance": {
                "scope": "local-dry-run-fixtures-only",
                "source": "NIP-01/NIP-34 source-inspected 2026-06-22; no signing, publishing, or fixture id replacement",
                "reports": [
                    conformance_report(repo_event, label="repository_announcement"),
                    *[
                        conformance_report(event, label=event.get("fixture_name", f"collaboration_event_{index}"))
                        for index, event in enumerate(collaboration_fixture.get("events", []))
                        if isinstance(event, dict)
                    ],
                ],
            },
        },
    }
    if state_status:
        assert state_status_fixture is not None
        exported["repository_state"] = state_status["repository_state"]
        exported["status_checks"] = state_status["status_checks"]
        exported["dry_run"]["state_status"] = state_status["dry_run"]["state_status"]
        exported["dry_run"]["repository_state_event"] = state_status["dry_run"]["repository_state_event"]
        exported["dry_run"]["conformance"]["reports"].append(
            conformance_report(state_status_fixture["repository_state_event"], label="repository_state_event")
        )
    return exported


def main(argv: list[str]) -> int:
    if len(argv) not in {3, 4}:
        print(
            "usage: nip34_adapter.py fixtures/nostr-repo-announcement.json "
            "fixtures/nostr-collaboration-events.json [fixtures/nostr-repo-state-status.json]",
            file=sys.stderr,
        )
        return 2
    state_status = load_json(argv[3]) if len(argv) == 4 else None
    exported = export_fixture_pair(load_json(argv[1]), load_json(argv[2]), state_status)
    print(json.dumps(exported, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
