# SOMAS GitHub Copilot Agents

## Overview

The SOMAS (Self-Sovereign Orchestrated Multi-Agent System) uses a team of **12 specialized GitHub Copilot agents** to orchestrate the entire software development lifecycle. Each agent is purpose-built for specific stages or cross-cutting concerns, enabling autonomous, AI-driven development from ideation to deployment.

### Agent Team Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SOMAS Agent Ecosystem                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Pipeline Agents (7):          Cross-Stage Agents (4):     │
│  ├─ Planner         [Ideation]      ├─ Reviewer            │
│  ├─ Specifier   [Specification]    ├─ Orchestrator         │
│  ├─ Simulator      [Simulation]    ├─ Documenter           │
│  ├─ Architect    [Architecture]    ├─ Security             │
│  ├─ Implementer  [Implementation]  │                        │
│  ├─ Tester        [Validation]     Strategic Agent (1):    │
│  └─ Deployer         [Staging]     └─ Advisor (o1-preview) │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Design Philosophy:**
- **Specialized Expertise**: Each agent focuses on one domain
- **Sequential Handoffs**: Pipeline agents pass artifacts stage-to-stage
- **Parallel Reviews**: Cross-stage agents work concurrently
- **Model Optimization**: GPT-4o for execution, o1-preview for strategy

---

## Complete Agent Catalog

### Pipeline Agents (Sequential Execution)

#### 1. **@somas-planner** - Ideation Agent
- **Stage**: Ideation (Stage 1)
- **Model**: GPT-4o
- **Role**: Transform rough ideas into structured project plans
- **Invocation**: `@somas-planner create initial plan for [project idea]`
- **Inputs**: 
  - Project idea (from issue description)
  - User requirements and constraints
- **Outputs**: 
  - `initial_plan.yml` - Structured project plan
  - High-level feature breakdown
  - Technology stack recommendations
  - Risk assessment
- **Agent File**: `.somas/agents/planner.yml`
- **Best Used For**: 
  - New project kickoffs
  - Feature planning
  - Feasibility analysis

**Example Usage:**
```markdown
@somas-planner create initial plan for a real-time chat application 
with end-to-end encryption, supporting 10,000 concurrent users
```

---

#### 2. **@somas-specifier** - Specification Agent
- **Stage**: Specification (Stage 2)
- **Model**: GPT-4o
- **Role**: Create complete, unambiguous specifications from project plans
- **Invocation**: `@somas-specifier generate SPEC.md from initial_plan.yml`
- **Inputs**:
  - `initial_plan.yml` (from Planner)
  - Stakeholder feedback (issue comments)
- **Outputs**:
  - `SPEC.md` - Complete specification document
    - Functional requirements (REQ-F-XXX)
    - Non-functional requirements (REQ-NF-XXX)
    - User stories with acceptance criteria
    - Data dictionary
    - API contracts
- **Agent File**: `.somas/agents/specifier.yml`
- **Best Used For**:
  - Detailed requirement documentation
  - API design
  - Data modeling

**Example Usage:**
```markdown
@somas-specifier review SPEC.md and add detailed error handling requirements 
for authentication flows
```

---

#### 3. **@somas-simulator** - Simulation Agent
- **Stage**: Simulation (Stage 3)
- **Model**: GPT-4o
- **Role**: Optimize development execution through Monte Carlo simulation
- **Invocation**: `@somas-simulator run optimization on SPEC.md`
- **Inputs**:
  - `SPEC.md` (from Specifier)
  - Historical analytics (`.somas/analytics/`)
- **Outputs**:
  - `execution_plan.yml` - Optimized task sequence
    - Task breakdown with duration estimates
    - Dependency graph
    - Risk-adjusted timelines (1000 iterations, 90% CI)
    - Parallelization strategy
- **Agent File**: `.somas/agents/simulator.yml`
- **Best Used For**:
  - Project scheduling
  - Resource allocation
  - Risk quantification

**Configuration:**
```yaml
optimization:
  simulation:
    method: "monte_carlo"
    iterations: 1000
    confidence_interval: 0.90
```

