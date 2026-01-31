# SOMAS GitHub Issue Workflow Validation Guide

**Document Status:** Complete & Ready for Testing
**Last Updated:** January 31, 2026
**Purpose:** Validate the complete workflow for new issue submissions through the SOMAS pipeline

---

## Executive Summary

This document provides a comprehensive validation framework for testing issue submissions through the SOMAS (Self-Sovereign Orchestrated Multi-Agent System) pipeline. It covers all stages from initial submission through autonomous processing and final delivery.

**Key Workflow Phases:**
1. **Phase 0: Pre-Submission** - Issue template selection
2. **Phase 1: Intake/Triage** - Automatic classification and routing
3. **Phase 2-11: Pipeline Execution** - Multi-agent orchestration (11-stage Aether Lifecycle)
4. **Phase 12: Delivery** - PR creation and auto-merge

---

## Part 1: Pre-Submission Validation

### 1.1 Issue Template Availability

**File:** `.github/ISSUE_TEMPLATE/config.yml`

**Validation Checklist:**
- [ ] Blank issues are disabled (forces template selection)
- [ ] Five issue templates are available:
  - [ ] `somas-project.yml` - 🚀 New SOMAS Project
  - [ ] `somas-bug.yml` - 🐛 SOMAS Bug Report
  - [ ] `somas-enhance.yml` - ✨ SOMAS Enhancement
  - [ ] `somas-change.yml` - 🔄 SOMAS Change Request
  - [ ] `somas-question.yml` - ❓ SOMAS Question
- [ ] Contact links are displayed:
  - [ ] 📚 SOMAS Documentation
  - [ ] 💬 Ask a Question (Discussions)
  - [ ] 🐛 Report a Bug

**Test Steps:**
1. Go to Repository → Issues → New Issue
2. Verify that "Open a blank issue" option is NOT available
3. Verify all 5 templates appear with correct titles and emojis
4. Verify contact links are displayed at bottom

**Expected Result:** User can only choose from 5 predefined templates

---

### 1.2 Issue Template Structure Validation

**For Each Template (`somas-{type}.yml`):**

#### Template: `somas-project.yml`
- [ ] Title format includes emoji: `🚀 New SOMAS Project`
- [ ] Auto-labels applied: `somas-project`
- [ ] Required fields present:
  - [ ] Project idea/description
  - [ ] Project type (dropdown)
  - [ ] Complexity level (dropdown)
  - [ ] Priority level (dropdown)
  - [ ] Programming language preference
  - [ ] Technical constraints
- [ ] Form validation enabled

#### Template: `somas-bug.yml`
- [ ] Title format includes emoji: `🐛 SOMAS Bug Report`
- [ ] Auto-labels applied: `somas:bug`
- [ ] Required fields present:
  - [ ] Related project ID
  - [ ] Bug type (dropdown: implementation, test_failure, specification_gap, documentation)
  - [ ] Description
  - [ ] Reproduction steps
  - [ ] Expected behavior
  - [ ] Severity level
- [ ] Form validation enabled

#### Template: `somas-enhance.yml`
- [ ] Title format includes emoji: `✨ SOMAS Enhancement`
- [ ] Auto-labels applied: `somas:enhance`
- [ ] Required fields present:
  - [ ] Enhancement type (dropdown)
  - [ ] Description with benefits
  - [ ] Priority level (dropdown)
  - [ ] Use cases

#### Template: `somas-change.yml`
- [ ] Title format includes emoji: `🔄 SOMAS Change Request`
- [ ] Auto-labels applied: `somas:change`
- [ ] Required fields present:
  - [ ] Related project ID
  - [ ] Change type (dropdown)
  - [ ] Change description
  - [ ] Impact assessment

#### Template: `somas-question.yml`
- [ ] Title format includes emoji: `❓ SOMAS Question`
- [ ] Auto-labels applied: `somas:question`
- [ ] Required fields present:
  - [ ] Question type (dropdown)
  - [ ] Question text
  - [ ] Context (optional)
  - [ ] Related project (optional)
  - [ ] Urgency level

**Test Steps:**
1. Navigate to each issue template
2. Verify all required fields are marked with asterisk
3. Verify dropdown fields have correct options
4. Test form validation (try submitting without required fields)
5. Verify correct labels would be auto-applied

