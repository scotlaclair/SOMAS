# SOMAS GitHub Issue Workflow - Visual Diagram

## Complete Workflow Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   SOMAS GITHUB ISSUE WORKFLOW PIPELINE                       │
│                        (Self-Sovereign Multi-Agent System)                    │
└─────────────────────────────────────────────────────────────────────────────┘

                              PHASE 0: PRE-SUBMISSION
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                               │
│  User Initiates New Issue                                                   │
│         │                                                                     │
│         ├─→ Repository Issues Tab                                            │
│         │                                                                     │
│         ├─→ Select Issue Template:                                           │
│         │   ├─ 🚀 SOMAS Project         (somas-project.yml)                 │
│         │   ├─ 🐛 Bug Report            (somas-bug.yml)                     │
│         │   ├─ ✨ Enhancement            (somas-enhance.yml)                │
│         │   ├─ 🔄 Change Request        (somas-change.yml)                  │
│         │   └─ ❓ Question               (somas-question.yml)               │
│         │                                                                     │
│         └─→ Fill Required Fields & Submit                                    │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘

                              PHASE 1: INTAKE & TRIAGE
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                               │
│  [1] ISSUE CREATED EVENT                                                    │
│         │                                                                     │
│         └─→ Auto-applies label: somas:{type}                                 │
│             • somas-project (for new projects)                              │
│             • somas:bug (for bug reports)                                    │
│             • somas:change (for changes)                                     │
│             • somas:enhance (for enhancements)                               │
│             • somas:question (for questions)                                 │
│                                                                               │
│  [2] TRIGGER: intake-triage.yml Workflow                                    │
│         │                                                                     │
│         └─→ GitHub Actions: SOMAS: Phase 1 (Intake)                         │
│             • Sets up Python 3.10 environment                               │
│             • Installs dependencies                                          │
│             • Invokes Triage Agent                                           │
│                                                                               │
│  [3] TRIAGE AGENT EXECUTION                                                 │
│         │                                                                     │
│         ├─→ Analyzes issue content                                           │
│         ├─→ Classifies issue type                                            │
│         ├─→ Calculates confidence score (0.0-1.0)                            │
│         ├─→ Routes to appropriate agent                                      │
│         ├─→ Estimates effort level                                           │
│         ├─→ Generates: triage_report.md                                      │
│         │                                                                     │
│         └─→ Output Format (YAML):                                            │
│             • issue_number                                                   │
│             • classification (change|enhancement|question|bug)              │
│             • confidence score                                               │
│             • routing (agent assignment)                                     │
│             • estimated_effort                                               │
│             • action (route|defer|reject|escalate)                          │
│             • next_steps                                                     │
│                                                                               │
│  [4] TRIAGE COMMENT POSTED                                                  │
│         │                                                                     │
│         └─→ Posts analysis to issue as comment:                             │
│             • Classification result                                          │
│             • Confidence score                                               │
│             • Routing decision                                               │
│             • Next steps                                                     │
│                                                                               │
│  [5] ADVISOR CONSULTATION (Conditional)                                     │
│         │                                                                     │
│         └─→ IF confidence < 0.8 OR high complexity:                         │
│             • Invokes Advisor Agent                                          │
│             • Posts strategic recommendations                               │
│             • Clarifies approach                                             │
│                                                                               │
│  [6] LABELS UPDATED                                                         │
│         │                                                                     │
│         ├─→ Adds: somas:triaged                                             │
│         ├─→ Adds: somas:dev (enables pipeline)                              │
│         └─→ Adds: somas-project (if applicable)                             │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘

              PHASE 2-11: 11-STAGE AETHER LIFECYCLE PIPELINE
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                               │
│  [TRIGGER] somas-orchestrator.yml                                           │
│  Invoked by: somas:dev label + copilot comments                             │
│                                                                               │
│  PROJECT INITIALIZATION:                                                    │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                         │ │
│  │  • Create: .somas/projects/project-{id}/                              │ │
│  │  • Initialize: state.json (project state)                             │ │
│  │  • Create: artifacts/ subdirectory                                     │ │
│  │  • Create: logs/ subdirectory                                          │ │
│  │  • Generate: metadata.json (project info)                             │ │
│  │                                                                         │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                               │
│  AETHER LIFECYCLE: 11 SEQUENTIAL STAGES                                     │
│                                                                               │
│  STAGE 1: INTAKE                    (somas:stage:intake)                    │
│  ├─ Agent: Triage (already done) + Advisor                                 │
│  ├─ Output: Triage report, Strategic guidance                              │
│  ├─ Next Label: somas:stage:specify                                        │
│  └─ Time: ~2 min                                                             │
│       │                                                                      │
│       ▼                                                                      │
│                                                                               │
│  STAGE 2: SPECIFY                   (somas:stage:specify)                   │
│  ├─ Agent: Specifier                                                         │
│  ├─ Output: SPEC.md (detailed specification)                               │
│  ├─ Artifacts: SPEC.md saved to artifacts/                                 │
│  ├─ Next Label: somas:stage:plan                                           │
│  └─ Time: ~5 min                                                             │
│       │                                                                      │
│       ▼                                                                      │
│                                                                               │
│  STAGE 3: PLAN                      (somas:stage:plan)                      │
│  ├─ Agents: Simulator, Architect, Planner                                  │
│  ├─ Outputs:                                                                 │
│  │  • Simulation results                                                     │
│  │  • Architecture design (architecture.md)                                 │
│  │  • Execution plan (execution_plan.yml)                                  │
│  ├─ Artifacts: architecture.md, execution_plan.yml                         │
│  ├─ Next Label: somas:stage:decompose                                      │
│  └─ Time: ~5 min                                                             │
│       │                                                                      │
│       ▼                                                                      │
│                                                                               │
│  STAGE 4: DECOMPOSE                 (somas:stage:decompose)                 │
│  ├─ Agent: Decomposer                                                        │
│  ├─ Output: Task decomposition (task list)                                 │
│  ├─ Artifacts: task_list.md, task_decomposition.yml                        │
│  ├─ Next Label: somas:stage:implement                                      │
│  └─ Time: ~2 min                                                             │
│       │                                                                      │
│       ▼                                                                      │
│                                                                               │
│  STAGE 5: IMPLEMENT                 (somas:stage:implement)                 │
│  ├─ Agents: Implementer, Copilot                                            │
│  ├─ Output: Generated source code                                           │
│  ├─ Artifacts: implementation.md, source code files                        │
│  ├─ Next Label: somas:stage:verify                                         │
│  └─ Time: ~15 min                                                            │
│       │                                                                      │
│       ▼                                                                      │
│                                                                               │
│  STAGE 6: VERIFY                    (somas:stage:verify)                    │
│  ├─ Agents: Validator, Tester, Debugger                                    │
│  ├─ Output: Test results, bug fixes                                        │
│  ├─ Artifacts: test_results.json, test coverage                            │
│  ├─ Quality Gate: Test coverage > 90%                                      │
│  ├─ Next Label: somas:stage:integrate                                      │
│  └─ Time: ~10 min                                                            │
│       │                                                                      │
│       ▼                                                                      │
│                                                                               │
│  STAGE 7: INTEGRATE                 (somas:stage:integrate)                 │
│  ├─ Agents: Merger, Validator                                               │
│  ├─ Output: Code merged, integration validated                             │
│  ├─ Quality Gate: All checks passing                                       │
│  ├─ Next Label: somas:stage:harden                                         │
│  └─ Time: ~5 min                                                             │
│       │                                                                      │
│       ▼                                                                      │
│                                                                               │
│  STAGE 8: HARDEN                    (somas:stage:harden)                    │
│  ├─ Agent: Security                                                          │
│  ├─ Output: Security report, vulnerability scan                            │
│  ├─ Artifacts: security_report.md                                          │
│  ├─ Quality Gate: No critical vulnerabilities                              │
│  ├─ Next Label: somas:stage:release                                        │
│  └─ Time: ~10 min                                                            │
│       │                                                                      │
│       ▼                                                                      │
│                                                                               │
│  STAGE 9: RELEASE                   (somas:stage:release)                   │
│  ├─ Agent: Deployer                                                          │
│  ├─ Output: Deployment artifacts, release notes                            │
│  ├─ Artifacts: deployment_guide.md                                         │
│  ├─ Next Label: somas:stage:operate                                        │
│  └─ Time: ~5 min                                                             │
│       │                                                                      │
│       ▼                                                                      │
│                                                                               │
│  STAGE 10: OPERATE                  (somas:stage:operate)                   │
│  ├─ Agent: Operator                                                          │
│  ├─ Output: SLO monitoring, operational guide                              │
│  ├─ Next Label: somas:stage:analyze                                        │
│  └─ Time: ~5 min                                                             │
│       │                                                                      │
│       ▼                                                                      │
│                                                                               │
│  STAGE 11: ANALYZE                  (somas:stage:analyze)                   │
│  ├─ Agents: Analyzer, Documenter                                            │
│  ├─ Output: Final report, complete documentation                           │
│  ├─ Artifacts: README.md, final_report.md                                  │
│  ├─ Next Label: state:complete                                             │
│  └─ Time: ~10 min                                                            │
│       │                                                                      │
│       ▼                                                                      │
│                                                                               │
│  ✓ PIPELINE COMPLETE                                                         │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘

                          PHASE 12: DELIVERY & INTEGRATION
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                               │
│  [1] PULL REQUEST CREATION                                                  │
│         │                                                                     │
│         ├─→ PR Title: "SOMAS: Project {ID} - {Description}"                 │
│         ├─→ PR Source: somas/project-{id}                                   │
│         ├─→ PR Target: dev                                                   │
│         ├─→ PR Body includes:                                                │
│         │   • Project summary                                                │
│         │   • Artifacts generated                                            │
│         │   • Test results                                                   │
│         │   • Quality metrics                                                │
│         │   • Links to issue & artifacts                                    │
│         │                                                                     │
│         └─→ PR Checks:                                                       │
│             • JSON validation ✓                                             │
│             • Code linting ✓                                                 │
│             • Type checking ✓                                                │
│             • Security scanning (CodeQL, Semgrep) ✓                         │
│             • All tests passing ✓                                            │
│                                                                               │
│  [2] AUTO-MERGE DECISION                                                    │
│         │                                                                     │
│         └─→ If all checks passing and no manual changes needed:             │
│             • Apply squash merge                                             │
│             • Auto-merge to dev branch                                       │
│             • Add labels: somas-generated, state:complete                  │
│             • Close issue                                                    │
│             • Post completion comment                                        │
│                                                                               │
│  [3] HUMAN REVIEW (if needed)                                               │
│         │                                                                     │
│         └─→ If escalation required:                                         │
│             • Add label: needs-human-review                                 │
│             • Block auto-merge                                               │
│             • Notify code owners                                             │
│             • Await manual approval                                          │
│                                                                               │
│  [4] COMPLETION NOTIFICATION                                                │
│         │                                                                     │
│         └─→ Post final comment to issue:                                    │
│             • Completion status ✓                                            │
│             • Link to PR                                                     │
│             • Link to artifacts                                              │
│             • Execution time & metrics                                      │
│             • Cost summary (if tracked)                                      │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘

                          SAFETY MECHANISMS
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                               │
│  CIRCUIT BREAKER                                                             │
│  ├─ Limit: Max 20 agent invocations per issue                              │
│  ├─ Trigger: At 20 invocations                                              │
│  ├─ Action: Add somas:circuit-breaker label + warning comment              │
│  ├─ Disable: Manual label removal by human                                  │
│  └─ Purpose: Prevent runaway automation                                     │
│                                                                               │
│  ERROR RECOVERY                                                              │
│  ├─ State Checkpoints: After each stage completion                          │
│  ├─ Atomic Writes: File locking prevents corruption                         │
│  ├─ Retry Logic: Up to 3 retries with exponential backoff                  │
│  ├─ Fallback: Escalate to human on repeated failures                       │
│  └─ Audit Trail: All transitions logged in transitions.jsonl               │
│                                                                               │
│  HUMAN ESCALATION                                                            │
│  ├─ Triggers:                                                                │
│  │  • Triage confidence < 0.8                                                │
│  │  • Agent returns requires_human_review                                    │
│  │  • Security scan finds vulnerabilities                                   │
│  │  • Test coverage < 90%                                                    │
│  │  • Circuit breaker activated                                              │
│  │  • Multiple retries exhausted                                             │
│  │                                                                             │
│  └─ Actions:                                                                 │
│     • Add: needs-human-review label                                         │
│     • Post: Escalation comment with details                                 │
│     • Block: Auto-merge                                                      │
│     • Notify: Code owners (if configured)                                    │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘

                          DATA PERSISTENCE
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                               │
│  PROJECT DIRECTORY STRUCTURE                                                │
│  .somas/projects/project-{id}/                                             │
│  ├── state.json                    # Current project state                  │
│  ├── metadata.json                 # Project metadata                       │
│  ├── transitions.jsonl             # State transition audit log             │
│  ├── artifacts/                    # Generated artifacts                     │
│  │   ├── SPEC.md                   # Specification document                 │
│  │   ├── architecture.md            # Architecture design                    │
│  │   ├── execution_plan.yml         # Execution plan                         │
│  │   ├── task_list.md               # Task decomposition                     │
│  │   ├── implementation.md          # Implementation notes                   │
│  │   ├── test_results.json          # Test results                          │
│  │   ├── security_report.md         # Security findings                     │
│  │   ├── deployment_guide.md        # Deployment instructions               │
│  │   └── source/                    # Generated source code                 │
│  │       └── [language-specific files]                                      │
│  │                                                                             │
│  └── logs/                         # Execution logs                          │
│      ├── intake.log                 # Phase 1 logs                           │
│      ├── specify.log                # Phase 2 logs                           │
│      ├── plan.log                   # Phase 3 logs                           │
│      └── ...                        # Logs for all 11 stages                 │
│                                                                               │
│  ATOMICITY & LOCKING                                                        │
│  ├─ Mechanism: File locking (filelock library)                              │
│  ├─ Usage: Temp file + rename pattern for atomic writes                    │
│  ├─ Purpose: Prevent data corruption on concurrent access                   │
│  └─ Verification: All writes follow lock-write-rename pattern              │
│                                                                               │
│  STATE SCHEMA                                                                │
│  {                                                                            │
│    "issue_number": 123,                                                      │
│    "project_id": "project-123",                                              │
│    "created_at": "2026-01-31T10:00:00Z",                                    │
│    "current_stage": "specify",                                               │
│    "stages_completed": ["intake"],                                           │
│    "agent_invocations": 3,                                                   │
│    "status": "in_progress",                                                  │
│    "artifacts": [...],                                                       │
│    "errors": [],                                                              │
│    "last_updated": "2026-01-31T10:15:30Z"                                   │
│  }                                                                            │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Workflow Trigger Matrix

