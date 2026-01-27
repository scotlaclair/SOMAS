# CLAUDE.md - AI Assistant Guide for SOMAS

This document provides context for AI assistants working with the SOMAS (Self-Sovereign Orchestrated Multi-Agent System) codebase.

## Project Overview

SOMAS is an AI-first Software Development Life Cycle (SDLC) that orchestrates specialized AI agents to autonomously build production-ready software. It features an 11-stage neurology-inspired pipeline with 15+ specialized AI agents powered by 2026 Frontier Tier models.

**Key Concepts:**
- Fully autonomous development pipeline with minimal human intervention
- Comment-driven orchestration via GitHub Issues
- State persistence with automatic recovery from failures
- Circuit breaker safeguards prevent runaway automation
- Human engagement required ONLY for final merge approval

## Directory Structure

```
/home/user/SOMAS/
├── .github/
│   ├── workflows/          # 11 GitHub Actions workflows
│   ├── LABELS.md           # Label system documentation
│   └── labeler.yml         # PR auto-labeling rules
├── .somas/
│   ├── agents/             # 15 agent YAML configurations
│   ├── stages/             # 11 stage definitions
│   ├── config.yml          # Main system configuration (~1000 lines)
│   ├── apo/                # Autonomous Prompt Optimization configs
│   ├── architecture/       # Architecture Decision Records (ADRs)
│   ├── prompts/            # Agent prompt templates
│   ├── templates/          # State/schema templates
│   ├── knowledge/          # Approved libraries database
│   ├── patterns/           # Design patterns reference
│   ├── backlog.md          # Future work items
│   └── roadmap.md          # Strategic roadmap
├── somas/                   # Python source code
│   ├── core/
│   │   ├── state_manager.py     # State persistence (~1000 lines)
│   │   ├── circuit_breaker.py   # Safety mechanisms
│   │   ├── feedback_loop.py     # Spec-simulation feedback
│   │   └── runner.py            # Task execution coordinator
│   ├── agents/
│   │   └── cost_tracker.py      # API cost tracking
│   ├── analytics/
│   │   └── poc_metrics.py       # Metrics collection
│   └── apo/
│       └── task_complexity_analyzer.py
├── tests/                   # Test suite
│   ├── test_state_manager.py    # Comprehensive state tests
│   └── test_circuit_breaker.py  # Circuit breaker tests
├── docs/somas/              # Documentation
├── scripts/                 # Utility scripts
├── README.md               # Main project documentation
└── SECURITY.md             # Security policy
```

## Development Commands

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_state_manager.py -v

# Run with coverage
python -m pytest tests/ --cov=somas --cov-report=term-missing
```

### Dependencies
```bash
# Install dependencies
pip install -r requirements.txt

# Required packages: filelock, pyyaml
```

### Label Setup
```bash
# Create all GitHub labels for the SOMAS workflow
./scripts/setup-labels.sh
```

## Pipeline Stages (11-Stage Architecture)

| # | Code | Stage | Description | Agent |
|---|------|-------|-------------|-------|
| 1 | SIGNAL | Intake | Catch initial request | planner |
| 2 | DESIGN | Specify | Expand into requirements | specifier |
| 3 | GRID | Plan | Map components & strategy | simulator |
| 4 | LINE | Decompose | Break into atomic tasks | decomposer |
| 5 | MCP | Implement | Generate code | coder |
| 6 | PULSE | Verify | Run tests | validator |
| 7 | SYNAPSE | Integrate | Connect & merge | merger |
| 8 | OVERLOAD | Harden | Stress test & document | tester |
| 9 | VELOCITY | Release | Deploy at speed | deployer |
| 10 | VIBE | Operate | Monitor SLOs | operator |
| 11 | WHOLE | Learn | Analyze & loop back | analyzer |

## Code Conventions

### Python Style
- Python 3.11+ required
- Type hints used throughout
- Docstrings for public methods
- Security-first: validate all inputs

### File Naming
- Python modules: `snake_case.py`
- Test files: `test_*.py`
- YAML configs: `kebab-case.yml` or `snake_case.yml`

### Import Order
```python
# Standard library
import json
import os
from pathlib import Path

# Third-party
from filelock import FileLock
import yaml

# Local
from somas.core.state_manager import StateManager
```

### Error Handling
```python
# Use specific exceptions, not bare except
try:
    operation()
except FileNotFoundError:
    handle_missing_file()
except json.JSONDecodeError as e:
    handle_invalid_json(e)
```

## Security Guidelines

**CRITICAL - Always follow these patterns:**

### Input Validation
```python
import re
# Project IDs must match pattern: project-\d+
PROJECT_ID_PATTERN = re.compile(r'^project-\d+$')

def validate_project_id(project_id: str) -> bool:
    return bool(PROJECT_ID_PATTERN.match(project_id))
```

### Path Traversal Prevention
```python
# Always resolve and verify paths
def validate_path(path: Path, base_dir: Path) -> bool:
    resolved = path.resolve()
    # Check for symlinks
    if resolved != path.resolve(strict=False):
        return False
    # Check path is within base directory
    try:
        resolved.relative_to(base_dir.resolve())
        return True
    except ValueError:
        return False
```

### Safe JSON Operations
```python
# Use json module, never shell commands
import json
import os
import tempfile
# Read
with open(filepath, 'r') as f:
    data = json.load(f)
