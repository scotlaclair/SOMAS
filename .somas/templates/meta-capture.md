# Meta-Captured Recommendation

**Source:** PR #`[PR-NUMBER]` - [View Discussion](`[COMMENT-LINK]`)  
**Captured Date:** `[DATE]`  
**Captured By:** `[AGENT/USER]`  
**Status:** `New | Routed | In Progress | Completed | Archived`

---

## Recommendation Summary

`[Brief 1-2 sentence summary of the recommendation]`

---

## Full Recommendation Content

### Category
- [ ] Architecture
- [ ] Process
- [ ] Configuration
- [ ] Testing
- [ ] Security
- [ ] Performance
- [ ] Documentation
- [ ] Other: `_______`

### Priority Level
- [ ] Must Address Soon (create follow-up issue)
- [ ] Should Consider (add to backlog)
- [ ] Future Enhancement (add to roadmap)
- [ ] Informational (reference only)

### Original Content

```
[Copy the full recommendation text from the PR review comment]
```

---

## Context

### Related PR Information
- **PR Title:** `[PR-TITLE]`
- **PR Description:** `[Brief excerpt of what the PR addressed]`
- **Changed Files:** `[Key files changed in the PR]`
- **Labels:** `[PR labels]`

### Discussion Thread
`[Link to specific comment thread if applicable]`

### Related Components/Features
- Component: `[Component name]`
- Stage: `[Pipeline stage]`
- Agents Involved: `[Agent names]`

---

## Suggested Routing

### Primary Action
- [ ] Create follow-up issue with `somas:follow-up` label
- [ ] Incorporate into Architecture Decision Record (ADR)
- [ ] Add to `.somas/backlog.md`
- [ ] Add to `.somas/roadmap.md`
- [ ] Update existing documentation
- [ ] Assign to project owner for immediate action

### Secondary Actions
- [ ] Update agent instructions in `.somas/agents/`
- [ ] Add to quality gate checklist
- [ ] Update configuration templates
- [ ] Add to security review checklist
- [ ] Document in lessons learned

---

## Routing Details

### If Creating Issue
**Issue Title:** `[CHANGE] [Brief description from recommendation]`  
**Issue Type:** Change | Enhancement | Bug | Question  
**Labels:** `somas:follow-up`, `[other-labels]`  
**Assignee:** `[username or leave empty]`  
**Project ID:** `[project-id if applicable]`

### If Creating ADR
**ADR Title:** `[ADR-XXX: Decision Title]`  
**ADR Path:** `.somas/architecture/ADRs/ADR-XXX-[slug].md`  
**Decision Category:** Architecture | Process | Technology | Security

### If Adding to Backlog/Roadmap
**Target File:** `.somas/backlog.md` | `.somas/roadmap.md`  
**Section:** `[Section name in the file]`  
**Estimated Effort:** Small | Medium | Large | Unknown

---

## Impact Assessment

### Affects
- [ ] Specifications
- [ ] Architecture
- [ ] Implementation
- [ ] Testing
- [ ] Documentation
- [ ] Configuration
- [ ] Security
- [ ] Performance

### Scope
- [ ] Single component/feature
- [ ] Multiple components
- [ ] System-wide
- [ ] Process/workflow
- [ ] Cross-project

### Urgency Rationale
`[Explanation of why this is classified at the chosen priority level]`

---

## Implementation Notes

### Prerequisites
`[What needs to be in place before this can be addressed?]`

### Constraints
`[Any technical, resource, or timeline constraints to consider]`

### Suggested Approach
`[If the recommendation included implementation guidance, capture it here]`

### Related Work
- Related Issue: `#[issue-number]`
- Related PR: `#[pr-number]`
- Related ADR: `ADR-XXX`

---

## Follow-up Actions

### Immediate (Within 1-2 sprints)
- [ ] Action 1
- [ ] Action 2

### Short-term (2-4 sprints)
- [ ] Action 1
- [ ] Action 2

