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

For issues or questions:
- **Owner:** @scotlaclair
- **Repository:** github.com/scotlaclair/SOMAS
- **Documentation:** /docs/somas/

---

*Last Updated: 2024*
