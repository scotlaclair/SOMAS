# SOMAS: Self-Sovereign Orchestrated Multi-Agent System

**Aether-Powered Autonomous Software Development**

SOMAS is a "Process-as-Code" software development lifecycle (SDLC) engine. Unlike traditional CI/CD which automates deployment, SOMAS automates development.

It utilizes **20 Specialized Autonomous Agents** governed by the **11-State Aether Lifecycle** to transform raw intent (issues) into production-ready code.

---

## Architecture: The Aether Lifecycle

SOMAS does not run linearly. It operates as a **deterministic state machine**. Each state acts as a Gate that must be satisfied by specific agents before the artifact promotes to the next stage.

### The 11-State Machine

| State | Phase | Responsible Agents | Function |
|-------|-------|-------------------|----------|
| 01 | **INTAKE** | Triage, Advisor | Ingests issues, determines feasibility, and routes request type. |
| 02 | **SPECIFY** | Specifier, Requirements | Converts vague intent into strict functional specifications (PRD). |
| 03 | **PLAN** | Planner, Architect | Architect designs system structure; Planner builds the task graph. |
| 04 | **DECOMPOSE** | Decomposer | Breaks architecture into atomic implementation tasks (≤ 4hrs). |
| 05 | **IMPLEMENT** | Implementer, Copilot | Generates actual code, tests, and config based on decomposed tasks. |
| 06 | **VERIFY** | Tester, Debugger | Runs test suites. Debugger autonomously attempts fixes (Self-Healing). |
| 07 | **INTEGRATE** | Merger, Validator | Resolves merge conflicts and validates integration contracts. |
| 08 | **HARDEN** | Security | Performs SAST/DAST scanning and dependency audits. |
| 09 | **RELEASE** | Deployer | Packages artifacts, generates changelogs, and manages releases. |
| 10 | **OPERATE** | Operator | Performs post-deployment health checks and monitoring setup. |
| 11 | **ANALYZE** | Analyzer, Documenter | Reviews metrics for optimization loops and updates documentation. |

---

## The Agents (Workforce)

SOMAS employs a workforce of specialized agents, each with a narrow "Single Responsibility" scope.

### Governance & Strategy

| Agent | Role |
|-------|------|
| **Orchestrator** | The runtime engine. Manages state transitions and context passing. |
| **Advisor** | Provides strategic guidance and feasibility analysis. |
| **Architect** | Defines high-level system design, patterns, and file structures. |
| **Planner** | Creates execution schedules and dependency graphs. |
| **Security** | Enforces security policies and vulnerability scanning. |

### Execution & Engineering

| Agent | Role |
|-------|------|
| **Implementer** | The primary coder. Writes file content based on specs. |
| **Copilot** | Assists Implementer with snippets, refactoring, and completions. |
| **Decomposer** | Breaks complex requirements into atomic coding tasks. |
| **Debugger** | Analyzes stack traces and iteratively patches code. |
| **Merger** | Handles git operations, branching, and conflict resolution. |

### Quality & Verification

| Agent | Role |
|-------|------|
| **Tester** | Executes unit and integration test runners. |
| **Validator** | Verifies system state against the original Requirements. |
| **Reviewer** | Performs static analysis and code style reviews (human-proxy). |
| **Specifier** | Writes detailed technical specifications. |
| **Requirements** | Extracts and manages functional requirements. |

### Operations & Maintenance

| Agent | Role |
|-------|------|
| **Triage** | First responder to new issues/requests. |
| **Deployer** | Manages build artifacts and publication. |
| **Operator** | Ensures system stability after deployment. |
| **Analyzer** | Computes metrics and identifies process bottlenecks. |
| **Documenter** | Maintains knowledge base and updates READMEs. |

---

## Getting Started

### Prerequisites

- Python 3.9+
- Git
- OpenAI API Key (or compatible LLM provider)

### Installation

```bash
# Clone the repository
git clone https://github.com/scotlaclair/somas.git
cd somas

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Copy `.env.example` to `.env`
2. Add your API keys:

```env
OPENAI_API_KEY=sk-...
GITHUB_TOKEN=ghp-...
```

### Running the Pipeline

You can trigger the autonomous pipeline manually or via GitHub Issues.

**CLI Mode:**

```bash
# Run the autonomous pipeline for a specific issue
python -m somas.core.runner --issue_number 123
```

**GitHub Mode:**

Simply apply the label `somas:change` to any Issue. The GitHub Action will trigger the Intake stage automatically.

---

## Governance & Security

SOMAS is designed to be **Self-Sovereign**. It operates on its own dev branch and creates Pull Requests.

- **No Direct Push**: Agents cannot push directly to main.
- **Human-in-the-Loop**: Critical gates (like Release) require human approval on the PR.
- **Sandboxing**: All agent code execution is sandboxed (Docker support coming soon).

---

## Documentation

- [Alignment Strategy](docs/somas/alignment.md)
- [Agent Definitions](.somas/agents/)
- [Stage Configuration](.somas/stages/)

---

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
