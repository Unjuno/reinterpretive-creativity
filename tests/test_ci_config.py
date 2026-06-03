from pathlib import Path
import unittest


class TestCIConfig(unittest.TestCase):
    def test_workflow_dispatch_is_not_enabled(self):
        workflow = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertNotIn("workflow_dispatch", workflow)

    def test_ci_runs_on_push_and_pull_request(self):
        workflow = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn("push:", workflow)
        self.assertIn("pull_request:", workflow)


if __name__ == "__main__":
    unittest.main()