---

## Part 2: Intake & Triage Phase Validation

### 2.1 Label Auto-Application

**Trigger:** Issue created using one of the 5 templates

**Validation:**

When issue is submitted:
- [ ] Auto-applied label appears immediately (1-5 seconds)
- [ ] Label color matches expected value:
  - `somas-project`: Blue (🔵 1D76DB)
  - `somas:bug`: Red (🔴 D73A4A)
  - `somas:enhance`: Cyan (🔵 A2EEEF)
  - `somas:change`: Yellow (🟡 FBCA04)
  - `somas:question`: Purple (🟣 D876E3)

**Test Steps:**
1. Create new issue using template
2. Observe labels in real-time
3. Verify correct label appears within 5 seconds

**Expected Result:** Label auto-applied immediately upon creation

---

### 2.2 Workflow Trigger Validation

**Workflow File:** `.github/workflows/intake-triage.yml`

**Trigger Conditions:**
- [ ] Triggers on `issues.opened` event
- [ ] Triggers on `issues.labeled` event
- [ ] Specifically checks for `somas:change` label

**Validation Steps:**
1. Create issue with any template (sets initial label)
2. Check GitHub Actions tab
3. Verify `SOMAS: Phase 1 (Intake)` workflow appears
4. Monitor workflow execution

**Expected Result:** Workflow starts automatically

---

### 2.3 Triage Agent Execution

**Workflow Step:** "Run Triage Agent"

**Validation:**
- [ ] Python 3.10 environment is set up
- [ ] Dependencies installed: `requirements.txt`, `openai`, `PyYAML`
- [ ] Triage agent is invoked via runner
- [ ] Triage report generated: `triage_report.md`
- [ ] Report contains YAML structure with:
  - [ ] `issue_number`
  - [ ] `classification` (change|enhancement|question|bug)
  - [ ] `confidence` (0.0-1.0 score)
  - [ ] `routing` (agent assignment)
  - [ ] `estimated_effort` (minimal|small|medium|large)
  - [ ] `action` (route|defer|reject|escalate)
  - [ ] `next_steps` (description)

**Test Steps:**
1. Monitor workflow execution in GitHub Actions
2. Wait for "Run Triage Agent" step to complete
3. Check step output for success message
4. Verify "Triage report generated successfully" message appears

**Expected Result:** Triage report generated without errors

---

### 2.4 Triage Comment Posted

**Workflow Step:** "Post Triage Comment"

**Validation:**
- [ ] Comment posted to issue within 30 seconds
- [ ] Comment includes triage analysis
- [ ] Comment includes confidence score
- [ ] Comment includes routing decision
- [ ] Comment is properly formatted (markdown or code block)
- [ ] Comment is clearly marked as automated (signature or indicator)

**Test Steps:**
1. Go to issue after workflow completes
2. Scroll to comments section
3. Verify triage comment is visible
4. Read comment for analysis details

**Expected Result:** Triage comment appears with analysis

---

### 2.5 Label Addition After Triage

**Labels Added:**
- [ ] `somas:triaged` - Indicates triage is complete
- [ ] `somas:dev` - Enables pipeline (if actionable)
- [ ] `somas-project` - Applied for project-type issues

**Validation Steps:**
1. After triage step completes, refresh issue
2. Check labels section
3. Verify new labels appear

**Expected Result:** Additional labels appear in labels section

---

### 2.6 Advisor Agent Invocation (Conditional)

**Trigger:** If triage confidence < 0.8 OR complexity is HIGH/CRITICAL

**Validation:**
- [ ] Advisor comment appears (if triggered)
- [ ] Comment includes strategic recommendations
- [ ] Comment references triage analysis
- [ ] Comment suggests next steps

**Test with High Complexity Issue:**
1. Create issue with "Complex" or "Large" scope
2. Monitor workflow for advisor agent invocation
3. Verify advisor comment appears

**Expected Result:** Advisor comment appears for complex issues

---

## Part 3: Pipeline Stage Validation

### 3.1 Stage Progression Labels