```
┌─────────────────────────┬──────────────────────┬──────────────────────┐
│    ISSUE TEMPLATE       │   AUTO-APPLIED LABEL │   INITIAL WORKFLOW   │
├─────────────────────────┼──────────────────────┼──────────────────────┤
│ 🚀 SOMAS Project        │ somas-project        │ intake-triage.yml    │
│                         │ somas:dev            │ → somas-pipeline.yml │
├─────────────────────────┼──────────────────────┼──────────────────────┤
│ 🐛 Bug Report           │ somas:bug            │ intake-triage.yml    │
│                         │ somas:dev            │ (routed to bugfix)   │
├─────────────────────────┼──────────────────────┼──────────────────────┤
│ ✨ Enhancement          │ somas:enhance        │ intake-triage.yml    │
│                         │ somas:dev            │ (routed to backlog)  │
├─────────────────────────┼──────────────────────┼──────────────────────┤
│ 🔄 Change Request       │ somas:change         │ intake-triage.yml    │
│                         │ somas:dev            │ (injected at stage)  │
├─────────────────────────┼──────────────────────┼──────────────────────┤
│ ❓ Question             │ somas:question       │ intake-triage.yml    │
│                         │ (no somas:dev)       │ (advisor only)       │
└─────────────────────────┴──────────────────────┴──────────────────────┘
```

