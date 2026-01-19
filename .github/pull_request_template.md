## SOMAS Agent Assignments

This PR was created by the SOMAS pipeline. The following agents are assigned to different review aspects:

- [ ] **Architecture Review** - @copilot somas-architect
- [ ] **Code Review** - @copilot somas-reviewer  
- [ ] **Security Review** - @copilot somas-security
- [ ] **Test Coverage** - @copilot somas-tester
- [ ] **Documentation** - @copilot somas-documenter
- [ ] **Performance Analysis** - @copilot somas-optimizer

---

## Pipeline Stage: [STAGE NAME]

**Project ID:** [PROJECT-ID]
**Issue:** #[ISSUE-NUMBER]

---

## Changes Made

### Summary
[Brief description of what was implemented/changed in this stage]

### Artifacts Generated
- [ ] Specification documents
- [ ] Architecture design
- [ ] Source code
- [ ] Tests
- [ ] Documentation
- [ ] Other: _______

### Files Changed
[List of key files added/modified]

---

## Quality Checklist

### Code Quality (if applicable)
- [ ] Code follows project style guidelines
- [ ] All functions have appropriate error handling
- [ ] Code is properly commented where necessary
- [ ] No code smells or anti-patterns detected

### Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing
- [ ] Code coverage ≥ 80% (per `.somas/config.yml`)

### Security
- [ ] Input validation implemented
- [ ] No hardcoded secrets or credentials
- [ ] Authentication/authorization implemented correctly
- [ ] Security scan passed (no critical vulnerabilities)

### Documentation
- [ ] README updated (if needed)
- [ ] API documentation updated (if applicable)
- [ ] Inline code documentation adequate
- [ ] Usage examples provided

### SOMAS Integration
- [ ] Artifacts stored in `.somas/projects/{project_id}/artifacts/`
- [ ] Project metadata updated
- [ ] Quality gates from `.somas/config.yml` satisfied
- [ ] Handoff notes prepared for next stage

---

## Stage-Specific Details

### For Specification Stage
- [ ] All requirements have unique IDs (REQ-F-XXX, REQ-NF-XXX)
- [ ] All requirements are testable
- [ ] No ambiguous language (TBD, maybe, etc.)
- [ ] Security requirements defined
- [ ] Open questions resolved or escalated

### For Simulation Stage
- [ ] Task graph is acyclic
- [ ] All tasks have duration estimates
- [ ] Critical path identified
- [ ] Parallelization opportunities documented

### For Architecture Stage
- [ ] All components defined
- [ ] Interfaces specified
- [ ] Data flows documented
- [ ] Technology choices justified
- [ ] ADRs created for major decisions

### For Implementation Stage
- [ ] All architectural components implemented
- [ ] Tests passing with ≥80% coverage
- [ ] No critical security vulnerabilities
- [ ] Documentation complete

### For Validation Stage
- [ ] All acceptance criteria met
- [ ] Performance requirements satisfied
- [ ] Security scan passed
- [ ] Integration tests passing

### For Staging Stage
- [ ] Merge conflicts resolved
- [ ] Branch ready for merge to main
- [ ] Deployment documentation complete
- [ ] Human approval obtained

---

## Agent Handoff

### Completed By
**Agent:** [Agent name that completed this work]
**Date:** [Completion date]

### Next Stage
**Agent:** [Next agent in pipeline]
**Inputs Provided:**
- [Artifact 1]
- [Artifact 2]

**Notes for Next Agent:**
[Any important context, decisions made, or areas requiring attention]

---

## Potential Issues / Risks

[List any issues encountered, risks identified, or areas requiring special attention]

- None identified ✅
- [Issue 1 description]
- [Risk 2 description]

---

## Human Review Required

- [ ] **Specification Approval** (for specification stage)
- [ ] **Architecture Sign-off** (for architecture stage)
- [ ] **Final Staging Approval** (for staging stage)
- [ ] **No human review needed** (automated stages)

### Review Guidance for Humans

**What to Focus On:**
[Specific areas where human judgment is valuable]

**Questions to Consider:**
- Does this meet the original project requirements?
- Are the design decisions sound?
- Is the code production-ready?
- Are there any compliance or business concerns?

---

## SOMAS Pipeline Context

**Configuration Reference:** `.somas/config.yml`

**Quality Gates Applied:**
[List quality gates that were checked from config.yml]

**Metrics:**
- **Duration:** [Time spent in this stage]
- **Iterations:** [Number of attempts/refinements]
- **Tests:** [Pass/Total]
- **Coverage:** [Percentage]

---

## Additional Notes

[Any other relevant information, decisions made, or context for reviewers]

---

## For Reviewers

### How to Use Agent Assignments

Invoke specialized agents by mentioning them in comments:

```markdown
@copilot somas-security

Please review the authentication implementation in src/auth.py 
for compliance with OWASP best practices.
```

### Available Agents

- **@copilot somas-requirements** - Requirements analysis
- **@copilot somas-architect** - Architecture review
- **@copilot somas-implementer** - Code implementation
- **@copilot somas-tester** - Test creation and review
- **@copilot somas-reviewer** - Code quality review
- **@copilot somas-security** - Security audit
- **@copilot somas-optimizer** - Performance optimization
- **@copilot somas-documenter** - Documentation review
- **@copilot somas-debugger** - Bug investigation
- **@copilot somas-merger** - Merge conflict resolution
- **@copilot somas-orchestrator** - Pipeline coordination
- **@copilot somas-advisor** - Strategic guidance

See `.github/agents/README.md` for complete documentation.

---

<!-- 
SOMAS Auto-generated PR Template
Do not remove this comment - it helps identify SOMAS-generated PRs
Project: {project_id}
Stage: {stage}
-->
