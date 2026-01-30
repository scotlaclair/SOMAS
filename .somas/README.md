# SOMAS Configuration Directory (.somas/)

## Overview

The `.somas/` directory contains the complete configuration ecosystem for the SOMAS (Self-Sovereign Orchestrated Multi-Agent System) autonomous software development pipeline. This hidden directory houses all configuration files, agent definitions, templates, and supporting assets that drive the AI-orchestrated development process.

## Directory Structure

### `agents/`
AI agent configurations and orchestration definitions.

- **README.md**: Comprehensive agent documentation
- **agents.json**: Machine-readable agent index
- **_base.yml**: Base configuration inherited by all agents
- **{agent}.yml**: Individual agent definitions (17 specialized agents)

### `analytics/`
Analytics and metrics configuration schemas.

- **schema.yml**: Data structure definitions for analytics

### `apo/`
Autonomous Pipeline Orchestration configurations.

- **base-prompt.yml**: Core APO prompt templates
- **mental-models.yml**: Mental model definitions
- **task-analyzer.yml**: Task complexity analysis configuration
- **chains/**: Chain strategy definitions

### `architecture/`
Architecture patterns and reference designs.

### `config/`
Configuration management and validation.

### `knowledge/`
Knowledge base and reference materials.

### `patterns/`
Design patterns and best practices.

- **README.md**: Pattern documentation and usage guidelines

### `prompts/`
Prompt engineering templates and strategies.

### `stages/`
Pipeline stage definitions (11-stage Aether Lifecycle).

- **{stage}.yml**: Individual stage configurations

### `templates/`
Artifact templates for pipeline outputs.

- **SPEC.md**: Requirements specification template
- **architecture.md**: Architecture design template
- **execution_plan.yml**: Implementation planning template
- ***.json**: Schema definitions for state management

## Key Configuration Files

### `config.yml`
Main SOMAS configuration file defining:
- Pipeline stages and orchestration
- AI agent provider configurations
- Quality gates and validation rules
- Security settings and access controls
- Optimization parameters

### `backlog.md`
Product backlog and roadmap items.

### `roadmap.md`
Strategic roadmap and milestones.

## Usage Guidelines

### For Pipeline Operators
- Modify `config.yml` to adjust pipeline behavior
- Update agent configurations in `agents/` for new capabilities
- Add templates in `templates/` for new artifact types
- Configure stages in `stages/` for process changes

### For AI Agents
- Reference `config.yml` for pipeline settings
- Use templates from `templates/` for consistent outputs
- Follow patterns from `patterns/` for design consistency
- Access knowledge from `knowledge/` for context

### For Developers
- Extend agent capabilities in `agents/`
- Add new stages in `stages/`
- Create templates in `templates/`
- Document patterns in `patterns/`

## Security Considerations

- Validate all configuration changes through testing
- Review agent configurations for security implications
- Ensure templates don't expose sensitive information
- Monitor access to configuration files

## Maintenance

- Update timestamps in README files when making changes
- Validate configuration syntax before deployment
- Test pipeline changes in isolated environments
- Document configuration changes in changelog

---

*Last updated: January 30, 2026 12:00 UTC*</content>
<parameter name="filePath">/Users/architect/Developer/projects/somas/.somas/README.md