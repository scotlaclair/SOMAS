# SOMAS Iterative Implementation Plan

**Strategy:** Vertical Slices.

**Rule:** Do not move to the next Sprint until the current Sprint's "Exit Gate" is passing in the live repo.

---

## Sprint 1: The Gatekeeper (Stage 01 - INTAKE)

**Goal:** A user creates an Issue, and SOMAS autonomously triages and explicitly accepts or rejects it.

### 1. Prerequisite Check (The Input)

- [x] **Issue Template:** `.github/ISSUE_TEMPLATE/somas-change.yml`
  - **Action:** Ensure it applies the label `somas:change` automatically.

### 2. The Logic (The Missing Piece)

- [ ] **Create Prompt:** `prompts/triage/classify.md`
  - **Role:** Product Manager.
  - **Task:** Read Issue Body -> Output JSON classification.

- [ ] **Create Prompt:** `prompts/advisor/alignment.md`
  - **Role:** CTO.
  - **Task:** Read Issue vs. project.goals -> Output alignment score.

### 3. The Infrastructure (The Wiring)

- [ ] **Update Workflow:** `.github/workflows/somas-pipeline.yml`
  - **Task:** Update the steps to load the specific prompts created above.
  - **Task:** Ensure it writes the Agent's output as a GitHub Comment.

### 4. Verification (The Test)

- **Manual Trigger:** Open a new Issue with the `somas:change` label.
- **Success:** You see a comment from `github-actions` within 30 seconds: "Feasibility Analysis: 85%. Proceeding to Specification."

---

## Sprint 2: The Architect (Stages 02-03 - SPEC & PLAN)

**Goal:** Convert the accepted Issue into a set of strict Markdown documents (SPEC and ARCH).

### 1. The Logic

- [ ] **Create Prompt:** `prompts/specifier/generate_prd.md`
- [ ] **Create Prompt:** `prompts/architect/system_design.md`

### 2. The Infrastructure

- [ ] **Update Agent Configs:** Ensure `.somas/agents/specifier.yml` points to the new prompt.
- [ ] **Git Ops:** Enable the runner to Commit the new files (`docs/specs/*.md`) back to the repo.

### 3. Verification

- **Manual Trigger:** Add label `somas:stage:02-specify` to the Issue from Sprint 1.
- **Success:** A new file `docs/specs/ISSUE-1.md` appears in the file tree.

---

## Sprint 3: The Planner (Stage 04 - DECOMPOSE)

**Goal:** Transform the static Architecture document into actionable GitHub Checkboxes.

### 1. The Logic

- [ ] **Create Prompt:** `prompts/decomposer/breakdown.md`

### 2. The Infrastructure

- [ ] **Update Workflow:** Ensure it can parse the DAG JSON and call the GitHub API to update the Issue Body.

### 3. Verification

- **Manual Trigger:** Add label `somas:stage:04-decompose`.
- **Success:** The Issue body is updated with a Task List:
  - [ ] Create `/somas/core/new_feature.py`
  - [ ] Update `config.yml`

---

## Sprint 4: The Builder (Stage 05 - IMPLEMENT)

**Goal:** The "Magic Trick". Agents writing code.

### 1. The Logic

- [ ] **Review Prompt:** `prompts/templates/single_shot_implementer.md` (Already exists, refine it).

### 2. The Infrastructure

- [ ] **Workflow Update:** `somas-dev-autonomous.yml`.
  - **Task:** Ensure it creates a New Branch (`feature/issue-1`).
  - **Task:** Ensure it opens a Pull Request.

### 3. Verification

- **Manual Trigger:** Click the checkbox on the Task List.
- **Success:** A new PR is opened containing valid Python code.

---

## Sprint 5: The Verifier (Stages 06-11)

**Goal:** Safety, Testing, and Merging.

- [ ] **Create Prompts:** tester, debugger, security.
- [ ] **Configure Gates:** Set strict "Stop" signals in CI if tests fail.

---

## Recommendation for NOW

**Focus ONLY on Sprint 1.**

Ignore the code generation. Ignore the testing.

Let's just get the bot to **Read an Issue** and **Reply intelligently**.

> Shall I generate the two missing prompts for Sprint 1 (`classify.md` and `alignment.md`) so you can run the first test?
