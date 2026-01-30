"""
SOMAS Agents Module.

This module contains AI agent implementations and utilities for the SOMAS
autonomous pipeline. Each agent is specialized for specific pipeline tasks
and optimized with appropriate AI models.

Agent Types:
    Pipeline Agents:
        - Orchestrator: Pipeline coordination and state management
        - Triage: Request classification and routing
        - Planner: Requirements analysis and roadmap creation
        - Specifier: Complete specification generation
        - Simulator: Monte Carlo simulation for task optimization
        - Decomposer: Atomic task decomposition
        - Coder/Implementer: Production-ready code generation
        - Validator: Comprehensive validation and testing
        - Merger: Code integration and merge conflict resolution
        - Tester: Stress testing and hardening
        - Deployer: Deployment preparation and release
        - Operator: Operational monitoring and SLO tracking
        - Analyzer: Post-mortem analysis and learning loop

    Support Agents:
        - Advisor: Strategic guidance and recommendations
        - Debugger: Bug investigation and fixes
        - Security: Vulnerability scanning and security review
        - Documenter: Documentation and API references

Utilities:
    cost_tracker: Usage tracking for subscription optimization

Agent Configuration:
    Each agent is configured through YAML files in ``.somas/agents/``:

    - Role and responsibilities
    - AI model provider (e.g., Claude Sonnet 4.5, GPT-5.2)
    - Prompt templates and instructions
    - Output format specifications
    - Quality checks

Example:
    Agent configuration structure::

        # .somas/agents/implementer.yml
        role: "Code Implementation Specialist"
        provider: "claude_sonnet_4_5"
        instructions: |
          Generate production-ready code based on architecture design.
        output_format:
          - "Source code files"
          - "Unit tests"

See Also:
    - .somas/agents/ for individual agent configurations
    - .github/agents/ for GitHub Copilot integration instructions
    - docs/somas/developer-guide.md for agent development guide
"""

__all__ = []
