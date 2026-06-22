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
SCHEMA_PATH = ROOT / "schemas" / "project-registry.schema.json"
FIXTURE_PATH = ROOT / "fixtures" / "example-project.registry.json"
RADICLE_FIXTURE_PATH = ROOT / "fixtures" / "radicle-backed-project.registry.json"
NOSTR_COLLAB_FIXTURE_PATH = ROOT / "fixtures" / "nostr-collaboration-events.json"
LOCAL_RELEASE_ARTIFACT_PATH = ROOT / "fixtures" / "local-release-artifact.txt"
FIXTURE_PATHS = [FIXTURE_PATH, RADICLE_FIXTURE_PATH]
RENDERER = ROOT / "scripts" / "render_project_page.py"
CIDV1_BASE32_RE = re.compile(r"^b[a-z2-7]{20,}$")


class RegistryFixtureTests(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        self.radicle_fixture = json.loads(RADICLE_FIXTURE_PATH.read_text(encoding="utf-8"))
        self.nostr_collab_fixture = json.loads(NOSTR_COLLAB_FIXTURE_PATH.read_text(encoding="utf-8"))
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
            self.assertIn("Protocol / substrate hints", html)
            self.assertIn("local-release-artifact.txt", html)


if __name__ == "__main__":
    unittest.main()
