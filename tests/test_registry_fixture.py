import json
import base64
import hashlib
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import nip34_adapter
import forge_registry
import live_gate_inventory
import next_loop_controller
import preflight_static_artifact
import render_forge_app
import render_project_page

SCHEMA_PATH = ROOT / "schemas" / "project-registry.schema.json"
LIVE_EVIDENCE_SCHEMA_PATH = ROOT / "schemas" / "live-evidence-index.schema.json"
FIXTURE_PATH = ROOT / "fixtures" / "example-project.registry.json"
PORTABLE_FIXTURE_PATH = ROOT / "fixtures" / "portable-lab.registry.json"
RADICLE_FIXTURE_PATH = ROOT / "fixtures" / "radicle-backed-project.registry.json"
ONBOARDING_SAMPLE_FIXTURE_PATH = ROOT / "fixtures" / "onboarding-sample.registry.json"
NOSTR_REPO_FIXTURE_PATH = ROOT / "fixtures" / "nostr-repo-announcement.json"
NOSTR_COLLAB_FIXTURE_PATH = ROOT / "fixtures" / "nostr-collaboration-events.json"
NOSTR_STATE_STATUS_FIXTURE_PATH = ROOT / "fixtures" / "nostr-repo-state-status.json"
NOSTR_LIVE_READBACK_FIXTURE_PATH = ROOT / "fixtures" / "nostr-live-readback-events.json"
LIVE_REPLAY_CHECKLIST_PATH = ROOT / "fixtures" / "live-adapter-replay-checklist.json"
LIVE_EVIDENCE_INDEX_PATH = ROOT / "fixtures" / "live-evidence-index.json"
NEXT_LOOP_CONTROLLER_PATH = ROOT / "fixtures" / "next-loop-controller.json"
NEXT_LOOP_WORKFLOW_PATH = ROOT / ".github" / "workflows" / "next-loop.yml"
CI_WORKFLOW_PATH = ROOT / ".github" / "workflows" / "ci.yml"
LOCAL_RELEASE_ARTIFACT_PATH = ROOT / "fixtures" / "local-release-artifact.txt"
ONBOARDING_SAMPLE_ARTIFACT_PATH = ROOT / "fixtures" / "onboarding-sample-artifact.txt"
HELIA_LOCAL_EVIDENCE_PATH = ROOT / "evidence" / "helia-local-ipfs-add-get-2026-06-28.json"
PUBLIC_GATEWAY_PREFLIGHT_PATH = ROOT / "evidence" / "public-gateway-pinning-preflight-2026-06-28.json"
NOSTR_ISSUE_PATCH_READBACK_PATH = ROOT / "evidence" / "nostr-loop43-issue-patch-readback-2026-06-28.json"
RADICLE_BROADER_CHECK_PATH = ROOT / "evidence" / "radicle-loop44-broader-check-2026-06-28.json"
RADICLE_PROJECT_REPO_SMOKE_PATH = ROOT / "evidence" / "radicle-project-repo-smoke-2026-06-29.json"
RADICLE_FRESH_READBACK_CHECK_PATH = ROOT / "evidence" / "radicle-fresh-readback-check-2026-06-29.json"
RADICLE_UPDATE_CONTINUITY_CHECK_PATH = ROOT / "evidence" / "radicle-update-continuity-check-2026-06-29.json"
RADICLE_RETAINED_DELEGATE_CHECK_PATH = ROOT / "evidence" / "radicle-retained-delegate-check-2026-06-29.json"
RADICLE_RETAINED_UPDATE_CHECK_PATH = ROOT / "evidence" / "radicle-retained-update-check-2026-06-29.json"
RADICLE_INDEPENDENT_AVAILABILITY_CHECK_PATH = ROOT / "evidence" / "radicle-independent-availability-check-2026-06-29.json"
RADICLE_SEED_RESTART_CHECK_PATH = ROOT / "evidence" / "radicle-seed-restart-check-2026-06-29.json"
RADICLE_VPS_FOLLOWER_PUBLIC_READBACK_PATH = ROOT / "evidence" / "radicle-vps-follower-public-readback-2026-06-29.json"
RADICLE_VPS_FOLLOWER_SYSTEMD_SERVICE_PATH = ROOT / "evidence" / "radicle-vps-follower-systemd-service-2026-06-29.json"
RADICLE_PUBLIC_SEED_HEALTH_CHECK_PATH = ROOT / "evidence" / "radicle-public-seed-health-check-2026-06-29.json"
RADICLE_PUBLIC_SEED_UPDATE_PROPAGATION_PATH = ROOT / "evidence" / "radicle-public-seed-update-propagation-2026-06-29.json"
RADICLE_PUBLIC_SEED_UPDATE_HEALTH_CHECK_PATH = ROOT / "evidence" / "radicle-public-seed-update-health-check-2026-06-29.json"
RADICLE_EXTERNAL_HEALTH_TIMER_PATH = ROOT / "evidence" / "radicle-external-health-timer-2026-06-29.json"
RADICLE_EXTERNAL_HEALTH_TIMER_LATEST_PATH = ROOT / "evidence" / "radicle-external-health-timer-latest-ef16e2a-2026-06-29.json"
RADICLE_PUBLIC_SEED_UPDATE_EF16E2A_PATH = ROOT / "evidence" / "radicle-public-seed-update-ef16e2a-2026-06-29.json"
RADICLE_PUBLIC_SEED_UPDATE_EF16E2A_HEALTH_CHECK_PATH = ROOT / "evidence" / "radicle-public-seed-update-health-check-ef16e2a-2026-06-29.json"
RADICLE_UBUNTU_WORK_FOLLOWER_BOOTSTRAP_PATH = ROOT / "evidence" / "radicle-ubuntu-work-follower-bootstrap-2026-06-29.json"
RADICLE_SECOND_SEED_TAILNET_HEALTH_PATH = ROOT / "evidence" / "radicle-second-seed-tailnet-health-2026-06-29.json"
KEYLESS_REGISTRY_IMPORT_PATH = ROOT / "fixtures" / "keyless-attestation.registry-verification.json"
FIXTURE_PATHS = [FIXTURE_PATH, PORTABLE_FIXTURE_PATH, RADICLE_FIXTURE_PATH]
RENDERER = ROOT / "scripts" / "render_project_page.py"
STATIC_PREFLIGHT = ROOT / "scripts" / "preflight_static_artifact.py"
PORTABLE_BUNDLE_REVIEW_CHECKLIST = ROOT / "docs" / "portable-bundle-review-checklist.md"
RADICLE_PERSISTENT_SEED_PLAN = ROOT / "docs" / "radicle-persistent-seed-plan.md"
RADICLE_RETAINED_RID_QUICKSTART = ROOT / "docs" / "radicle-retained-rid-quickstart.md"
OUTPUT_DEMO_HTML = ROOT / "output" / "demo-project.html"
OUTPUT_VERIFICATION_BUNDLE = ROOT / "output" / "decentralized-forge-verification-bundle.zip"
OUTPUT_FORGE_APP_HTML = ROOT / "output" / "forge-app.html"
OUTPUT_FORGE_APP_WITH_ONBOARDING_HTML = ROOT / "output" / "forge-app-with-onboarding-sample.html"
OUTPUT_PORTABLE_HTML = ROOT / "output" / "portable-lab.html"
OUTPUT_ONBOARDING_SAMPLE_HTML = ROOT / "output" / "onboarding-sample.registry.html"
OUTPUT_DEMO_SUMMARY = ROOT / "output" / "demo-project.summary.json"
OUTPUT_PORTABLE_SUMMARY = ROOT / "output" / "portable-lab.summary.json"
OUTPUT_ONBOARDING_SAMPLE_SUMMARY = ROOT / "output" / "onboarding-sample.registry.summary.json"
OUTPUT_ONBOARDING_SAMPLE_REPORT = ROOT / "output" / "onboarding-sample.bundle-report.json"
CIDV1_BASE32_RE = re.compile(r"^b[a-z2-7]{20,}$")


