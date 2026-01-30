# SOMAS Documentation

**Self-Sovereign Orchestrated Multi-Agent System**

Complete technical documentation for the autonomous AI development pipeline.

---

## Table of Contents

1. [Introduction](#introduction)
2. [How SOMAS Works](#how-somas-works)
3. [Pipeline Stages](#pipeline-stages)
4. [Agent System](#agent-system)
5. [Triage System](#triage-system)
6. [Configuration](#configuration)
7. [State Persistence](#state-persistence)
8. [Autonomy & Self-Healing](#autonomy--self-healing)
9. [Quality Assurance](#quality-assurance)
10. [Security](#security)
11. [Optimization](#optimization)
12. [Advanced Usage](#advanced-usage)
13. [Troubleshooting](#troubleshooting)

---

## Introduction

SOMAS is an AI-first Software Development Life Cycle (SDLC) that transforms project ideas into production-ready software through orchestrated AI agents. The system leverages 2026 Frontier Tier models (GPT-5.2-Codex, Claude Opus 4.5, Claude Sonnet 4.5, GPT-5.2, Gemini 3 Pro, and Grok Code Fast 1) to handle the complete development lifecycle autonomously.

### Key Concepts

- **Fully Autonomous**: AI agents handle all 11 pipeline stages with minimal human intervention
- **15 Specialized Agents**: Each with domain expertise and optimal AI model selection
- **Self-Healing**: Automatic retry and debugging for validation failures
- **Simulation-Based Optimization**: Monte Carlo analysis for optimal task sequencing
- **Bounded Autonomy**: Human engagement only for final merge approval and unrecoverable failures
- **Quality First**: 80%+ test coverage, security scanning, and comprehensive code review
- **Aether Lifecycle**: 11-stage autonomous development pipeline with specialized AI agents

---

## How SOMAS Works

### Workflow Overview

```
Issue created with somas-project label →
Pipeline initializes (11 stages) →
All stages execute autonomously →
PR created for human review →
Human approves and merges
```

### Detailed Flow

1. **Issue Creation & Trigger**
   - User creates GitHub issue with project idea
   - Adds `somas-project` label
   - Workflow automatically initializes

2. **Project Initialization**
   - Creates project directory structure
   - Generates project metadata
   - Initializes all 11 pipeline stages

3. **Autonomous Execution**
   - Stages 1-10 execute without human intervention
   - Each stage invokes specialized AI agents via issue comments
   - Agents generate artifacts and commit results
   - Progress tracked in issue comments

4. **Self-Healing Validation**
   - Validation failures trigger automatic retry (up to 3 attempts)
   - Debugger agent investigates and fixes issues
   - Only escalates to human after retries exhausted

5. **Release & Human Review**
   - Stage 9 (RELEASE) creates pull request with all artifacts
   - Human reviews generated code (ONLY human touchpoint)
   - Approves and merges when ready

6. **Learning Loop**
   - Stage 11 (ANALYZE) analyzes entire pipeline execution
   - Extracts lessons learned and optimization opportunities
   - Updates knowledge base for continuous improvement

7. **Completion**
   - Code merged to main branch
   - Project artifacts archived
   - Metrics recorded for continuous learning
   - State persisted for audit and recovery

---

## State Persistence

**New in v1.0.0**: SOMAS now includes comprehensive JSON-based state persistence for robust fault recovery and forensics.

### State Files

Each project maintains three persistent state files:

- **`state.json`**: Complete pipeline state with checkpoints, labels, and metrics
- **`dead_letters.json`**: Failed agent contexts for recovery and replay
- **`transitions.jsonl`**: Chronological audit log of all transitions

### Key Features

- **Automatic Recovery**: Resume from last successful checkpoint on failure
- **Audit Trail**: Complete history of all state transitions and events
- **Forensics**: Rich context for debugging failures
- **Metrics**: Detailed execution metrics per stage
- **Replay**: Ability to replay failed operations with full context

### Example State Structure

```json
{
  "project_id": "project-123",
  "current_stage": "implementation",
  "status": "in_progress",
  "checkpoints": [...],
  "metrics": {
    "total_duration_seconds": 1800,
    "agent_invocations": 5,
    "dead_letters": 0
  },
  "recovery_info": {
    "last_successful_checkpoint": "chk-abc123",
    "can_resume": true
  }
}
```

📖 **Full Documentation**: See [State Persistence Guide](./STATE_PERSISTENCE.md)

---

## Pipeline Stages

### Stage 1: Ideation

**Agent**: Planner (GPT-5.2)  
**Autonomous**: Yes  
**Duration**: ~5-10 minutes

**Purpose**: Transform raw idea into structured plan

**Activities**:
- Extract and analyze requirements from issue
- Define project scope and constraints
- Create high-level implementation roadmap
- Identify dependencies and risks
- Estimate timeline and resource needs

**Output**: `initial_plan.md`

**Quality Gates**: N/A (planning stage)

---

### Stage 2: Specification

**Agent**: Specifier (GPT-5.2)  
**Autonomous**: Yes (No human gate)  
**Duration**: ~15-30 minutes

**Purpose**: Generate complete, unambiguous specification

**Activities**:
- Create comprehensive SPEC.md document
- Define functional and non-functional requirements
- Document user stories with acceptance criteria
- Specify API contracts and data models
- Resolve all ambiguities and open questions

**Output**: `SPEC.md`, `requirements.yml`

**Quality Gates**:
- All requirements have unique IDs
- All requirements are testable
- No ambiguous language (TBD, maybe, etc.)
- All open questions resolved

---

### Stage 3: Simulation

**Agent**: Simulator (GPT-5.2)  
**Autonomous**: Yes  
**Duration**: ~10-15 minutes

**Purpose**: Optimize task execution through Monte Carlo simulation

**Activities**:
- Run 1000+ Monte Carlo iterations
- Simulate different task execution sequences
- Identify optimal task order
- Determine critical path
- Maximize parallelization opportunities
- Estimate timeline with 90% confidence

**Output**: `execution_plan.yml`, `simulation_results.json`

**Quality Gates**:
- Task graph is acyclic
- All tasks have duration estimates
- Critical path identified
- Parallelization opportunities documented

---

### Stage 4: Architecture

**Agent**: Architect (Claude Opus 4.5)  
**Autonomous**: Yes  
**Duration**: ~30-60 minutes

**Purpose**: Design system architecture and components

**Activities**:
- Design high-level system architecture
- Define components and their interactions
- Create data models and schemas
- Specify API contracts and interfaces
- Document technology choices and ADRs
- Design for scalability and maintainability

**Output**: `ARCHITECTURE.md`, `api_specs.yml`, `data_models.yml`, ADRs

**Quality Gates**:
- All components defined with clear responsibilities
- Interfaces specified with contracts
- Data flows documented
- Technology choices justified

---

### Stage 5: Implementation

**Agents**: Implementer (GPT-5.2-Codex), Tester (Claude Sonnet 4.5), Security (GPT-5.2), Optimizer (Claude Sonnet 4.5), Documenter (Gemini 3 Pro)  
**Autonomous**: Yes  
**Duration**: ~2-8 hours (varies by complexity)

**Purpose**: Generate production-ready code with comprehensive tests

**Activities**:
- Generate source code following architecture
- Create comprehensive test suites (80%+ coverage)
- Perform security vulnerability scanning
- Optimize performance bottlenecks
- Document code and APIs
- Make incremental commits

**Output**: Source code, tests, documentation in `implementation/` directory

**Quality Gates**:
- All tests passing
- Code coverage > 80%
- No critical security vulnerabilities
- Documentation complete
- Code follows best practices

---

### Stage 6: Validation

**Agents**: Tester (Claude Sonnet 4.5), Reviewer (Claude Sonnet 4.5), Security (GPT-5.2), Debugger (Claude Haiku 4.5)  
**Autonomous**: Yes (with auto-retry)  
**Duration**: ~30-90 minutes  
**Max Retries**: 3

**Purpose**: Independent quality verification and validation

**Activities**:
- Run all tests and verify coverage
- Perform comprehensive code quality review
- Execute security vulnerability scan
- Validate against all acceptance criteria
- Check performance requirements
- **Auto-retry on failure**: Debugger investigates and fixes issues

**Output**: `validation_report.json`, `test_results.json`, `security_scan.json`

**Quality Gates**:
- All acceptance criteria met
- All tests passing
- Code coverage > 80%
- Security scan passed
- Performance requirements satisfied

**Self-Healing**:
1. Attempt 1: Run validation suite
2. If failed, invoke Debugger agent
3. Attempt 2: Re-run validation after fixes
4. Repeat up to 3 total attempts
5. Escalate to human only after all retries exhausted

---

### Stage 7: Staging

**Agents**: Merger (Claude Opus 4.5), Documenter (Gemini 3 Pro)  
**Autonomous**: No (requires human approval)  
**Duration**: Variable (waits for human review)

**Purpose**: Prepare for merge and request human approval

**Activities**:
- Create pull request with all artifacts
- Generate deployment documentation
- Resolve any merge conflicts
- Aggregate final status and metrics
- Request human review and approval

**Output**: Pull request, deployment docs, final report

**Quality Gates**: Human approval required

**Human Action**: This is the **ONLY** stage requiring human intervention. Human reviews the complete work product and approves merge when ready.

---

## Agent System

### 13 Specialized Agents

SOMAS uses 13 specialized AI agents, each powered by the optimal AI model for their task:

| Agent | Model | Stage(s) | Responsibilities |
|-------|-------|----------|------------------|
| **Triage** | Grok Code Fast 1 | Entry Point | Request classification, routing, escalation |
| **Orchestrator** | Grok Code Fast 1 | All | Pipeline coordination, state management, agent handoff |
| **Planner** | GPT-5.2 | Ideation | Requirements analysis, roadmap creation |
| **Specifier** | GPT-5.2 | Specification | Complete specification generation |
| **Simulator** | GPT-5.2 | Simulation | Monte Carlo simulation, task optimization |
| **Architect** | Claude Opus 4.5 | Architecture | System architecture, design decisions |
| **Implementer** | GPT-5.2-Codex | Implementation | Production-ready code generation |
| **Tester** | Claude Sonnet 4.5 | Implementation, Validation | Test suite creation, test execution |
| **Reviewer** | Claude Sonnet 4.5 | Validation | Code quality review, architecture review |
| **Security** | GPT-5.2 | Implementation, Validation | Security scanning, vulnerability detection |
| **Optimizer** | Claude Sonnet 4.5 | Implementation | Performance optimization |
| **Debugger** | Claude Haiku 4.5 | Validation (on failure) | Bug investigation and fixes |
| **Documenter** | Gemini 3 Pro | Implementation, Staging | Documentation, API references |
| **Merger** | Claude Opus 4.5 | Staging | Merge preparation, conflict resolution |

### Agent Invocation

Agents are invoked via GitHub issue comments during workflow execution:

```yaml
# Example: Invoking the Planner agent
- uses: actions/github-script@v7
  with:
    script: |
      await github.rest.issues.createComment({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: context.payload.issue.number,
        body: `## Stage 1: Ideation
        
**Agent:** @somas-planner
**Task:** Analyze requirements and create implementation plan
**Output:** .somas/projects/${projectId}/artifacts/initial_plan.md`
      });
```

Agents respond by:
1. Reading the project context and inputs
2. Performing their specialized task
3. Generating output artifacts
4. Committing results to the repository

---

## Triage System

### Overview

The Triage System provides an external entry point for change requests, enhancements, questions, and bugs without disrupting the autonomous pipeline. Instead of requiring a full 7-stage pipeline restart for minor changes, the triage agent intelligently routes requests to the appropriate stage.

### Why Triage?

**Problems Solved:**
- ❌ Previously: All changes required full pipeline restart
- ❌ Previously: No way to inject changes into in-progress projects
- ❌ Previously: Questions triggered unnecessary pipeline execution
- ❌ Previously: Minor bugs required full validation cycle

**With Triage:**
- ✅ Changes injected at the right stage (planner, architect, or implementer)
- ✅ Questions routed to advisor without pipeline execution
- ✅ Bugs routed directly to debugger or tester
- ✅ Enhancements prioritized and queued appropriately

### Issue Templates

Four specialized issue templates handle different request types:

#### 1. Change Request (`somas-change.yml`)
**Label:** `somas:change`

Use when you need to modify an existing in-progress project:
- Scope additions or reductions
- Requirement modifications
- Constraint changes
- Priority adjustments

**Example:** "Add user authentication to the API"

#### 2. Enhancement Suggestion (`somas-enhance.yml`)
**Label:** `somas:enhance`

Use for new feature ideas or improvements:
- Feature ideas
- Performance improvements
- Optimizations
- Documentation enhancements

**Prioritization:**
- **Critical/High**: Routed to planner immediately
- **Medium/Low**: Added to backlog
- **Future**: Tagged for later consideration

**Example:** "Add caching layer to improve API performance"

#### 3. Question/Research (`somas-question.yml`)
**Label:** `somas:question`

Use for questions or research requests:
- Technical questions
- Process clarifications
- Feasibility studies
- Technology recommendations

**Important:** Questions NEVER trigger pipeline execution. They are informational only.

**Example:** "Should we use PostgreSQL or MongoDB for this project?"

#### 4. Bug Report (`somas-bug.yml`)
**Label:** `somas:bug`

Use to report bugs in projects or SOMAS itself:
- Implementation bugs
- Test failures
- Specification gaps
- Documentation errors

**Example:** "API returns HTTP 500 instead of 429 for rate limiting"

### Triage Agent

**Agent:** Triage (Grok Code Fast 1)  
**Purpose:** Fast classification and routing of incoming requests  
**Configuration:** `.somas/agents/triage.yml`  
**Instructions:** `.github/agents/somas-triage.md`

#### Deterministic Routing Criteria

The triage agent uses **deterministic criteria** (not heuristics) to classify and route requests:

**Route to PLANNER** when:
- ✅ Adds new functional requirements
- ✅ Removes or modifies existing requirements
- ✅ Changes project scope by >10%
- ✅ Introduces new dependencies
- ✅ Modifies acceptance criteria

**Route to ARCHITECT** when:
- ✅ Changes component interactions without new requirements
- ✅ Technology stack modification
- ✅ API contract changes within existing scope
- ✅ Database schema changes

**Route to IMPLEMENTER** when:
- ✅ Bug fix within existing spec
- ✅ Performance optimization without spec change
- ✅ Code refactoring
- ✅ Minor implementation improvements

**Route to ADVISOR** when:
- ✅ Feasibility questions
- ✅ Technology recommendations
- ✅ Best practice inquiries
- ✅ Research into alternatives

**DEFER to Backlog** when:
- ✅ Enhancement for future version
- ✅ Nice-to-have with no urgency
- ✅ Dependent on other pending changes

**REJECT** when:
- ✅ Out of project scope entirely
- ✅ Duplicate of existing issue
- ✅ Conflicts with core requirements
- ✅ Should use different issue template

#### Confidence-Based Escalation

The triage agent calculates confidence for each classification:

- **High Confidence (>0.9)**: Proceed automatically
- **Medium Confidence (0.8-0.9)**: Proceed with logging
- **Low Confidence (<0.8)**: **Escalate to human** (@scotlaclair)

This ensures that ambiguous or complex cases get human review instead of being misrouted.

### Triage Workflow

```
Issue Created with triage label →
  ↓
Triage Agent Analyzes Request →
  ↓
Classification & Confidence Calculation →
  ↓
Routing Decision (deterministic) →
  ↓
Route to Target Agent OR Escalate to Human
```

### Change Injection Flow

When triage routes a change request to planner:

1. **Impact Analysis**: Planner analyzes impact on existing SPEC.md
2. **Change Proposal**: Planner creates proposal with:
   - Affected requirements (by ID)
   - New/modified requirements
   - Estimated simulation impact
3. **Approval**: Auto-approved for small changes, human review for large changes
4. **Update**: SPEC.md updated with new revision
5. **Re-simulation**: Simulation re-run if scope changed significantly
6. **Continue**: Pipeline continues from appropriate stage

### How to Submit Requests

1. **Go to Issues** → Click "New Issue"
2. **Select Template**:
   - 🔄 SOMAS Change Request
   - ✨ SOMAS Enhancement Suggestion
   - ❓ SOMAS Question/Research
   - 🐛 SOMAS Bug Report
3. **Fill in Details**: Provide all required information
4. **Submit**: Issue is auto-labeled and triage agent is invoked
5. **Wait for Triage**: Agent responds with classification and routing decision
6. **Track Progress**: Follow the routed agent's work in issue comments

### Triage Output Format

The triage agent always responds with structured output:

```yaml
triage_result:
  issue_number: 125
  classification: change
  confidence: 0.95
  routing:
    agent: planner
    reason: "Adds new functional requirement (authentication) affecting multiple components"
  linked_project: project-123
  spec_impact: true
  estimated_effort: large
  action: route
  next_steps: |
    1. Planner will analyze impact on existing SPEC.md
    2. Create change proposal with affected requirements
    3. Update SPEC.md with authentication requirements
    4. Re-run simulation to optimize task order
    5. Architecture will incorporate auth design
```

### Design Principles

1. **Deterministic over Heuristic**: Clear rules, not fuzzy matching
2. **Minimal Intervention**: Route to latest possible stage (don't restart entire pipeline)
3. **Spec as Truth**: All requirement changes flow through spec
4. **Audit Trail**: All triage decisions logged with justification
5. **Fail Safe**: When uncertain, escalate to human (don't guess)

### When to Use Each Template

| Scenario | Template | Will Trigger Pipeline? |
|----------|----------|------------------------|
| Add feature to existing project | Change Request | Yes (from appropriate stage) |
| Suggest new feature idea | Enhancement | Depends on priority |
| Ask "How does X work?" | Question | No (informational only) |
| Report implementation bug | Bug Report | Yes (debugger stage only) |
| Change architecture approach | Change Request | Yes (from architect stage) |
| Optimize performance | Enhancement (medium priority) | No (deferred to backlog) |
| Research technology options | Question | No (advisor responds) |
| Fix broken tests | Bug Report | Yes (tester stage only) |

### Benefits

**For Users:**
- ✅ Don't need to understand pipeline stages
- ✅ Changes handled efficiently
- ✅ Questions answered without overhead
- ✅ Clear feedback on what happens next

**For SOMAS:**
- ✅ Minimal pipeline disruption
- ✅ Deterministic routing reduces errors
- ✅ Human escalation for edge cases
- ✅ Audit trail for all decisions
- ✅ Prevents unnecessary full pipeline runs

---

## Configuration

### Main Configuration: `.somas/config.yml`

Key configuration sections:

#### Pipeline Stages

```yaml
pipeline:
  stages:
    - id: "specification"
      human_gate: false      # No human approval needed
      auto_proceed: true     # Automatically proceed to next stage
      
    - id: "validation"
      max_retries: 3         # Auto-retry failures up to 3 times
      
    - id: "staging"
      human_gate: true       # ONLY stage requiring human approval
      auto_proceed: false
      human_action: "merge_approval"
```

#### Agent Configurations

```yaml
agents:
  providers:
    gpt_5_2_codex:
      model: "gpt-5.2-codex"
      temperature: 0.3
      max_tokens: 8000
      
  agent_configs:
    implementer:
      provider: "gpt_5_2_codex"
      config_file: ".somas/agents/implementer.yml"
```

#### Quality Gates

```yaml
quality_gates:
  specification:
    - "All requirements have unique IDs"
    - "All requirements are testable"
    
  implementation:
    - "All tests passing"
    - "Code coverage > 80%"
    - "No critical security vulnerabilities"
```

### Agent Configuration Files: `.somas/agents/*.yml`

Each agent has a detailed configuration:

```yaml
# Example: .somas/agents/implementer.yml
role: "Code Implementation Specialist"
provider: "gpt_5_2_codex"

instructions: |
  Generate production-ready code based on architecture design.
  Follow best practices and coding standards.
  Ensure comprehensive error handling.

output_format:
  - "Source code files"
  - "Unit tests"
  - "Integration tests"
  
quality_checks:
  - "Code compiles without errors"
  - "All tests pass"
  - "No security vulnerabilities"
```

### Stage Configuration Files: `.somas/stages/*.yml`

Stage-specific settings:

```yaml
# Example: .somas/stages/specification.yml
specification:
  id: "specification"
  order: 2
  objective: "Produce complete, unambiguous specification"
  
  agents:
    primary: "specifier"
    review: "reviewer"
    
  human_gate: false  # Autonomous - no human approval
```

---

## Autonomy & Self-Healing

### Autonomous Operation Principles

1. **Minimal Human Intervention**
   - Human engaged ONLY for final merge approval
   - Human notified ONLY when autonomous resolution fails

2. **Bounded Autonomy**
   - All stages 1-6 are fully autonomous
   - Stage 7 (Staging) requires human approval
   - Clear escalation path when automation cannot resolve issues

3. **Progress Transparency**
   - All agent activities logged in issue comments
   - Real-time pipeline status visible
   - Artifact generation tracked

### Self-Healing Validation

When validation failures occur:

```
Attempt 1: Run validation suite
  ↓ (if failed)
Invoke Debugger agent to investigate and fix
  ↓
Attempt 2: Re-run validation
  ↓ (if failed)
Invoke Debugger again
  ↓
Attempt 3: Final validation attempt
  ↓ (if still failed)
Escalate to human: @scotlaclair
```

**Key Features**:
- Automatic retry up to 3 attempts
- Debugger agent analyzes failures and applies fixes
- No human intervention unless all retries exhausted
- Failure analysis stored for learning

### Retry Logic Implementation

Implemented in Stage 6 (Validation):

```javascript
const maxRetries = 3;
let attempt = 0;
let passed = false;

while (attempt < maxRetries && !passed) {
  attempt++;
  
  // Run validation
  await runValidationSuite();
  
  // Check results
  passed = await checkQualityGates();
  
  if (!passed && attempt < maxRetries) {
    // Invoke debugger
    await invokeDebugger();
    await waitForFixes();
  }
}

if (!passed) {
  // Escalate to human
  await notifyHuman();
}
```

---

## Quality Assurance

### Built-in Quality Checks

**Code Quality**:
- Comprehensive code review by Reviewer agent
- Adherence to coding standards
- Clean architecture principles
- Proper error handling

**Testing**:
- 80%+ code coverage requirement
- Unit tests for all components
- Integration tests for system interactions
- Edge case coverage

**Security**:
- Automated vulnerability scanning
- Secure coding practices validation
- Dependency security checks
- Input validation verification

**Performance**:
- Performance profiling
- Bottleneck identification
- Optimization recommendations

### Quality Gates by Stage

Each stage has specific quality gates that must pass before proceeding:

**Specification**:
- ✅ All requirements uniquely identified
- ✅ All requirements testable
- ✅ No ambiguous language
- ✅ Zero open questions

**Implementation**:
- ✅ All tests passing
- ✅ Code coverage > 80%
- ✅ No critical vulnerabilities
- ✅ Documentation complete

**Validation**:
- ✅ All acceptance criteria met
- ✅ Performance requirements satisfied
- ✅ Security scan clean
- ✅ Integration tests passing

---

## Security

### Security Measures

**Input Validation**:
- Project IDs validated to prevent path traversal
- User input sanitized
- Command injection prevention

**Secure Coding**:
- Dedicated Security agent reviews all code
- OWASP Top 10 coverage
- Secure defaults enforced

**Secrets Management**:
- GitHub Secrets for API keys
- No hardcoded credentials
- Secure environment variable handling

**Vulnerability Scanning**:
- CodeQL integration
- Dependency scanning with Dependabot
- Regular security audits

### Security Agent

The Security agent (GPT-5.2) performs:
- Static code analysis
- Vulnerability scanning
- Secure coding practice verification
- Dependency security checks
- Security best practices validation

Runs in:
- Stage 5 (Implementation) - Reviews generated code
- Stage 6 (Validation) - Final security audit

---

## Optimization

### Monte Carlo Simulation

SOMAS uses Monte Carlo simulation in Stage 3 to optimize task execution:

**Process**:
1. Generate task dependency graph
2. Run 1000+ simulations with varying parameters
3. Track task durations and dependencies
4. Identify optimal execution sequence
5. Determine critical path
6. Maximize parallelization

**Benefits**:
- 40-60% reduction in overall timeline
- Optimal resource utilization
- Risk identification early
- Data-driven task ordering

**Output**: `execution_plan.yml` with optimized task sequence

### Parallelization

SOMAS maximizes parallel execution:

```yaml
parallelization:
  enabled: true
  max_concurrent_tasks: 5
  respect_dependencies: true
  load_balancing_strategy: "duration_based"
```

**Strategies**:
- Identify independent tasks
- Schedule longest tasks first
- Balance load across resources
- Respect dependencies

### Continuous Learning

SOMAS learns from each run:

```yaml
learning:
  enabled: true
  record_all_runs: true
  update_estimates_from_actuals: true
  pattern_extraction: true
```

**Learning Areas**:
- Duration estimation improvement
- Task decomposition patterns
- Common failure modes
- Optimization opportunities

---

## Advanced Usage

### Manual Stage Execution

Run specific stages manually:

```yaml
# Workflow dispatch with stage selection
workflow_dispatch:
  inputs:
    stage:
      type: choice
      options:
        - all
        - ideation
        - specification
        - simulation
        - architecture
        - implementation
        - validation
        - staging
```

### Custom Agent Configuration

Customize agent behavior by editing `.somas/agents/*.yml`:

```yaml
# Customize temperature for more creative output
implementer:
  provider: "gpt_5_2_codex"
  temperature: 0.5  # Default: 0.3
  
  # Add custom instructions
  custom_instructions: |
    Focus on clean, maintainable code.
    Prefer functional programming patterns.
    Use TypeScript for all JavaScript code.
```

### GitHub Project Integration

SOMAS automatically creates GitHub Projects for visual tracking:

```yaml
project_management:
  enabled: true
  github_project:
    create_per_pipeline: true
    template: "SOMAS Pipeline"
```

**Features**:
- Real-time status updates
- Task decomposition visualization
- Progress tracking
- Metrics dashboard

---

## Troubleshooting

### Common Issues

**Validation Failures**
- **Symptom**: Stage 6 fails repeatedly
- **Solution**: Check validation logs, review test failures, verify acceptance criteria met
- **Auto-healing**: Debugger agent automatically investigates after first failure

**Artifact Not Generated**
- **Symptom**: Stage waits indefinitely for artifact
- **Solution**: Check agent logs, verify agent invoked correctly, increase timeout
- **Prevention**: Artifact verification has 5-30 minute timeouts depending on stage

**PR Creation Failed**
- **Symptom**: Stage 7 completes but no PR created
- **Solution**: Verify branch exists, check permissions, manually create PR
- **Note**: Workflow logs will indicate specific failure reason

### Debug Mode

Enable verbose logging:

```yaml
development:
  debug_mode: true
  verbose_logging: true
  save_intermediate_states: true
```

### Getting Help

1. Check issue comments for agent activity logs
2. Review workflow logs in GitHub Actions
3. Examine project artifacts in `.somas/projects/{project-id}/`
4. Check configuration files for misconfigurations
5. Open an issue with `somas:help` label

---

## Metrics & Analytics

SOMAS tracks comprehensive metrics:

```yaml
analytics:
  track:
    - "task_duration_vs_estimate"
    - "iteration_count_by_task_type"
    - "parallel_efficiency"
    - "critical_path_accuracy"
    - "human_intervention_frequency"
```

**Stored in**: `.somas/analytics/runs/`

**Used for**:
- Continuous improvement
- Estimation accuracy
- Process optimization
- Pattern identification

---

## FAQ

**Q: How long does a typical project take?**  
A: Varies by complexity:
- Simple CLI tools: 30-60 minutes
- Web applications: 2-4 hours  
- Complex systems: 4-8 hours

**Q: When do I need to get involved?**  
A: Only twice:
1. Creating the initial issue with project description
2. Reviewing and approving the final PR (Stage 7)

**Q: What if validation fails 3 times?**  
A: You'll be notified to investigate manually. The pipeline provides detailed logs of what failed and what the Debugger agent attempted.

**Q: Can I customize which AI models are used?**  
A: Yes! Edit `.somas/config.yml` agent provider mappings. Current models are optimized for each task.

**Q: Does SOMAS work with private repositories?**  
A: Yes, as long as GitHub Actions is enabled and required secrets are configured.

**Q: Can I skip stages?**  
A: Not recommended as stages depend on previous outputs. However, you can manually run specific stages using workflow_dispatch.

**Q: What languages are supported?**  
A: All major languages. Specify your preference in the project description. SOMAS will use appropriate tools and frameworks.

---

## Additional Resources

### Core Documentation

- **[Architecture Diagrams](architecture-diagrams.md)** - Visual system architecture (Mermaid)
- **[Configuration Reference](configuration-reference.md)** - Complete configuration options
- **[Developer Guide](developer-guide.md)** - Extending and modifying SOMAS
- **[Test Strategy](test-strategy.md)** - Testing philosophy and patterns
- **[Operations Runbook](operations-runbook.md)** - Operational procedures

### Guides

- **[Optimization Guide](optimization-guide.md)** - Advanced optimization techniques
- **[Copilot Integration](COPILOT_GUIDE.md)** - GitHub Copilot usage patterns
- **[APO Guide](apo-guide.md)** - Autonomous Prompt Optimization
- **[Migration Guide](MIGRATION_GUIDE.md)** - Configuration migration
- **[Troubleshooting](TROUBLESHOOTING.md)** - Common issues and solutions
- **[State Persistence](STATE_PERSISTENCE.md)** - State management guide

### API Reference

- **[API Documentation](../api/)** - Auto-generated from docstrings (run `pdoc somas`)

### Project Files

- **[CONTRIBUTING.md](../../CONTRIBUTING.md)** - Contribution guidelines
- **[CHANGELOG.md](../../CHANGELOG.md)** - Version history
- **[Configuration](../../.somas/config.yml)** - Main config file

---

## License

MIT License - See [LICENSE](../../LICENSE) for details

---

**Questions or feedback?** Open an issue with the `somas:question` label.
