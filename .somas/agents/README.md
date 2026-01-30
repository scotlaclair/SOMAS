# SOMAS Agent Configurations

This directory contains the configuration files for all AI agents in the SOMAS (Self-Sovereign Orchestrated Multi-Agent System) autonomous development pipeline.

**Last Updated:** January 30, 2026 12:00 UTC
**Agent Count:** 17 active agents
**Format Version:** SOMAS Agent v1.0

## Overview

SOMAS employs a specialized workforce of 17 AI agents, each optimized for specific stages of the 11-stage Aether lifecycle. Each agent inherits from a common base configuration and is tailored for its domain expertise.

## Agent Architecture

### Inheritance System

All agents inherit from `_base.yml`, which provides:
- Default quality standards and collaboration protocols
- Output structure templates
- Communication formats
- Retry and timeout configurations

### Configuration Format

Each agent follows this structure:

```yaml
agent:
  name: "Agent Name"
  role: "Brief role description"
  provider: "ai_model_provider"
  inherits: "_base"

responsibilities:
  primary:
    - "Core responsibility 1"
    - "Core responsibility 2"
  secondary:
    - "Supporting responsibility 1"

instructions: |
  Detailed behavioral instructions for the agent...

# Agent-specific configuration
# (varies by agent type)
```

## Agent Index

For programmatic access and automated tracking, see `agents.json` - a machine-readable index of all agent configurations with metadata, categories, and relationships.

### Using the Agent Index

The `agents.json` file provides:
- **Complete agent inventory** with file paths and metadata
- **Category mappings** for logical grouping
- **Stage assignments** showing which agents work in each Aether lifecycle stage
- **Provider distribution** tracking AI model usage across agents
- **Status tracking** for active vs archived configurations
- **Last modified timestamps** for change tracking

**Example usage:**
```bash
# Get all agents for a specific stage
jq '.stages.implement' agents.json

# Find agents by provider
jq '.providers."claude_sonnet_4_5".agents' agents.json

# List agents by category
jq '.categories.implementation.agents' agents.json
```

## Key Agent Categories

### Governance & Strategy
- **orchestrator**: Pipeline coordination and state management
- **advisor**: Strategic guidance and alignment validation
- **planner**: High-level planning and requirements analysis

### Analysis & Design
- **specifier**: Requirements specification and PRD generation
- **architect**: System architecture and design
- **simulator**: Task optimization and feasibility analysis

### Implementation
- **decomposer**: Task breakdown into executable units
- **implementer**: Primary code generation agent
- **coder**: Alternative implementation agent

### Quality Assurance
- **tester**: Comprehensive testing suite creation
- **validator**: Code review and integration validation
- **reviewer**: Quality assurance and standards enforcement
- **security**: Security scanning and vulnerability assessment

### Operations
- **merger**: Merge conflict resolution and integration
- **deployer**: Deployment orchestration and release management
- **operator**: Runtime monitoring and health checks
- **analyzer**: Performance analysis and continuous improvement
- **documenter**: Technical documentation and knowledge capture

## Agent Communication

### Handoff Protocol

Agents communicate through structured handoffs following the base configuration's collaboration protocol:

1. **Context Passing**: Provide complete context for the next agent
2. **Artifact References**: Link to generated artifacts and documentation
3. **Assumption Documentation**: Clearly state assumptions and decisions
4. **Escalation Points**: Identify areas requiring human intervention

### Quality Gates

Each agent enforces quality standards defined in `_base.yml`:
- Code quality and style guidelines
- Documentation requirements
- Testing coverage minimums
- Security best practices

## Adding New Agents

### Process

1. **Identify Need**: Determine which stage/purpose requires the new agent
2. **Create Configuration**: Copy an existing agent as template
3. **Update Metadata**: Set name, role, provider, and responsibilities
4. **Define Instructions**: Write clear behavioral instructions
5. **Configure Specializations**: Add agent-specific configuration
6. **Test Integration**: Verify handoffs and quality gates
7. **Update Documentation**: Add to this README and workflow references

### Template

```yaml
# New Agent Configuration
agent:
  name: "NewAgent"
  role: "Specific purpose description"
  provider: "appropriate_ai_model"
  inherits: "_base"

responsibilities:
  primary:
    - "Primary responsibility"
  secondary:
    - "Supporting responsibilities"

instructions: |
  Detailed instructions for the agent's behavior...

# Agent-specific configuration here
```

## Configuration Validation

### Required Fields

- `agent.name`: Human-readable agent name
- `agent.role`: Brief role description
- `agent.provider`: AI model provider identifier
- `agent.inherits`: Must be `"_base"`
- `responsibilities.primary`: Array of core responsibilities
- `instructions`: Detailed behavioral guidance

### Optional Fields

- `responsibilities.secondary`: Supporting responsibilities
- `execution_mode`: Single-shot vs iterative execution
- `feedback_loop`: Configuration for spec-simulation feedback
- `validations`: Custom validation rules
- Agent-specific configuration blocks

## Troubleshooting

### Common Issues

1. **Provider Mismatch**: Ensure provider matches available models in `.somas/config.yml`
2. **Stage Misalignment**: Verify agent is assigned to appropriate Aether lifecycle stage
3. **Handoff Failures**: Check artifact paths and context passing
4. **Quality Gate Failures**: Review base configuration standards

### Debugging

- Check agent logs in `projects/{id}/logs/`
- Verify configuration syntax with YAML validator
- Test agent isolation before pipeline integration
- Review handoff artifacts for completeness

## Related Documentation

- `.somas/config.yml`: Main system configuration
- `.somas/stages/`: Stage definitions and workflows
- `.somas/templates/`: Artifact templates
- `docs/somas/`: Complete SOMAS documentation
- `docs/somas/architecture-diagrams.md`: System architecture overview

## Maintenance

- Keep agent configurations aligned with Aether lifecycle stages
- Update provider models based on performance benchmarking
- Review and update instructions based on operational feedback
- Maintain consistency across similar agent types
- Archive outdated configurations in `archived/` directory

### Updating Tracking Information

When modifying agent configurations:

1. **Update README.md** timestamp and agent count
2. **Update agents.json** with new metadata and timestamps
3. **Run validation** to ensure JSON schema compliance
4. **Test integrations** with pipeline workflows

**Automated tracking script example:**
```bash
#!/bin/bash
# Update agent index after changes
find . -name "*.yml" -not -path "./archived/*" | wc -l > agent_count.txt
date -u +"%Y-%m-%dT%H:%M:%SZ" > last_updated.txt
# Update agents.json programmatically
```</content>
<parameter name="filePath">/Users/architect/Developer/projects/somas/.somas/agents/README.md