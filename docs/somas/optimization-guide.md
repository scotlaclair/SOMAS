# SOMAS Optimization Guide

**Advanced techniques for optimizing the SOMAS pipeline**

---

## Table of Contents

1. [Understanding Simulation](#understanding-simulation)
2. [Interpreting Execution Plans](#interpreting-execution-plans)
3. [Tuning Parallelization](#tuning-parallelization)
4. [Understanding Metrics](#understanding-metrics)
5. [Advanced Configuration](#advanced-configuration)
6. [Common Optimization Patterns](#common-optimization-patterns)

---

## Understanding Simulation

### How Monte Carlo Simulation Works

The SOMAS simulator uses Monte Carlo analysis to predict project outcomes:

#### 1. Task Graph Construction

From the specification, the simulator builds a Directed Acyclic Graph (DAG):
- **Nodes** = Tasks (from requirements, user stories, components)
- **Edges** = Dependencies (data, logical, resource, integration)
- **Weights** = Duration estimates with uncertainty

**Example:**
```yaml
task_graph:
  TASK-001:
    name: "Database Schema Design"
    dependencies: []
    duration:
      optimistic: 4.0
      most_likely: 6.5
      pessimistic: 10.0
  
  TASK-005:
    name: "Core API Implementation"
    dependencies: ["TASK-001"]
    duration:
      optimistic: 8.0
      most_likely: 12.3
      pessimistic: 18.0
```

#### 2. Duration Distribution

Each task uses a **PERT (Beta) distribution**:
- **Optimistic** (10th percentile): Best case, no issues
- **Most Likely** (50th percentile): Expected typical case
- **Pessimistic** (90th percentile): With complications

**Formula:**
```
Mean = (Optimistic + 4 × MostLikely + Pessimistic) / 6
StdDev = (Pessimistic - Optimistic) / 6
```

#### 3. Simulation Process

For 1000 iterations:
1. Sample duration for each task from its distribution
2. Calculate earliest start time (considering dependencies)
3. Calculate project completion time
4. Record which tasks are on the critical path
5. Store results

#### 4. Results Analysis

From 1000 iterations, calculate:
- **Mean completion time**: Expected duration
- **P90 completion time**: 90% confidence level
- **Critical path frequency**: Which tasks are critical most often
- **Task slack**: How much delay each task can tolerate

### Interpreting Simulation Results

#### Completion Time Statistics

```yaml
mean_hours: 42.5          # Expected duration
median_hours: 40.2        # Middle value (50% likelihood)
p90_hours: 58.3           # 90% confident it will finish by this time
standard_deviation: 8.7   # Variability in outcomes
```

**What this means:**
- Most likely complete in ~40-43 hours
- 90% chance to complete within 58 hours
- High variability (StdDev = 8.7) suggests significant uncertainty

#### Critical Path Analysis

```yaml
critical_path:
  - task_id: "TASK-005"
    probability: 0.95      # Critical in 95% of simulations
    mean_duration: 12.3
```

**Probability Interpretation:**
- **> 0.90**: Almost always critical - optimize this task!
- **0.70 - 0.90**: Frequently critical - monitor closely
- **0.50 - 0.70**: Sometimes critical - depends on other tasks
- **< 0.50**: Rarely critical - has slack time

#### Risk Indicators

**High Risk Factors:**
- High probability of being on critical path (> 0.70)
- Large duration variance (StdDev / Mean > 0.5)
- Many dependencies (> 5 tasks depend on this)
- Novel technology or approach

---

## Interpreting Execution Plans

### Execution Plan Structure

An execution plan divides work into **phases** where tasks can run in parallel:

```yaml
phase_2:
  name: "Core Implementation"
  duration: 18-24 hours
  parallel_tasks: 4
  
  tasks:
    - task_id: "TASK-005"
      duration: 12.3 hours
      risk: "HIGH"
      assignee: "Backend Developer 1"
      
    - task_id: "TASK-006"
      duration: 10.5 hours
      assignee: "Frontend Developer 1"
```

### Reading the Plan

#### Phase Characteristics

**Duration Range**: "18-24 hours"
- Lower bound: If all tasks complete at optimistic time
- Upper bound: If all tasks complete at pessimistic time
- Actual time determined by the **longest task** in the phase

**Parallel Tasks**: 4
- Number of tasks that can run simultaneously
- Requires this many developers/resources

**Team Size Needed**: 4
- Optimal team allocation for this phase
- More developers won't speed it up (no more parallel work)

#### Task Assignments

**Risk Levels:**
- **HIGH**: Requires senior developer, frequent check-ins
- **MEDIUM**: Standard complexity, normal oversight
- **LOW**: Straightforward, minimal risk

**Dependencies:**
```yaml
depends_on: ["TASK-001", "TASK-002"]
```
- Must wait for these tasks to complete before starting

### Optimizing Based on the Plan

#### 1. Front-load High-Risk Tasks

If simulation shows a high-risk task:
```yaml
- task_id: "TASK-005"
  risk: "HIGH"
  probability: 0.95  # Almost always critical
```

**Actions:**
- Start this task immediately (even before scheduled)
- Allocate your best developer
- Consider a proof-of-concept spike first
- Add daily check-ins

#### 2. Increase Parallelization

If you have more resources than max concurrent tasks:
```yaml
max_concurrent_tasks: 4
peak_concurrency_phase: "Phase 2"
```

**Options:**
- Decompose large tasks into smaller ones
- Look for hidden parallelization opportunities
- Consider pair programming on high-risk tasks

#### 3. Address Bottlenecks

If one task blocks many others:
```yaml
bottleneck_tasks:
  - task_id: "TASK-005"
    delay_caused_hours: 8
    blocks: 8 downstream tasks
```

**Actions:**
- Start this task early
- Allocate extra resources
- Prepare mocks/stubs to unblock downstream work
- Consider alternative approaches

---

## Tuning Parallelization

### Configuration Parameters

```yaml
optimization:
  parallelization:
    enabled: true
    max_concurrent_tasks: 5
    respect_dependencies: true
    load_balancing_strategy: "duration_based"
```

### Max Concurrent Tasks

**How to determine:**
```
max_concurrent_tasks = min(
  team_size,
  average_parallel_opportunities,
  resource_limits
)
```

**Guidelines:**
- **Small team (1-3)**: Set to 2-3
- **Medium team (4-8)**: Set to 4-6
- **Large team (9+)**: Set to 6-10

**Warning:** Setting too high can cause:
- Integration conflicts
- Communication overhead
- Code review bottlenecks

### Load Balancing Strategies

#### Duration-Based (Default)
```yaml
load_balancing_strategy: "duration_based"
```
Groups tasks so each developer has similar total hours.

**Best for:** Balanced workloads, equal skill levels

#### Skill-Based
```yaml
load_balancing_strategy: "skill_based"
```
Assigns tasks based on developer expertise.

**Best for:** Varied skill levels, specialized tasks

#### Dependency-Based
```yaml
load_balancing_strategy: "dependency_based"
```
Minimizes dependencies between parallel tasks.

**Best for:** Complex integration scenarios

### Measuring Parallelization Efficiency

```yaml
parallel_efficiency:
  planned_parallel_tasks: 4
  actual_parallel_tasks: 3.2  # Average achieved
  efficiency_score: 0.80      # 80% efficiency
```

**Efficiency Score:**
- **> 0.85**: Excellent parallelization
- **0.70 - 0.85**: Good, minor improvements possible
- **0.50 - 0.70**: Fair, review bottlenecks
- **< 0.50**: Poor, major issues present

**Common Issues:**
- **Underutilized:** Some developers idle while others work
- **Blocked:** Dependencies prevent true parallelism
- **Contention:** Developers waiting on each other

---

## Understanding Metrics

### Task Duration vs. Estimate

```yaml
task_duration_vs_estimate:
  estimated_duration_hours: 8.0
  actual_duration_hours: 10.5
  estimation_error_percent: 31.25
```

**Error Analysis:**
- **< 20%**: Good estimate
- **20-50%**: Moderate error, adjust factors
- **> 50%**: Poor estimate, investigate why

**Patterns to watch:**
- Consistently over/under estimating certain task types
- High variance in novel technology tasks
- Better estimates as project progresses (learning)

### Iteration Count by Task Type

```yaml
iteration_count_by_task_type:
  task_type: "api_implementation"
  mean_iterations: 2.3
  median_iterations: 2
```

**Interpretation:**
- **1 iteration**: Task completed correctly first time
- **2-3 iterations**: Normal for complex tasks
- **> 3 iterations**: Possible issues with spec clarity or complexity

**Common reasons for iterations:**
- Requirement misunderstanding
- Integration issues discovered late
- Test failures
- Code review feedback
- Performance issues

### Parallel Efficiency

```yaml
parallel_efficiency:
  planned_duration_hours: 24
  actual_duration_hours: 28
  efficiency_score: 0.86
  idle_time_hours: 4.2
```

**Optimization targets:**
- **Reduce idle time**: Better task decomposition
- **Improve efficiency**: More parallel-friendly architecture
- **Balance loads**: Reassign tasks based on complexity

### Critical Path Accuracy

```yaml
critical_path_accuracy:
  precision: 0.85      # 85% of predicted were actually critical
  recall: 0.92         # 92% of actual critical were predicted
  f1_score: 0.88       # Overall accuracy
```

**F1 Score Interpretation:**
- **> 0.85**: Excellent prediction
- **0.70 - 0.85**: Good prediction
- **< 0.70**: Model needs more training data

**If accuracy is low:**
- More training data needed (run more projects)
- Task complexity factors need adjustment
- Dependencies not properly captured

### Human Intervention Frequency

```yaml
human_intervention_frequency:
  stage: "specification"
  intervention_type: "clarification"
  wait_time_hours: 12
  could_be_automated: false
```

**Optimize by:**
- Better specification templates
- More detailed examples in prompts
- Clearer acceptance criteria
- Automated clarification workflows

---

## Advanced Configuration

### Adaptive Task Sizing

```yaml
optimization:
  adaptive_sizing:
    enabled: true
    target_task_duration_minutes: 240
    max_task_duration_minutes: 480
    auto_decompose: true
```

**Purpose:** Automatically split large/uncertain tasks

**When tasks are decomposed:**
- Estimated duration > max_task_duration
- Variance > threshold (high uncertainty)
- Multiple distinct functional areas

**Benefits:**
- Better progress visibility
- Earlier detection of issues
- More parallelization opportunities
- Reduced risk per task

### Rerun Simulation Threshold

```yaml
optimization:
  simulation:
    rerun_on_spec_change: true
    change_threshold_percent: 20
```

**When to rerun:**
- Specification changes > 20% of requirements
- Major scope additions
- Critical path tasks change significantly
- Actual durations deviate > 30% from estimates

### Risk-Based Prioritization

```yaml
optimization:
  task_prioritization:
    strategy: "critical_path_first"
    consider_risk: true
    consider_dependencies: true
```

**Prioritization order:**
1. High-risk tasks on critical path
2. Tasks blocking multiple others
3. High-risk tasks with slack
4. Normal tasks on critical path
5. Everything else

---

## Common Optimization Patterns

### Pattern 1: Front-Load Risk

**Problem:** High-risk task late in pipeline causes delays

**Solution:**
```yaml
recommendations:
  - action: "Start TASK-005 proof-of-concept early"
    rationale: "Validate approach before full implementation"
    impact: "Reduces overall project risk by 35%"
```

**Implementation:**
1. Create 2-hour spike task
2. Validate technical approach
3. Document findings
4. Proceed with confidence or pivot

### Pattern 2: Mock External Dependencies

**Problem:** Integration tasks blocked by external systems

**Solution:**
```yaml
recommendations:
  - action: "Create mock services during Phase 1"
    rationale: "Enables independent testing"
    impact: "Reduces TASK-008 risk and duration by 20%"
```

**Implementation:**
1. Define interface contracts early
2. Create mock implementations
3. Develop against mocks
4. Swap in real services during integration

### Pattern 3: Decompose Critical Path Tasks

**Problem:** Large task on critical path has high variance

**Solution:**
```yaml
recommendations:
  - action: "Split TASK-005 into 3 sub-tasks"
    subtasks:
      - "TASK-005A: Data Layer (4h)"
      - "TASK-005B: Business Logic (5h)"
      - "TASK-005C: REST Endpoints (3.3h)"
    impact: "Reduces risk, enables parallelization"
```

**Benefits:**
- Lower variance per task
- Enables parallel work
- Better progress visibility
- Early validation of each layer

### Pattern 4: Buffer Critical Path

**Problem:** Small delays on critical path cause cascading issues

**Solution:**
```yaml
recommendations:
  - action: "Add 15% buffer to critical path tasks"
    rationale: "Critical path determines completion"
    impact: "Increases P90 confidence from 58.3 to 52.1 hours"
```

**Buffer allocation:**
- **High risk tasks**: +20-30%
- **Medium risk tasks**: +15%
- **Low risk tasks**: +10%
- **Non-critical path**: No buffer needed

### Pattern 5: Optimize Phase Transitions

**Problem:** Long delays between phases

**Solution:**
```yaml
recommendations:
  - action: "Overlap Phase 2 and Phase 3"
    rationale: "Start integration planning while implementation continues"
    impact: "Reduces total duration by 15%"
```

**Safe overlaps:**
- Architecture → Implementation (low-risk components)
- Implementation → Testing (unit tests during development)
- Testing → Documentation (while fixing bugs)

### Pattern 6: Continuous Integration Testing

**Problem:** Integration issues discovered late

**Solution:**
```yaml
recommendations:
  - action: "Add daily integration tests during Phase 2"
    rationale: "Catch integration issues early"
    impact: "Reduces TASK-008 duration and risk"
```

**Implementation:**
1. Set up CI pipeline in Phase 1
2. Add integration tests incrementally
3. Run full suite daily
4. Fix issues immediately

---

## Optimization Checklist

Before starting a project:
- [ ] Review historical data for similar projects
- [ ] Set realistic parallelization limits
- [ ] Identify high-risk tasks early
- [ ] Plan for external dependencies
- [ ] Allocate buffers appropriately

During specification:
- [ ] Ensure requirements are decomposable
- [ ] Identify integration points
- [ ] Document complexity factors
- [ ] Plan for testing early

After simulation:
- [ ] Review critical path tasks
- [ ] Validate risk assessments
- [ ] Check parallelization opportunities
- [ ] Verify team size requirements
- [ ] Consider decomposition recommendations

During execution:
- [ ] Track actual vs. estimated durations
- [ ] Monitor critical path changes
- [ ] Record reasons for iterations
- [ ] Document blocking issues
- [ ] Update risk assessments

After completion:
- [ ] Review all metrics
- [ ] Update estimation models
- [ ] Document lessons learned
- [ ] Refine decomposition rules
- [ ] Improve templates

---

## Further Reading

- **SOMAS Documentation** - `/docs/somas/README.md`
- **Configuration Reference** - `/.somas/config.yml`
- **Analytics Schema** - `/.somas/analytics/schema.yml`
- **Agent Configurations** - `/.somas/agents/`

---

*For questions or issues, contact @scotlaclair*
