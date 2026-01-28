#!/usr/bin/env python3
"""
SOMAS Agent Runner

This script wraps LLM agent invocations for the SOMAS pipeline.
It accepts task parameters and coordinates agent execution with proper
context and output management.

Usage:
    # Single task mode
    python runner.py --agent <name> ...

    # Autonomous mode
    python runner.py --mode autonomous --project_id <id>

Security:
    - All file paths are validated to prevent path traversal
    - Project IDs are validated against safe patterns
    - No shell injection via proper subprocess handling
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

# Import state manager
try:
    from .state_manager import StateManager
except ImportError:
    from state_manager import StateManager


class SOMASRunner:
    """Orchestrates agent execution for SOMAS pipeline tasks."""

    def __init__(self, config_path: str = ".somas/config.yml"):
        """Initialize runner with SOMAS configuration."""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.repo_root = Path.cwd()
        self.state_manager = StateManager()

    def _load_config(self) -> Dict[str, Any]:
        """Load and parse SOMAS configuration."""
        try:
            with open(self.config_path, "r") as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config from {self.config_path}: {e}", file=sys.stderr)
            sys.exit(1)

    def _validate_project_id(self, project_id: str) -> bool:
        """
        Validate project ID to prevent path traversal attacks.

        Args:
            project_id: Project identifier to validate

        Returns:
            True if valid, False otherwise
        """
        # Must match pattern: project-<number>
        pattern = r"^project-\d+$"
        return bool(re.match(pattern, project_id))

    def _validate_path(self, path: str) -> bool:
        """
        Validate file path to prevent path traversal.

        Args:
            path: File path to validate

        Returns:
            True if safe, False otherwise
        """
        try:
            # Resolve to absolute path
            abs_path = Path(path).resolve()
            # Ensure it's within the repository
            abs_path.relative_to(self.repo_root)
            return True
        except (ValueError, RuntimeError):
            return False

    def _get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """
        Get agent configuration from SOMAS config.

        Args:
            agent_name: Name of the agent

        Returns:
            Agent configuration dictionary
        """
        agents_config = self.config.get("agents", {}).get("agent_configs", {})

        if agent_name not in agents_config:
            print(
                f"Warning: Agent '{agent_name}' not found in config. Using defaults.",
                file=sys.stderr,
            )
            return {"provider": "gpt_5_2", "description": f"Agent: {agent_name}"}

        return agents_config[agent_name]

    def _load_context_files(self, context_files: List[str]) -> Dict[str, str]:
        """
        Load content from context files.

        Args:
            context_files: List of file paths to load

        Returns:
            Dictionary mapping file paths to their content
        """
        context = {}

        for file_path in context_files:
            # Validate path
            if not self._validate_path(file_path):
                print(f"Warning: Skipping invalid path: {file_path}", file=sys.stderr)
                continue

            try:
                with open(file_path, "r") as f:
                    context[file_path] = f.read()
            except Exception as e:
                print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)

        return context

    def run_task(
        self,
        agent: str,
        task_name: str,
        task_desc: str,
        context_files: List[str],
        output_path: str,
        project_id: Optional[str] = None,
        stage: Optional[str] = None,
    ) -> int:
        """
        Execute a single task with the specified agent.

        Args:
            agent: Name of the agent to use
            task_name: Short name of the task
            task_desc: Detailed description of the task
            context_files: List of file paths providing context
            output_path: Where to write the output
            project_id: Optional project identifier
            stage: Optional pipeline stage name

        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        # Validate project_id if provided
        if project_id and not self._validate_project_id(project_id):
            print(f"Error: Invalid project_id format: {project_id}", file=sys.stderr)
            return 1

        # Validate output path
        if not self._validate_path(output_path):
            print(f"Error: Invalid output path: {output_path}", file=sys.stderr)
            return 1

        # Get agent configuration
        agent_config = self._get_agent_config(agent)
        provider = agent_config.get("provider", "gpt_5_2")

        # Load context files
        context = self._load_context_files(context_files)

        # Prepare task metadata
        task_metadata = {
            "task_name": task_name,
            "task_description": task_desc,
            "agent": agent,
            "provider": provider,
            "context_files": list(context.keys()),
            "output_path": output_path,
            "project_id": project_id,
            "stage": stage,
        }

        print(f"Executing task: {task_name}")
        print(f"Agent: {agent} (Provider: {provider})")
        print(f"Context files: {len(context)}")

        # Log agent invocation to state if project_id provided
        if project_id and stage:
            try:
                self.state_manager.log_transition(
                    project_id=project_id,
                    event_type="agent_invoked",
                    stage=stage,
                    agent=agent,
                    metadata={
                        "task_name": task_name,
                        "task_description": task_desc,
                        "provider": provider,
                    },
                )
            except Exception as e:
                print(f"Warning: Could not log agent invocation: {e}", file=sys.stderr)

        # TODO: Actual agent invocation would happen here
        # For now, create a placeholder output
        start_time = datetime.utcnow()
        success = False
        error_info = None

        try:
            # Ensure output directory exists
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            # Write task metadata and placeholder result
            with open(output_path, "w") as f:
                f.write(f"# Task: {task_name}\n\n")
                f.write(f"**Description:** {task_desc}\n\n")
                f.write(f"**Agent:** {agent}\n")
                f.write(f"**Provider:** {provider}\n\n")
                f.write("## Status\n\n")
                f.write(
                    "Task execution placeholder. Integration with actual AI agents pending.\n\n"
                )
                f.write("## Metadata\n\n")
                f.write("```json\n")
                json.dump(task_metadata, f, indent=2)
                f.write("\n```\n")

            print(f"Task completed successfully. Output written to: {output_path}")
            success = True

        except Exception as e:
            print(f"Error executing task: {e}", file=sys.stderr)
            error_info = {"type": type(e).__name__, "message": str(e)}

        # Log completion or failure to state if project_id provided
        if project_id and stage:
            try:
                end_time = datetime.utcnow()
                duration = (end_time - start_time).total_seconds()

                if success:
                    self.state_manager.log_transition(
                        project_id=project_id,
                        event_type="agent_completed",
                        stage=stage,
                        agent=agent,
                        metadata={"task_name": task_name, "output_path": output_path},
                        metrics={"duration_seconds": duration},
                        artifacts=[{"path": output_path, "action": "created"}],
                    )
                else:
                    self.state_manager.log_transition(
                        project_id=project_id,
                        event_type="agent_failed",
                        stage=stage,
                        agent=agent,
                        error=error_info,
                        metadata={"task_name": task_name},
                        metrics={"duration_seconds": duration},
                    )

                    # Create dead letter entry for failure
                    self.state_manager.add_dead_letter(
                        project_id=project_id,
                        stage=stage,
                        agent=agent,
                        error=error_info,
                        context={
                            "task_name": task_name,
                            "task_description": task_desc,
                            "context_files": list(context.keys()),
                            "output_path": output_path,
                        },
                        request={"task": task_name, "parameters": task_metadata},
                    )

            except Exception as e:
                print(f"Warning: Could not log task completion: {e}", file=sys.stderr)

        return 0 if success else 1

    def run_autonomous_pipeline(self, project_id: str) -> int:
        """
        Execute the full autonomous pipeline stages sequentially.

        Args:
            project_id: Project identifier

        Returns:
            Exit code
        """
        print(f"Starting Autonomous Pipeline for {project_id}")

        # Define the pipeline sequence
        # Format: (agent, task_name, description, output_file, stage)
        pipeline_stages = [
            (
                "planner",
                "Ideation",
                "Create initial plan",
                "initial_plan.yml",
                "signal",
            ),
            (
                "specifier",
                "Specification",
                "Create detailed specs",
                "SPEC.md",
                "design",
            ),
            (
                "simulator",
                "Simulation",
                "Optimize execution plan",
                "execution_plan.yml",
                "grid",
            ),
            (
                "architect",
                "Architecture",
                "Design system architecture",
                "ARCHITECTURE.md",
                "design",
            ),
            (
                "implementer",
                "Implementation",
                "Generate source code",
                "implementation_report.md",
                "mcp",
            ),
            (
                "validator",
                "Validation",
                "Run tests and validation",
                "test_results.json",
                "pulse",
            ),
            (
                "tester",
                "Hardening",
                "Stress testing and edge cases",
                "hardening_report.md",
                "pulse",
            ),
            (
                "security",
                "Security Scan",
                "Vulnerability assessment",
                "security_scan.md",
                "pulse",
            ),
            ("reviewer", "Code Review", "Quality review", "review_report.md", "pulse"),
            (
                "merger",
                "Integration",
                "Prepare for merge",
                "integration_report.md",
                "synapse",
            ),
            (
                "deployer",
                "Release",
                "Prepare deployment artifacts",
                "deployment_report.md",
                "velocity",
            ),
            (
                "operator",
                "Operations",
                "Monitor operational metrics",
                "operations_report.md",
                "vibe",
            ),
            (
                "analyzer",
                "Learning",
                "Analyze pipeline performance and generate insights",
                "analysis_report.md",
                "whole",
            )
        ]

        project_dir = self.repo_root / ".somas" / "projects" / project_id
        artifacts_dir = project_dir / "artifacts"
        artifacts_dir.mkdir(parents=True, exist_ok=True)

        context_files = []

        for agent, task, desc, artifact, stage in pipeline_stages:
            print(f"\n>>> Executing Stage: {task} ({agent})")

            output_path = str(artifacts_dir / artifact)

            # Add previous artifacts to context
            current_context = [
                str(artifacts_dir / f)
                for f in ["initial_plan.yml", "SPEC.md", "ARCHITECTURE.md"]
                if (artifacts_dir / f).exists()
            ]

            exit_code = self.run_task(
                agent=agent,
                task_name=task,
                task_desc=desc,
                context_files=current_context,
                output_path=output_path,
                project_id=project_id,
                stage=stage,
            )

            if exit_code != 0:
                print(f"Pipeline failed at stage: {task}")
                return exit_code

        print("\n>>> Autonomous Pipeline Completed Successfully")
        return 0


