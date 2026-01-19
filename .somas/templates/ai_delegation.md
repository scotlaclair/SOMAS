# AI Agent Delegation Template

**Project ID:** `[PROJECT-ID]`  
**Delegation ID:** `[DELEGATION-ID]`  
**Date:** `[DATE]`  
**Status:** `Requested | In Progress | Completed | Rejected`

---

## Delegation Request

### From Agent
**Agent:** `[SOURCE-AGENT]` (e.g., copilot, specifier, simulator)  
**Stage:** `[CURRENT-STAGE]` (e.g., implementation, validation)  
**Task ID:** `[TASK-ID]` (if applicable)

### To Agent
**Target Agent:** `[TARGET-AGENT]` (e.g., specifier, architect, validator, gemini, codex)  
**Required Capability:** `[CAPABILITY]` (e.g., requirement clarification, design review, optimization)

---

## Reason for Delegation

### Issue Description
[Clear description of why delegation is needed]

**Examples:**
- Ambiguous requirement needs clarification
- Architecture design needs revision
- Complex algorithm needs optimization
- Specification incomplete for implementation
- Validation uncovered design flaw

### Blocking Task
**Task ID:** `[TASK-ID]`  
**Task Description:** [Brief description of blocked task]  
**Impact:** [High | Medium | Low]

### Urgency
- [ ] Critical (blocks critical path)
- [ ] High (blocks multiple tasks)
- [ ] Medium (blocks single task)
- [ ] Low (improvement opportunity)

---

## Context Provided

### Relevant Artifacts
List all artifacts the target agent should review:
- `projects/[PROJECT-ID]/artifacts/SPEC.md` - Section [X]
- `projects/[PROJECT-ID]/artifacts/ARCHITECTURE.md` - Component [Y]
- `projects/[PROJECT-ID]/artifacts/execution_plan.yml` - Task [Z]
- [Other relevant files]

### Specific Section/Requirement
**Reference:** [e.g., REQ-F-042, Section 3.2, Component "UserAuth"]  
**Current Content:**
```
[Quote the relevant section that needs attention]
```

### Problem Statement
[Detailed explanation of the specific issue or question]

**Example:**
```
REQ-F-042 states "The system should handle errors appropriately" but doesn't 
specify:
1. What constitutes an "appropriate" error response
2. Which HTTP status codes to use for different error types
3. Whether errors should be logged, and at what level
4. How to handle errors in async operations
```

---

## Requested Output

### Specific Questions
1. [Question 1]
2. [Question 2]
3. [Question 3]

### Expected Deliverable
[Description of what the target agent should produce]

**Examples:**
- Updated specification with clarified requirements
- Revised architecture design for component X
- Optimized task sequence with updated dependencies
- Validation report with recommendations
- Algorithm design with complexity analysis

### Output Location
**File Path:** `projects/[PROJECT-ID]/[TARGET_PATH]`  
**Format:** [Markdown | YAML | JSON | Code]

### Acceptance Criteria
How will we know the delegation is complete and satisfactory?
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

---

## Additional Information

### Related Delegation Requests
- [Link to related delegation if applicable]

### Constraints
[Any constraints the target agent should be aware of]
- Time constraints: [e.g., needed by specific date]
- Technical constraints: [e.g., must use specific technology]
- Budget constraints: [e.g., optimization must not exceed X complexity]

### Preferences
[Any preferences for how to handle this]
- Preferred approach: [if applicable]
- Things to avoid: [if applicable]

---

## Agent Response

### From Target Agent
**Agent:** `[TARGET-AGENT]`  
**Response Date:** `[DATE]`  
**Status:** `Completed | Need More Info | Cannot Complete | Rejected`

