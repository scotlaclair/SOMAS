"""
Feedback Loop Module for SOMAS Autonomous Pipeline

Enables spec-simulation feedback loop where simulation can send projects
back to specification stage if gaps or issues are found.

@copilot-context: Critical for autonomous execution
"""

import logging
from typing import Dict, Any, Optional, List
from enum import Enum

logger = logging.getLogger(__name__)


class SimulationStatus(Enum):
    """Status codes for simulation execution"""
    READY = "ready"                    # Ready to proceed to architecture
    NEEDS_REVISION = "needs_revision"  # Must go back to specification
    BLOCKED = "blocked"                # Critical issues requiring human intervention


class FeedbackType(Enum):
    """Types of feedback that can be sent"""
    CIRCULAR_DEPENDENCIES = "circular_dependencies"
    UNREALISTIC_ESTIMATES = "unrealistic_estimates"
    MISSING_DEPENDENCIES = "missing_dependencies"
    INSUFFICIENT_GRANULARITY = "insufficient_granularity"
    HIGH_RISK_NO_MITIGATION = "high_risk_no_mitigation"
    INVALID_TASK_GRAPH = "invalid_task_graph"


class SpecSimulationFeedbackLoop:
    """
    Manages the feedback loop between specification and simulation stages.
    
    Simulation can send projects back to specification if gaps found.
    Maximum 3 iterations before escalation to human.
    """
    
    def __init__(self, max_iterations: int = 3):
        """
        Initialize feedback loop
        
        Args:
            max_iterations: Maximum feedback iterations before escalation
        """
        self.max_iterations = max_iterations
        self.iteration_count = {}  # Track iterations per project
        
    def execute_simulation_stage(
        self, 
        project_id: str,
        spec: Dict[str, Any],
        simulator_agent: Any,
        specifier_agent: Any
    ) -> Dict[str, Any]:
        """
        Execute simulation stage with feedback loop capability
        
        Args:
            project_id: Unique project identifier
            spec: Specification document
            simulator_agent: Agent for simulation
            specifier_agent: Agent for specification revision
            
        Returns:
            Simulation results or revised specification
        """
        # Initialize iteration counter for this project
        if project_id not in self.iteration_count:
            self.iteration_count[project_id] = 0
            
        logger.info(f"Executing simulation for project {project_id} "
                   f"(iteration {self.iteration_count[project_id] + 1}/{self.max_iterations})")
        
        # Run simulation
        simulation = simulator_agent.simulate(spec)
        
        # Check simulation status
        if simulation.status == SimulationStatus.READY:
            logger.info(f"Project {project_id} ready to proceed to architecture")
            return simulation
            
        elif simulation.status == SimulationStatus.NEEDS_REVISION:
            # Check if we've exceeded max iterations
            if self.iteration_count[project_id] >= self.max_iterations:
                logger.error(f"Project {project_id} exceeded max feedback iterations")
                return self._escalate_to_human(
                    project_id, 
                    simulation.feedback_required,
                    "Max iterations exceeded"
                )
            
            # Send feedback to Specifier
            logger.info(f"Sending feedback to specifier for project {project_id}")
            logger.debug(f"Feedback: {simulation.feedback_required}")
            
            revised_spec = specifier_agent.revise_specification(
                spec,
                feedback=simulation.feedback_required
            )
            
            # Increment iteration counter
            self.iteration_count[project_id] += 1
            
            # Re-simulate (recursive, respects max_iterations)
            return self.execute_simulation_stage(
                project_id,
                revised_spec,
                simulator_agent,
                specifier_agent
            )
            
        elif simulation.status == SimulationStatus.BLOCKED:
            logger.error(f"Project {project_id} blocked with critical issues")
            return self._escalate_to_human(
                project_id,
                simulation.blocking_issues,
                "Critical blocking issues"
            )
            
        else:
            logger.error(f"Unknown simulation status: {simulation.status}")
            return self._escalate_to_human(
                project_id,
                {"error": "Unknown status"},
                "Unknown simulation status"
            )
    
    def _escalate_to_human(
        self,
        project_id: str,
        issues: List[Dict[str, Any]],
        reason: str
    ) -> Dict[str, Any]:
        """
        Escalate project to human review
        
        Args:
            project_id: Project identifier
            issues: List of issues requiring human attention
            reason: Reason for escalation
            
        Returns:
            Escalation result
        """
        logger.warning(f"Escalating project {project_id} to human: {reason}")
        
        escalation_result = {
            "status": "escalated",
            "project_id": project_id,
            "reason": reason,
            "issues": issues,
            "iterations_attempted": self.iteration_count.get(project_id, 0),
            "action_required": "Human review and manual specification revision",
            "escalation_owner": "@scotlaclair"
        }
        
        # Log escalation for tracking
        self._log_escalation(escalation_result)
        
        return escalation_result
    
    def _log_escalation(self, escalation: Dict[str, Any]) -> None:
        """
        Log escalation for metrics and audit trail
        
        Args:
            escalation: Escalation details
        """
        # In production, this would write to persistent storage
        logger.warning(f"ESCALATION: {escalation}")
        
    def reset_project_counter(self, project_id: str) -> None:
        """
        Reset iteration counter for a project
        
        Args:
            project_id: Project identifier
        """
        if project_id in self.iteration_count:
            del self.iteration_count[project_id]
            logger.info(f"Reset iteration counter for project {project_id}")
    
    def get_project_stats(self, project_id: str) -> Dict[str, Any]:
        """
        Get statistics for a project's feedback loop
        
        Args:
            project_id: Project identifier
            
        Returns:
            Statistics dictionary
        """
        return {
            "project_id": project_id,
            "iterations": self.iteration_count.get(project_id, 0),
            "max_iterations": self.max_iterations,
            "remaining_iterations": max(0, self.max_iterations - self.iteration_count.get(project_id, 0))
        }


