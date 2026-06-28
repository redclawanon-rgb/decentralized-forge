import json
import base64
import hashlib
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import nip34_adapter
import forge_registry
import live_gate_inventory
import next_loop_controller
import preflight_static_artifact

SCHEMA_PATH = ROOT / "schemas" / "project-registry.schema.json"
FIXTURE_PATH = ROOT / "fixtures" / "example-project.registry.json"
PORTABLE_FIXTURE_PATH = ROOT / "fixtures" / "portable-lab.registry.json"
RADICLE_FIXTURE_PATH = ROOT / "fixtures" / "radicle-backed-project.registry.json"
NOSTR_REPO_FIXTURE_PATH = ROOT / "fixtures" / "nostr-repo-announcement.json"
NOSTR_COLLAB_FIXTURE_PATH = ROOT / "fixtures" / "nostr-collaboration-events.json"
NOSTR_STATE_STATUS_FIXTURE_PATH = ROOT / "fixtures" / "nostr-repo-state-status.json"
NOSTR_LIVE_READBACK_FIXTURE_PATH = ROOT / "fixtures" / "nostr-live-readback-events.json"
LIVE_REPLAY_CHECKLIST_PATH = ROOT / "fixtures" / "live-adapter-replay-checklist.json"
LIVE_EVIDENCE_INDEX_PATH = ROOT / "fixtures" / "live-evidence-index.json"
NEXT_LOOP_CONTROLLER_PATH = ROOT / "fixtures" / "next-loop-controller.json"
NEXT_LOOP_WORKFLOW_PATH = ROOT / ".github" / "workflows" / "next-loop.yml"
LOCAL_RELEASE_ARTIFACT_PATH = ROOT / "fixtures" / "local-release-artifact.txt"
FIXTURE_PATHS = [FIXTURE_PATH, PORTABLE_FIXTURE_PATH, RADICLE_FIXTURE_PATH]
RENDERER = ROOT / "scripts" / "render_project_page.py"
STATIC_PREFLIGHT = ROOT / "scripts" / "preflight_static_artifact.py"
OUTPUT_DEMO_HTML = ROOT / "output" / "demo-project.html"
OUTPUT_PORTABLE_HTML = ROOT / "output" / "portable-lab.html"
OUTPUT_DEMO_SUMMARY = ROOT / "output" / "demo-project.summary.json"
OUTPUT_PORTABLE_SUMMARY = ROOT / "output" / "portable-lab.summary.json"
CIDV1_BASE32_RE = re.compile(r"^b[a-z2-7]{20,}$")


class RegistryFixtureTests(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        self.portable_fixture = json.loads(PORTABLE_FIXTURE_PATH.read_text(encoding="utf-8"))
        self.radicle_fixture = json.loads(RADICLE_FIXTURE_PATH.read_text(encoding="utf-8"))
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
        for fixture in self.fixtures:
            self.assertIsInstance(fixture, dict)
            self.assertEqual(fixture["schema_version"], "decentralized-forge.project-registry.v1")

    def test_forge_registry_cli_exports_deterministic_summaries(self):
        demo_summary = forge_registry.registry_summary(self.fixture, FIXTURE_PATH)
        portable_summary = forge_registry.registry_summary(self.portable_fixture, PORTABLE_FIXTURE_PATH)
        self.assertEqual(demo_summary, json.loads(OUTPUT_DEMO_SUMMARY.read_text(encoding="utf-8")))
        self.assertEqual(portable_summary, json.loads(OUTPUT_PORTABLE_SUMMARY.read_text(encoding="utf-8")))
        self.assertEqual(portable_summary["project"]["id"], "portable-lab")
        self.assertEqual(portable_summary["counts"]["issues"], 1)
        self.assertEqual(portable_summary["counts"]["patches"], 1)
        self.assertEqual(portable_summary["counts"]["artifacts"], 1)
        self.assertEqual(portable_summary["counts"]["verification_states"], 4)
        self.assertFalse(portable_summary["non_claims"]["production_ready"])

    def test_forge_registry_cli_renders_second_fixture_without_demo_adapters(self):
        html = OUTPUT_PORTABLE_HTML.read_text(encoding="utf-8")
        self.assertIn("Portable Lab Registry Fixture", html)
        self.assertIn("portable-lab", html)
        self.assertIn("Prototype boundary", html)
        self.assertIn("Second local registry fixture only", html)
        self.assertNotIn("NIP-34 fixture adapter", html)
        self.assertNotIn("Live evidence index", html)

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

        blocked = {gate["id"]: gate["requires"] for gate in controller["blocked_without_explicit_target"]}
        for required_gate in [
            "live_ipfs_storage",
            "broader_radicle_public_network",
            "nostr_publish_or_extra_readback",
            "signing_provenance",
            "spending_or_paid_infrastructure",
            "production_private_keys",
            "direct_outreach",
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
        self.assertIn("Blocked without explicit target", result.stdout)
        self.assertIn("No live IPFS daemon", result.stdout)
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
        self.assertEqual(index["loop"], 35)
        self.assertFalse(index["claim_policy"]["contains_secret_values"])
        by_id = {item["id"]: item for item in index["evidence"]}
        self.assertEqual(
            set(by_id),
            {
                "loop23-radicle-local-cli-replay",
                "loop25-nostr-selected-relay-readback",
                "loop34-radicle-disposable-public-smoke",
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
