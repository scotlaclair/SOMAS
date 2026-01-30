"""
SOMAS APO (Autonomous Prompt Optimization) Module.

This module provides the cognitive enhancement layer for all SOMAS agents,
enabling them to self-select optimal mental models and reasoning strategies
for any task.

Components:
    Mental Models:
        - First Principles Thinking: Break down to fundamental truths
        - Inversion: Consider what could go wrong
        - Second-Order Thinking: Consider downstream effects
        - OODA Loop: Observe, Orient, Decide, Act
        - Occam's Razor: Prefer simpler solutions
        - Six Thinking Hats: Multiple perspective analysis
        - Tree of Thoughts: Branching exploration of options

    Task Analyzer:
        - Complexity scoring (simple, moderate, complex)
        - Domain detection with confidence scoring
        - Risk factor assessment
        - Automatic model routing based on complexity

    Chain Strategies:
        - Sequential: Linear step-by-step processing
        - Collision: Multiple perspectives resolved
        - Draft-Critique-Refine: Iterative improvement
        - Parallel Synthesis: Concurrent exploration with merge
        - Strategic Diamond: Diverge then converge

    Quality Verification:
        - Completeness, correctness, clarity checks
        - Iterative improvement loop (max 3 iterations)
        - Human escalation for unresolvable issues

Configuration:
    APO is configured in ``.somas/config.yml`` under the ``apo`` section:

    - ``enabled``: Toggle APO for all agents
    - ``mental_models``: Available models and agent preferences
    - ``task_analyzer``: Complexity thresholds and routing rules
    - ``chains``: Strategy selection rules
    - ``quality``: Verification checklist and loop settings

Usage Flow:
    1. Task received by agent
    2. Task analyzer scores complexity
    3. Appropriate mental models selected
    4. Chain strategy determined
    5. Agent processes with APO enhancement
    6. Quality verification loop
    7. Output with reasoning trail

Example:
    APO configuration for an agent::

        apo:
          enabled: true
          mental_models:
            agent_preferences:
              specifier:
                prefer: ["inversion", "second_order_thinking"]
          task_analyzer:
            minimum_complexity_for_apo: 2.0
            auto_routing:
              enabled: true

Anti-Patterns Prevented:
    - Early answering without analysis
    - Single-perspective thinking
    - Skipping verification
    - Overconfident outputs

See Also:
    - docs/somas/apo-guide.md for detailed APO documentation
    - .somas/apo/mental-models.yml for model definitions
    - .somas/apo/task-analyzer.yml for analyzer configuration
"""

__all__ = []
