"""
SOMAS Core Module.

This module contains the core functionality for the SOMAS autonomous pipeline,
including orchestration, state management, and utility functions.

Components:
    state_manager: JSON-based state persistence with checkpointing and recovery
    runner: Agent execution and pipeline orchestration
    feedback_loop: Spec-simulation feedback loop for iterative refinement
    circuit_breaker: Fault tolerance for external service calls

State Management:
    The core module provides robust state persistence through three files:

    - ``state.json``: Complete pipeline state with checkpoints and metrics
    - ``dead_letters.json``: Failed agent contexts for recovery and replay
    - ``transitions.jsonl``: Chronological audit log of all state transitions

Key Classes:
    StateManager: Manages pipeline state with checkpoint rotation
    SpecSimulationFeedbackLoop: Handles iterative spec refinement
    CircuitBreaker: Prevents cascading failures in external calls

Example:
    Using the state manager::

        from somas.core.state_manager import StateManager

        manager = StateManager(project_id="my-project")
        manager.create_checkpoint("implementation", {"files": ["main.py"]})
        state = manager.get_current_state()

Configuration:
    State manager settings in ``.somas/config.yml``::

        state_manager:
          max_checkpoints: 20  # Number of checkpoints to retain

See Also:
    - docs/somas/STATE_PERSISTENCE.md for detailed state management guide
    - .somas/config.yml for configuration options
"""

__version__ = "1.0.0"
__all__ = ["__version__"]