**Example Usage:**
```markdown
@somas-simulator recalculate execution plan with increased risk multiplier 
for external API integrations
```

---

#### 4. **@somas-architect** - Architecture Agent
- **Stage**: Architecture (Stage 4)
- **Model**: GPT-4o
- **Role**: Design system architecture and detailed technical specifications
- **Invocation**: `@somas-architect design architecture from SPEC.md`
- **Inputs**:
  - `SPEC.md` (from Specifier)
  - `execution_plan.yml` (from Simulator)
- **Outputs**:
  - `ARCHITECTURE.md` - System design document
    - Component diagrams
    - Technology stack with justifications
    - Database schema
    - API endpoint definitions
    - Security architecture
    - Deployment topology
- **Agent File**: `.somas/agents/architect.yml`
- **Best Used For**:
  - System design decisions
  - Technology selection
  - Scalability planning

**Example Usage:**
```markdown
@somas-architect evaluate microservices vs monolithic architecture 
for this system, considering the 10K user requirement
```

---

#### 5. **@somas-implementer** - Implementation Agent
- **Stage**: Implementation (Stage 5)
- **Model**: GPT-4o
- **Role**: Generate production-ready source code
- **Invocation**: `@somas-implementer implement [component] from ARCHITECTURE.md`
- **Inputs**:
  - `ARCHITECTURE.md` (from Architect)
  - `execution_plan.yml` task definitions
  - Code templates (`.somas/templates/`)
- **Outputs**:
  - Source code files
  - Unit tests
  - Integration tests
  - Configuration files
  - Documentation comments
- **Agent File**: `.somas/agents/implementer.yml`
- **Best Used For**:
  - Writing new features
  - Refactoring existing code
  - Bug fixes

**Example Usage:**
```markdown
@somas-implementer generate the WebSocket handler with connection pooling 
as specified in ARCHITECTURE.md section 4.2
```

---

#### 6. **@somas-tester** - Testing Agent
- **Stage**: Validation (Stage 6)
- **Model**: GPT-4o
- **Role**: Comprehensive testing and quality validation
- **Invocation**: `@somas-tester validate implementation against SPEC.md`
- **Inputs**:
  - Source code (from Implementer)
  - `SPEC.md` requirements
  - Test templates (`.somas/templates/test_plan.yml`)
- **Outputs**:
  - `TEST_REPORT.md` - Test results
    - Unit test coverage (target: >80%)
    - Integration test results
    - Performance benchmarks
    - Security scan results
    - Requirement traceability matrix
- **Agent File**: `.somas/agents/tester.yml`
- **Best Used For**:
  - Test coverage analysis
  - Performance testing
  - Regression testing

**Example Usage:**
```markdown
@somas-tester run load tests for 10,000 concurrent WebSocket connections 
and report results
```

---

#### 7. **@somas-deployer** - Deployment Agent
- **Stage**: Staging (Stage 7)
- **Model**: GPT-4o
- **Role**: Prepare deployment artifacts and infrastructure
- **Invocation**: `@somas-deployer prepare staging deployment`
- **Inputs**:
  - Validated code (from Tester)
  - `ARCHITECTURE.md` deployment specs
- **Outputs**:
  - `DEPLOYMENT_GUIDE.md`
  - Infrastructure as Code (Terraform/CloudFormation)
  - CI/CD pipeline configurations
  - Container definitions (Dockerfile, docker-compose.yml)
  - Environment configurations
- **Agent File**: `.somas/agents/deployer.yml`
- **Best Used For**:
  - Infrastructure provisioning
  - CI/CD setup
  - Environment configuration

**Example Usage:**
```markdown
@somas-deployer generate Kubernetes manifests for staging environment 
with horizontal pod autoscaling
```

---

### Cross-Stage Agents (Parallel Execution)

#### 8. **@somas-reviewer** - Code Review Agent
- **Stage**: All stages (cross-cutting)
- **Model**: GPT-4o
- **Role**: Provide expert code reviews and quality feedback
- **Invocation**: `@somas-reviewer review this PR`
- **Scope**:
  - Code quality and best practices
  - Security vulnerabilities
  - Performance concerns
  - Architectural alignment
  - Test coverage
