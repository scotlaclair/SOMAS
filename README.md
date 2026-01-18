# SOMAS
**Self-Sovereign Orchestrated Multi-Agent System - Autonomous AI Development Pipeline**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![SOMAS Version](https://img.shields.io/badge/SOMAS-v1.0.0-green.svg)](.somas/config.yml)

---

## Overview

SOMAS is an AI-first Software Development Life Cycle (SDLC) that transforms project ideas into production-ready software through orchestrated AI agents. The system currently supports **two operational modes**:

### SOMAS Extended (Current - 7-Stage Pipeline)
An enhanced pipeline featuring complete specification and simulation-based optimization:
- **7-Stage Pipeline** with specification and simulation optimization  
- **Monte Carlo Analysis** for optimal task sequencing
- **GitHub Project Integration** for visual progress tracking
- **Specification Gates** for requirement clarification
- **Continuous Learning** from historical data

### SOMAS Lite (5-Stage Pipeline)  
The original autonomous pipeline with comprehensive agent documentation:
- **5-Stage Pipeline** (Ideation → Architecture → Implementation → Validation → Staging)
- **8 Specialized AI Agents** with detailed configurations
- **Multi-Provider AI** (GitHub Copilot, Gemini, OpenAI GPT-4)
- **Comprehensive Documentation** for each agent and stage
- **Quality Gates** (80% test coverage, security scanning, code review)

---

## Quick Start

### Using SOMAS Extended (7-Stage)

1. Create an issue with your project idea
2. Add the `somas-project` label
3. The pipeline will automatically:
   - Generate a specification (with human approval gate)
   - Run simulations to optimize task ordering
   - Execute through all 7 stages
   - Track progress in GitHub Projects

### Using SOMAS Lite (5-Stage)

1. Create an issue using the SOMAS Project Request template
2. Add the `somas:start` label  
3. The pipeline will autonomously:
   - Plan, design, implement, validate, and document
   - Create a PR with all generated code
   - Request human approval at the staging gate

---

## Documentation

### SOMAS Extended
- [Main Documentation](docs/somas/README.md)
- [Optimization Guide](docs/somas/optimization-guide.md)

### SOMAS Lite
- [Getting Started](docs/somas/getting-started.md)  
- [Agent Configurations](.somas/agents/)

For complete documentation on both modes, architecture details, and configuration options, see the full documentation in the `docs/` directory.

---

## Choosing Between Extended and Lite

### Use SOMAS Extended When:
- You need detailed specifications before implementation
- You want optimal task ordering through simulation
- You need GitHub Project integration for tracking

### Use SOMAS Lite When:
- You want faster, more autonomous execution
- You have well-defined requirements already
- You prefer comprehensive agent documentation

---

## License

MIT License - See [LICENSE](LICENSE) for details

---

**Ready to build something amazing?**  
[Create your first SOMAS project →](../../issues/new/choose)
