"""
Tests for SOMAS Runner error handling and validation.

This test suite verifies the error handling improvements made to address
critical gaps identified in code review.
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path

from somas.core.runner import SOMASRunner


class TestRunnerErrorHandling(unittest.TestCase):
    """Test error handling in SOMASRunner."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.repo_root = Path(self.temp_dir)
        self.orig_cwd = os.getcwd()

        # Create minimal config structure
        self.config_dir = self.repo_root / ".somas"
        self.config_dir.mkdir()
        self.config_path = self.config_dir / "config.yml"

        # Create minimal valid config
        self.config_path.write_text(
            """
version: "1.0.0"
agents:
  providers:
    test_provider:
      model: "test-model"
  agent_configs:
    test_agent:
      provider: "test_provider"
"""
        )

        # Change to temp directory so runner uses it as repo_root
        os.chdir(self.temp_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        os.chdir(self.orig_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_project_id_validation_valid(self):
        """Test that valid project IDs pass validation."""
        runner = SOMASRunner()

        valid_ids = [
            "project-1",
            "project-123",
            "project-999999",
        ]

        for project_id in valid_ids:
            with self.subTest(project_id=project_id):
                self.assertTrue(
                    runner._validate_project_id(project_id),
                    f"Project ID {project_id} should be valid",
                )

    def test_project_id_validation_invalid(self):
        """Test invalid project IDs fail validation (prevents traversal)."""
        runner = SOMASRunner()

        invalid_ids = [
            "../../../etc/passwd",
            "project-123/../../../etc/passwd",
            "project-",
            "project-abc",
            "project",
            "../../secrets",
            "project-123/../../secrets",
            "",
            "null",
        ]

        for project_id in invalid_ids:
            with self.subTest(project_id=project_id):
                self.assertFalse(
                    runner._validate_project_id(project_id),
                    f"Project ID {project_id} should be rejected",
                )

    def test_run_autonomous_pipeline_validates_project_id(self):
        """Test run_autonomous_pipeline validates project_id."""
        runner = SOMASRunner()

        # Test with invalid project_id
        exit_code = runner.run_autonomous_pipeline(
            "../../../etc/passwd"
        )

        # Should return non-zero exit code for invalid project_id
        self.assertEqual(
            exit_code,
            1,
            "Should return error code for invalid project_id",
        )

    def test_load_config_file_not_found(self):
        """Test _load_config raises RuntimeError for missing file."""
        # Create runner, then change config path to non-existent file
        runner = SOMASRunner()
        runner.config_path = Path("nonexistent/config.yml")

        with self.assertRaises(RuntimeError) as context:
            runner._load_config()

        self.assertIn("Config file not found", str(context.exception))

    def test_load_config_invalid_yaml(self):
        """Test _load_config raises RuntimeError for invalid YAML."""
        # Write invalid YAML to config file
        self.config_path.write_text("invalid: yaml: content: [unclosed")

        with self.assertRaises(RuntimeError) as context:
            SOMASRunner()  # Will raise during __init__

        self.assertIn("Invalid YAML", str(context.exception))

    def test_ensure_valid_project_id_auto_generate(self):
        """Test auto-generation of project ID from issue number."""
        runner = SOMASRunner()

        # Test auto-generation when project_id is empty
        generated_id = runner._ensure_valid_project_id("", issue_number=123)
        self.assertEqual(generated_id, "project-123")

        # Test auto-generation when project_id is None
        generated_id = runner._ensure_valid_project_id(None, issue_number=456)
        self.assertEqual(generated_id, "project-456")

    def test_ensure_valid_project_id_sanitize(self):
        """Test sanitization of malformed project IDs."""
        runner = SOMASRunner()

        # Test sanitization of project ID with extra characters
        sanitized = runner._ensure_valid_project_id(
            "project-123-extra-stuff", issue_number=None
        )
        self.assertEqual(sanitized, "project-123")

    def test_ensure_valid_project_id_missing_both(self):
        """Test error when both project_id and issue_number missing."""
        runner = SOMASRunner()

        with self.assertRaises(ValueError) as context:
            runner._ensure_valid_project_id("", issue_number=None)

        self.assertIn("missing", str(context.exception).lower())

    def test_ensure_valid_project_id_invalid(self):
        """Test error for completely invalid project ID."""
        runner = SOMASRunner()

        with self.assertRaises(ValueError) as context:
            runner._ensure_valid_project_id(
                "../../../etc/passwd", issue_number=None
            )

        self.assertIn("Invalid project ID", str(context.exception))


class TestRunnerProjectIDInjectionPrevention(unittest.TestCase):
    """Security tests for project ID path traversal prevention."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.repo_root = Path(self.temp_dir)
        self.orig_cwd = os.getcwd()

        # Create minimal config
        config_dir = self.repo_root / ".somas"
        config_dir.mkdir()
        config_path = config_dir / "config.yml"
        config_path.write_text(
            """
version: "1.0.0"
agents:
  providers:
    test_provider:
      model: "test-model"
  agent_configs:
    test_agent:
      provider: "test_provider"
"""
        )

        os.chdir(self.temp_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        os.chdir(self.orig_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_path_traversal_attacks_blocked(self):
        """Verify path traversal attacks are blocked."""
        runner = SOMASRunner()

        # Common path traversal attack patterns
        attack_patterns = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32",
            "project-123/../../../secrets",
            "project-123/../../.env",
            "./../../sensitive_data",
            "../../../../root/.ssh/id_rsa",
        ]

        for attack_id in attack_patterns:
            with self.subTest(attack_id=attack_id):
                # run_autonomous_pipeline should reject these
                exit_code = runner.run_autonomous_pipeline(attack_id)
                self.assertEqual(
                    exit_code,
                    1,
                    f"Path traversal attack {attack_id} should be blocked",
                )


if __name__ == "__main__":
    unittest.main()