- **Agent File**: `.somas/agents/reviewer.yml`
- **Best Used For**:
  - Pull request reviews
  - Architecture decision validation
  - Pre-merge quality checks

**Example Usage:**
```markdown
@somas-reviewer focus on security implications of the new authentication flow
```

---

#### 9. **@somas-orchestrator** - Pipeline Orchestration Agent
- **Stage**: All stages (cross-cutting)
- **Model**: GPT-4o
- **Role**: Coordinate agent handoffs and manage pipeline state
- **Invocation**: `@somas-orchestrator advance to next stage`
- **Responsibilities**:
  - Stage transition validation
  - Artifact verification
  - Human gate management
  - Error recovery
  - Progress tracking
- **Agent File**: `.somas/agents/orchestrator.yml`
- **Best Used For**:
  - Pipeline troubleshooting
  - Stage status checks
  - Manual stage advancement

**Example Usage:**
```markdown
@somas-orchestrator check if all stage 4 artifacts are complete and ready 
for implementation
```

---

#### 10. **@somas-documenter** - Documentation Agent
- **Stage**: All stages (cross-cutting)
- **Model**: GPT-4o
- **Role**: Generate and maintain comprehensive documentation
- **Invocation**: `@somas-documenter update docs for [feature]`
- **Outputs**:
  - User documentation
  - API documentation
  - Developer guides
  - README files
  - Inline code comments
  - Architecture Decision Records (ADRs)
- **Agent File**: `.somas/agents/documenter.yml`
- **Best Used For**:
  - User manual creation
  - API reference generation
  - Onboarding documentation

**Example Usage:**
```markdown
@somas-documenter create API documentation for all WebSocket endpoints 
with curl examples
```

---

#### 11. **@somas-security** - Security Agent
- **Stage**: All stages (cross-cutting)
- **Model**: GPT-4o
- **Role**: Security analysis, threat modeling, and vulnerability assessment
- **Invocation**: `@somas-security analyze [component] for vulnerabilities`
- **Analysis Areas**:
  - Input validation
  - Authentication/authorization
  - Data encryption
  - SQL injection, XSS, CSRF
  - Dependency vulnerabilities
  - Secret management
- **Agent File**: `.somas/agents/security.yml`
- **Best Used For**:
  - Security audits
  - Threat modeling
  - Penetration testing guidance

**Example Usage:**
```markdown
@somas-security perform threat model analysis for the chat message encryption system
```

---

### Strategic Agent

#### 12. **@somas-advisor** - Strategic Advisor
- **Stage**: Meta-level (cross-cutting)
- **Model**: **o1-preview** (Advanced reasoning)
- **Role**: High-level strategic guidance and complex problem-solving
- **Invocation**: `@somas-advisor evaluate [strategic decision]`
- **Use Cases**:
  - Technology stack selection
  - Architectural pattern evaluation
  - Risk vs. benefit analysis
  - Trade-off decisions (e.g., performance vs. maintainability)
  - Complex debugging strategies
- **Agent File**: `.somas/agents/advisor.yml`
- **When to Use**:
  - Critical architectural decisions
  - Deadlock resolution
  - Unexpected technical challenges
  - Multi-agent coordination issues

**Why o1-preview?**
- Extended reasoning capability for complex decisions
- Better at exploring solution spaces
- Excels at multi-step logical analysis

**Example Usage:**
```markdown
@somas-advisor should we use event sourcing or traditional CRUD for this chat 
system? Consider scalability, debugging complexity, and team expertise.
```

---

## How to Use Custom Agents

### In GitHub Issues

**Single Agent Invocation:**
```markdown
@somas-planner create an initial plan for a task management system 
with Kanban boards and time tracking
```

**Sequential Handoff:**
```markdown
1. @somas-planner create initial plan
2. (Wait for plan artifact)
3. @somas-specifier generate SPEC.md from the plan
4. @somas-simulator optimize execution plan
```

