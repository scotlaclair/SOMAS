# SOMAS GitHub Actions Workflows

## Overview

The workflows directory contains GitHub Actions automation that powers the SOMAS autonomous development pipeline. These workflows handle CI/CD, security scanning, quality assurance, and pipeline orchestration across the 11-stage Aether Lifecycle.

## Workflow Categories

### Pipeline Orchestration (`somas-*.yml`)

#### `somas-pipeline.yml` - Main Pipeline
**Purpose:** Orchestrates the complete 11-stage Aether Lifecycle
**Triggers:** Manual dispatch, scheduled runs
**Stages:** Intake → Specify → Plan → Decompose → Implement → Verify → Integrate → Harden → Release → Operate → Analyze
**Agents:** 17 specialized AI agents across all stages

#### `somas-orchestrator.yml` - Coordination Hub
**Purpose:** Manages inter-stage communication and artifact handoffs
**Triggers:** Pipeline events, agent completions
**Function:** State management, error recovery, progress tracking

#### `somas-dev-autonomous.yml` - Development Mode
**Purpose:** Enables autonomous development with human oversight
**Triggers:** Push to feature branches, manual dispatch
**Features:** AI-driven implementation, automated testing, security validation

### Stage-Specific Workflows

#### `somas-stage-02.yml` - Specification Stage
**Purpose:** Handles requirement gathering and specification generation
**Triggers:** Issue creation, manual dispatch
**Output:** SPEC.md and requirement artifacts

#### `somas-meta-capture.yml` - Metadata Collection
**Purpose:** Captures project metadata and context for pipeline processing
**Triggers:** Project creation, metadata updates
**Output:** Project configuration and context files

### Quality & Security (`*-security.yml`, `codeql.yml`, `semgrep.yml`)

#### `pr-security.yml` - Pull Request Security
**Purpose:** Security validation for all pull requests
**Triggers:** PR opened, updated, or reopened
**Checks:** Dependency review, vulnerability scanning, security policies

#### `validate-consistency.yml` - Cross-Reference Validation
**Purpose:** Ensures repository consistency and validates cross-references
**Triggers:** Push to main/develop, PR opened/updated
**Checks:** Agent configurations, skill references, template files, YAML/JSON syntax
**Features:** Automated validation, PR comments, consistency matrix validation

#### `codeql.yml` - CodeQL Security Analysis
**Purpose:** Advanced security vulnerability detection
**Triggers:** Push, PR, weekly schedule
**Languages:** JavaScript, Python, and repository languages
**Features:** Static analysis, vulnerability detection, code quality

#### `semgrep.yml` - Semantic Code Analysis
**Purpose:** Custom security rules and code quality checks
**Triggers:** Push, PR events
**Rules:** Custom security patterns, code standards

### Maintenance & Automation

#### `sync-stage-milestones.yml` - Milestone Sync
**Purpose:** Synchronizes project milestones with pipeline stages
**Triggers:** Milestone changes, project updates
**Function:** Automated milestone management and progress tracking

#### `somas-project-sync.yml` - Project Synchronization
**Purpose:** Keeps project boards and issues synchronized
**Triggers:** Issue/PR updates, project changes
**Function:** Automated project management and status updates

#### `intake-triage.yml` - Issue Triage
**Purpose:** Automated classification and routing of incoming issues
**Triggers:** Issue creation and updates
**Agents:** Triage agent for initial classification

### Pull Request Management

#### `somas-pr-continue.yml` - PR Continuation
**Purpose:** Continues autonomous development on pull requests
**Triggers:** PR comments with continuation commands
**Function:** Resumes AI development workflow on existing PRs

#### `pr-checklist-detector.yml` - Checklist Validation
**Purpose:** Validates pull request checklists and requirements
**Triggers:** PR opened, updated
**Checks:** Required approvals, testing completion, documentation

## Workflow Architecture

### Trigger Types
- **Manual:** `workflow_dispatch` for on-demand execution
- **Scheduled:** Cron jobs for maintenance and monitoring
- **Event-driven:** Push, PR, issue events for reactive automation

### Agent Integration
- **Copilot Agents:** 17 specialized agents for different stages
- **External APIs:** Integration with AI providers (Claude, GPT, Gemini, Grok)
- **Artifact Storage:** GitHub repositories for pipeline artifacts

### Security Model
- **Least Privilege:** Minimal required permissions per workflow
- **Secret Management:** GitHub secrets for API keys and tokens
- **Audit Logging:** Comprehensive logging for security monitoring

## Usage Guidelines

### For Pipeline Operators
- Use manual dispatch for testing new pipeline configurations
- Monitor workflow runs for errors and performance issues
- Update workflow files when adding new pipeline stages

### For Developers
- Workflows run automatically on PR creation
- Check workflow status before merging pull requests
- Address any workflow failures promptly

### For Maintainers
- Keep workflow files synchronized with pipeline changes
- Test workflow modifications in feature branches
- Document workflow changes and their purposes

## Monitoring & Debugging

### Workflow Logs
- Access logs through GitHub Actions tab
- Check job status and error messages
- Review artifact outputs for debugging

### Common Issues
- **Permission Errors:** Check workflow permissions in repository settings
- **Secret Missing:** Ensure required secrets are configured
- **API Limits:** Monitor rate limits for external API calls

### Performance Optimization
- Use appropriate runner sizes for compute-intensive jobs
- Implement caching for dependencies and build artifacts
- Schedule heavy workflows during off-peak hours

## Integration Points

- **GitHub Issues:** Automated issue routing and management
- **Project Boards:** Workflow status synchronization
- **Branch Protection:** Required workflow checks for merges
- **Notifications:** Slack/Discord integration for alerts

---

*Last updated: January 30, 2026 12:00 UTC*</content>
<parameter name="filePath">/Users/architect/Developer/projects/somas/.github/workflows/README.md