# SOMAS Issue Templates

## Overview

The ISSUE_TEMPLATE directory contains structured GitHub issue templates that guide users to provide comprehensive information when reporting bugs, requesting features, or asking questions about SOMAS projects. These templates ensure consistent issue formatting and enable automated routing to appropriate SOMAS agents.

## Template Categories

### `somas-bug.yml` - Bug Reports
For reporting bugs in SOMAS-generated code, pipeline failures, or system issues.

**Triggers routing to:**
- Implementation bugs → Implementer agent
- Test failures → Tester agent
- Specification gaps → Planner agent
- Documentation issues → Documenter agent

### `somas-change.yml` - Change Requests
For requesting modifications to existing SOMAS projects or pipeline behavior.

**Includes:**
- Current vs desired state analysis
- Impact assessment
- Implementation complexity evaluation

### `somas-enhance.yml` - Feature Requests
For proposing new features or enhancements to SOMAS capabilities.

**Captures:**
- Feature description and use cases
- Technical requirements
- Integration points with existing pipeline

### `somas-project.yml` - New Projects
For initiating new SOMAS-managed software development projects.

**Gathers:**
- Project requirements and scope
- Technical constraints and preferences
- Timeline and priority information

### `somas-question.yml` - Questions & Support
For asking questions about SOMAS usage, configuration, or troubleshooting.

**Supports:**
- Usage guidance requests
- Configuration questions
- Pipeline troubleshooting
- Best practices inquiries

## Configuration

### `config.yml`
- **blank_issues_enabled: false** - Forces use of structured templates
- **contact_links** - Provides helpful links for documentation, discussions, and bug reports

## Template Structure

Each template follows a consistent structure:

1. **Header Section** - Clear title, description, and routing information
2. **Required Fields** - Essential information for proper classification
3. **Optional Fields** - Additional context and details
4. **Validation** - Input validation and format checking

## Automated Processing

Templates are designed to work with SOMAS automation:

- **Label Assignment** - Automatic labeling based on issue type
- **Agent Routing** - Issues routed to appropriate specialized agents
- **Priority Assessment** - Urgency and impact evaluation
- **Project Association** - Links issues to specific SOMAS projects

## Usage Guidelines

### For Users
- Choose the most appropriate template for your issue type
- Fill out all required fields completely
- Provide specific examples and reproduction steps
- Include relevant project IDs and context

### For Maintainers
- Update templates as SOMAS capabilities evolve
- Test template functionality regularly
- Monitor issue quality and template effectiveness
- Add new templates for emerging issue types

## Integration Points

- **GitHub Issues API** - Automated issue creation and management
- **SOMAS Triage Agent** - Initial issue classification and routing
- **Project Boards** - Issue tracking and workflow management
- **Label System** - Automated categorization and prioritization

## Quality Assurance

Templates include validation for:
- Required field completion
- Format checking (URLs, project IDs, etc.)
- Input length limits
- Prohibited content filtering

---

*Last updated: January 30, 2026 12:00 UTC*</content>
<parameter name="filePath">/Users/architect/Developer/projects/somas/.github/ISSUE_TEMPLATE/README.md