**Parallel Reviews:**
```markdown
@somas-reviewer @somas-security @somas-documenter 

Please review the authentication implementation in PR #123
```

---

### In Pull Requests

**Code Review:**
```markdown
@somas-reviewer please review this PR with focus on:
- Error handling patterns
- Test coverage
- Performance implications
```

**Security Audit:**
```markdown
@somas-security audit this authentication flow for vulnerabilities
```

**Documentation Generation:**
```markdown
@somas-documenter generate API documentation for the new endpoints 
added in this PR
```

---

### In GitHub Actions Workflows

**Workflow Integration:**
```yaml
name: SOMAS Pipeline - Stage 3

on:
  workflow_dispatch:
    inputs:
      project_id:
        required: true
        
jobs:
  simulation:
    runs-on: ubuntu-latest
    steps:
      - name: Invoke Simulator Agent
        run: |
          gh issue comment ${{ github.event.issue.number }} \
            --body "@somas-simulator run optimization on SPEC.md"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          
      - name: Wait for Simulation Results
        # Poll for execution_plan.yml artifact
        
      - name: Validate Results
        run: |
          if [ ! -f "projects/$PROJECT_ID/artifacts/execution_plan.yml" ]; then
            echo "❌ Simulation failed to produce execution plan"
            exit 1
          fi
```

---

## Agent Interaction Patterns

### 1. Sequential Handoffs (Pipeline Agents)

```
Planner → Specifier → Simulator → Architect → Implementer → Tester → Deployer
```

**Pattern:**
1. Agent N completes work, stores artifact
2. Orchestrator validates artifact
3. Agent N+1 reads artifact, begins work

**Example:**
```markdown
# Issue: Create chat application

Comment 1: @somas-planner create initial plan
→ Produces: initial_plan.yml

Comment 2: @somas-specifier generate SPEC.md from initial_plan.yml
→ Produces: SPEC.md

Comment 3: @somas-simulator run optimization on SPEC.md
→ Produces: execution_plan.yml
```

---

### 2. Parallel Reviews (Cross-Stage Agents)

```
                    ┌─→ Reviewer
Implementation PR ──┼─→ Security
                    └─→ Documenter
```

**Pattern:**
All agents invoked simultaneously, work independently

**Example:**
```markdown
@somas-reviewer @somas-security @somas-documenter

PR #45 implements WebSocket authentication. Please review from your 
respective areas of expertise.
```

---

### 3. Advisor Consultation Pattern

```
Agent encounters complex decision → Consult Advisor → Agent proceeds with guidance
```

**Example:**
```markdown
# During Architecture Stage

@somas-architect I'm designing the message queue system.

@somas-advisor Should I use:
A) RabbitMQ with priority queues
B) Kafka for event streaming
C) Redis Pub/Sub for simplicity

Context: 10K concurrent users, message ordering critical, 
moderate persistence requirements.

(Advisor provides analysis)

@somas-architect proceed with option B (Kafka) as recommended by advisor
```

---

### 4. Error Recovery Pattern

```
Stage fails → Orchestrator detects → Human reviews → Orchestrator retries
```

**Example:**
```markdown
@somas-orchestrator 

Stage 5 (Implementation) failed due to missing dependencies in ARCHITECTURE.md.

@somas-architect please update section 3.2 with Redis configuration details

@somas-orchestrator retry stage 5 after architect updates
```

---

## Integration with SOMAS Configuration

All agents are configured through:

### 1. Main Configuration (`.somas/config.yml`)

```yaml
agents:
  providers:
    copilot:
      model: "gpt-4o"
      temperature: 0.3  # Lower = more deterministic
      max_tokens: 4000
      
  agent_configs:
    planner:
      provider: "copilot"
      config_file: ".somas/agents/planner.yml"
    # ... other agents
```

### 2. Individual Agent Files (`.somas/agents/*.yml`)

```yaml
# Example: .somas/agents/specifier.yml
specifier:
  id: "specifier"
  version: "1.0.0"
  provider: "copilot"
  
  prompt:
    role: |
      You are the SOMAS Specifier...
      
    instructions: |
      ## SPECIFICATION CREATION PROTOCOL
      1. ANALYZE INPUT...
      
    output_format:
      file: "SPEC.md"
      template: ".somas/templates/specification.md"
```

