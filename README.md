# SOMAS Lite

**Self-Sovereign Orchestrated Multi-Agent System**

An autonomous development pipeline that transforms project ideas into production-ready code using AI agents powered by GitHub Copilot, Gemini Code Assist, and OpenAI GPT-4.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![SOMAS Version](https://img.shields.io/badge/SOMAS-v1.0.0-green.svg)](.somas/config.yml)

---

## 🚀 What is SOMAS?

SOMAS Lite is an autonomous AI-powered development pipeline that takes your project ideas from concept to production-ready code with minimal human intervention. Simply describe your project in a GitHub issue, and SOMAS orchestrates a team of specialized AI agents to plan, design, implement, test, and document your solution.

### Key Features

- 🤖 **Autonomous Development**: AI agents handle the entire development lifecycle
- 🎯 **Multi-Agent Coordination**: Specialized agents for planning, architecture, coding, testing, and more
- 🔄 **Iterative Refinement**: Agents collaborate and refine until quality gates are met
- ✅ **Quality Assurance**: Built-in testing, code review, and security analysis
- 📝 **Comprehensive Documentation**: Auto-generated docs, API references, and guides
- 🔒 **Security First**: Automated vulnerability scanning and secure coding practices
- 🌐 **Multi-Provider**: Leverages Copilot, Gemini, and GPT-4 for optimal results

---

## 🏗️ Architecture

SOMAS operates through a **5-stage pipeline**, each with specialized AI agents:

```
┌─────────────┐    ┌──────────────┐    ┌─────────────────┐    ┌────────────┐    ┌─────────┐
│  Ideation   │ -> │ Architecture │ -> │ Implementation  │ -> │ Validation │ -> │ Staging │
│  (Planner)  │    │ (Architect)  │    │(Implementer+    │    │ (Tester+   │    │(Doc+    │
│             │    │              │    │    Tester)      │    │ Reviewer+  │    │Reviewer)│
│             │    │              │    │                 │    │ Security)  │    │         │
└─────────────┘    └──────────────┘    └─────────────────┘    └────────────┘    └─────────┘
```

### Specialized Agents

| Agent | Provider | Role |
|-------|----------|------|
| **Orchestrator** | Copilot | Coordinates pipeline, manages state, handles failures |
| **Planner** | OpenAI GPT-4 | Analyzes requirements, creates roadmap |
| **Architect** | GPT-4 + Gemini | Designs system architecture, defines components |
| **Implementer** | Copilot | Generates production-ready code |
| **Tester** | Copilot | Creates comprehensive test suites (80%+ coverage) |
| **Reviewer** | Gemini | Performs code quality and architecture reviews |
| **Security** | Gemini | Scans for vulnerabilities, validates secure coding |
| **Documenter** | Copilot | Creates documentation, guides, and examples |

---

## 🎯 Quick Start

### 1. Create a Project Request

1. Go to [Issues](../../issues/new/choose)
2. Select "🤖 SOMAS Project Request"
3. Fill in your project idea and requirements
4. Submit the issue

### 2. Start the Pipeline

Add the `somas:start` label to your issue. SOMAS will:
- Create a feature branch (`somas/{issue-number}`)
- Create a draft pull request
- Begin autonomous development

### 3. Monitor Progress

Watch the pipeline progress through stages:
- 🎯 **Ideation**: Requirements analysis and planning
- 🏗️ **Architecture**: System design and component definition
- ⚙️ **Implementation**: Code generation and testing
- ✅ **Validation**: Quality assurance and security review
- 📝 **Staging**: Documentation and final review

### 4. Review and Approve

When the staging stage completes:
- You'll be notified (@scotlaclair) for review
- Review the generated code in the PR
- Approve and merge when ready

---

## 📋 Pipeline Stages

### Stage 1: Ideation
**Agent:** Planner (OpenAI GPT-4)
- Extracts and analyzes requirements
- Defines project scope
- Creates implementation roadmap
- Identifies dependencies and constraints

### Stage 2: Architecture
**Agent:** Architect (GPT-4 + Gemini)
- Designs system architecture
- Defines components and interactions
- Creates data models
- Documents architectural decisions (ADRs)

### Stage 3: Implementation
**Agents:** Implementer + Tester (Copilot)
- Generates production-ready code
- Implements comprehensive error handling
- Creates unit and integration tests
- Achieves 80%+ test coverage

### Stage 4: Validation
**Agents:** Tester + Reviewer + Security (Copilot + Gemini)
- Runs complete test suite
- Performs code quality review
- Conducts security vulnerability scan
- Validates best practices compliance

### Stage 5: Staging
**Agents:** Documenter + Reviewer (Copilot + Gemini)
**Requires Human Approval**
- Creates comprehensive documentation
- Generates API references
- Writes usage examples
- Prepares for release

---

## 🔧 Configuration

SOMAS is configured via `.somas/config.yml`:

```yaml
system:
  name: "SOMAS Lite"
  version: "1.0.0"

pipeline:
  trigger:
    method: "github_issue"
    label: "somas:start"

quality:
  test_coverage_minimum: 80
  linting_required: true

limits:
  iterations:
    per_task: 5
    per_step: 10
    per_stage: 25
    per_pipeline: 100
```

See [`.somas/config.yml`](.somas/config.yml) for full configuration options.

---

## 🤖 Agent Configuration

Each agent has a dedicated configuration file in `.somas/agents/`:

- **orchestrator.yml**: Pipeline coordination and state management
- **planner.yml**: Requirements analysis and planning
- **architect.yml**: System design and architecture
- **implementer.yml**: Code generation
- **tester.yml**: Test suite creation
- **reviewer.yml**: Code quality review
- **security.yml**: Security analysis
- **documenter.yml**: Documentation generation

These configurations define agent roles, responsibilities, tasks, and quality standards.

---

## 📚 Documentation

- **[Full Documentation](docs/somas/README.md)**: Complete SOMAS guide
- **[Getting Started](docs/somas/getting-started.md)**: Your first SOMAS project
- **[Agent Configurations](.somas/agents/)**: Detailed agent specifications
- **[Templates](.somas/templates/)**: Plan and architecture templates
- **[Design Patterns](.somas/patterns/)**: Common patterns and best practices

---

## 🎨 Project Types Supported

- **APIs**: REST/GraphQL services
- **CLI Tools**: Command-line applications
- **Libraries**: Reusable packages and modules
- **Web Apps**: Frontend applications
- **Scripts**: Automation and utility scripts

---

## 🔒 Security

SOMAS includes comprehensive security features:
- Automated vulnerability scanning
- Input validation verification
- Secure coding practice enforcement
- Dependency security checks
- Security agent review

All generated code follows security best practices and is scanned for common vulnerabilities.

---

## 🚦 Quality Gates

SOMAS enforces quality standards at each stage:
- ✅ All requirements implemented
- ✅ 80%+ test coverage
- ✅ All tests passing
- ✅ Code review approved
- ✅ No critical security issues
- ✅ Documentation complete
- ✅ Architecture compliance verified

---

## 🤝 Human-in-the-Loop

While SOMAS is autonomous, it requires human approval at key points:
- **Staging Gate**: Final review before deployment
- **Quality Issues**: When quality gates fail after retries
- **Security Concerns**: Critical vulnerabilities detected
- **Iteration Limits**: When max iterations exceeded

You'll be notified (@scotlaclair) when intervention is needed.

---

## 📊 Iteration Limits

To prevent infinite loops, SOMAS enforces iteration limits:
- Per task: 5 iterations
- Per step: 10 iterations
- Per stage: 25 iterations
- Per pipeline: 100 iterations

When limits are reached, human intervention is requested.

---

## 🛠️ Technology

SOMAS leverages multiple AI providers:
- **GitHub Copilot**: Code generation, testing, documentation
- **Gemini Code Assist**: Code review, security analysis
- **OpenAI GPT-4**: Strategic planning, architecture design

This multi-provider approach ensures optimal results by using each AI's strengths.

---

## 📝 Example Workflow

1. **Submit Issue**: "Create a CLI tool for analyzing GitHub repos"
2. **Add Label**: `somas:start`
3. **Pipeline Executes**:
   - Planner creates project roadmap
   - Architect designs the CLI structure
   - Implementer writes Python code with argparse
   - Tester creates comprehensive test suite
   - Reviewer validates code quality
   - Security scans for vulnerabilities
   - Documenter creates README and usage guide
4. **Review PR**: Check generated code and tests
5. **Approve**: Merge when satisfied
6. **Deploy**: Use the generated CLI tool!

---

## 🌟 Benefits

- **Speed**: From idea to code in minutes/hours, not days
- **Quality**: Consistent high-quality code with tests and docs
- **Best Practices**: Follows established patterns and standards
- **Security**: Built-in security analysis and validation
- **Documentation**: Comprehensive docs generated automatically
- **Learning**: Review AI-generated code to learn patterns

---

## 📖 Learn More

- **[Getting Started Guide](docs/somas/getting-started.md)**: Step-by-step first project
- **[Full Documentation](docs/somas/README.md)**: Complete reference
- **[Agent Configurations](.somas/agents/)**: Understanding the agents
- **[Design Patterns](.somas/patterns/)**: Common patterns used

---

## 🤔 FAQ

**Q: Can I modify the generated code?**  
A: Absolutely! The generated code is a starting point. Review and refine as needed.

**Q: What languages are supported?**  
A: SOMAS can generate code in any major language. Specify your preference in the issue.

**Q: How long does it take?**  
A: Varies by project complexity. Simple tools: minutes. Complex systems: hours.

**Q: Can I customize agent behavior?**  
A: Yes! Edit `.somas/agents/*.yml` to customize prompts and requirements.

**Q: What if I don't like the generated code?**  
A: Add comments on the PR with requested changes, or manually refine the code.

---

## 📜 License

MIT License - See [LICENSE](LICENSE) for details

---

## 🙏 Acknowledgments

SOMAS Lite is powered by:
- GitHub Copilot
- Gemini Code Assist  
- OpenAI GPT-4

---

**Ready to build something amazing?**  
[Create your first SOMAS project →](../../issues/new/choose)
# SOMAS
Self-Sovereign Orchestrated Multi-Agent System - Autonomous AI Development Pipeline

## Overview

SOMAS is an AI-first Software Development Life Cycle (SDLC) that transforms project ideas into production-ready software through orchestrated AI agents. The system features:

- **7-Stage Pipeline** with complete specification and simulation optimization
- **Autonomous AI Agents** specialized for each development phase
- **Simulation-Based Optimization** using Monte Carlo analysis for optimal task sequencing
- **GitHub Project Integration** for visual progress tracking and metrics collection
- **Human Gates** at critical decision points
- **Continuous Learning** from historical data to improve estimates

## Pipeline Architecture

```
┌─────────────┐
│  Ideation   │  High-level plan from project idea
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Specification   │  Complete, unambiguous spec (HUMAN GATE ✋)
└──────┬──────────┘
       │
       ▼
┌─────────────┐
│ Simulation  │  Optimal task sequencing via Monte Carlo
└──────┬──────┘
       │
       ▼
┌──────────────┐
│ Architecture │  System design and component planning
└──────┬───────┘
       │
       ▼
┌────────────────┐
│ Implementation │  Code generation following optimized plan
└──────┬─────────┘
       │
       ▼
┌────────────┐
│ Validation │  Comprehensive testing and verification
└──────┬─────┘
       │
       ▼
┌──────────┐
│ Staging  │  Deploy to staging (HUMAN GATE ✋)
└──────────┘
```

## Key Features

### 🎯 Complete Specification Stage
Before architecture begins, SOMAS creates a comprehensive specification document with:
- Enumerated, testable functional requirements
- Measurable non-functional requirements
- User stories with acceptance criteria
- Data dictionary and API contracts
- Security and integration requirements
- **Human approval gate** to ensure quality before proceeding

**Why?** Reduces iteration risk by catching requirement issues early, preventing costly rework in later stages.

### 🔬 Simulation & Optimization
Monte Carlo simulation (1000 iterations) determines the optimal task execution strategy:
- **Critical path identification** - Know which tasks determine project completion
- **Parallelization opportunities** - Execute independent tasks simultaneously
- **Risk assessment** - Identify high-risk tasks with mitigation strategies
- **Duration prediction** - 90% confidence intervals for completion time
- **Task optimization** - Recommendations for decomposition and sizing

**Impact:** Reduces total pipeline duration by 40-60% through intelligent parallelization and risk management.

### 📊 GitHub Project Integration
Automatic integration with GitHub Projects provides:
- Visual progress tracking across all pipeline stages
- Task issues created from execution plan
- Automated card movement between columns
- Metrics tracking (cycle time, throughput, estimation accuracy)
- Clear visibility of human intervention points

### 📈 Analytics & Learning
Continuous learning from every pipeline run:
- Task duration vs. estimate accuracy
- Iteration patterns by task type
- Parallelization efficiency
- Critical path prediction accuracy
- Human intervention frequency

Machine learning models improve over time, providing better estimates and recommendations.

## Quick Start

### 1. Create a Project

Create a GitHub issue with:
- **Label:** `somas-project`
- **Title:** Your project name  
- **Description:** Project idea and requirements

### 2. Automatic Execution

The pipeline automatically executes through 7 stages:
1. **Ideation** - High-level planning
2. **Specification** - Detailed requirements (requires your approval ✋)
3. **Simulation** - Execution optimization
4. **Architecture** - System design
5. **Implementation** - Code generation
6. **Validation** - Testing and verification
7. **Staging** - Deployment preparation (requires your approval ✋)

### 3. Track Progress

Monitor progress through:
- **GitHub Project Board** - Visual task tracking
- **Workflow Runs** - Stage completion status
- **Analytics Dashboard** - Performance metrics

### 4. Human Gates

You'll be notified at two critical gates:
- **After Specification** - Approve complete requirements document
- **After Staging** - Approve deployment to production

## Configuration

Main configuration: `.somas/config.yml`

Key settings:
```yaml
optimization:
  simulation:
    enabled: true
    iterations: 1000
  parallelization:
    enabled: true
    max_concurrent_tasks: 5
    
project_management:
  enabled: true
  github_project:
    create_per_pipeline: true
    
analytics:
  enabled: true
  track:
    - task_duration_vs_estimate
    - parallel_efficiency
```

## Documentation

- **[SOMAS Documentation](docs/somas/README.md)** - Complete system documentation
- **[Optimization Guide](docs/somas/optimization-guide.md)** - Advanced optimization techniques
- **[Configuration Reference](.somas/config.yml)** - Full configuration options
- **[Analytics Schema](.somas/analytics/schema.yml)** - Metrics and data structure

## Directory Structure

```
.somas/
├── config.yml                    # Main configuration
├── stages/                       # Stage definitions
│   ├── specification.yml         # Specification stage
│   ├── simulation.yml            # Simulation stage
│   └── ...
├── agents/                       # AI agent configurations
│   ├── specifier.yml             # Specification agent
│   ├── simulator.yml             # Simulation agent
│   └── ...
├── templates/                    # Document templates
│   ├── SPEC.md                   # Specification template
│   ├── execution_plan.yml        # Execution plan template
│   └── ...
└── analytics/                    # Analytics and learning
    ├── schema.yml                # Data schema
    └── runs/                     # Historical run data

.github/
├── workflows/
│   ├── somas-pipeline.yml        # Main 7-stage pipeline
│   └── somas-project-sync.yml    # GitHub Project integration
└── project-template.yml          # Project board template

docs/somas/
├── README.md                     # System documentation
├── optimization-guide.md         # Optimization techniques
├── MIGRATION_GUIDE.md            # Migration guide for configuration updates
└── TROUBLESHOOTING.md            # Common issues and solutions
```

## Documentation

- **[System Documentation](docs/somas/README.md)** - Complete SOMAS overview and architecture
- **[Migration Guide](docs/somas/MIGRATION_GUIDE.md)** - Guide for migrating configurations and understanding changes
- **[Troubleshooting Guide](docs/somas/TROUBLESHOOTING.md)** - Solutions to common issues and debugging tips
- **[Optimization Guide](docs/somas/optimization-guide.md)** - Advanced optimization techniques

## Key Benefits

✅ **Faster Development** - 40-60% reduction in timeline through optimization  
✅ **Higher Quality** - Complete specifications prevent requirement issues  
✅ **Better Visibility** - GitHub Projects integration shows real-time progress  
✅ **Risk Management** - Early identification of high-risk tasks with mitigations  
✅ **Continuous Improvement** - Analytics and learning improve every run  
✅ **Human Control** - Approval gates at critical decision points  
✅ **Security Hardened** - Input validation, injection prevention, and secure defaults

## Security

SOMAS has been hardened with multiple security improvements:

- **Input Validation** - Project IDs validated to prevent path traversal attacks
- **Injection Prevention** - Safe JSON encoding prevents shell injection
- **Secure Defaults** - Division-by-zero protection and error handling
- **Dependency Management** - Proper installation and version management
- **Regular Scans** - CodeQL security scanning integrated into development

For security concerns, please open a security advisory rather than a public issue.

## Owner

**@scotlaclair** - All notifications and approvals

## License

This project is under active development. License information will be added in a future release.

---

*SOMAS - Autonomous AI development from idea to production*