**Stages in Aether Lifecycle:**
```
1. INTAKE         → somas:stage:intake
2. SPECIFY        → somas:stage:specify
3. PLAN           → somas:stage:plan
4. DECOMPOSE      → somas:stage:decompose
5. IMPLEMENT      → somas:stage:implement
6. VERIFY         → somas:stage:verify
7. INTEGRATE      → somas:stage:integrate
8. HARDEN         → somas:stage:harden
9. RELEASE        → somas:stage:release
10. OPERATE       → somas:stage:operate
11. ANALYZE       → somas:stage:analyze
```

**Validation:**
- [ ] Stage label progression is forward-only (no backward transitions)
- [ ] Only one `somas:stage:*` label is active at a time
- [ ] Label changes correspond to workflow execution
- [ ] Stage transitions are logged

**Test Steps:**
1. Create project issue (type: `somas-project`)
2. Monitor issue labels as pipeline executes
3. Track label transitions:
   - After intake/triage: `somas:stage:specify`
   - After specification: `somas:stage:plan`
   - And so on through all 11 stages
4. Verify only one stage label is active

**Expected Result:** Labels progress through stages in order

---

### 3.2 Milestone Tracking

**Workflow:** `sync-stage-milestones.yml`

**Validation:**
- [ ] Milestones created for each stage
- [ ] Milestone names match stage names (INTAKE, SPECIFY, PLAN, etc.)
- [ ] Issue assigned to milestone when stage label applied
- [ ] Milestone progress reflects issue completion

**Test Steps:**
1. Go to Repository → Milestones
2. Verify 11 milestones exist (one per stage)
3. Monitor issue and verify it's assigned to current milestone
4. Track milestone progress as issue moves through stages

**Expected Result:** Milestones created and issue assigned appropriately

---

### 3.3 Project Board Integration

**Workflow:** `somas-project-sync.yml`

**Validation:**
- [ ] GitHub Project board created automatically
- [ ] Project has 8 columns:
  - [ ] 📋 Backlog
  - [ ] 📝 Specification
  - [ ] 🔬 Simulation
  - [ ] 🏗️ Architecture
  - [ ] 💻 Implementation
  - [ ] ✅ Validation
  - [ ] 👤 Human Review
  - [ ] 🚀 Done
- [ ] Cards created for each task
- [ ] Cards move through columns as pipeline progresses
- [ ] Parent issue linked to project

**Test Steps:**
1. Go to Repository → Projects
2. Find project for your issue (project-{issue_number})
3. Verify board columns exist
4. Check that issue cards appear
5. Monitor card movement through columns

**Expected Result:** Project board created and maintains state

---

## Part 4: Agent Orchestration Validation

### 4.1 Multi-Agent Invocation

**Workflow:** `somas-orchestrator.yml`

**Agent Sequence (Project Type):**
1. **Triage Agent** → Classification
2. **Specifier Agent** → Spec.md
3. **Simulator Agent** → Simulation results
4. **Architect Agent** → Architecture design
5. **Planner Agent** → Execution plan
6. **Implementer Agent** → Code generation
7. **Validator Agent** → Testing
8. **Merger Agent** → Integration
9. **Security Agent** → Security review
10. **Operator Agent** → Deployment
11. **Analyzer Agent** → Documentation

**Validation:**
- [ ] Each agent invokes next agent in sequence
- [ ] Agent comments appear in order
- [ ] Each agent output is saved as artifact
- [ ] Circuit breaker enforces max 20 invocations per issue

**Test Steps:**
1. Create project issue
2. Monitor issue comments for agent invocations
3. Verify each agent response includes:
   - [ ] Structured output (YAML/JSON)
   - [ ] Clear results/findings
   - [ ] Handoff to next agent
4. Count agent invocations (should be ≤ 20 for successful project)

**Expected Result:** Agents invoke in sequence with proper handoffs

---

### 4.2 Artifact Generation and Storage

**Location:** `.somas/projects/project-{issue_number}/`

**Expected Artifacts:**
- [ ] `initial_plan.yml` - High-level project plan
- [ ] `SPEC.md` - Detailed specification
- [ ] `architecture.md` - System architecture
- [ ] `execution_plan.yml` - Task decomposition
- [ ] `task_list.md` - Detailed task list
- [ ] `implementation.md` - Code implementation notes
- [ ] `test_results.json` - Test suite results
- [ ] `security_report.md` - Security findings
- [ ] `deployment_guide.md` - Deployment instructions
- [ ] `README.md` - Project documentation