### 3. Stage Definitions (`.somas/stages/*.yml`)

```yaml
# Example: .somas/stages/specification.yml
specification:
  id: "specification"
  order: 2
  agent: "specifier"
  
  inputs:
    - "initial_plan.yml"
    
  outputs:
    - "SPEC.md"
    
  quality_gates:
    - all_requirements_have_ids: true
    - all_user_stories_have_acceptance_criteria: true
```

---

## Model Selection Rationale

### GPT-4o for 11 Agents

**Why GPT-4o?**
- **Speed**: 2x faster than GPT-4 Turbo
- **Cost**: 50% cheaper per token
- **Quality**: Same capabilities for structured tasks
- **Multimodal**: Handles code, diagrams, documentation

**Optimal For:**
- Code generation (Implementer)
- Structured document creation (Specifier, Architect)
- Pattern recognition (Reviewer, Security)
- Simulation calculations (Simulator)

**Temperature Settings:**
- `0.1-0.3`: Code generation (deterministic)
- `0.3-0.5`: Documentation (balanced)
- `0.5-0.7`: Planning/ideation (creative)

---

### o1-preview for Advisor

**Why o1-preview?**
- **Extended Reasoning**: 10x more compute for complex decisions
- **Multi-Step Analysis**: Evaluates trade-offs systematically
- **Solution Space Exploration**: Considers alternatives thoroughly

**Use Sparingly:**
- ~10x cost of GPT-4o
- Slower response time
- Only for strategic, high-impact decisions

**Examples of Advisor-Worthy Questions:**
- "Should we rewrite this module in Rust for performance?"
- "How do we handle distributed transactions across 5 microservices?"
- "What's the best caching strategy for this data access pattern?"

---

## Best Practices

### Agent Selection

✅ **DO:**
- Use pipeline agents sequentially in order
- Invoke cross-stage agents in parallel for reviews
- Consult Advisor for strategic decisions only
- Let Orchestrator manage stage transitions

❌ **DON'T:**
- Skip pipeline stages (breaks artifact chain)
- Use Advisor for routine tasks (cost/speed)
- Invoke agents without providing necessary context
- Manually manage stage transitions (let Orchestrator handle)

---

### Invocation Patterns

**Good:**
```markdown
@somas-implementer implement the WebSocket handler defined in 
ARCHITECTURE.md section 4.2, following the error handling patterns 
in .somas/patterns/error-handling.yml
```

**Bad:**
```markdown
@somas-implementer make websocket stuff
```

**Key Principles:**
1. **Be Specific**: Reference exact files/sections
2. **Provide Context**: Link to specs, requirements, constraints
3. **Set Scope**: Define what should/shouldn't be included
4. **Reference Patterns**: Point to templates/examples

---

### Context Provision

Agents work best with:
- **Explicit Inputs**: File paths, section numbers
- **Clear Constraints**: Performance targets, security requirements
- **Success Criteria**: How to measure completion
- **Related Work**: Links to related issues, PRs, docs

**Example:**
```markdown
@somas-architect design database schema for the chat system.

Requirements:
- Support 10K concurrent connections (SPEC.md REQ-NF-002)
- Message retention: 30 days
- Full-text search on messages
- Horizontal scalability

Constraints:
- Use PostgreSQL (existing infrastructure)
- Budget: $500/month
- Data residency: EU

Reference:
- Existing schema: projects/project-001/db/schema.sql
- Similar project: projects/project-003/ARCHITECTURE.md
```

---

## Security Considerations

### Agent Permissions

All agents operate with:
- **Read Access**: Repository code, issues, PRs
- **Write Access**: Comments, artifacts (via commits)
- **No Secrets Access**: Cannot read GitHub Secrets directly

