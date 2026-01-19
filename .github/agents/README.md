# SOMAS Custom Agents

This directory contains the configuration and profiles for the 12 specialized GitHub Copilot custom agents that power the SOMAS (Self-Sovereign Orchestrated Multi-Agent System) development pipeline.

## Agent Overview

SOMAS uses a **multi-model approach** to maximize agent effectiveness by matching each agent's cognitive requirements to the optimal AI model based on 2026 benchmarks and specialized capabilities.

| Agent | Model | Role | Stage |
|-------|-------|------|-------|
| [somas-requirements](./somas-requirements.md) | o1 | Requirements extraction and analysis | Ideation/Specification |
| [somas-architect](./somas-architect.md) | Claude 3.7 Sonnet | System architecture and design | Architecture |
| [somas-implementer](./somas-implementer.md) | Claude 3.7 Sonnet | Production code generation | Implementation |
| [somas-tester](./somas-tester.md) | GPT-4o | Test generation and QA | Validation |
| [somas-reviewer](./somas-reviewer.md) | o1 | Code quality and logic review | Validation |
| [somas-security](./somas-security.md) | o1 | Security analysis and vulnerability detection | Validation |
| [somas-optimizer](./somas-optimizer.md) | o1 | Performance analysis and optimization | Validation |
| [somas-documenter](./somas-documenter.md) | Gemini 2.0 Flash | Comprehensive documentation generation | Staging |
| [somas-debugger](./somas-debugger.md) | o1 | Bug investigation and root cause analysis | As needed |
| [somas-merger](./somas-merger.md) | GPT-4o | Merge conflict resolution | As needed |
| [somas-orchestrator](./somas-orchestrator.md) | GPT-4o | Pipeline coordination and state management | All stages |
| [somas-advisor](./somas-advisor.md) | o1 | Strategic planning and architectural decisions | As needed |

## Model Selection Strategy

SOMAS uses a **multi-model strategy** to maximize agent effectiveness across the SDLC pipeline. Rather than using a single AI model for all agents, we match each agent's cognitive requirements to the optimal model based on 2026 benchmarks and specialized capabilities.

### Reasoning-Heavy Agents (o1)

Used for agents requiring deep logical analysis, adversarial thinking, and deductive reasoning:

- **somas-requirements**: Disambiguating vague inputs and finding edge cases
- **somas-reviewer**: Identifying subtle logic flaws
- **somas-security**: Adversarial security analysis
- **somas-optimizer**: Algorithmic complexity analysis
- **somas-debugger**: Root cause investigation
- **somas-advisor**: Strategic planning and trade-off analysis

**Why o1?** Chain-of-thought reasoning reduces hallucinations and produces more thorough analysis in domains requiring "thinking before responding."

### Architecture & Implementation Agents (Claude 3.7 Sonnet)

Used for agents requiring structural consistency and high-quality code generation:

- **somas-architect**: System design and ADRs
- **somas-implementer**: Production code generation

**Why Claude 3.7 Sonnet?** Widely recognized as "The Architect" in 2026 benchmarks; superior at maintaining complex system context and producing idiomatic, maintainable code structures (SWE-bench SOTA).

### Documentation Agent (Gemini 2.0 Flash / 2.5 Pro)

Used for the documentation specialist:

- **somas-documenter**: Comprehensive documentation generation

**Why Gemini?** Extended context window (up to 2M tokens in Gemini 2.5 Pro) allows ingesting entire repository and SOMAS config simultaneously, ensuring documentation never drifts from code reality.

### Coordination Agents (GPT-4o)

Used for agents requiring speed, reliability, and low latency:

- **somas-tester**: High-volume test generation
- **somas-merger**: Merge conflict resolution
- **somas-orchestrator**: Pipeline state management

**Why GPT-4o?** Optimal speed/cost ratio for high-throughput, coordination-focused tasks where deep reasoning is not required.

## Using Custom Agents

### In Pull Requests

Tag agents in PR comments to request specific reviews:

```markdown
@copilot somas-architect please review the system design in ARCHITECTURE.md

@copilot somas-security perform a security analysis of the authentication implementation

@copilot somas-optimizer analyze the performance of the search algorithm
```

### In Code Comments

Use agent-specific tags in code comments:

```python
# @somas-reviewer: Please verify this error handling logic
# @somas-security: Check if this input validation is sufficient
# @somas-optimizer: Is this the most efficient approach?
```

### In Issues

Reference agents when creating tasks:

```markdown
## Task: Implement User Authentication

**Agents Required**:
- @copilot somas-requirements - Extract detailed requirements
- @copilot somas-architect - Design authentication system
- @copilot somas-implementer - Generate implementation
- @copilot somas-security - Security review
```

