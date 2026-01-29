# Stage 1: The Gatekeeper - Verification Checklist

**Goal:** Ensure SOMAS autonomously triages, classifies, and routes new issues.

---

## 1. File Existence Check

Ensure the following files exist in your repository with the correct content.

### Logic (The Brain)

- [ ] `.somas/prompts/triage/classify.md`
- [ ] `.somas/prompts/advisor/alignment.md`

### Configuration (The Body)

- [ ] `.somas/agents/triage.yml`
- [ ] `.somas/agents/advisor.yml`

### Infrastructure (The Nervous System)

- [ ] `.github/workflows/somas-pipeline.yml`

---

## 2. Functional Testing Script

### Test A: The "Happy Path" (Feature Request)

**Action:** Create a new Issue.

- **Title:** "Add Dark Mode to Dashboard"
- **Body:** "As a user, I want to toggle dark mode so I can work at night."
- **Label:** `somas:change`

**Expected Behavior:**

1. Workflow `SOMAS: Phase 1 (Intake)` starts.
2. Triage Agent comments on the issue.
3. Advisor Agent comments on the issue.
4. Label `somas:change` is removed.
5. Label `somas:stage:02-specify` is added.