class RegistryFixtureTests(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        self.portable_fixture = json.loads(PORTABLE_FIXTURE_PATH.read_text(encoding="utf-8"))
        self.radicle_fixture = json.loads(RADICLE_FIXTURE_PATH.read_text(encoding="utf-8"))
        self.onboarding_sample_fixture = json.loads(ONBOARDING_SAMPLE_FIXTURE_PATH.read_text(encoding="utf-8"))
        self.nostr_repo_fixture = json.loads(NOSTR_REPO_FIXTURE_PATH.read_text(encoding="utf-8"))
        self.nostr_collab_fixture = json.loads(NOSTR_COLLAB_FIXTURE_PATH.read_text(encoding="utf-8"))
        self.nostr_state_status_fixture = json.loads(NOSTR_STATE_STATUS_FIXTURE_PATH.read_text(encoding="utf-8"))
        self.nostr_live_readback_fixture = json.loads(NOSTR_LIVE_READBACK_FIXTURE_PATH.read_text(encoding="utf-8"))
        self.live_replay_checklist = json.loads(LIVE_REPLAY_CHECKLIST_PATH.read_text(encoding="utf-8"))
        self.live_evidence_index = json.loads(LIVE_EVIDENCE_INDEX_PATH.read_text(encoding="utf-8"))
        self.next_loop_controller = json.loads(NEXT_LOOP_CONTROLLER_PATH.read_text(encoding="utf-8"))
        self.fixtures = [json.loads(path.read_text(encoding="utf-8")) for path in FIXTURE_PATHS]

    def iter_artifacts(self):
        for fixture in self.fixtures:
            for release in fixture.get("releases", []):
                for artifact in release.get("artifacts", []):
                    yield fixture, release, artifact

    def fixture_file_uri_path(self, uri):
        self.assertTrue(uri.startswith("file://"))
        relative_path = uri.removeprefix("file://")
        self.assertFalse(relative_path.startswith("/"), "fixture artifact URIs must be repository-relative")
        return ROOT / relative_path

    def local_raw_cidv1_for_bytes(self, content):
        digest = hashlib.sha256(content).digest()
        cid_bytes = bytes([0x01, 0x55, 0x12, 0x20]) + digest
        return "b" + base64.b32encode(cid_bytes).decode("ascii").lower().rstrip("=")

    def current_git_head(self):
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return result.stdout.strip()

    def git_commit_exists(self, commit):
        subprocess.run(
            ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )

    def assert_fixture_head_is_current_or_ancestor(self, fixture_head):
        current_head = self.current_git_head()
        if fixture_head == current_head:
            return
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", fixture_head, current_head],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )

    def test_schema_and_fixtures_are_valid_json_objects(self):
        self.assertIsInstance(self.schema, dict)
        self.assertIsInstance(json.loads(LIVE_EVIDENCE_SCHEMA_PATH.read_text(encoding="utf-8")), dict)
        for fixture in self.fixtures:
            self.assertIsInstance(fixture, dict)
            self.assertEqual(fixture["schema_version"], "decentralized-forge.project-registry.v1")

    def test_live_evidence_index_hashes_match_recorded_files(self):
        errors = forge_registry.validate_live_evidence_index(LIVE_EVIDENCE_INDEX_PATH)
        self.assertEqual(errors, [])
        refreshed = forge_registry.refresh_live_evidence_hashes(LIVE_EVIDENCE_INDEX_PATH)
        self.assertEqual(refreshed, self.live_evidence_index)
        for item in self.live_evidence_index["evidence"]:
            evidence_path = ROOT / item["evidence_file"]
            self.assertTrue(evidence_path.is_file())
            canonical_bytes = forge_registry.canonical_evidence_bytes(evidence_path)
            self.assertEqual(item["evidence_sha256"], hashlib.sha256(canonical_bytes).hexdigest())
            self.assertEqual(item["evidence_size_bytes"], len(canonical_bytes))

    def test_live_evidence_index_validator_rejects_stale_hashes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_index = Path(tmpdir) / "live-evidence-index.json"
            tampered = json.loads(json.dumps(self.live_evidence_index))
            tampered["evidence"][0]["evidence_sha256"] = "0" * 64
            tmp_index.write_text(json.dumps(tampered), encoding="utf-8")
            errors = forge_registry.validate_live_evidence_index(tmp_index)
            self.assertTrue(any("evidence_sha256 does not match" in error for error in errors))

    def test_forge_registry_doctor_is_read_only_and_secret_free(self):
        report = forge_registry.doctor_report()
        self.assertEqual(report["schema_version"], "decentralized-forge.doctor.v1")
        self.assertTrue(report["checks"]["live_evidence_index_valid"])
        self.assertIn("git", report["tools"])
        self.assertIn("rad", report["tools"])
        combined = json.dumps(report).lower()
        self.assertIn("no live protocol actions", combined)
        self.assertIn("does not publish protocol events", combined)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, combined)

    def test_forge_registry_cli_exports_deterministic_summaries(self):
        demo_summary = forge_registry.registry_summary(self.fixture, FIXTURE_PATH)
        portable_summary = forge_registry.registry_summary(self.portable_fixture, PORTABLE_FIXTURE_PATH)
        onboarding_summary = forge_registry.registry_summary(self.onboarding_sample_fixture, ONBOARDING_SAMPLE_FIXTURE_PATH)
        self.assertEqual(demo_summary, json.loads(OUTPUT_DEMO_SUMMARY.read_text(encoding="utf-8")))
        self.assertEqual(portable_summary, json.loads(OUTPUT_PORTABLE_SUMMARY.read_text(encoding="utf-8")))
        self.assertEqual(onboarding_summary, json.loads(OUTPUT_ONBOARDING_SAMPLE_SUMMARY.read_text(encoding="utf-8")))
        self.assertEqual(portable_summary["project"]["id"], "portable-lab")
        self.assertEqual(portable_summary["counts"]["issues"], 1)
        self.assertEqual(portable_summary["counts"]["patches"], 1)
        self.assertEqual(portable_summary["counts"]["artifacts"], 1)
        self.assertEqual(portable_summary["counts"]["verification_states"], 4)
        self.assertFalse(portable_summary["non_claims"]["production_ready"])
        self.assertEqual(onboarding_summary["project"]["id"], "onboarding-sample")
        self.assertEqual(onboarding_summary["counts"]["artifacts"], 1)
        self.assertEqual(onboarding_summary["artifact_names"], ["onboarding-sample-artifact.txt"])

    def test_forge_registry_cli_renders_second_fixture_without_demo_adapters(self):
        html = OUTPUT_PORTABLE_HTML.read_text(encoding="utf-8")
        self.assertIn("Portable Lab Registry Fixture", html)
        self.assertIn("portable-lab", html)
        self.assertIn("Prototype boundary", html)
        self.assertIn("Second local registry fixture only", html)
        self.assertNotIn("NIP-34 fixture adapter", html)
        self.assertNotIn("Live evidence index", html)

    def test_committed_onboarding_sample_is_current_and_bounded(self):
        registry = self.onboarding_sample_fixture
        render_project_page.validate_registry(registry)
        self.assertEqual(registry["project"]["id"], "onboarding-sample")
        self.assertEqual(registry["project"]["name"], "Onboarding Sample")
        self.assertEqual(registry["clone_urls"][0]["url"], "file://.")
        self.assertEqual(registry["maintainers"][0]["public_id"], "local-import-placeholder")
        self.assertEqual(registry["signature"]["status"], "unsigned-fixture")
        self.assertEqual(len(registry["releases"]), 1)
        artifact = registry["releases"][0]["artifacts"][0]
        artifact_bytes = ONBOARDING_SAMPLE_ARTIFACT_PATH.read_bytes()
        expected_sha256 = hashlib.sha256(artifact_bytes).hexdigest()
        self.assertEqual(artifact["name"], "onboarding-sample-artifact.txt")
        self.assertEqual(artifact["uri"], "file://fixtures/onboarding-sample-artifact.txt")
        self.assertEqual(artifact["sha256"], expected_sha256)
        self.assertEqual(artifact["hashes"]["sha256"], expected_sha256)
        self.assertEqual(artifact["size_bytes"], len(artifact_bytes))
        self.assertTrue(artifact["availability"]["local_fixture"])
        self.assertFalse(artifact["availability"]["pinned"])
        self.assertFalse(artifact["availability"]["live_ipfs_verified"])
        self.assertFalse(artifact["availability"]["paid_storage"])
        self.assertFalse(artifact["availability"]["durability_claim"])
        scopes = {state["scope"] for state in registry["verification_states"]}
        self.assertEqual(scopes, {"registry.local_import_scaffold", "registry.local_artifact_metadata"})
        scaffold_state = [state for state in registry["verification_states"] if state["scope"] == "registry.local_import_scaffold"][0]
        commit_match = re.search(r"commit ([0-9a-f]{40})", scaffold_state["evidence"])
        self.assertIsNotNone(commit_match)
        self.assert_fixture_head_is_current_or_ancestor(commit_match.group(1))

        with tempfile.TemporaryDirectory() as tmpdir:
            generated = Path(tmpdir) / "onboarding-sample.html"
            self.assertEqual(render_project_page.main([str(ONBOARDING_SAMPLE_FIXTURE_PATH), str(generated)]), 0)
            self.assertEqual(generated.read_text(encoding="utf-8"), OUTPUT_ONBOARDING_SAMPLE_HTML.read_text(encoding="utf-8"))

        report = json.loads(OUTPUT_ONBOARDING_SAMPLE_REPORT.read_text(encoding="utf-8"))
        self.assertEqual(report, forge_registry.bundle_report(OUTPUT_VERIFICATION_BUNDLE))
        self.assertTrue(report["verification"]["valid"])
        self.assertIn("onboarding-sample", {project["project"]["id"] for project in report["projects"]})

        combined = json.dumps(registry).lower()
        for required_boundary in ["local registry scaffold only", "local file metadata only", "no ipfs add", "not-pinned"]:
            self.assertIn(required_boundary, combined)
        for unsupported_claim in ["production ready", "durably stored", "pinned and available", "slsa compliant"]:
            self.assertNotIn(unsupported_claim, combined)

    def test_static_forge_app_is_current_and_non_publishing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            generated = Path(tmpdir) / "forge-app.html"
            self.assertEqual(render_forge_app.main([str(generated)]), 0)
            self.assertEqual(generated.read_text(encoding="utf-8"), OUTPUT_FORGE_APP_HTML.read_text(encoding="utf-8"))

        html = OUTPUT_FORGE_APP_HTML.read_text(encoding="utf-8")
        self.assertIn("Decentralized Forge Workbench", html)
        self.assertIn("Issues & patches", html)
        self.assertIn("Nostr collaboration draft", html)
        self.assertIn("unsigned local draft", html)
        self.assertIn("no relay publish action", html)
        self.assertIn("Project set", html)
        self.assertIn("projectSetCommand", html)
        self.assertIn("loop43-nostr-issue-patch-readback", html)
        self.assertIn("selected-relay-issue-patch-readback-verified", html)

        data_match = re.search(
            r'<script id="forge-data" type="application/json">(.*?)</script>',
            html,
            re.S,
        )
        self.assertIsNotNone(data_match)
        app_data = json.loads(data_match.group(1))
        self.assertEqual(app_data["schema_version"], "decentralized-forge.static-app-data.v1")
        self.assertEqual(app_data["generated_from"]["output"], "output/forge-app.html")
        self.assertEqual(
            app_data["generated_from"]["registries"],
            ["fixtures/example-project.registry.json", "fixtures/portable-lab.registry.json"],
        )
        self.assertEqual(len(app_data["projects"]), 2)
        self.assertEqual(app_data["projects"][0]["registry"]["project"]["id"], "demo-project")
        self.assertEqual({item["type"] for item in app_data["live_nostr_collaboration"]}, {"issue", "patch"})
        self.assertEqual(len(app_data["live_nostr_collaboration"]), 2)
        self.assertEqual(app_data["live_evidence_index"]["loop"], 73)
        self.assertIn("static app does not publish protocol events", app_data["non_claims"])

        for forbidden_runtime in [
            "new WebSocket",
            "fetch(",
            "SimplePool",
            "finalizeEvent",
            "generateSecretKey",
            "pool.publish",
        ]:
            self.assertNotIn(forbidden_runtime, html)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, html.lower())

    def test_static_forge_app_can_import_onboarding_sample(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            generated = Path(tmpdir) / "forge-app-with-onboarding-sample.html"
            self.assertEqual(
                render_forge_app.main(
                    [
                        str(generated),
                        "--registry",
                        str(FIXTURE_PATH),
                        "--registry",
                        str(PORTABLE_FIXTURE_PATH),
                        "--registry",
                        str(ONBOARDING_SAMPLE_FIXTURE_PATH),
                    ]
                ),
                0,
            )
            self.assertEqual(
                generated.read_text(encoding="utf-8"),
                OUTPUT_FORGE_APP_WITH_ONBOARDING_HTML.read_text(encoding="utf-8"),
            )

        html = OUTPUT_FORGE_APP_WITH_ONBOARDING_HTML.read_text(encoding="utf-8")
        data_match = re.search(
            r'<script id="forge-data" type="application/json">(.*?)</script>',
            html,
            re.S,
        )
        self.assertIsNotNone(data_match)
        app_data = json.loads(data_match.group(1))
        project_ids = [project["registry"]["project"]["id"] for project in app_data["projects"]]
        self.assertEqual(project_ids, ["demo-project", "portable-lab", "onboarding-sample"])
        self.assertIn("Project set", html)
        self.assertIn("projectSetCommand", html)
        self.assertEqual(app_data["generated_from"]["output"], "output/forge-app-with-onboarding-sample.html")
        self.assertIn("fixtures/onboarding-sample.registry.json", app_data["generated_from"]["registries"])
        onboarding = [project for project in app_data["projects"] if project["registry"]["project"]["id"] == "onboarding-sample"][0]
        self.assertEqual(onboarding["summary"]["artifact_names"], ["onboarding-sample-artifact.txt"])
        self.assertIn("static app does not publish protocol events", app_data["non_claims"])
        for forbidden_runtime in [
            "new WebSocket",
            "fetch(",
            "SimplePool",
            "finalizeEvent",
            "generateSecretKey",
            "pool.publish",
        ]:
            self.assertNotIn(forbidden_runtime, html)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, html.lower())

    def test_verification_bundle_is_current_and_self_verifying(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            generated = Path(tmpdir) / "verification-bundle.zip"
            manifest = forge_registry.create_verification_bundle(generated)
            self.assertEqual(manifest["schema_version"], "decentralized-forge.verification-bundle.v1")
            self.assertEqual(generated.read_bytes(), OUTPUT_VERIFICATION_BUNDLE.read_bytes())

        self.assertEqual(forge_registry.verify_verification_bundle(OUTPUT_VERIFICATION_BUNDLE), [])
        self.assertEqual(forge_registry.verify_verification_bundle_cleanroom(OUTPUT_VERIFICATION_BUNDLE), [])
        report = forge_registry.bundle_report(OUTPUT_VERIFICATION_BUNDLE)
        self.assertTrue(report["verification"]["valid"])
        self.assertEqual(report["schema_version"], "decentralized-forge.bundle-report.v1")
        self.assertEqual(report["source_type"], "zip")
        self.assertEqual(report["evidence"]["entry_count"], len(self.live_evidence_index["evidence"]))
        self.assertEqual(
            {project["project"]["id"] for project in report["projects"]},
            {"demo-project", "portable-lab", "rad:zLoop4RadicleFixture1111111111111111111111111", "onboarding-sample"},
        )
        self.assertIn("bundle does not publish protocol events", report["non_claims"])
        self.assertIn("Durable storage", report["verification_gaps"][0])
        text_report = forge_registry.format_bundle_report(report)
        self.assertIn("Decentralized Forge bundle report", text_report)
        self.assertIn("demo-project: Demo Decentralized Forge Project", text_report)
        self.assertIn("selected_relay_readback", text_report)
        with tempfile.TemporaryDirectory() as tmpdir:
            extracted = Path(tmpdir) / "bundle"
            extracted.mkdir()
            self.assertEqual(forge_registry.safe_extract_bundle(OUTPUT_VERIFICATION_BUNDLE, extracted), [])
            extracted_report = forge_registry.bundle_report(extracted)
            self.assertTrue(extracted_report["verification"]["valid"])
            self.assertEqual(extracted_report["source_type"], "directory")
            self.assertEqual(extracted_report["bundle"], report["bundle"])
            self.assertEqual(extracted_report["evidence"], report["evidence"])
        with zipfile.ZipFile(OUTPUT_VERIFICATION_BUNDLE, "r") as archive:
            self.assertIn(forge_registry.DEFAULT_BUNDLE_MANIFEST_PATH, archive.namelist())
            manifest = json.loads(archive.read(forge_registry.DEFAULT_BUNDLE_MANIFEST_PATH).decode("utf-8"))
            self.assertEqual(manifest["file_count"], len(manifest["files"]))
            self.assertEqual(manifest["evidence_index"]["entry_count"], len(self.live_evidence_index["evidence"]))
            self.assertIn("bundle does not publish protocol events", manifest["non_claims"])
            self.assertIn(
                "python scripts/forge_registry.py verify-bundle-cleanroom output/decentralized-forge-verification-bundle.zip",
                manifest["suggested_verification_commands"],
            )
            self.assertIn(
                "python scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip",
                manifest["suggested_verification_commands"],
            )
            self.assertIn(
                "python scripts/forge_registry.py export-bundle-release-note output/decentralized-forge-verification-bundle.zip",
                manifest["suggested_verification_commands"],
            )
            self.assertIn(
                "python scripts/forge_registry.py radicle-retained-quickstart",
                manifest["suggested_verification_commands"],
            )
            payload_paths = {item["path"] for item in manifest["files"]}
            for expected_path in [
                "fixtures/example-project.registry.json",
                "fixtures/portable-lab.registry.json",
                "fixtures/onboarding-sample.registry.json",
                "fixtures/onboarding-sample-artifact.txt",
                "fixtures/live-evidence-index.json",
                "evidence/nostr-loop43-issue-patch-readback-2026-06-28.json",
                "output/demo-project.html",
                "output/portable-lab.html",
                "output/onboarding-sample.registry.html",
                "output/forge-app.html",
                "output/forge-app-with-onboarding-sample.html",
                "output/demo-project.summary.json",
                "output/portable-lab.summary.json",
                "output/onboarding-sample.registry.summary.json",
                "docs/radicle-persistent-seed-plan.md",
                "docs/radicle-retained-rid-quickstart.md",
                "docs/portable-bundle-review-checklist.md",
                "scripts/bootstrap_radicle_follower_seed.py",
                "scripts/forge_registry.py",
                "scripts/install_tcp_relay_user_service.py",
                "scripts/run_radicle_independent_availability_check.py",
                "scripts/run_radicle_seed_restart_check.py",
            ]:
                self.assertIn(expected_path, payload_paths)

            entries = {item["id"]: item for item in manifest["evidence_index"]["entries"]}
            self.assertEqual(set(entries), {item["id"] for item in self.live_evidence_index["evidence"]})
            for evidence_item in self.live_evidence_index["evidence"]:
                manifest_item = entries[evidence_item["id"]]
                self.assertEqual(manifest_item["evidence_file"], evidence_item["evidence_file"])
                self.assertEqual(manifest_item["evidence_sha256"], evidence_item["evidence_sha256"])
                self.assertEqual(manifest_item["evidence_size_bytes"], evidence_item["evidence_size_bytes"])

            manifest_blob = json.dumps(manifest, sort_keys=True).lower()
            for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
                self.assertNotIn(accidental_secret_marker, manifest_blob)

    def test_portable_bundle_review_checklist_preserves_release_boundaries(self):
        checklist = PORTABLE_BUNDLE_REVIEW_CHECKLIST.read_text(encoding="utf-8")
        for required_command in [
            "python scripts/forge_registry.py verify-bundle output/decentralized-forge-verification-bundle.zip",
            "python scripts/forge_registry.py verify-bundle-cleanroom output/decentralized-forge-verification-bundle.zip",
            "python scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip",
            "python scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip --json",
            "python scripts/forge_registry.py export-bundle-release-note output/decentralized-forge-verification-bundle.zip",
            "python scripts/forge_registry.py radicle-retained-quickstart",
            "python scripts/forge_registry.py verify-local --skip-npm-ci",
        ]:
            self.assertIn(required_command, checklist)
        for required_boundary in [
            "not a signed release",
            "no private key",
            "no durability",
            "censorship-resistance",
            "security guarantee",
            "SLSA compliance",
            "production-readiness",
        ]:
            self.assertIn(required_boundary, checklist)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, checklist.lower())

    def test_bundle_release_note_export_is_reviewable_and_secret_free(self):
        note = forge_registry.format_bundle_release_note(OUTPUT_VERIFICATION_BUNDLE)
        self.assertIn("# Decentralized Forge Portable Bundle Release Note", note)
        self.assertIn(f"- commit: `{self.current_git_head()}`", note)
        self.assertIn("- bundle_sha256: `", note)
        self.assertIn("- verification: `valid`", note)
        self.assertIn("python scripts/forge_registry.py verify-bundle output/decentralized-forge-verification-bundle.zip", note)
        self.assertIn("python scripts/forge_registry.py verify-bundle-cleanroom output/decentralized-forge-verification-bundle.zip", note)
        self.assertIn("python scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip --json", note)
        self.assertIn("Stop Conditions", note)
        self.assertIn("report-bundle` shows", note)
        self.assertIn("not a production forge", note)
        self.assertIn("not a production forge, signed release, durability proof", note)
        for project_id in ["demo-project", "portable-lab", "rad:zLoop4RadicleFixture1111111111111111111111111", "onboarding-sample"]:
            self.assertIn(project_id, note)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, note.lower())

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "bundle-release-note.md"
            exit_code = forge_registry.main([
                "export-bundle-release-note",
                str(OUTPUT_VERIFICATION_BUNDLE),
                str(output),
            ])
            self.assertEqual(exit_code, 0)
            self.assertEqual(output.read_text(encoding="utf-8"), f"{note}\n")

    def test_scaffold_registry_from_local_git_repo_is_valid_and_bounded(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "sample-widget"
            repo.mkdir()
            subprocess.run(["git", "init", "-b", "main"], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            (repo / "README.md").write_text("# Sample Widget\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md"], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Fixture Author",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "commit",
                    "-m",
                    "initial",
                ],
                cwd=repo,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            output = Path(tmpdir) / "sample-widget.registry.json"
            exit_code = forge_registry.main([
                "scaffold-registry",
                str(repo),
                str(output),
                "--project-id",
                "sample-widget",
                "--name",
                "Sample Widget",
            ])
            self.assertEqual(exit_code, 0)

            registry = json.loads(output.read_text(encoding="utf-8"))
            render_project_page.validate_registry(registry)
            self.assertEqual(registry["project"]["id"], "sample-widget")
            self.assertEqual(registry["project"]["name"], "Sample Widget")
            self.assertEqual(registry["project"]["default_branch"], "main")
            self.assertEqual(registry["clone_urls"][0]["transport"], "git")
            self.assertTrue(registry["clone_urls"][0]["url"].startswith("file://"))
            self.assertEqual(registry["maintainers"][0]["public_id"], "local-import-placeholder")
            self.assertEqual(registry["signature"]["status"], "unsigned-fixture")
            self.assertEqual(registry["verification_states"][0]["scope"], "registry.local_import_scaffold")
            self.assertFalse(registry["verification_states"][0]["live_verified"])
            combined = json.dumps(registry).lower()
            for required_boundary in ["no live protocol publication", "no live protocol", "no-artifact-cid", "not-pinned"]:
                self.assertIn(required_boundary, combined)
            for unsupported_claim in ["production ready", "durably stored", "pinned and available", "slsa compliant"]:
                self.assertNotIn(unsupported_claim, combined)
            guidance = forge_registry.scaffold_registry_guidance(output)
            self.assertIn(f"python scripts/forge_registry.py validate {output}", guidance[0])
            self.assertTrue(any("Review placeholder maintainer identity" in item for item in guidance))

    def test_attach_local_artifact_updates_scaffold_without_live_claims(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "artifact-widget"
            repo.mkdir()
            subprocess.run(["git", "init", "-b", "main"], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            (repo / "README.md").write_text("# Artifact Widget\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md"], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Fixture Author",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "commit",
                    "-m",
                    "initial",
                ],
                cwd=repo,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            registry_path = Path(tmpdir) / "artifact-widget.registry.json"
            artifact_path = Path(tmpdir) / "artifact-widget.txt"
            artifact_bytes = b"artifact bytes\nwith exact hashing\r\n"
            artifact_path.write_bytes(artifact_bytes)

            self.assertEqual(forge_registry.main(["scaffold-registry", str(repo), str(registry_path)]), 0)
            args = [
                "attach-local-artifact",
                str(registry_path),
                str(artifact_path),
                "--version",
                "0.1.0-local",
                "--tag",
                "v0.1.0-local",
                "--timestamp",
                "2026-06-29T00:00:00Z",
            ]
            self.assertEqual(forge_registry.main(args), 0)
            self.assertEqual(forge_registry.main(args), 0)

            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            render_project_page.validate_registry(registry)
            self.assertEqual(len(registry["releases"]), 1)
            release = registry["releases"][0]
            self.assertEqual(release["version"], "0.1.0-local")
            self.assertEqual(release["tag"], "v0.1.0-local")
            self.assertEqual(len(release["artifacts"]), 1)
            artifact = release["artifacts"][0]
            expected_sha256 = hashlib.sha256(artifact_bytes).hexdigest()
            self.assertEqual(artifact["name"], "artifact-widget.txt")
            self.assertEqual(artifact["media_type"], "text/plain")
            self.assertEqual(artifact["size_bytes"], len(artifact_bytes))
            self.assertEqual(artifact["sha256"], expected_sha256)
            self.assertEqual(artifact["hashes"]["sha256"], expected_sha256)
            self.assertTrue(artifact["uri"].startswith("file://"))
            self.assertEqual(artifact["signature"], "unsigned-local-artifact-metadata")
            self.assertEqual(artifact["attestation"], "absent")
            availability = artifact["availability"]
            self.assertTrue(availability["local_fixture"])
            self.assertFalse(availability["pinned"])
            self.assertFalse(availability["live_ipfs_verified"])
            self.assertFalse(availability["paid_storage"])
            self.assertFalse(availability["durability_claim"])
            self.assertIn("no IPFS add", availability["notes"])

            states = registry["verification_states"]
            self.assertEqual(sum(1 for state in states if state["scope"] == "registry.local_artifact_metadata"), 1)
            artifact_state = [state for state in states if state["scope"] == "registry.local_artifact_metadata"][0]
            self.assertEqual(artifact_state["state"], "local-fixture")
            self.assertFalse(artifact_state["live_verified"])
            self.assertFalse(artifact_state["synthetic"])
            self.assertIn(expected_sha256, artifact_state["evidence"])
            self.assertEqual(registry["updated_at"], "2026-06-29T00:00:00Z")
            self.assertEqual(registry["substrates"]["ipfs"]["pinning_status"], "not-pinned")
            self.assertFalse(registry["substrates"]["ipfs"]["live_ipfs_verified"])
            self.assertFalse(registry["substrates"]["ipfs"]["durability_claim"])
            combined = json.dumps(registry).lower()
            for required_boundary in ["local file metadata only", "no ipfs add", "no ipfs", "not-pinned"]:
                self.assertIn(required_boundary, combined)
            for unsupported_claim in ["production ready", "durably stored", "pinned and available", "slsa compliant"]:
                self.assertNotIn(unsupported_claim, combined)

    def test_onboard_local_project_chains_local_outputs_and_bundle_report(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "onboard-widget"
            repo.mkdir()
            subprocess.run(["git", "init", "-b", "main"], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            (repo / "README.md").write_text("# Onboard Widget\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md"], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Fixture Author",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "commit",
                    "-m",
                    "initial",
                ],
                cwd=repo,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            artifact_path = Path(tmpdir) / "onboard-widget.bin"
            artifact_bytes = b"\x00local onboarding artifact bytes\n"
            artifact_path.write_bytes(artifact_bytes)
            registry_path = Path(tmpdir) / "onboard-widget.registry.json"
            summary_path = Path(tmpdir) / "onboard-widget.summary.json"
            html_path = Path(tmpdir) / "onboard-widget.html"
            bundle_path = Path(tmpdir) / "verification-bundle.zip"
            report_path = Path(tmpdir) / "bundle-report.json"

            exit_code = forge_registry.main([
                "onboard-local-project",
                str(repo),
                str(artifact_path),
                "--registry",
                str(registry_path),
                "--summary",
                str(summary_path),
                "--html",
                str(html_path),
                "--bundle",
                str(bundle_path),
                "--report-json",
                str(report_path),
                "--project-id",
                "onboard-widget",
                "--project-name",
                "Onboard Widget",
                "--version",
                "0.2.0-local",
                "--tag",
                "v0.2.0-local",
                "--timestamp",
                "2026-06-29T00:00:00Z",
            ])
            self.assertEqual(exit_code, 0)

            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            render_project_page.validate_registry(registry)
            artifact = registry["releases"][0]["artifacts"][0]
            expected_sha256 = hashlib.sha256(artifact_bytes).hexdigest()
            self.assertEqual(registry["project"]["id"], "onboard-widget")
            self.assertEqual(registry["project"]["name"], "Onboard Widget")
            self.assertEqual(registry["releases"][0]["version"], "0.2.0-local")
            self.assertEqual(artifact["name"], "onboard-widget.bin")
            self.assertEqual(artifact["media_type"], "application/octet-stream")
            self.assertEqual(artifact["size_bytes"], len(artifact_bytes))
            self.assertEqual(artifact["sha256"], expected_sha256)
            self.assertTrue(artifact["uri"].startswith("file://"))

            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(summary["project"]["id"], "onboard-widget")
            self.assertEqual(summary["counts"]["artifacts"], 1)
            self.assertEqual(summary["artifact_names"], ["onboard-widget.bin"])
            html = html_path.read_text(encoding="utf-8")
            self.assertIn("Onboard Widget", html)
            self.assertIn("onboard-widget.bin", html)
            self.assertEqual(forge_registry.verify_verification_bundle(bundle_path), [])
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertTrue(report["verification"]["valid"])
            self.assertEqual(report["source"], str(bundle_path))
            combined = json.dumps({"registry": registry, "summary": summary, "report": report}).lower()
            for required_boundary in ["local registry scaffold only", "local file metadata only", "no ipfs add", "not-pinned"]:
                self.assertIn(required_boundary, combined)
            for unsupported_claim in ["production ready", "durably stored", "pinned and available", "slsa compliant"]:
                self.assertNotIn(unsupported_claim, combined)

    def test_live_gate_inventory_is_read_only_and_secret_free(self):
        payload = live_gate_inventory.inventory()
        self.assertEqual(payload["schema_version"], "decentralized-forge.live-gate-inventory.v1")
        self.assertEqual(payload["scope"], "local tool inventory only")
        self.assertEqual(
            set(payload["groups"]),
            {"ipfs_storage", "nostr", "radicle", "signing_provenance"},
        )
        combined = json.dumps(payload).lower()
        for required_non_action in [
            "no ipfs daemon was started",
            "no nostr event was signed",
            "no radicle node",
            "no signing key",
        ]:
            self.assertIn(required_non_action, combined)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, combined)

    def test_next_loop_controller_is_approval_bounded(self):
        controller = self.next_loop_controller
        self.assertEqual(
            controller["schema_version"],
            "decentralized-forge.next-loop-controller.v1",
        )
        self.assertEqual(controller["mode"], "approval-bounded")
        self.assertEqual(controller["max_iterations_per_run"], 1)
        self.assertIn("run_local_verification_suite", controller["approved_safe_actions"])
        self.assertEqual(controller["standing_live_approval"]["approved_by"], "user_chat_2026-06-28")

        approved_live = {
            action["id"]: action["scope"]
            for action in controller["standing_live_approval"]["approved_live_action_scope"]
        }
        for approved_gate in [
            "live_ipfs_storage_free_project_scoped",
            "radicle_disposable_public_network_checks",
            "nostr_disposable_publish_readback",
            "signing_provenance_disposable_or_keyless_test",
        ]:
            self.assertIn(approved_gate, approved_live)

        blocked = {gate["id"]: gate["requires"] for gate in controller["blocked_without_separate_approval"]}
        for required_gate in [
            "spending_or_paid_infrastructure",
            "production_private_keys",
            "direct_outreach",
            "persistent_public_seed_or_background_service",
            "stronger_claims",
        ]:
            self.assertIn(required_gate, blocked)
        combined = json.dumps(controller).lower()
        for forbidden_default in ["auto-push", "auto-publish", "auto-commit"]:
            self.assertNotIn(forbidden_default, combined)
        self.assertIn("wallet", combined)
        self.assertIn("production/private personal keys", combined)

    def test_next_loop_controller_plan_is_secret_free_and_non_live(self):
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "next_loop_controller.py"),
                "--plan-only",
                "--allow-dirty",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Next Loop Controller Report", result.stdout)
        self.assertIn("Approved live action scope", result.stdout)
        self.assertIn("Still blocked without separate approval", result.stdout)
        self.assertIn("Live IPFS, Radicle, Nostr, and signing actions are approved", result.stdout)
        self.assertIn("Still stop before spending", result.stdout)
        combined = result.stdout.lower()
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, combined)

    def test_next_loop_controller_workflow_is_manual_only(self):
        workflow = NEXT_LOOP_WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch", workflow)
        self.assertNotIn("schedule:", workflow)
        self.assertIn("python scripts/next_loop_controller.py --check --skip-npm-ci", workflow)
        self.assertNotIn("git push", workflow)
        self.assertNotIn("gh discussion", workflow)

    def test_ci_workflow_generates_keyless_attestations_for_release_artifacts(self):
        workflow = CI_WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn("id-token: write", workflow)
        self.assertIn("attestations: write", workflow)
        self.assertIn("artifact-metadata: write", workflow)
        self.assertIn("uses: actions/attest@v4", workflow)
        self.assertIn("if: github.event_name == 'push' && github.ref == 'refs/heads/main'", workflow)
        self.assertIn("npm run verify:helia", workflow)
        self.assertIn("python scripts/forge_registry.py render-app output/forge-app.html", workflow)
        self.assertIn("python scripts/forge_registry.py render-app output/forge-app-with-onboarding-sample.html --registry fixtures/example-project.registry.json --registry fixtures/portable-lab.registry.json --registry fixtures/onboarding-sample.registry.json", workflow)
        self.assertIn("python scripts/forge_registry.py export-bundle output/decentralized-forge-verification-bundle.zip", workflow)
        self.assertIn("python scripts/forge_registry.py verify-bundle output/decentralized-forge-verification-bundle.zip", workflow)
        self.assertIn("python scripts/forge_registry.py verify-bundle-cleanroom output/decentralized-forge-verification-bundle.zip", workflow)
        self.assertIn("python scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip --json", workflow)
        self.assertIn("python scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip --json --output output/onboarding-sample.bundle-report.json", workflow)
        self.assertIn("python scripts/forge_registry.py export-bundle-release-note output/decentralized-forge-verification-bundle.zip", workflow)
        for subject in [
            "output/demo-project.html",
            "output/forge-app.html",
            "output/forge-app-with-onboarding-sample.html",
            "output/portable-lab.html",
            "output/onboarding-sample.registry.html",
            "output/demo-project.summary.json",
            "output/portable-lab.summary.json",
            "output/onboarding-sample.registry.summary.json",
            "output/onboarding-sample.bundle-report.json",
            "output/decentralized-forge-verification-bundle.zip",
            "evidence/local-release-artifact-2026-06-22.car",
            "fixtures/local-release-artifact.txt",
            "fixtures/onboarding-sample-artifact.txt",
            "fixtures/onboarding-sample.registry.json",
        ]:
            self.assertIn(subject, workflow)

    def test_live_replay_checklist_is_secret_free_and_gated(self):
        checklist = self.live_replay_checklist
        self.assertEqual(
            checklist["schema_version"],
            "decentralized-forge.live-adapter-replay-checklist.v1",
        )
        self.assertGreaterEqual(checklist["loop"], 20)
        self.assertFalse(checklist["discovery"]["rad_found_in_loop_20"])
        self.assertFalse(checklist["discovery"]["rad_version_checked"])
        self.assertFalse(checklist["discovery"]["unsafe_installers_used"])
        self.assertFalse(checklist["discovery"]["network_protocol_actions_used"])
        self.assertEqual(
            checklist["radicle_local_replay"]["status_after_loop_20"],
            "blocked_no_approved_rad_binary_found",
        )
        self.assertEqual(checklist["nostr_disposable_readback"]["status_after_loop_20"], "planned_not_executed")

        if checklist["loop"] >= 21:
            self.assertTrue(checklist["discovery"]["rad_found_after_loop_21"])
            self.assertIn("rad 1.", checklist["discovery"]["rad_version_after_loop_21"])
            self.assertTrue(checklist["discovery"]["nak_found_after_loop_21"])
            self.assertIn("v0.", checklist["discovery"]["nak_version_after_loop_21"])
            self.assertEqual(
                checklist["radicle_local_replay"]["status_after_loop_21"],
                "tooling_installed_version_recorded_replay_not_executed",
            )
            nostr_gate = checklist["nostr_disposable_readback"]
            self.assertEqual(
                nostr_gate["status_after_loop_21"],
                "project_key_generated_offline_signed_event_verified_not_published",
            )
            self.assertRegex(nostr_gate["public_key_hex"], r"^[0-9a-f]{64}$")
            self.assertTrue(nostr_gate["public_key_npub"].startswith("npub1"))
            self.assertRegex(nostr_gate["offline_signature_event_id"], r"^[0-9a-f]{64}$")
            self.assertTrue(nostr_gate["local_signature_verified"])
            self.assertFalse(nostr_gate["relay_published_after_loop_21"])
            self.assertFalse(nostr_gate["relay_readback_after_loop_21"])

        if checklist["loop"] >= 22:
            discovery = checklist["discovery"]
            self.assertTrue(discovery["loop_22_preflight_recorded"])
            self.assertTrue(discovery["rad_version_checked_after_loop_22"])
            self.assertTrue(discovery["rad_help_checked_after_loop_22"])
            self.assertTrue(discovery["rad_init_help_checked_after_loop_22"])
            self.assertTrue(discovery["rad_inspect_help_checked_after_loop_22"])
            self.assertFalse(discovery["rad_status_command_available_after_loop_22"])
            self.assertFalse(discovery["network_protocol_actions_used_after_loop_22"])
            radicle_gate = checklist["radicle_local_replay"]
            self.assertEqual(
                radicle_gate["status_after_loop_22"],
                "preflight_help_inspected_replay_ready_under_permission_a_not_executed",
            )
            self.assertEqual(
                radicle_gate["preflight_evidence"],
                "evidence/radicle-local-replay-preflight-2026-06-22.md",
            )
            self.assertIn(
                "rad_init_with_no_confirm_no_seed_private_and_disposable_repo",
                radicle_gate["safe_local_replay_command_surface_after_loop_22"],
            )
            self.assertIn("rad_node_start", radicle_gate["forbidden_in_first_replay_after_loop_22"])
            self.assertFalse(radicle_gate["replay_executed_after_loop_22"])

        if checklist["loop"] >= 23:
            radicle_gate = checklist["radicle_local_replay"]
            self.assertEqual(
                radicle_gate["status_after_loop_23"],
                "local_cli_verified_private_no_seed_disposable_replay",
            )
            self.assertTrue(radicle_gate["replay_executed_after_loop_23"])
            self.assertEqual(
                radicle_gate["evidence_file_after_loop_23"],
                "evidence/radicle-local-replay-2026-06-22.md",
            )
            self.assertRegex(radicle_gate["local_rid_after_loop_23"], r"^rad:z[0-9A-Za-z]+$")
            self.assertTrue(radicle_gate["local_delegate_did_after_loop_23"].startswith("did:key:"))
            self.assertEqual(radicle_gate["visibility_after_loop_23"], "private")
            self.assertFalse(radicle_gate["seed_published_after_loop_23"])
            self.assertFalse(radicle_gate["node_started_after_loop_23"])
            self.assertFalse(radicle_gate["sync_or_announce_after_loop_23"])
            self.assertFalse(radicle_gate["remote_peer_config_after_loop_23"])
            self.assertFalse(radicle_gate["public_network_replication_verified_after_loop_23"])

        if checklist["loop"] >= 24:
            discovery = checklist["discovery"]
            self.assertTrue(discovery["loop_24_nostr_relay_selection_recorded"])
            self.assertFalse(discovery["network_protocol_actions_used_after_loop_24"])
            nostr_gate = checklist["nostr_disposable_readback"]
            self.assertEqual(
                nostr_gate["status_after_loop_24"],
                "relay_selected_payload_signed_locally_not_published",
            )
            self.assertEqual(
                nostr_gate["selected_relays_after_loop_24"],
                ["wss://relay.damus.io", "wss://nos.lol"],
            )
            self.assertTrue(nostr_gate["relay_info_checked_after_loop_24"])
            self.assertFalse(nostr_gate["relay_payment_required_after_loop_24"])
            self.assertFalse(nostr_gate["relay_auth_required_after_loop_24"])
            self.assertEqual(nostr_gate["event_kind_after_loop_24"], 30617)
            self.assertRegex(nostr_gate["signed_event_id_after_loop_24"], r"^[0-9a-f]{64}$")
            self.assertTrue(nostr_gate["local_signature_verified_after_loop_24"])
            self.assertFalse(nostr_gate["relay_published_after_loop_24"])
            self.assertFalse(nostr_gate["relay_readback_after_loop_24"])

        if checklist["loop"] >= 25:
            discovery = checklist["discovery"]
            self.assertTrue(discovery["loop_25_nostr_publish_readback_recorded"])
            self.assertTrue(discovery["network_protocol_actions_used_after_loop_25"])
            nostr_gate = checklist["nostr_disposable_readback"]
            self.assertEqual(
                nostr_gate["status_after_loop_25"],
                "published_and_read_back_from_selected_relays_with_disposable_project_key",
            )
            self.assertEqual(
                nostr_gate["event_id_after_loop_25"],
                nostr_gate["signed_event_id_after_loop_24"],
            )
            self.assertEqual(
                nostr_gate["published_relays_after_loop_25"],
                ["wss://relay.damus.io", "wss://nos.lol"],
            )
            self.assertEqual(
                nostr_gate["readback_verified_relays_after_loop_25"],
                ["wss://relay.damus.io", "wss://nos.lol"],
            )
            self.assertTrue(nostr_gate["relay_published_after_loop_25"])
            self.assertTrue(nostr_gate["relay_readback_after_loop_25"])
            self.assertTrue(nostr_gate["readback_field_match_after_loop_25"])
            self.assertTrue(nostr_gate["local_signature_verified_after_loop_25"])
            self.assertTrue(nostr_gate["readback_signature_verified_after_loop_25"])
            self.assertFalse(nostr_gate["production_or_personal_key_used_after_loop_25"])
            self.assertFalse(nostr_gate["paid_infrastructure_used_after_loop_25"])
            self.assertFalse(nostr_gate["direct_outreach_after_loop_25"])
            self.assertIn("no_durability_guarantee", nostr_gate["non_claims_after_loop_25"])

        if checklist["loop"] >= 28:
            discovery = checklist["discovery"]
            self.assertTrue(discovery["loop_28_nostr_readback_check_recorded"])
            self.assertTrue(discovery["network_protocol_actions_used_after_loop_28"])
            nostr_gate = checklist["nostr_disposable_readback"]
            self.assertEqual(
                nostr_gate["status_after_loop_28"],
                "readback_persistence_divergence_checked_no_new_publish",
            )
            self.assertEqual(
                nostr_gate["selected_relays_rechecked_after_loop_28"],
                ["wss://relay.damus.io", "wss://nos.lol"],
            )
            self.assertEqual(
                nostr_gate["extra_relays_checked_after_loop_28"],
                ["wss://relay.primal.net", "wss://nostr.wine"],
            )
            self.assertIn("wss://relay.primal.net", nostr_gate["readback_verified_relays_after_loop_28"])
            self.assertIn("wss://nostr.wine", nostr_gate["unmatched_relays_after_loop_28"])
            self.assertFalse(nostr_gate["new_event_published_after_loop_28"])
            self.assertFalse(nostr_gate["production_or_personal_key_used_after_loop_28"])
            self.assertFalse(nostr_gate["paid_infrastructure_used_after_loop_28"])
            self.assertFalse(nostr_gate["direct_outreach_after_loop_28"])

        if checklist["loop"] >= 29:
            discovery = checklist["discovery"]
            self.assertTrue(discovery["loop_29_nip34_live_event_import_recorded"])
            self.assertFalse(discovery["network_protocol_actions_used_after_loop_29"])
            nostr_gate = checklist["nostr_disposable_readback"]
            self.assertEqual(
                nostr_gate["status_after_loop_29"],
                "selected_relay_readback_evidence_imported_into_nip34_adapter_no_new_publish",
            )
            self.assertEqual(nostr_gate["live_readback_fixture_after_loop_29"], "fixtures/nostr-live-readback-events.json")
            self.assertFalse(nostr_gate["new_event_published_after_loop_29"])
            self.assertFalse(nostr_gate["relay_fetch_performed_after_loop_29"])
            self.assertIn("issue_event_readback_not_verified", nostr_gate["missing_nip34_semantics_after_loop_29"])
            self.assertFalse(nostr_gate["production_or_personal_key_used_after_loop_29"])
            self.assertFalse(nostr_gate["paid_infrastructure_used_after_loop_29"])
            self.assertFalse(nostr_gate["direct_outreach_after_loop_29"])

        if checklist["loop"] >= 30:
            discovery = checklist["discovery"]
            self.assertTrue(discovery["loop_30_radicle_public_network_preflight_recorded"])
            self.assertFalse(discovery["network_protocol_actions_used_after_loop_30"])
            radicle_gate = checklist["radicle_local_replay"]
            self.assertEqual(
                radicle_gate["status_after_loop_30"],
                "public_network_gate_preflight_help_inspected_permission_g_blocked",
            )
            self.assertEqual(
                radicle_gate["public_network_preflight_evidence_after_loop_30"],
                "evidence/radicle-public-network-preflight-2026-06-22.md",
            )
            self.assertEqual(
                radicle_gate["public_network_gate_plan_after_loop_30"],
                "docs/radicle-public-network-gate-plan.md",
            )
            self.assertTrue(radicle_gate["permission_f_preflight_completed_after_loop_30"])
            self.assertFalse(radicle_gate["permission_g_granted_after_loop_30"])
            self.assertFalse(radicle_gate["public_radicle_network_actions_after_loop_30"])
            self.assertFalse(radicle_gate["node_started_after_loop_30"])
            self.assertFalse(radicle_gate["publish_or_seed_after_loop_30"])
            self.assertFalse(radicle_gate["sync_or_announce_after_loop_30"])
            self.assertFalse(radicle_gate["remote_clone_or_fetch_after_loop_30"])
            self.assertIn("rad publish --help", radicle_gate["help_surfaces_inspected_after_loop_30"])
            self.assertIn("rad_clone_or_remote_fetch", radicle_gate["permission_g_forbidden_until_approved"])

        if checklist["loop"] >= 31:
            discovery = checklist["discovery"]
            self.assertTrue(discovery["loop_31_storage_preflight_recorded"])
            self.assertEqual(discovery["loop_31_storage_gate_plan"], "docs/public-storage-evidence-gate-plan.md")
            self.assertEqual(
                discovery["loop_31_storage_preflight_evidence"],
                "evidence/storage-tooling-preflight-2026-06-22.md",
            )
            self.assertFalse(discovery["storage_network_actions_used_after_loop_31"])
            self.assertFalse(discovery["paid_storage_or_wallet_actions_after_loop_31"])
            storage_gate = checklist["public_storage_preflight"]
            self.assertEqual(
                storage_gate["status_after_loop_31"],
                "preflight_inventory_and_plan_complete_no_live_storage",
            )
            self.assertTrue(storage_gate["permission_h_preflight_completed_after_loop_31"])
            self.assertFalse(storage_gate["installed_ipfs_or_car_tooling_after_loop_31"])
            self.assertFalse(storage_gate["ipfs_add_or_fetch_after_loop_31"])
            self.assertFalse(storage_gate["ipfs_daemon_started_after_loop_31"])
            self.assertFalse(storage_gate["car_file_created_after_loop_31"])
            self.assertFalse(storage_gate["package_installed_after_loop_31"])
            self.assertFalse(storage_gate["public_gateway_checked_after_loop_31"])
            self.assertFalse(storage_gate["paid_pinning_after_loop_31"])
            self.assertFalse(storage_gate["filecoin_or_arweave_wallet_used_after_loop_31"])
            self.assertFalse(storage_gate["paid_storage_used_after_loop_31"])
            self.assertFalse(storage_gate["durability_claim_after_loop_31"])
            self.assertEqual(
                storage_gate["local_fixture_cid_v1_raw_base32"],
                "bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua",
            )
            package_names = {pkg["package"] for pkg in storage_gate["read_only_package_metadata_checked_after_loop_31"]}
            self.assertIn("ipfs-car", package_names)
            self.assertIn("@ipld/car", package_names)

        if checklist["loop"] >= 33:
            discovery = checklist["discovery"]
            self.assertTrue(discovery["loop_33_local_car_cid_fixture_recorded"])
            self.assertEqual(
                discovery["loop_33_local_car_cid_evidence"],
                "evidence/local-car-cid-fixture-2026-06-22.json",
            )
            self.assertFalse(discovery["storage_network_actions_used_after_loop_33"])
            self.assertFalse(discovery["paid_storage_or_wallet_actions_after_loop_33"])
            storage_gate = checklist["public_storage_preflight"]
            self.assertEqual(
                storage_gate["status_after_loop_33"],
                "local_car_cid_fixture_verified_with_project_scoped_lockfile_dependencies",
            )
            self.assertTrue(storage_gate["permission_i_local_car_cid_completed_after_loop_33"])
            self.assertEqual(
                storage_gate["local_car_cid_evidence_after_loop_33"],
                "evidence/local-car-cid-fixture-2026-06-22.json",
            )
            self.assertEqual(storage_gate["lockfile_after_loop_33"], "package-lock.json")
            self.assertTrue(storage_gate["package_installed_after_loop_33"])
            self.assertTrue(storage_gate["car_file_created_after_loop_33"])
            self.assertEqual(
                storage_gate["car_root_cid_after_loop_33"],
                "bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua",
            )
            self.assertEqual(storage_gate["car_block_count_after_loop_33"], 1)
            self.assertTrue(storage_gate["car_block_bytes_match_input_after_loop_33"])
            self.assertTrue(storage_gate["verification_passed_after_loop_33"])
            self.assertFalse(storage_gate["ipfs_add_or_fetch_after_loop_33"])
            self.assertFalse(storage_gate["ipfs_daemon_started_after_loop_33"])
            self.assertFalse(storage_gate["public_gateway_checked_after_loop_33"])
            self.assertFalse(storage_gate["paid_pinning_after_loop_33"])
            self.assertFalse(storage_gate["filecoin_or_arweave_wallet_used_after_loop_33"])
            self.assertFalse(storage_gate["paid_storage_used_after_loop_33"])
            self.assertFalse(storage_gate["durability_claim_after_loop_33"])

        if checklist["loop"] >= 34:
            discovery = checklist["discovery"]
            self.assertTrue(discovery["loop_34_radicle_public_network_smoke_recorded"])
            self.assertEqual(
                discovery["loop_34_radicle_public_network_smoke_evidence"],
                "evidence/radicle-public-network-smoke-2026-06-22.json",
            )
            self.assertTrue(discovery["network_protocol_actions_used_after_loop_34"])
            radicle_gate = checklist["radicle_local_replay"]
            self.assertEqual(
                radicle_gate["status_after_loop_34"],
                "disposable_public_radicle_seed_and_remote_clone_smoke_verified",
            )
            self.assertTrue(radicle_gate["permission_g_public_smoke_completed_after_loop_34"])
            self.assertEqual(
                radicle_gate["public_network_smoke_evidence_after_loop_34"],
                "evidence/radicle-public-network-smoke-2026-06-22.json",
            )
            self.assertRegex(radicle_gate["public_smoke_rid_after_loop_34"], r"^rad:z[0-9A-Za-z]+$")
            self.assertEqual(radicle_gate["visibility_after_loop_34"], "public")
            self.assertTrue(radicle_gate["node_started_after_loop_34"])
            self.assertTrue(radicle_gate["publish_or_public_init_after_loop_34"])
            self.assertTrue(radicle_gate["seed_policy_updated_after_loop_34"])
            self.assertTrue(radicle_gate["sync_or_announce_after_loop_34"])
            self.assertTrue(radicle_gate["clone_node_started_after_loop_34"])
            self.assertTrue(radicle_gate["clone_node_connected_to_seed_after_loop_34"])
            self.assertTrue(radicle_gate["remote_clone_or_fetch_after_loop_34"])
            self.assertTrue(radicle_gate["readback_matches_after_loop_34"])
            self.assertTrue(radicle_gate["verification_passed_after_loop_34"])
            self.assertTrue(radicle_gate["temporary_state_removed_after_loop_34"])
            self.assertFalse(radicle_gate["production_or_personal_key_used_after_loop_34"])
            self.assertFalse(radicle_gate["paid_infrastructure_used_after_loop_34"])
            self.assertFalse(radicle_gate["direct_outreach_after_loop_34"])
            self.assertIn("no_broad_radicle_network_availability_claim", radicle_gate["non_claims_after_loop_34"])

        if checklist["loop"] >= 35:
            discovery = checklist["discovery"]
            self.assertTrue(discovery["loop_35_consolidation_recorded"])
            self.assertEqual(
                discovery["loop_35_consolidation_evidence"],
                "evidence/loop35-consolidation-2026-06-22.md",
            )
            self.assertFalse(discovery["new_network_or_storage_actions_after_loop_35"])
            self.assertFalse(discovery["new_cron_jobs_after_loop_35"])
            consolidation = checklist["loop_35_consolidation"]
            self.assertEqual(
                consolidation["status"],
                "complete_as_docs_context_status_checklist_test_consolidation",
            )
            self.assertTrue((ROOT / consolidation["evidence"]).exists())
            self.assertEqual(
                consolidation["consolidated_loop_33_evidence"],
                "evidence/local-car-cid-fixture-2026-06-22.json",
            )
            self.assertEqual(
                consolidation["consolidated_loop_34_evidence"],
                "evidence/radicle-public-network-smoke-2026-06-22.json",
            )
            self.assertFalse(consolidation["new_public_protocol_action"])
            self.assertFalse(consolidation["new_storage_network_action"])
            self.assertFalse(consolidation["new_public_update_posted"])
            self.assertFalse(consolidation["new_cron_jobs_created"])
            self.assertIn("paid_storage_or_wallet_actions", consolidation["remaining_gates"])
            self.assertIn("preserves all non-claims", consolidation["claim_boundary"])

        required_global_gates = {
            "approved_tooling_path_required",
            "temporary_or_disposable_state_only",
            "no_production_or_private_personal_keys",
            "no_spending_or_paid_infrastructure",
            "no_public_seed_publishing_by_default",
            "no_relay_publishing_or_signing_until_prerequisites_met",
            "no_direct_outreach",
            "no_unsupported_security_censorship_durability_or_production_claims",
        }
        self.assertLessEqual(required_global_gates, set(checklist["global_gates"]))
        self.assertIn("use_temp_RAD_HOME", checklist["radicle_local_replay"]["required_before_replay"])
        self.assertIn(
            "disposable_project_scoped_key_storage_documented_without_secret_values",
            checklist["nostr_disposable_readback"]["required_before_publish"],
        )
        self.assertFalse(checklist["secrets_policy"]["contains_secret_values"])
        forbidden_blob = json.dumps(checklist).lower()
        for forbidden in ["secret_key", "seed_phrase", "production_private", "paid_service_token"]:
            self.assertIn(forbidden, forbidden_blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, forbidden_blob)

    def test_loop21_offline_nostr_proof_is_public_and_unpublished(self):
        checklist = self.live_replay_checklist
        if checklist["loop"] < 21:
            self.skipTest("Loop 21 Nostr proof not recorded yet")
        nostr_gate = checklist["nostr_disposable_readback"]
        proof_path = ROOT / nostr_gate["offline_signature_proof"]
        proof = json.loads(proof_path.read_text(encoding="utf-8"))
        self.assertEqual(proof["id"], nostr_gate["offline_signature_event_id"])
        self.assertEqual(proof["pubkey"], nostr_gate["public_key_hex"])
        self.assertEqual(proof["kind"], 1)
        self.assertIn("Not published to any relay", proof["content"])
        proof_blob = json.dumps(proof).lower()
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, proof_blob)

    def test_loop23_radicle_local_replay_evidence_is_bounded(self):
        checklist = self.live_replay_checklist
        if checklist["loop"] < 23:
            self.skipTest("Loop 23 Radicle replay evidence not recorded yet")
        radicle_gate = checklist["radicle_local_replay"]
        evidence_path = ROOT / radicle_gate["evidence_file_after_loop_23"]
        evidence = evidence_path.read_text(encoding="utf-8")
        self.assertIn(radicle_gate["local_rid_after_loop_23"], evidence)
        self.assertIn(radicle_gate["local_delegate_did_after_loop_23"], evidence)
        self.assertIn("local CLI verification only", evidence)
        self.assertIn("No `rad node start`", evidence)
        self.assertIn("No secret values are recorded here", evidence)
        evidence_blob = evidence.lower()
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, evidence_blob)

    def test_loop30_radicle_public_network_preflight_is_help_only(self):
        checklist = self.live_replay_checklist
        if checklist["loop"] < 30:
            self.skipTest("Loop 30 Radicle public-network preflight not recorded yet")
        radicle_gate = checklist["radicle_local_replay"]
        evidence_path = ROOT / radicle_gate["public_network_preflight_evidence_after_loop_30"]
        plan_path = ROOT / radicle_gate["public_network_gate_plan_after_loop_30"]
        evidence = evidence_path.read_text(encoding="utf-8")
        plan = plan_path.read_text(encoding="utf-8")
        self.assertIn("Permission F only", evidence)
        self.assertIn("No Radicle identity was created or reused", evidence)
        self.assertIn("rad publish --help", evidence)
        self.assertIn("rad clone --help", evidence)
        self.assertIn("Permission G was granted and one disposable smoke is complete", plan)
        self.assertIn("Further Radicle public-network actions", plan)
        self.assertIn("exact Loop 34 disposable public seed/clone/readback smoke", plan)
        combined = f"{evidence}\n{plan}".lower()
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, combined)

    def test_loop31_storage_preflight_is_plan_only(self):
        checklist = self.live_replay_checklist
        if checklist["loop"] < 31:
            self.skipTest("Loop 31 storage/IPFS preflight not recorded yet")
        storage_gate = checklist["public_storage_preflight"]
        evidence_path = ROOT / storage_gate["storage_preflight_evidence_after_loop_31"]
        plan_path = ROOT / storage_gate["storage_gate_plan_after_loop_31"]
        evidence = evidence_path.read_text(encoding="utf-8")
        plan = plan_path.read_text(encoding="utf-8")
        self.assertIn("Permission H only", evidence)
        self.assertIn("`command -v ipfs` | missing", evidence)
        self.assertIn("`ipfs-car` | `3.1.0`", evidence)
        self.assertIn("No package install was performed", evidence)
        self.assertIn("No IPFS add/fetch/pin", evidence)
        self.assertIn("Loop 33 candidate: local CAR/CID fixture verification", plan)
        self.assertIn("live_ipfs_verified", plan)
        self.assertIn("paid pinning", plan.lower())
        self.assertIn("would not prove paid pinning", plan)
        combined = f"{evidence}\n{plan}".lower()
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, combined)

    def test_loop33_local_car_cid_fixture_evidence_is_bounded(self):
        checklist = self.live_replay_checklist
        if checklist["loop"] < 33:
            self.skipTest("Loop 33 local CAR/CID evidence not recorded yet")
        storage_gate = checklist["public_storage_preflight"]
        evidence_path = ROOT / storage_gate["local_car_cid_evidence_after_loop_33"]
        car_path = ROOT / storage_gate["local_car_file_after_loop_33"]
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))

        self.assertEqual(evidence["schema_version"], "decentralized-forge.local-car-cid-fixture.v1")
        self.assertEqual(evidence["loop"], 33)
        self.assertTrue(evidence["verification_passed"])
        self.assertEqual(evidence["input_artifact"], "fixtures/local-release-artifact.txt")
        self.assertEqual(evidence["input_size_bytes"], LOCAL_RELEASE_ARTIFACT_PATH.stat().st_size)
        self.assertEqual(evidence["input_sha256"], hashlib.sha256(LOCAL_RELEASE_ARTIFACT_PATH.read_bytes()).hexdigest())
        self.assertEqual(evidence["cid"], storage_gate["car_root_cid_after_loop_33"])
        self.assertEqual(evidence["car_root_cids"], [storage_gate["car_root_cid_after_loop_33"]])
        self.assertEqual(evidence["car_block_count"], 1)
        self.assertTrue(evidence["car_root_matches_cid"])
        self.assertTrue(evidence["car_block_cid_matches"])
        self.assertTrue(evidence["car_block_bytes_match_input"])
        self.assertEqual(evidence["dependencies"]["@ipld/car"], "5.4.6")
        self.assertEqual(evidence["dependencies"]["multiformats"], "14.0.0")
        self.assertEqual(evidence["lockfile"], "package-lock.json")
        self.assertTrue(car_path.is_file())
        self.assertEqual(car_path.stat().st_size, evidence["car_size_bytes"])

        evidence_blob = json.dumps(evidence).lower()
        for action_not_taken in [
            "no ipfs daemon was started",
            "no ipfs add/fetch/pin command was run",
            "no public gateway was queried",
            "no wallet, filecoin, arweave, paid pinning, or paid storage action was used",
        ]:
            self.assertIn(action_not_taken, evidence_blob)
        for required_non_claim in [
            "no durability",
            "global availability",
            "censorship-resistance",
            "security",
            "production-readiness",
        ]:
            self.assertIn(required_non_claim, evidence_blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, evidence_blob)

    def test_loop41_helia_local_ipfs_add_get_evidence_is_bounded(self):
        evidence = json.loads(HELIA_LOCAL_EVIDENCE_PATH.read_text(encoding="utf-8"))

        self.assertEqual(evidence["schema_version"], "decentralized-forge.helia-local-ipfs-add-get.v1")
        self.assertEqual(evidence["loop"], 41)
        self.assertEqual(evidence["scope"], "local Helia/IPFS UnixFS add-get verification only")
        self.assertTrue(evidence["verification_passed"])
        self.assertEqual(evidence["input_artifact"], "fixtures/local-release-artifact.txt")
        self.assertEqual(evidence["input_size_bytes"], LOCAL_RELEASE_ARTIFACT_PATH.stat().st_size)
        self.assertEqual(evidence["input_sha256"], hashlib.sha256(LOCAL_RELEASE_ARTIFACT_PATH.read_bytes()).hexdigest())
        self.assertEqual(evidence["local_unixfs_cid"], evidence["loop_33_raw_cid"])
        self.assertEqual(evidence["local_unixfs_cid"], "bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua")
        self.assertEqual(evidence["readback_size_bytes"], evidence["input_size_bytes"])
        self.assertTrue(evidence["readback_bytes_match_input"])
        self.assertTrue(evidence["readback_sha256_matches_input"])
        self.assertEqual(evidence["dependencies"]["helia"], "6.1.4")
        self.assertEqual(evidence["dependencies"]["@helia/unixfs"], "7.2.1")
        self.assertEqual(evidence["lockfile"], "package-lock.json")
        self.assertFalse(evidence["contains_secret_values"])
        self.assertFalse(evidence["private_keys_used"])
        self.assertFalse(evidence["paid_infrastructure_used"])
        self.assertFalse(evidence["public_gateway_queried"])
        self.assertFalse(evidence["pinned"])
        self.assertFalse(evidence["helia_started"])
        self.assertFalse(evidence["persistent_daemon_started"])
        self.assertFalse(evidence["durability_claim"])
        self.assertFalse(evidence["production_readiness_claim"])

        evidence_blob = json.dumps(evidence).lower()
        for action_not_taken in [
            "no public gateway was queried",
            "no public pinning service was used",
            "no paid storage, filecoin, arweave, wallet, or spending action was used",
            "no persistent ipfs/kubo daemon",
        ]:
            self.assertIn(action_not_taken, evidence_blob)
        for required_non_claim in [
            "no durability",
            "global availability",
            "censorship-resistance",
            "security",
            "production-readiness",
        ]:
            self.assertIn(required_non_claim, evidence_blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, evidence_blob)

    def test_loop42_public_gateway_pinning_preflight_is_bounded(self):
        evidence = json.loads(PUBLIC_GATEWAY_PREFLIGHT_PATH.read_text(encoding="utf-8"))

        self.assertEqual(evidence["schema_version"], "decentralized-forge.public-gateway-pinning-preflight.v1")
        self.assertEqual(evidence["loop"], 42)
        self.assertTrue(evidence["verification_passed"])
        self.assertTrue(evidence["public_gateway_queried"])
        self.assertEqual(evidence["cid"], "bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua")
        self.assertEqual(evidence["input_sha256"], hashlib.sha256(LOCAL_RELEASE_ARTIFACT_PATH.read_bytes()).hexdigest())
        self.assertEqual(len(evidence["gateways"]), 3)
        self.assertEqual(evidence["successful_gateway_readback_count"], 0)
        self.assertFalse(evidence["pinning_preflight"]["pinning_provider_selected"])
        self.assertFalse(evidence["pinning_preflight"]["account_or_token_used"])
        self.assertFalse(evidence["pinning_preflight"]["pin_request_sent"])
        self.assertFalse(evidence["paid_infrastructure_used"])
        self.assertFalse(evidence["wallet_used"])
        self.assertFalse(evidence["durability_claim"])

        evidence_blob = json.dumps(evidence).lower()
        for required in [
            "no pinning provider account or token was used",
            "no ipfs daemon or persistent service was started",
            "does not prove durability",
            "successful_gateway_readback_count",
        ]:
            self.assertIn(required, evidence_blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:", "api_token"]:
            self.assertNotIn(accidental_secret_marker, evidence_blob)

    def test_loop43_nostr_issue_patch_readback_evidence_is_bounded(self):
        evidence = json.loads(NOSTR_ISSUE_PATCH_READBACK_PATH.read_text(encoding="utf-8"))

        self.assertEqual(evidence["schema_version"], "decentralized-forge.nostr-issue-patch-readback.v1")
        self.assertEqual(evidence["loop"], 43)
        self.assertTrue(evidence["verification_passed"])
        self.assertEqual(evidence["tool"]["package"], "nostr-tools")
        self.assertEqual(evidence["tool"]["version"], "2.23.8")
        self.assertEqual(evidence["source_fixture"], "fixtures/nostr-collaboration-events.json")
        self.assertEqual(evidence["event_count"], 2)
        self.assertEqual({event["kind"] for event in evidence["events"]}, {1621, 1617})
        self.assertEqual(set(evidence["accepted_relays"]), {"wss://relay.damus.io", "wss://nos.lol"})
        self.assertEqual(set(evidence["readback_verified_relays"]), {"wss://relay.damus.io", "wss://nos.lol"})
        self.assertFalse(evidence["private_keys_recorded"])
        self.assertFalse(evidence["production_or_personal_key_used"])
        for event in evidence["events"]:
            self.assertRegex(event["id"], r"^[0-9a-f]{64}$")
            self.assertRegex(event["pubkey"], r"^[0-9a-f]{64}$")
            self.assertTrue(event["local_signature_verified"])
            self.assertTrue(any(item["ok"] for item in event["publish"]))
            self.assertTrue(any(item["matched"] and item["verify_readback"] for item in event["readback"]))

        evidence_blob = json.dumps(evidence).lower()
        for required in [
            "no secret key material is recorded",
            "not proof of global propagation",
            "not proof of full nip-34 or forge protocol compatibility",
            "production-readiness",
        ]:
            self.assertIn(required, evidence_blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, evidence_blob)

    def test_loop44_radicle_broader_check_records_current_blocker(self):
        evidence = json.loads(RADICLE_BROADER_CHECK_PATH.read_text(encoding="utf-8"))

        self.assertEqual(evidence["schema_version"], "decentralized-forge.radicle-broader-check.v1")
        self.assertEqual(evidence["loop"], 44)
        self.assertTrue(evidence["verification_passed"])
        self.assertEqual(evidence["target_prior_disposable_rid"], "rad:z2WtozFrCRhygh9CGzyUN57CN7Nwa")
        self.assertFalse(evidence["rad_cli"]["available"])
        self.assertIn("spawnSync rad ENOENT", evidence["rad_cli"]["error"])
        self.assertEqual(len(evidence["web_route_probes"]), 3)
        self.assertEqual(len(evidence["direct_node_probes"]), 3)
        self.assertFalse(evidence["cli_broader_clone_or_sync_executed"])
        self.assertFalse(evidence["private_keys_used"])
        self.assertFalse(evidence["paid_infrastructure_used"])
        self.assertFalse(evidence["persistent_service_started"])
        self.assertIn("rad CLI is not available", evidence["finding"])

        evidence_blob = json.dumps(evidence).lower()
        for required in [
            "no radicle identity was created or reused",
            "no rad node, seed, publish, sync, clone, connect, or remote command was run",
            "does not prove broader radicle availability",
        ]:
            self.assertIn(required, evidence_blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:", "passphrase"]:
            self.assertNotIn(accidental_secret_marker, evidence_blob)

    def test_loop59_radicle_project_repo_smoke_is_bounded(self):
        evidence = json.loads(RADICLE_PROJECT_REPO_SMOKE_PATH.read_text(encoding="utf-8"))

        self.assertEqual(evidence["schema_version"], "decentralized-forge.radicle-project-repo-smoke.v1")
        self.assertEqual(evidence["loop"], 59)
        self.assertTrue(evidence["verification_passed"])
        self.assertRegex(evidence["rid"], r"^rad:z[0-9A-Za-z]+$")
        self.assertEqual(evidence["visibility"], "public")
        self.assertEqual(evidence["source_commit"], evidence["seed_repo_commit"])
        self.assertEqual(evidence["source_commit"], evidence["clone_commit"])
        self.assertTrue(evidence["node_started"])
        self.assertTrue(evidence["publish_succeeded"])
        self.assertTrue(evidence["seed_succeeded"])
        self.assertTrue(evidence["sync_succeeded"])
        self.assertTrue(evidence["clone_node_started"])
        self.assertTrue(evidence["clone_node_connected_to_seed"])
        self.assertTrue(evidence["remote_clone_succeeded"])
        self.assertTrue(evidence["readback_commit_matches_source"])

        evidence_blob = json.dumps(evidence).lower()
        for required in [
            "current decentralized-forge commit",
            "separate temporary radicle profile",
            "global replication",
            "broad radicle network availability claim",
            "production-readiness",
        ]:
            self.assertIn(required, evidence_blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:", "api_token"]:
            self.assertNotIn(accidental_secret_marker, evidence_blob)

    def test_loop60_radicle_fresh_readback_check_is_bounded(self):
        evidence = json.loads(RADICLE_FRESH_READBACK_CHECK_PATH.read_text(encoding="utf-8"))

        self.assertEqual(evidence["schema_version"], "decentralized-forge.radicle-fresh-readback-check.v1")
        self.assertEqual(evidence["loop"], 60)
        self.assertTrue(evidence["verification_passed"])
        self.assertEqual(evidence["source_evidence"], "evidence/radicle-project-repo-smoke-2026-06-29.json")
        self.assertEqual(evidence["target_rid"], "rad:zWGy1Ssjb7tBbwDbdGLqeHCsUqwr")
        self.assertEqual(evidence["expected_commit"], evidence["clone_commit"])
        self.assertFalse(evidence["original_seed_profile_reused"])
        self.assertFalse(evidence["explicit_original_seed_used"])
        self.assertTrue(evidence["node_started"])
        self.assertTrue(evidence["clone_succeeded"])
        self.assertTrue(evidence["readback_commit_matches_expected"])
        self.assertTrue(evidence["fresh_network_readback_observed"])

        command_words = json.dumps([command["cmd"] for command in evidence["commands"]]).lower()
        self.assertNotIn("node connect", command_words)
        self.assertNotIn("--seed", command_words)

        evidence_blob = json.dumps(evidence).lower()
        for required in [
            "fresh temporary radicle profile",
            "no original loop 59 rad_home or seed repository was reused",
            "no explicit connection to the original loop 59 seed node was requested",
            "normal network path",
            "not a durability",
        ]:
            self.assertIn(required, evidence_blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:", "api_token"]:
            self.assertNotIn(accidental_secret_marker, evidence_blob)

    def test_loop61_radicle_update_continuity_check_is_bounded(self):
        evidence = json.loads(RADICLE_UPDATE_CONTINUITY_CHECK_PATH.read_text(encoding="utf-8"))

        self.assertEqual(evidence["schema_version"], "decentralized-forge.radicle-update-continuity-check.v1")
        self.assertEqual(evidence["loop"], 61)
        self.assertTrue(evidence["verification_completed"])
        self.assertTrue(evidence["verification_passed"])
        self.assertEqual(evidence["source_evidence"], "evidence/radicle-fresh-readback-check-2026-06-29.json")
        self.assertEqual(evidence["target_rid"], "rad:zWGy1Ssjb7tBbwDbdGLqeHCsUqwr")
        self.assertTrue(evidence["current_extends_prior_recorded_commit"])
        self.assertFalse(evidence["original_loop59_seed_profile_reused"])
        self.assertFalse(evidence["original_loop59_delegate_key_available"])
        self.assertTrue(evidence["clone_succeeded"])
        self.assertEqual(evidence["clone_prior_commit"], evidence["prior_recorded_commit"])
        self.assertEqual(evidence["post_import_commit"], evidence["current_source_commit"])
        self.assertTrue(evidence["push_attempted"])
        self.assertTrue(evidence["push_succeeded"])
        self.assertRegex(evidence["push_remote"], r"^rad://zWGy1Ssjb7tBbwDbdGLqeHCsUqwr/z6[0-9A-Za-z]+$")
        self.assertTrue(evidence["current_commit_pushed_to_same_rid_peer_namespace"])
        self.assertTrue(evidence["sync_after_push_succeeded"])
        self.assertTrue(evidence["readback_clone_succeeded"])
        self.assertEqual(evidence["readback_commit"], evidence["prior_recorded_commit"])
        self.assertFalse(evidence["same_rid_current_commit_readback_observed"])
        self.assertTrue(evidence["default_readback_remained_original_delegate_commit"])
        self.assertFalse(evidence["likely_delegate_authority_blocked_update"])

        evidence_blob = json.dumps(evidence).lower()
        for required in [
            "fresh identity published the current commit",
            "default fresh clone still checked out the original delegate main",
            "no original loop 59 rad_home, seed repository, or delegate private key was reused",
            "does not prove the project is immutable",
            "no full radicle compatibility claim",
        ]:
            self.assertIn(required, evidence_blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:", "api_token"]:
            self.assertNotIn(accidental_secret_marker, evidence_blob)

    def test_loop62_radicle_retained_delegate_check_is_bounded(self):
        evidence = json.loads(RADICLE_RETAINED_DELEGATE_CHECK_PATH.read_text(encoding="utf-8"))

        self.assertEqual(evidence["schema_version"], "decentralized-forge.radicle-retained-delegate-check.v1")
        self.assertEqual(evidence["loop"], 62)
        self.assertTrue(evidence["verification_passed"])
        self.assertEqual(evidence["state_root_shape"], ".tmp/radicle-retained-delegate (gitignored; not committed; not bundled)")
        self.assertFalse(evidence["secret_values_recorded"])
        self.assertFalse(evidence["passphrase_file_created_this_run"])
        self.assertFalse(evidence["auth_profile_created_this_run"])
        self.assertFalse(evidence["initialized_new_rid"])
        self.assertTrue(evidence["retained_state_reused"])
        self.assertEqual(evidence["prior_rid"], evidence["rid"])
        self.assertRegex(evidence["rid"], r"^rad:z[0-9A-Za-z]+$")
        self.assertRegex(evidence["delegate_did"], r"^did:key:z6[0-9A-Za-z]+$")
        self.assertRegex(evidence["retained_peer_id"], r"^z6[0-9A-Za-z]+$")
        self.assertEqual(evidence["retained_node_id"], evidence["retained_peer_id"])
        self.assertEqual(evidence["source_commit"], evidence["worktree_commit"])
        self.assertTrue(evidence["worktree_matches_source"])
        self.assertEqual(evidence["visibility"], "public")
        self.assertTrue(evidence["push_succeeded"])
        self.assertTrue(evidence["node_started"])
        self.assertTrue(evidence["publish_succeeded"])
        self.assertTrue(evidence["seed_succeeded"])
        self.assertTrue(evidence["inventory_sync_succeeded"])
        self.assertTrue(evidence["sync_succeeded"])
        self.assertTrue(evidence["readback_node_started"])
        self.assertTrue(evidence["readback_clone_succeeded"])
        self.assertEqual(evidence["readback_commit"], evidence["source_commit"])
        self.assertTrue(evidence["default_readback_matches_source"])
        self.assertTrue(evidence["direct_seed_node_connect_succeeded"])
        self.assertTrue(evidence["direct_seed_clone_succeeded"])
        self.assertEqual(evidence["direct_seed_readback_commit"], evidence["source_commit"])
        self.assertTrue(evidence["direct_seed_readback_matches_source"])

        evidence_blob = json.dumps(evidence).lower()
        for required in [
            "gitignored",
            "no secret passphrase or radicle key material was written to committed evidence",
            "future default public-routing availability",
            "not a durability",
            "no full radicle compatibility claim",
        ]:
            self.assertIn(required, evidence_blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:", "api_token"]:
            self.assertNotIn(accidental_secret_marker, evidence_blob)

    def test_loop63_radicle_retained_update_check_is_bounded(self):
        evidence = json.loads(RADICLE_RETAINED_UPDATE_CHECK_PATH.read_text(encoding="utf-8"))

        self.assertEqual(evidence["schema_version"], "decentralized-forge.radicle-retained-update-check.v1")
        self.assertEqual(evidence["loop"], 63)
        self.assertTrue(evidence["verification_passed"])
        self.assertEqual(evidence["source_evidence"], "evidence/radicle-retained-delegate-check-2026-06-29.json")
        self.assertEqual(evidence["target_rid"], "rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy")
        self.assertEqual(evidence["observed_rid"], evidence["target_rid"])
        self.assertTrue(evidence["same_retained_rid"])
        self.assertNotEqual(evidence["prior_recorded_commit"], evidence["current_source_commit"])
        self.assertEqual(evidence["prior_recorded_commit"], evidence["prior_default_readback_commit"])
        self.assertTrue(evidence["current_extends_prior_recorded_commit"])
        self.assertTrue(evidence["advanced_from_prior_recorded_commit"])
        self.assertEqual(evidence["state_root_shape"], "<retained-state-root> (local host/WSL state; not committed; not bundled)")
        self.assertFalse(evidence["secret_values_recorded"])
        self.assertFalse(evidence["passphrase_file_created_this_run"])
        self.assertTrue(evidence["retained_profile_available"])
        self.assertRegex(evidence["delegate_did"], r"^did:key:z6[0-9A-Za-z]+$")
        self.assertRegex(evidence["retained_peer_id"], r"^z6[0-9A-Za-z]+$")
        self.assertEqual(evidence["retained_node_id"], evidence["retained_peer_id"])
        self.assertEqual(evidence["worktree_commit"], evidence["current_source_commit"])
        self.assertTrue(evidence["worktree_matches_source"])
        self.assertEqual(evidence["visibility"], "public")
        self.assertTrue(evidence["push_succeeded"])
        self.assertTrue(evidence["node_started"])
        self.assertTrue(evidence["publish_succeeded"])
        self.assertTrue(evidence["seed_succeeded"])
        self.assertTrue(evidence["inventory_sync_succeeded"])
        self.assertFalse(evidence["sync_succeeded"])
        self.assertTrue(evidence["readback_node_started"])
        self.assertFalse(evidence["readback_clone_succeeded"])
        self.assertEqual(evidence["readback_commit"], "")
        self.assertFalse(evidence["default_readback_matches_source"])
        self.assertTrue(evidence["direct_seed_node_connect_succeeded"])
        self.assertTrue(evidence["direct_seed_clone_succeeded"])
        self.assertEqual(evidence["direct_seed_readback_commit"], evidence["current_source_commit"])
        self.assertTrue(evidence["direct_seed_readback_matches_source"])

        evidence_blob = json.dumps(evidence).lower()
        for required in [
            "same-rid update",
            "gitignored project-scoped radicle maintainer state advanced the same rid",
            "no secret passphrase or radicle key material was written to committed evidence",
            "no future default public-routing availability claim",
            "not a durability",
        ]:
            self.assertIn(required, evidence_blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:", "api_token"]:
            self.assertNotIn(accidental_secret_marker, evidence_blob)

    def test_loop65_radicle_independent_availability_check_is_bounded(self):
        prior = json.loads(RADICLE_RETAINED_UPDATE_CHECK_PATH.read_text(encoding="utf-8"))
        evidence = json.loads(RADICLE_INDEPENDENT_AVAILABILITY_CHECK_PATH.read_text(encoding="utf-8"))

        self.assertEqual(evidence["schema_version"], "decentralized-forge.radicle-independent-availability-check.v1")
        self.assertEqual(evidence["loop"], 65)
        self.assertTrue(evidence["verification_passed"])
        self.assertEqual(evidence["source_evidence"], "evidence/radicle-retained-update-check-2026-06-29.json")
        self.assertEqual(evidence["target_rid"], prior["target_rid"])
        self.assertEqual(evidence["observed_rid"], evidence["target_rid"])
        self.assertTrue(evidence["same_retained_rid"])
        self.assertEqual(evidence["prior_verified_commit"], prior["current_source_commit"])
        self.assertNotEqual(evidence["prior_verified_commit"], evidence["current_source_commit"])
        self.assertTrue(evidence["current_extends_prior_verified_commit"])
        self.assertTrue(evidence["advanced_from_prior_verified_commit"])
        self.assertEqual(evidence["state_root_shape"], "<retained-state-root> (local host/WSL state; not committed; not bundled)")
        self.assertIn("/tmp/df-radicle-independent-availability-*", evidence["reader_state_shape"])
        self.assertFalse(evidence["secret_values_recorded"])
        self.assertFalse(evidence["retained_passphrase_file_created_this_run"])
        self.assertTrue(evidence["retained_profile_available"])
        self.assertEqual(evidence["retained_node_id"], evidence["retained_peer_id"])
        self.assertEqual(evidence["worktree_commit"], evidence["current_source_commit"])
        self.assertTrue(evidence["worktree_matches_source"])
        self.assertEqual(evidence["visibility"], "public")
        self.assertTrue(evidence["push_succeeded"])
        self.assertTrue(evidence["maintainer_node_started"])
        self.assertTrue(evidence["publish_succeeded"])
        self.assertTrue(evidence["maintainer_seed_succeeded"])
        self.assertTrue(evidence["reader_a_node_started"])
        self.assertTrue(evidence["reader_a_connected_to_maintainer"])
        self.assertTrue(evidence["reader_a_clone_succeeded"])
        self.assertEqual(evidence["reader_a_readback_commit"], evidence["current_source_commit"])
        self.assertTrue(evidence["reader_a_readback_matches_source"])
        self.assertTrue(evidence["follower_seed_succeeded"])
        self.assertTrue(evidence["follower_sync_succeeded"])
        self.assertTrue(evidence["reader_b_node_started"])
        self.assertTrue(evidence["reader_b_connected_to_follower"])
        self.assertTrue(evidence["reader_b_clone_succeeded"])
        self.assertEqual(evidence["reader_b_readback_commit"], evidence["current_source_commit"])
        self.assertTrue(evidence["reader_b_readback_matches_source"])

        evidence_blob = json.dumps(evidence).lower()
        for required in [
            "independent follower-seed readback",
            "reader a cloned from the retained maintainer seed",
            "reader b",
            "no persistent public seed service was kept running after verification",
            "no future default public-routing availability claim",
        ]:
            self.assertIn(required, evidence_blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:", "api_token"]:
            self.assertNotIn(accidental_secret_marker, evidence_blob)

    def test_loop66_radicle_seed_restart_check_is_bounded(self):
        prior = json.loads(RADICLE_INDEPENDENT_AVAILABILITY_CHECK_PATH.read_text(encoding="utf-8"))
        evidence = json.loads(RADICLE_SEED_RESTART_CHECK_PATH.read_text(encoding="utf-8"))

        self.assertEqual(evidence["schema_version"], "decentralized-forge.radicle-seed-restart-check.v1")
        self.assertEqual(evidence["loop"], 66)
        self.assertTrue(evidence["verification_passed"])
        self.assertEqual(evidence["source_evidence"], "evidence/radicle-independent-availability-check-2026-06-29.json")
        self.assertEqual(evidence["target_rid"], prior["target_rid"])
        self.assertEqual(evidence["observed_rid"], evidence["target_rid"])
        self.assertTrue(evidence["same_retained_rid"])
        self.assertEqual(evidence["prior_verified_commit"], prior["current_source_commit"])
        self.assertNotEqual(evidence["prior_verified_commit"], evidence["current_source_commit"])
        self.assertTrue(evidence["current_extends_prior_verified_commit"])
        self.assertTrue(evidence["advanced_from_prior_verified_commit"])
        self.assertEqual(evidence["state_root_shape"], "<retained-state-root> (local host/WSL state; not committed; not bundled)")
        self.assertIn("/tmp/df-radicle-seed-restart-*", evidence["reader_state_shape"])
        self.assertEqual(evidence["seed_listen_addr"], "127.0.0.1:8799")
        self.assertFalse(evidence["seed_address_publicly_reachable"])
        self.assertFalse(evidence["separate_host_readback_observed"])
        self.assertFalse(evidence["secret_values_recorded"])
        self.assertFalse(evidence["retained_passphrase_file_created_this_run"])
        self.assertTrue(evidence["retained_profile_available"])
        self.assertEqual(evidence["retained_peer_id"], evidence["first_seed_node_id"])
        self.assertEqual(evidence["retained_peer_id"], evidence["restart_seed_node_id"])
        self.assertTrue(evidence["first_seed_node_started"])
        self.assertTrue(evidence["first_seed_policy_succeeded"])
        self.assertTrue(evidence["first_reader"]["node_started"])
        self.assertTrue(evidence["first_reader"]["connected_to_seed"])
        self.assertTrue(evidence["first_reader"]["clone_succeeded"])
        self.assertEqual(evidence["first_reader"]["readback_commit"], evidence["current_source_commit"])
        self.assertTrue(evidence["first_reader"]["readback_matches_source"])
        self.assertTrue(evidence["stop_after_first_succeeded"])
        self.assertTrue(evidence["restart_seed_node_started"])
        self.assertTrue(evidence["restart_seed_policy_succeeded"])
        self.assertTrue(evidence["same_seed_node_after_restart"])
        self.assertTrue(evidence["second_reader"]["node_started"])
        self.assertTrue(evidence["second_reader"]["connected_to_seed"])
        self.assertTrue(evidence["second_reader"]["clone_succeeded"])
        self.assertEqual(evidence["second_reader"]["readback_commit"], evidence["current_source_commit"])
        self.assertTrue(evidence["second_reader"]["readback_matches_source"])
        self.assertTrue(evidence["final_stop_succeeded"])
        self.assertFalse(evidence["persistent_seed_service_left_running"])
        self.assertEqual(evidence["worktree_commit"], evidence["current_source_commit"])
        self.assertTrue(evidence["worktree_matches_source"])
        self.assertEqual(evidence["visibility"], "public")
        self.assertTrue(evidence["push_succeeded"])
        self.assertTrue(evidence["publish_succeeded"])

        evidence_blob = json.dumps(evidence).lower()
        for required in [
            "restartable retained-rid radicle seed rehearsal",
            "fresh reader cloned before seed restart",
            "another fresh reader cloned after the retained seed restarted",
            "no public firewall/router/nat change was made",
            "no separate-host or separate-network readback was observed",
            "no persistent public seed service was left running after verification",
        ]:
            self.assertIn(required, evidence_blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:", "api_token"]:
            self.assertNotIn(accidental_secret_marker, evidence_blob)

    def test_loop67_radicle_vps_follower_public_readback_is_bounded(self):
        prior = json.loads(RADICLE_SEED_RESTART_CHECK_PATH.read_text(encoding="utf-8"))
        evidence = json.loads(RADICLE_VPS_FOLLOWER_PUBLIC_READBACK_PATH.read_text(encoding="utf-8"))

        self.assertEqual(evidence["schema_version"], "decentralized-forge.radicle-vps-follower-public-readback.v1")
        self.assertEqual(evidence["loop"], 67)
        self.assertTrue(evidence["verification_passed"])
        self.assertEqual(evidence["source_evidence"], "evidence/radicle-seed-restart-check-2026-06-29.json")
        self.assertEqual(evidence["target_rid"], prior["target_rid"])
        self.assertEqual(evidence["expected_commit"], "610fc3da9757d0cb123aa5976db552b991b766d4")
        self.assertEqual(evidence["vps_host"], "openclaw")
        self.assertEqual(evidence["vps_public_ip"], "187.77.19.162")
        self.assertEqual(
            evidence["vps_seed_address"],
            "z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776",
        )
        self.assertTrue(evidence["vps_seed_left_running"])
        self.assertTrue(evidence["public_seed_address_reachable"])
        self.assertTrue(evidence["coordinator_tcp_test_succeeded"])
        self.assertTrue(evidence["ubuntu_work_tcp_test_succeeded"])
        self.assertFalse(evidence["retained_state_copied_to_vps"])
        self.assertTrue(evidence["vps_follower_clone_from_retained_seed_succeeded"])
        self.assertEqual(evidence["vps_follower_readback_commit"], evidence["expected_commit"])
        self.assertTrue(evidence["vps_follower_readback_matches_expected"])
        self.assertTrue(evidence["temporary_bridge_used_for_vps_bootstrap"])
        self.assertTrue(evidence["temporary_bridge_stopped_after_bootstrap"])
        self.assertTrue(evidence["maintainer_seed_stopped_after_bootstrap"])
        self.assertEqual(evidence["fresh_reader_host"], "ubuntu-work")
        self.assertIn("/tmp/df-openclaw-public-readback-*", evidence["fresh_reader_state_shape"])
        self.assertTrue(evidence["fresh_reader_connected_to_public_seed"])
        self.assertTrue(evidence["fresh_reader_clone_succeeded"])
        self.assertEqual(evidence["fresh_reader_readback_commit"], evidence["expected_commit"])
        self.assertTrue(evidence["fresh_reader_readback_matches_expected"])
        self.assertFalse(evidence["secret_values_recorded"])

        evidence_blob = json.dumps(evidence).lower()
        for required in [
            "public vps follower-seed readback",
            "retained maintainer key material was not copied to the vps",
            "fresh reader on ubuntu-work connected to openclaw",
            "not a permanent durability",
        ]:
            self.assertIn(required, evidence_blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:", "api_token"]:
            self.assertNotIn(accidental_secret_marker, evidence_blob)

    def test_loop68_radicle_vps_follower_systemd_service_is_bounded(self):
        evidence = json.loads(RADICLE_VPS_FOLLOWER_SYSTEMD_SERVICE_PATH.read_text(encoding="utf-8"))
        health = json.loads(RADICLE_PUBLIC_SEED_HEALTH_CHECK_PATH.read_text(encoding="utf-8"))

        self.assertEqual(evidence["schema_version"], "decentralized-forge.radicle-vps-follower-systemd-service.v1")
        self.assertEqual(evidence["loop"], 68)
        self.assertEqual(evidence["rid"], "rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy")
        self.assertEqual(evidence["expected_commit"], "610fc3da9757d0cb123aa5976db552b991b766d4")
        self.assertEqual(evidence["service"]["manager"], "systemd --user")
        self.assertEqual(evidence["service"]["name"], "decentralized-forge-radicle-seed.service")
        self.assertTrue(evidence["service"]["enabled"])
        self.assertTrue(evidence["service"]["active_after_restart"])
        self.assertEqual(evidence["service"]["restart_policy"], "always")
        self.assertTrue(evidence["service"]["linger_enabled"])
        self.assertFalse(evidence["secret_handling"]["secret_values_recorded"])
        self.assertFalse(evidence["secret_handling"]["retained_maintainer_key_material_copied_to_vps"])
        self.assertTrue(evidence["verification"]["systemd_restart_succeeded"])
        self.assertEqual(evidence["verification"]["post_restart_public_readback_commit"], evidence["expected_commit"])
        self.assertTrue(evidence["verification"]["post_restart_public_readback_matches_expected"])
        self.assertTrue(health["verification_passed"])
        self.assertEqual(health["readback_commit"], evidence["expected_commit"])

        blob = json.dumps(evidence).lower()
        for required in ["restart-safe user systemd service", "retained maintainer key material was not copied", "not a permanent durability"]:
            self.assertIn(required, blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:", "api_token"]:
            self.assertNotIn(accidental_secret_marker, blob)

    def test_loop69_public_seed_health_check_is_bounded(self):
        evidence = json.loads(RADICLE_PUBLIC_SEED_HEALTH_CHECK_PATH.read_text(encoding="utf-8"))

        self.assertEqual(evidence["schema_version"], "decentralized-forge.public-radicle-seed-health-check.v1")
        self.assertTrue(evidence["verification_passed"])
        self.assertTrue(evidence["auth_succeeded"])
        self.assertTrue(evidence["node_started"])
        self.assertTrue(evidence["connected_to_seed"])
        self.assertTrue(evidence["clone_succeeded"])
        self.assertEqual(evidence["expected_commit"], "610fc3da9757d0cb123aa5976db552b991b766d4")
        self.assertEqual(evidence["readback_commit"], evidence["expected_commit"])
        self.assertTrue(evidence["readback_matches_expected"])
        self.assertEqual(evidence["temp_state"], "removed")
        self.assertFalse(evidence["secret_values_recorded"])
        self.assertEqual(evidence["node_stop"]["returncode"], 0)

        blob = json.dumps(evidence).lower()
        for required in ["fresh local radicle profile", "not a durability", "default public-routing"]:
            self.assertIn(required, blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:", "api_token"]:
            self.assertNotIn(accidental_secret_marker, blob)

    def test_loop70_public_seed_update_propagation_is_bounded(self):
        prior = json.loads(RADICLE_VPS_FOLLOWER_PUBLIC_READBACK_PATH.read_text(encoding="utf-8"))
        evidence = json.loads(RADICLE_PUBLIC_SEED_UPDATE_PROPAGATION_PATH.read_text(encoding="utf-8"))
        health = json.loads(RADICLE_PUBLIC_SEED_UPDATE_HEALTH_CHECK_PATH.read_text(encoding="utf-8"))

        self.assertEqual(evidence["schema_version"], "decentralized-forge.radicle-public-seed-update-propagation.v1")
        self.assertEqual(evidence["loop"], 70)
        self.assertEqual(evidence["rid"], prior["target_rid"])
        self.assertEqual(evidence["prior_public_seed_commit"], prior["expected_commit"])
        self.assertEqual(evidence["updated_commit"], "64efbada294d4a57c014a27398b92e344c6d68aa")
        self.assertTrue(evidence["retained_update"]["seed_restart_script_passed"])
        self.assertTrue(evidence["retained_update"]["retained_rid_advanced_to_updated_commit"])
        self.assertTrue(evidence["vps_sync"]["temporary_bridge_used"])
        self.assertTrue(evidence["vps_sync"]["temporary_bridge_stopped"])
        self.assertTrue(evidence["vps_sync"]["maintainer_seed_stopped_after_sync"])
        self.assertTrue(evidence["vps_sync"]["vps_sync_from_retained_maintainer_seed_succeeded"])
        self.assertEqual(evidence["vps_sync"]["vps_local_clone_readback_commit"], evidence["updated_commit"])
        self.assertTrue(evidence["vps_sync"]["vps_local_clone_readback_matches_updated_commit"])
        self.assertTrue(evidence["public_readback"]["fresh_reader_connected_to_public_seed"])
        self.assertEqual(evidence["public_readback"]["fresh_reader_readback_commit"], evidence["updated_commit"])
        self.assertTrue(evidence["public_readback"]["fresh_reader_readback_matches_updated_commit"])
        self.assertTrue(evidence["public_readback"]["fresh_reader_temp_state_removed"])
        self.assertTrue(evidence["verification_passed"])
        self.assertFalse(evidence["secret_values_recorded"])
        self.assertFalse(evidence["retained_maintainer_key_material_copied_to_vps"])
        self.assertTrue(health["verification_passed"])
        self.assertEqual(health["readback_commit"], evidence["updated_commit"])

        blob = json.dumps(evidence).lower()
        for required in [
            "temporary maintainer-seed bridge",
            "automatic future propagation",
            "retained maintainer key material was not copied",
        ]:
            self.assertIn(required, blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:", "api_token"]:
            self.assertNotIn(accidental_secret_marker, blob)

    def test_loop71_external_health_timer_is_bounded(self):
        evidence = json.loads(RADICLE_EXTERNAL_HEALTH_TIMER_PATH.read_text(encoding="utf-8"))
        latest = json.loads(RADICLE_EXTERNAL_HEALTH_TIMER_LATEST_PATH.read_text(encoding="utf-8"))

        self.assertEqual(evidence["schema_version"], "decentralized-forge.radicle-external-health-timer.v1")
        self.assertEqual(evidence["loop"], 71)
        self.assertEqual(evidence["rid"], "rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy")
        self.assertEqual(evidence["expected_commit"], "ef16e2ad39d3e13bdcc9d454443c5bbb17733c68")
        self.assertEqual(evidence["health_host"], "ubuntu-work")
        self.assertEqual(evidence["service"]["manager"], "systemd --user")
        self.assertTrue(evidence["service"]["timer_active"])
        self.assertTrue(evidence["service"]["timer_enabled"])
        self.assertTrue(evidence["service"]["persistent"])
        self.assertTrue(evidence["verification"]["forced_timer_service_run_succeeded"])
        self.assertTrue(evidence["verification"]["latest_json_exists"])
        self.assertTrue(evidence["verification"]["latest_verification_passed"])
        self.assertEqual(evidence["verification"]["latest_readback_commit"], evidence["expected_commit"])
        self.assertTrue(evidence["verification"]["latest_readback_matches_expected"])
        self.assertFalse(evidence["secret_values_recorded"])
        self.assertTrue(latest["verification_passed"])
        self.assertEqual(latest["readback_commit"], evidence["expected_commit"])
        self.assertEqual(latest["temp_state"], "removed")

        blob = json.dumps(evidence).lower() + json.dumps(latest).lower()
        for required in ["external scheduled public radicle seed health check", "automatic repair", "not proof of durability"]:
            self.assertIn(required, blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:", "api_token"]:
            self.assertNotIn(accidental_secret_marker, blob)

    def test_loop72_public_seed_update_to_hardening_commit_is_bounded(self):
        evidence = json.loads(RADICLE_PUBLIC_SEED_UPDATE_EF16E2A_PATH.read_text(encoding="utf-8"))
        health = json.loads(RADICLE_PUBLIC_SEED_UPDATE_EF16E2A_HEALTH_CHECK_PATH.read_text(encoding="utf-8"))

        self.assertEqual(evidence["schema_version"], "decentralized-forge.radicle-public-seed-update-propagation.v1")
        self.assertEqual(evidence["loop"], 72)
        self.assertEqual(evidence["prior_public_seed_commit"], "64efbada294d4a57c014a27398b92e344c6d68aa")
        self.assertEqual(evidence["updated_commit"], "ef16e2ad39d3e13bdcc9d454443c5bbb17733c68")
        self.assertTrue(evidence["retained_update"]["seed_restart_script_passed"])
        self.assertTrue(evidence["vps_sync"]["temporary_bridge_stopped"])
        self.assertTrue(evidence["vps_sync"]["maintainer_seed_stopped_after_sync"])
        self.assertTrue(evidence["vps_sync"]["vps_sync_succeeded"])
        self.assertEqual(evidence["vps_sync"]["vps_local_clone_readback_commit"], evidence["updated_commit"])
        self.assertTrue(evidence["public_readback"]["fresh_reader_connected_to_public_seed"])
        self.assertEqual(evidence["public_readback"]["fresh_reader_readback_commit"], evidence["updated_commit"])
        self.assertTrue(evidence["public_readback"]["fresh_reader_readback_matches_updated_commit"])
        self.assertTrue(evidence["verification_passed"])
        self.assertFalse(evidence["secret_values_recorded"])
        self.assertFalse(evidence["retained_maintainer_key_material_copied_to_vps"])
        self.assertTrue(health["verification_passed"])
        self.assertEqual(health["readback_commit"], evidence["updated_commit"])

        blob = json.dumps(evidence).lower()
        for required in ["hardening commit", "automatic future propagation", "retained maintainer key material was not copied"]:
            self.assertIn(required, blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:", "api_token"]:
            self.assertNotIn(accidental_secret_marker, blob)

    def test_loop73_second_follower_seed_tailnet_readback_is_bounded(self):
        bootstrap = json.loads(RADICLE_UBUNTU_WORK_FOLLOWER_BOOTSTRAP_PATH.read_text(encoding="utf-8"))
        health = json.loads(RADICLE_SECOND_SEED_TAILNET_HEALTH_PATH.read_text(encoding="utf-8"))

        self.assertEqual(bootstrap["schema_version"], "decentralized-forge.radicle-follower-seed-bootstrap.v1")
        self.assertEqual(bootstrap["rid"], "rad:z3Q8ePG6Qs4PQi1SWf9BEzDayENcy")
        self.assertEqual(bootstrap["expected_commit"], "ef16e2ad39d3e13bdcc9d454443c5bbb17733c68")
        self.assertEqual(bootstrap["readback_commit"], bootstrap["expected_commit"])
        self.assertTrue(bootstrap["readback_matches_expected"])
        self.assertEqual(bootstrap["seed_policy_scope"], "all")
        self.assertEqual(bootstrap["node_id"], "z6MksRdjzuN2VYV4HTXdVSchitJ8Bq1zbx8WhBb3KhyfSm6A")
        self.assertEqual(bootstrap["listen"], "127.0.0.1:8877")
        self.assertFalse(bootstrap["left_running"])
        self.assertFalse(bootstrap["secret_values_recorded"])

        self.assertEqual(health["schema_version"], "decentralized-forge.public-radicle-seed-health-check.v1")
        self.assertEqual(health["seed"], "z6MksRdjzuN2VYV4HTXdVSchitJ8Bq1zbx8WhBb3KhyfSm6A@100.83.206.66:8877")
        self.assertEqual(health["rid"], bootstrap["rid"])
        self.assertEqual(health["expected_commit"], bootstrap["expected_commit"])
        self.assertTrue(health["auth_succeeded"])
        self.assertTrue(health["node_started"])
        self.assertTrue(health["connected_to_seed"])
        self.assertTrue(health["clone_succeeded"])
        self.assertEqual(health["readback_commit"], health["expected_commit"])
        self.assertTrue(health["readback_matches_expected"])
        self.assertTrue(health["verification_passed"])
        self.assertEqual(health["temp_state"], "removed")
        self.assertFalse(health["secret_values_recorded"])

        blob = json.dumps(bootstrap).lower() + json.dumps(health).lower()
        self.assertIn("not a durability", blob)
        self.assertIn("production-readiness claim", blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:", "api_token"]:
            self.assertNotIn(accidental_secret_marker, blob)

    def test_radicle_retained_quickstart_is_evidence_bounded(self):
        evidence = json.loads(RADICLE_PUBLIC_SEED_UPDATE_EF16E2A_PATH.read_text(encoding="utf-8"))
        model = forge_registry.retained_radicle_quickstart_model()
        rendered = forge_registry.format_retained_radicle_quickstart(model)

        self.assertEqual(model["schema_version"], "decentralized-forge.radicle-retained-quickstart.v1")
        self.assertEqual(model["source_evidence_id"], "loop72-radicle-public-seed-update-ef16e2a")
        self.assertEqual(model["source_evidence_file"], "evidence/radicle-public-seed-update-ef16e2a-2026-06-29.json")
        self.assertEqual(model["rid"], evidence["rid"])
        self.assertEqual(model["expected_commit"], evidence["updated_commit"])
        self.assertEqual(model["readback_commit"], evidence["public_readback"]["fresh_reader_readback_commit"])
        self.assertEqual(model["availability_mode"], "public VPS follower-seed update readback")
        self.assertTrue(model["follower_seed_succeeded"])
        self.assertFalse(model["seed_restart_verified"])
        self.assertTrue(model["persistent_seed_service_left_running"])
        self.assertTrue(model["seed_address_publicly_reachable"])
        self.assertFalse(model["default_public_routing_observed"])
        self.assertFalse(model["retained_state_committed"])
        self.assertFalse(model["secret_values_recorded"])
        self.assertIn(f"rad node connect {evidence['vps_seed_address']} --timeout 30s", model["commands"])
        self.assertIn(
            f"rad clone --timeout 120s --seed {evidence['vps_seed_node_id']} {evidence['rid']} decentralized-forge",
            model["commands"],
        )
        self.assertIn(f"git rev-parse HEAD prints {evidence['updated_commit']}", model["expected_verification"])
        for required_nonclaim in [
            "not a default public-routing claim",
            "not a durability guarantee",
            "not a committed secret or key backup",
            "not maintainer key material on the VPS",
            "not proof of automatic future update propagation",
        ]:
            self.assertIn(required_nonclaim, model["non_claims"])
            self.assertIn(required_nonclaim, rendered)

        self.assertIn("Retained Radicle direct-seed quickstart", rendered)
        self.assertIn(evidence["rid"], rendered)
        self.assertIn(evidence["updated_commit"], rendered)
        self.assertIn(evidence["vps_seed_address"], rendered)
        self.assertIn("availability mode: `public VPS follower-seed update readback`", rendered)
        self.assertIn("follower seed succeeded in evidence: `true`", rendered)
        self.assertIn("public seed address observed: `true`", rendered)
        self.assertIn("persistent seed service left running: `true`", rendered)
        self.assertIn("default public routing observed: `false`", rendered)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "radicle-retained-quickstart.md"
            exit_code = forge_registry.main(["radicle-retained-quickstart", str(output)])
            self.assertEqual(exit_code, 0)
            self.assertEqual(output.read_text(encoding="utf-8"), f"{rendered}\n")

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "radicle-retained-quickstart.json"
            exit_code = forge_registry.main(["radicle-retained-quickstart", str(output), "--json"])
            self.assertEqual(exit_code, 0)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), model)

        combined = json.dumps(model).lower() + rendered.lower()
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:", "api_token"]:
            self.assertNotIn(accidental_secret_marker, combined)

    def test_radicle_retained_rid_quickstart_doc_matches_latest_availability(self):
        evidence = json.loads(RADICLE_PUBLIC_SEED_UPDATE_EF16E2A_PATH.read_text(encoding="utf-8"))
        doc = RADICLE_RETAINED_RID_QUICKSTART.read_text(encoding="utf-8")

        self.assertIn("python scripts/forge_registry.py radicle-retained-quickstart", doc)
        self.assertIn(evidence["rid"], doc)
        self.assertIn(evidence["updated_commit"], doc)
        self.assertIn(evidence["vps_seed_address"], doc)
        self.assertIn("evidence/radicle-public-seed-update-ef16e2a-2026-06-29.json", doc)
        self.assertIn(f"rad node connect {evidence['vps_seed_address']} --timeout 30s", doc)
        self.assertIn(
            f"rad clone --timeout 120s --seed {evidence['vps_seed_node_id']} {evidence['rid']} decentralized-forge",
            doc,
        )
        for required_boundary in [
            "Loop 72 proved a public direct-seed update readback",
            "not a durability guarantee",
            "not proof of automatic future update propagation",
            "not proof of broad Radicle network availability",
            "not production readiness",
            "not maintainer key material on the VPS",
            "docs/radicle-persistent-seed-plan.md",
        ]:
            self.assertIn(required_boundary, doc)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:", "api_token"]:
            self.assertNotIn(accidental_secret_marker, doc.lower())

    def test_radicle_persistent_seed_plan_is_bounded(self):
        evidence = json.loads(RADICLE_PUBLIC_SEED_UPDATE_EF16E2A_PATH.read_text(encoding="utf-8"))
        plan = RADICLE_PERSISTENT_SEED_PLAN.read_text(encoding="utf-8")

        self.assertIn(evidence["rid"], plan)
        self.assertIn(evidence["updated_commit"], plan)
        self.assertIn(evidence["vps_seed_address"], plan)
        self.assertIn("evidence/radicle-public-seed-update-ef16e2a-2026-06-29.json", plan)
        self.assertIn("evidence/radicle-external-health-timer-2026-06-29.json", plan)
        self.assertIn("evidence/radicle-public-seed-update-propagation-2026-06-29.json", plan)
        self.assertIn("evidence/radicle-public-seed-health-check-2026-06-29.json", plan)
        self.assertIn("evidence/radicle-vps-follower-systemd-service-2026-06-29.json", plan)
        self.assertIn("evidence/radicle-vps-follower-public-readback-2026-06-29.json", plan)
        self.assertIn("evidence/radicle-seed-restart-check-2026-06-29.json", plan)
        self.assertIn("evidence/radicle-independent-availability-check-2026-06-29.json", plan)
        self.assertIn("A user can clone decentralized-forge from a published Radicle seed address", plan)
        self.assertIn("rad node start", plan)
        self.assertIn("rad seed", plan)
        self.assertIn(f"rad node connect {evidence['vps_seed_address']} --timeout 30s", plan)
        for required_boundary in [
            "Do not claim durable storage",
            "Do not commit the passphrase",
            "Promote the persistent seed address",
            "not claim permanent durability",
            "automatic future update propagation",
            "future default public-routing availability",
        ]:
            self.assertIn(required_boundary, plan)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:", "api_token"]:
            self.assertNotIn(accidental_secret_marker, plan.lower())

    def test_loop45_keyless_attestation_registry_import_is_bounded(self):
        evidence = json.loads(KEYLESS_REGISTRY_IMPORT_PATH.read_text(encoding="utf-8"))

        self.assertEqual(evidence["schema_version"], "decentralized-forge.registry-verification-import.v1")
        self.assertEqual(evidence["loop"], 45)
        self.assertEqual(evidence["source_evidence"], "evidence/github-keyless-attestation-2026-06-28.json")
        self.assertEqual(evidence["subject_count"], 6)
        self.assertFalse(evidence["registry_fixture_provenance_replaced"])
        self.assertFalse(evidence["contains_secret_values"])
        self.assertFalse(evidence["private_keys_used"])
        self.assertFalse(evidence["production_readiness_claim"])
        self.assertEqual(len(evidence["verification_states"]), 1)
        state = evidence["verification_states"][0]
        self.assertEqual(state["scope"], "github-actions.keyless_artifact_attestation")
        self.assertEqual(state["state"], "live-verified")
        self.assertTrue(state["live_verified"])
        self.assertFalse(state["synthetic"])
        self.assertIn("does not replace the registry fixture ci.provenance row", state["claim_boundary"])

        evidence_blob = json.dumps(evidence).lower()
        for required in [
            "does not claim slsa compliance",
            "does not claim production supply-chain security",
            "does not use production/private personal signing keys",
        ]:
            self.assertIn(required, evidence_blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, evidence_blob)

    def test_loop34_radicle_public_smoke_evidence_is_bounded(self):
        checklist = self.live_replay_checklist
        if checklist["loop"] < 34:
            self.skipTest("Loop 34 Radicle public smoke evidence not recorded yet")
        radicle_gate = checklist["radicle_local_replay"]
        evidence_path = ROOT / radicle_gate["public_network_smoke_evidence_after_loop_34"]
        report_path = ROOT / radicle_gate["public_network_smoke_report_after_loop_34"]
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        report = report_path.read_text(encoding="utf-8")

        self.assertEqual(evidence["schema_version"], "decentralized-forge.radicle-public-network-smoke.v1")
        self.assertEqual(evidence["loop"], 34)
        self.assertTrue(evidence["verification_passed"])
        self.assertEqual(evidence["rid"], radicle_gate["public_smoke_rid_after_loop_34"])
        self.assertEqual(evidence["visibility"], "public")
        self.assertTrue(evidence["node_started"])
        self.assertTrue(evidence["publish_succeeded"])
        self.assertTrue(evidence["seed_succeeded"])
        self.assertTrue(evidence["sync_succeeded"])
        self.assertTrue(evidence["clone_node_started"])
        self.assertTrue(evidence["clone_node_connected_to_seed"])
        self.assertTrue(evidence["remote_clone_succeeded"])
        self.assertTrue(evidence["readme_readback_matches"])
        self.assertIn("removed after evidence capture", evidence["temp_state_root_shape"])
        self.assertIn("Overall verification passed: `True`", report)
        self.assertIn(evidence["rid"], report)

        evidence_blob = json.dumps(evidence).lower()
        for action_not_taken in [
            "no production/private personal keys were used",
            "no paid infrastructure or spending was used",
            "no direct outreach or named peer targeting was used",
        ]:
            self.assertIn(action_not_taken, evidence_blob)
        for required_non_claim in [
            "no durability",
            "censorship-resistance",
            "security",
            "global replication",
            "identity-trust",
            "production-readiness",
            "no broad radicle network availability claim",
        ]:
            self.assertIn(required_non_claim, evidence_blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:", "passphrase"]:
            self.assertNotIn(accidental_secret_marker, evidence_blob)

    def test_loop24_nostr_signed_preview_is_bounded_and_unpublished(self):
        checklist = self.live_replay_checklist
        if checklist["loop"] < 24:
            self.skipTest("Loop 24 Nostr relay selection evidence not recorded yet")
        nostr_gate = checklist["nostr_disposable_readback"]
        signed_path = ROOT / nostr_gate["signed_event_preview_after_loop_24"]
        signed_event = json.loads(signed_path.read_text(encoding="utf-8"))
        self.assertEqual(signed_event["id"], nostr_gate["signed_event_id_after_loop_24"])
        self.assertEqual(signed_event["pubkey"], nostr_gate["public_key_hex"])
        self.assertEqual(signed_event["kind"], 30617)
        self.assertIn("prototype/research", signed_event["content"])
        self.assertIn("does not claim production readiness", signed_event["content"])
        self.assertFalse(nostr_gate["relay_published_after_loop_24"])
        self.assertFalse(nostr_gate["relay_readback_after_loop_24"])
        relay_tags = [tag[1] for tag in signed_event["tags"] if tag and tag[0] == "relays"]
        self.assertEqual(relay_tags, nostr_gate["selected_relays_after_loop_24"])
        event_blob = json.dumps(signed_event).lower()
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, event_blob)

    def test_loop25_nostr_publish_readback_evidence_is_bounded(self):
        checklist = self.live_replay_checklist
        if checklist["loop"] < 25:
            self.skipTest("Loop 25 Nostr publish/readback evidence not recorded yet")
        nostr_gate = checklist["nostr_disposable_readback"]
        evidence_path = ROOT / nostr_gate["publish_readback_json_after_loop_25"]
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        self.assertEqual(evidence["event_id"], nostr_gate["event_id_after_loop_25"])
        self.assertEqual(evidence["pubkey"], nostr_gate["public_key_hex"])
        self.assertEqual(evidence["accepted_relays"], nostr_gate["published_relays_after_loop_25"])
        self.assertEqual(evidence["readback_verified_relays"], nostr_gate["readback_verified_relays_after_loop_25"])
        self.assertEqual(evidence["kind"], 30617)
        self.assertEqual(evidence["local_verify"]["returncode"], 0)
        for publish in evidence["publish"]:
            self.assertEqual(publish["returncode"], 0)
            self.assertIn(publish["relay"], nostr_gate["published_relays_after_loop_25"])
        for readback in evidence["readback"]:
            self.assertTrue(readback["matched"])
            self.assertTrue(readback["field_match"])
            self.assertEqual(readback["verify_readback"]["returncode"], 0)
            self.assertEqual(readback["events"][0]["id"], nostr_gate["event_id_after_loop_25"])
        evidence_blob = json.dumps(evidence).lower()
        for required_non_claim in [
            "not proof of global propagation",
            "not proof of censorship resistance",
            "not production readiness",
        ]:
            self.assertIn(required_non_claim, evidence_blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, evidence_blob)

    def test_loop28_nostr_readback_check_evidence_is_bounded(self):
        checklist = self.live_replay_checklist
        if checklist["loop"] < 28:
            self.skipTest("Loop 28 Nostr readback persistence evidence not recorded yet")
        nostr_gate = checklist["nostr_disposable_readback"]
        evidence_path = ROOT / nostr_gate["readback_check_json_after_loop_28"]
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        self.assertEqual(evidence["loop"], 28)
        self.assertEqual(evidence["event_id"], nostr_gate["event_id_after_loop_25"])
        self.assertEqual(evidence["selected_relays"], nostr_gate["selected_relays_rechecked_after_loop_28"])
        self.assertEqual(evidence["extra_relays"], nostr_gate["extra_relays_checked_after_loop_28"])
        self.assertEqual(evidence["verified_relays"], nostr_gate["readback_verified_relays_after_loop_28"])
        by_relay = {readback["relay"]: readback for readback in evidence["readback"]}
        for selected_relay in nostr_gate["selected_relays_rechecked_after_loop_28"]:
            self.assertTrue(by_relay[selected_relay]["matched"])
            self.assertTrue(by_relay[selected_relay]["field_match"])
            self.assertEqual(by_relay[selected_relay]["verify_readback"]["returncode"], 0)
        self.assertTrue(by_relay["wss://relay.primal.net"]["matched"])
        self.assertFalse(by_relay["wss://nostr.wine"]["matched"])
        evidence_blob = json.dumps(evidence).lower()
        for required_non_claim in [
            "not proof of global propagation",
            "not proof of censorship resistance",
            "not production readiness",
            "not full nip-34 or forge protocol compatibility",
        ]:
            self.assertIn(required_non_claim, evidence_blob)
        for action_not_taken in [
            "no new nostr event was published",
            "no secret key material was read or printed",
            "no radicle public-network action was taken",
        ]:
            self.assertIn(action_not_taken, evidence_blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, evidence_blob)

    def test_loop29_nostr_live_readback_fixture_import_is_bounded(self):
        fixture = self.nostr_live_readback_fixture
        self.assertEqual(fixture["schema_version"], "decentralized-forge.nostr-live-readback-events.v1")
        self.assertEqual(fixture["loop"], 29)
        self.assertEqual(fixture["source_evidence"], "evidence/nostr-loop25-publish-readback-2026-06-22.json")
        self.assertIn("selected-relay readback evidence only", fixture["claim_boundary"])
        self.assertEqual(len(fixture["events"]), 1)
        entry = fixture["events"][0]
        event = entry["event"]
        self.assertEqual(event["id"], entry["source_event_id"])
        self.assertEqual(event["pubkey"], entry["source_pubkey"])
        self.assertEqual(event["kind"], 30617)
        self.assertTrue(entry["selected_relay_readback_verified"])
        self.assertFalse(entry["new_event_published_in_loop_29"])
        self.assertIn("does not verify NIP-34 issue", json.dumps(entry["non_claims"]))

        parsed = nip34_adapter.parse_live_readback_fixture(fixture)
        self.assertEqual(parsed["events"][0]["event_id"], event["id"])
        self.assertEqual(parsed["events"][0]["readback_verified_relays"], ["wss://relay.damus.io", "wss://nos.lol"])
        report = parsed["conformance_reports"][0]
        self.assertTrue(report["event_id_computed"])
        self.assertTrue(report["event_id_matches_recorded_id"])
        self.assertTrue(report["signed"])
        self.assertTrue(report["published"])
        state = parsed["verification_states"][0]
        self.assertEqual(state["scope"], "nip34.adapter.live_repository_announcement_readback")
        self.assertEqual(state["state"], "live-verified")
        self.assertTrue(state["live_verified"])
        self.assertFalse(state["synthetic"])
        self.assertIn("selected-relay readback evidence only", state["claim_boundary"])

        exported = nip34_adapter.export_fixture_pair(
            self.nostr_repo_fixture,
            self.nostr_collab_fixture,
            self.nostr_state_status_fixture,
            fixture,
        )
        live_states = [state for state in exported["verification_states"] if state["scope"] == "nip34.adapter.live_repository_announcement_readback"]
        self.assertEqual(len(live_states), 1)
        self.assertEqual(exported["live_readback"]["events"][0]["event_id"], event["id"])
        blob = json.dumps(exported).lower()
        for required_non_claim in [
            "not proof of global propagation",
            "not proof of censorship resistance",
            "not production readiness",
            "not full nip-34 or forge protocol compatibility",
        ]:
            self.assertIn(required_non_claim, blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, blob)

    def test_loop26_live_evidence_index_imports_only_bounded_evidence(self):
        index = self.live_evidence_index
        self.assertEqual(index["schema_version"], "decentralized-forge.live-evidence-index.v1")
        self.assertEqual(index["loop"], 73)
        self.assertFalse(index["claim_policy"]["contains_secret_values"])
        by_id = {item["id"]: item for item in index["evidence"]}
        self.assertEqual(
            set(by_id),
            {
                "loop23-radicle-local-cli-replay",
                "loop25-nostr-selected-relay-readback",
                "loop34-radicle-disposable-public-smoke",
                "loop40-github-keyless-artifact-attestation",
                "loop41-helia-local-ipfs-add-get",
                "loop42-public-gateway-pinning-preflight",
                "loop43-nostr-issue-patch-readback",
                "loop44-radicle-broader-check",
                "loop45-keyless-attestation-registry-import",
                "loop59-radicle-project-repo-smoke",
                "loop60-radicle-fresh-readback-check",
                "loop61-radicle-update-continuity-check",
                "loop62-radicle-retained-delegate-check",
                "loop63-radicle-retained-update-check",
                "loop65-radicle-independent-availability-check",
                "loop66-radicle-seed-restart-check",
                "loop67-radicle-vps-follower-public-readback",
                "loop68-radicle-vps-follower-systemd-service",
                "loop69-radicle-public-seed-health-check",
                "loop70-radicle-public-seed-update-propagation",
                "loop71-radicle-external-health-timer",
                "loop72-radicle-public-seed-update-ef16e2a",
                "loop73-radicle-second-follower-tailnet-readback",
            },
        )

        radicle = by_id["loop23-radicle-local-cli-replay"]
        self.assertEqual(radicle["protocol"], "radicle")
        self.assertEqual(radicle["state"], "local-cli-verified")
        self.assertTrue(radicle["local_cli_verified"])
        self.assertFalse(radicle["live_network_action"])
        self.assertFalse(radicle["selected_relay_readback_verified"])
        self.assertEqual(radicle["evidence_file"], "evidence/radicle-local-replay-2026-06-22.md")
        self.assertEqual(radicle["public_identifiers"]["visibility"], "private")
        self.assertIn("no public seed publication", radicle["non_claims"])
        self.assertIn("Later Loop 34 evidence", radicle["notes"])

        nostr = by_id["loop25-nostr-selected-relay-readback"]
        self.assertEqual(nostr["protocol"], "nostr")
        self.assertEqual(nostr["state"], "selected-relay-readback-verified")
        self.assertTrue(nostr["live_network_action"])
        self.assertTrue(nostr["local_cli_verified"])
        self.assertTrue(nostr["selected_relay_readback_verified"])
        self.assertEqual(nostr["evidence_file"], "evidence/nostr-loop25-publish-readback-2026-06-22.json")
        self.assertEqual(nostr["public_identifiers"]["event_id"], self.live_replay_checklist["nostr_disposable_readback"]["event_id_after_loop_25"])
        self.assertEqual(nostr["public_identifiers"]["relays"], ["wss://relay.damus.io", "wss://nos.lol"])
        self.assertIn("not proof of global propagation", nostr["non_claims"])

        radicle_public = by_id["loop34-radicle-disposable-public-smoke"]
        self.assertEqual(radicle_public["protocol"], "radicle")
        self.assertEqual(radicle_public["state"], "disposable-public-smoke-verified")
        self.assertTrue(radicle_public["live_network_action"])
        self.assertTrue(radicle_public["local_cli_verified"])
        self.assertFalse(radicle_public["selected_relay_readback_verified"])
        self.assertEqual(radicle_public["evidence_file"], "evidence/radicle-public-network-smoke-2026-06-22.json")
        self.assertEqual(
            radicle_public["public_identifiers"]["rid"],
            self.live_replay_checklist["radicle_local_replay"]["public_smoke_rid_after_loop_34"],
        )
        self.assertIn("not proof of broad Radicle network availability", radicle_public["non_claims"])

        attestation = by_id["loop40-github-keyless-artifact-attestation"]
        self.assertEqual(attestation["protocol"], "github-actions")
        self.assertEqual(attestation["state"], "hosted-keyless-attestation-generated")
        self.assertTrue(attestation["live_network_action"])
        self.assertFalse(attestation["synthetic"])
        self.assertEqual(attestation["public_identifiers"]["subject_count"], 6)
        self.assertIn("not a SLSA compliance claim", attestation["non_claims"])
        self.assertIn("not a registry fixture provenance import", attestation["non_claims"])

        helia = by_id["loop41-helia-local-ipfs-add-get"]
        self.assertEqual(helia["protocol"], "ipfs")
        self.assertEqual(helia["state"], "local-helia-add-get-verified")
        self.assertFalse(helia["live_network_action"])
        self.assertFalse(helia["synthetic"])
        self.assertEqual(
            helia["public_identifiers"]["cid"],
            "bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua",
        )
        self.assertIn("not proof of public gateway availability", helia["non_claims"])
        self.assertIn("not proof of durability", helia["non_claims"])

        gateway = by_id["loop42-public-gateway-pinning-preflight"]
        self.assertEqual(gateway["protocol"], "ipfs")
        self.assertEqual(gateway["state"], "public-gateway-no-readback-observed")
        self.assertTrue(gateway["live_network_action"])
        self.assertEqual(gateway["public_identifiers"]["successful_gateway_readback_count"], 0)
        self.assertFalse(gateway["public_identifiers"]["pinning_provider_selected"])
        self.assertIn("not proof of pinning", gateway["non_claims"])

        nostr_issue_patch = by_id["loop43-nostr-issue-patch-readback"]
        self.assertEqual(nostr_issue_patch["protocol"], "nostr")
        self.assertEqual(nostr_issue_patch["state"], "selected-relay-issue-patch-readback-verified")
        self.assertTrue(nostr_issue_patch["live_network_action"])
        self.assertTrue(nostr_issue_patch["selected_relay_readback_verified"])
        self.assertEqual(len(nostr_issue_patch["public_identifiers"]["event_ids"]), 2)
        self.assertEqual(nostr_issue_patch["public_identifiers"]["kinds"], [1621, 1617])
        self.assertIn("not proof of relay durability", nostr_issue_patch["non_claims"])

        radicle_broader = by_id["loop44-radicle-broader-check"]
        self.assertEqual(radicle_broader["protocol"], "radicle")
        self.assertEqual(radicle_broader["state"], "cli-blocked-readonly-route-probed")
        self.assertTrue(radicle_broader["live_network_action"])
        self.assertFalse(radicle_broader["public_identifiers"]["rad_cli_available"])
        self.assertIn("not a broader Radicle CLI verification", radicle_broader["non_claims"])

        keyless_import = by_id["loop45-keyless-attestation-registry-import"]
        self.assertEqual(keyless_import["protocol"], "github-actions")
        self.assertEqual(keyless_import["state"], "registry-shaped-import-recorded")
        self.assertFalse(keyless_import["live_network_action"])
        self.assertFalse(keyless_import["public_identifiers"]["registry_fixture_provenance_replaced"])
        self.assertIn("not a replacement for fixtures/example-project.registry.json ci.provenance", keyless_import["non_claims"])

        radicle_project = by_id["loop59-radicle-project-repo-smoke"]
        self.assertEqual(radicle_project["protocol"], "radicle")
        self.assertEqual(radicle_project["state"], "project-repo-radicle-readback-verified")
        self.assertTrue(radicle_project["live_network_action"])
        self.assertTrue(radicle_project["local_cli_verified"])
        self.assertFalse(radicle_project["selected_relay_readback_verified"])
        self.assertEqual(radicle_project["evidence_file"], "evidence/radicle-project-repo-smoke-2026-06-29.json")
        self.assertRegex(radicle_project["public_identifiers"]["rid"], r"^rad:z[0-9A-Za-z]+$")
        self.assertEqual(
            radicle_project["public_identifiers"]["source_commit"],
            radicle_project["public_identifiers"]["clone_commit"],
        )
        self.assertIn("not proof of broad Radicle network availability", radicle_project["non_claims"])

        radicle_fresh = by_id["loop60-radicle-fresh-readback-check"]
        self.assertEqual(radicle_fresh["protocol"], "radicle")
        self.assertEqual(radicle_fresh["state"], "fresh-network-readback-observed")
        self.assertTrue(radicle_fresh["live_network_action"])
        self.assertTrue(radicle_fresh["local_cli_verified"])
        self.assertFalse(radicle_fresh["selected_relay_readback_verified"])
        self.assertEqual(radicle_fresh["evidence_file"], "evidence/radicle-fresh-readback-check-2026-06-29.json")
        self.assertEqual(radicle_fresh["public_identifiers"]["rid"], radicle_project["public_identifiers"]["rid"])
        self.assertEqual(
            radicle_fresh["public_identifiers"]["expected_commit"],
            radicle_fresh["public_identifiers"]["clone_commit"],
        )
        self.assertFalse(radicle_fresh["public_identifiers"]["original_seed_profile_reused"])
        self.assertFalse(radicle_fresh["public_identifiers"]["explicit_original_seed_used"])
        self.assertIn("not proof of permanent durability", radicle_fresh["non_claims"])

        radicle_update = by_id["loop61-radicle-update-continuity-check"]
        self.assertEqual(radicle_update["protocol"], "radicle")
        self.assertEqual(radicle_update["state"], "fresh-peer-update-default-readback-original-delegate")
        self.assertTrue(radicle_update["live_network_action"])
        self.assertTrue(radicle_update["local_cli_verified"])
        self.assertFalse(radicle_update["selected_relay_readback_verified"])
        self.assertEqual(radicle_update["evidence_file"], "evidence/radicle-update-continuity-check-2026-06-29.json")
        self.assertEqual(radicle_update["public_identifiers"]["rid"], radicle_project["public_identifiers"]["rid"])
        self.assertTrue(radicle_update["public_identifiers"]["fresh_peer_push_observed"])
        self.assertFalse(radicle_update["public_identifiers"]["same_rid_current_commit_default_readback_observed"])
        self.assertEqual(
            radicle_update["public_identifiers"]["default_readback_commit"],
            radicle_update["public_identifiers"]["prior_recorded_commit"],
        )
        self.assertIn("not proof of canonical default-branch update continuity", radicle_update["non_claims"])

        radicle_retained = by_id["loop62-radicle-retained-delegate-check"]
        self.assertEqual(radicle_retained["protocol"], "radicle")
        self.assertEqual(radicle_retained["state"], "retained-delegate-default-readback-verified")
        self.assertTrue(radicle_retained["live_network_action"])
        self.assertTrue(radicle_retained["local_cli_verified"])
        self.assertFalse(radicle_retained["selected_relay_readback_verified"])
        self.assertFalse(radicle_retained["synthetic"])
        self.assertEqual(radicle_retained["evidence_file"], "evidence/radicle-retained-delegate-check-2026-06-29.json")
        self.assertRegex(radicle_retained["public_identifiers"]["rid"], r"^rad:z[0-9A-Za-z]+$")
        self.assertRegex(radicle_retained["public_identifiers"]["delegate_did"], r"^did:key:z6[0-9A-Za-z]+$")
        self.assertEqual(
            radicle_retained["public_identifiers"]["source_commit"],
            radicle_retained["public_identifiers"]["default_readback_commit"],
        )
        self.assertTrue(radicle_retained["public_identifiers"]["default_readback_matches_source"])
        self.assertEqual(
            radicle_retained["public_identifiers"]["source_commit"],
            radicle_retained["public_identifiers"]["direct_seed_readback_commit"],
        )
        self.assertTrue(radicle_retained["public_identifiers"]["direct_seed_readback_matches_source"])
        self.assertEqual(radicle_retained["public_identifiers"]["retained_state_scope"], ".tmp/radicle-retained-delegate")
        self.assertFalse(radicle_retained["public_identifiers"]["retained_state_committed"])
        self.assertFalse(radicle_retained["public_identifiers"]["secret_values_recorded"])
        self.assertIn("not proof of future default public-routing availability", radicle_retained["non_claims"])
        self.assertIn("not a committed secret or key backup", radicle_retained["non_claims"])

        radicle_retained_update = by_id["loop63-radicle-retained-update-check"]
        self.assertEqual(radicle_retained_update["protocol"], "radicle")
        self.assertEqual(radicle_retained_update["state"], "retained-rid-direct-seed-update-readback-verified")
        self.assertTrue(radicle_retained_update["live_network_action"])
        self.assertTrue(radicle_retained_update["local_cli_verified"])
        self.assertFalse(radicle_retained_update["selected_relay_readback_verified"])
        self.assertFalse(radicle_retained_update["synthetic"])
        self.assertEqual(radicle_retained_update["evidence_file"], "evidence/radicle-retained-update-check-2026-06-29.json")
        self.assertEqual(radicle_retained_update["public_identifiers"]["rid"], radicle_retained["public_identifiers"]["rid"])
        self.assertEqual(
            radicle_retained_update["public_identifiers"]["prior_recorded_commit"],
            radicle_retained["public_identifiers"]["source_commit"],
        )
        self.assertTrue(radicle_retained_update["public_identifiers"]["same_retained_rid"])
        self.assertTrue(radicle_retained_update["public_identifiers"]["advanced_from_prior_recorded_commit"])
        self.assertFalse(radicle_retained_update["public_identifiers"]["default_readback_matches_source"])
        self.assertEqual(radicle_retained_update["public_identifiers"]["default_readback_commit"], "")
        self.assertEqual(
            radicle_retained_update["public_identifiers"]["direct_seed_readback_commit"],
            radicle_retained_update["public_identifiers"]["current_source_commit"],
        )
        self.assertTrue(radicle_retained_update["public_identifiers"]["direct_seed_readback_matches_source"])
        self.assertFalse(radicle_retained_update["public_identifiers"]["retained_state_committed"])
        self.assertFalse(radicle_retained_update["public_identifiers"]["secret_values_recorded"])
        self.assertIn("not proof of future default public-routing availability", radicle_retained_update["non_claims"])
        self.assertIn("not a committed secret or key backup", radicle_retained_update["non_claims"])

        radicle_independent = by_id["loop65-radicle-independent-availability-check"]
        self.assertEqual(radicle_independent["protocol"], "radicle")
        self.assertEqual(radicle_independent["state"], "retained-rid-follower-seed-readback-verified")
        self.assertTrue(radicle_independent["live_network_action"])
        self.assertTrue(radicle_independent["local_cli_verified"])
        self.assertFalse(radicle_independent["selected_relay_readback_verified"])
        self.assertFalse(radicle_independent["synthetic"])
        self.assertEqual(radicle_independent["evidence_file"], "evidence/radicle-independent-availability-check-2026-06-29.json")
        self.assertEqual(radicle_independent["public_identifiers"]["rid"], radicle_retained_update["public_identifiers"]["rid"])
        self.assertEqual(
            radicle_independent["public_identifiers"]["prior_verified_commit"],
            radicle_retained_update["public_identifiers"]["current_source_commit"],
        )
        self.assertTrue(radicle_independent["public_identifiers"]["same_retained_rid"])
        self.assertTrue(radicle_independent["public_identifiers"]["advanced_from_prior_verified_commit"])
        self.assertEqual(
            radicle_independent["public_identifiers"]["reader_a_readback_commit"],
            radicle_independent["public_identifiers"]["current_source_commit"],
        )
        self.assertTrue(radicle_independent["public_identifiers"]["reader_a_readback_matches_source"])
        self.assertTrue(radicle_independent["public_identifiers"]["follower_seed_succeeded"])
        self.assertEqual(
            radicle_independent["public_identifiers"]["reader_b_readback_commit"],
            radicle_independent["public_identifiers"]["current_source_commit"],
        )
        self.assertTrue(radicle_independent["public_identifiers"]["reader_b_readback_matches_source"])
        self.assertFalse(radicle_independent["public_identifiers"]["retained_state_committed"])
        self.assertFalse(radicle_independent["public_identifiers"]["secret_values_recorded"])
        self.assertFalse(radicle_independent["public_identifiers"]["persistent_seed_service_started"])
        self.assertIn("not a persistent public seed service", radicle_independent["non_claims"])
        self.assertIn("not proof of future default public-routing availability", radicle_independent["non_claims"])

        radicle_seed_restart = by_id["loop66-radicle-seed-restart-check"]
        self.assertEqual(radicle_seed_restart["protocol"], "radicle")
        self.assertEqual(radicle_seed_restart["state"], "retained-rid-seed-restart-readback-verified")
        self.assertTrue(radicle_seed_restart["live_network_action"])
        self.assertTrue(radicle_seed_restart["local_cli_verified"])
        self.assertFalse(radicle_seed_restart["selected_relay_readback_verified"])
        self.assertFalse(radicle_seed_restart["synthetic"])
        self.assertEqual(radicle_seed_restart["evidence_file"], "evidence/radicle-seed-restart-check-2026-06-29.json")
        self.assertEqual(radicle_seed_restart["public_identifiers"]["rid"], radicle_independent["public_identifiers"]["rid"])
        self.assertEqual(
            radicle_seed_restart["public_identifiers"]["prior_verified_commit"],
            radicle_independent["public_identifiers"]["current_source_commit"],
        )
        self.assertTrue(radicle_seed_restart["public_identifiers"]["same_retained_rid"])
        self.assertTrue(radicle_seed_restart["public_identifiers"]["advanced_from_prior_verified_commit"])
        self.assertFalse(radicle_seed_restart["public_identifiers"]["seed_address_publicly_reachable"])
        self.assertFalse(radicle_seed_restart["public_identifiers"]["separate_host_readback_observed"])
        self.assertEqual(
            radicle_seed_restart["public_identifiers"]["first_reader_readback_commit"],
            radicle_seed_restart["public_identifiers"]["current_source_commit"],
        )
        self.assertTrue(radicle_seed_restart["public_identifiers"]["first_reader_readback_matches_source"])
        self.assertEqual(
            radicle_seed_restart["public_identifiers"]["second_reader_readback_commit"],
            radicle_seed_restart["public_identifiers"]["current_source_commit"],
        )
        self.assertTrue(radicle_seed_restart["public_identifiers"]["second_reader_readback_matches_source"])
        self.assertEqual(
            radicle_seed_restart["public_identifiers"]["first_seed_node_id"],
            radicle_seed_restart["public_identifiers"]["restart_seed_node_id"],
        )
        self.assertTrue(radicle_seed_restart["public_identifiers"]["same_seed_node_after_restart"])
        self.assertFalse(radicle_seed_restart["public_identifiers"]["retained_state_committed"])
        self.assertFalse(radicle_seed_restart["public_identifiers"]["secret_values_recorded"])
        self.assertFalse(radicle_seed_restart["public_identifiers"]["persistent_seed_service_left_running"])
        self.assertIn("not proof of public seed address reachability", radicle_seed_restart["non_claims"])
        self.assertIn("not proof of separate-network availability", radicle_seed_restart["non_claims"])
        self.assertIn("not an always-on persistent public seed service", radicle_seed_restart["non_claims"])

        radicle_vps = by_id["loop67-radicle-vps-follower-public-readback"]
        self.assertEqual(radicle_vps["protocol"], "radicle")
        self.assertEqual(radicle_vps["state"], "public-vps-follower-seed-readback-verified")
        self.assertTrue(radicle_vps["live_network_action"])
        self.assertTrue(radicle_vps["local_cli_verified"])
        self.assertFalse(radicle_vps["selected_relay_readback_verified"])
        self.assertFalse(radicle_vps["synthetic"])
        self.assertEqual(radicle_vps["evidence_file"], "evidence/radicle-vps-follower-public-readback-2026-06-29.json")
        self.assertEqual(radicle_vps["public_identifiers"]["rid"], radicle_seed_restart["public_identifiers"]["rid"])
        self.assertEqual(
            radicle_vps["public_identifiers"]["prior_verified_commit"],
            radicle_seed_restart["public_identifiers"]["current_source_commit"],
        )
        self.assertTrue(radicle_vps["public_identifiers"]["same_retained_rid"])
        self.assertEqual(radicle_vps["public_identifiers"]["current_source_commit"], "610fc3da9757d0cb123aa5976db552b991b766d4")
        self.assertEqual(
            radicle_vps["public_identifiers"]["vps_seed_address"],
            "z6Mkk7qWfxE18R4jt5ruXmv1a7zydT9r1sY5LXx21PWySA4f@187.77.19.162:8776",
        )
        self.assertTrue(radicle_vps["public_identifiers"]["vps_seed_left_running"])
        self.assertTrue(radicle_vps["public_identifiers"]["public_seed_address_reachable"])
        self.assertEqual(radicle_vps["public_identifiers"]["fresh_reader_host"], "ubuntu-work")
        self.assertEqual(
            radicle_vps["public_identifiers"]["fresh_reader_readback_commit"],
            radicle_vps["public_identifiers"]["current_source_commit"],
        )
        self.assertTrue(radicle_vps["public_identifiers"]["fresh_reader_readback_matches_expected"])
        self.assertFalse(radicle_vps["public_identifiers"]["retained_state_copied_to_vps"])
        self.assertFalse(radicle_vps["public_identifiers"]["retained_state_committed"])
        self.assertFalse(radicle_vps["public_identifiers"]["secret_values_recorded"])
        self.assertTrue(radicle_vps["public_identifiers"]["temporary_bridge_stopped_after_bootstrap"])
        self.assertTrue(radicle_vps["public_identifiers"]["maintainer_seed_stopped_after_bootstrap"])
        self.assertIn("not maintainer key material on the VPS", radicle_vps["non_claims"])
        self.assertIn("not proof of future default public-routing availability", radicle_vps["non_claims"])

        radicle_service = by_id["loop68-radicle-vps-follower-systemd-service"]
        self.assertEqual(radicle_service["protocol"], "radicle")
        self.assertEqual(radicle_service["state"], "public-vps-follower-service-restart-readback-verified")
        self.assertTrue(radicle_service["live_network_action"])
        self.assertTrue(radicle_service["local_cli_verified"])
        self.assertFalse(radicle_service["synthetic"])
        self.assertEqual(radicle_service["evidence_file"], "evidence/radicle-vps-follower-systemd-service-2026-06-29.json")
        self.assertTrue(radicle_service["public_identifiers"]["systemd_user_service_enabled"])
        self.assertTrue(radicle_service["public_identifiers"]["systemd_service_active_after_restart"])
        self.assertTrue(radicle_service["public_identifiers"]["systemd_linger_enabled"])
        self.assertEqual(radicle_service["public_identifiers"]["fresh_reader_readback_commit"], radicle_service["public_identifiers"]["current_source_commit"])
        self.assertFalse(radicle_service["public_identifiers"]["secret_values_recorded"])
        self.assertFalse(radicle_service["public_identifiers"]["retained_maintainer_key_material_copied_to_vps"])
        self.assertIn("not maintainer key material on the VPS", radicle_service["non_claims"])

        radicle_health = by_id["loop69-radicle-public-seed-health-check"]
        self.assertEqual(radicle_health["protocol"], "radicle")
        self.assertEqual(radicle_health["state"], "public-seed-health-check-verified")
        self.assertTrue(radicle_health["live_network_action"])
        self.assertTrue(radicle_health["local_cli_verified"])
        self.assertFalse(radicle_health["synthetic"])
        self.assertEqual(radicle_health["evidence_file"], "evidence/radicle-public-seed-health-check-2026-06-29.json")
        self.assertEqual(radicle_health["public_identifiers"]["health_check_script"], "scripts/check_public_radicle_seed.py")
        self.assertTrue(radicle_health["public_identifiers"]["fresh_reader_connected_to_public_seed"])
        self.assertTrue(radicle_health["public_identifiers"]["fresh_reader_clone_succeeded"])
        self.assertEqual(radicle_health["public_identifiers"]["fresh_reader_readback_commit"], radicle_health["public_identifiers"]["current_source_commit"])
        self.assertTrue(radicle_health["public_identifiers"]["fresh_reader_temp_state_removed"])
        self.assertFalse(radicle_health["public_identifiers"]["secret_values_recorded"])

        radicle_public_update = by_id["loop70-radicle-public-seed-update-propagation"]
        self.assertEqual(radicle_public_update["protocol"], "radicle")
        self.assertEqual(radicle_public_update["state"], "public-vps-follower-update-readback-verified")
        self.assertTrue(radicle_public_update["live_network_action"])
        self.assertTrue(radicle_public_update["local_cli_verified"])
        self.assertFalse(radicle_public_update["synthetic"])
        self.assertEqual(radicle_public_update["evidence_file"], "evidence/radicle-public-seed-update-propagation-2026-06-29.json")
        self.assertEqual(radicle_public_update["public_identifiers"]["rid"], radicle_vps["public_identifiers"]["rid"])
        self.assertEqual(
            radicle_public_update["public_identifiers"]["prior_verified_commit"],
            radicle_vps["public_identifiers"]["current_source_commit"],
        )
        self.assertEqual(radicle_public_update["public_identifiers"]["current_source_commit"], "64efbada294d4a57c014a27398b92e344c6d68aa")
        self.assertTrue(radicle_public_update["public_identifiers"]["same_retained_rid"])
        self.assertTrue(radicle_public_update["public_identifiers"]["systemd_user_service_enabled"])
        self.assertTrue(radicle_public_update["public_identifiers"]["temporary_bridge_used"])
        self.assertTrue(radicle_public_update["public_identifiers"]["temporary_bridge_stopped_after_sync"])
        self.assertTrue(radicle_public_update["public_identifiers"]["maintainer_seed_stopped_after_sync"])
        self.assertTrue(radicle_public_update["public_identifiers"]["vps_sync_from_retained_maintainer_seed_succeeded"])
        self.assertEqual(
            radicle_public_update["public_identifiers"]["vps_local_clone_readback_commit"],
            radicle_public_update["public_identifiers"]["current_source_commit"],
        )
        self.assertTrue(radicle_public_update["public_identifiers"]["vps_local_clone_readback_matches_updated_commit"])
        self.assertEqual(
            radicle_public_update["public_identifiers"]["fresh_reader_readback_commit"],
            radicle_public_update["public_identifiers"]["current_source_commit"],
        )
        self.assertTrue(radicle_public_update["public_identifiers"]["fresh_reader_readback_matches_expected"])
        self.assertFalse(radicle_public_update["public_identifiers"]["retained_state_committed"])
        self.assertFalse(radicle_public_update["public_identifiers"]["secret_values_recorded"])
        self.assertFalse(radicle_public_update["public_identifiers"]["retained_maintainer_key_material_copied_to_vps"])
        self.assertIn("not proof of automatic future update propagation", radicle_public_update["non_claims"])
        self.assertIn("not maintainer key material on the VPS", radicle_public_update["non_claims"])

        radicle_health_timer = by_id["loop71-radicle-external-health-timer"]
        self.assertEqual(radicle_health_timer["protocol"], "radicle")
        self.assertEqual(radicle_health_timer["state"], "external-health-timer-readback-verified")
        self.assertTrue(radicle_health_timer["live_network_action"])
        self.assertTrue(radicle_health_timer["local_cli_verified"])
        self.assertFalse(radicle_health_timer["synthetic"])
        self.assertEqual(radicle_health_timer["evidence_file"], "evidence/radicle-external-health-timer-2026-06-29.json")
        self.assertEqual(radicle_health_timer["public_identifiers"]["health_host"], "ubuntu-work")
        self.assertTrue(radicle_health_timer["public_identifiers"]["health_timer_active"])
        self.assertTrue(radicle_health_timer["public_identifiers"]["health_timer_enabled"])
        self.assertTrue(radicle_health_timer["public_identifiers"]["health_timer_persistent"])
        self.assertTrue(radicle_health_timer["public_identifiers"]["latest_verification_passed"])
        self.assertEqual(
            radicle_health_timer["public_identifiers"]["latest_readback_commit"],
            radicle_health_timer["public_identifiers"]["current_source_commit"],
        )
        self.assertFalse(radicle_health_timer["public_identifiers"]["secret_values_recorded"])
        self.assertIn("not proof of automatic repair", radicle_health_timer["non_claims"])

        radicle_public_update_ef16 = by_id["loop72-radicle-public-seed-update-ef16e2a"]
        self.assertEqual(radicle_public_update_ef16["protocol"], "radicle")
        self.assertEqual(radicle_public_update_ef16["state"], "public-vps-follower-update-readback-verified")
        self.assertTrue(radicle_public_update_ef16["live_network_action"])
        self.assertTrue(radicle_public_update_ef16["local_cli_verified"])
        self.assertFalse(radicle_public_update_ef16["synthetic"])
        self.assertEqual(radicle_public_update_ef16["evidence_file"], "evidence/radicle-public-seed-update-ef16e2a-2026-06-29.json")
        self.assertEqual(radicle_public_update_ef16["public_identifiers"]["rid"], radicle_public_update["public_identifiers"]["rid"])
        self.assertEqual(
            radicle_public_update_ef16["public_identifiers"]["prior_verified_commit"],
            radicle_public_update["public_identifiers"]["current_source_commit"],
        )
        self.assertEqual(radicle_public_update_ef16["public_identifiers"]["current_source_commit"], "ef16e2ad39d3e13bdcc9d454443c5bbb17733c68")
        self.assertTrue(radicle_public_update_ef16["public_identifiers"]["external_health_timer_enabled"])
        self.assertTrue(radicle_public_update_ef16["public_identifiers"]["temporary_bridge_stopped_after_sync"])
        self.assertTrue(radicle_public_update_ef16["public_identifiers"]["maintainer_seed_stopped_after_sync"])
        self.assertTrue(radicle_public_update_ef16["public_identifiers"]["vps_sync_succeeded"])
        self.assertEqual(
            radicle_public_update_ef16["public_identifiers"]["fresh_reader_readback_commit"],
            radicle_public_update_ef16["public_identifiers"]["current_source_commit"],
        )
        self.assertTrue(radicle_public_update_ef16["public_identifiers"]["fresh_reader_readback_matches_expected"])
        self.assertFalse(radicle_public_update_ef16["public_identifiers"]["retained_state_committed"])
        self.assertFalse(radicle_public_update_ef16["public_identifiers"]["secret_values_recorded"])
        self.assertFalse(radicle_public_update_ef16["public_identifiers"]["retained_maintainer_key_material_copied_to_vps"])
        self.assertIn("not proof of automatic future update propagation", radicle_public_update_ef16["non_claims"])
        self.assertIn("not maintainer key material on the VPS", radicle_public_update_ef16["non_claims"])

        radicle_second_seed = by_id["loop73-radicle-second-follower-tailnet-readback"]
        self.assertEqual(radicle_second_seed["protocol"], "radicle")
        self.assertEqual(radicle_second_seed["state"], "second-follower-tailnet-readback-verified")
        self.assertTrue(radicle_second_seed["live_network_action"])
        self.assertTrue(radicle_second_seed["local_cli_verified"])
        self.assertFalse(radicle_second_seed["synthetic"])
        self.assertEqual(radicle_second_seed["evidence_file"], "evidence/radicle-second-seed-tailnet-health-2026-06-29.json")
        self.assertEqual(radicle_second_seed["public_identifiers"]["rid"], radicle_public_update_ef16["public_identifiers"]["rid"])
        self.assertEqual(
            radicle_second_seed["public_identifiers"]["current_source_commit"],
            radicle_public_update_ef16["public_identifiers"]["current_source_commit"],
        )
        self.assertEqual(
            radicle_second_seed["public_identifiers"]["fresh_reader_readback_commit"],
            radicle_second_seed["public_identifiers"]["current_source_commit"],
        )
        self.assertTrue(radicle_second_seed["public_identifiers"]["fresh_reader_readback_matches_expected"])
        self.assertTrue(radicle_second_seed["public_identifiers"]["second_seed_state_host_separate_from_public_seed"])
        self.assertTrue(radicle_second_seed["public_identifiers"]["second_seed_systemd_user_service_enabled"])
        self.assertTrue(radicle_second_seed["public_identifiers"]["second_seed_service_active"])
        self.assertFalse(radicle_second_seed["public_identifiers"]["second_seed_public_internet_relay_enabled"])
        self.assertFalse(radicle_second_seed["public_identifiers"]["second_seed_public_internet_address_approved"])
        self.assertFalse(radicle_second_seed["public_identifiers"]["retained_state_committed"])
        self.assertFalse(radicle_second_seed["public_identifiers"]["secret_values_recorded"])
        self.assertFalse(radicle_second_seed["public_identifiers"]["retained_maintainer_key_material_copied_to_second_seed"])
        self.assertIn("not a second public internet seed yet", radicle_second_seed["non_claims"])
        self.assertIn("not maintainer key material on ubuntu-work", radicle_second_seed["non_claims"])

    def test_loop40_github_keyless_attestation_evidence_is_bounded(self):
        index = self.live_evidence_index
        by_id = {item["id"]: item for item in index["evidence"]}
        evidence_path = ROOT / by_id["loop40-github-keyless-artifact-attestation"]["evidence_file"]
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))

        self.assertEqual(evidence["schema_version"], "decentralized-forge.github-keyless-attestation.v1")
        self.assertEqual(evidence["loop"], 40)
        self.assertEqual(evidence["workflow_run"]["conclusion"], "success")
        self.assertEqual(evidence["workflow_run"]["commit"], "1b6e6c84036c52f6dee0bbbee49fdc5e29787dc7")
        self.assertEqual(evidence["attestation"]["action"], "actions/attest@v4")
        self.assertEqual(evidence["attestation"]["predicate_type"], "https://slsa.dev/provenance/v1")
        self.assertEqual(evidence["attestation"]["transparency_log_entries"], 1)
        self.assertEqual(len(evidence["attestation"]["subjects"]), 6)
        self.assertFalse(evidence["contains_secret_values"])
        self.assertFalse(evidence["private_keys_used"])
        self.assertFalse(evidence["paid_infrastructure_used"])
        self.assertFalse(evidence["production_readiness_claim"])
        self.assertFalse(evidence["registry_fixture_provenance_imported"])
        for required_non_claim in [
            "does not use production/private personal signing keys",
            "does not make the registry fixture provenance object verified",
            "does not claim SLSA compliance",
        ]:
            self.assertIn(required_non_claim, evidence["non_claims"])
        blob = json.dumps(evidence).lower()
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, blob)

        blob = json.dumps(index).lower()
        for forbidden_overclaim in [
            "radicle durable public seed/network availability verified",
            "nostr durability or global propagation verified",
            "production readiness verified",
            "full nip-34 or forge compatibility verified",
        ]:
            self.assertIn(forbidden_overclaim, blob)
        for accidental_secret_marker in ["nsec1", "-----begin", "private key:", "seed phrase:"]:
            self.assertNotIn(accidental_secret_marker, blob)

    def test_required_top_level_fields(self):
        for fixture in self.fixtures:
            with self.subTest(project=fixture["project"]["id"]):
                for field in self.schema["required"]:
                    self.assertIn(field, fixture)

    def test_no_unknown_top_level_fields_in_fixtures(self):
        allowed = set(self.schema["properties"])
        for fixture in self.fixtures:
            with self.subTest(project=fixture["project"]["id"]):
                self.assertLessEqual(set(fixture), allowed)

    def test_schema_allows_explicit_verification_state_labels(self):
        verification_states = self.schema["properties"].get("verification_states")
        self.assertIsInstance(verification_states, dict)
        self.assertEqual(verification_states["type"], "array")
        item_schema = verification_states["items"]
        for field in ["scope", "state", "evidence", "live_verified", "synthetic", "claim_boundary"]:
            self.assertIn(field, item_schema["required"])
            self.assertIn(field, item_schema["properties"])
        self.assertEqual(
            set(item_schema["properties"]["state"]["enum"]),
            {"local-fixture", "source-inspected-mapping", "synthetic-fixture", "live-unverified", "live-verified"},
        )

    def test_fixtures_include_non_overclaiming_verification_states(self):
        allowed_states = {"local-fixture", "source-inspected-mapping", "synthetic-fixture", "live-unverified", "live-verified"}
        for fixture in self.fixtures:
            with self.subTest(project=fixture["project"]["id"]):
                states = fixture.get("verification_states", [])
                self.assertGreaterEqual(len(states), 3)
                by_scope = {state["scope"]: state for state in states}
                self.assertIn("registry.renderer", by_scope)
                self.assertIn("radicle.mapping", by_scope)
                self.assertIn("artifact-metadata.ipfs", by_scope)
                self.assertIn("ci.provenance", by_scope)
                for state in states:
                    self.assertIn(state["state"], allowed_states)
                    self.assertIsInstance(state["live_verified"], bool)
                    self.assertIsInstance(state["synthetic"], bool)
                    self.assertTrue(state["evidence"])
                    self.assertTrue(state["claim_boundary"])
                    if state["state"] != "live-verified":
                        self.assertFalse(state["live_verified"])

    def test_protocol_verification_states_do_not_claim_unverified_live_support(self):
        protocol_scopes = ("nostr", "nip34", "radicle", "ipfs", "artifact-metadata", "ci.provenance", "sigstore")
        forbidden_claims = [
            "censorship-proof",
            "production ready",
            "slsa-compliant",
            "sigstore-verified",
            "in-toto-verified",
            "durably stored",
            "pinned and available",
            "relay-accepted",
        ]
        for fixture in self.fixtures:
            for state in fixture.get("verification_states", []):
                with self.subTest(project=fixture["project"]["id"], scope=state["scope"]):
                    if any(marker in state["scope"] for marker in protocol_scopes):
                        self.assertFalse(state["live_verified"])
                        self.assertNotEqual(state["state"], "live-verified")
                    text = json.dumps(state).lower()
                    for claim in forbidden_claims:
                        self.assertNotIn(claim, text)

    def test_required_project_fields(self):
        for fixture in self.fixtures:
            with self.subTest(project=fixture["project"]["id"]):
                project = fixture["project"]
                for field in ["id", "name", "description", "default_branch"]:
                    self.assertIn(field, project)
                    self.assertTrue(project[field])

    def test_maintainers_and_clone_urls_cover_mvp(self):
        allowed_maintainer_types = {"nostr", "radicle", "did", "ssh", "other"}
        allowed_clone_transports = {"git", "https", "ssh", "radicle", "nostr", "other"}
        for fixture in self.fixtures:
            with self.subTest(project=fixture["project"]["id"]):
                maintainers = fixture["maintainers"]
                clone_urls = fixture["clone_urls"]
                self.assertGreaterEqual(len(maintainers), 1)
                self.assertGreaterEqual(len(clone_urls), 1)
                for maintainer in maintainers:
                    self.assertIn(maintainer["id_type"], allowed_maintainer_types)
                    self.assertTrue(maintainer["public_id"])
                for clone in clone_urls:
                    self.assertIn(clone["transport"], allowed_clone_transports)
                    self.assertTrue(clone["url"])
                self.assertTrue(any(clone["url"].startswith("file://") for clone in clone_urls))

    def test_fixture_includes_collaboration_and_release_data(self):
        for fixture in self.fixtures:
            with self.subTest(project=fixture["project"]["id"]):
                self.assertGreaterEqual(len(fixture.get("issues", [])), 1)
                self.assertGreaterEqual(len(fixture.get("patches", [])), 1)
                self.assertGreaterEqual(len(fixture.get("releases", [])), 1)
                artifact = fixture["releases"][0]["artifacts"][0]
                self.assertEqual(len(artifact["sha256"]), 64)

    def test_release_artifact_hashes_and_availability_flags_are_explicit(self):
        hex64 = re.compile(r"^[0-9a-f]{64}$")
        for fixture, release, artifact in self.iter_artifacts():
            with self.subTest(project=fixture["project"]["id"], release=release["version"], artifact=artifact["name"]):
                self.assertRegex(artifact["sha256"], hex64)
                self.assertEqual(artifact["hashes"]["sha256"], artifact["sha256"])

                availability = artifact["availability"]
                self.assertFalse(availability["pinned"])
                self.assertFalse(availability["live_ipfs_verified"])
                self.assertFalse(availability["paid_storage"])
                self.assertFalse(availability["durability_claim"])

    def test_local_fixture_file_artifacts_exist_and_hashes_match(self):
        for fixture, release, artifact in self.iter_artifacts():
            with self.subTest(project=fixture["project"]["id"], release=release["version"], artifact=artifact["name"]):
                availability = artifact["availability"]

                if not availability["local_fixture"]:
                    self.assertFalse(availability["pinned"])
                    self.assertFalse(availability["live_ipfs_verified"])
                    self.assertFalse(availability["paid_storage"])
                    self.assertFalse(availability["durability_claim"])
                    continue

                uri = artifact["uri"]
                if not uri.startswith("file://"):
                    continue

                artifact_path = self.fixture_file_uri_path(uri)
                self.assertTrue(artifact_path.is_file(), f"missing local fixture artifact: {artifact_path}")

                actual_sha256 = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
                self.assertEqual(artifact["sha256"], actual_sha256)
                self.assertEqual(artifact["hashes"]["sha256"], actual_sha256)

    def test_local_release_fixture_hash_and_cid_are_computed_but_not_published(self):
        content = LOCAL_RELEASE_ARTIFACT_PATH.read_bytes()
        expected_sha256 = hashlib.sha256(content).hexdigest()
        expected_cid = self.local_raw_cidv1_for_bytes(content)

        artifact = self.fixture["releases"][0]["artifacts"][0]
        self.assertEqual(artifact["name"], "local-release-artifact.txt")
        self.assertEqual(artifact["size_bytes"], len(content))
        self.assertEqual(artifact["sha256"], expected_sha256)
        self.assertEqual(artifact["hashes"]["sha256"], expected_sha256)

        content_addresses = artifact["content_addresses"]
        self.assertEqual(len(content_addresses), 1)
        address = content_addresses[0]
        self.assertEqual(address["protocol"], "ipfs")
        self.assertEqual(address["cid"], expected_cid)
        self.assertEqual(artifact["cid"], expected_cid)
        self.assertRegex(address["cid"], CIDV1_BASE32_RE)
        self.assertEqual(address["cid_version"], 1)
        self.assertEqual(address["multibase"], "base32")
        self.assertEqual(address["multicodec"], "raw")
        self.assertEqual(address["multihash"], "sha2-256")
        self.assertTrue(address["derived_from_local_fixture"])
        self.assertTrue(address["matches_artifact_hash"])
        self.assertEqual(address["verification_status"], "local-computed-not-fetched")

        ipfs = self.fixture["substrates"]["ipfs"]
        self.assertIn(expected_cid, ipfs["artifact_cids"])
        self.assertEqual(ipfs["pinning_status"], "not-pinned")
        self.assertFalse(ipfs["live_ipfs_verified"])
        self.assertFalse(ipfs["paid_storage"])
        self.assertFalse(ipfs["durability_claim"])

    def test_fixture_includes_required_substrate_hints(self):
        substrates = self.fixture["substrates"]
        for key in ["nip34", "radicle", "forgefed", "ipfs", "sigstore_slsa"]:
            self.assertIn(key, substrates)

    def test_loop7_ci_checks_are_synthetic_local_and_sensible(self):
        checks = self.fixture["ci_checks"]
        self.assertGreaterEqual(len(checks), 1)
        allowed_status = {"queued", "in_progress", "completed", "cancelled", "skipped"}
        terminal_status = {"completed", "cancelled", "skipped"}
        allowed_conclusion = {"success", "failure", "neutral", "cancelled", "skipped", "timed_out", "action_required"}
        ids = set()

        for check in checks:
            with self.subTest(check=check["id"]):
                self.assertNotIn(check["id"], ids)
                ids.add(check["id"])
                self.assertEqual(check["provider"], "local-fake")
                self.assertIn(check["status"], allowed_status)
                self.assertIn(check["conclusion"], allowed_conclusion)
                self.assertTrue(check["synthetic"])
                self.assertFalse(check["published"])
                self.assertRegex(check["commit"], r"^[0-9a-f]{40}$")
                self.assertTrue(check["repository"].startswith("file://"))
                self.assertLessEqual(check["started_at"], check["completed_at"])
                if check["conclusion"] == "success":
                    self.assertIn(check["status"], terminal_status)
                self.assertIn("Synthetic", check["notes"])
                self.assertNotIn("github.com/", check.get("url", ""))

    def test_loop7_fake_attestation_links_artifact_commit_repo_and_ci_checks(self):
        artifact = self.fixture["releases"][0]["artifacts"][0]
        provenance = artifact["provenance"]
        ci_checks = {check["id"]: check for check in self.fixture["ci_checks"]}

        self.assertEqual(provenance["status"], "synthetic-local-only")
        self.assertTrue(provenance["synthetic"])
        self.assertEqual(provenance["artifact_name"], artifact["name"])
        self.assertEqual(provenance["artifact_sha256"], artifact["sha256"])
        self.assertEqual(provenance["tag"], self.fixture["releases"][0]["tag"])
        self.assertTrue(provenance["repository"].startswith("file://"))
        self.assertRegex(provenance["commit"], r"^[0-9a-f]{40}$")
        self.assertIn(provenance["artifact_sha256"], artifact["attestation"])
        self.assertIn(provenance["commit"], artifact["attestation"])
        self.assertIn("synthetic=true", artifact["attestation"])
        self.assertIn("no-slsa-claim=true", artifact["attestation"])

        for material in provenance["materials"]:
            self.assertIn(provenance["commit"], material["uri"])
            self.assertEqual(material["digest"].get("gitCommit"), provenance["commit"])

        self.assertGreaterEqual(len(provenance["ci_check_ids"]), 1)
        for check_id in provenance["ci_check_ids"]:
            self.assertIn(check_id, ci_checks)
            check = ci_checks[check_id]
            self.assertEqual(check["commit"], provenance["commit"])
            self.assertEqual(check["repository"], provenance["repository"])
            self.assertEqual(check["status"], "completed")
            self.assertEqual(check["conclusion"], "success")

    def test_loop7_no_real_signatures_keys_or_slsa_claims(self):
        artifact = self.fixture["releases"][0]["artifacts"][0]
        provenance = artifact["provenance"]
        verification = provenance["verification"]
        sigstore = self.fixture["substrates"]["sigstore_slsa"]

        self.assertEqual(self.fixture["signature"]["status"], "unsigned-fixture")
        self.assertEqual(self.fixture["signature"]["algorithm"], "none")
        self.assertEqual(self.fixture["signature"]["value"], "")
        self.assertEqual(artifact["signature"], "unsigned-fixture")
        self.assertTrue(verification["local_schema_only"])
        for field in [
            "real_sigstore_verified",
            "real_in_toto_verified",
            "slsa_level_claimed",
            "uses_real_signature",
            "uses_private_key",
        ]:
            self.assertFalse(verification[field])
        for field in [
            "real_sigstore_verified",
            "real_cosign_verified",
            "real_in_toto_verified",
            "slsa_level_claimed",
            "rekor_uploaded",
            "private_keys_used",
        ]:
            self.assertFalse(sigstore[field])
        self.assertEqual(sigstore["production_claim"], "none")
        self.assertIn("no-real-signature", provenance["boundaries"])
        self.assertIn("no-private-key", provenance["boundaries"])
        self.assertIn("no-slsa-level-claim", provenance["boundaries"])

    def test_radicle_fixture_models_source_inspected_local_spike(self):
        fixture = self.radicle_fixture
        radicle = fixture["substrates"]["radicle"]

        self.assertTrue(fixture["project"]["id"].startswith("rad:z"))
        self.assertEqual(radicle["rid"], fixture["project"]["id"])
        self.assertTrue(any(clone["transport"] == "radicle" for clone in fixture["clone_urls"]))
        self.assertTrue(any(maintainer["id_type"] == "radicle" for maintainer in fixture["maintainers"]))

        verification = radicle["local_verification"]
        self.assertTrue(verification["source_inspected"])
        self.assertFalse(verification["cli_installed"])
        self.assertFalse(verification["live_cli_verified"])
        self.assertFalse(verification["published"])

        source = radicle["source_evidence"]
        self.assertEqual(source["repo_path"], "/tmp/radicle-heartwood")
        self.assertEqual(source["commit"], "90aaec1c9eee77a0beebece48f460c1424c1c8bd")
        self.assertIn("rad-id.1.adoc", source["files"])
        self.assertIn("rad-patch.1.adoc", source["files"])

    def test_radicle_fixture_preserves_identity_issue_and_patch_mapping(self):
        radicle = self.radicle_fixture["substrates"]["radicle"]
        identity = radicle["identity_payload"]

        self.assertEqual(identity["project_payload"], "xyz.radicle.project")
        self.assertEqual(identity["threshold"], 1)
        self.assertGreaterEqual(len(identity["delegates"]), 1)
        self.assertIn("refs/heads/master", identity["canonical_refs"])
        self.assertIn("refs/tags/*", identity["canonical_refs"])

        issue = radicle["issues"][0]
        self.assertEqual(issue["radicle_status"], "open")
        self.assertEqual(issue["registry_status"], self.radicle_fixture["issues"][0]["status"])
        self.assertIn("rad issue open", issue["source_command_shape"])

        patch = radicle["patches"][0]
        self.assertEqual(patch["source_ref"], "refs/patches")
        self.assertEqual(patch["registry_status"], self.radicle_fixture["patches"][0]["status"])
        self.assertIn("git push rad", patch["open_command_shape"])

    def _tags_by_name(self, event):
        grouped = {}
        for tag in event["tags"]:
            self.assertIsInstance(tag, list)
            self.assertGreaterEqual(len(tag), 2)
            grouped.setdefault(tag[0], []).append(tag)
        return grouped

    def test_nostr_collaboration_fixture_preserves_issue_and_patch_shapes(self):
        fixture = self.nostr_collab_fixture
        self.assertEqual(fixture["source_registry"], "fixtures/example-project.registry.json")
        self.assertEqual(fixture["relay_tool_check"]["fallback"], "dry-run-fixtures")
        self.assertFalse(fixture["relay_tool_check"]["usable_local_relay_found"])
        self.assertEqual(fixture["synthetic_key_policy"]["private_keys"], "none")

        events = fixture["events"]
        self.assertEqual([event["kind"] for event in events], [1621, 1617])
        self.assertEqual([event["mapped_registry_path"] for event in events], ["issues[0]", "patches[0]"])

        registry_issue = self.fixture["issues"][0]
        registry_patch = self.fixture["patches"][0]
        issue_event, patch_event = events

        self.assertIn(registry_issue["summary"], issue_event["content"])
        self.assertIn(registry_patch["summary"], patch_event["content"])
        self.assertIn("diff --git", patch_event["content"])

        for event in events:
            tags = self._tags_by_name(event)
            self.assertEqual(event["nip"], 34)
            self.assertIn("a", tags)
            self.assertIn(fixture["repo_address"], [tag[1] for tag in tags["a"]])
            self.assertIn("subject", tags)
            self.assertIn("status", tags)
            self.assertTrue(event["id"].startswith("dry-run-"))
            self.assertTrue(event["sig"].startswith("dry-run-"))
            self.assertRegex(event["pubkey"], r"^[012]+$")
            self.assertEqual(len(event["pubkey"]), 64)

    def test_nostr_fixture_documents_nip35_boundary(self):
        boundary = self.nostr_collab_fixture["nip35_boundary"]
        self.assertEqual(boundary["status"], "documented-no-collaboration-event")
        self.assertIn("artifact metadata", boundary["reason"])
        self.assertIn("does not define repository issue or patch", boundary["reason"])

    def test_nip34_adapter_round_trips_repo_announcement_to_registry_concepts(self):
        exported = nip34_adapter.export_fixture_pair(
            self.nostr_repo_fixture,
            self.nostr_collab_fixture,
        )

        self.assertEqual(exported["project"]["id"], self.fixture["project"]["id"])
        self.assertEqual(exported["project"]["name"], self.fixture["project"]["name"])
        self.assertEqual(exported["project"]["description"], self.fixture["project"]["description"])
        self.assertEqual(exported["project"]["web_urls"], self.fixture["project"]["web_urls"])
        self.assertEqual(
            [clone["url"] for clone in exported["clone_urls"]],
            [clone["url"] for clone in self.fixture["clone_urls"]],
        )
        self.assertEqual(
            exported["maintainers"],
            [
                {
                    "id_type": "nostr",
                    "public_id": self.fixture["maintainers"][0]["public_id"],
                    "role": "maintainer",
                }
            ],
        )
        self.assertEqual(exported["substrates"]["nip34"]["repository_kind"], 30617)
        self.assertEqual(exported["substrates"]["nip34"]["repo_id_tag"], self.fixture["project"]["id"])
        self.assertEqual(exported["substrates"]["nip34"]["relay_hints"], ["wss://relay.example.invalid"])
        self.assertEqual(exported["substrates"]["nip34"]["publish_status"], "dry-run-only")

    def test_nip34_adapter_round_trips_issue_and_patch_content_mappings(self):
        exported = nip34_adapter.export_fixture_pair(
            self.nostr_repo_fixture,
            self.nostr_collab_fixture,
        )

        self.assertEqual(len(exported["issues"]), 1)
        self.assertEqual(len(exported["patches"]), 1)
        issue = exported["issues"][0]
        patch = exported["patches"][0]
        registry_issue = self.fixture["issues"][0]
        registry_patch = self.fixture["patches"][0]

        self.assertEqual(issue["id"], "dry-run-issue-event-id-not-computed")
        self.assertEqual(issue["title"], registry_issue["title"])
        self.assertEqual(issue["status"], registry_issue["status"])
        self.assertEqual(issue["summary"], registry_issue["summary"])
        self.assertEqual(issue["source_event_kind"], 1621)
        self.assertEqual(issue["repository"], self.nostr_collab_fixture["repo_address"])
        self.assertIn("Dry-run issue body only", issue["content"])

        self.assertEqual(patch["id"], "dry-run-patch-event-id-not-computed")
        self.assertEqual(patch["title"], registry_patch["title"])
        self.assertEqual(patch["status"], registry_patch["status"])
        self.assertEqual(patch["summary"], registry_patch["summary"])
        self.assertEqual(patch["source_event_kind"], 1617)
        self.assertEqual(patch["repository"], self.nostr_collab_fixture["repo_address"])
        self.assertIn("diff --git", patch["content"])

    def test_nip34_adapter_preserves_dry_run_non_claim_fields(self):
        exported = nip34_adapter.export_fixture_pair(
            self.nostr_repo_fixture,
            self.nostr_collab_fixture,
        )

        dry_run = exported["dry_run"]
        self.assertEqual(dry_run["repository"]["id"], "dry-run-not-computed")
        self.assertEqual(dry_run["repository"]["sig"], "dry-run-not-signed")
        self.assertIn("Not published", dry_run["repository"]["notice"])
        self.assertEqual(dry_run["collaboration"]["relay_tool_check"]["fallback"], "dry-run-fixtures")
        self.assertFalse(dry_run["collaboration"]["relay_tool_check"]["usable_local_relay_found"])
        self.assertEqual(dry_run["collaboration"]["synthetic_key_policy"]["private_keys"], "none")
        self.assertEqual(dry_run["collaboration"]["nip35_boundary"]["status"], "documented-no-collaboration-event")
        self.assertEqual([event["published"] for event in dry_run["events"]], [False, False])
        self.assertTrue(all(event["id"].startswith("dry-run-") for event in dry_run["events"]))
        self.assertTrue(all(event["sig"].startswith("dry-run-") for event in dry_run["events"]))

    def test_nip34_conformance_reports_cover_dry_run_event_shapes(self):
        exported = nip34_adapter.export_fixture_pair(
            self.nostr_repo_fixture,
            self.nostr_collab_fixture,
            self.nostr_state_status_fixture,
        )

        conformance = exported["dry_run"]["conformance"]
        self.assertEqual(conformance["scope"], "local-dry-run-fixtures-only")
        reports = conformance["reports"]
        self.assertEqual(
            [report["label"] for report in reports],
            [
                "repository_announcement",
                "demo-project-issue-1",
                "demo-project-patch-1",
                "repository_state_event",
            ],
        )
        self.assertEqual([report["kind"] for report in reports], [30617, 1621, 1617, 30618])

        source_events = [
            self.nostr_repo_fixture,
            *self.nostr_collab_fixture["events"],
            self.nostr_state_status_fixture["repository_state_event"],
        ]
        for report, event in zip(reports, source_events):
            with self.subTest(label=report["label"]):
                shape = report["shape"]
                self.assertTrue(report["nip34_kind_known"])
                self.assertTrue(shape["required_fields_present"])
                self.assertTrue(shape["valid_for_local_fixture"])
                self.assertTrue(shape["pubkey_is_lower_hex_64"])
                self.assertTrue(shape["pubkey_is_fixture_synthetic"])
                self.assertTrue(shape["created_at_is_int"])
                self.assertTrue(shape["kind_is_int"])
                self.assertTrue(shape["tags_are_arrays_of_strings"])
                self.assertTrue(shape["content_is_string"])
                self.assertEqual(shape["errors"], [])
                self.assertTrue(report["id_is_placeholder"])
                self.assertTrue(report["sig_is_placeholder"])
                self.assertFalse(report["event_id_computed"])
                self.assertFalse(report["signed"])
                self.assertFalse(report["published"])
                self.assertRegex(report["possible_event_id"], r"^[0-9a-f]{64}$")
                serialized = json.dumps(
                    [0, event["pubkey"], event["created_at"], event["kind"], event["tags"], event["content"]],
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
                self.assertEqual(report["serialized_event_payload"], serialized)
                self.assertEqual(report["possible_event_id"], hashlib.sha256(serialized.encode("utf-8")).hexdigest())
                self.assertNotEqual(report["possible_event_id"], event["id"])

    def test_nip34_adapter_exports_verification_states_vocabulary(self):
        exported = nip34_adapter.export_fixture_pair(
            self.nostr_repo_fixture,
            self.nostr_collab_fixture,
            self.nostr_state_status_fixture,
        )
        states = exported["verification_states"]
        self.assertEqual(
            [state["scope"] for state in states],
            [
                "nip34.adapter.repository_announcement",
                "nip34.adapter.collaboration_events",
                "nip34.adapter.conformance_reports",
                "nip34.adapter.repository_state",
                "nip34.adapter.status_checks",
            ],
        )
        allowed_states = {"local-fixture", "source-inspected-mapping", "synthetic-fixture"}
        forbidden_claims = [
            "censorship-proof",
            "production ready",
            "slsa-compliant",
            "sigstore-verified",
            "in-toto-verified",
            "durably stored",
            "pinned and available",
            "relay-accepted",
            "live-verified",
        ]
        for state in states:
            with self.subTest(scope=state["scope"]):
                for field in ["scope", "state", "evidence", "live_verified", "synthetic", "claim_boundary"]:
                    self.assertIn(field, state)
                self.assertIn(state["state"], allowed_states)
                self.assertFalse(state["live_verified"])
                self.assertTrue(state["synthetic"])
                self.assertIn("nip34_adapter.py", state["claim_boundary"])
                self.assertIn("2026-06-22", state["last_checked_at"])
                self.assertTrue(state["evidence"])
                self.assertTrue(state["notes"])
                text = json.dumps(state).lower()
                for claim in forbidden_claims:
                    self.assertNotIn(claim, text)

    def test_nip01_event_shape_rejects_invalid_tag_and_content_shapes(self):
        invalid = json.loads(json.dumps(self.nostr_repo_fixture))
        invalid["tags"] = [["d", "demo-project"], ["bad", 123]]
        invalid["content"] = {"not": "a string"}

        shape = nip34_adapter.validate_nip01_event_shape(invalid)
        report = nip34_adapter.conformance_report(invalid, label="invalid")

        self.assertFalse(shape["valid_for_local_fixture"])
        self.assertFalse(shape["tags_are_arrays_of_strings"])
        self.assertFalse(shape["content_is_string"])
        self.assertIn("tags[1] values must be strings", shape["errors"])
        self.assertIn("content must be a string", shape["errors"])
        self.assertIsNone(nip34_adapter.possible_event_id(invalid))
        self.assertIsNone(report["possible_event_id"])
        self.assertIsNone(report["serialized_event_payload"])
        self.assertFalse(report["event_id_computed"])
        with self.assertRaisesRegex(ValueError, "not eligible"):
            nip34_adapter.nip01_serialized_event_payload(invalid)

    def test_nip01_event_shape_rejects_bool_integer_fields(self):
        for field in ["created_at", "kind"]:
            with self.subTest(field=field):
                invalid = json.loads(json.dumps(self.nostr_repo_fixture))
                invalid[field] = True

                shape = nip34_adapter.validate_nip01_event_shape(invalid)
                report = nip34_adapter.conformance_report(invalid, label=f"bool-{field}")

                self.assertFalse(shape["valid_for_local_fixture"])
                self.assertFalse(shape[f"{field}_is_int"])
                self.assertIn(f"{field} must be an int", shape["errors"])
                self.assertIsNone(nip34_adapter.possible_event_id(invalid))
                self.assertIsNone(report["possible_event_id"])
                self.assertIsNone(report["serialized_event_payload"])
                self.assertFalse(report["event_id_computed"])

    def test_nip01_event_shape_rejects_missing_pubkey_and_non_list_tags(self):
        missing_pubkey = json.loads(json.dumps(self.nostr_repo_fixture))
        missing_pubkey.pop("pubkey")
        missing_shape = nip34_adapter.validate_nip01_event_shape(missing_pubkey)
        missing_report = nip34_adapter.conformance_report(missing_pubkey, label="missing-pubkey")

        self.assertFalse(missing_shape["required_fields_present"])
        self.assertFalse(missing_shape["valid_for_local_fixture"])
        self.assertIn("missing required field: pubkey", missing_shape["errors"])
        self.assertIsNone(nip34_adapter.possible_event_id(missing_pubkey))
        self.assertIsNone(missing_report["possible_event_id"])

        non_list_tags = json.loads(json.dumps(self.nostr_repo_fixture))
        non_list_tags["tags"] = {"not": "a list"}
        tags_shape = nip34_adapter.validate_nip01_event_shape(non_list_tags)
        tags_report = nip34_adapter.conformance_report(non_list_tags, label="non-list-tags")

        self.assertFalse(tags_shape["valid_for_local_fixture"])
        self.assertFalse(tags_shape["tags_are_arrays_of_strings"])
        self.assertIn("tags must be a list", tags_shape["errors"])
        self.assertIsNone(nip34_adapter.possible_event_id(non_list_tags))
        self.assertIsNone(tags_report["possible_event_id"])

    def test_renderer_outputs_expected_html(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "demo.html"
            result = subprocess.run(
                [sys.executable, str(RENDERER), str(FIXTURE_PATH), str(output)],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            html = output.read_text(encoding="utf-8")
            self.assertIn("Demo Decentralized Forge Project", html)
            self.assertIn("Maintainers", html)
            self.assertIn("Clone URLs", html)
            self.assertIn("Protocol substrate details", html)
            self.assertIn("CI / provenance checks", html)
            self.assertIn("Verification states", html)
            self.assertIn("Verification labels", html)
            self.assertIn("Registry verification states summary", html)
            self.assertIn("Counts by state", html)
            self.assertIn("Counts by live verification flag", html)
            self.assertIn("Counts by synthetic flag", html)
            self.assertIn("Claim-boundary summary", html)
            self.assertIn("Registry verification rows grouped by state", html)
            self.assertIn("<dt>Verification row count</dt><dd><code>5</code></dd>", html)
            self.assertIn("<dt>Live-verified row count</dt><dd><code>0</code></dd>", html)
            self.assertIn("<dt>Live-unverified or local row count</dt><dd><code>5</code></dd>", html)
            self.assertIn("<dt>Synthetic row count</dt><dd><code>3</code></dd>", html)
            self.assertIn("local-fixture</span>: <strong>2</strong>", html)
            self.assertIn("source-inspected-mapping</span>: <strong>1</strong>", html)
            self.assertIn("synthetic-fixture</span>: <strong>2</strong>", html)
            self.assertIn("live_verified=false</span>: <strong>5</strong>", html)
            self.assertIn("verification-state-local-fixture", html)
            self.assertNotIn("live_verified=true</span>: <strong>1</strong>", html)
            self.assertIn("artifact-metadata.ipfs", html)
            self.assertIn("A scope is not live-verified unless its row says so explicitly", html)
            self.assertIn("Artifact availability", html)
            self.assertIn("Content addresses", html)
            self.assertIn("Provenance / attestation", html)
            self.assertIn("Prototype boundary", html)
            self.assertIn("does not claim production readiness", html)
            self.assertIn("No SLSA level claimed", html)
            self.assertIn("Published publicly", html)
            self.assertIn("Live IPFS verified", html)
            self.assertIn("Durability claim", html)
            self.assertIn("local-fake-ci-001", html)
            self.assertIn("synthetic-local-only", html)
            self.assertIn("bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua", html)
            self.assertIn("sigstore_slsa", html)
            self.assertIn("local-release-artifact.txt", html)

    def test_nip34_repository_state_fixture_maps_recorded_git_head(self):
        fixture = self.nostr_state_status_fixture
        fixture_head = fixture["source_git_head"]
        self.assertRegex(fixture_head, r"^[0-9a-f]{40}$")
        self.git_commit_exists(fixture_head)
        self.assert_fixture_head_is_current_or_ancestor(fixture_head)
        event = fixture["repository_state_event"]
        tags = self._tags_by_name(event)

        self.assertEqual(event["kind"], 30618)
        self.assertEqual(tags["d"][0][1], self.fixture["project"]["id"])
        self.assertEqual(tags["HEAD"][0][1], "ref: refs/heads/main")
        self.assertEqual(tags["refs/heads/main"][0][1], fixture_head)
        self.assertIn(fixture["repo_address"], [tag[1] for tag in tags["a"]])

        exported = nip34_adapter.export_fixture_pair(
            self.nostr_repo_fixture,
            self.nostr_collab_fixture,
            self.nostr_state_status_fixture,
        )
        state = exported["repository_state"]
        self.assertEqual(state["kind"], 30618)
        self.assertEqual(state["repo_id_tag"], self.fixture["project"]["id"])
        self.assertEqual(state["head"], "ref: refs/heads/main")
        self.assertEqual(state["head_ref"], "refs/heads/main")
        self.assertEqual(state["head_commit"], fixture_head)
        self.assertEqual(state["refs"], {"refs/heads/main": fixture_head})

    def test_nip34_state_status_fixture_preserves_local_only_non_claims(self):
        exported = nip34_adapter.export_fixture_pair(
            self.nostr_repo_fixture,
            self.nostr_collab_fixture,
            self.nostr_state_status_fixture,
        )
        dry_run = exported["dry_run"]
        state_event = dry_run["repository_state_event"]
        state_status = dry_run["state_status"]
        non_claims = state_status["non_claims"]

        self.assertEqual(state_event["id"], "dry-run-repo-state-id-not-computed")
        self.assertEqual(state_event["sig"], "dry-run-repo-state-not-signed")
        self.assertFalse(state_event["published"])
        self.assertIn("Not published", state_status["notice"])
        for field in [
            "published",
            "relay_published",
            "relay_fetched",
            "event_id_computed",
            "signed",
            "private_keys_used",
            "public_ci_status_created",
            "live_nip_status_semantics_claimed",
        ]:
            self.assertFalse(non_claims[field])

        checks = exported["status_checks"]
        self.assertEqual([check["source_ci_check_id"] for check in checks], ["local-fake-ci-001", "local-fake-ci-002"])
        for check in checks:
            self.assertEqual(check["target_commit"], exported["repository_state"]["head_commit"])
            self.assertEqual(check["target_ref"], "refs/heads/main")
            self.assertTrue(check["synthetic"])
            self.assertFalse(check["published"])
            self.assertIn("Fixture-only", check["notes"])
            self.assertIn("no", check["notes"].lower())

    def test_nip34_state_status_rejects_status_checks_for_other_commits_or_refs(self):
        mismatched_commit = json.loads(json.dumps(self.nostr_state_status_fixture))
        mismatched_commit["status_checks"][0]["target_commit"] = "f" * 40
        with self.assertRaisesRegex(ValueError, "target_commit"):
            nip34_adapter.export_fixture_pair(
                self.nostr_repo_fixture,
                self.nostr_collab_fixture,
                mismatched_commit,
            )

        mismatched_ref = json.loads(json.dumps(self.nostr_state_status_fixture))
        mismatched_ref["status_checks"][0]["target_ref"] = "refs/heads/other"
        with self.assertRaisesRegex(ValueError, "target_ref"):
            nip34_adapter.export_fixture_pair(
                self.nostr_repo_fixture,
                self.nostr_collab_fixture,
                mismatched_ref,
            )

    def test_renderer_can_include_local_nip34_adapter_fixture_section(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "demo.html"
            result = subprocess.run(
                [
                    sys.executable,
                    str(RENDERER),
                    str(FIXTURE_PATH),
                    str(output),
                    "--nip34-repo-fixture",
                    str(NOSTR_REPO_FIXTURE_PATH),
                    "--nip34-collaboration-fixture",
                    str(NOSTR_COLLAB_FIXTURE_PATH),
                    "--nip34-state-status-fixture",
                    str(NOSTR_STATE_STATUS_FIXTURE_PATH),
                    "--nip34-live-readback-fixture",
                    str(NOSTR_LIVE_READBACK_FIXTURE_PATH),
                    "--live-evidence-index",
                    str(LIVE_EVIDENCE_INDEX_PATH),
                ],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            html = output.read_text(encoding="utf-8")
            self.assertIn("NIP-34 fixture adapter", html)
            self.assertIn("local parser/conformance output", html)
            self.assertIn("Dry-run rows do not perform relay publishing, signing, fixture ID replacement, relay fetching, or live verification", html)
            self.assertIn("possible_event_id values are local reference hashes only", html)
            self.assertIn("Local NIP-34 conformance summary", html)
            self.assertIn("Adapter verification states", html)
            self.assertIn("Adapter-local verification labels", html)
            self.assertIn("Adapter verification states summary", html)
            self.assertIn("Adapter verification rows grouped by state", html)
            self.assertIn("<dt>Verification row count</dt><dd><code>6</code></dd>", html)
            self.assertIn("<dt>Live-verified row count</dt><dd><code>1</code></dd>", html)
            self.assertIn("<dt>Live-unverified or local row count</dt><dd><code>5</code></dd>", html)
            self.assertIn("<dt>Synthetic row count</dt><dd><code>5</code></dd>", html)
            self.assertIn("local-fixture</span>: <strong>3</strong>", html)
            self.assertIn("source-inspected-mapping</span>: <strong>1</strong>", html)
            self.assertIn("synthetic-fixture</span>: <strong>1</strong>", html)
            self.assertIn("live-verified</span>: <strong>1</strong>", html)
            self.assertIn("live_verified=true</span>: <strong>1</strong>", html)
            self.assertIn("live_verified=false</span>: <strong>5</strong>", html)
            self.assertIn("nip34.adapter.repository_announcement", html)
            self.assertIn("nip34.adapter.collaboration_events", html)
            self.assertIn("nip34.adapter.conformance_reports", html)
            self.assertIn("nip34.adapter.repository_state", html)
            self.assertIn("nip34.adapter.status_checks", html)
            self.assertIn("nip34.adapter.live_repository_announcement_readback", html)
            self.assertIn("They are separate from the top-level registry verification states", html)
            self.assertIn("dry_run.conformance.reports[]", html)
            self.assertIn("Conformance report count", html)
            self.assertIn("<dt>Conformance report count</dt><dd><code>4</code></dd>", html)
            self.assertIn("Known NIP-34 kind count", html)
            self.assertIn("<dt>Known NIP-34 kind count</dt><dd><code>4</code></dd>", html)
            self.assertIn("Conformance: repository_announcement", html)
            self.assertIn("Conformance: demo-project-issue-1", html)
            self.assertIn("Conformance: demo-project-patch-1", html)
            self.assertIn("Conformance: repository_state_event", html)
            self.assertIn("Valid for local fixture", html)
            self.assertIn("ID is placeholder", html)
            self.assertIn("Signature is placeholder", html)
            self.assertIn("Signed", html)
            self.assertIn("Published", html)
            self.assertIn("Possible event ID (local reference only)", html)
            self.assertIn("they do not replace fixture IDs and are not signed or relay-accepted event ID claims", html)
            exported = nip34_adapter.export_fixture_pair(
                self.nostr_repo_fixture,
                self.nostr_collab_fixture,
                self.nostr_state_status_fixture,
            )
            for report in exported["dry_run"]["conformance"]["reports"]:
                self.assertIn(report["possible_event_id"], html)
            self.assertNotIn("serialized_event_payload", html)
            self.assertNotIn("diff --git a/README.md", html)
            self.assertIn("Repo ID", html)
            self.assertIn("demo-project", html)
            self.assertIn("wss://relay.example.invalid", html)
            self.assertIn("Issue count", html)
            self.assertIn("Patch count", html)
            self.assertIn("Define portable project identity", html)
            self.assertIn("Add static registry renderer", html)
            self.assertIn("dry-run-issue-event-id-not-computed", html)
            self.assertIn("dry-run-patch-event-id-not-computed", html)
            self.assertIn("usable_local_relay_found", html)
            self.assertIn("dry-run-fixtures", html)
            self.assertIn("private_keys", html)
            self.assertIn("none", html)
            self.assertIn("documented-no-collaboration-event", html)
            self.assertIn("Repository state fixture", html)
            self.assertIn("State kind", html)
            self.assertIn("30618", html)
            fixture_head = self.nostr_state_status_fixture["source_git_head"]
            self.assertIn(fixture_head, html)
            self.assertIn("Fixture-only status/check projections", html)
            self.assertIn("local-fixture-projection", html)
            self.assertIn("public_ci_status_created", html)
            self.assertIn("live_nip_status_semantics_claimed", html)
            self.assertIn("Live evidence index", html)
            self.assertIn("Narrow evidence only", html)
            self.assertIn("loop23-radicle-local-cli-replay", html)
            self.assertIn("loop25-nostr-selected-relay-readback", html)
            self.assertIn("loop34-radicle-disposable-public-smoke", html)
            self.assertIn("loop40-github-keyless-artifact-attestation", html)
            self.assertIn("hosted-keyless-attestation-generated", html)
            self.assertIn("Selected-relay readback verified", html)
            self.assertIn("local-cli-verified", html)
            self.assertIn("selected-relay-readback-verified", html)
            self.assertIn("rad:z33oByNZxkxXAChhD54B4XiSsQkao", html)
            self.assertIn("rad:z2WtozFrCRhygh9CGzyUN57CN7Nwa", html)
            self.assertIn("4cd841ac7d3c15c3e2a0ab1e65b5d704b7032adea2d7dcd171ab613657d48eba", html)
            self.assertIn("not proof of global propagation", html)
            self.assertIn("not proof of broad Radicle network availability", html)
            self.assertIn("Contains secret values", html)
            self.assertIn("NIP-34 live readback import", html)
            self.assertIn("Selected-relay readback only", html)
            self.assertIn("Loop 29 performs no new relay publish/fetch/signing", html)
            self.assertIn("Live readback event: loop25-live-repository-announcement", html)
            self.assertIn("New event published in Loop 29", html)
            self.assertIn("decentralized-forge-live-adapter-prototype-2026-06-22", html)

    def test_renderer_requires_nip34_fixture_args_as_a_pair(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "demo.html"
            result = subprocess.run(
                [
                    sys.executable,
                    str(RENDERER),
                    str(FIXTURE_PATH),
                    str(output),
                    "--nip34-repo-fixture",
                    str(NOSTR_REPO_FIXTURE_PATH),
                ],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("must be provided together", result.stderr)

    def test_static_artifact_preflight_accepts_regenerated_all_fixture_output(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "demo-project.html"
            result = preflight_static_artifact.render_to(output)
            self.assertEqual(result.returncode, 0, result.stderr)
            failures = preflight_static_artifact.check_static_artifact(output)
            self.assertEqual(failures, [])

    def test_static_artifact_preflight_rejects_stale_or_overclaiming_output(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "demo-project.html"
            result = preflight_static_artifact.render_to(output)
            self.assertEqual(result.returncode, 0, result.stderr)
            html = output.read_text(encoding="utf-8")
            output.write_text(
                html.replace("Prototype boundary", "Prototype boundary stale")
                + "\nproduction-ready decentralized forge\n",
                encoding="utf-8",
            )
            failures = preflight_static_artifact.check_static_artifact(output)
            self.assertTrue(any("unsupported claim phrase" in failure for failure in failures))
            self.assertTrue(any("generated artifact is stale" in failure for failure in failures))

    def test_static_artifact_preflight_cli_checks_committed_output(self):
        result = subprocess.run(
            [sys.executable, str(STATIC_PREFLIGHT)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Static artifact preflight passed", result.stdout)
        self.assertTrue(OUTPUT_DEMO_HTML.is_file())

    def test_renderer_escapes_fixture_values_in_new_sections(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            registry = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
            registry["project"]["description"] = "<script>alert('project')</script>"
            registry["releases"][0]["artifacts"][0]["name"] = "artifact <unsafe> & demo"
            registry["ci_checks"][0]["notes"] = "CI note <b>not html</b>"
            registry["substrates"]["ipfs"]["cid_status"] = "<not-fetched>"

            input_path = tmp / "registry.json"
            output = tmp / "demo.html"
            input_path.write_text(json.dumps(registry), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(RENDERER), str(input_path), str(output)],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            html = output.read_text(encoding="utf-8")
            self.assertIn("&lt;script&gt;alert(&#x27;project&#x27;)&lt;/script&gt;", html)
            self.assertIn("artifact &lt;unsafe&gt; &amp; demo", html)
            self.assertIn("CI note &lt;b&gt;not html&lt;/b&gt;", html)
            self.assertIn("&lt;not-fetched&gt;", html)
            self.assertNotIn("<script>alert('project')</script>", html)
            self.assertNotIn("CI note <b>not html</b>", html)


if __name__ == "__main__":
    unittest.main()
