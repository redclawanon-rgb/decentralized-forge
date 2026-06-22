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


def yes_no(value: object) -> str:
    """Render an explicit boolean-ish flag without implying verification."""
    if value is True:
        return '<span class="flag yes">yes</span>'
    if value is False:
        return '<span class="flag no">no</span>'
    if value is None:
        return '<span class="flag unknown">not listed</span>'
    return f'<span class="flag unknown">{esc(value)}</span>'


def field(label: str, value: object, code: bool = True) -> str:
    if value is None or value == "":
        value_html = "<em>not listed</em>"
    elif code:
        value_html = f"<code>{esc(value)}</code>"
    else:
        value_html = esc(value)
    return f"<dt>{esc(label)}</dt><dd>{value_html}</dd>"


def render_artifact(artifact: dict) -> str:
    availability = artifact.get("availability", {})
    content_address_items = []
    for address in artifact.get("content_addresses", []):
        content_address_items.append(
            "<dl class=\"metadata\">"
            + field("Protocol", address.get("protocol"))
            + field("CID", address.get("cid"))
            + field("CID version", address.get("cid_version"))
            + field("Multibase", address.get("multibase"))
            + field("Multicodec", address.get("multicodec"))
            + field("Multihash", address.get("multihash"))
            + f"<dt>Derived from local fixture</dt><dd>{yes_no(address.get('derived_from_local_fixture'))}</dd>"
            + f"<dt>Matches artifact hash</dt><dd>{yes_no(address.get('matches_artifact_hash'))}</dd>"
            + field("Verification status", address.get("verification_status"))
            + field("Notes", address.get("notes"), code=False)
            + "</dl>"
        )

    provenance = artifact.get("provenance", {})
    verification = provenance.get("verification", {}) if isinstance(provenance, dict) else {}
    provenance_items = []
    if provenance:
        provenance_items.append(
            "<dl class=\"metadata\">"
            + field("Status", provenance.get("status"))
            + field("Builder", provenance.get("builder"))
            + field("Repository", provenance.get("repository"))
            + field("Commit", provenance.get("commit"))
            + field("Tag", provenance.get("tag"))
            + field("Predicate type", provenance.get("predicate_type"))
            + f"<dt>Synthetic fixture</dt><dd>{yes_no(provenance.get('synthetic'))}</dd>"
            + f"<dt>Local schema only</dt><dd>{yes_no(verification.get('local_schema_only'))}</dd>"
            + f"<dt>Real Sigstore verified</dt><dd>{yes_no(verification.get('real_sigstore_verified'))}</dd>"
            + f"<dt>Real in-toto verified</dt><dd>{yes_no(verification.get('real_in_toto_verified'))}</dd>"
            + f"<dt>No SLSA level claimed</dt><dd>{yes_no(not verification.get('slsa_level_claimed', False))}</dd>"
            + f"<dt>Uses private key</dt><dd>{yes_no(verification.get('uses_private_key'))}</dd>"
            + field("CI check IDs", ", ".join(provenance.get("ci_check_ids", [])))
            + field("Boundaries", ", ".join(provenance.get("boundaries", [])), code=False)
            + field("Verification notes", verification.get("notes"), code=False)
            + "</dl>"
        )

    return (
        '<article class="artifact">'
        f"<h4>{esc(artifact.get('name', 'artifact'))}</h4>"
        + '<dl class="metadata">'
        + field("Media type", artifact.get("media_type"))
        + field("Size bytes", artifact.get("size_bytes"))
        + field("URI", artifact.get("uri"))
        + field("SHA-256", artifact.get("sha256"))
        + field("CID", artifact.get("cid"))
        + field("Signature", artifact.get("signature"))
        + "</dl>"
        + "<h5>Artifact availability</h5>"
        + '<dl class="metadata">'
        + f"<dt>Local fixture available</dt><dd>{yes_no(availability.get('local_fixture'))}</dd>"
        + f"<dt>Pinned</dt><dd>{yes_no(availability.get('pinned'))}</dd>"
        + f"<dt>Live IPFS verified</dt><dd>{yes_no(availability.get('live_ipfs_verified'))}</dd>"
        + f"<dt>Paid storage</dt><dd>{yes_no(availability.get('paid_storage'))}</dd>"
        + f"<dt>Durability claim</dt><dd>{yes_no(availability.get('durability_claim'))}</dd>"
        + field("Availability notes", availability.get("notes"), code=False)
        + "</dl>"
        + "<h5>Content addresses</h5>"
        + list_items(content_address_items)
        + "<h5>Provenance / attestation</h5>"
        + '<dl class="metadata">'
        + field("Attestation fixture", artifact.get("attestation"))
        + "</dl>"
        + list_items(provenance_items)
        + "</article>"
    )


