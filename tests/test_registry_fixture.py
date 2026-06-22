import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "project-registry.schema.json"
FIXTURE_PATH = ROOT / "fixtures" / "example-project.registry.json"
RENDERER = ROOT / "scripts" / "render_project_page.py"


class RegistryFixtureTests(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def test_schema_and_fixture_are_valid_json_objects(self):
        self.assertIsInstance(self.schema, dict)
        self.assertIsInstance(self.fixture, dict)
        self.assertEqual(self.fixture["schema_version"], "decentralized-forge.project-registry.v1")

    def test_required_top_level_fields(self):
        for field in self.schema["required"]:
            self.assertIn(field, self.fixture)

    def test_required_project_fields(self):
        project = self.fixture["project"]
        for field in ["id", "name", "description", "default_branch"]:
            self.assertIn(field, project)
            self.assertTrue(project[field])

    def test_maintainers_and_clone_urls_cover_mvp(self):
        maintainers = self.fixture["maintainers"]
        clone_urls = self.fixture["clone_urls"]
        self.assertGreaterEqual(len(maintainers), 1)
        self.assertGreaterEqual(len(clone_urls), 1)
        allowed_maintainer_types = {"nostr", "radicle", "did", "ssh", "other"}
        allowed_clone_transports = {"git", "https", "ssh", "radicle", "nostr", "other"}
        for maintainer in maintainers:
            self.assertIn(maintainer["id_type"], allowed_maintainer_types)
            self.assertTrue(maintainer["public_id"])
        for clone in clone_urls:
            self.assertIn(clone["transport"], allowed_clone_transports)
            self.assertTrue(clone["url"])
        self.assertTrue(any(clone["url"].startswith("file://") for clone in clone_urls))

    def test_fixture_includes_collaboration_and_release_data(self):
        self.assertGreaterEqual(len(self.fixture.get("issues", [])), 1)
        self.assertGreaterEqual(len(self.fixture.get("patches", [])), 1)
        self.assertGreaterEqual(len(self.fixture.get("releases", [])), 1)
        artifact = self.fixture["releases"][0]["artifacts"][0]
        self.assertEqual(len(artifact["sha256"]), 64)

    def test_fixture_includes_required_substrate_hints(self):
        substrates = self.fixture["substrates"]
        for key in ["nip34", "radicle", "forgefed", "ipfs", "sigstore_slsa"]:
            self.assertIn(key, substrates)

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
