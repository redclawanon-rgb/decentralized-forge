#!/usr/bin/env python3
"""Stdlib-only helpers for local NIP-34 fixture parsing.

This module intentionally parses existing dry-run fixtures only. It does not
sign events, compute Nostr event ids, publish to relays, or verify relay state.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REPOSITORY_KIND = 30617
ISSUE_KIND = 1621
PATCH_KIND = 1617


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


def export_fixture_pair(repo_event: dict[str, Any], collaboration_fixture: dict[str, Any]) -> dict[str, Any]:
    """Round-trip local NIP-34 fixtures back to registry-shaped concepts."""
    repo = parse_repository_announcement(repo_event)
    collaboration = parse_collaboration_fixture(collaboration_fixture)

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
        },
    }
    return exported


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "usage: nip34_adapter.py fixtures/nostr-repo-announcement.json "
            "fixtures/nostr-collaboration-events.json",
            file=sys.stderr,
        )
        return 2
    exported = export_fixture_pair(load_json(argv[1]), load_json(argv[2]))
    print(json.dumps(exported, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