**Security Pattern:**
```yaml
# Workflows pass secrets to agents indirectly
jobs:
  deploy:
    steps:
      - name: Prepare Config
        run: |
          # Python handles secret injection (safe from injection)
          python3 << 'PYTHON'
          import os
          config = {
            'api_key': os.environ['API_KEY']  # From GitHub Secrets
          }
          # Agent sees config file, not secret directly
          PYTHON
        env:
          API_KEY: ${{ secrets.API_KEY }}
```

---

### Input Validation

Agents must validate:
- **Project IDs**: Prevent path traversal
- **File Paths**: Sanitize before operations
- **User Input**: Validate against expected formats

**Example from Copilot Instructions:**
```python
# @copilot-example: Always validate project IDs
import re

def validate_project_id(project_id):
    if not re.match(r'^project-\d+$', project_id):
        raise ValueError("Invalid project ID format")
    return project_id
```

---

### Sensitive Data

**Agent Restrictions:**
1. Never log secrets or credentials
2. Redact sensitive data in comments
3. Use environment variables for configuration
4. Validate all outputs before committing

---

## Troubleshooting

### Common Issues

#### Agent Not Responding

**Symptoms:** Agent mention doesn't trigger action

**Solutions:**
1. Check agent name: `@somas-planner` (not `@planner`)
2. Verify agent exists: See `.github/agents/` directory
3. Check permissions: Agent must have repo access
4. Review invocation syntax: Include clear instructions

---

#### Wrong Artifact Generated

**Symptoms:** Agent produces unexpected output format

**Solutions:**
1. Check template: `.somas/templates/[stage].md`
2. Verify agent config: `.somas/agents/[agent].yml`
3. Provide explicit format requirements in invocation
4. Review agent's `output_format` section

---

#### Stage Won't Advance

**Symptoms:** Orchestrator blocks progression

**Solutions:**
1. Validate artifacts exist:
   ```bash
   ls -la projects/[project-id]/artifacts/
   ```
2. Check quality gates: `.somas/stages/[stage].yml`
3. Review stage completion criteria
4. Ask Orchestrator for status:
   ```markdown
   @somas-orchestrator report status of stage [N]
   ```

---

#### Simulation Results Unrealistic

**Symptoms:** Execution plan has impossible timelines

**Solutions:**
1. Review risk multipliers: `.somas/config.yml`
2. Check historical data: `.somas/analytics/runs/`
3. Provide task complexity hints to Simulator
4. Adjust confidence interval (increase iterations)

---

### Debug Commands

```markdown
# Check pipeline state
@somas-orchestrator show current pipeline status

# Validate artifacts
@somas-orchestrator verify all stage [N] artifacts

# Review agent configuration
@somas-orchestrator show configuration for [agent-name]

# Get agent help
@somas-[agent-name] help

# Request strategic guidance
@somas-advisor diagnose why stage [N] is failing
```

---

## Related Documentation

### Agent Configuration
- **Base Agent Config**: `.somas/agents/_base.yml`
- **Pipeline Agents**: `.somas/agents/{planner,specifier,simulator,architect,implementer,tester,deployer}.yml`
- **Cross-Stage Agents**: `.somas/agents/{reviewer,orchestrator,documenter,security}.yml`
- **Strategic Agent**: `.somas/agents/advisor.yml`

### Pipeline Configuration
- **Main Config**: `.somas/config.yml`
- **Stage Definitions**: `.somas/stages/*.yml`
- **Workflow Templates**: `.github/workflows/somas-*.yml`

### Templates
- **Specification**: `.somas/templates/specification.md`
- **Architecture**: `.somas/templates/architecture.md`
- **Execution Plan**: `.somas/templates/execution_plan.yml`
- **Test Plan**: `.somas/templates/test_plan.yml`

### Patterns
- **Error Handling**: `.somas/patterns/error-handling.yml`
- **Security**: `.somas/patterns/security.yml`
- **Testing**: `.somas/patterns/testing.yml`

### Documentation
- **SOMAS Overview**: `docs/somas/README.md`
- **Optimization Guide**: `docs/somas/optimization-guide.md`
- **Troubleshooting**: `docs/somas/TROUBLESHOOTING.md`
- **Copilot Instructions**: `.github/copilot-instructions.md`

---

## Examples

