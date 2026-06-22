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

SCHEMA_PATH = ROOT / "schemas" / "project-registry.schema.json"
FIXTURE_PATH = ROOT / "fixtures" / "example-project.registry.json"
RADICLE_FIXTURE_PATH = ROOT / "fixtures" / "radicle-backed-project.registry.json"
NOSTR_REPO_FIXTURE_PATH = ROOT / "fixtures" / "nostr-repo-announcement.json"
NOSTR_COLLAB_FIXTURE_PATH = ROOT / "fixtures" / "nostr-collaboration-events.json"
NOSTR_STATE_STATUS_FIXTURE_PATH = ROOT / "fixtures" / "nostr-repo-state-status.json"
LOCAL_RELEASE_ARTIFACT_PATH = ROOT / "fixtures" / "local-release-artifact.txt"
FIXTURE_PATHS = [FIXTURE_PATH, RADICLE_FIXTURE_PATH]
RENDERER = ROOT / "scripts" / "render_project_page.py"
CIDV1_BASE32_RE = re.compile(r"^b[a-z2-7]{20,}$")


class RegistryFixtureTests(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        self.radicle_fixture = json.loads(RADICLE_FIXTURE_PATH.read_text(encoding="utf-8"))
        self.nostr_repo_fixture = json.loads(NOSTR_REPO_FIXTURE_PATH.read_text(encoding="utf-8"))
        self.nostr_collab_fixture = json.loads(NOSTR_COLLAB_FIXTURE_PATH.read_text(encoding="utf-8"))
        self.nostr_state_status_fixture = json.loads(NOSTR_STATE_STATUS_FIXTURE_PATH.read_text(encoding="utf-8"))
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
            self.assertIn("No relay publishing, signing, fixture ID replacement, relay fetching, or live verification is performed or claimed", html)
            self.assertIn("possible_event_id values are local reference hashes only", html)
            self.assertIn("Local NIP-34 conformance summary", html)
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
