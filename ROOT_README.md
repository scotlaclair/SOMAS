# SOMAS Root Directory

This document provides an overview of all files in the SOMAS repository root directory.

## Directory Structure

```
/
├── .claude/              # Claude AI assistant configuration
├── .gemini/              # Gemini AI assistant configuration
├── .github/              # GitHub workflows, templates, and automation
├── .somas/               # SOMAS configuration, agents, and templates
├── archived/             # Archived project files
├── docs/                 # Comprehensive documentation
├── scripts/              # Maintenance and utility scripts
├── somas/                # Core Python package
├── tests/                # Unit test suite
├── skills/               # Skills library
└── [root files]          # Project-level documentation and configuration
```

## Root Files Overview

### 📋 Project Documentation
- **[README.md](README.md)** - Main project overview, architecture, and getting started guide
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and release notes
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines and development setup
- **[SECURITY.md](SECURITY.md)** - Security policy and vulnerability reporting

### 🔧 Configuration Files
- **[requirements.txt](requirements.txt)** - Python dependencies with version constraints
- **[skill-rules.json](skill-rules.json)** - AI agent skill activation rules and triggers
- **[retrieval.yml](retrieval.yml)** - Retrieval-Augmented Generation (RAG) knowledge sources

### 📚 Implementation Documentation
- **[AUTONOMOUS_PIPELINE_SUMMARY.md](AUTONOMOUS_PIPELINE_SUMMARY.md)** - Autonomous pipeline implementation details
- **[COMMENT_DRIVEN_ORCHESTRATION.md](COMMENT_DRIVEN_ORCHESTRATION.md)** - Comment-driven orchestration system guide
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Dynamic parallel orchestration implementation
- **[CLAUDE.md](CLAUDE.md)** - AI assistant guide for working with SOMAS
- **[CROSS_REFERENCE_MATRIX.md](CROSS_REFERENCE_MATRIX.md)** - Cross-reference validation and dependency mapping

### 🛠️ Utility Scripts
- **[resolve-pr1-conflicts.sh](resolve-pr1-conflicts.sh)** - Automated PR conflict resolution script
- **[scripts/validate-consistency.sh](scripts/validate-consistency.sh)** - Cross-reference validation script

## File Categories

### Essential Reading (Start Here)
1. [README.md](README.md) - Project overview and architecture
2. [CONTRIBUTING.md](CONTRIBUTING.md) - Development setup and guidelines
3. [SECURITY.md](SECURITY.md) - Security considerations

### Configuration
4. [requirements.txt](requirements.txt) - Python dependencies
5. [skill-rules.json](skill-rules.json) - Agent skill rules
6. [retrieval.yml](retrieval.yml) - Knowledge retrieval config

### Implementation Details
7. [AUTONOMOUS_PIPELINE_SUMMARY.md](AUTONOMOUS_PIPELINE_SUMMARY.md) - Pipeline automation
8. [COMMENT_DRIVEN_ORCHESTRATION.md](COMMENT_DRIVEN_ORCHESTRATION.md) - Orchestration system
9. [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Technical implementation
10. [CLAUDE.md](CLAUDE.md) - AI assistant guide

### Maintenance
11. [CHANGELOG.md](CHANGELOG.md) - Version history
12. [resolve-pr1-conflicts.sh](resolve-pr1-conflicts.sh) - Conflict resolution

## Navigation Guide

- **New to SOMAS?** → Start with [README.md](README.md)
- **Want to contribute?** → Read [CONTRIBUTING.md](CONTRIBUTING.md)
- **Security concerns?** → Check [SECURITY.md](SECURITY.md)
- **Technical details?** → See implementation docs above
- **Version changes?** → Review [CHANGELOG.md](CHANGELOG.md)

## Directory Documentation

Each major directory has its own README.md and index.json file:
- [.somas/](.somas/) - Configuration and templates
- [somas/](somas/) - Core Python package
- [.github/](.github/) - GitHub automation
- [scripts/](scripts/) - Utility scripts
- [skills/](skills/) - Skills library
- [tests/](tests/) - Test suite
- [docs/](docs/) - Documentation

---

*This index is automatically maintained. Last updated: January 30, 2026*