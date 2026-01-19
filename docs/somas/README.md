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

SOMAS Lite is an autonomous development pipeline that transforms project ideas into production-ready code using AI agents. It coordinates multiple specialized AI agents (powered by GPT-5.2-Codex, Claude Opus 4.5, Claude Sonnet 4.5, GPT-5.2, Gemini 3 Pro, and Grok Code Fast 1) to handle the complete software development lifecycle.

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
# SOMAS Documentation

**Self-Sovereign Orchestrated Multi-Agent System**

An autonomous AI development pipeline that transforms project ideas into production-ready software through orchestrated AI agents.

---

## Overview

SOMAS is an AI-first Software Development Life Cycle (SDLC) that uses specialized AI agents to automate the entire development process from ideation to deployment. The system emphasizes:

- **Complete Specification** before architecture begins
- **Simulation-based optimization** for task sequencing
- **Parallel execution** where possible
- **Human gates** at critical decision points
- **Continuous learning** from historical data

---

## Pipeline Stages

### Stage 1: Ideation

**Purpose**: Transform raw idea into structured plan

**Agent**: Planner (OpenAI GPT-4)

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

**Agent**: Architect (OpenAI GPT-4 + Gemini)

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
- **Provider**: AI system (GPT-5.2-Codex, Claude Opus/Sonnet 4.5, GPT-5.2, Gemini 3 Pro, Grok Code Fast 1)
- **Instructions**: Detailed task procedures
- **Quality Standards**: Output requirements
- **Handoff Protocol**: Context for next agent

### Agent Details

#### Orchestrator
- **Provider**: Grok Code Fast 1
- **Role**: Pipeline coordinator
- **Responsibilities**:
  - Manage pipeline state
  - Coordinate agent handoffs
  - Handle failures and retries
  - Enforce iteration limits
  - Request human intervention when needed

#### Planner
- **Provider**: GPT-5.2
- **Role**: Requirements analyst and strategic planner
- **Responsibilities**:
  - Requirements analysis
  - Scope definition
  - Problem decomposition
  - Roadmap creation
  - Risk assessment

#### Architect
- **Provider**: Claude Opus 4.5
- **Role**: System designer
- **Responsibilities**:
  - System architecture design
  - Component definition
  - Data model design
  - API specification
  - Technology stack selection
  - ADR documentation

#### Implementer
- **Provider**: GPT-5.2-Codex
- **Role**: Software engineer
- **Responsibilities**:
  - Code generation
  - Error handling implementation
  - Input validation
  - Incremental commits
  - Best practices adherence

#### Tester
- **Provider**: Claude Sonnet 4.5
- **Role**: QA engineer
- **Responsibilities**:
  - Test suite creation
  - 80%+ coverage achievement
  - Edge case testing
  - Integration testing
  - Bug identification

#### Reviewer
- **Provider**: Claude Sonnet 4.5
- **Role**: Senior code reviewer
- **Responsibilities**:
  - Code quality assessment
  - Architecture compliance verification
  - Best practices checking
  - Documentation review
  - Test coverage review

#### Security
- **Provider**: GPT-5.2
- **Role**: Security analyst
- **Responsibilities**:
  - Vulnerability scanning
  - Input validation review
  - Authentication/authorization review
  - Secure coding verification
  - Dependency security check

#### Documenter
- **Provider**: Gemini 3 Pro
- **Role**: Technical writer
- **Responsibilities**:
  - README creation
  - API documentation
  - Usage examples
  - Setup guides
  - Troubleshooting guides
SOMAS executes projects through 7 sequential stages:

### Stage 1: Ideation (Order 1)
**Agent:** Planner  
**Objective:** Create a high-level plan from the project idea  
**Human Gate:** No  

Takes the project idea from an issue and produces an initial plan with:
- Problem statement
- Proposed solution approach
- High-level component breakdown
- Initial timeline estimate

### Stage 2: Specification (Order 2) ⭐ NEW
**Agent:** Specifier  
**Objective:** Produce complete, unambiguous specification document  
**Human Gate:** Yes  

