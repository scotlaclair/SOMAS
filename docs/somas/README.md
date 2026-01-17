# SOMAS Lite Documentation

Welcome to the complete documentation for SOMAS (Self-Sovereign Orchestrated Multi-Agent System) Lite.

---

## Table of Contents

1. [Introduction](#introduction)
2. [How SOMAS Works](#how-somas-works)
3. [Pipeline Stages](#pipeline-stages)
4. [Agent System](#agent-system)
5. [Configuration](#configuration)
6. [Project Types](#project-types)
7. [Quality Assurance](#quality-assurance)
8. [Security](#security)
9. [Troubleshooting](#troubleshooting)
10. [Advanced Usage](#advanced-usage)

---

## Introduction

SOMAS Lite is an autonomous development pipeline that transforms project ideas into production-ready code using AI agents. It coordinates multiple specialized AI agents (powered by GitHub Copilot, Gemini Code Assist, and Codex) to handle the complete software development lifecycle.

### Key Concepts

- **Autonomous Pipeline**: Minimal human intervention required
- **Multi-Agent System**: Specialized agents for different tasks
- **Multi-Provider AI**: Leverages strengths of different AI systems
- **Quality First**: Built-in testing, review, and security scanning
- **Human-in-the-Loop**: Human approval at critical decision points

---

## How SOMAS Works

### Workflow Overview

```
User creates issue → Add somas:start label → SOMAS creates branch & PR → 
Pipeline executes (5 stages) → Human reviews → Approve & merge
```

### Detailed Flow

1. **Issue Creation**
   - User creates issue using SOMAS project template
   - Describes project idea, type, and requirements
   
2. **Pipeline Trigger**
   - User adds `somas:start` label
   - GitHub Actions workflow activates
   
3. **Branch & PR Setup**
   - Creates feature branch: `somas/{issue-number}`
   - Creates draft pull request
   - Links PR to source issue
   
4. **Stage Execution**
   - Orchestrator manages pipeline stages
   - Agents execute tasks within each stage
   - Progress updates posted to issue and PR
   
5. **Human Review**
   - PR marked ready for review at staging gate
   - Owner (@scotlaclair) notified
   - Review generated code and approve
   
6. **Completion**
   - Merge approved PR
   - Close source issue
   - Deploy/use generated code

---

## Pipeline Stages

### Stage 1: Ideation

**Purpose**: Transform raw idea into structured plan

**Agent**: Planner (Codex)

**Activities**:
- Extract requirements from issue
- Define project scope and boundaries
- Break down into tasks
- Create implementation roadmap
- Identify dependencies and risks

**Output**: Project plan document (`.somas/output/plan.md`)

**Auto-proceed**: Yes

---

### Stage 2: Architecture

**Purpose**: Design system architecture

**Agent**: Architect (Codex + Gemini)

**Activities**:
- Design high-level architecture
- Define components and interactions
- Create data models
- Specify APIs and interfaces
- Document architectural decisions (ADRs)
- Select technology stack

**Output**: Architecture document (`.somas/output/architecture.md`)

**Auto-proceed**: Yes

---

### Stage 3: Implementation

**Purpose**: Generate production code and tests

**Agents**: Implementer + Tester (Copilot)

**Activities**:
- Implement all components
- Add error handling and validation
- Create comprehensive test suites
- Achieve 80%+ code coverage
- Make incremental commits

**Output**: Source code, test files

**Auto-proceed**: Yes

---

### Stage 4: Validation

**Purpose**: Ensure quality and security

**Agents**: Tester + Reviewer + Security (Copilot + Gemini)

**Activities**:
- Run complete test suite
- Verify coverage meets threshold
- Perform code quality review
- Conduct security vulnerability scan
- Validate best practices compliance
- Fix identified issues

**Output**: Test results, review reports, security assessment

**Auto-proceed**: Yes

---

### Stage 5: Staging

**Purpose**: Finalize documentation and prepare for release

**Agents**: Documenter + Reviewer (Copilot + Gemini)

**Activities**:
- Create comprehensive README
- Generate API documentation
- Write usage examples
- Create setup/deployment guides
- Final code review

**Output**: Documentation files, README

**Auto-proceed**: **No** (requires human approval)

---

## Agent System

### Agent Architecture

Each agent is a specialized AI entity with:
- **Role**: Clear identity and purpose
- **Provider**: AI system (Copilot/Gemini/Codex)
- **Instructions**: Detailed task procedures
- **Quality Standards**: Output requirements
- **Handoff Protocol**: Context for next agent

### Agent Details

#### Orchestrator
- **Provider**: GitHub Copilot
- **Role**: Pipeline coordinator
- **Responsibilities**:
  - Manage pipeline state
  - Coordinate agent handoffs
  - Handle failures and retries
  - Enforce iteration limits
  - Request human intervention when needed

#### Planner
- **Provider**: Codex
- **Role**: Requirements analyst and strategic planner
- **Responsibilities**:
  - Requirements analysis
  - Scope definition
  - Problem decomposition
  - Roadmap creation
  - Risk assessment

#### Architect
- **Provider**: Codex (design) + Gemini (review)
- **Role**: System designer
- **Responsibilities**:
  - System architecture design
  - Component definition
  - Data model design
  - API specification
  - Technology stack selection
  - ADR documentation

#### Implementer
- **Provider**: GitHub Copilot
- **Role**: Software engineer
- **Responsibilities**:
  - Code generation
  - Error handling implementation
  - Input validation
  - Incremental commits
  - Best practices adherence

#### Tester
- **Provider**: GitHub Copilot
- **Role**: QA engineer
- **Responsibilities**:
  - Test suite creation
  - 80%+ coverage achievement
  - Edge case testing
  - Integration testing
  - Bug identification

#### Reviewer
- **Provider**: Gemini Code Assist
- **Role**: Senior code reviewer
- **Responsibilities**:
  - Code quality assessment
  - Architecture compliance verification
  - Best practices checking
  - Documentation review
  - Test coverage review

#### Security
- **Provider**: Gemini Code Assist
- **Role**: Security analyst
- **Responsibilities**:
  - Vulnerability scanning
  - Input validation review
  - Authentication/authorization review
  - Secure coding verification
  - Dependency security check

#### Documenter
- **Provider**: GitHub Copilot
- **Role**: Technical writer
- **Responsibilities**:
  - README creation
  - API documentation
  - Usage examples
  - Setup guides
  - Troubleshooting guides

---

## Configuration

### Global Configuration (`.somas/config.yml`)

```yaml
system:
  name: "SOMAS Lite"
  version: "1.0.0"
  owner: "scotlaclair"

pipeline:
  trigger:
    method: "github_issue"
    label: "somas:start"
  
  stages:
    - id: "ideation"
      agents: ["planner"]
      auto_proceed: true
    # ... other stages

quality:
  test_coverage_minimum: 80
  linting_required: true

limits:
  iterations:
    per_task: 5
    per_step: 10
    per_stage: 25
    per_pipeline: 100

providers:
  github_copilot:
    role: "executor"
    tasks: ["code_generation", "tests", "documentation"]
  gemini_code_assist:
    role: "reviewer"
    tasks: ["architecture_review", "security_analysis"]
  codex:
    role: "planner"
    tasks: ["planning", "reasoning"]
```

### Customizing Configuration

You can modify:
- **Quality thresholds**: Adjust test coverage minimum
- **Iteration limits**: Change max iterations per stage
- **Stage behavior**: Enable/disable auto-proceed
- **Agent assignments**: Change which agents work on stages

---

## Project Types

### API (REST/GraphQL)

**Best For**: Backend services, web APIs

**Generated Components**:
- API endpoint handlers
- Request/response models
- Input validation
- Error handling
- API documentation (OpenAPI/Swagger)
- Integration tests

**Example Request**: "Create a REST API for managing tasks with CRUD operations"

---

### CLI Tool

**Best For**: Command-line utilities, automation scripts

**Generated Components**:
- Argument parsing
- Command handlers
- Configuration management
- Help documentation
- Unit and integration tests

**Example Request**: "Create a CLI tool for analyzing code complexity"

---

### Library

**Best For**: Reusable packages, modules

**Generated Components**:
- Public API
- Internal implementation
- Type definitions
- Comprehensive documentation
- Usage examples
- Unit tests

**Example Request**: "Create a library for parsing and validating email addresses"

---

### Web App

**Best For**: Frontend applications, user interfaces

**Generated Components**:
- Component structure
- State management
- API integration
- Styling
- Responsive design
- Component tests

**Example Request**: "Create a web app for tracking personal expenses"

---

### Script

**Best For**: One-off automation, data processing

**Generated Components**:
- Main script logic
- Configuration handling
- Error handling
- Logging
- Documentation
- Tests (where applicable)

**Example Request**: "Create a script to backup GitHub repositories"

---

## Quality Assurance

### Testing Standards

- **Minimum Coverage**: 80%
- **Test Types**: Unit, integration, end-to-end
- **Edge Cases**: Null, empty, boundary values
- **Error Paths**: Exception and error handling

### Code Quality Metrics

- **Readability**: Clear naming, appropriate comments
- **Maintainability**: Modular, DRY, SOLID principles
- **Performance**: Efficient algorithms and data structures
- **Best Practices**: Language-specific standards

### Review Process

1. **Automated Testing**: All tests must pass
2. **Coverage Check**: 80%+ coverage verified
3. **Code Review**: Gemini reviews for quality
4. **Security Scan**: Vulnerability assessment
5. **Human Review**: Final approval by owner

---

## Security

### Security Measures

1. **Input Validation**: All inputs validated and sanitized
2. **Authentication**: Secure authentication implementation
3. **Authorization**: Proper access control
4. **Data Protection**: Encryption for sensitive data
5. **Dependency Scanning**: Check for vulnerable packages
6. **Secure Coding**: Following OWASP guidelines

### Vulnerability Scanning

The Security agent scans for:
- Injection vulnerabilities (SQL, command, etc.)
- XSS vulnerabilities
- Authentication bypass
- Sensitive data exposure
- Insecure deserialization
- Using components with known vulnerabilities
- Security misconfigurations

### Security Reports

Security assessments include:
- Vulnerability severity ratings
- Exploitation scenarios
- Remediation guidance
- Secure code examples
- OWASP/CWE references

---

## Troubleshooting

### Pipeline Issues

**Issue**: Pipeline not starting after adding label

**Solutions**:
- Verify `somas:start` label is correct
- Check GitHub Actions is enabled
- Review workflow permissions
- Check for workflow syntax errors

---

**Issue**: Stage taking too long / appears stuck

**Solutions**:
- Check iteration count (may be near limit)
- Review agent logs in workflow
- Check for API rate limits
- Verify agent configuration is correct

---

**Issue**: Quality gates failing

**Solutions**:
- Review test failure messages
- Check coverage reports
- Review code quality issues
- Address security vulnerabilities
- Iterate on fixes

---

### Code Quality Issues

**Issue**: Generated code doesn't meet requirements

**Solutions**:
- Provide more detailed requirements in issue
- Add constraints and preferences
- Review and refine manually
- Add comments on PR for changes

---

**Issue**: Tests failing

**Solutions**:
- Review test output
- Check for environment issues
- Verify dependencies are installed
- Fix implementation bugs
- Re-run tests

---

## Advanced Usage

### Custom Agent Configuration

Modify agent behavior by editing `.somas/agents/*.yml`:

```yaml
agent:
  name: "Custom Agent"
  role: "Specialized Role"
  
instructions: |
  Custom instructions here...

quality_requirements:
  - "Custom requirement 1"
  - "Custom requirement 2"
```

### Custom Templates

Create custom templates in `.somas/templates/` for:
- Project plans
- Architecture documents
- Code structures
- Documentation formats

### Extending the Pipeline

Add custom stages by:
1. Defining stage in `.somas/config.yml`
2. Creating agent configuration
3. Updating workflow to invoke agent

### Integration with CI/CD

SOMAS-generated code can integrate with:
- GitHub Actions for CI/CD
- External testing services
- Deployment platforms
- Monitoring services

---

## Best Practices

### Writing Good Project Requests

✅ **Do**:
- Be specific about requirements
- Provide examples
- Specify constraints
- Mention edge cases
- Include preferred technologies

❌ **Don't**:
- Be too vague
- Omit critical requirements
- Ignore non-functional requirements
- Forget to specify project type

### Reviewing Generated Code

✅ **Do**:
- Review for correctness
- Test functionality
- Check security implications
- Verify documentation accuracy
- Validate against requirements

❌ **Don't**:
- Blindly merge without review
- Ignore test failures
- Skip security assessment
- Forget to validate edge cases

---

## Support

For issues, questions, or feature requests:
- Open an issue in the repository
- Review existing documentation
- Check troubleshooting section
- Contact @scotlaclair

---

## Contributing

Contributions to SOMAS Lite are welcome! Areas for contribution:
- Agent prompt improvements
- New agent types
- Template enhancements
- Documentation improvements
- Bug fixes

---

## Changelog

### v1.0.0 (Current)
- Initial SOMAS Lite release
- 8 specialized agents
- 5-stage pipeline
- Multi-provider AI support
- Comprehensive testing and security
- Full documentation

---

**Next Steps**: [Try your first project →](getting-started.md)
