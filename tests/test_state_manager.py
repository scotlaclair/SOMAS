#!/usr/bin/env python3
"""
Unit tests for SOMAS State Manager

Tests the state persistence, dead letter vault, and transition audit functionality.
"""

import unittest
import json
import tempfile
import shutil
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
        import threading
        
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
                    errors.append((worker_id, e))
        
        # Spawn 5 concurrent workers
        threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Assertions
        self.assertEqual(len(errors), 0, f"Errors during concurrent access: {errors}")
        
        # Verify state integrity
        state = self.state_manager.get_state(project_id)
        self.assertEqual(len(state["checkpoints"]), 50, 
                        f"Expected 50 checkpoints, got {len(state['checkpoints'])}")
        
        # Verify all checkpoint IDs are unique
        self.assertEqual(len(set(checkpoints_created)), 50,
                        f"Expected 50 unique checkpoint IDs, got {len(set(checkpoints_created))}")
    
    def test_parallel_stage_transitions(self):
        """Verify stage updates don't corrupt state under concurrency."""
        import threading
        import time
        
        project_id = "project-888"
        self.state_manager.initialize_project(project_id, 888, "Stage Test")
        
        errors = []
        lock = threading.Lock()
        
        def start_worker():
            try:
                self.state_manager.start_stage(project_id, "ideation", "planner")
            except Exception as e:
                with lock:
                    errors.append(e)
        
        def complete_worker():
            try:
                time.sleep(0.01)  # Slight delay to ensure start happens first
                self.state_manager.complete_stage(project_id, "ideation", artifacts=["test.md"])
            except Exception as e:
                with lock:
                    errors.append(e)
        
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
        # Status should be either in_progress or completed (depending on timing)
        self.assertIn(state["stages"]["ideation"]["status"], ["in_progress", "completed"],
                     f"Unexpected status: {state['stages']['ideation']['status']}")
    
    def test_parallel_dead_letter_creation(self):
        """Verify dead letter creation doesn't corrupt state under concurrency."""
        import threading
        
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
                            "message": f"Error from worker {worker_id}, iteration {i}"
                        },
                        context={"worker_id": worker_id, "iteration": i}
                    )
                    with lock:
                        dead_letter_ids.append(dl_id)
            except Exception as e:
                with lock:
                    errors.append((worker_id, e))
        
        # Spawn 3 concurrent workers
        threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Assertions
        self.assertEqual(len(errors), 0, f"Errors during concurrent access: {errors}")
        
        # Verify dead letters integrity
        dead_letters = self.state_manager.get_dead_letters(project_id)
        self.assertEqual(len(dead_letters), 15, 
                        f"Expected 15 dead letters, got {len(dead_letters)}")
        
        # Verify all dead letter IDs are unique
        self.assertEqual(len(set(dead_letter_ids)), 15,
                        f"Expected 15 unique dead letter IDs, got {len(set(dead_letter_ids))}")
        
        # Verify state metrics were updated correctly
        state = self.state_manager.get_state(project_id)
        self.assertEqual(state["metrics"]["dead_letters"], 15,
                        f"Expected 15 dead letters in metrics, got {state['metrics']['dead_letters']}")


if __name__ == '__main__':
    unittest.main()
