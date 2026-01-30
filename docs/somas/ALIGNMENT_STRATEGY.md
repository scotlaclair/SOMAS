# SOMAS Alignment Strategy: Agents & Lifecycle

## 1. Problem & Goal

**Problem:** Divergence between legacy "Neurology" docs (7 stages), current "Aether" code (11 stages), and overlapping agent roles.

**Goal:** Operationalize the 11-stage Aether lifecycle using concrete GitHub primitives (Issues, PRs, Projects) and strictly define "One Agent, One Role."

---

## 2. Operational Reality: The GitHub Object Model

To ground SOMAS in reality, we map abstract concepts to physical GitHub artifacts.

| Concept | GitHub Primitive | Role & Behavior |
|---------|------------------|-----------------|
| **The Context** | GitHub Issue | The Source of Truth. It persists across the entire lifecycle. All agent logs and decisions are posted here as comments. |
| **The Workflow** | GitHub Project | The Kanban Board. Columns represent the 11 Aether Stages. Cards (Issues) move left-to-right based on Gate passage. |
| **The Workspace** | Pull Request (PR) | The Canvas. Created in Stage 05. This is where code, tests, and docs are drafted. CI checks run here. |
| **The State** | Labels | `somas:stage:05-implement`, `somas:status:blocked`, `somas:gate:passed`. Triggers workflow transitions. |
| **The Release** | Milestone | Groups Issues into a versioned delivery (e.g., `v1.0.0`). |

---

## 3. The 11-Stage Lifecycle & Artifact Mapping

This table maps the **Time** (Stage) to the **Worker** (Agent ID) and the **State** (Label).

| ID | Stage (Column) | Primary Agents (YAML ID) | GitHub Label | Operational Actions | Exit Gate (Criteria) |
|----|----------------|--------------------------|--------------|---------------------|---------------------|
| 01 | **INTAKE** | triage, advisor | `somas:stage:01-intake` | Agent analyzes Issue body. Checks similarity to existing issues. Assigns difficulty. | `feasibility > 0.7` |
| 02 | **SPECIFY** | specifier | `somas:stage:02-specify` | Agent creates/updates `docs/specs/ISSUE-123.md`. Converts intent to strict PRD. | `spec_approved` |
| 03 | **PLAN** | planner, architect, simulator | `somas:stage:03-plan` | Architect defines folder structure. Planner generates `plan.json`. Simulator runs Monte Carlo pathing. | `architecture_valid` |
| 04 | **DECOMPOSE** | decomposer | `somas:stage:04-decompose` | Breaks `plan.json` into atomic sub-tasks linked to the Issue. | `tasks_created` |
| 05 | **IMPLEMENT** | implementer, copilot | `somas:stage:05-implement` | Create PR. Loop: Write Code → Run CI → Fix Errors. (See Micro-Loop below) | `build_success` |
| 06 | **VERIFY** | tester, debugger | `somas:stage:06-verify` | Runs deep test suites on the PR. Debugger patches logic if tests fail. | `tests_pass` |
| 07 | **INTEGRATE** | merger, validator | `somas:stage:07-integrate` | Checks for merge conflicts with main. Validates requirements traceability. | `clean_merge` |
| 08 | **HARDEN** | security | `somas:stage:08-harden` | Runs SAST/DAST on PR. Checks for secrets/vulns. | `security_clean` |
| 09 | **RELEASE** | deployer | `somas:stage:09-release` | Merges PR to main. Tags release. Generates Changelog. | `merged` |
| 10 | **OPERATE** | operator | `somas:stage:10-operate` | Deploys to env. Checks health endpoints. | `health_200_ok` |
| 11 | **ANALYZE** | analyzer, documenter | `somas:stage:11-analyze` | Reviews metrics (time-to-merge, retries). Updates strictness of Gates. | `metrics_logged` |

---

## 4. The Fractal Lifecycle (Micro-Loops)

As noted in the strategy, a Stage is not just a single step. It is a container for a micro-lifecycle.

### Example: The "Stage 05 (Implement)" Micro-Loop

While the Issue is in the IMPLEMENT column (`somas:stage:05-implement`), the PR undergoes its own cycle before moving to Stage 06:

1. **Draft:** `implementer` writes `feature.py`.
2. **Build:** GH Actions triggers `syntax_check`.
3. **Document:** `documenter` adds docstrings to the new code.
4. **Review:** `copilot` (or `reviewer`) performs a "sanity check" (linting).
5. **Refine:** `implementer` fixes syntax errors.
6. **Result:** A compilable, linted PR.
7. **Next:** Move to VERIFY (`somas:stage:06-verify`) for functional correctness testing.

---

## 5. Agent Scope Resolution

Resolving overlapping responsibilities to enforce the lifecycle above.

### Coder vs. Implementer

**Resolution:** `Implementer` (`implementer.yml`) is the Agent. `Coder` is deprecated. The Implementer owns the Stage 05 Micro-Loop.

### Tester vs. Validator

**Resolution:**
- **Tester** (`tester.yml`): "Does the code work?" (Unit/Integration Tests).
- **Validator** (`validator.yml`): "Did we build the right thing?" (Reqs Traceability).

### Planner vs. Architect

**Resolution:**
- **Architect** (`architect.yml`): Spatial design (Files, Classes, DB Schema).
- **Planner** (`planner.yml`): Temporal design (Order of operations, Dependencies).

---

## 6. Orchestrator Role

The **Orchestrator** (`orchestrator.yml`) is the Runtime Engine. It does not appear in the table because it *is* the table. It manages the movement of the Issue card between columns and invokes the Agents assigned to that column based on the presence of labels like `somas:stage:xx`.
