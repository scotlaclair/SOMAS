# GitHub Copilot Instructions for SOMAS

## Project Overview
SOMAS (Self-Sovereign Orchestrated Multi-Agent System) is an AI-first Software Development Life Cycle (SDLC) that transforms project ideas into production-ready software through orchestrated AI agents.

## AI Agent Ecosystem
This project uses multiple AI agents for different stages:
- **Codex (GPT-4)**: Specification, simulation, architecture, deployment
- **Gemini Pro**: Validation and testing
- **GitHub Copilot**: Implementation and code generation

## Code Generation Guidelines

### Architecture Patterns
When generating code for SOMAS:
1. **Configuration-Driven**: All behavior is driven by `.somas/config.yml`
2. **Agent-Based**: Each pipeline stage has a dedicated agent (see `.somas/agents/`)
3. **Template-Based**: Use templates from `.somas/templates/` for consistency
4. **Workflow-Driven**: GitHub Actions orchestrate the pipeline (see `.github/workflows/`)

### Naming Conventions
- Agent files: `{agent_name}.yml` in `.somas/agents/`
- Stage files: `{stage_name}.yml` in `.somas/stages/`
- Project directories: `projects/{project_id}/`
- Artifact files: Follow templates in `.somas/templates/`

### Security Requirements
@copilot CRITICAL: Always implement these security measures:
- Input validation for all project IDs (prevent path traversal)
- Use Python for JSON encoding (prevent shell injection)
- Never hardcode secrets or tokens
- Validate file paths before operations
- Use parameterized queries for any database operations

### AI Agent Delegation
@copilot When implementing features that involve AI agents:
1. Check `.somas/config.yml` for agent provider configuration
2. Use the appropriate agent based on the stage (see `agents.agent_configs`)
3. Follow the prompt structure in `.somas/agents/{agent}.yml`
4. Respect quality gates defined in `quality_gates` section

### Testing Expectations
@copilot When generating test code:
- Unit tests should validate configuration parsing
- Integration tests should verify agent orchestration
- Security tests should check input validation
- Performance tests should verify simulation accuracy

### Pipeline Stage Implementation
@copilot For each pipeline stage:
1. Read stage config from `.somas/stages/{stage}.yml`
2. Load agent config from `.somas/agents/{agent}.yml`
3. Generate artifacts using templates from `.somas/templates/`
4. Store outputs in `projects/{project_id}/artifacts/`
5. Update project metadata in `projects/{project_id}/metadata.json`

## AI-Specific Tags for Review

### @copilot-review
Use this tag in code comments to request Copilot review of critical sections:
```yaml
# @copilot-review: Verify this configuration matches security requirements
security:
  secrets_management:
    provider: "github_secrets"
```

### @copilot-delegate
Use this tag to indicate when work should be delegated to other AI agents:
```yaml
# @copilot-delegate: Use specifier agent for requirement generation
# See .somas/agents/specifier.yml for prompt structure
```

### @copilot-context
Use this tag to provide important context for code generation:
```python
# @copilot-context: This function processes Monte Carlo simulation results
# Input format matches .somas/templates/execution_plan.yml
def process_simulation_results(results):
    pass
```

## Integration Points

### GitHub Actions Workflows
@copilot When modifying workflows in `.github/workflows/`:
- Use safe command execution (avoid eval, use proper quoting)
- Reference secrets via `${{ secrets.NAME }}`
- Use Python for JSON operations (not jq or bash)
- Include proper error handling and status checks

### Agent Configuration
@copilot When creating or modifying agent configs:
- Follow the structure in existing files like `.somas/agents/specifier.yml`
- Include `role`, `instructions`, and `output_format` sections
- Define quality checks with patterns to detect/reject
- Specify output file paths clearly

### Template Creation
@copilot When creating templates:
- Use placeholders like `[PROJECT-ID]`, `[DATE]`, `[USERNAME]`
- Include clear instructions and examples
- Ensure all sections are well-documented
- Follow markdown best practices for readability

## Multi-Agent Collaboration

### Delegation Strategy
@copilot Follow this strategy for AI agent delegation:

1. **Specification Stage** → Delegate to Codex (specifier agent)
   - Input: Project idea, initial plan
   - Output: Complete SPEC.md with requirements

2. **Simulation Stage** → Delegate to Codex (simulator agent)
   - Input: SPEC.md
   - Output: execution_plan.yml with optimized task sequence

3. **Implementation Stage** → Use GitHub Copilot (coder agent)
   - Input: Architecture design, execution plan
   - Output: Source code, tests, documentation

4. **Validation Stage** → Delegate to Gemini (validator agent)
   - Input: Implementation artifacts
   - Output: Test results, quality metrics

### Inter-Agent Communication
@copilot Agents communicate through artifacts:
- Stage N outputs artifacts to `projects/{id}/artifacts/`
- Stage N+1 reads artifacts as inputs
- Metadata tracks completion status in `projects/{id}/metadata.json`

## Code Review Instructions

### For Pull Requests
@copilot When reviewing PRs:
1. Check if changes follow configuration structure
2. Verify security measures are implemented
3. Ensure templates are used correctly
4. Validate workflow modifications don't break pipeline
5. Check that agent configurations are properly formatted

### Quality Checklist
@copilot Use this checklist for code quality:
- [ ] Configuration follows YAML best practices
- [ ] Agent prompts are clear and unambiguous
- [ ] Security validation is present
- [ ] Error handling is comprehensive
- [ ] Artifacts follow template structure
- [ ] Documentation is updated
- [ ] Tests cover new functionality

## Common Patterns

### Safe Project ID Handling
```python
# @copilot-example: Always validate project IDs
import re

def validate_project_id(project_id):
    # Prevent path traversal attacks
    if not re.match(r'^project-\d+$', project_id):
        raise ValueError("Invalid project ID format")
    return project_id
```

### Safe JSON Encoding
```python
# @copilot-example: Use Python for JSON encoding
import json

metadata = {
    'project_id': project_id,
    'title': title,  # Safe from shell injection
    'created_at': datetime.utcnow().isoformat()
}

with open(f'path/to/{project_id}/metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)
```

### Agent Invocation Pattern
```bash
# @copilot-example: Safe agent invocation in workflows
PROJECT_ID="${{ inputs.project_id }}"

# Validate input
if [[ ! "$PROJECT_ID" =~ ^project-[0-9]+$ ]]; then
  echo "Invalid project ID"
  exit 1
fi

# Process with Python
python3 << 'PYTHON_SCRIPT'
import os
import json

project_id = os.environ['PROJECT_ID']
# Safe to use project_id here
PYTHON_SCRIPT
```

## Resources

- **Configuration Reference**: `.somas/config.yml`
- **Agent Definitions**: `.somas/agents/*.yml`
- **Stage Definitions**: `.somas/stages/*.yml`
- **Templates**: `.somas/templates/*.md`
- **Documentation**: `docs/somas/README.md`
- **Workflows**: `.github/workflows/*.yml`

## Getting Help

@copilot For questions about:
- **Architecture**: See `docs/somas/README.md`
- **Configuration**: See `.somas/config.yml` with inline comments
- **Security**: See security section in config and workflow implementations
- **Optimization**: See `docs/somas/optimization-guide.md`
- **Troubleshooting**: See `docs/somas/TROUBLESHOOTING.md`

---

@copilot Remember: This is a multi-agent system. Your role as Copilot is primarily implementation (code generation). Delegate specification, simulation, and validation to the appropriate specialized agents.
