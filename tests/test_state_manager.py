#!/usr/bin/env python3
"""
Unit tests for SOMAS State Manager

Tests the state persistence, dead letter vault, and transition audit functionality.
"""

import unittest
import json
import tempfile
import shutil
import threading
from pathlib import Path
from datetime import datetime

# Add somas to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "somas"))

from core.state_manager import StateManager


class TestStateManager(unittest.TestCase):
    """Test cases for StateManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory for test projects
        self.test_dir = tempfile.mkdtemp()
        self.state_manager = StateManager(projects_dir=Path(self.test_dir))
        self.project_id = "project-123"
        self.issue_number = 123
        self.title = "Test Project"
        
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_project_initialization(self):
        """Test project initialization creates all required files."""
        # Initialize project
        state = self.state_manager.initialize_project(
            project_id=self.project_id,
            issue_number=self.issue_number,
            title=self.title
        )
        
        # Check state returned
        self.assertEqual(state["project_id"], self.project_id)
        self.assertEqual(state["issue_number"], self.issue_number)
        self.assertEqual(state["status"], "initializing")
        self.assertEqual(state["current_stage"], "ideation")
        
        # Check files created
        project_dir = Path(self.test_dir) / self.project_id
        self.assertTrue((project_dir / "state.json").exists())
        self.assertTrue((project_dir / "dead_letters.json").exists())
        self.assertTrue((project_dir / "transitions.jsonl").exists())
        
        # Check state.json content
        with open(project_dir / "state.json", 'r') as f:
            state_file = json.load(f)
        self.assertEqual(state_file["project_id"], self.project_id)
        self.assertEqual(len(state_file["stages"]), 7)
        self.assertEqual(state_file["metrics"]["dead_letters"], 0)
        
        # Check dead_letters.json content
        with open(project_dir / "dead_letters.json", 'r') as f:
            dead_letters = json.load(f)
        self.assertEqual(dead_letters["project_id"], self.project_id)
        self.assertEqual(len(dead_letters["entries"]), 0)
        
        # Check transitions.jsonl has initialization entry
        with open(project_dir / "transitions.jsonl", 'r') as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 1)
        transition = json.loads(lines[0])
        self.assertEqual(transition["event_type"], "project_initialized")
    
    def test_invalid_project_id(self):
        """Test that invalid project IDs are rejected."""
        # Path traversal attempt
        with self.assertRaises(ValueError):
            self.state_manager.initialize_project(
                project_id="../evil",
                issue_number=1,
                title="Test"
            )
        
        # Invalid format (should be project-<number>)
        with self.assertRaises(ValueError):
            self.state_manager.initialize_project(
                project_id="invalid-format",
                issue_number=1,
                title="Test"
            )
    
    def test_start_stage(self):
        """Test starting a pipeline stage."""
        # Initialize project
        self.state_manager.initialize_project(
            project_id=self.project_id,
            issue_number=self.issue_number,
            title=self.title
        )
        
        # Start stage
        state = self.state_manager.start_stage(
            project_id=self.project_id,
            stage="implementation",
            agent="coder"
        )
        
        # Check state updated
        self.assertEqual(state["current_stage"], "implementation")
        self.assertEqual(state["status"], "in_progress")
        self.assertEqual(state["stages"]["implementation"]["status"], "in_progress")
        self.assertEqual(state["stages"]["implementation"]["agent"], "coder")
        self.assertIn("started_at", state["stages"]["implementation"])
        
        # Check metrics updated
        self.assertEqual(state["metrics"]["agent_invocations"], 1)
        
        # Check transition logged
        transitions = self.state_manager.get_transitions(self.project_id)
        stage_started = [t for t in transitions if t["event_type"] == "stage_started"]
        self.assertEqual(len(stage_started), 1)
        self.assertEqual(stage_started[0]["stage"], "implementation")
        self.assertEqual(stage_started[0]["agent"], "coder")
    
    def test_complete_stage(self):
        """Test completing a pipeline stage."""
        # Initialize and start
        self.state_manager.initialize_project(
            project_id=self.project_id,
            issue_number=self.issue_number,
            title=self.title
        )
        self.state_manager.start_stage(
            project_id=self.project_id,
            stage="ideation",
            agent="planner"
        )
        
        # Complete stage
        artifacts = ["artifacts/plan.md"]
        state = self.state_manager.complete_stage(
            project_id=self.project_id,
            stage="ideation",
            artifacts=artifacts,
            create_checkpoint=True
        )
        
        # Check state updated
        self.assertEqual(state["stages"]["ideation"]["status"], "completed")
        self.assertIn("completed_at", state["stages"]["ideation"])
        self.assertIn("duration_seconds", state["stages"]["ideation"])
        self.assertEqual(state["stages"]["ideation"]["artifacts"], artifacts)
        
        # Check metrics updated
        self.assertEqual(state["metrics"]["artifacts_generated"], 1)
        self.assertIn("ideation", state["metrics"]["stage_durations"])
        
        # Check checkpoint created
        self.assertEqual(len(state["checkpoints"]), 1)
        checkpoint = state["checkpoints"][0]
        self.assertEqual(checkpoint["stage"], "ideation")
        self.assertEqual(checkpoint["status"], "success")
        self.assertEqual(checkpoint["artifacts"], artifacts)
        
        # Check recovery info updated
        self.assertEqual(state["recovery_info"]["last_successful_checkpoint"], checkpoint["id"])
        
        # Check transitions logged
        transitions = self.state_manager.get_transitions(self.project_id)
        completed = [t for t in transitions if t["event_type"] == "stage_completed"]
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0]["stage"], "ideation")
        
        checkpoint_created = [t for t in transitions if t["event_type"] == "checkpoint_created"]
        self.assertEqual(len(checkpoint_created), 1)
    
    def test_fail_stage(self):
        """Test recording a stage failure."""
        # Initialize and start
        self.state_manager.initialize_project(
            project_id=self.project_id,
            issue_number=self.issue_number,
            title=self.title
        )
        self.state_manager.start_stage(
            project_id=self.project_id,
            stage="validation",
            agent="validator"
        )
        
        # Fail stage
        error = {
            "type": "TestFailureError",
            "message": "3 tests failed"
        }
        context = {
            "test_suite": "integration_tests"
        }
        state = self.state_manager.fail_stage(
            project_id=self.project_id,
            stage="validation",
            agent="validator",
            error=error,
            context=context,
            create_dead_letter=True
        )
        
        # Check state updated
        self.assertEqual(state["stages"]["validation"]["status"], "failed")
        self.assertEqual(state["stages"]["validation"]["error"], error["message"])
        self.assertEqual(state["status"], "failed")
        
        # Check dead letter created
        dead_letters = self.state_manager.get_dead_letters(self.project_id)
        self.assertEqual(len(dead_letters), 1)
        
        dead_letter = dead_letters[0]
        self.assertEqual(dead_letter["stage"], "validation")
        self.assertEqual(dead_letter["agent"], "validator")
        self.assertEqual(dead_letter["error"]["type"], error["type"])
        self.assertEqual(dead_letter["error"]["message"], error["message"])
        self.assertIn("test_suite", dead_letter["context"])
        self.assertEqual(dead_letter["attempt_number"], 1)
        self.assertFalse(dead_letter["recovery_attempted"])
        
        # Check metrics updated
        self.assertEqual(state["metrics"]["dead_letters"], 1)
        
        # Check transitions logged
        transitions = self.state_manager.get_transitions(self.project_id)
        failed = [t for t in transitions if t["event_type"] == "stage_failed"]
        self.assertEqual(len(failed), 1)
        
        error_recorded = [t for t in transitions if t["event_type"] == "error_recorded"]
        self.assertEqual(len(error_recorded), 1)


class TestConcurrentAccess(unittest.TestCase):
    """Test cases for concurrent access to StateManager."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory for test projects
        self.test_dir = tempfile.mkdtemp()
        self.state_manager = StateManager(projects_dir=Path(self.test_dir))
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_parallel_checkpoint_writes(self):
        """Verify no corruption under parallel checkpoint creation."""
        project_id = "project-999"
        self.state_manager.initialize_project(project_id, 999, "Concurrency Test")
        
        errors = []
        checkpoints_created = []
        lock = threading.Lock()
        
        def worker(worker_id):
            try:
                for i in range(10):
                    chk_id = self.state_manager.create_checkpoint(
                        project_id, 
                        stage=f"test-{worker_id}", 
                        status="success"
                    )
                    with lock:
                        checkpoints_created.append(chk_id)
            except Exception as e:
                with lock:
                    errors.append((worker_id, str(e)))
        
        # Spawn 5 concurrent workers
        threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Assertions
        self.assertEqual(len(errors), 0, f"Errors during concurrent access: {errors}")
        
        # Verify state integrity - with rotation, should have max_checkpoints
        state = self.state_manager.get_state(project_id)
        max_checkpoints = self.state_manager._get_max_checkpoints()
        self.assertEqual(len(state["checkpoints"]), max_checkpoints, 
                         f"Expected {max_checkpoints} checkpoints (due to rotation) but got {len(state['checkpoints'])}")
        
        # Verify all checkpoint IDs created were unique (even though only max_checkpoints are retained)
        self.assertEqual(len(set(checkpoints_created)), 50,
                        "Not all checkpoint IDs are unique")
    
    def test_parallel_stage_transitions(self):
        """Verify stage updates don't corrupt state under concurrency."""
        project_id = "project-888"
        self.state_manager.initialize_project(project_id, 888, "Stage Test")
        
        errors = []
        lock = threading.Lock()
        stage_started = threading.Event()
        
        def start_worker():
            try:
                self.state_manager.start_stage(project_id, "ideation", "planner")
                stage_started.set()  # Signal that stage has started
            except Exception as e:
                with lock:
                    errors.append(f"start_worker: {str(e)}")
        
        def complete_worker():
            try:
                # Wait for stage to be started before completing
                if not stage_started.wait(timeout=5.0):
                    with lock:
                        errors.append("complete_worker: timeout waiting for stage to start")
                    return
                self.state_manager.complete_stage(project_id, "ideation", artifacts=["test.md"])
            except Exception as e:
                with lock:
                    errors.append(f"complete_worker: {str(e)}")
        
        threads = [
            threading.Thread(target=start_worker),
            threading.Thread(target=complete_worker),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Should complete without corruption
        self.assertEqual(len(errors), 0, f"Errors during concurrent access: {errors}")
        
        state = self.state_manager.get_state(project_id)
        self.assertIn(state["stages"]["ideation"]["status"], ["in_progress", "completed"],
                     f"Unexpected stage status: {state['stages']['ideation']['status']}")
    
    def test_parallel_dead_letter_writes(self):
        """Verify dead letter writes don't corrupt under concurrency."""
        project_id = "project-777"
        self.state_manager.initialize_project(project_id, 777, "Dead Letter Test")
        
        errors = []
        dead_letter_ids = []
        lock = threading.Lock()
        
        def worker(worker_id):
            try:
                for i in range(5):
                    dl_id = self.state_manager.add_dead_letter(
                        project_id=project_id,
                        stage=f"stage-{worker_id}",
                        agent=f"agent-{worker_id}",
                        error={
                            "type": "TestError",
                            "message": f"Test error {worker_id}-{i}"
                        },
                        context={"worker": worker_id, "iteration": i}
                    )
                    with lock:
                        dead_letter_ids.append(dl_id)
            except Exception as e:
                with lock:
                    errors.append((worker_id, str(e)))
        
        # Spawn 3 concurrent workers
        threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Assertions
        self.assertEqual(len(errors), 0, f"Errors during concurrent access: {errors}")
        
        # Verify dead letter integrity
        dead_letters = self.state_manager.get_dead_letters(project_id)
        self.assertEqual(len(dead_letters), 15,
                        f"Expected 15 dead letters but got {len(dead_letters)}")
        
        # Verify all dead letter IDs are unique
        self.assertEqual(len(set(dead_letter_ids)), 15,
                        "Not all dead letter IDs are unique")
        
        # Verify state metrics updated correctly
        state = self.state_manager.get_state(project_id)
        self.assertEqual(state["metrics"]["dead_letters"], 15,
                        f"Expected 15 dead letters in metrics but got {state['metrics']['dead_letters']}")


class TestSecurityValidation(unittest.TestCase):
    """Test cases for security validation and injection prevention."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.state_manager = StateManager(projects_dir=Path(self.test_dir))
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)
    
    def test_project_id_rejects_path_traversal(self):
        """Ensure path traversal attempts are blocked."""
        malicious_ids = [
            "../../../etc/passwd",
            "project-1/../../../etc",
            "project-1/../../secret",
            "..\\..\\windows\\system32",
            "..",
            "../",
            "project-1/..",
        ]
        
        for bad_id in malicious_ids:
            with self.assertRaises(ValueError, msg=f"Should reject: {bad_id}"):
                self.state_manager._validate_project_id(bad_id)
    
    def test_project_id_rejects_command_injection(self):
        """Ensure command injection attempts are blocked."""
        malicious_ids = [
            'project-1; rm -rf /',
            'project-1 && echo pwned',
            'project-1`whoami`',
            'project-1$(cat /etc/passwd)',
            'my-project"; rm -rf /; echo "',
            'project-1|cat /etc/passwd',
            'project-1\nrm -rf /',
        ]
        
        for bad_id in malicious_ids:
            with self.assertRaises(ValueError, msg=f"Should reject: {bad_id}"):
                self.state_manager._validate_project_id(bad_id)
    
    def test_project_id_rejects_special_characters(self):
        """Ensure special characters are blocked."""
        malicious_ids = [
            'project-1/subdir',
            'project-1\\subdir',
            'project@123',
            'project#123',
            'project 123',  # spaces
            'project\t123',  # tabs
            'project\n123',  # newlines
        ]
        
        for bad_id in malicious_ids:
            with self.assertRaises(ValueError, msg=f"Should reject: {bad_id}"):
                self.state_manager._validate_project_id(bad_id)
    
    def test_project_id_accepts_valid_format(self):
        """Ensure valid project IDs are accepted."""
        valid_ids = [
            "project-1",
            "project-123",
            "project-999999",
            "project-0",
        ]
        
        for good_id in valid_ids:
            try:
                result = self.state_manager._validate_project_id(good_id)
                self.assertTrue(result, f"Should accept: {good_id}")
            except ValueError as e:
                self.fail(f"Valid ID rejected: {good_id} - {e}")
    
    def test_path_construction_prevents_escape(self):
        """Verify path construction stays within project directory."""
        # Valid path should work
        path = self.state_manager._get_safe_project_path("project-123")
        self.assertIn(self.test_dir, str(path))
        self.assertTrue(str(path).startswith(str(Path(self.test_dir).resolve())))
        
        # Invalid IDs should fail during validation
        with self.assertRaises(ValueError):
            self.state_manager._get_safe_project_path("../escape")
        
        with self.assertRaises(ValueError):
            self.state_manager._get_safe_project_path("project-1; rm -rf /")
    
    def test_safe_path_resolution(self):
        """Test that _get_safe_project_path resolves paths correctly."""
        project_id = "project-456"
        
        # Get the safe path
        safe_path = self.state_manager._get_safe_project_path(project_id)
        
        # Verify it's a resolved absolute path
        self.assertTrue(safe_path.is_absolute())
        
        # Verify it's within the base directory
        base_path = Path(self.test_dir).resolve()
        self.assertTrue(str(safe_path).startswith(str(base_path)))
        
        # Verify it ends with the project_id
        self.assertTrue(str(safe_path).endswith(project_id))
    
    def test_project_id_empty_string(self):
        """Ensure empty strings are rejected."""
        with self.assertRaises(ValueError):
            self.state_manager._validate_project_id("")
    
    def test_project_id_only_numbers(self):
        """Ensure project IDs must have 'project-' prefix."""
        with self.assertRaises(ValueError):
            self.state_manager._validate_project_id("123")
    
    def test_project_id_wrong_prefix(self):
        """Ensure only 'project-' prefix is accepted."""
        invalid_ids = [
            "proj-123",
            "PROJECT-123",  # uppercase
            "project_123",  # underscore instead of hyphen
            "projects-123",
        ]
        
        for bad_id in invalid_ids:
            with self.assertRaises(ValueError, msg=f"Should reject: {bad_id}"):
                self.state_manager._validate_project_id(bad_id)
    
    def test_initialize_project_with_malicious_title(self):
        """Verify that malicious titles don't cause issues."""
        project_id = "project-999"
        
        # Titles with potential injection attempts
        malicious_titles = [
            'My Project"; rm -rf /; echo "pwned',
            'Project $(cat /etc/passwd)',
            'Project `whoami`',
            'Project && echo hacked',
            'Project || rm -rf /',
        ]
        
        for title in malicious_titles:
            # Should successfully initialize without injection
            try:
                state = self.state_manager.initialize_project(
                    project_id=project_id,
                    issue_number=999,
                    title=title
                )
                
                # Verify the state was created
                self.assertEqual(state["project_id"], project_id)
                
                # Clean up for next iteration
                project_dir = Path(self.test_dir) / project_id
                if project_dir.exists():
                    shutil.rmtree(project_dir)
                    
            except Exception as e:
                self.fail(f"Initialization failed with title '{title}': {e}")


class TestCheckpointRotation(unittest.TestCase):
    """Test cases for checkpoint rotation functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.state_manager = StateManager(projects_dir=Path(self.test_dir))
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)
    
    def test_checkpoint_rotation_limits_array_size(self):
        """Verify checkpoints are rotated when exceeding max_checkpoints."""
        project_id = "project-9001"
        self.state_manager.initialize_project(project_id, 9001, "Rotation Test")
        
        # Get the configured max checkpoints
        max_checkpoints = self.state_manager._get_max_checkpoints()
        
        # Create more checkpoints than the limit
        num_checkpoints = 30
        for i in range(num_checkpoints):
            self.state_manager.create_checkpoint(
                project_id,
                stage=f"stage-{i}",
                status="success"
            )
        
        state = self.state_manager.get_state(project_id)
        
        # Should not exceed max_checkpoints
        self.assertLessEqual(len(state["checkpoints"]), max_checkpoints,
                            f"Expected at most {max_checkpoints} checkpoints but got {len(state['checkpoints'])}")
        
        # Oldest checkpoints should be pruned (first ones created)
        # The remaining checkpoints should be the most recent
        checkpoint_stages = [c["stage"] for c in state["checkpoints"]]
        self.assertNotIn("stage-0", checkpoint_stages, "Oldest checkpoint should be pruned")
        self.assertIn("stage-29", checkpoint_stages, "Most recent checkpoint should be kept")
    
    def test_checkpoint_rotation_preserves_recovery_info(self):
        """Verify last_successful_checkpoint remains valid after rotation."""
        project_id = "project-9002"
        self.state_manager.initialize_project(project_id, 9002, "Recovery Test")
        
        # Create checkpoints up to limit
        for i in range(25):
            chk_id = self.state_manager.create_checkpoint(
                project_id,
                stage=f"stage-{i}",
                status="success"
            )
        
        state = self.state_manager.get_state(project_id)
        
        # Recovery info should point to most recent successful checkpoint
        last_chk = state["recovery_info"]["last_successful_checkpoint"]
        checkpoint_ids = [c["id"] for c in state["checkpoints"]]
        
        # Last successful checkpoint should still exist in array
        self.assertIn(last_chk, checkpoint_ids,
                     "Last successful checkpoint should exist in retained checkpoints")
    
    def test_checkpoint_rotation_with_failed_checkpoints(self):
        """Verify rotation works correctly with mixed success/failed checkpoints."""
        project_id = "project-9003"
        self.state_manager.initialize_project(project_id, 9003, "Mixed Test")
        
        # Create mix of successful and failed checkpoints
        for i in range(25):
            status = "success" if i % 3 == 0 else "failed"
            self.state_manager.create_checkpoint(
                project_id,
                stage=f"stage-{i}",
                status=status
            )
        
        state = self.state_manager.get_state(project_id)
        
        # Should not exceed max_checkpoints
        max_checkpoints = self.state_manager._get_max_checkpoints()
        self.assertLessEqual(len(state["checkpoints"]), max_checkpoints)
        
        # Verify mix of statuses is preserved in recent checkpoints
        statuses = [c["status"] for c in state["checkpoints"]]
        self.assertIn("success", statuses, "Should have successful checkpoints")
        self.assertIn("failed", statuses, "Should have failed checkpoints")
    
    def test_checkpoint_no_rotation_below_limit(self):
        """Verify no rotation occurs when below MAX_CHECKPOINTS."""
        project_id = "project-9004"
        self.state_manager.initialize_project(project_id, 9004, "Small Test")
        
        # Create fewer checkpoints than the limit
        num_checkpoints = 10
        for i in range(num_checkpoints):
            self.state_manager.create_checkpoint(
                project_id,
                stage=f"stage-{i}",
                status="success"
            )
        
        state = self.state_manager.get_state(project_id)
        
        # All checkpoints should be retained
        self.assertEqual(len(state["checkpoints"]), num_checkpoints,
                        f"Expected {num_checkpoints} checkpoints, got {len(state['checkpoints'])}")
        
        # All stages should be present
        checkpoint_stages = [c["stage"] for c in state["checkpoints"]]
        for i in range(num_checkpoints):
            self.assertIn(f"stage-{i}", checkpoint_stages,
                         f"Stage {i} should be present")
    
    def test_checkpoint_rotation_keeps_most_recent(self):
        """Verify rotation keeps the most recent N checkpoints in order."""
        project_id = "project-9005"
        self.state_manager.initialize_project(project_id, 9005, "Order Test")
        
        # Get the configured max checkpoints
        max_checkpoints = self.state_manager._get_max_checkpoints()
        
        # Create exactly max_checkpoints + 5 checkpoints
        num_checkpoints = max_checkpoints + 5
        for i in range(num_checkpoints):
            self.state_manager.create_checkpoint(
                project_id,
                stage=f"stage-{i:02d}",  # Zero-padded for easier verification
                status="success"
            )
        
        state = self.state_manager.get_state(project_id)
        
        # Should have exactly max_checkpoints checkpoints
        self.assertEqual(len(state["checkpoints"]), max_checkpoints)
        
        # Verify it's the last max_checkpoints (stages 5-24 for default 20)
        checkpoint_stages = [c["stage"] for c in state["checkpoints"]]
        expected_stages = [f"stage-{i:02d}" for i in range(5, num_checkpoints)]
        self.assertEqual(checkpoint_stages, expected_stages,
                        f"Should keep the most recent {max_checkpoints} checkpoints in order")


if __name__ == '__main__':
    unittest.main()
