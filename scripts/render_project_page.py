#!/usr/bin/env python3
"""Render a decentralized-forge project registry to a static HTML page.

Stdlib only by design.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from collections import Counter
from pathlib import Path

import nip34_adapter

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
VERIFICATION_STATE_ORDER = [
    "local-fixture",
    "source-inspected-mapping",
    "synthetic-fixture",
    "live-unverified",
    "live-verified",
]


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


def css_token(value: object) -> str:
    """Return a conservative CSS class token for fixture-derived labels."""
    token = "".join(ch if ch.isalnum() else "-" for ch in str(value).lower()).strip("-")
    return token or "unknown"


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


def ordered_count_items(counts: Counter, preferred_order: list[str]) -> list[tuple[str, int]]:
    ordered = [(key, counts[key]) for key in preferred_order if counts.get(key, 0)]
    ordered.extend((key, counts[key]) for key in sorted(counts) if key not in preferred_order)
    return ordered


def render_count_chips(items: list[tuple[str, int]], class_prefix: str) -> str:
    if not items:
        return "<p><em>None listed.</em></p>"
    return (
        '<ul class="summary-chips">\n'
        + "\n".join(
            f'  <li class="summary-chip {esc(class_prefix)}-{esc(css_token(label))}">'
            f'<span class="chip-label">{esc(label)}</span>: <strong>{esc(count)}</strong></li>'
            for label, count in items
        )
        + "\n</ul>"
    )


def summarize_verification_states(states: list[dict]) -> dict:
    state_counts = Counter(str(state.get("state", "unknown")) for state in states)
    live_counts = Counter("live_verified=true" if state.get("live_verified") is True else "live_verified=false" for state in states)
    synthetic_counts = Counter("synthetic=true" if state.get("synthetic") is True else "synthetic=false" for state in states)
    boundary_counts = Counter(str(state.get("claim_boundary", "not listed")) for state in states)
    return {
        "total": len(states),
        "state_counts": state_counts,
        "live_counts": live_counts,
        "synthetic_counts": synthetic_counts,
        "boundary_counts": boundary_counts,
    }


def render_verification_summary(states: list[dict], label: str, css_scope: str) -> str:
    summary = summarize_verification_states(states)
    return (
        f'<div class="verification-summary {esc(css_scope)}">'
        f"<h3>{esc(label)} summary</h3>"
        + '<dl class="metadata">'
        + field("Verification row count", summary["total"])
        + field("Live-verified row count", summary["live_counts"].get("live_verified=true", 0))
        + field("Live-unverified or local row count", summary["live_counts"].get("live_verified=false", 0))
        + field("Synthetic row count", summary["synthetic_counts"].get("synthetic=true", 0))
        + field("Non-synthetic row count", summary["synthetic_counts"].get("synthetic=false", 0))
        + "</dl>"
        + "<h4>Counts by state</h4>"
        + render_count_chips(ordered_count_items(summary["state_counts"], VERIFICATION_STATE_ORDER), "state")
        + "<h4>Counts by live verification flag</h4>"
        + render_count_chips(ordered_count_items(summary["live_counts"], ["live_verified=true", "live_verified=false"]), "live")
        + "<h4>Counts by synthetic flag</h4>"
        + render_count_chips(ordered_count_items(summary["synthetic_counts"], ["synthetic=true", "synthetic=false"]), "synthetic")
        + "<h4>Claim-boundary summary</h4>"
        + render_count_chips(ordered_count_items(summary["boundary_counts"], []), "boundary")
        + "</div>"
    )


def render_verification_rows_grouped(states: list[dict]) -> str:
    grouped = {state: [] for state in VERIFICATION_STATE_ORDER}
    extra_groups: dict[str, list[dict]] = {}
    for state in states:
        state_label = str(state.get("state", "unknown"))
        if state_label in grouped:
            grouped[state_label].append(state)
        else:
            extra_groups.setdefault(state_label, []).append(state)

    sections = []
    for state_label in VERIFICATION_STATE_ORDER:
        rows = grouped[state_label]
        if rows:
            sections.append(
                f'<div class="verification-state-group verification-state-group-{esc(css_token(state_label))}">'
                f"<h4>{esc(state_label)} ({esc(len(rows))})</h4>"
                + list_items([render_verification_state(row) for row in rows])
                + "</div>"
            )
    for state_label in sorted(extra_groups):
        rows = extra_groups[state_label]
        sections.append(
            f'<div class="verification-state-group verification-state-group-{esc(css_token(state_label))}">'
            f"<h4>{esc(state_label)} ({esc(len(rows))})</h4>"
            + list_items([render_verification_state(row) for row in rows])
            + "</div>"
        )
    return "".join(sections) if sections else "<p><em>None listed.</em></p>"


def render_verification_state(state: dict) -> str:
    state_label = state.get("state", "unknown")
    return (
        f'<article class="verification-state verification-state-{esc(css_token(state_label))}">'
        + '<dl class="metadata">'
        + field("Scope", state.get("scope"))
        + field("State", state_label)
        + f"<dt>Live verified</dt><dd>{yes_no(state.get('live_verified'))}</dd>"
        + f"<dt>Synthetic</dt><dd>{yes_no(state.get('synthetic'))}</dd>"
        + field("Evidence", state.get("evidence"), code=False)
        + field("Claim boundary", state.get("claim_boundary"), code=False)
        + field("Last checked", state.get("last_checked_at"))
        + field("Notes", state.get("notes"), code=False)
        + "</dl>"
        + "</article>"
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


def render_nip34_adapter_item(kind_label: str, item: dict) -> str:
    return (
        '<article class="adapter-item">'
        f"<h4>{esc(kind_label)}: {esc(item.get('title', 'Untitled'))}</h4>"
        + '<dl class="metadata">'
        + field("ID", item.get("id"))
        + field("Status", item.get("status"))
        + field("Source event kind", item.get("source_event_kind"))
        + field("Repository address", item.get("repository"))
        + field("Mapped registry path", item.get("mapped_registry_path"))
        + field("Summary", item.get("summary"), code=False)
        + "</dl>"
        + "</article>"
    )


def render_nip34_status_check(check: dict) -> str:
    return (
        '<article class="adapter-item">'
        f"<h4>Status/check: {esc(check.get('name', 'Untitled'))}</h4>"
        + '<dl class="metadata">'
        + field("Source CI check", check.get("source_ci_check_id"))
        + field("Mapped registry path", check.get("mapped_registry_path"))
        + field("Provider", check.get("provider"))
        + field("Status", check.get("status"))
        + field("Conclusion", check.get("conclusion"))
        + field("Target type", check.get("target_type"))
        + field("Target ref", check.get("target_ref"))
        + field("Target commit", check.get("target_commit"))
        + f"<dt>Synthetic</dt><dd>{yes_no(check.get('synthetic'))}</dd>"
        + f"<dt>Published</dt><dd>{yes_no(check.get('published'))}</dd>"
        + field("Notes", check.get("notes"), code=False)
        + "</dl>"
        + "</article>"
    )


def render_nip34_conformance_report(report: dict) -> str:
    shape = report.get("shape", {}) if isinstance(report.get("shape", {}), dict) else {}
    return (
        '<article class="adapter-item conformance-report">'
        f"<h4>Conformance: {esc(report.get('label', 'fixture event'))}</h4>"
        + '<dl class="metadata">'
        + field("Label", report.get("label"), code=False)
        + field("Kind", report.get("kind"))
        + f"<dt>Known NIP-34 kind</dt><dd>{yes_no(report.get('nip34_kind_known'))}</dd>"
        + f"<dt>Valid for local fixture</dt><dd>{yes_no(shape.get('valid_for_local_fixture'))}</dd>"
        + f"<dt>ID is placeholder</dt><dd>{yes_no(report.get('id_is_placeholder'))}</dd>"
        + f"<dt>Signature is placeholder</dt><dd>{yes_no(report.get('sig_is_placeholder'))}</dd>"
        + f"<dt>Signed</dt><dd>{yes_no(report.get('signed'))}</dd>"
        + f"<dt>Published</dt><dd>{yes_no(report.get('published'))}</dd>"
        + field("Possible event ID (local reference only)", report.get("possible_event_id"))
        + "</dl>"
        + "</article>"
    )


def render_nip34_adapter_verification_states(states: list) -> str:
    state_dicts = [state for state in states if isinstance(state, dict)]
    if not state_dicts:
        return ""
    return (
        "<h3>Adapter verification states</h3>"
        '<p class="notice"><strong>Adapter-local verification labels:</strong> these rows use the same '
        "<code>verification_states[]</code> vocabulary as the registry, but they describe only the optional NIP-34 fixture import below. "
        "They are separate from the top-level registry verification states and do not make live protocol claims.</p>"
        + render_verification_summary(state_dicts, "Adapter verification states", "adapter-verification-summary")
        + "<h4>Adapter verification rows grouped by state</h4>"
        + render_verification_rows_grouped(state_dicts)
    )


def render_nip34_conformance_summary(conformance: dict) -> str:
    reports = conformance.get("reports", []) if isinstance(conformance, dict) else []
    if not isinstance(reports, list) or not reports:
        return ""
    report_dicts = [report for report in reports if isinstance(report, dict)]
    known_count = sum(1 for report in report_dicts if report.get("nip34_kind_known") is True)
    report_items = [render_nip34_conformance_report(report) for report in report_dicts]
    return (
        "<h3>Local NIP-34 conformance summary</h3>"
        '<p class="notice"><strong>Local reference only:</strong> these rows summarize dry-run fixture shape metadata exported by '
        "<code>dry_run.conformance.reports[]</code>. Possible event IDs are local NIP-01 reference hashes only; "
        "they do not replace fixture IDs and are not signed or relay-accepted event ID claims.</p>"
        + '<dl class="metadata">'
        + field("Conformance report count", len(report_dicts))
        + field("Known NIP-34 kind count", known_count)
        + field("Conformance scope", conformance.get("scope"), code=False)
        + field("Conformance source", conformance.get("source"), code=False)
        + "</dl>"
        + list_items(report_items)
    )


def render_nip34_live_readback_event(event: dict) -> str:
    project = event.get("project", {}) if isinstance(event.get("project", {}), dict) else {}
    return (
        '<article class="adapter-item live-readback-event">'
        f"<h4>Live readback event: {esc(event.get('label', 'event'))}</h4>"
        + '<dl class="metadata">'
        + field("Event ID", event.get("event_id"))
        + field("Kind", event.get("kind"))
        + field("Pubkey", event.get("pubkey"))
        + field("Imported project ID", project.get("id"))
        + field("Imported project name", project.get("name"), code=False)
        + field("Readback verified relays", json.dumps(event.get("readback_verified_relays", []), sort_keys=True))
        + field("Publish relays", json.dumps(event.get("publish_relays", []), sort_keys=True))
        + f"<dt>Selected-relay readback verified</dt><dd>{yes_no(event.get('selected_relay_readback_verified'))}</dd>"
        + f"<dt>Readback fields match</dt><dd>{yes_no(event.get('readback_field_match'))}</dd>"
        + f"<dt>Local signature verified by nak</dt><dd>{yes_no(event.get('local_signature_verified_by_nak'))}</dd>"
        + f"<dt>Readback signature verified by nak</dt><dd>{yes_no(event.get('readback_signature_verified_by_nak'))}</dd>"
        + f"<dt>New event published in Loop 29</dt><dd>{yes_no(event.get('new_event_published_in_loop_29'))}</dd>"
        + "</dl>"
        + "<h5>Live readback non-claims</h5>"
        + list_items([esc(non_claim) for non_claim in event.get("non_claims", [])])
        + "</article>"
    )


def render_nip34_live_readback_section(live_readback: dict) -> str:
    if not isinstance(live_readback, dict) or not live_readback:
        return ""
    events = [event for event in live_readback.get("events", []) if isinstance(event, dict)]
    reports = [report for report in live_readback.get("conformance_reports", []) if isinstance(report, dict)]
    return (
        "<h3>NIP-34 live readback import</h3>"
        '<p class="notice"><strong>Selected-relay readback only:</strong> this subsection imports recorded Loop 25 Nostr evidence. '
        "It is separate from dry-run fixtures and does not claim durability, global propagation, censorship resistance, identity trust, security guarantees, production readiness, or full NIP-34/forge compatibility. "
        "Loop 29 performs no new relay publish/fetch/signing.</p>"
        + '<dl class="metadata">'
        + field("Live fixture schema", live_readback.get("schema_version"))
        + field("Source evidence", live_readback.get("source_evidence"), code=False)
        + field("Scope", live_readback.get("scope"))
        + field("Claim boundary", live_readback.get("claim_boundary"), code=False)
        + field("Live readback event count", len(events))
        + field("Live readback conformance report count", len(reports))
        + "</dl>"
        + list_items([render_nip34_live_readback_event(event) for event in events])
        + "<h4>Live readback conformance reports</h4>"
        + list_items([render_nip34_conformance_report(report) for report in reports])
    )


def render_json_block(value: object) -> str:
    return f"<pre><code>{esc(json.dumps(value, indent=2, sort_keys=True))}</code></pre>"


def load_live_evidence_index(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RegistryError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise RegistryError("live evidence index root must be an object")
    if data.get("schema_version") != "decentralized-forge.live-evidence-index.v1":
        raise RegistryError("unsupported live evidence index schema_version")
    evidence = data.get("evidence")
    if not isinstance(evidence, list):
        raise RegistryError("live evidence index evidence must be an array")
    for item in evidence:
        if not isinstance(item, dict):
            raise RegistryError("live evidence entries must be objects")
        for key in ["id", "protocol", "scope", "state", "evidence_file", "verification_summary", "non_claims"]:
            if not item.get(key):
                raise RegistryError(f"live evidence entry missing required field: {key}")
        if item.get("selected_relay_readback_verified") and item.get("protocol") != "nostr":
            raise RegistryError("selected relay readback evidence must be Nostr-scoped")
    return data


def render_live_evidence_item(item: dict) -> str:
    identifiers = item.get("public_identifiers", {}) if isinstance(item.get("public_identifiers"), dict) else {}
    return (
        f'<article class="live-evidence live-evidence-{esc(css_token(item.get("state", "unknown")))}">'
        f"<h3>{esc(item.get('id'))}</h3>"
        + '<dl class="metadata">'
        + field("Protocol", item.get("protocol"))
        + field("Scope", item.get("scope"))
        + field("Evidence state", item.get("state"))
        + field("Verified at", item.get("verified_at"))
        + field("Evidence file", item.get("evidence_file"), code=False)
        + field("Summary", item.get("verification_summary"), code=False)
        + f"<dt>Live network action</dt><dd>{yes_no(item.get('live_network_action'))}</dd>"
        + f"<dt>Local CLI verified</dt><dd>{yes_no(item.get('local_cli_verified'))}</dd>"
        + f"<dt>Selected-relay readback verified</dt><dd>{yes_no(item.get('selected_relay_readback_verified'))}</dd>"
        + f"<dt>Synthetic</dt><dd>{yes_no(item.get('synthetic'))}</dd>"
        + field("Public identifiers", json.dumps(identifiers, sort_keys=True))
        + field("Notes", item.get("notes"), code=False)
        + "</dl>"
        + "<h4>Non-claims preserved</h4>"
        + list_items([esc(non_claim) for non_claim in item.get("non_claims", [])])
        + "</article>"
    )


def render_live_evidence_section(index: dict | None) -> str:
    if not index:
        return ""
    evidence = [item for item in index.get("evidence", []) if isinstance(item, dict)]
    policy = index.get("claim_policy", {}) if isinstance(index.get("claim_policy", {}), dict) else {}
    return (
        "<section>"
        "<h2>Live evidence index</h2>"
        '<p class="notice"><strong>Narrow evidence only:</strong> these rows import Loop 23/25/34 evidence into the renderer. '
        "They distinguish local CLI verification, selected-relay readback, and one disposable public Radicle smoke from unverified durability, global propagation, censorship resistance, identity trust, production readiness, security guarantees, and full protocol compatibility.</p>"
        + '<dl class="metadata">'
        + field("Index schema", index.get("schema_version"))
        + field("Loop", index.get("loop"))
        + field("Created", index.get("created_at"))
        + f"<dt>Contains secret values</dt><dd>{yes_no(policy.get('contains_secret_values'))}</dd>"
        + field("Allowed claims", "; ".join(policy.get("allowed_claims", [])), code=False)
        + field("Forbidden claims", "; ".join(policy.get("forbidden_claims", [])), code=False)
        + "</dl>"
        + list_items([render_live_evidence_item(item) for item in evidence])
        + "</section>"
    )


def render_nip34_adapter_section(exported: dict | None) -> str:
    if not exported:
        return ""

    project = exported.get("project", {})
    nip34 = exported.get("substrates", {}).get("nip34", {})
    dry_run = exported.get("dry_run", {})
    collaboration = dry_run.get("collaboration", {}) if isinstance(dry_run, dict) else {}
    relay_tool_check = collaboration.get("relay_tool_check", {}) if isinstance(collaboration, dict) else {}
    synthetic_key_policy = collaboration.get("synthetic_key_policy", {}) if isinstance(collaboration, dict) else {}
    nip35_boundary = collaboration.get("nip35_boundary", {}) if isinstance(collaboration, dict) else {}
    issues = exported.get("issues", [])
    patches = exported.get("patches", [])
    repository_state = exported.get("repository_state", {})
    status_checks = exported.get("status_checks", [])
    repository_dry_run = dry_run.get("repository", {}) if isinstance(dry_run, dict) else {}
    state_status_dry_run = dry_run.get("state_status", {}) if isinstance(dry_run, dict) else {}
    repository_state_event = dry_run.get("repository_state_event", {}) if isinstance(dry_run, dict) else {}
    conformance = dry_run.get("conformance", {}) if isinstance(dry_run, dict) else {}
    adapter_verification_states = exported.get("verification_states", [])
    live_readback = exported.get("live_readback", {}) if isinstance(exported.get("live_readback", {}), dict) else {}

    issue_items = [render_nip34_adapter_item("Issue", issue) for issue in issues]
    patch_items = [render_nip34_adapter_item("Patch", patch) for patch in patches]
    status_items = [render_nip34_status_check(check) for check in status_checks]

    return (
        "<section>"
        "<h2>NIP-34 fixture adapter</h2>"
        '<p class="notice"><strong>NIP-34 local parser/conformance output:</strong> '
        "this section is generated from local NIP-34 fixture files via <code>scripts/nip34_adapter.py</code>. "
        "Dry-run rows do not perform relay publishing, signing, fixture ID replacement, relay fetching, or live verification; "
        "possible_event_id values are local reference hashes only, not signed or relay-accepted event ID claims. "
        "If a live readback fixture is supplied, it is displayed separately as selected-relay evidence only. Dry-run placeholders remain visible so fixture rows cannot be mistaken for live Nostr events.</p>"
        '<dl class="metadata">'
        + field("Repo ID", project.get("id"))
        + field("Repo name", project.get("name"), code=False)
        + field("Repository kind", nip34.get("repository_kind"))
        + field("Repo ID tag", nip34.get("repo_id_tag"))
        + field("Relay hints", json.dumps(nip34.get("relay_hints", []), sort_keys=True))
        + field("Publish status", nip34.get("publish_status"))
        + field("Issue count", len(issues))
        + field("Patch count", len(patches))
        + field("Repository dry-run event ID", repository_dry_run.get("id"))
        + field("Repository dry-run signature", repository_dry_run.get("sig"))
        + "</dl>"
        + render_nip34_adapter_verification_states(adapter_verification_states)
        + render_nip34_conformance_summary(conformance)
        + render_nip34_live_readback_section(live_readback)
        + "<h3>Repository state fixture</h3>"
        + '<dl class="metadata">'
        + field("State kind", repository_state.get("kind"))
        + field("State repo ID tag", repository_state.get("repo_id_tag"))
        + field("Repository address", repository_state.get("repository_address"))
        + field("HEAD", repository_state.get("head"))
        + field("HEAD ref", repository_state.get("head_ref"))
        + field("HEAD commit", repository_state.get("head_commit"))
        + field("Refs", json.dumps(repository_state.get("refs", {}), sort_keys=True))
        + field("State dry-run event ID", repository_state_event.get("id"))
        + field("State dry-run signature", repository_state_event.get("sig"))
        + "</dl>"
        "<h3>Imported issues</h3>"
        + list_items(issue_items)
        + "<h3>Imported patches</h3>"
        + list_items(patch_items)
        + "<h3>Fixture-only status/check projections</h3>"
        + list_items(status_items)
        + "<h3>Dry-run / non-claim fields</h3>"
        + "<h4>Relay tool check</h4>"
        + render_json_block(relay_tool_check)
        + "<h4>Synthetic key policy</h4>"
        + render_json_block(synthetic_key_policy)
        + "<h4>NIP-35 boundary</h4>"
        + render_json_block(nip35_boundary)
        + "<h4>Repository state/status non-claims</h4>"
        + render_json_block(state_status_dry_run)
        + "</section>"
    )


def render_registry(data: dict, nip34_adapter_export: dict | None = None, live_evidence_index: dict | None = None) -> str:
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
    verification_states = [state for state in data.get("verification_states", []) if isinstance(state, dict)]
    verification_state_summary = render_verification_summary(
        verification_states,
        "Registry verification states",
        "registry-verification-summary",
    )
    verification_state_groups = render_verification_rows_grouped(verification_states)

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
    .verification-summary {{ border: 1px solid #d7e0ef; border-radius: 0.4rem; padding: 0.75rem; margin: 0.75rem 0; background: #f8fbff; }}
    .summary-chips {{ display: flex; flex-wrap: wrap; gap: 0.4rem; padding: 0; margin: 0.4rem 0 0.8rem; list-style: none; }}
    .summary-chip {{ border: 1px solid #ddd; border-radius: 999px; padding: 0.15rem 0.6rem; background: #fff; }}
    .summary-chip.state-local-fixture, .verification-state-local-fixture {{ border-color: #9cc3ff; }}
    .summary-chip.state-source-inspected-mapping, .verification-state-source-inspected-mapping {{ border-color: #b49cff; }}
    .summary-chip.state-synthetic-fixture, .verification-state-synthetic-fixture {{ border-color: #f0bd65; }}
    .summary-chip.state-live-unverified, .verification-state-live-unverified {{ border-color: #d98b7f; }}
    .summary-chip.state-live-verified, .verification-state-live-verified {{ border-color: #73bf7b; }}
    .verification-state {{ border-left: 0.25rem solid #ddd; padding-left: 0.75rem; }}
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
  <section><h2>Verification states</h2><p class="notice"><strong>Verification labels:</strong> these records separate local fixtures, source-inspected mappings, synthetic fixtures, live-unverified scopes, and live-verified evidence. A scope is not live-verified unless its row says so explicitly.</p>{verification_state_summary}<h3>Registry verification rows grouped by state</h3>{verification_state_groups}</section>
  {render_live_evidence_section(live_evidence_index)}
  <section><h2>Protocol substrate details</h2>{list_items(substrate_items)}</section>
  {render_nip34_adapter_section(nip34_adapter_export)}
  <section><h2>Signature status</h2><p><code>{esc(json.dumps(data.get('signature', {}), sort_keys=True))}</code></p></section>
</body>
</html>
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", type=Path, help="Input project registry JSON")
    parser.add_argument("output", type=Path, help="Output HTML path")
    parser.add_argument("--nip34-repo-fixture", type=Path, help="Optional local NIP-34 repository announcement fixture JSON")
    parser.add_argument("--nip34-collaboration-fixture", type=Path, help="Optional local NIP-34 collaboration events fixture JSON")
    parser.add_argument("--nip34-state-status-fixture", type=Path, help="Optional local NIP-34 repository state/status fixture JSON")
    parser.add_argument("--nip34-live-readback-fixture", type=Path, help="Optional recorded NIP-34 live readback evidence fixture JSON")
    parser.add_argument("--live-evidence-index", type=Path, help="Optional live/local evidence index JSON")
    args = parser.parse_args(argv)
    if bool(args.nip34_repo_fixture) != bool(args.nip34_collaboration_fixture):
        parser.error("--nip34-repo-fixture and --nip34-collaboration-fixture must be provided together")
    if args.nip34_state_status_fixture and not (args.nip34_repo_fixture and args.nip34_collaboration_fixture):
        parser.error("--nip34-state-status-fixture requires the paired NIP-34 repository and collaboration fixtures")
    if args.nip34_live_readback_fixture and not (args.nip34_repo_fixture and args.nip34_collaboration_fixture):
        parser.error("--nip34-live-readback-fixture requires the paired NIP-34 repository and collaboration fixtures")
    try:
        data = load_registry(args.registry)
        nip34_export = None
        if args.nip34_repo_fixture and args.nip34_collaboration_fixture:
            state_status_fixture = nip34_adapter.load_json(args.nip34_state_status_fixture) if args.nip34_state_status_fixture else None
            live_readback_fixture = nip34_adapter.load_json(args.nip34_live_readback_fixture) if args.nip34_live_readback_fixture else None
            nip34_export = nip34_adapter.export_fixture_pair(
                nip34_adapter.load_json(args.nip34_repo_fixture),
                nip34_adapter.load_json(args.nip34_collaboration_fixture),
                state_status_fixture,
                live_readback_fixture,
            )
        live_evidence_index = load_live_evidence_index(args.live_evidence_index) if args.live_evidence_index else None
        rendered = render_registry(data, nip34_export, live_evidence_index)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    except (RegistryError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"registry error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
