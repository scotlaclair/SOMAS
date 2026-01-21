# GitHub Copilot Integration Guide

## Overview

This guide explains how to use GitHub Copilot effectively with the SOMAS (Self-Sovereign Orchestrated Multi-Agent System) project. SOMAS leverages multiple AI agents including GitHub Copilot for code implementation.

## Table of Contents

1. [Understanding SOMAS Multi-Agent Architecture](#understanding-somas-multi-agent-architecture)
2. [Copilot's Role in the Pipeline](#copilots-role-in-the-pipeline)
3. [Using Copilot Instructions](#using-copilot-instructions)
4. [AI Agent Delegation](#ai-agent-delegation)
5. [Best Practices](#best-practices)
6. [Code Examples](#code-examples)
7. [Troubleshooting](#troubleshooting)

---

## Understanding SOMAS Multi-Agent Architecture

SOMAS uses a multi-agent approach where different AI systems handle different stages of development:

| Agent | Provider | Stage | Responsibility |
|-------|----------|-------|----------------|
| Planner | GPT-5.2 | Ideation | High-level planning |
| Specifier | Claude Sonnet 4.5 | Specification | Requirements documentation |
| Simulator | Claude Sonnet 4.5 | Simulation | Task optimization |
| Architect | Claude Opus 4.5 | Architecture | System design |
| **Implementer** | **Claude Sonnet 4.5** | **Implementation** | **Code generation** |
| Tester | Claude Sonnet 4.5 | Testing | Test suite creation |
| Reviewer | Claude Sonnet 4.5 | Review | Code quality assessment |
| Security | GPT-5.2 | Security | Vulnerability scanning |
| Documenter | Gemini 3 Pro | Documentation | Technical writing |
| Orchestrator | Grok Code Fast 1 | Coordination | Pipeline management |

### Why Multiple Agents?

Each agent is specialized for its domain:
- **Claude Sonnet 4.5** is the #1 SWE-bench coding model, optimized for implementation and testing
- **Claude Opus 4.5** provides the deepest reasoning for architecture and system design
- **GPT-5.2** excels at general intelligence tasks like requirements and security analysis
- **Gemini 3 Pro** has massive context windows for comprehensive documentation
- **Grok Code Fast 1** provides lowest latency for orchestration and routing

---

## Copilot's Role in the Pipeline

### Primary Responsibilities

As the **Implementation Agent**, Copilot handles:

1. **Code Generation**
   - Implementing functionality based on specifications
   - Following architectural designs
   - Creating clean, maintainable code

2. **Test Creation**
   - Writing unit tests for all functions
   - Creating integration tests
   - Ensuring >80% code coverage

3. **Documentation**
   - Inline code comments
   - API documentation
   - Module README files

4. **Refactoring**
   - Improving code quality
   - Optimizing performance
   - Maintaining consistency

### What Copilot Does NOT Do

- **Specification Writing**: Delegate to Specifier agent
- **Architecture Design**: Delegate to Architect agent
- **Task Optimization**: Delegate to Simulator agent
- **Final Validation**: Delegate to Validator agent

---

## Using Copilot Instructions

### Repository-Level Instructions

SOMAS provides repository-level instructions at:
```
.github/copilot-instructions.md
```

These instructions are automatically available to Copilot when working in this repository.

### Meta-Comments for Copilot

Use special comment tags to guide Copilot:

#### @copilot-review
Request Copilot to review specific code sections:

```python
# @copilot-review: Verify input validation is comprehensive
def process_user_input(data):
    if not validate_input(data):
        raise ValueError("Invalid input")
    return sanitize(data)
```

#### @copilot-context
Provide important context for code generation:

```python
# @copilot-context: This function processes Monte Carlo simulation results
# Expected input format matches .somas/templates/execution_plan.yml
# Output should update project metadata with completion statistics
def process_simulation_results(results):
    # Copilot will generate code with this context in mind
    pass
```

#### @copilot-delegate
Indicate when to delegate to other agents:

```yaml
# @copilot-delegate: Use specifier agent for requirement generation
# Agent config: .somas/agents/specifier.yml
# This is not a code generation task
specification:
  agent: "specifier"
  provider: "codex"
```

#### @copilot-security
Highlight security-critical code:

```python
# @copilot-security: CRITICAL - This validates project IDs to prevent path traversal
def validate_project_id(project_id):
    import re
    if not re.match(r'^project-\d+$', project_id):
        raise ValueError("Invalid project ID format")
    return project_id
```

---

## AI Agent Delegation

### When to Delegate

Delegate to other agents when you encounter:

1. **Ambiguous Requirements** → Delegate to **Specifier**
   - Unclear specifications
   - Missing acceptance criteria
   - Undefined behavior for edge cases

2. **Design Issues** → Delegate to **Architect**
   - Scalability concerns
   - Integration challenges
   - Performance bottlenecks

3. **Complex Algorithms** → Delegate to **Simulator**
   - Optimization problems
   - Task scheduling
   - Resource allocation

4. **Validation Needed** → Delegate to **Validator**
   - Independent code review
   - Testing strategy
   - Quality assurance

### Delegation Process

1. **Create Delegation Request**

Use the template at `.somas/templates/ai_delegation.md`:

```json
{
  "delegation_id": "delegation-001",
  "from_agent": "copilot",
  "to_agent": "specifier",
  "reason": "Ambiguous requirement in REQ-F-042",
  "context": {
    "artifact": "SPEC.md",
    "section": "REQ-F-042",
    "issue": "Error handling not sufficiently detailed"
  },
  "questions": [
    "What HTTP status codes for validation errors?",
    "Should all errors be logged?",
    "How to handle async operation errors?"
  ],
  "blocking_task": "task-042"
}
```

2. **Save Request**

Save to: `projects/{project-id}/delegation_requests.json`

3. **Target Agent Processes**

The target agent will:
- Review the context
- Answer questions
- Update relevant artifacts
- Save response to `projects/{project-id}/delegation_responses.json`

4. **Resume Implementation**

Once clarification received, continue implementation with updated understanding.

### Delegation Examples

#### Example 1: Requirement Clarification

```python
# Need clarification before implementing error handling
# @copilot-delegate: specifier - REQ-F-042 error handling unclear

# Create delegation request
delegation = {
    "to_agent": "specifier",
    "issue": "REQ-F-042 doesn't specify HTTP status codes",
    "questions": [
        "Which status codes for different error types?",
        "Should errors be logged? At what level?"
    ]
}

# Wait for clarification before implementing
# TODO: Implement error handling after clarification
```

#### Example 2: Architecture Concern

```python
# @copilot-delegate: architect - Scalability issue in current design

# Current design is single-threaded but requirement needs 1000 req/sec
# Request architecture review for parallel processing approach

delegation = {
    "to_agent": "architect",
    "component": "DataProcessor",
    "issue": "Single-threaded design won't meet performance requirements",
    "constraint": "Must maintain API compatibility"
}

# Wait for revised architecture before implementing
```

---

## Best Practices

### 1. Read Before Writing

Before generating code:
```bash
# Always review these files first:
projects/{id}/artifacts/SPEC.md         # Requirements
projects/{id}/artifacts/ARCHITECTURE.md # Design
projects/{id}/artifacts/execution_plan.yml # Task sequence
```

### 2. Follow the Execution Plan

The Simulator agent has optimized the task sequence. Follow it:

```yaml
# execution_plan.yml shows optimal order
critical_path:
  - task-001: "Database schema"     # Do this first
  - task-005: "API endpoints"       # Then this
  - task-012: "Frontend components" # Then this
```

### 3. Implement Security First

Always include security measures:

```python
# ✅ GOOD: Validate and sanitize
def create_user(username, email):
    # @copilot-security: Input validation
    username = validate_username(username)
    email = validate_email(email)
    
    # Use parameterized query
    query = "INSERT INTO users (username, email) VALUES (%s, %s)"
    db.execute(query, (username, email))

# ❌ BAD: No validation, SQL injection risk
def create_user(username, email):
    query = f"INSERT INTO users VALUES ('{username}', '{email}')"
    db.execute(query)
```

### 4. Write Tests Alongside Code

Use TDD approach:

```python
# Test first
def test_user_creation():
    user = create_user("john", "john@example.com")
    assert user.username == "john"
    assert user.email == "john@example.com"

# Then implementation
def create_user(username, email):
    # Implementation here
    pass
```

### 5. Use Configuration

Don't hardcode values:

```python
# ✅ GOOD: Use configuration
from config import settings

def connect_database():
    return Database(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER
    )

# ❌ BAD: Hardcoded values
def connect_database():
    return Database(
        host="localhost",
        port=5432,
        user="admin"
    )
```

### 6. Document as You Go

Add meaningful comments:

```python
# @copilot-context: Processes Monte Carlo simulation results
# Input: Dictionary with simulation statistics from simulator agent
# Output: Updated execution plan with optimized task sequence
def optimize_task_sequence(simulation_results):
    """
    Optimizes task execution order based on Monte Carlo simulation.
    
    Args:
        simulation_results: Dict containing:
            - mean_duration: Average completion time
            - critical_path: List of critical tasks
            - parallel_groups: Tasks that can run in parallel
    
    Returns:
        Optimized execution plan with updated task sequence
    """
    pass
```

---

## Code Examples

### Example 1: Safe Project ID Handling

```python
# @copilot-security: Prevents path traversal attacks
import re
import os

def get_project_path(project_id):
    """
    Safely constructs project path with validation.
    
    @copilot-context: Project IDs must match pattern 'project-\\\\d+'
    """
    # Validate format
    if not re.match(r'^project-\d+$', project_id):
        raise ValueError(f"Invalid project ID: {project_id}")
    
    # Construct safe path
    base_path = os.path.abspath(".somas/projects")
    project_path = os.path.join(base_path, project_id)
    
    # Verify path is within base directory
    if not project_path.startswith(base_path):
        raise ValueError("Path traversal attempt detected")
    
    return project_path
```

### Example 2: Reading Agent Configuration

```python
# @copilot-context: Agent configs are in .somas/agents/*.yml
import yaml

def load_agent_config(agent_name):
    """
    Loads configuration for specified agent.
    
    @copilot-review: Ensure proper error handling for missing files
    """
    config_path = f".somas/agents/{agent_name}.yml"
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        raise ValueError(f"Agent config not found: {agent_name}")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in {config_path}: {e}")
```

### Example 3: Processing Specification

```python
# @copilot-context: SPEC.md follows template from .somas/templates/SPEC.md
import re

def extract_requirements(spec_content):
    """
    Extracts requirements from specification document.
    
    @copilot-review: Verify regex patterns match template format
    """
    # Pattern matches: ### REQ-F-001: Title
    pattern = r'### (REQ-[FN]+-\\d+):\\s*(.+?)$'
    
    requirements = []
    for match in re.finditer(pattern, spec_content, re.MULTILINE):
        req_id = match.group(1)
        title = match.group(2)
        requirements.append({
            'id': req_id,
            'title': title,
            'type': 'functional' if 'REQ-F' in req_id else 'non-functional'
        })
    
    return requirements
```

### Example 4: Creating Delegation Request

```python
# @copilot-delegate: Template at .somas/templates/ai_delegation.md
import json
from datetime import datetime

def create_delegation_request(project_id, to_agent, reason, context, questions):
    """
    Creates a delegation request to another AI agent.
    
    @copilot-context: Facilitates inter-agent communication in SOMAS
    """
    delegation = {
        "delegation_id": f"delegation-{datetime.now().timestamp()}",
        "from_agent": "copilot",
        "to_agent": to_agent,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "requested",
        "reason": reason,
        "context": context,
        "questions": questions,
        "urgency": "high" if context.get("blocking") else "medium"
    }
    
    # Save to delegation requests file
    request_path = f"projects/{project_id}/delegation_requests.json"
    
    # Load existing requests
    try:
        with open(request_path, 'r') as f:
            requests = json.load(f)
    except FileNotFoundError:
        requests = []
    
    # Add new request
    requests.append(delegation)
    
    # Save updated requests
    with open(request_path, 'w') as f:
        json.dump(requests, f, indent=2)
    
    return delegation["delegation_id"]
```

---

## Troubleshooting

### Issue: Copilot Suggestions Don't Match Project Style

**Solution:** Ensure `.github/copilot-instructions.md` is present and review the file to verify it contains project-specific guidance.

### Issue: Unclear What to Implement Next

**Solution:** Check the execution plan:
```bash
cat projects/{project-id}/artifacts/execution_plan.yml
```

Look for tasks in the current phase that haven't been implemented.

### Issue: Requirement Ambiguous

**Solution:** Create a delegation request to the Specifier agent:
```python
create_delegation_request(
    project_id="project-123",
    to_agent="specifier",
    reason="Ambiguous requirement needs clarification",
    context={"requirement": "REQ-F-042"},
    questions=["What HTTP status codes to use?"]
)
```

### Issue: Architecture Doesn't Support Requirement

**Solution:** Delegate to Architect agent for design revision before continuing implementation.

### Issue: Test Failures

**Solution:**
1. Review specification to confirm expected behavior
2. Check if requirement was misunderstood
3. Verify test assertions match acceptance criteria
4. If requirement is wrong, delegate back to Specifier

---

## Resources

### Configuration Files
- **Main Config**: `.somas/config.yml`
- **Copilot Agent**: `.somas/agents/copilot.yml`
- **Copilot Instructions**: `.github/copilot-instructions.md`

### Templates
- **Delegation Template**: `.somas/templates/ai_delegation.md`
- **Specification Template**: `.somas/templates/SPEC.md`

### Documentation
- **System Overview**: `docs/somas/README.md`
- **Optimization Guide**: `docs/somas/optimization-guide.md`
- **Troubleshooting**: `docs/somas/TROUBLESHOOTING.md`

### Workflows
- **Main Pipeline**: `.github/workflows/somas-pipeline.yml`
- **Project Sync**: `.github/workflows/somas-project-sync.yml`

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│  COPILOT QUICK REFERENCE                            │
├─────────────────────────────────────────────────────┤
│  Role: Code Implementation (Stage 5)                │
│                                                      │
│  Read First:                                         │
│    □ projects/{id}/artifacts/SPEC.md                │
│    □ projects/{id}/artifacts/ARCHITECTURE.md        │
│    □ projects/{id}/artifacts/execution_plan.yml     │
│                                                      │
│  Security Checklist:                                 │
│    □ Input validation                               │
│    □ Output sanitization                            │
│    □ No hardcoded secrets                           │
│    □ Parameterized queries                          │
│                                                      │
│  Quality Gates:                                      │
│    □ Tests written                                   │
│    □ Coverage >80%                                   │
│    □ Documentation complete                         │
│    □ Linting passes                                  │
│                                                      │
│  Delegate When:                                      │
│    • Requirement unclear → specifier                │
│    • Design inadequate → architect                  │
│    • Algorithm complex → simulator                  │
│    • Need validation → validator                    │
│                                                      │
│  Meta-Comment Tags:                                  │
│    @copilot-review   - Request review               │
│    @copilot-context  - Provide context              │
│    @copilot-delegate - Indicate delegation          │
│    @copilot-security - Security-critical code       │
└─────────────────────────────────────────────────────┘
```

---

**Remember**: You're part of a team of specialized AI agents. Use delegation to leverage the expertise of other agents when needed. Your strength is code generation—use it well!
