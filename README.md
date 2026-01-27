# SOMAS

**Self-Sovereign Orchestrated Multi-Agent System**

An autonomous AI development pipeline that transforms project ideas into production-ready software through orchestrated AI agents powered by 2026 Frontier Tier models.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![SOMAS Version](https://img.shields.io/badge/SOMAS-v1.0.0-green.svg)](.somas/config.yml)

---

## 🚀 What is SOMAS?

SOMAS is an AI-first Software Development Life Cycle (SDLC) that orchestrates specialized AI agents to autonomously build production-ready software. Simply describe your project in a GitHub issue, and SOMAS handles the entire development lifecycle with minimal human intervention.

### Key Features

- 🤖 **Fully Autonomous**: AI agents handle the complete development lifecycle
- 🎯 **12 Specialized Agents**: Each with domain expertise and optimal AI models
- 🔄 **Self-Healing**: Automatic retry and debugging for failures
- ✅ **Quality Assurance**: 80%+ test coverage, security scanning, code review
- 📊 **Simulation-Based Optimization**: Monte Carlo analysis for optimal task sequencing
- 📝 **Complete Documentation**: Auto-generated specs, architecture docs, and API references
- 🔒 **Security First**: Automated vulnerability scanning and secure coding practices
- 🌐 **2026 Frontier Models**: GPT-5.2-Codex, Claude Opus 4.5, Gemini 3 Pro, and more

---

## 🏗️ Architecture

SOMAS operates through a **7-stage autonomous pipeline**:

```
┌──────────┐   ┌──────────────┐   ┌────────────┐   ┌──────────────┐
│ Ideation │ → │Specification │ → │ Simulation │ → │ Architecture │
│(Planner) │   │ (Specifier)  │   │(Simulator) │   │ (Architect)  │
└──────────┘   └──────────────┘   └────────────┘   └──────────────┘
                                                            ↓
┌──────────┐   ┌────────────┐   ┌────────────────────────┐
│ Staging  │ ← │ Validation │ ← │   Implementation       │
│(Merger)  │   │ (Tester+   │   │ (Implementer+Tester+   │
│          │   │  Reviewer+ │   │  Security+Optimizer)   │
│          │   │  Security) │   │                        │
└──────────┘   └────────────┘   └────────────────────────┘
```

### 12 Specialized AI Agents

SOMAS leverages the best 2026 Frontier Tier models for each task:

| Agent | Model | Role |
|-------|-------|------|
| **Orchestrator** | Grok Code Fast 1 | Pipeline coordination and state management |
| **Planner** | GPT-5.2 | Requirements analysis and roadmap creation |
| **Specifier** | GPT-5.2 | Complete specification generation |
| **Simulator** | GPT-5.2 | Monte Carlo simulation for task optimization |
| **Architect** | Claude Opus 4.5 | System architecture and design |
| **Implementer** | GPT-5.2-Codex | Production-ready code generation |
| **Tester** | Claude Sonnet 4.5 | Comprehensive test suites (80%+ coverage) |
| **Reviewer** | Claude Sonnet 4.5 | Code quality and architecture reviews |
| **Security** | GPT-5.2 | Security vulnerability scanning |
| **Optimizer** | Claude Sonnet 4.5 | Performance optimization |
| **Debugger** | Claude Haiku 4.5 | Bug investigation and fixes |
| **Documenter** | Gemini 3 Pro | Documentation and API references |
| **Merger** | Claude Opus 4.5 | Merge preparation and conflict resolution |

---

## 🎯 Quick Start

### 1. Create a Project Request

1. Go to [Issues](../../issues/new/choose)
2. Select "🤖 SOMAS Project Request" template
3. Describe your project idea and requirements
4. Submit the issue

### 2. Start the Pipeline

Add the `somas-project` label to your issue. SOMAS will automatically:
- Create a feature branch
- Initialize the 7-stage pipeline
- Begin autonomous development

### 3. Monitor Progress

Watch the pipeline progress through stages:
- 🎯 **Ideation** - Requirements analysis and planning
- 📋 **Specification** - Complete specification document
- 🔬 **Simulation** - Monte Carlo optimization of task sequence
- 🏗️ **Architecture** - System design and component definition
- ⚙️ **Implementation** - Code generation with tests
- ✅ **Validation** - Quality assurance and security review (auto-retry on failure)
- 📝 **Staging** - PR creation and merge preparation

### 4. Review and Approve

When staging completes:
- You'll be notified (@scotlaclair) for final review
- Review the generated code in the PR
- Approve and merge when ready

**Human engagement required ONLY for:**
- Final merge approval
- Failures after max retries exhausted

---

## 📋 Pipeline Stages

### Stage 1: Ideation
**Agent:** Planner (GPT-5.2)  
**Autonomous:** Yes

- Extracts and analyzes requirements
- Defines project scope and constraints
- Creates high-level implementation roadmap
- Identifies dependencies and risks

### Stage 2: Specification
**Agent:** Specifier (GPT-5.2)  
**Autonomous:** Yes *(No human gate)*

- Generates complete SPEC.md document
- Defines functional and non-functional requirements
- Documents API contracts and data models
- Creates user stories with acceptance criteria
- Resolves ambiguities and open questions

### Stage 3: Simulation
**Agent:** Simulator (GPT-5.2)  
**Autonomous:** Yes

- Runs Monte Carlo simulations (1000 iterations)
- Identifies optimal task execution sequence
- Determines critical path
- Estimates timeline and resource needs
- Maximizes parallelization opportunities

### Stage 4: Architecture
**Agent:** Architect (Claude Opus 4.5)  
**Autonomous:** Yes

- Designs system architecture
- Defines components and interfaces
- Creates data flow diagrams
- Documents technology choices and ADRs
- Designs API specifications

### Stage 5: Implementation
**Agents:** Implementer, Tester, Security, Optimizer  
**Models:** GPT-5.2-Codex, Claude Sonnet 4.5, GPT-5.2  
**Autonomous:** Yes

- Generates production-ready code
- Creates comprehensive test suites (80%+ coverage)
- Performs security vulnerability scanning
- Optimizes performance bottlenecks
- Documents code and APIs

### Stage 6: Validation
**Agents:** Tester, Reviewer, Security, Debugger  
**Models:** Claude Sonnet 4.5, GPT-5.2, Claude Haiku 4.5  
**Autonomous:** Yes (with auto-retry)

- Runs all tests and verifies coverage
- Performs code quality review
- Executes security vulnerability scan
- Auto-retries on failure (max 3 attempts)
- Invokes Debugger agent to fix issues
- Notifies human only after retries exhausted

### Stage 7: Staging
**Agents:** Merger, Documenter  
**Models:** Claude Opus 4.5, Gemini 3 Pro  
**Autonomous:** No (requires human approval)

- Creates pull request with all artifacts
- Generates deployment documentation
- Resolves merge conflicts
- Requests human review and approval
- **ONLY stage requiring human interaction**

---

## 🔄 Autonomy & Self-Healing

### Automatic Retry Logic

When validation failures occur:
1. **Attempt 1-3**: Debugger agent investigates and fixes issues
2. **Each retry**: Full validation suite runs again
3. **After retry 3**: Human notified for intervention

### Bounded Autonomy

SOMAS operates autonomously with clear boundaries:
- ✅ **Autonomous**: All 6 stages (Ideation → Validation)
- ⏸️ **Human Gate**: Only at Staging (final merge approval)
- 🚨 **Human Escalation**: Only when max retries exhausted

### Progress Notifications

Pipeline progress is reported via:
- Issue comments with stage completion status
- PR description updates with checklist
- Notifications on failures requiring intervention

---

## 📊 Quality Gates

Each stage has quality gates that must pass:

**Specification:**
- All requirements have unique IDs
- All requirements are testable
- No ambiguous language (TBD, maybe, etc.)
- All open questions resolved

**Implementation:**
- All tests passing
- Code coverage > 80%
- No critical security vulnerabilities
- Documentation complete

**Validation:**
- All acceptance criteria met
- Performance requirements satisfied
- Security scan passed
- Integration tests passing

---

## 🔒 Security

SOMAS implements security best practices:

- **Input Validation**: Project IDs validated to prevent path traversal
- **Injection Prevention**: Safe JSON encoding prevents shell injection
- **Security Scanning**: Automated vulnerability scanning in every pipeline
- **Secure Defaults**: Division-by-zero protection and error handling
- **Agent Review**: Dedicated Security agent reviews all code

---

## ⚙️ Configuration

### Main Configuration

See [`.somas/config.yml`](.somas/config.yml) for complete configuration including:
- Pipeline stage definitions
- AI agent provider mappings
- Quality gate requirements
- Optimization settings
- Security configurations

### Agent Configurations

Each agent has a detailed configuration file in [`.somas/agents/`](.somas/agents/):
- Role and responsibilities
- Prompt templates
- Output format specifications
- Quality checks

### Stage Definitions

Stage-specific configurations in [`.somas/stages/`](.somas/stages/):
- Input/output artifacts
- Agent assignments
- Quality gates
- Timeout settings

### Label System

SOMAS uses a comprehensive label system for workflow triggers, triage, and state machine orchestration. See [`.github/LABELS.md`](.github/LABELS.md) for:
- Complete label definitions
- Automated setup instructions
- Workflow integration details
- Label management best practices

Quick setup: Run `./scripts/setup-labels.sh` to create all labels at once.

---

## 📚 Documentation

- **[System Documentation](docs/somas/README.md)** - Complete SOMAS architecture
- **[Label System](.github/LABELS.md)** - Workflow labels and state machine setup
- **[Optimization Guide](docs/somas/optimization-guide.md)** - Advanced optimization techniques
- **[Copilot Integration](docs/somas/COPILOT_GUIDE.md)** - GitHub Copilot usage guide
- **[Troubleshooting](docs/somas/TROUBLESHOOTING.md)** - Common issues and solutions
- **[Migration Guide](docs/somas/MIGRATION_GUIDE.md)** - Configuration migration guide

---

## 💡 Example Use Cases

### Web Application
```
Issue: "Build a task management app with React frontend and Node.js backend"
Result: Full-stack application with tests, docs, and deployment config
```

### CLI Tool
```
Issue: "Create a Python CLI tool for file organization"
Result: Python package with argparse CLI, tests, and PyPI setup
```

### API Service
```
Issue: "Build a REST API for user authentication with JWT"
Result: API with endpoints, tests, security scanning, and OpenAPI spec
```

---

## 🎓 Advanced Features

### Monte Carlo Simulation

SOMAS uses Monte Carlo analysis to:
- Simulate 1000+ possible execution scenarios
- Identify the optimal task sequence
- Predict timeline with 90% confidence
- Maximize parallel task execution

### GitHub Project Integration

Automatic GitHub Project board creation:
- Visual progress tracking
- Task decomposition with sub-issues
- Real-time status updates
- Historical metrics and analytics

### Continuous Learning

SOMAS learns from each run:
- Duration estimation improvement
- Pattern extraction from successful runs
- Risk threshold adjustment
- Decomposition rule refinement

---

## 🤔 FAQ

**Q: How long does a project take?**  
A: Varies by complexity. Simple tools: 30-60 minutes. Complex systems: 2-8 hours.

**Q: Can I modify the generated code?**  
A: Absolutely! Review and refine as needed before merging.

**Q: What languages are supported?**  
A: Any major language. Specify preference in your project description.

**Q: Can I customize agent behavior?**  
A: Yes! Edit `.somas/agents/*.yml` to customize prompts and requirements.

**Q: What if validation fails repeatedly?**  
A: After 3 automatic retry attempts, you'll be notified to investigate manually.

**Q: Does SOMAS work with private repositories?**  
A: Yes, as long as GitHub Actions and required API keys are configured.

---

## 📜 License

MIT License - See [LICENSE](LICENSE) for details

---

## 🙏 Acknowledgments

SOMAS is powered by the 2026 Frontier Tier AI models:
- **GPT-5.2-Codex** (OpenAI) - SOTA coding agent
- **Claude Opus 4.5** (Anthropic) - Deepest reasoning
- **Claude Sonnet 4.5** (Anthropic) - Balanced power
- **GPT-5.2** (OpenAI) - General intelligence
- **Gemini 3 Pro** (Google) - Multimodal & long context
- **Grok Code Fast 1** (xAI) - Low latency orchestration

---

## 👤 Owner

**@scotlaclair** - Notifications and approvals

---

**Ready to build something amazing?**  
[Create your first SOMAS project →](../../issues/new/choose)