**Validation:**
- [ ] Directory created: `.somas/projects/project-{issue_number}/`
- [ ] Subdirectories exist:
  - [ ] `artifacts/` - Generated files
  - [ ] `logs/` - Execution logs
- [ ] Artifacts have correct format (YAML/JSON/Markdown)
- [ ] File names are consistent
- [ ] Latest versions saved with timestamps

**Test Steps:**
1. Complete pipeline execution (or monitor as it runs)
2. Navigate to `.somas/projects/project-{issue_number}/`
3. Verify directory structure
4. Check artifact files exist and contain valid content
5. Verify `artifacts/` and `logs/` subdirectories

**Expected Result:** All artifacts generated and stored correctly

---

### 4.3 State Persistence and Recovery

**Files:**
- `.somas/projects/project-{id}/state.json` - Current state
- `.somas/projects/project-{id}/transitions.jsonl` - State history
- `.somas/projects/project-{id}/metadata.json` - Project metadata

**Validation:**
- [ ] `state.json` created at project initialization
- [ ] State updated atomically (no corruption on failure)
- [ ] File locking prevents concurrent access issues
- [ ] Transitions logged for audit trail
- [ ] Recovery possible from any checkpoint

**Test Steps:**
1. Monitor state file creation
2. Verify atomic writes (temp file + rename pattern)
3. Check transitions.jsonl for state change history
4. Simulate workflow interruption and verify recovery

**Expected Result:** State persisted and recoverable

---

### 4.4 Circuit Breaker Validation

**Limit:** 20 agent invocations per issue