def main():
    """Main entry point for the runner CLI."""
    parser = argparse.ArgumentParser(
        description="SOMAS Agent Runner - Execute pipeline tasks with AI agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Execute a single implementation task
  python runner.py --agent coder --task_name "API-Implementation" \\
      --task_desc "Implement REST API endpoints" \\
      --context_files "SPEC.md,ARCHITECTURE.md" \\
      --output_path "artifacts/task_result.md"

  # Execute with project context
  python runner.py --agent coder --task_name "Database-Setup" \\
      --task_desc "Create database schema" \\
      --context_files "data_models.yml" \\
      --output_path "artifacts/db_result.md" \\
      --project_id "project-123"

  # Execute autonomous pipeline
  python runner.py --mode autonomous --project_id "project-123"
        """,
    )

    parser.add_argument(
        "--mode",
        choices=["task", "autonomous"],
        default="task",
        help="Execution mode: single task or full autonomous pipeline",
    )

    parser.add_argument(
        "--agent",
        required=False,
        help="Name of the agent to use (e.g., coder, architect, tester)",
    )

    parser.add_argument(
        "--task_name",
        required=False,
        help='Short name for the task (e.g., "API-Implementation")',
    )

    parser.add_argument(
        "--task_desc",
        required=False,
        help="Detailed description of what the task should accomplish",
    )

    parser.add_argument(
        "--context_files",
        required=False,
        help="Comma-separated list of file paths to provide as context",
    )

    parser.add_argument(
        "--output_path", required=False, help="Path where task output should be written"
    )

    parser.add_argument(
        "--project_id",
        required=False,
        help='Optional project identifier (e.g., "project-123")',
    )

    parser.add_argument(
        "--stage",
        required=False,
        help='Optional pipeline stage name (e.g., "implementation")',
    )

    parser.add_argument(
        "--config",
        default=".somas/config.yml",
        help="Path to SOMAS configuration file (default: .somas/config.yml)",
    )

    args = parser.parse_args()

    # Initialize runner
    runner = SOMASRunner(config_path=args.config)

    if args.mode == "autonomous":
        if not args.project_id:
            parser.error("--project_id is required for autonomous mode")
        exit_code = runner.run_autonomous_pipeline(args.project_id)
    else:
        # Validate required args for task mode
        if not all([args.agent, args.task_name, args.task_desc, args.output_path]):
            parser.error(
                "Task mode requires --agent, --task_name, --task_desc, and --output_path"
            )

        # Parse context files
        context_files = [
            f.strip() for f in (args.context_files or "").split(",") if f.strip()
        ]

        # Execute task
        exit_code = runner.run_task(
            agent=args.agent,
            task_name=args.task_name,
            task_desc=args.task_desc,
            context_files=context_files,
            output_path=args.output_path,
            project_id=args.project_id,
            stage=args.stage,
        )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