### Long-term (Backlog/Roadmap)
- [ ] Action 1
- [ ] Action 2

---

## Review and Approval

### Reviewed By
**Reviewer:** `[Reviewer name/agent]`  
**Review Date:** `[DATE]`  
**Decision:** Approved | Modified | Rejected | Deferred  
**Notes:** `[Any review comments]`

### Owner Assignment
**Owner:** `[Assigned owner]`  
**Expected Completion:** `[Date or milestone]`

---

## Completion Tracking

### Deliverables
- [ ] Issue created: `#[issue-number]`
- [ ] ADR created: `[ADR path]`
- [ ] Backlog/Roadmap updated: `[commit link]`
- [ ] Documentation updated: `[file paths]`
- [ ] Configuration updated: `[file paths]`

### Verification
- [ ] Implementation completed
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Reviewed and approved
- [ ] Merged to main

### Closure
**Closed Date:** `[DATE]`  
**Closed By:** `[Agent/user]`  
**Final Status:** `Completed | Superseded | Obsolete | Rejected`  
**Outcome:** `[Brief description of what was accomplished]`

---

## Notes and Discussion

`[Any additional notes, clarifications, or discussion about this recommendation]`

---

## Metadata

**Created At:** `[TIMESTAMP]`  
**Updated At:** `[TIMESTAMP]`  
**Version:** `1.0`  
**Tags:** `[tag1, tag2, tag3]`  
**Related Projects:** `[project-id-1, project-id-2]`

---

## Example Usage

### Example 1: Must Address Soon - Circuit Breaker Enhancement

```yaml
meta_capture:
  source: "PR #28"
  category: "Configuration"
  priority: "Must Address Soon"
  
  recommendation:
    summary: "Add circuit breaker state persistence across restarts"
    content: |
      Circuit breaker state is currently in-memory only. For production
      deployments, state should persist across service restarts to avoid
      all breakers resetting simultaneously and causing a thundering herd.
    
  routing:
    primary_action: "Create follow-up issue"
    issue_title: "[CHANGE] Add circuit breaker state persistence"
    labels: ["somas:follow-up", "somas:enhancement", "priority:high"]
    
  impact:
    affects: ["Configuration", "Architecture"]
    scope: "System-wide"
    urgency: "High - needed before production deployment"
```

### Example 2: Future Enhancement - Advanced Simulation

```yaml
meta_capture:
  source: "PR #26"
  category: "Performance"
  priority: "Future Enhancement"
  
  recommendation:
    summary: "Monte Carlo simulation could benefit from adaptive sampling"
    content: |
      Current simulation uses fixed sample size. For complex projects,
      adaptive sampling could reduce computation time while maintaining
      accuracy by focusing samples on high-variance task sequences.
    
  routing:
    primary_action: "Add to roadmap"
    target_file: ".somas/roadmap.md"
    section: "Optimization & Performance"
    
  impact:
    affects: ["Performance"]
    scope: "Single component"
    urgency: "Low - optimization opportunity"
```

### Example 3: Architecture Decision - ADR Creation

```yaml
meta_capture:
  source: "PR #28"
  category: "Architecture"
  priority: "Must Address Soon"
  
  recommendation:
    summary: "Document circuit breaker threshold decision rationale"
    content: |
      The choice of 5-failure threshold and 60-second timeout should be
      documented in an ADR with analysis of alternatives and trade-offs.
    
  routing:
    primary_action: "Create ADR"
    adr_title: "ADR-001: Circuit Breaker Thresholds"
    adr_path: ".somas/architecture/ADRs/ADR-001-circuit-breaker-thresholds.md"
    
  impact:
    affects: ["Architecture", "Documentation"]
    scope: "System-wide"
    urgency: "Medium - needed for architectural clarity"
```

---

**Note:** This template facilitates capturing valuable recommendations from PR reviews and routing them to appropriate artifacts (issues, ADRs, backlog, roadmap) to ensure institutional knowledge is preserved and actionable.
