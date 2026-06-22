#!/usr/bin/env python3
"""Render a decentralized-forge project registry to a static HTML page.

Stdlib only by design.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

REQUIRED_TOP_LEVEL = [
    "schema_version",
    "project",
    "maintainers",
    "clone_urls",
    "created_at",
    "updated_at",
]
REQUIRED_PROJECT = ["id", "name", "description", "default_branch"]
EXPECTED_SCHEMA_VERSION = "decentralized-forge.project-registry.v1"


class RegistryError(ValueError):
    """Raised when a registry fixture is invalid for the MVP renderer."""


def load_registry(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RegistryError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise RegistryError("registry root must be an object")
    validate_registry(data)
    return data


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RegistryError(message)


def validate_registry(data: dict) -> None:
    for key in REQUIRED_TOP_LEVEL:
        require(key in data, f"missing required top-level field: {key}")
    require(data["schema_version"] == EXPECTED_SCHEMA_VERSION, "unsupported schema_version")
    require(isinstance(data["project"], dict), "project must be an object")
    for key in REQUIRED_PROJECT:
        require(key in data["project"], f"missing required project field: {key}")
        require(bool(data["project"][key]), f"project.{key} must not be empty")
    require(bool(isinstance(data["maintainers"], list) and data["maintainers"]), "maintainers must be a non-empty array")
    for maintainer in data["maintainers"]:
        require(isinstance(maintainer, dict), "maintainer entries must be objects")
        require(maintainer.get("id_type") in {"nostr", "radicle", "did", "ssh", "other"}, "maintainer id_type is invalid")
        require(bool(maintainer.get("public_id")), "maintainer public_id is required")
        require(bool(maintainer.get("name")), "maintainer name is required")
    require(bool(isinstance(data["clone_urls"], list) and data["clone_urls"]), "clone_urls must be a non-empty array")
    for clone in data["clone_urls"]:
        require(isinstance(clone, dict), "clone URL entries must be objects")
        require(clone.get("transport") in {"git", "https", "ssh", "radicle", "nostr", "other"}, "clone transport is invalid")
        require(bool(clone.get("url")), "clone url is required")


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def list_items(items: list[str]) -> str:
    if not items:
        return "<p><em>None listed.</em></p>"
    return "<ul>\n" + "\n".join(f"  <li>{item}</li>" for item in items) + "\n</ul>"


def render_registry(data: dict) -> str:
    project = data["project"]
    maintainer_items = [
        f"<strong>{esc(m['name'])}</strong> — {esc(m['id_type'])}: <code>{esc(m['public_id'])}</code> ({esc(m.get('role', 'maintainer'))})"
        for m in data.get("maintainers", [])
    ]
    clone_items = [
        f"<strong>{esc(c['transport'])}</strong>: <code>{esc(c['url'])}</code>{' <em>primary</em>' if c.get('primary') else ''}"
        for c in data.get("clone_urls", [])
    ]
    issue_items = [
        f"<strong>{esc(i.get('id', 'issue'))}</strong> [{esc(i.get('status', 'unknown'))}] {esc(i.get('title', 'Untitled'))}<br>{esc(i.get('summary', ''))}"
        for i in data.get("issues", [])
    ]
    patch_items = [
        f"<strong>{esc(p.get('id', 'patch'))}</strong> [{esc(p.get('status', 'unknown'))}] {esc(p.get('title', 'Untitled'))}<br>{esc(p.get('summary', ''))}"
        for p in data.get("patches", [])
    ]
    release_items = []
    for release in data.get("releases", []):
        artifacts = []
        for artifact in release.get("artifacts", []):
            artifacts.append(
                f"{esc(artifact.get('name', 'artifact'))}: <code>{esc(artifact.get('sha256', ''))}</code>"
                + (f" CID <code>{esc(artifact.get('cid'))}</code>" if artifact.get("cid") else "")
                + (f" signature <code>{esc(artifact.get('signature'))}</code>" if artifact.get("signature") else "")
            )
        release_items.append(
            f"<strong>{esc(release.get('version', 'release'))}</strong> tag <code>{esc(release.get('tag', ''))}</code>"
            + list_items(artifacts)
        )
    substrate_items = []
    for name, value in sorted(data.get("substrates", {}).items()):
        substrate_items.append(f"<strong>{esc(name)}</strong>: <code>{esc(json.dumps(value, sort_keys=True))}</code>")

    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <title>{esc(project['name'])}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 900px; margin: 2rem auto; line-height: 1.5; padding: 0 1rem; }}
    code {{ background: #f4f4f4; padding: 0.1rem 0.25rem; }}
    section {{ border-top: 1px solid #ddd; margin-top: 1.5rem; padding-top: 1rem; }}
  </style>
</head>
<body>
  <h1>{esc(project['name'])}</h1>
  <p>{esc(project['description'])}</p>
  <p><strong>Project ID:</strong> <code>{esc(project['id'])}</code><br>
     <strong>Default branch:</strong> <code>{esc(project['default_branch'])}</code><br>
     <strong>Registry updated:</strong> <code>{esc(data['updated_at'])}</code></p>

  <section><h2>Maintainers</h2>{list_items(maintainer_items)}</section>
  <section><h2>Clone URLs</h2>{list_items(clone_items)}</section>
  <section><h2>Issues</h2>{list_items(issue_items)}</section>
  <section><h2>Patches / PRs</h2>{list_items(patch_items)}</section>
  <section><h2>Releases</h2>{list_items(release_items)}</section>
  <section><h2>Protocol / substrate hints</h2>{list_items(substrate_items)}</section>
  <section><h2>Signature status</h2><p><code>{esc(json.dumps(data.get('signature', {}), sort_keys=True))}</code></p></section>
</body>
</html>
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", type=Path, help="Input project registry JSON")
    parser.add_argument("output", type=Path, help="Output HTML path")
    args = parser.parse_args(argv)
    try:
        data = load_registry(args.registry)
        rendered = render_registry(data)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    except RegistryError as exc:
        print(f"registry error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
