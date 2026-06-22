import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "project-registry.schema.json"
FIXTURE_PATH = ROOT / "fixtures" / "example-project.registry.json"
RADICLE_FIXTURE_PATH = ROOT / "fixtures" / "radicle-backed-project.registry.json"
FIXTURE_PATHS = [FIXTURE_PATH, RADICLE_FIXTURE_PATH]
RENDERER = ROOT / "scripts" / "render_project_page.py"


class RegistryFixtureTests(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        self.radicle_fixture = json.loads(RADICLE_FIXTURE_PATH.read_text(encoding="utf-8"))
        self.fixtures = [json.loads(path.read_text(encoding="utf-8")) for path in FIXTURE_PATHS]

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

    def test_fixture_includes_required_substrate_hints(self):
        substrates = self.fixture["substrates"]
        for key in ["nip34", "radicle", "forgefed", "ipfs", "sigstore_slsa"]:
            self.assertIn(key, substrates)

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
            self.assertIn("demo-project-source.tar.gz", html)


if __name__ == "__main__":
    unittest.main()
