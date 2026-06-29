#!/usr/bin/env python3
"""Render the first usable decentralized-forge app shell as static HTML."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

import forge_registry
import nip34_adapter
import render_project_page

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "output" / "forge-app.html"
DEFAULT_REGISTRIES = [
    ROOT / "fixtures" / "example-project.registry.json",
    ROOT / "fixtures" / "portable-lab.registry.json",
]
DEFAULT_NIP34_REPO = ROOT / "fixtures" / "nostr-repo-announcement.json"
DEFAULT_NIP34_COLLAB = ROOT / "fixtures" / "nostr-collaboration-events.json"
DEFAULT_NIP34_STATE = ROOT / "fixtures" / "nostr-repo-state-status.json"
DEFAULT_NIP34_LIVE = ROOT / "fixtures" / "nostr-live-readback-events.json"
DEFAULT_LIVE_EVIDENCE = ROOT / "fixtures" / "live-evidence-index.json"
DEFAULT_KEYLESS_IMPORT = ROOT / "fixtures" / "keyless-attestation.registry-verification.json"


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def esc_json_for_script(payload: object) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True).replace("</", "<\\/")


def tag_value(tags: list, key: str, default: str = "") -> str:
    for tag in tags:
        if isinstance(tag, list) and len(tag) >= 2 and tag[0] == key:
            return str(tag[1])
    return default


def live_nostr_collaboration(evidence: dict) -> list[dict]:
    if evidence.get("schema_version") != "decentralized-forge.nostr-issue-patch-readback.v1":
        return []
    rows: list[dict] = []
    for item in evidence.get("events", []):
        readback_events = [
            readback.get("event")
            for readback in item.get("readback", [])
            if isinstance(readback, dict) and readback.get("matched") and isinstance(readback.get("event"), dict)
        ]
        event = readback_events[0] if readback_events else None
        tags = event.get("tags", []) if isinstance(event, dict) else []
        rows.append(
            {
                "id": item.get("id"),
                "kind": item.get("kind"),
                "type": "issue" if item.get("kind") == 1621 else "patch",
                "title": tag_value(tags, "subject", item.get("fixture_name", "")),
                "status": tag_value(tags, "status", "readback"),
                "summary": (event.get("content", "") if isinstance(event, dict) else "").split("\n\n")[-1].strip()[:360],
                "pubkey": item.get("pubkey"),
                "readback_relays": [
                    readback.get("relay")
                    for readback in item.get("readback", [])
                    if isinstance(readback, dict) and readback.get("matched") and readback.get("verify_readback")
                ],
                "mapped_registry_path": item.get("mapped_registry_path"),
                "claim_boundary": evidence.get("claim_boundary"),
            }
        )
    return rows


def build_app_data(args: argparse.Namespace) -> dict:
    registries = [render_project_page.load_registry(path) for path in args.registries]
    registry_sources = [relative(path) for path in args.registries]
    live_evidence_index = read_json(args.live_evidence_index)
    nip34_export = nip34_adapter.export_fixture_pair(
        read_json(args.nip34_repo_fixture),
        read_json(args.nip34_collaboration_fixture),
        read_json(args.nip34_state_status_fixture),
        nip34_adapter.load_json(args.nip34_live_readback_fixture),
    )
    nostr_issue_patch_evidence = read_json(ROOT / "evidence" / "nostr-loop43-issue-patch-readback-2026-06-28.json")
    keyless_import = read_json(args.keyless_import)

    projects = []
    for source, registry in zip(registry_sources, registries):
        projects.append(
            {
                "source": source,
                "summary": forge_registry.registry_summary(registry, ROOT / source),
                "registry": registry,
            }
        )

    return {
        "schema_version": "decentralized-forge.static-app-data.v1",
        "generated_from": {
            "registries": registry_sources,
            "live_evidence_index": relative(args.live_evidence_index),
            "nip34_repo_fixture": relative(args.nip34_repo_fixture),
            "nip34_collaboration_fixture": relative(args.nip34_collaboration_fixture),
            "nip34_state_status_fixture": relative(args.nip34_state_status_fixture),
            "nip34_live_readback_fixture": relative(args.nip34_live_readback_fixture),
            "keyless_import": relative(args.keyless_import),
        },
        "projects": projects,
        "nip34": nip34_export,
        "live_nostr_collaboration": live_nostr_collaboration(nostr_issue_patch_evidence),
        "live_evidence_index": live_evidence_index,
        "keyless_import": keyless_import,
        "non_claims": [
            "static app does not publish protocol events",
            "static app does not sign events or use private keys",
            "static app does not start daemons, spend money, use wallets, or contact paid services",
            "static app does not claim durability, censorship resistance, broad availability, security, or production readiness",
        ],
    }


def render_html(app_data: dict) -> str:
    data_json = esc_json_for_script(app_data)
    title = "Decentralized Forge Workbench"
    html_doc = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__TITLE__</title>
  <style>
    :root {{
      --ink: #1e2428;
      --muted: #5e6970;
      --line: #d7dde1;
      --panel: #f6f8f9;
      --paper: #ffffff;
      --good: #116b4f;
      --warn: #8a5b00;
      --bad: #9b2c2c;
      --blue: #245f9f;
      --teal: #0f6f74;
      --rose: #9a3b5a;
      --shadow: 0 1px 2px rgba(0,0,0,.07);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background: #eef2f4;
      font: 14px/1.45 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    button, input, select, textarea {{ font: inherit; }}
    .app {{
      min-height: 100vh;
      display: grid;
      grid-template-columns: 248px minmax(0, 1fr);
    }}
    .rail {{
      background: #182126;
      color: #edf3f5;
      padding: 18px 14px;
      position: sticky;
      top: 0;
      height: 100vh;
      overflow: auto;
    }}
    .brand {{ margin: 0 0 18px; font-size: 18px; font-weight: 700; }}
    .project-select {{
      width: 100%;
      min-height: 36px;
      border: 1px solid #435059;
      background: #10171b;
      color: #fff;
      border-radius: 6px;
      padding: 6px 8px;
    }}
    .nav {{ display: grid; gap: 6px; margin-top: 18px; }}
    .nav button {{
      min-height: 36px;
      border: 0;
      border-radius: 6px;
      background: transparent;
      color: #d7e2e7;
      text-align: left;
      padding: 8px 10px;
      cursor: pointer;
    }}
    .nav button[aria-selected="true"] {{ background: #2b3941; color: #fff; }}
    main {{ padding: 22px; min-width: 0; }}
    .topbar {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 18px;
      margin-bottom: 18px;
    }}
    h1 {{ margin: 0; font-size: 26px; line-height: 1.15; letter-spacing: 0; }}
    h2 {{ margin: 0 0 12px; font-size: 19px; letter-spacing: 0; }}
    h3 {{ margin: 0 0 8px; font-size: 15px; letter-spacing: 0; }}
    p {{ margin: 0 0 10px; }}
    .muted {{ color: var(--muted); }}
    .grid {{ display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 12px; }}
    .metric, .panel, .item {{
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 7px;
      box-shadow: var(--shadow);
    }}
    .metric {{ padding: 12px; min-height: 76px; }}
    .metric strong {{ display: block; font-size: 23px; line-height: 1.1; }}
    .panel {{ padding: 14px; margin-bottom: 12px; }}
    .item {{ padding: 12px; margin-bottom: 10px; }}
    .span-3 {{ grid-column: span 3; }}
    .span-4 {{ grid-column: span 4; }}
    .span-6 {{ grid-column: span 6; }}
    .span-8 {{ grid-column: span 8; }}
    .span-12 {{ grid-column: span 12; }}
    .toolbar {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 12px; }}
    .toolbar input, .toolbar select, .field input, .field select, .field textarea {{
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 8px 9px;
      background: #fff;
      min-height: 36px;
    }}
    .toolbar input {{ min-width: min(320px, 100%); }}
    .segmented {{ display: inline-grid; grid-template-columns: 1fr 1fr; border: 1px solid var(--line); border-radius: 6px; overflow: hidden; }}
    .segmented button {{ border: 0; background: #fff; min-height: 34px; padding: 6px 10px; cursor: pointer; }}
    .segmented button[aria-pressed="true"] {{ background: #244558; color: #fff; }}
    .badge {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      border-radius: 999px;
      padding: 3px 8px;
      border: 1px solid var(--line);
      background: var(--panel);
      color: var(--ink);
      font-size: 12px;
      margin: 2px 4px 2px 0;
      max-width: 100%;
    }}
    .badge.good {{ border-color: #84baa8; color: var(--good); background: #edf8f4; }}
    .badge.warn {{ border-color: #d7bf74; color: var(--warn); background: #fff8df; }}
    .badge.bad {{ border-color: #d9a0a0; color: var(--bad); background: #fff0f0; }}
    .badge.blue {{ border-color: #9bb9d6; color: var(--blue); background: #eef6ff; }}
    .badge.rose {{ border-color: #d8a4b6; color: var(--rose); background: #fff2f6; }}
    dl.meta {{ display: grid; grid-template-columns: minmax(130px, 210px) minmax(0, 1fr); gap: 6px 12px; margin: 0; }}
    dt {{ color: var(--muted); }}
    dd {{ margin: 0; min-width: 0; overflow-wrap: anywhere; }}
    code, textarea.output {{ font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", monospace; }}
    .field {{ display: grid; gap: 5px; margin-bottom: 10px; }}
    .field textarea {{ min-height: 142px; resize: vertical; }}
    .output {{ width: 100%; min-height: 240px; resize: vertical; background: #10171b; color: #e8f1f4; }}
    .actions {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .primary, .secondary {{
      min-height: 36px;
      border-radius: 6px;
      padding: 7px 11px;
      cursor: pointer;
      border: 1px solid transparent;
    }}
    .primary {{ color: #fff; background: var(--teal); }}
    .secondary {{ color: var(--ink); background: #fff; border-color: var(--line); }}
    .hidden {{ display: none !important; }}
    @media (max-width: 860px) {{
      .app {{ grid-template-columns: 1fr; }}
      .rail {{ position: relative; height: auto; }}
      main {{ padding: 14px; }}
      .topbar {{ display: block; }}
      .span-3, .span-4, .span-6, .span-8 {{ grid-column: span 12; }}
      dl.meta {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
<div class="app">
  <aside class="rail">
    <p class="brand">Decentralized Forge</p>
    <select id="projectSelect" class="project-select" aria-label="Project"></select>
    <nav class="nav" aria-label="Views">
      <button data-view="overview" aria-selected="true">Overview</button>
      <button data-view="collaboration" aria-selected="false">Issues & patches</button>
      <button data-view="releases" aria-selected="false">Releases</button>
      <button data-view="evidence" aria-selected="false">Evidence</button>
      <button data-view="draft" aria-selected="false">Nostr draft</button>
    </nav>
  </aside>
  <main>
    <header class="topbar">
      <div>
        <h1 id="projectTitle"></h1>
        <p id="projectDescription" class="muted"></p>
      </div>
      <div id="projectBadges"></div>
    </header>
    <section id="view-overview"></section>
    <section id="view-collaboration" class="hidden"></section>
    <section id="view-releases" class="hidden"></section>
    <section id="view-evidence" class="hidden"></section>
    <section id="view-draft" class="hidden"></section>
  </main>
</div>
<script id="forge-data" type="application/json">__DATA_JSON__</script>
<script>
const app = JSON.parse(document.getElementById('forge-data').textContent);
let state = {{ projectIndex: 0, view: 'overview', evidenceProtocol: 'all', evidenceQuery: '', collabFilter: 'all', draftType: 'issue' }};

const $ = (id) => document.getElementById(id);
const project = () => app.projects[state.projectIndex];
const registry = () => project().registry;
const text = (value) => value == null || value === '' ? 'not listed' : String(value);
const badgeClass = (value) => value === true ? 'good' : value === false ? 'warn' : 'blue';
const escapeHtml = (value) => text(value).replace(/[&<>"']/g, (ch) => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[ch]));

function badge(label, kind = '') {{
  return `<span class="badge ${{kind}}">${{escapeHtml(label)}}</span>`;
}}

function meta(rows) {{
  return `<dl class="meta">${{rows.map(([k, v]) => `<dt>${{escapeHtml(k)}}</dt><dd>${{escapeHtml(v)}}</dd>`).join('')}}</dl>`;
}}

function setView(view) {{
  state.view = view;
  document.querySelectorAll('.nav button').forEach((button) => button.setAttribute('aria-selected', String(button.dataset.view === view)));
  ['overview', 'collaboration', 'releases', 'evidence', 'draft'].forEach((name) => $(`view-${{name}}`).classList.toggle('hidden', name !== view));
  render();
}}

function renderShell() {{
  const select = $('projectSelect');
  select.innerHTML = app.projects.map((item, index) => `<option value="${{index}}">${{escapeHtml(item.registry.project.name)}}</option>`).join('');
  select.value = String(state.projectIndex);
  select.onchange = () => {{ state.projectIndex = Number(select.value); render(); }};
  document.querySelectorAll('.nav button').forEach((button) => button.onclick = () => setView(button.dataset.view));
}}

function renderHeader() {{
  const reg = registry();
  $('projectTitle').textContent = reg.project.name;
  $('projectDescription').textContent = reg.project.description;
  $('projectBadges').innerHTML = [
    badge(reg.project.default_branch, 'blue'),
    badge(`${{reg.clone_urls.length}} clone URL${{reg.clone_urls.length === 1 ? '' : 's'}}`, 'blue'),
    badge(`${{app.live_evidence_index.evidence.length}} evidence rows`, 'good')
  ].join('');
}}

function renderOverview() {{
  const reg = registry();
  const summary = project().summary;
  $('view-overview').innerHTML = `
    <div class="grid">
      ${{metric('Issues', summary.counts.issues)}}
      ${{metric('Patches', summary.counts.patches)}}
      ${{metric('Artifacts', summary.counts.artifacts)}}
      ${{metric('Evidence', app.live_evidence_index.evidence.length)}}
    </div>
    <div class="grid">
      <section class="panel span-6"><h2>Maintainers</h2>${{reg.maintainers.map((m) => `<div class="item">${{meta([['Name', m.name], ['ID type', m.id_type], ['Public ID', m.public_id], ['Role', m.role]])}}</div>`).join('')}}</section>
      <section class="panel span-6"><h2>Clone URLs</h2>${{reg.clone_urls.map((clone) => `<div class="item">${{badge(clone.transport, 'blue')}}<code>${{escapeHtml(clone.url)}}</code></div>`).join('')}}</section>
      <section class="panel span-12"><h2>Trust boundary</h2>${{app.non_claims.map((claim) => badge(claim, 'warn')).join('')}}</section>
    </div>`;
}}

function metric(label, value) {{
  return `<div class="metric span-3"><strong>${{escapeHtml(value)}}</strong><span class="muted">${{escapeHtml(label)}}</span></div>`;
}}

function collaborationRows() {{
  const localIssues = (registry().issues || []).map((item) => ({{...item, type: 'issue', evidence: 'local registry fixture'}}));
  const localPatches = (registry().patches || []).map((item) => ({{...item, type: 'patch', evidence: 'local registry fixture'}}));
  const live = app.live_nostr_collaboration.map((item) => ({{...item, evidence: 'selected-relay readback'}}));
  return [...live, ...localIssues, ...localPatches].filter((item) => state.collabFilter === 'all' || item.type === state.collabFilter);
}}

function renderCollaboration() {{
  $('view-collaboration').innerHTML = `
    <div class="toolbar">
      <select id="collabFilter" aria-label="Collaboration filter">
        <option value="all">All records</option>
        <option value="issue">Issues</option>
        <option value="patch">Patches</option>
      </select>
      ${{badge('selected-relay readback is narrow evidence', 'warn')}}
    </div>
    <div id="collabList"></div>`;
  $('collabFilter').value = state.collabFilter;
  $('collabFilter').onchange = (event) => {{ state.collabFilter = event.target.value; renderCollaboration(); }};
  $('collabList').innerHTML = collaborationRows().map((item) => `
    <article class="item">
      <h3>${{escapeHtml(item.title || item.id)}}</h3>
      <p class="muted">${{escapeHtml(item.summary || item.content || '')}}</p>
      ${{badge(item.type, item.type === 'issue' ? 'blue' : 'rose')}}
      ${{badge(item.status || 'readback', 'good')}}
      ${{badge(item.evidence, item.evidence.includes('readback') ? 'good' : 'warn')}}
      ${{item.readback_relays ? item.readback_relays.map((relay) => badge(relay, 'blue')).join('') : ''}}
      ${{meta([['ID', item.id], ['Mapped path', item.mapped_registry_path], ['Boundary', item.claim_boundary || 'local fixture only']])}}
    </article>`).join('');
}}

function renderReleases() {{
  const releases = registry().releases || [];
  $('view-releases').innerHTML = releases.map((release) => `
    <section class="panel">
      <h2>${{escapeHtml(release.version)}} <span class="muted">${{escapeHtml(release.tag)}}</span></h2>
      ${(release.artifacts || []).map((artifact) => `
        <article class="item">
          <h3>${{escapeHtml(artifact.name)}}</h3>
          ${{meta([['SHA-256', artifact.sha256], ['CID', artifact.cid], ['URI', artifact.uri], ['Signature', artifact.signature]])}}
          ${{badge('local fixture: ' + text(artifact.availability?.local_fixture), badgeClass(artifact.availability?.local_fixture))}}
          ${{badge('pinned: ' + text(artifact.availability?.pinned), badgeClass(artifact.availability?.pinned))}}
          ${{badge('durability claim: ' + text(artifact.availability?.durability_claim), badgeClass(!artifact.availability?.durability_claim))}}
        </article>`).join('')}
    </section>`).join('');
}}

function renderEvidence() {{
  const protocols = ['all', ...new Set(app.live_evidence_index.evidence.map((item) => item.protocol))];
  const query = state.evidenceQuery.toLowerCase();
  const rows = app.live_evidence_index.evidence.filter((item) => {{
    const protocolOk = state.evidenceProtocol === 'all' || item.protocol === state.evidenceProtocol;
    const queryOk = !query || JSON.stringify(item).toLowerCase().includes(query);
    return protocolOk && queryOk;
  }});
  $('view-evidence').innerHTML = `
    <div class="toolbar">
      <select id="evidenceProtocol" aria-label="Evidence protocol">${{protocols.map((p) => `<option value="${{p}}">${{p}}</option>`).join('')}}</select>
      <input id="evidenceQuery" type="search" value="${{escapeHtml(state.evidenceQuery)}}" placeholder="Filter evidence" aria-label="Filter evidence">
    </div>
    <div id="evidenceList"></div>`;
  $('evidenceProtocol').value = state.evidenceProtocol;
  $('evidenceProtocol').onchange = (event) => {{ state.evidenceProtocol = event.target.value; renderEvidence(); }};
  $('evidenceQuery').oninput = (event) => {{ state.evidenceQuery = event.target.value; renderEvidence(); }};
  $('evidenceList').innerHTML = rows.map((item) => `
    <article class="item">
      <h3>${{escapeHtml(item.id)}}</h3>
      <p>${{escapeHtml(item.verification_summary)}}</p>
      ${{badge(item.protocol, 'blue')}}
      ${{badge(item.state, item.synthetic ? 'warn' : 'good')}}
      ${{badge('live network: ' + item.live_network_action, badgeClass(item.live_network_action))}}
      ${{badge('selected relay: ' + item.selected_relay_readback_verified, badgeClass(item.selected_relay_readback_verified))}}
      ${{meta([['Evidence file', item.evidence_file], ['Evidence SHA-256', item.evidence_sha256], ['Scope', item.scope], ['Non-claims', item.non_claims.join('; ')]])}}
    </article>`).join('');
}}

function currentRepoAddress() {{
  return app.nip34.repository?.address || '30617:0000000000000000000000000000000000000000000000000000000000000000:demo-project';
}}

function draftEvent() {{
  const title = $('draftTitle')?.value || '';
  const body = $('draftBody')?.value || '';
  const status = $('draftStatus')?.value || 'open';
  const kind = state.draftType === 'issue' ? 1621 : 1617;
  return {{
    draft_notice: 'unsigned local draft; not signed, not published, not relayed',
    kind,
    created_at: Math.floor(Date.now() / 1000),
    tags: [
      ['a', currentRepoAddress(), '', 'root'],
      ['subject', title],
      ['status', status],
      ['t', 'decentralized-forge'],
      ['client', 'decentralized-forge-static-workbench']
    ],
    content: body,
    non_claims: app.non_claims
  }};
}}

function updateDraftOutput() {{
  $('draftOutput').value = JSON.stringify(draftEvent(), null, 2);
}}

function renderDraft() {{
  $('view-draft').innerHTML = `
    <section class="panel">
      <h2>Nostr collaboration draft</h2>
      <div class="segmented" role="group" aria-label="Draft type">
        <button id="draftIssue" aria-pressed="${{state.draftType === 'issue'}}">Issue</button>
        <button id="draftPatch" aria-pressed="${{state.draftType === 'patch'}}">Patch</button>
      </div>
      <div class="grid" style="margin-top:12px">
        <div class="span-6">
          <label class="field">Title<input id="draftTitle" value="${{state.draftType === 'issue' ? 'Define portable project identity' : 'Add static registry renderer'}}"></label>
          <label class="field">Status<select id="draftStatus"><option value="open">open</option><option value="proposed">proposed</option><option value="review">review</option></select></label>
          <label class="field">Body<textarea id="draftBody">${{state.draftType === 'issue' ? 'Track a concrete collaboration question for the project.' : 'Summarize a patch proposal or paste a small format-patch body.'}}</textarea></label>
          <div class="actions">
            <button id="refreshDraft" class="primary">Refresh draft</button>
            <button id="downloadDraft" class="secondary">Download JSON</button>
          </div>
        </div>
        <div class="span-6">
          <label class="field">Draft JSON<textarea id="draftOutput" class="output" readonly></textarea></label>
          ${{badge('unsigned local draft', 'warn')}}${{badge('no relay publish action', 'good')}}
        </div>
      </div>
    </section>`;
  $('draftIssue').onclick = () => {{ state.draftType = 'issue'; renderDraft(); }};
  $('draftPatch').onclick = () => {{ state.draftType = 'patch'; renderDraft(); }};
  ['draftTitle', 'draftStatus', 'draftBody'].forEach((id) => $(id).oninput = updateDraftOutput);
  $('refreshDraft').onclick = updateDraftOutput;
  $('downloadDraft').onclick = () => {{
    updateDraftOutput();
    const blob = new Blob([$('draftOutput').value + '\\n'], {{ type: 'application/json' }});
    const anchor = document.createElement('a');
    anchor.href = URL.createObjectURL(blob);
    anchor.download = `nostr-${{state.draftType}}-draft.json`;
    anchor.click();
    URL.revokeObjectURL(anchor.href);
  }};
  updateDraftOutput();
}}

function render() {{
  renderHeader();
  if (state.view === 'overview') renderOverview();
  if (state.view === 'collaboration') renderCollaboration();
  if (state.view === 'releases') renderReleases();
  if (state.view === 'evidence') renderEvidence();
  if (state.view === 'draft') renderDraft();
}}

renderShell();
render();
</script>
</body>
</html>
"""
    html_doc = html_doc.replace("{{", "{").replace("}}", "}")
    return html_doc.replace("__TITLE__", html.escape(title)).replace("__DATA_JSON__", data_json)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", nargs="?", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--registry", dest="registries", action="append", type=Path, default=[])
    parser.add_argument("--nip34-repo-fixture", type=Path, default=DEFAULT_NIP34_REPO)
    parser.add_argument("--nip34-collaboration-fixture", type=Path, default=DEFAULT_NIP34_COLLAB)
    parser.add_argument("--nip34-state-status-fixture", type=Path, default=DEFAULT_NIP34_STATE)
    parser.add_argument("--nip34-live-readback-fixture", type=Path, default=DEFAULT_NIP34_LIVE)
    parser.add_argument("--live-evidence-index", type=Path, default=DEFAULT_LIVE_EVIDENCE)
    parser.add_argument("--keyless-import", type=Path, default=DEFAULT_KEYLESS_IMPORT)
    args = parser.parse_args(argv)
    if not args.registries:
        args.registries = DEFAULT_REGISTRIES
    app_data = build_app_data(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_html(app_data), encoding="utf-8")
    print(f"wrote forge app: {relative(args.output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
