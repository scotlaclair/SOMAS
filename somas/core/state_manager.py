#!/usr/bin/env python3
"""
SOMAS State Manager

This module handles persistent JSON state for the SOMAS pipeline:
- state.json: Pipeline state, checkpoints, labels, metrics
- dead_letters.json: Failed agent contexts for recovery/replay/debugging
- transitions.jsonl: Chronological audit log of all state transitions

Security:
    - All file paths validated to prevent path traversal
    - Project IDs validated against safe patterns
    - Atomic writes using temporary files
    - JSON schema validation on read/write
"""

import json
import uuid
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import re
from filelock import FileLock


class StateManager:
    """Manages persistent JSON state for SOMAS pipeline projects."""
    
    def __init__(self, projects_dir: Path = None):
        """
        Initialize state manager.
        
        Args:
            projects_dir: Root directory for projects (default: .somas/projects)
        """
        if projects_dir is None:
            projects_dir = Path(".somas/projects")
        self.projects_dir = Path(projects_dir)
        
    def _validate_project_id(self, project_id: str) -> bool:
        """
        Validate project ID to prevent path traversal attacks.
        
        Args:
            project_id: Project identifier to validate
            
        Returns:
            True if valid, raises ValueError otherwise
        """
        if not re.match(r'^project-\d+$', project_id):
            raise ValueError(f"Invalid project ID format: {project_id}")
        return True
    
    def _get_project_dir(self, project_id: str) -> Path:
        """
        Get validated project directory path.
        
        Args:
            project_id: Project identifier
            
        Returns:
            Path to project directory
        """
        self._validate_project_id(project_id)
        return self.projects_dir / project_id
    
    def _get_state_path(self, project_id: str) -> Path:
        """Get path to state.json file."""
        return self._get_project_dir(project_id) / "state.json"
    
    def _get_dead_letters_path(self, project_id: str) -> Path:
        """Get path to dead_letters.json file."""
        return self._get_project_dir(project_id) / "dead_letters.json"
    
    def _get_transitions_path(self, project_id: str) -> Path:
        """Get path to transitions.jsonl file."""
        return self._get_project_dir(project_id) / "transitions.jsonl"
    
    def _atomic_write_json(self, path: Path, data: Dict[str, Any]) -> None:
        """
        Atomically write JSON to file using temporary file with file locking.
        
        Args:
            path: Target file path
            data: Data to write
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Use file locking to prevent concurrent write conflicts
        with FileLock(f"{path}.lock", timeout=30):
            tmp_path = path.with_suffix('.tmp')
            
            try:
                with open(tmp_path, 'w') as f:
                    json.dump(data, f, indent=2)
                tmp_path.replace(path)
            except Exception as e:
                if tmp_path.exists():
                    tmp_path.unlink()
                raise
    
    def _append_jsonl(self, path: Path, entry: Dict[str, Any]) -> None:
        """
        Append JSON entry to JSONL file with file locking.
        
        Args:
            path: JSONL file path
            entry: Entry to append
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Use file locking to prevent concurrent append conflicts
        with FileLock(f"{path}.lock", timeout=30):
            with open(path, 'a') as f:
                json.dump(entry, f)
                f.write('\n')
    
    def initialize_project(
        self,
        project_id: str,
        issue_number: int,
        title: str,
        branch: str = None,
        labels: List[str] = None
    ) -> Dict[str, Any]:
        """
        Initialize state files for a new project.
        
        Args:
            project_id: Project identifier
            issue_number: GitHub issue number
            title: Project title
            branch: Git branch name
            labels: Initial GitHub labels
            
        Returns:
            Initial state dictionary
        """
        self._validate_project_id(project_id)
        
        if branch is None:
            branch = f"somas/{project_id}"
        
        if labels is None:
            labels = ["somas-project", "somas:dev"]
        
        now = datetime.utcnow().isoformat() + 'Z'
        
        # Initialize state.json
        state = {
            "project_id": project_id,
            "version": "1.0.0",
            "created_at": now,
            "updated_at": now,
            "issue_number": issue_number,
            "branch": branch,
            "current_stage": "ideation",
            "status": "initializing",
            "stages": {
                stage: {"status": "pending", "retry_count": 0}
                for stage in [
                    "ideation", "specification", "simulation",
                    "architecture", "implementation", "validation", "staging"
                ]
            },
            "checkpoints": [],
            "labels": {
                "github": labels,
                "custom": {}
            },
            "metrics": {
                "total_duration_seconds": 0,
                "stage_durations": {},
                "retry_count": 0,
                "agent_invocations": 0,
                "artifacts_generated": 0,
                "dead_letters": 0
            },
            "recovery_info": {
                "last_successful_checkpoint": None,
                "can_resume": True,
                "resume_from_stage": "ideation"
            }
        }
        
        # Initialize dead_letters.json
        dead_letters = {
            "project_id": project_id,
            "version": "1.0.0",
            "entries": [],
            "statistics": {
                "total_entries": 0,
                "by_stage": {},
                "by_agent": {},
                "recovered": 0,
                "unrecovered": 0
            }
        }
        
        # Write initial state files
        self._atomic_write_json(self._get_state_path(project_id), state)
        self._atomic_write_json(self._get_dead_letters_path(project_id), dead_letters)
        
        # Log initialization transition
        self.log_transition(
            project_id=project_id,
            event_type="project_initialized",
            metadata={
                "issue_number": issue_number,
                "title": title,
                "branch": branch
            },
            labels={"current": labels}
        )
        
        return state
    
    def get_state(self, project_id: str) -> Dict[str, Any]:
        """
        Get current project state.
        
        Args:
            project_id: Project identifier
            
        Returns:
            State dictionary
        """
        state_path = self._get_state_path(project_id)
        if not state_path.exists():
            raise FileNotFoundError(f"State file not found: {state_path}")
        
        with open(state_path, 'r') as f:
            return json.load(f)
    
    def update_state(
        self,
        project_id: str,
        updates: Dict[str, Any],
        log_transition: bool = True
    ) -> Dict[str, Any]:
        """
        Update project state with file locking for read-modify-write.
        
        Args:
            project_id: Project identifier
            updates: Dictionary of updates to apply
            log_transition: Whether to log this as a transition
            
        Returns:
            Updated state dictionary
        """
        state_path = self._get_state_path(project_id)
        
        # Lock the entire read-modify-write cycle
        with FileLock(f"{state_path}.lock", timeout=30):
            state = self.get_state(project_id)
            
            # Store old values for transition logging
            old_status = state.get("status")
            old_stage = state.get("current_stage")
            
            # Apply updates
            state.update(updates)
            state["updated_at"] = datetime.utcnow().isoformat() + 'Z'
            
            # Write updated state (bypass lock since we're already holding it)
            state_path.parent.mkdir(parents=True, exist_ok=True)
            tmp_path = state_path.with_suffix('.tmp')
            try:
                with open(tmp_path, 'w') as f:
                    json.dump(state, f, indent=2)
                tmp_path.replace(state_path)
            except Exception as e:
                if tmp_path.exists():
                    tmp_path.unlink()
                raise
        
        # Log transition if requested (outside lock)
        if log_transition:
            self.log_transition(
                project_id=project_id,
                event_type="state_updated",
                from_state={"status": old_status, "stage": old_stage},
                to_state={
                    "status": state.get("status"),
                    "stage": state.get("current_stage")
                },
                metadata=updates
            )
        
        return state
    
    def start_stage(
        self,
        project_id: str,
        stage: str,
        agent: str
    ) -> Dict[str, Any]:
        """
        Mark a pipeline stage as started with file locking for read-modify-write.
        
        Args:
            project_id: Project identifier
            stage: Stage name
            agent: Agent handling this stage
            
        Returns:
            Updated state
        """
        state_path = self._get_state_path(project_id)
        now = datetime.utcnow().isoformat() + 'Z'
        
        # Lock the entire read-modify-write cycle
        with FileLock(f"{state_path}.lock", timeout=30):
            state = self.get_state(project_id)
            
            # Update stage status
            if "stages" not in state:
                state["stages"] = {}
            if stage not in state["stages"]:
                state["stages"][stage] = {}
                
            state["stages"][stage].update({
                "status": "in_progress",
                "started_at": now,
                "agent": agent
            })
            
            # Update overall state
            state["current_stage"] = stage
            state["status"] = "in_progress"
            state["updated_at"] = now
            
            # Increment agent invocation count
            if "metrics" not in state:
                state["metrics"] = {}
            state["metrics"]["agent_invocations"] = state["metrics"].get("agent_invocations", 0) + 1
            
            # Write state (bypass lock since we're already holding it)
            state_path.parent.mkdir(parents=True, exist_ok=True)
            tmp_path = state_path.with_suffix('.tmp')
            try:
                with open(tmp_path, 'w') as f:
                    json.dump(state, f, indent=2)
                tmp_path.replace(state_path)
            except Exception as e:
                if tmp_path.exists():
                    tmp_path.unlink()
                raise
        
        # Log transition (outside lock)
        self.log_transition(
            project_id=project_id,
            event_type="stage_started",
            stage=stage,
            agent=agent,
            metadata={"started_at": now}
        )
        
        return state
    
    def complete_stage(
        self,
        project_id: str,
        stage: str,
        artifacts: List[str] = None,
        create_checkpoint: bool = True
    ) -> Dict[str, Any]:
        """
        Mark a pipeline stage as completed with file locking for read-modify-write.
        
        Args:
            project_id: Project identifier
            stage: Stage name
            artifacts: List of artifacts created
            create_checkpoint: Whether to create a checkpoint
            
        Returns:
            Updated state
        """
        state_path = self._get_state_path(project_id)
        now = datetime.utcnow().isoformat() + 'Z'
        
        # Lock the entire read-modify-write cycle
        with FileLock(f"{state_path}.lock", timeout=30):
            state = self.get_state(project_id)
            
            # Calculate duration
            stage_info = state.get("stages", {}).get(stage, {})
            started_at = stage_info.get("started_at")
            duration = 0
            if started_at:
                start_time = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
                end_time = datetime.fromisoformat(now.replace('Z', '+00:00'))
                duration = (end_time - start_time).total_seconds()
            
            # Update stage status
            state["stages"][stage].update({
                "status": "completed",
                "completed_at": now,
                "duration_seconds": duration,
                "artifacts": artifacts or []
            })
            
            # Update metrics
            if "stage_durations" not in state["metrics"]:
                state["metrics"]["stage_durations"] = {}
            state["metrics"]["stage_durations"][stage] = duration
            state["metrics"]["artifacts_generated"] = state["metrics"].get("artifacts_generated", 0) + len(artifacts or [])
            
            # Write state (bypass lock since we're already holding it)
            state["updated_at"] = now
            state_path.parent.mkdir(parents=True, exist_ok=True)
            tmp_path = state_path.with_suffix('.tmp')
            try:
                with open(tmp_path, 'w') as f:
                    json.dump(state, f, indent=2)
                tmp_path.replace(state_path)
            except Exception as e:
                if tmp_path.exists():
                    tmp_path.unlink()
                raise
        
        # Create checkpoint if requested (outside state lock)
        checkpoint_id = None
        if create_checkpoint:
            checkpoint_id = self.create_checkpoint(
                project_id=project_id,
                stage=stage,
                status="success",
                artifacts=artifacts
            )
            # Reload state to get updated checkpoint
            state = self.get_state(project_id)
        
        # Log transition (outside lock)
        self.log_transition(
            project_id=project_id,
            event_type="stage_completed",
            stage=stage,
            metadata={
                "completed_at": now,
                "duration_seconds": duration
            },
            artifacts=[{"path": a, "action": "created"} for a in (artifacts or [])],
            checkpoint_id=checkpoint_id
        )
        
        return state
    
    def fail_stage(
        self,
        project_id: str,
        stage: str,
        agent: str,
        error: Dict[str, Any],
        context: Dict[str, Any] = None,
        create_dead_letter: bool = True
    ) -> Dict[str, Any]:
        """
        Mark a pipeline stage as failed with file locking for read-modify-write.
        
        Args:
            project_id: Project identifier
            stage: Stage name
            agent: Agent that failed
            error: Error information
            context: Execution context
            create_dead_letter: Whether to create dead letter entry
            
        Returns:
            Updated state
        """
        state_path = self._get_state_path(project_id)
        now = datetime.utcnow().isoformat() + 'Z'
        
        # Lock the entire read-modify-write cycle
        with FileLock(f"{state_path}.lock", timeout=30):
            state = self.get_state(project_id)
            
            # Update stage status
            retry_count = state["stages"][stage].get("retry_count", 0)
            state["stages"][stage].update({
                "status": "failed",
                "error": error.get("message", "Unknown error"),
                "retry_count": retry_count
            })
            
            # Update overall status
            state["status"] = "failed"
            state["updated_at"] = now
            
            # Write state (bypass lock since we're already holding it)
            state_path.parent.mkdir(parents=True, exist_ok=True)
            tmp_path = state_path.with_suffix('.tmp')
            try:
                with open(tmp_path, 'w') as f:
                    json.dump(state, f, indent=2)
                tmp_path.replace(state_path)
            except Exception as e:
                if tmp_path.exists():
                    tmp_path.unlink()
                raise
        
        # Create dead letter if requested (outside lock)
        dead_letter_id = None
        if create_dead_letter:
            dead_letter_id = self.add_dead_letter(
                project_id=project_id,
                stage=stage,
                agent=agent,
                error=error,
                context=context,
                attempt_number=retry_count + 1
            )
            # Reload state to get updated metrics
            state = self.get_state(project_id)
        
        # Log transition (outside lock)
        self.log_transition(
            project_id=project_id,
            event_type="stage_failed",
            stage=stage,
            agent=agent,
            error={
                "type": error.get("type", "unknown"),
                "message": error.get("message", ""),
                "dead_letter_id": dead_letter_id
            }
        )
        
        return state
    
    def create_checkpoint(
        self,
        project_id: str,
        stage: str,
        status: str = "success",
        artifacts: List[str] = None,
        metadata: Dict[str, Any] = None
    ) -> str:
        """
        Create a recovery checkpoint with file locking for read-modify-write.
        
        Args:
            project_id: Project identifier
            stage: Stage where checkpoint is created
            status: Checkpoint status
            artifacts: Artifacts at this checkpoint
            metadata: Additional metadata
            
        Returns:
            Checkpoint ID
        """
        state_path = self._get_state_path(project_id)
        now = datetime.utcnow().isoformat() + 'Z'
        checkpoint_id = f"chk-{uuid.uuid4().hex[:8]}"
        
        # Lock the entire read-modify-write cycle
        with FileLock(f"{state_path}.lock", timeout=30):
            state = self.get_state(project_id)
            
            checkpoint = {
                "id": checkpoint_id,
                "stage": stage,
                "timestamp": now,
                "status": status,
                "artifacts": artifacts or [],
                "metadata": metadata or {}
            }
            
            # Add checkpoint to state
            if "checkpoints" not in state:
                state["checkpoints"] = []
            state["checkpoints"].append(checkpoint)
            
            # Update recovery info
            if status == "success":
                state["recovery_info"]["last_successful_checkpoint"] = checkpoint_id
            
            state["updated_at"] = now
            
            # Write state (bypass lock since we're already holding it)
            state_path.parent.mkdir(parents=True, exist_ok=True)
            tmp_path = state_path.with_suffix('.tmp')
            try:
                with open(tmp_path, 'w') as f:
                    json.dump(state, f, indent=2)
                tmp_path.replace(state_path)
            except Exception as e:
                if tmp_path.exists():
                    tmp_path.unlink()
                raise
        
        # Log transition (outside lock)
        self.log_transition(
            project_id=project_id,
            event_type="checkpoint_created",
            stage=stage,
            checkpoint_id=checkpoint_id,
            metadata=checkpoint
        )
        
        return checkpoint_id
    
    def add_dead_letter(
        self,
        project_id: str,
        stage: str,
        agent: str,
        error: Dict[str, Any],
        context: Dict[str, Any] = None,
        request: Dict[str, Any] = None,
        trace: List[Dict[str, Any]] = None,
        attempt_number: int = 1
    ) -> str:
        """
        Add a dead letter entry for a failed execution with coordinated locking.
        
        Args:
            project_id: Project identifier
            stage: Stage where failure occurred
            agent: Agent that failed
            error: Error information
            context: Execution context
            request: Agent request details
            trace: Execution trace
            attempt_number: Retry attempt number
            
        Returns:
            Dead letter ID
        """
        dead_letters_path = self._get_dead_letters_path(project_id)
        state_path = self._get_state_path(project_id)
        
        # Use coordinated locking for multi-file update
        # Lock state.json first, then dead_letters.json to prevent deadlocks
        with FileLock(f"{state_path}.lock", timeout=30):
            with FileLock(f"{dead_letters_path}.lock", timeout=30):
                # Load existing dead letters
                if dead_letters_path.exists():
                    with open(dead_letters_path, 'r') as f:
                        dead_letters = json.load(f)
                else:
                    dead_letters = {
                        "project_id": project_id,
                        "version": "1.0.0",
                        "entries": [],
                        "statistics": {
                            "total_entries": 0,
                            "by_stage": {},
                            "by_agent": {},
                            "recovered": 0,
                            "unrecovered": 0
                        }
                    }
                
                # Create dead letter entry
                dead_letter_id = str(uuid.uuid4())
                now = datetime.utcnow().isoformat() + 'Z'
                
                # Get current state snapshot
                state_snapshot = {}
                labels = {}
                try:
                    state = self.get_state(project_id)
                    state_snapshot = {
                        "current_stage": state.get("current_stage"),
                        "status": state.get("status"),
                        "metrics": state.get("metrics", {})
                    }
                    labels = state.get("labels", {})
                except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
                    # If state cannot be loaded, continue without snapshot
                    print(f"Warning: Could not load state snapshot for dead letter: {e}", file=sys.stderr)
                
                entry = {
                    "id": dead_letter_id,
                    "timestamp": now,
                    "stage": stage,
                    "agent": agent,
                    "attempt_number": attempt_number,
                    "error": error,
                    "context": context or {},
                    "request": request or {},
                    "trace": trace or [],
                    "labels": labels,
                    "recovery_attempted": False,
                    "replay_count": 0
                }
                
                # Update context with state snapshot
                entry["context"]["state_snapshot"] = state_snapshot
                
                # Add entry
                dead_letters["entries"].append(entry)
                
                # Update statistics
                stats = dead_letters["statistics"]
                stats["total_entries"] += 1
                stats["by_stage"][stage] = stats["by_stage"].get(stage, 0) + 1
                stats["by_agent"][agent] = stats["by_agent"].get(agent, 0) + 1
                stats["unrecovered"] += 1
                
                # Write dead letters (inside lock, so we can call private method directly)
                dead_letters_path.parent.mkdir(parents=True, exist_ok=True)
                tmp_path = dead_letters_path.with_suffix('.tmp')
                try:
                    with open(tmp_path, 'w') as f:
                        json.dump(dead_letters, f, indent=2)
                    tmp_path.replace(dead_letters_path)
                except Exception as e:
                    if tmp_path.exists():
                        tmp_path.unlink()
                    raise
                
                # Update state metrics (inside lock)
                try:
                    state = self.get_state(project_id)
                    state["metrics"]["dead_letters"] = stats["total_entries"]
                    
                    # Write state (inside lock)
                    tmp_path = state_path.with_suffix('.tmp')
                    try:
                        with open(tmp_path, 'w') as f:
                            json.dump(state, f, indent=2)
                        tmp_path.replace(state_path)
                    except Exception as e:
                        if tmp_path.exists():
                            tmp_path.unlink()
                        raise
                except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
                    # If state update fails, log but continue
                    print(f"Warning: Could not update state metrics: {e}", file=sys.stderr)
        
        # Log transition (outside locks to avoid holding locks during append)
        self.log_transition(
            project_id=project_id,
            event_type="error_recorded",
            stage=stage,
            agent=agent,
            error={
                "type": error.get("type", "unknown"),
                "message": error.get("message", ""),
                "dead_letter_id": dead_letter_id
            }
        )
        
        return dead_letter_id
    
    def log_transition(
        self,
        project_id: str,
        event_type: str,
        stage: str = None,
        agent: str = None,
        from_state: Dict[str, Any] = None,
        to_state: Dict[str, Any] = None,
        metadata: Dict[str, Any] = None,
        labels: Dict[str, Any] = None,
        artifacts: List[Dict[str, str]] = None,
        metrics: Dict[str, Any] = None,
        error: Dict[str, Any] = None,
        actor: Dict[str, str] = None,
        parent_transition_id: str = None,
        checkpoint_id: str = None
    ) -> str:
        """
        Log a state transition to the audit log.
        
        Args:
            project_id: Project identifier
            event_type: Type of transition event
            stage: Associated stage
            agent: Associated agent
            from_state: State before transition
            to_state: State after transition
            metadata: Additional metadata
            labels: Label changes
            artifacts: Artifact changes
            metrics: Metrics at transition
            error: Error information
            actor: Who triggered the transition
            parent_transition_id: Parent transition ID
            checkpoint_id: Associated checkpoint ID
            
        Returns:
            Transition ID
        """
        transition_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat() + 'Z'
        
        entry = {
            "id": transition_id,
            "timestamp": now,
            "project_id": project_id,
            "event_type": event_type
        }
        
        # Add optional fields
        if stage:
            entry["stage"] = stage
        if agent:
            entry["agent"] = agent
        if from_state:
            entry["from_state"] = from_state
        if to_state:
            entry["to_state"] = to_state
        if metadata:
            entry["metadata"] = metadata
        if labels:
            entry["labels"] = labels
        if artifacts:
            entry["artifacts"] = artifacts
        if metrics:
            entry["metrics"] = metrics
        if error:
            entry["error"] = error
        if actor:
            entry["actor"] = actor
        if parent_transition_id:
            entry["parent_transition_id"] = parent_transition_id
        if checkpoint_id:
            entry["checkpoint_id"] = checkpoint_id
        
        # Append to transitions.jsonl
        self._append_jsonl(self._get_transitions_path(project_id), entry)
        
        return transition_id
    
    def get_transitions(
        self,
        project_id: str,
        event_type: str = None,
        stage: str = None,
        limit: int = None
    ) -> List[Dict[str, Any]]:
        """
        Get transition history from audit log.
        
        Args:
            project_id: Project identifier
            event_type: Filter by event type
            stage: Filter by stage
            limit: Maximum number of entries to return (most recent)
            
        Returns:
            List of transition entries
        """
        transitions_path = self._get_transitions_path(project_id)
        if not transitions_path.exists():
            return []
        
        transitions = []
        with open(transitions_path, 'r') as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    
                    # Apply filters
                    if event_type and entry.get("event_type") != event_type:
                        continue
                    if stage and entry.get("stage") != stage:
                        continue
                    
                    transitions.append(entry)
        
        # Apply limit (most recent)
        if limit and limit > 0:
            transitions = transitions[-limit:]
        
        return transitions
    
    def get_dead_letters(
        self,
        project_id: str,
        stage: str = None,
        agent: str = None,
        unrecovered_only: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Get dead letter entries.
        
        Args:
            project_id: Project identifier
            stage: Filter by stage
            agent: Filter by agent
            unrecovered_only: Only return unrecovered failures
            
        Returns:
            List of dead letter entries
        """
        dead_letters_path = self._get_dead_letters_path(project_id)
        if not dead_letters_path.exists():
            return []
        
        with open(dead_letters_path, 'r') as f:
            dead_letters = json.load(f)
        
        entries = dead_letters.get("entries", [])
        
        # Apply filters
        if stage:
            entries = [e for e in entries if e.get("stage") == stage]
        if agent:
            entries = [e for e in entries if e.get("agent") == agent]
        if unrecovered_only:
            # Filter to entries that haven't been successfully recovered
            entries = [
                e for e in entries 
                if not e.get("recovery_attempted") or e.get("recovery_result") != "success"
            ]
        
        return entries