Creates a comprehensive SPEC.md document with:
- **Executive Summary**
- **Functional Requirements** (enumerated, testable, with unique IDs)
- **Non-Functional Requirements** (measurable)
- **User Stories** with acceptance criteria
- **Data Dictionary** (entities, attributes, relationships)
- **API Contracts** (draft endpoints and schemas)
- **UI/UX Requirements** (if applicable)
- **Security Requirements**
- **Integration Requirements**
- **Constraints & Assumptions**
- **Glossary**
- **Open Questions** (must be resolved before approval)

**Why This Stage Matters:**
- Reduces iteration risk (spec changes don't cascade through architecture)
- Creates a human review gate for completeness
- Gives AI agents full context for subsequent stages
- Catches requirement issues earlier, reducing rework

**Quality Gates:**
- ✅ All requirements have unique IDs
- ✅ All requirements are testable
- ✅ No ambiguous language (TBD, maybe, etc.)
- ✅ Open questions resolved or escalated

### Stage 3: Simulation (Order 3) ⭐ NEW
**Agent:** Simulator  
**Objective:** Determine optimal task sequencing through Monte Carlo simulation  
**Human Gate:** No  

Analyzes the specification and produces:
- **Task Dependency Graph** (DAG)
- **Duration Estimates** (optimistic, most likely, pessimistic)
- **Monte Carlo Simulation Results** (1000 iterations)
- **Critical Path** identification
- **Parallel Execution Phases**
- **High-Risk Tasks** with mitigations
- **Optimal Execution Plan**

**Outputs:**
- `execution_plan.yml` - Detailed execution strategy
- `task_graph.yml` - Task dependency visualization data

**Benefits:**
- Identifies critical path and parallelization opportunities
- Predicts completion times with confidence intervals
- Optimizes task sizing based on historical data
- Reduces total pipeline duration by 40-60%

### Stage 4: Architecture (Order 4)
**Agent:** Architect  
**Objective:** Design system architecture  
**Human Gate:** No  

Creates architectural design documents:
- Component diagrams
- Data models
- API specifications
- Technology stack decisions
- Deployment architecture

### Stage 5: Implementation (Order 5)
**Agent:** Coder  
**Objective:** Write production-ready code  
**Human Gate:** No  

Implements the system according to:
- Architecture specifications
- Task execution plan
- Quality standards
- Security requirements

Follows the optimized task sequence from simulation.

### Stage 6: Validation (Order 6)
**Agent:** Validator  
**Objective:** Comprehensive testing and validation  
**Human Gate:** No  

Performs:
- Unit testing
- Integration testing
- Performance testing
- Security scanning
- Acceptance criteria verification

### Stage 7: Staging (Order 7)
**Agent:** Deployer  
**Objective:** Deploy to staging environment  
**Human Gate:** Yes  

Prepares and deploys:
- Staging environment setup
- Deployment scripts
- Documentation
- Monitoring setup

Final human review before production deployment.

---

## Agent Roles

### Specifier
**Provider:** Codex  
**Purpose:** Creates detailed, unambiguous specifications

**Capabilities:**
- Requirements extraction and enumeration
- User story creation with acceptance criteria
- Data structure definition
- API contract drafting
- Ambiguity detection and resolution

**Quality Checks:**
- Testability validation
- Ambiguity detection (flags "TBD", "maybe", etc.)
- Completeness verification
- Unique ID enforcement

### Simulator
**Provider:** Codex  
**Purpose:** Optimizes task execution through simulation

**Capabilities:**
- Task graph construction from specifications
- Duration estimation (PERT distribution)
- Monte Carlo simulation (1000 iterations)
- Critical path analysis
- Parallelization opportunity identification
- Task decomposition recommendations

**Outputs:**
- Completion time statistics (mean, P90, confidence intervals)
- Critical path with probabilities
- High-risk tasks with mitigations
- Optimal execution plan with parallel phases

---

## Optimization Features

### 1. Simulation-Based Planning ⭐ NEW

The simulator uses Monte Carlo analysis to determine optimal task sequencing:

**Process:**
1. **Build Task Graph** - Extract tasks and dependencies from SPEC.md
2. **Estimate Durations** - Use PERT distribution (optimistic, likely, pessimistic)
3. **Run Simulation** - 1000 iterations sampling from distributions
4. **Analyze Results** - Mean, P90, critical path frequency
5. **Identify Parallelization** - Find tasks with no mutual dependencies
6. **Optimize Sizing** - Recommend splitting large/uncertain tasks
7. **Output Plan** - Execution strategy with phases and assignments

**Benefits:**
- Predicts completion time with 90% confidence intervals
- Identifies bottlenecks before they occur
- Optimizes team allocation
- Reduces project risk through early decomposition

### 2. GitHub Project Integration ⭐ NEW

Automatic integration with GitHub Projects for visual tracking:

**Features:**
- Creates project board when pipeline starts
- Creates issues for each task/component
- Moves cards between columns as stages progress
- Updates custom fields with metrics
- Links issues to PRs automatically
- Tracks time in each stage

**Project Columns:**
- 📋 Backlog
- 📝 Specification
- 🔬 Simulation
- 🏗️ Architecture
- 💻 Implementation
- ✅ Validation
- 👤 Human Review
- 🚀 Done

**Tracked Metrics:**
- Time in stage
- Iteration count
- Blocker duration
- Human wait time
- Estimation accuracy

### 3. Analytics & Learning

Continuous learning from historical data:

**Collected Metrics:**
- Task duration vs. estimate
- Iteration count by task type
- Parallel execution efficiency
- Critical path prediction accuracy
- Human intervention frequency

**Learning Models:**
- **Duration Estimator** - Predicts task durations based on features
- **Critical Path Predictor** - Identifies which tasks will be critical

**Data Schema:** See `.somas/analytics/schema.yml`

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
    tasks: ["code_generation", "tests", "documentation", "pr_creation"]
  gemini_code_assist:
    role: "reviewer"
    tasks: ["architecture_review", "security_analysis", "code_quality"]
  openai_gpt4:
    role: "planner"
    tasks: ["planning", "reasoning", "problem_decomposition"]
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
Main configuration file: `.somas/config.yml`

### Key Configuration Sections:

#### Optimization Settings
```yaml
optimization:
  simulation:
    enabled: true
    method: "monte_carlo"
    iterations: 1000
    rerun_on_spec_change: true
    
  parallelization:
    enabled: true
    max_concurrent_tasks: 5
    respect_dependencies: true
    
  adaptive_sizing:
    enabled: true
    target_task_duration_minutes: 240  # 4 hours
    auto_decompose: true
```

#### Project Management
```yaml
project_management:
  enabled: true
  github_project:
    create_per_pipeline: true
    template: "SOMAS Pipeline"
    task_decomposition:
      create_issues_for: "each_component"
      link_to_parent: true
```

#### Analytics
```yaml
analytics:
  enabled: true
  storage: ".somas/analytics/runs/"
  retention_days: 90
  track:
    - "task_duration_vs_estimate"
    - "iteration_count_by_task_type"
    - "parallel_efficiency"
```

---

## Workflow Files

### `.github/workflows/somas-pipeline.yml`
Main pipeline execution workflow:
- Triggers on issue creation with `somas-project` label
- Executes all 7 stages sequentially
- Records metrics after completion
- Handles human gates

### `.github/workflows/somas-project-sync.yml`
GitHub Project synchronization:
- Creates project boards
- Creates task issues from execution plan
- Moves cards between columns
- Updates project status
- Records project events

---

## Human Gates

Human intervention points for critical decisions:

### Specification Stage (Gate 1)
**When:** After SPEC.md is created  
**Purpose:** Verify completeness and correctness of specification  
**Owner:** @scotlaclair  

**Review Checklist:**
- [ ] All requirements are clear and testable
- [ ] No ambiguous language
- [ ] Security requirements adequate
- [ ] Open questions resolved
- [ ] Scope is appropriate

### Staging Stage (Gate 2)
**When:** Before production deployment  
**Purpose:** Final validation before release  
**Owner:** @scotlaclair  

**Review Checklist:**
- [ ] All tests passing
- [ ] Performance requirements met
- [ ] Security scan passed
- [ ] Documentation complete
- [ ] Deployment plan reviewed

---

## Directory Structure

```
.somas/
├── config.yml                      # Main configuration
├── stages/                         # Stage definitions
│   ├── specification.yml           # NEW: Specification stage
│   ├── simulation.yml              # NEW: Simulation stage
│   └── ...
├── agents/                         # Agent configurations
│   ├── specifier.yml               # NEW: Specifier agent
│   ├── simulator.yml               # NEW: Simulator agent
│   └── ...
├── templates/                      # Document templates
│   ├── SPEC.md                     # NEW: Specification template
│   ├── execution_plan.yml          # NEW: Execution plan template
│   └── ...
├── analytics/                      # Analytics data
│   ├── schema.yml                  # NEW: Analytics schema
│   └── runs/                       # Run data storage
└── projects/                       # Active projects
    └── {project_id}/
        ├── artifacts/              # Stage outputs
        ├── logs/                   # Execution logs
        └── metadata.json           # Project metadata

.github/
├── workflows/
│   ├── somas-pipeline.yml          # UPDATED: 7-stage pipeline
│   └── somas-project-sync.yml      # NEW: Project sync
└── project-template.yml            # NEW: Project template

docs/
└── somas/
    ├── README.md                   # This file
    └── optimization-guide.md       # NEW: Optimization guide
```

---

## Getting Started

### 1. Create a New Project

Create a GitHub issue with:
- Label: `somas-project`
- Title: Your project name
- Description: Project idea and requirements

### 2. Pipeline Execution

The pipeline will automatically:
1. **Ideation** - Create initial plan
2. **Specification** - Generate SPEC.md (requires your approval)
3. **Simulation** - Optimize task sequence
4. **Architecture** - Design system
5. **Implementation** - Write code
6. **Validation** - Test everything
7. **Staging** - Deploy for review (requires your approval)

### 3. Track Progress

View progress on:
- **GitHub Project Board** - Visual task tracking
- **Pipeline Workflow** - Stage completion status
- **Analytics Dashboard** - Performance metrics

### 4. Review & Approve

You'll be notified at human gates:
- **After Specification** - Review and approve SPEC.md
- **After Staging** - Review and approve deployment

---

## Best Practices

### For Specifications
- Be specific and avoid ambiguous language
- Define all requirements with acceptance criteria
- Resolve all open questions before approval
- Include security requirements upfront

### For Simulation
- Provide accurate complexity estimates
- Review high-risk tasks and mitigations
- Consider parallelization recommendations
- Re-run if specification changes significantly

### For Project Management
- Keep issues updated with actual progress
- Record actual durations for learning
- Document reasons for iterations
- Note when human intervention was needed

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
### Specification Not Approved
- Check for ambiguous language (TBD, maybe, etc.)
- Ensure all requirements have unique IDs
- Verify all open questions are resolved
- Confirm security requirements are complete

### Simulation Issues
- Verify SPEC.md is complete and well-formed
- Check for circular dependencies in requirements
- Ensure task complexity estimates are reasonable
- Review historical data quality

### Pipeline Failures
- Check workflow logs for error details
- Verify all required secrets are configured
- Ensure human gates are not timing out
- Review quality gate criteria

---

## Further Reading

- [Optimization Guide](./optimization-guide.md) - Detailed optimization techniques
- [Configuration Reference](./.somas/config.yml) - Full configuration options
- [Analytics Schema](./.somas/analytics/schema.yml) - Metrics and data structure
- [Agent Configurations](./.somas/agents/) - Individual agent settings

---

## Support

For issues, questions, or feature requests:
- Open an issue in the repository
- Review existing documentation
- Check troubleshooting section
- Contact the repository owner

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
For issues or questions:
- **Owner:** @scotlaclair
- **Repository:** github.com/scotlaclair/SOMAS
- **Documentation:** /docs/somas/

---

*Last Updated: 2026*