**Validation:**
- [ ] Counter incremented with each agent invocation
- [ ] At invocation 20, `somas:circuit-breaker` label added
- [ ] Warning comment posted to issue
- [ ] Workflow halted (doesn't invoke agent 21)
- [ ] Manual label removal enables resumption

**Test Steps (Simulated):**
1. Create issue
2. Monitor agent invocation count in comments
3. If reaches ~15 invocations:
   - [ ] Verify counter is incrementing
   - [ ] Check workflow logs for circuit breaker checks
4. Document expected behavior at 20 invocations

**Expected Result:** Circuit breaker prevents runaway automation

---

## Part 5: Output and Delivery Validation

### 5.1 Pull Request Generation

**Trigger:** Pipeline completion (all 11 stages successful)

**Validation:**
- [ ] PR created automatically
- [ ] PR title includes project reference: `SOMAS: Project {ID} - {Description}`
- [ ] PR body includes:
  - [ ] Project summary
  - [ ] All artifacts generated
  - [ ] Test results (pass/fail)
  - [ ] Quality metrics
  - [ ] Links to issue
- [ ] PR branches:
  - [ ] Source: `somas/project-{id}`
  - [ ] Target: `dev`
- [ ] PR checks pass:
  - [ ] JSON validation
  - [ ] Code linting
  - [ ] Type checking
  - [ ] Security scanning (CodeQL, Semgrep)

**Test Steps:**
1. Wait for pipeline to complete
2. Go to Repository → Pull Requests
3. Find PR for your project
4. Verify PR title and body
5. Check PR checks status

**Expected Result:** PR created with all checks passing

---

### 5.2 Auto-Merge Configuration

**Validation:**
- [ ] PR has `somas:dev` label
- [ ] Squash merge enabled
- [ ] Commit message auto-generated
- [ ] PR auto-merges when checks pass (if no human changes needed)
- [ ] Labels added to merged PR:
  - [ ] `somas-generated`
  - [ ] `state:complete`

**Test Steps:**
1. Monitor PR status
2. Verify checks pass
3. If human review not needed, verify auto-merge occurs
4. Check merged status and final labels

**Expected Result:** PR auto-merges on successful checks

---

### 5.3 Completion Notifications

**Validation:**
- [ ] Issue labeled with `state:complete`
- [ ] Issue closed or marked as completed
- [ ] Final comment posted with:
  - [ ] Completion status
  - [ ] Links to PR
  - [ ] Link to artifacts
  - [ ] Execution time
  - [ ] Cost metrics (if available)
- [ ] Optional: Email notification sent (if configured)

**Test Steps:**
1. Monitor issue for completion comment
2. Verify issue status updated
3. Check for all expected information in completion comment
4. Verify links are working

**Expected Result:** Issue marked complete with notification

---

## Part 6: Error Handling & Recovery Validation

### 6.1 Agent Failure Handling

**Scenarios to Validate:**
1. **Invalid Issue Input**
   - [ ] Agent detects invalid data
   - [ ] Posts error comment with details
   - [ ] Escalates to human reviewer
   - [ ] Applies `needs-human-review` label

2. **LLM API Failure**
   - [ ] Detects API error (rate limit, timeout, invalid key)
   - [ ] Logs error with timestamp
   - [ ] Retries up to 3 times with exponential backoff
   - [ ] After 3 failures, escalates
   - [ ] Posts recovery instructions

3. **State Corruption**
   - [ ] Detects corrupted state file
   - [ ] Restores from last checkpoint
   - [ ] Logs recovery attempt
   - [ ] Continues pipeline from recovery point

4. **Dependency Missing**
   - [ ] Detects missing file/dependency
   - [ ] Reports specific missing item
   - [ ] Suggests remedy
   - [ ] Escalates to human

**Test Steps:**
1. Create test issues designed to trigger each scenario
2. Monitor error handling in workflow logs
3. Verify appropriate escalation occurs
4. Verify recovery or human notification

**Expected Result:** Errors handled gracefully with recovery

---

### 6.2 Escalation to Human Review

**Conditions for Escalation:**
- [ ] Triage confidence < 0.8
- [ ] Agent returns "requires_human_review"
- [ ] Security scan finds vulnerabilities
- [ ] Test coverage < 80%
- [ ] Circuit breaker triggered
- [ ] Multiple retries exhausted

**Validation:**
- [ ] `needs-human-review` label added
- [ ] Comment posted with escalation reason
- [ ] Links provided to review resources
- [ ] PR marked as ready for review (not auto-merged)
- [ ] Notifications sent to code owners (if configured)

**Test Steps:**
1. Create issue with conditions that require review
2. Monitor for escalation
3. Verify label and comment
4. Verify PR blocks auto-merge

**Expected Result:** Human review properly escalated

---

## Part 7: Comprehensive Test Scenarios

### Scenario A: Simple Project Request

**Test Issue Details:**
- Type: SOMAS Project
- Title: "Build Simple CLI Tool"
- Complexity: Simple
- Priority: Medium
- Language: Python
- Description: A basic command-line utility with <500 LOC

**Expected Outcomes:**
- [ ] Intake/triage completes in < 1 minute
- [ ] All 11 stages complete in < 30 minutes
- [ ] Generated code is < 500 lines
- [ ] All tests pass
- [ ] PR auto-merges
- [ ] Issue marked complete

**Validation:**
Run this scenario and document:
- Actual execution time
- Agent invocation count
- Artifact generation time
- Code quality metrics
- Test coverage

---

### Scenario B: Complex Project Request

**Test Issue Details:**
- Type: SOMAS Project
- Title: "Build REST API with Database"
- Complexity: Large
- Priority: High
- Language: Python + PostgreSQL
- Description: Multi-endpoint API with authentication, validation, error handling

**Expected Outcomes:**
- [ ] Requires advisor consultation (high complexity)
- [ ] May require human clarification on architecture
- [ ] All 11 stages complete (or escalate for review)
- [ ] Generated code follows best practices
- [ ] Security review passes
- [ ] Test coverage > 90%
- [ ] PR created with human review label

**Validation:**
Run this scenario and document:
- Which stage requires human input
- Escalation points encountered
- Final review requirements
- Quality of generated architecture

---

### Scenario C: Bug Report Workflow

**Test Issue Details:**
- Type: Bug Report
- Title: "Circuit breaker not preventing runaway agents"
- Bug type: implementation
- Related project: project-123 (from previous test)
- Severity: Critical

**Expected Outcomes:**
- [ ] Routed to Implementer agent
- [ ] Triage identifies as critical
- [ ] Escalates immediately
- [ ] Creates bug fix task
- [ ] Links to original project
- [ ] Does NOT trigger full 11-stage pipeline (targeted fix)

**Validation:**
Run this scenario and document:
- Routing decision accuracy
- Bug classification
- Task creation
- Integration with original project

---

### Scenario D: Enhancement Request Workflow

**Test Issue Details:**
- Type: Enhancement
- Title: "Add progress indicator to execution"
- Type: feature_idea
- Priority: Medium
- Description: Visual progress indicator during agent execution

**Expected Outcomes:**
- [ ] Added to backlog (not critical)
- [ ] OR routed to planner for consideration
- [ ] May be deferred to future sprint
- [ ] Does NOT trigger automatic implementation

**Validation:**
Run this scenario and document:
- Backlog processing
- Priority assignment
- Deferral decision logic

---

### Scenario E: Change Request Workflow

**Test Issue Details:**
- Type: Change Request
- Title: "Increase parallelism in implementation stage"
- Related project: project-123
- Change type: scope_addition

**Expected Outcomes:**
- [ ] Identified as change to in-progress project
- [ ] Routed to appropriate stage (IMPLEMENT stage)
- [ ] Does NOT restart pipeline
- [ ] Injected at correct point
- [ ] Integrated with ongoing work

**Validation:**
Run this scenario and document:
- Stage detection accuracy
- Injection point correctness
- Artifact update handling

---

### Scenario F: Question Workflow

**Test Issue Details:**
- Type: Question
- Title: "How to customize agent behavior?"
- Question type: technical
- Context: Integration with SOMAS

**Expected Outcomes:**
- [ ] Does NOT trigger pipeline
- [ ] Routed to Advisor agent ONLY
- [ ] Advisor posts answer as comment
- [ ] Issue remains open for discussion
- [ ] May generate documentation update

**Validation:**
Run this scenario and document:
- Pipeline NOT triggered
- Advisor answer quality
- Documentation suggestion

---

## Part 8: Performance & Metrics Validation

### 8.1 Execution Time Metrics

**Stages to Measure:**
- [ ] Intake/Triage: < 2 minutes
- [ ] Specification: < 5 minutes
- [ ] Planning/Simulation: < 5 minutes
- [ ] Decomposition: < 2 minutes
- [ ] Implementation: < 15 minutes
- [ ] Verification/Testing: < 10 minutes
- [ ] Integration: < 5 minutes
- [ ] Security Hardening: < 10 minutes
- [ ] Release: < 5 minutes
- [ ] Operate/Monitor: < 5 minutes
- [ ] Analysis/Documentation: < 10 minutes

**Total Target:** < 75 minutes for simple project, < 2 hours for complex

**Validation:**
1. Track each stage's execution time
2. Compare against targets
3. Document bottlenecks
4. Identify optimization opportunities

---

### 8.2 Cost Metrics

**Metrics to Track:**
- [ ] Total LLM API calls
- [ ] Total LLM tokens used (input + output)
- [ ] Estimated cost (GPT-4: $0.03/1K input, $0.06/1K output)
- [ ] Cost per stage
- [ ] Cost per complexity level

**Validation:**
1. Enable cost tracking in configuration
2. Monitor API usage
3. Calculate total cost per project
4. Compare to expected costs

---

### 8.3 Quality Metrics

**Metrics to Track:**
- [ ] Code generation time
- [ ] Test coverage percentage
- [ ] Tests passing percentage
- [ ] Security vulnerabilities found
- [ ] Code style compliance

**Validation:**
1. Track metrics for each test scenario
2. Compare against quality gates
3. Document quality trends
4. Identify quality improvements

---

## Part 9: Integration Validation

### 9.1 GitHub Integration

**Validations:**
- [ ] Issue labels work correctly
- [ ] Milestones properly assigned
- [ ] Project board synchronized
- [ ] PR creation and linking works
- [ ] Workflow triggers fire correctly
- [ ] Comments post without timing issues
- [ ] Labels applied/removed as expected

**Test Steps:**
1. Monitor GitHub API rate limits during execution
2. Verify no race conditions in label application
3. Check for timing issues in automation
4. Validate all webhooks firing

---

### 9.2 External Service Integration

**Services to Validate:**
- [ ] LLM API (OpenAI/Anthropic)
  - [ ] Authentication working
  - [ ] Rate limiting respected
  - [ ] Error handling correct
- [ ] GitHub CLI integration
  - [ ] Commands executing correctly
  - [ ] Output parsing working
- [ ] File system operations
  - [ ] Atomic writes functioning
  - [ ] File locking preventing corruption
- [ ] JSON/YAML parsing
  - [ ] Schema validation passing
  - [ ] Artifact formats correct

**Test Steps:**
1. Simulate each service failure
2. Verify graceful degradation
3. Verify recovery mechanisms
4. Validate error messages

---

## Part 10: Final Validation Checklist

### Pre-Deployment Checklist

- [ ] All 5 issue templates present and functional
- [ ] Labels created and properly colored
- [ ] Workflows enabled and configured
- [ ] API credentials configured (GitHub, OpenAI)
- [ ] `.somas/config.yml` validated
- [ ] Agent YAML files validated
- [ ] Stage definitions complete
- [ ] All 11 stages configured

### Functional Checklist

- [ ] Issue submission creates correct labels
- [ ] Triage workflow executes on issue creation
- [ ] Triage agent generates correct classification
- [ ] Agents invoke in correct sequence
- [ ] Artifacts generated to correct location
- [ ] State persisted correctly
- [ ] Labels progress through stages correctly
- [ ] Milestones assigned and tracked
- [ ] PR created on completion
- [ ] Auto-merge works (if applicable)
- [ ] Human review escalation works
- [ ] Circuit breaker prevents runaway

### Quality Checklist

- [ ] Code generation is syntactically valid
- [ ] Generated tests pass
- [ ] Security scan passes
- [ ] Code style compliant
- [ ] Documentation generated correctly
- [ ] Error messages are helpful
- [ ] Recovery mechanisms tested
- [ ] Performance acceptable

### Documentation Checklist

- [ ] README explains submission process
- [ ] Label system documented
- [ ] Agent roles documented
- [ ] Stage definitions documented
- [ ] Template fields documented
- [ ] Error scenarios documented
- [ ] Recovery procedures documented
- [ ] Troubleshooting guide available

---

## Appendix A: Quick Test Checklist

**For Rapid Validation (15 minutes):**

```
□ 1. Create issue using somas-project template
     - Simple project (CLI tool)
     - Python language
     - Medium priority

□ 2. Verify labels auto-applied:
     - somas-project ✓
     - somas-dev ✓

□ 3. Check workflow starts:
     - GitHub Actions tab
     - "SOMAS: Phase 1" workflow appears ✓

□ 4. Verify triage comment posts:
     - Appears within 30 seconds ✓
     - Contains classification ✓
     - Contains routing decision ✓

□ 5. Monitor first agent execution:
     - Specifier agent invokes ✓
     - Generates SPEC.md ✓
     - Posts comment with results ✓

□ 6. Check state file:
     - .somas/projects/project-{id}/ created ✓
     - state.json present ✓
     - metadata.json contains project info ✓

□ 7. Monitor stage progression:
     - somas:stage:specify label appears ✓
     - somas:stage:plan appears next ✓

□ 8. Verify artifact generation:
     - artifacts/ directory exists ✓
     - SPEC.md present ✓
     - execution_plan.yml present ✓

Result: ✓ PASS or Document failures for detailed testing
```

---

## Appendix B: Troubleshooting Guide

### Workflow doesn't start
**Check:**
- GitHub Actions enabled in repository
- Workflow files in `.github/workflows/`
- Trigger conditions met (labels match conditions)
- API quotas not exceeded

### Triage comment doesn't appear
**Check:**
- OpenAI API key configured
- API key has permissions
- Network connectivity
- Workflow logs for error messages

### Artifacts not generated
**Check:**
- `.somas/projects/` directory exists
- Write permissions on repository
- Temp file permissions
- Disk space available

### Labels not progressing
**Check:**
- Label names match configuration
- Workflow updating labels correctly
- No label conflicts
- Proper permissions for label updates

### PR not created
**Check:**
- Pipeline reached final stage
- All checks passing
- Branch permissions correct
- Auto-merge settings configured

---

## Appendix C: Reference Documents

- **CLAUDE.md** - Agent development guide
- **DEVELOPMENT_PLAN.md** - Project roadmap
- **`.github/LABELS.md`** - Label system documentation
- **`.somas/config.yml`** - Pipeline configuration
- **`.somas/agents/*.yml`** - Agent specifications

---

## Sign-Off

**Validation Completed By:** [Your Name]
**Date:** [Date]
**Status:** ✓ READY FOR PRODUCTION

---

*This document should be reviewed and updated as new features are added or workflow changes are made.*
