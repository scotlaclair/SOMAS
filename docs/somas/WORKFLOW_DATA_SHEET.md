# SOMAS Workflow Data Sheet

**Status:** Audited (Mapped to Repo Files)

**Goal:** Map every data point required to script the lifecycle from start to finish.

---

## Phase 1: Initiation & Planning (Stages 01-04)

This phase operates entirely within the GitHub Issue context.

| Step | Stage ID | Phase Name | GitHub Context | Workflow File | Job ID | Trigger Event | Primary Agent | Agent Operation | Model ID | Prompt Template | Exit Gate | Next State Label |
|------|----------|------------|----------------|---------------|--------|---------------|---------------|-----------------|----------|-----------------|-----------|------------------|
| 1 | 01 | INTAKE | Issue | somas-pipeline.yml | triage | Label: somas:change | triage | analyze_request_type | gpt-4o-mini | prompts/triage/classify.md | feasibility > 0.7 | somas:stage:specify |
| 2 | 01 | INTAKE | Issue | somas-pipeline.yml | strategy | (Chained) | advisor | check_alignment | gpt-4o | prompts/advisor/alignment.md | score > 0.5 | somas:stage:specify |
| 3 | 02 | SPECIFY | Issue | somas-orchestrator.yml | specifier | Label: somas:stage:specify | specifier | generate_prd | gpt-4o | prompts/specifier/generate_prd.md | file_exists | somas:gate:spec-review |
| 4 | 02 | SPECIFY | Issue | somas-orchestrator.yml | verify | Label: gate:review | requirements | validate_spec | gpt-4o | prompts/requirements/verify.md | reqs_clear | somas:stage:plan |
| 5 | 03 | PLAN | Issue | somas-orchestrator.yml | architect | Label: somas:stage:plan | architect | design_system | o1-preview | prompts/architect/system_design.md | design_valid | (Handover) |
| 6 | 03 | PLAN | Issue | somas-orchestrator.yml | simulator | (Chained) | simulator | run_monte_carlo | gpt-4o-mini | prompts/simulator/monte_carlo.md | prob > 80% | (Handover) |
| 7 | 03 | PLAN | Issue | somas-orchestrator.yml | planner | (Chained) | planner | create_dag | gpt-4o | prompts/planner/create_dag.md | dag_acyclic | somas:stage:decompose |
| 8 | 04 | DECOMPOSE | Issue | somas-orchestrator.yml | decomposer | Label: somas:stage:decompose | decomposer | gen_tasks | gpt-4o | prompts/decomposer/breakdown.md | tasks > 0 | somas:stage:implement |

---

## Phase 2: Implementation & Verification (Stages 05-08)

This phase bridges the Issue (Requirements) and the Pull Request (Code).

| Step | Stage ID | Phase Name | GitHub Context | Workflow File | Job ID | Trigger Event | Primary Agent | Agent Operation | Model ID | Prompt Template | Exit Gate | Next State Label |
|------|----------|------------|----------------|---------------|--------|---------------|---------------|-----------------|----------|-----------------|-----------|------------------|
| 9 | 05 | IMPLEMENT | Issue | somas-pipeline-runner.yml | pr-create | Label: somas:stage:implement | implementer | create_pr | gpt-3.5-turbo | prompts/implementer/create_pr.md | pr_created | (PR Context) |
| 10 | 05 | IMPLEMENT | PR | somas-pipeline-runner.yml | autonomous-dev | Label: somas:stage:implement | implementer | write_code | claude-3-5-sonnet | prompts/templates/single_shot_implementer.md | compile_ok | (Wait) |
| 11 | 05 | IMPLEMENT | PR | somas-pr-continue.yml | review | synchronize | copilot | review_diff | gpt-4o | prompts/copilot/review.md | syntax_ok | somas:stage:verify |
| 12 | 06 | VERIFY | PR | somas-pipeline-runner.yml | test | Label: somas:stage:verify | tester | run_tests | gpt-4o-mini | prompts/tester/generate_tests.md | pass == 100% | somas:stage:integrate |
| 13 | 06 | VERIFY | PR | somas-pipeline-runner.yml | heal | test_fail | debugger | self_heal | gpt-4o | prompts/debugger/analyze_traceback.md | retry <= 3 | (Loop) |
| 14 | 07 | INTEGRATE | PR | pr-checklist-detector.yml | merge-check | Label: somas:stage:integrate | merger | check_conflict | git-native | N/A | conflicts == 0 | (Handover) |
| 15 | 07 | INTEGRATE | PR | somas-orchestrator.yml | trace | (Chained) | validator | trace_reqs | gpt-4o | prompts/validator/traceability.md | met == 100% | somas:stage:harden |
| 16 | 08 | HARDEN | PR | pr-security.yml | security | Label: somas:stage:harden | security | run_scans | codeql | N/A | vuln == 0 | somas:stage:release |

---

## Phase 3: Release & Operations (Stages 09-11)

Finalization and closure loops.

| Step | Stage ID | Phase Name | GitHub Context | Workflow File | Job ID | Trigger Event | Primary Agent | Agent Operation | Model ID | Prompt Template | Exit Gate | Next State Label |
|------|----------|------------|----------------|---------------|--------|---------------|---------------|-----------------|----------|-----------------|-----------|------------------|
| 17 | 09 | RELEASE | PR | somas-project-sync.yml | merge | Label: somas:stage:release | deployer | merge_pr | git-native | N/A | merged | (Release) |
| 18 | 09 | RELEASE | Release | somas-project-sync.yml | release | push:main | deployer | pub_release | git-native | N/A | published | somas:stage:operate |
| 19 | 10 | OPERATE | Deploy | somas-orchestrator.yml | monitor | Label: somas:stage:operate | operator | chk_health | curl/python | N/A | 200 OK | somas:stage:analyze |
| 20 | 11 | ANALYZE | Issue | somas-meta-capture.yml | metrics | Label: somas:stage:analyze | analyzer | gen_metrics | gpt-4o-mini | prompts/analyzer/post_mortem.md | logged | (Handover) |
| 21 | 11 | ANALYZE | Issue | somas-meta-capture.yml | close | (Chained) | documenter | update_kb | gpt-4o | prompts/documenter/changelog.md | closed | somas:status:completed |

---

## Extended Data Points

Each step in the workflow also tracks:

| Data Point | Description |
|------------|-------------|
| **Task Category** | Analysis, Generation, Verification, Ops, etc. |
| **Optimization Metric** | Accuracy, Completeness, Coverage, Speed, etc. |
| **Input Data** | What the agent receives (issue.body, SPEC.md, etc.) |
| **Output Data** | What the agent produces (Report, Code, Labels, etc.) |
| **Storage Location** | Where output is stored (Issue Comment, Git Repo, etc.) |
| **Data Format** | Markdown, JSON, Source Code, etc. |
| **Failure Label** | Label applied on failure (somas:status:rejected, etc.) |
| **Retry Policy** | None, 1x, 3x, 5x |
| **Timeout** | Maximum time allowed for step |
| **SLA (Target)** | Target completion time |
| **Cost Limit ($)** | Maximum cost per step |
| **Token Budget** | Maximum tokens per step |
| **HITL** | Human-in-the-loop required (Yes/No) |
| **Permissions** | Required GitHub permissions |