### Complete Pipeline Execution

```markdown
# Issue #100: Build a REST API for user management

## Stage 1: Ideation
@somas-planner create initial plan for a REST API supporting CRUD operations 
on users, with JWT authentication

→ Artifact: projects/project-100/artifacts/initial_plan.yml

## Stage 2: Specification  
@somas-specifier generate SPEC.md from initial_plan.yml, include detailed 
API contracts and validation rules

→ Artifact: projects/project-100/artifacts/SPEC.md

## Stage 3: Simulation
@somas-simulator run optimization on SPEC.md

→ Artifact: projects/project-100/artifacts/execution_plan.yml

## Stage 4: Architecture
@somas-architect design architecture from SPEC.md, use PostgreSQL for 
persistence and Redis for session caching

→ Artifact: projects/project-100/artifacts/ARCHITECTURE.md

## Stage 5: Implementation
@somas-implementer implement Task-001 from execution_plan.yml 
(User model and repository)

→ Commit: User model with validation

@somas-implementer implement Task-002 (Authentication middleware)

→ Commit: JWT middleware

## Stage 6: Validation
@somas-tester validate implementation against SPEC.md requirements 
REQ-F-001 through REQ-F-010

→ Artifact: projects/project-100/artifacts/TEST_REPORT.md

## Stage 7: Staging
@somas-deployer prepare Docker containerization and Kubernetes manifests

→ Artifacts: Dockerfile, k8s/*.yml
```

---

### Cross-Stage Review

```markdown
# PR #45: Implement WebSocket authentication

@somas-reviewer @somas-security @somas-documenter

Please review this PR:

**Reviewer**: Check code quality, error handling, test coverage
**Security**: Audit authentication flow for vulnerabilities  
**Documenter**: Generate API docs for new WebSocket endpoints

Context:
- Spec: projects/project-100/artifacts/SPEC.md (REQ-F-015 to REQ-F-020)
- Architecture: projects/project-100/artifacts/ARCHITECTURE.md (Section 5)
```

---

### Advisor Consultation

```markdown
# Issue #100, Comment during Architecture Stage

@somas-advisor I need strategic guidance on message queue selection.

**Context:**
- Real-time chat application
- 10,000 concurrent users
- Message ordering is critical
- Need message persistence for 30 days
- Budget: $500/month cloud costs

**Options:**
1. RabbitMQ with durable queues + priority queues
2. Apache Kafka for event streaming + replay capability
3. Redis Pub/Sub with Redis Streams for persistence
4. AWS SQS + DynamoDB for simplicity

**Trade-offs:**
- Operational complexity vs. features
- Cost vs. scalability
- Learning curve for team (3 junior devs, 1 senior)

**Question:** Which option best balances our requirements, constraints, 
and team capabilities?

(Advisor provides multi-step analysis)

@somas-architect proceed with Kafka as recommended, focusing on 
recommended configuration from advisor
```

---

## Quick Reference

| Agent | Invocation | Primary Use | Model |
|-------|-----------|-------------|-------|
| Planner | `@somas-planner` | Project planning | GPT-4o |
| Specifier | `@somas-specifier` | Requirement docs | GPT-4o |
| Simulator | `@somas-simulator` | Task optimization | GPT-4o |
| Architect | `@somas-architect` | System design | GPT-4o |
| Implementer | `@somas-implementer` | Code generation | GPT-4o |
| Tester | `@somas-tester` | Quality validation | GPT-4o |
| Deployer | `@somas-deployer` | Infrastructure | GPT-4o |
| Reviewer | `@somas-reviewer` | Code review | GPT-4o |
| Orchestrator | `@somas-orchestrator` | Pipeline mgmt | GPT-4o |
| Documenter | `@somas-documenter` | Documentation | GPT-4o |
| Security | `@somas-security` | Security audit | GPT-4o |
| Advisor | `@somas-advisor` | Strategic decisions | o1-preview |

---

**Version:** 1.0.0  
**Last Updated:** 2024  
**Maintained By:** SOMAS Core Team

For questions or issues with agents, create an issue with label `agent-support`.
