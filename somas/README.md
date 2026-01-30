# SOMAS Configuration Directory

## Overview

The `.somas/` directory contains configuration, agents, and supporting modules for the SOMAS (Self-Sovereign Orchestrated Multi-Agent System) autonomous software development pipeline.

## Directory Structure

### `agents/`
AI agent configurations and definitions. Contains YAML files defining each specialized agent, their roles, prompts, and capabilities.

- **README.md**: Agent documentation and usage guide
- **agents.json**: Machine-readable agent index
- **{agent}.yml**: Individual agent configurations

### `analytics/`
Proof-of-concept metrics tracking and reporting. Measures pipeline performance, time savings, and quality improvements.

- **poc_metrics.py**: Core metrics collection and analysis
- **README.md**: Analytics documentation

### `apo/`
Autonomous Pipeline Orchestration. Intelligent task complexity analysis and routing to appropriate processing strategies.

- **task_complexity_analyzer.py**: Complexity assessment engine
- **constants.py**: Scoring algorithms and thresholds
- **README.md**: APO documentation

### `core/`
Core SOMAS functionality and execution engine.

- **runner.py**: Main pipeline execution engine
- **state_manager.py**: Pipeline state persistence
- **circuit_breaker.py**: Failure handling and recovery
- **feedback_loop.py**: Learning and optimization
- **README.md**: Core module documentation

## Configuration Files

- **config.yml**: Main SOMAS configuration (when present)
- **stages/**: Pipeline stage definitions (when present)
- **templates/**: Artifact templates (when present)

## Usage

This directory is automatically managed by the SOMAS pipeline. Manual modifications should be made with caution and validated through testing.

---

*Last updated: January 30, 2026 12:00 UTC*</content>
<parameter name="filePath">/Users/architect/Developer/projects/somas/somas/README.md