def render_ci_check(check: dict) -> str:
    return (
        '<dl class="metadata">'
        + field("ID", check.get("id"))
        + field("Name", check.get("name"), code=False)
        + field("Provider", check.get("provider"))
        + field("Workflow", check.get("workflow"))
        + field("Status", check.get("status"))
        + field("Conclusion", check.get("conclusion"))
        + f"<dt>Synthetic</dt><dd>{yes_no(check.get('synthetic'))}</dd>"
        + f"<dt>Published publicly</dt><dd>{yes_no(check.get('published'))}</dd>"
        + field("Repository", check.get("repository"))
        + field("Commit", check.get("commit"))
        + field("URL", check.get("url"))
        + field("Notes", check.get("notes"), code=False)
        + "</dl>"
    )


def render_substrate(name: str, value: object) -> str:
    if not isinstance(value, dict):
        return f"<strong>{esc(name)}</strong>: <code>{esc(json.dumps(value, sort_keys=True))}</code>"
    rows = []
    for key, item in sorted(value.items()):
        if isinstance(item, bool):
            rows.append(f"<dt>{esc(key)}</dt><dd>{yes_no(item)}</dd>")
        elif isinstance(item, (list, dict)):
            rows.append(field(key, json.dumps(item, sort_keys=True)))
        else:
            rows.append(field(key, item))
    return f"<strong>{esc(name)}</strong><dl class=\"metadata\">{''.join(rows)}</dl>"


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
        artifacts = [render_artifact(artifact) for artifact in release.get("artifacts", [])]
        release_items.append(
            f"<h3>{esc(release.get('version', 'release'))}</h3><p>tag <code>{esc(release.get('tag', ''))}</code></p>"
            + list_items(artifacts)
        )
    substrate_items = []
    for name, value in sorted(data.get("substrates", {}).items()):
        substrate_items.append(render_substrate(name, value))
    ci_items = [render_ci_check(check) for check in data.get("ci_checks", [])]

    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <title>{esc(project['name'])}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 1000px; margin: 2rem auto; line-height: 1.5; padding: 0 1rem; }}
    code {{ background: #f4f4f4; padding: 0.1rem 0.25rem; }}
    section {{ border-top: 1px solid #ddd; margin-top: 1.5rem; padding-top: 1rem; }}
    .notice {{ background: #fff8d6; border: 1px solid #eadb8b; padding: 0.75rem; }}
    .artifact {{ border: 1px solid #ddd; border-radius: 0.4rem; padding: 1rem; margin: 0.75rem 0; }}
    .metadata {{ display: grid; grid-template-columns: minmax(10rem, 16rem) 1fr; gap: 0.35rem 0.75rem; }}
    .metadata dt {{ font-weight: 700; }}
    .metadata dd {{ margin: 0; overflow-wrap: anywhere; }}
    .flag {{ border-radius: 999px; padding: 0.05rem 0.5rem; font-weight: 700; }}
    .flag.yes {{ background: #e4f7e7; color: #126422; }}
    .flag.no {{ background: #f8e1df; color: #8b1c10; }}
    .flag.unknown {{ background: #eee; color: #333; }}
  </style>
</head>
<body>
  <h1>{esc(project['name'])}</h1>
  <p>{esc(project['description'])}</p>
  <p class="notice"><strong>Prototype boundary:</strong> this static page renders local registry fixture data. Synthetic CI/provenance, unsigned artifacts, and substrate hints are shown explicitly; the page does not claim production readiness, live pinning, real Sigstore/in-toto verification, Rekor upload, SLSA compliance, or public CI status unless those fields are verified separately.</p>
  <p><strong>Project ID:</strong> <code>{esc(project['id'])}</code><br>
     <strong>Default branch:</strong> <code>{esc(project['default_branch'])}</code><br>
     <strong>Registry updated:</strong> <code>{esc(data['updated_at'])}</code></p>

  <section><h2>Maintainers</h2>{list_items(maintainer_items)}</section>
  <section><h2>Clone URLs</h2>{list_items(clone_items)}</section>
  <section><h2>Issues</h2>{list_items(issue_items)}</section>
  <section><h2>Patches / PRs</h2>{list_items(patch_items)}</section>
  <section><h2>Releases</h2>{list_items(release_items)}</section>
  <section><h2>CI / provenance checks</h2>{list_items(ci_items)}</section>
  <section><h2>Protocol substrate details</h2>{list_items(substrate_items)}</section>
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