class SimulationValidator:
    """
    Validates simulation results for common issues
    """
    
    @staticmethod
    def validate_task_graph(task_graph: Dict[str, Any]) -> Optional[List[str]]:
        """
        Validate task graph for issues
        
        Args:
            task_graph: Task dependency graph
            
        Returns:
            List of issues found, or None if valid
        """
        issues = []
        
        # Check for circular dependencies
        if SimulationValidator._has_circular_dependencies(task_graph):
            issues.append("Circular dependencies detected in task graph")
        
        # Check for orphaned tasks
        orphaned = SimulationValidator._find_orphaned_tasks(task_graph)
        if orphaned:
            issues.append(f"Orphaned tasks found: {', '.join(orphaned)}")
        
        # Check for unrealistic estimates
        unrealistic = SimulationValidator._find_unrealistic_estimates(task_graph)
        if unrealistic:
            issues.append(f"Unrealistic task estimates: {', '.join(unrealistic)}")
        
        return issues if issues else None
    
    @staticmethod
    def _has_circular_dependencies(task_graph: Dict[str, Any]) -> bool:
        """
        Check for circular dependencies using DFS
        
        Note: This is a simplified placeholder implementation for POC.
        Production implementation would use proper graph algorithms with DFS/BFS.
        
        Returns:
            bool: Always False in placeholder (no validation performed)
        """
        # TODO: Implement proper cycle detection algorithm
        # For POC, we assume well-formed task graphs
        return False
    
    @staticmethod
    def _find_orphaned_tasks(task_graph: Dict[str, Any]) -> List[str]:
        """
        Find tasks with no path to root or leaf
        
        Note: This is a placeholder implementation for POC.
        Production would traverse graph to find disconnected tasks.
        
        Returns:
            List[str]: Always empty in placeholder (no validation performed)
        """
        # TODO: Implement graph traversal to find orphaned nodes
        # For POC, we assume all tasks are connected
        return []
    
    @staticmethod
    def _find_unrealistic_estimates(task_graph: Dict[str, Any]) -> List[str]:
        """
        Find tasks with unrealistic duration estimates
        
        Note: This is a placeholder implementation for POC.
        Production would analyze estimates against historical data.
        
        Returns:
            List[str]: Always empty in placeholder (no validation performed)
        """
        # TODO: Implement estimate validation against benchmarks
        # For POC, we accept all estimates
        return []


def load_artifact(project_id: str, artifact_name: str) -> Dict[str, Any]:
    """
    Load artifact from project directory
    
    Note: This is a placeholder implementation for POC.
    Production would read actual files from projects/{project_id}/artifacts/
    
    Args:
        project_id: Project identifier
        artifact_name: Name of artifact file
        
    Returns:
        Artifact contents as dictionary (empty dict in placeholder)
    """
    # TODO: Implement actual file reading
    # import yaml or json, read from filesystem
    logger.info(f"Loading artifact {artifact_name} for project {project_id}")
    return {}


def save_artifact(project_id: str, artifact_name: str, content: Dict[str, Any]) -> None:
    """
    Save artifact to project directory
    
    Note: This is a placeholder implementation for POC.
    Production would write actual files to projects/{project_id}/artifacts/
    
    Args:
        project_id: Project identifier
        artifact_name: Name of artifact file
        content: Artifact contents
    """
    # TODO: Implement actual file writing
    # import yaml or json, write to filesystem
    logger.info(f"Saving artifact {artifact_name} for project {project_id}")
