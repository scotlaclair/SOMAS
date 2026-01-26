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


if __name__ == '__main__':
    unittest.main()