# Write atomically
with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
    json.dump(data, tmp, indent=2)
    tmp.flush()
    os.fsync(tmp.fileno())
os.replace(tmp.name, filepath)  # Atomic rename
```

### File Locking
```python
from filelock import FileLock

lock = FileLock(f"{filepath}.lock")
with lock:
    # Thread-safe file operations
    pass
```

## Key Files to Reference

| File | Purpose |
|------|---------|
| `.somas/config.yml` | Main configuration - stages, agents, optimization |
| `.somas/agents/*.yml` | Individual agent configurations |
| `.somas/stages/*.yml` | Stage definitions with quality gates |
| `somas/core/state_manager.py` | State persistence implementation |
| `somas/core/circuit_breaker.py` | Safety mechanism implementation |
| `.github/workflows/somas-pipeline.yml` | Main pipeline workflow |
| `.github/workflows/somas-orchestrator.yml` | Comment-driven orchestration |
| `.github/LABELS.md` | Complete label system documentation |

## Testing Patterns

### Unit Tests
```python
class TestFeature(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        # Setup test fixtures

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_specific_behavior(self):
        # Arrange
        input_data = {...}
        # Act
        result = function_under_test(input_data)
        # Assert
        self.assertEqual(result, expected)
```

### Security Tests
```python
def test_path_traversal_prevention(self):
    """Verify path traversal attacks are blocked."""
    malicious_paths = [
        "../../../etc/passwd",
        "project-123/../../../etc/passwd",
        "/absolute/path/attack",
    ]
    for path in malicious_paths:
        with self.assertRaises(ValueError):
            validate_path(path)
```

### Concurrent Access Tests
```python
def test_concurrent_writes(self):
    """Verify no data corruption under concurrent access."""
    threads = []
    for i in range(5):
        t = threading.Thread(target=write_operation, args=(i,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    # Verify data integrity
```

## GitHub Workflows

### Label-Driven Triggers
- `somas-project`: Triggers full pipeline
- `somas:dev`: Enables autonomous development mode
- `stage:*`: Tracks pipeline progress through stages

### Key Workflows
- **somas-pipeline.yml**: Main 11-stage orchestration
- **somas-orchestrator.yml**: Comment-driven agent invocation
- **somas-meta-capture.yml**: Captures PR review recommendations
- **pr-security.yml**: Security scanning (CodeQL, Semgrep)

## Circuit Breaker Limits

| Limit | Value | Purpose |
|-------|-------|---------|
| Max agent invocations per issue | 20 | Prevent infinite loops |
| Max comments per hour | 10 | Rate limiting |
| Max retries before escalation | 3 | Failure recovery |
| Max feedback loop iterations | 3 | Spec-simulation cycles |
| Max checkpoints | 20 | State file rotation |

## Common Tasks

### Adding a New Agent
1. Create agent config in `.somas/agents/new_agent.yml`
2. Define role, responsibilities, and output format
3. Add to appropriate stage in `.somas/config.yml`
4. Update tests if agent has Python implementation

### Adding a New Stage
1. Create stage definition in `.somas/stages/new_stage.yml`
2. Add to pipeline in `.somas/config.yml`
3. Create corresponding label: `stage:new-stage`
4. Update workflow in `.github/workflows/somas-pipeline.yml`

### Modifying State Manager
1. Read `somas/core/state_manager.py` thoroughly
2. Maintain file locking patterns
3. Preserve atomic write operations
4. Add tests in `tests/test_state_manager.py`
5. Test concurrent access scenarios

### Creating ADRs
1. Follow template in `.somas/architecture/ADRs/README.md`
2. Use format: `ADR-NNN-title.md`
3. Document context, decision, and consequences

## Important Notes

1. **Never commit secrets** - Use GitHub Secrets for credentials
2. **Validate all inputs** - Project IDs, paths, user content
3. **Use atomic operations** - File writes use temp file + rename
4. **Test concurrent access** - State manager is used by parallel workflows
5. **Check circuit breakers** - Respect invocation limits
6. **Forward-only stages** - Pipeline cannot go backward

## Agent Model Assignments

| Agent | Model | Use Case |
|-------|-------|----------|
| planner | GPT-5.2 | Requirements analysis |
| specifier | Claude Sonnet 4.5 | Specification generation |
| simulator | Claude Sonnet 4.5 | Monte Carlo optimization |
| architect | Claude Opus 4.5 | System design |
| coder | Claude Sonnet 4.5 | Code generation |
| validator | Claude Sonnet 4.5 | Testing & validation |
| deployer | Claude Opus 4.5 | Deployment preparation |
| security | GPT-5.2 | Vulnerability scanning |
| documenter | Gemini 3 Pro | Documentation |
| orchestrator | Grok Code Fast 1 | Low-latency coordination |

## Quick Reference

```bash
# View project state
cat .somas/projects/PROJECT_ID/state.json

# Check dead letters (failed executions)
cat .somas/projects/PROJECT_ID/dead_letters.json

# View state transitions
cat .somas/projects/PROJECT_ID/transitions.jsonl

# Run security scan
gh workflow run pr-security.yml

# Check workflow status
gh run list --workflow=somas-pipeline.yml
```

## Getting Help

- **Documentation**: `docs/somas/README.md`
- **Troubleshooting**: `docs/somas/TROUBLESHOOTING.md`
- **Security Policy**: `SECURITY.md`
- **Label System**: `.github/LABELS.md`