### Resolution
[Target agent's response and deliverable]

**Deliverable Location:** `[PATH-TO-OUTPUT]`

### Clarifications Provided
[Any clarifications or explanations from target agent]

### Follow-up Needed
- [ ] No follow-up needed
- [ ] Requesting agent should verify solution
- [ ] Additional delegation may be needed for [X]

---

## Impact Assessment

### Tasks Unblocked
List tasks that can now proceed:
- Task [ID]: [Description]
- Task [ID]: [Description]

### Execution Plan Changes
- [ ] No changes to execution plan
- [ ] Minor adjustments needed
- [ ] Major re-sequencing required
- [ ] New tasks identified

### Timeline Impact
**Original Completion:** [DATE]  
**New Completion:** [DATE]  
**Delta:** [+/- X days]

---

## Lessons Learned

### Root Cause
[Why did this delegation become necessary?]

**Examples:**
- Specification was not detailed enough initially
- Architecture didn't consider edge case
- Requirements changed after specification approval
- Technical complexity was underestimated

### Prevention for Future
[How can we prevent similar delegations in the future?]

**Examples:**
- Add checklist item to specification stage
- Include this scenario in architecture review
- Update quality gate to catch this type of issue
- Add this to agent instruction prompt

### Process Improvement
[Suggested improvements to delegation process itself]

---

## Metadata

**Created By:** [AGENT-NAME]  
**Created At:** [TIMESTAMP]  
**Updated At:** [TIMESTAMP]  
**Priority:** [Critical | High | Medium | Low]  
**Category:** [Clarification | Design | Optimization | Validation | Other]

---

## Notes

[Any additional notes, context, or discussion]

---

## Example Usage

### Example 1: Requirement Clarification

```yaml
delegation_request:
  id: "delegation-001"
  from_agent: "copilot"
  to_agent: "specifier"
  task_id: "task-042"
  reason: "Ambiguous error handling requirement"
  
  context:
    artifact: "SPEC.md"
    section: "REQ-F-042"
    issue: "Error handling not sufficiently detailed"
  
  questions:
    - "What HTTP status codes should be used for validation errors?"
    - "Should all errors be logged? At what level?"
    - "How should async operation errors be communicated to client?"
  
  expected_output:
    type: "Updated SPEC.md"
    location: "projects/project-123/artifacts/SPEC.md"
    sections:
      - "REQ-F-042: Error Handling (updated)"
      - "REQ-NF-007: Logging Requirements (new)"
```

### Example 2: Architecture Revision

```yaml
delegation_request:
  id: "delegation-002"
  from_agent: "copilot"
  to_agent: "architect"
  task_id: "task-089"
  reason: "Discovered scalability issue during implementation"
  
  context:
    artifact: "ARCHITECTURE.md"
    component: "DataProcessor"
    issue: "Current design won't scale to required throughput"
  
  problem:
    description: "Single-threaded processing can handle 100 req/sec but requirement is 1000 req/sec"
    constraint: "Cannot change API contract"
  
  requested_output:
    type: "Revised architecture design"
    focus: "Parallel processing strategy"
    considerations:
      - "Maintain API compatibility"
      - "Handle out-of-order processing"
      - "Ensure data consistency"
```

### Example 3: Algorithm Optimization

```yaml
delegation_request:
  id: "delegation-003"
  from_agent: "copilot"
  to_agent: "simulator"
  task_id: "task-156"
  reason: "Need optimal solution for complex scheduling problem"
  
  context:
    problem: "Task scheduling with dependencies and resource constraints"
    current_approach: "Greedy algorithm, O(n²) complexity"
    issue: "Too slow for production workload (10k tasks)"
  
  requested_output:
    type: "Optimized algorithm design"
    target_complexity: "O(n log n) or better"
    deliverable:
      - "Algorithm description"
      - "Pseudo-code"
      - "Complexity analysis"
      - "Trade-offs discussion"
```

---

## Delegation Decision Tree

```
Is the issue blocking implementation?
├─ Yes → Create delegation request
│  ├─ Requirement unclear? → Delegate to Specifier
│  ├─ Design inadequate? → Delegate to Architect
│  ├─ Algorithm complex? → Delegate to Simulator
│  └─ Need validation? → Delegate to Validator
│
└─ No → Can you proceed with assumptions?
   ├─ Yes → Document assumptions, continue
   └─ No → Create delegation request for guidance
```

---

**Note:** This template facilitates communication between AI agents in the SOMAS pipeline. Each agent can request help from specialized agents while maintaining clear documentation of the delegation process.