## Agent Invocation Sequence (Project Type)

> **Note**: This is a simplified linear view. Some stages may invoke multiple agents in parallel. See the [AETHER LIFECYCLE](#aether-lifecycle-11-sequential-stages) section above for complete stage-by-stage agent assignments.

```
┌────────────────────────────────────────────────────────────────┐
│                  AGENT EXECUTION PIPELINE                      │
└────────────────────────────────────────────────────────────────┘

   1. TRIAGE AGENT + ADVISOR AGENT
      ↓ routes to next agent based on classification

   2. SPECIFIER AGENT + REQUIREMENTS AGENT
      ↓ (if project type)

   3. SIMULATOR AGENT + ARCHITECT AGENT + PLANNER AGENT
      ↓ (planning phase)

   4. DECOMPOSER AGENT
      ↓ (task breakdown)

   5. IMPLEMENTER AGENT + COPILOT AGENT
      ↓ (code generation)

   6. VALIDATOR AGENT + TESTER AGENT + DEBUGGER AGENT
      ↓ (testing & debugging with self-healing)

   7. MERGER AGENT + VALIDATOR AGENT
      ↓ (integration)

   8. SECURITY AGENT
      ↓ (hardening)

   9. DEPLOYER AGENT
      ↓ (release preparation)

   10. OPERATOR AGENT
       ↓ (operational readiness)

   11. ANALYZER AGENT + DOCUMENTER AGENT
       ↓ (final analysis)

   ✓ PIPELINE COMPLETE
       ↓
   Create PR → Auto-merge (or escalate for review)
```

## Label Lifecycle

```
ISSUE CREATED
    ↓
[AUTO-APPLIED] somas:{type} label
    ↓
INTAKE/TRIAGE WORKFLOW TRIGGERS
    ↓
[ADDED] somas:triaged
[ADDED] somas:dev (enables pipeline)
[ADDED] somas-project (if applicable)
    ↓
STAGE PROGRESSION
    ├─→ somas:stage:intake
    ├─→ somas:stage:specify (and removes :intake)
    ├─→ somas:stage:plan (and removes :specify)
    ├─→ somas:stage:decompose
    ├─→ somas:stage:implement
    ├─→ somas:stage:verify
    ├─→ somas:stage:integrate
    ├─→ somas:stage:harden
    ├─→ somas:stage:release
    ├─→ somas:stage:operate
    └─→ somas:stage:analyze
    ↓
COMPLETION
    ├─→ [REMOVED] somas:stage:analyze
    ├─→ [ADDED] state:complete
    ├─→ [ADDED] somas-generated
    └─→ ISSUE CLOSED
```

---

**Total Pipeline Execution Time:**
- Simple Project: 30-45 minutes
- Complex Project: 1-2 hours

**Success Criteria:**
- ✓ All 11 stages complete
- ✓ All tests passing (coverage > 90%)
- ✓ Security scan passing
- ✓ No circuit breaker triggered
- ✓ PR created and merged
