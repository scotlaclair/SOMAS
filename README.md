# SOMAS Lite

**Self-Sovereign Orchestrated Multi-Agent System**

An autonomous development pipeline that transforms project ideas into production-ready code using AI agents powered by GitHub Copilot, Gemini Code Assist, and Codex.

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
- 🌐 **Multi-Provider**: Leverages Copilot, Gemini, and Codex for optimal results

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
| **Planner** | Codex | Analyzes requirements, creates roadmap |
| **Architect** | Codex + Gemini | Designs system architecture, defines components |
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
**Agent:** Planner (Codex)
- Extracts and analyzes requirements
- Defines project scope
- Creates implementation roadmap
- Identifies dependencies and constraints

### Stage 2: Architecture
**Agent:** Architect (Codex + Gemini)
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
- **Codex**: Strategic planning, architecture design

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
- OpenAI Codex

---

**Ready to build something amazing?**  
[Create your first SOMAS project →](../../issues/new/choose)
