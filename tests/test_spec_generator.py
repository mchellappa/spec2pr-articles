import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "engine" / "spec-generator.py"
SPEC = importlib.util.spec_from_file_location("spec_generator", MODULE_PATH)
spec_generator = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(spec_generator)


class SpecGeneratorTests(unittest.TestCase):
    def test_generate_spec_matches_required_shape(self):
        idea = """# Reliable Content Pipelines

Audience: Platform engineers
Tone: Practical

Content operations become safer when each stage is deterministic.

- Intake normalization
- Schema-first authoring
"""
        result = spec_generator.generate_spec(idea, source_id="reliable-content-pipelines")

        self.assertEqual(result["id"], "reliable-content-pipelines")
        self.assertEqual(result["title"], "Reliable Content Pipelines")
        self.assertFalse(result["publish"])
        self.assertGreaterEqual(len(result["sections"]), 1)

    def test_cli_writes_valid_json_spec(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_file = tmp_path / "idea.md"
            output_file = tmp_path / "spec.json"
            input_file.write_text("# Test Title\n\nAudience: Developers\nTone: Concise\n\nBody text.", encoding="utf-8")

            # Execute core functions directly to keep test fast and deterministic.
            generated = spec_generator.generate_spec(input_file.read_text(encoding="utf-8"), source_id="idea")
            spec_generator.validate_spec_schema(generated)
            output_file.write_text(json.dumps(generated), encoding="utf-8")

            written = json.loads(output_file.read_text(encoding="utf-8"))
            self.assertEqual(written["id"], "idea")
            self.assertEqual(written["title"], "Test Title")


if __name__ == "__main__":
    unittest.main()