## Agent Capabilities by Stage

### Ideation Stage
- **somas-requirements**: Extract and analyze requirements from project ideas

### Specification Stage
- **somas-requirements**: Create comprehensive SPEC.md documents

### Simulation Stage
- **somas-optimizer**: Analyze task complexity and optimize execution plans

### Architecture Stage
- **somas-architect**: Design system architecture and create ADRs
- **somas-advisor**: Provide strategic guidance on tech choices

### Implementation Stage
- **somas-implementer**: Generate production-ready code
- **somas-orchestrator**: Coordinate implementation tasks

### Validation Stage
- **somas-tester**: Generate comprehensive test suites
- **somas-reviewer**: Perform code quality reviews
- **somas-security**: Conduct security analysis
- **somas-optimizer**: Identify performance bottlenecks
- **somas-orchestrator**: Validate quality gates

### Staging Stage
- **somas-documenter**: Generate comprehensive documentation
- **somas-orchestrator**: Coordinate deployment

### As-Needed
- **somas-debugger**: Investigate bugs and root causes
- **somas-merger**: Resolve merge conflicts
- **somas-advisor**: Strategic architectural decisions

## Model Availability Note

If specific models are not available in your GitHub Copilot subscription:

| Primary Model | Fallback Option | Adjustment Required |
|---------------|----------------|---------------------|
| o1 | GPT-4o | Add explicit "think step-by-step" prompts |
| Claude 3.7 Sonnet | GPT-4o or Claude 3.5 Sonnet | Increase code review iterations |
| Gemini 2.0 Flash | GPT-4o | Chunk documentation into smaller sections |

## Agent Performance Metrics

Each agent has been optimized for specific performance characteristics:

### Speed Priority (GPT-4o agents)
- **somas-tester**: Fast test generation for rapid iteration
- **somas-merger**: Quick conflict resolution
- **somas-orchestrator**: Low-latency state management

### Quality Priority (o1 agents)
- **somas-requirements**: Thorough requirements analysis
- **somas-reviewer**: Deep logic review
- **somas-security**: Comprehensive vulnerability analysis
- **somas-optimizer**: Detailed performance analysis
- **somas-debugger**: Systematic root cause investigation
- **somas-advisor**: Strategic decision analysis

### Context Priority (Gemini agent)
- **somas-documenter**: Whole-repository documentation awareness

### Architecture Priority (Claude agents)
- **somas-architect**: System-level design consistency
- **somas-implementer**: Idiomatic, maintainable code

## Best Practices

### 1. Choose the Right Agent
- Use specialist agents for their domain (don't ask somas-tester to design architecture)
- Leverage agent strengths (o1 for reasoning, GPT-4o for speed)
- Combine agents for comprehensive analysis (security + reviewer + optimizer)

### 2. Provide Context
- Give agents access to relevant files (SPEC.md, ARCHITECTURE.md)
- Reference requirements and constraints
- Explain the problem clearly

### 3. Iterate on Feedback
- Review agent outputs carefully
- Ask follow-up questions
- Request refinements when needed

### 4. Respect Agent Limitations
- o1 agents are slower but more thorough (worth the wait for critical analysis)
- GPT-4o agents are fast but may miss subtle issues (good for high-volume tasks)
- Gemini agent needs full codebase access (provide complete context)
- Claude agents excel at structure (leverage for architecture and code)

## Contributing

When adding new agents:

1. Create agent profile in `.github/agents/[agent-name].md`
2. Include YAML frontmatter with name, description, and model
3. Document agent's role, responsibilities, and capabilities
4. Add model-specific guidance section
5. Provide example inputs and outputs
6. Update this README with agent details
7. Add agent to MODEL_SELECTION.md with rationale

## Additional Resources

- [Model Selection Rationale](./MODEL_SELECTION.md) - Detailed explanation of model choices
- [SOMAS Pipeline Documentation](../../docs/somas/README.md) - Overall system architecture
- [Copilot Configuration](../copilot-config.yml) - Repository-wide Copilot settings
- [Copilot Instructions](../copilot-instructions.md) - General Copilot guidance

## Support

For questions or issues with custom agents:

1. Review agent profile documentation
2. Check [MODEL_SELECTION.md](./MODEL_SELECTION.md) for model-specific guidance
3. Open an issue with tag `custom-agents`
4. Reference specific agent and describe expected vs actual behavior

---

**Version**: 1.0.0 (2026-01-15)
**Last Updated**: 2026-01-19
