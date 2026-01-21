# Comment-Driven Orchestration - Implementation Guide

## Overview

This document describes the comment-driven orchestration system that enables fully autonomous SOMAS pipeline execution through GitHub Copilot agents.

## Architecture

### Workflow: `.github/workflows/somas-orchestrator.yml`

The orchestrator workflow implements a two-job pattern:

1. **Initialize Job** - Triggered when issue is labeled with `somas:dev`
2. **Orchestrate Job** - Triggered by issue comments containing `@copilot somas-`

### Agent Files: `.github/agents/somas-*.md`

Each agent has a markdown file that:
- Describes the agent's role and responsibilities
- Links to the corresponding `.somas/agents/*.yml` configuration
- Specifies required output format (YAML or Markdown)
- Provides examples and quality checklists

## Execution Flow

### 1. Initialization (Job: `initialize`)

**Trigger:** Issue opened/labeled with `somas:dev`

**Actions:**
```yaml
1. Checkout repository
2. Create project directory structure:
   projects/{project_id}/
   ├── artifacts/
   ├── logs/
   └── checkpoints/
3. Initialize metadata.json
4. Create feature branch (somas/project-{issue})
5. Commit initial structure
6. Post comment invoking @copilot somas-planner
```

**Output:** GitHub issue comment that looks like:
```markdown
🚀 **SOMAS Autonomous Pipeline Initiated**

**Project ID:** `project-123`
**Branch:** `somas/project-123`

---

@copilot somas-planner

Create initial plan for this project based on the issue description above.

**Required Output Format:**
```yaml
# initial_plan.yml
project:
  title: "..."
...
```

**Project Context:**
{issue body}
```

### 2. Orchestration (Job: `orchestrate`)

**Trigger:** Issue comment created by `copilot[bot]`

**Actions:**
```yaml
1. Checkout repository
2. Parse agent response:
   a. Extract YAML/Markdown code blocks
   b. Determine which agent responded
   c. Map agent to artifact type
   d. Determine next agent in sequence
3. Save artifacts:
   a. Switch to project branch
   b. Write artifacts to projects/{id}/artifacts/
   c. Update metadata.json
   d. Write log entry
4. Commit artifacts:
   a. git add projects/{id}/
   b. git commit -m "[{id}] {agent} stage complete"
   c. git push
5. Invoke next agent:
   a. Post comment with @copilot somas-{next}
   b. Include context and required output format
   OR
6. Complete pipeline:
   a. Create PR
   b. Enable auto-merge
   c. Post completion comment
```

### Agent Sequence

```
planner → specifier → simulator → architect → implementer → tester → reviewer → COMPLETE
```

Each transition includes:
- Artifact extraction from previous agent
- Commit to feature branch
- Comment invoking next agent with context

## Artifact Extraction

### YAML Blocks

**Pattern:** ````yaml\n([\s\S]*?)\n````

**Example Response:**
```markdown
Here's the initial plan:

```yaml
project:
  title: "Chat Application"
  description: "Real-time messaging"
```
```

**Extraction Result:**
- File: `projects/project-123/artifacts/initial_plan.yml`
- Content: The YAML block content

### Markdown Blocks

**Pattern:** ````markdown\n([\s\S]*?)\n````

**Example Response:**
```markdown
Here's the specification:

```markdown
# Project Specification

## Executive Summary
...
```
```

**Extraction Result:**
- File: `projects/project-123/artifacts/SPEC.md`
- Content: The Markdown block content

## Agent Response Detection

### Method 1: Comment Author Check
```javascript
if (commentAuthor !== 'copilot[bot]') {
  // Not an agent response, skip
  return;
}
```

### Method 2: Parent Comment Analysis
```javascript
// Find last human comment before this bot response
const humanComments = allComments.filter(c => 
  c.user.login !== 'copilot[bot]' &&
  c.id < currentComment.id
);

const lastHuman = humanComments[humanComments.length - 1];

// Check which agent was invoked
if (lastHuman.body.includes('@copilot somas-planner')) {
  agentName = 'planner';
  artifactName = 'initial_plan.yml';
  nextAgent = 'specifier';
}
```

## Agent Mapping

| Agent | Artifact | Next Agent | Format |
|-------|----------|------------|--------|
| planner | initial_plan.yml | specifier | YAML |
| specifier | SPEC.md | simulator | Markdown |
| simulator | execution_plan.yml | architect | YAML |
| architect | ARCHITECTURE.md | implementer | Markdown |
| implementer | source_code/ | tester | Markdown (code blocks) |
| tester | test_results.json | reviewer | JSON/Markdown |
| reviewer | review_report.md | COMPLETE | Markdown |

## Git Operations

All git operations use direct commands (not GitHub API for file content):

### Branch Creation
```bash
git config user.name "SOMAS Bot"
git config user.email "somas-bot@users.noreply.github.com"
git checkout -b "somas/project-${PROJECT_ID}"
git push -u origin "somas/project-${PROJECT_ID}"
```

### File Commits
```bash
git add "projects/${PROJECT_ID}/"
git commit -m "[${PROJECT_ID}] ${AGENT_NAME} stage complete"
git push origin "somas/project-${PROJECT_ID}"
```

### PR Creation (GitHub API)
```javascript
const pr = await github.rest.pulls.create({
  owner: context.repo.owner,
  repo: context.repo.repo,
  title: `[${projectId}] Autonomous Implementation`,
  body: '...',
  head: branchName,
  base: 'main'
});
```

### Auto-Merge (GitHub API)
```javascript
await github.rest.pulls.merge({
  owner: context.repo.owner,
  repo: context.repo.repo,
  pull_number: pr.data.number,
  merge_method: 'squash'
});
```

## Error Handling

### Agent Response Issues
- **No code blocks found**: Skip orchestration, wait for human intervention
- **Wrong format**: Log warning, save what's available
- **Multiple code blocks**: Use first block of expected type

### Git Operation Failures
- **Branch exists**: Checkout existing branch
- **No changes to commit**: Continue (echo "No changes")
- **Push fails**: Retry with exponential backoff (todo: implement)

### PR Creation Failures
- **PR already exists**: Skip creation, find existing PR
- **Merge conflicts**: Escalate to human via comment

## Testing Strategy

### Unit Testing (Manual Simulation)

1. **Create test issue:**
```markdown
Title: Test SOMAS Pipeline
Labels: somas:dev

Body: Create a simple CLI tool to validate JSON files
```

2. **Verify initialization:**
- Workflow creates branch
- Workflow posts planner invocation comment

3. **Simulate planner response:**
Post comment as if from copilot[bot] with:
```yaml
```yaml
project:
  title: "JSON Validator CLI"
...
```
```

4. **Verify orchestration:**
- Workflow extracts YAML
- Workflow commits to branch
- Workflow posts specifier invocation

5. **Repeat** for each stage

### Integration Testing (Real Copilot)

1. Create issue with `somas:dev` label
2. Wait for @copilot to respond
3. Monitor workflow execution
4. Verify artifacts are committed
5. Verify PR is created and auto-merged

## Monitoring & Debugging

### Workflow Logs
- Check Actions tab for workflow runs
- Look for "Parse Agent Response" step
- Check outputs: `agent_name`, `artifact_name`, `next_agent`

### Artifact Verification
```bash
git checkout somas/project-123
ls projects/project-123/artifacts/
cat projects/project-123/artifacts/initial_plan.yml
```

### Comment History
- Review issue comments for agent invocations
- Verify copilot[bot] responses
- Check for error messages in comments

## Configuration

### Agent Configs
Each agent's behavior defined in `.somas/agents/{agent}.yml`:
- Provider (model to use)
- Fallback model
- Prompt instructions
- Quality checks

### Workflow Timeouts
- Initialize job: No timeout (fast, <1 min)
- Orchestrate job: No timeout (depends on agent response time)
- Overall: 5 hours max per issue

### Retry Logic
- Agent invocations: No automatic retry (wait for human)
- Git operations: No retry yet (todo: implement)
- PR operations: No retry (fail fast, notify)

## Limitations & Future Work

### Current Limitations
1. **No validation** of extracted artifacts (assumes valid YAML/Markdown)
2. **No retry logic** for failed operations
3. **No parallel execution** (sequential only)
4. **No checkpoint resume** (starts from scratch)

### Planned Improvements
1. **Artifact validation** before commit
2. **Exponential backoff** for git operations
3. **Parallel agent execution** where possible
4. **State persistence** for pipeline resume
5. **Real-time progress** dashboard
6. **Cost tracking** per agent invocation

## Security Considerations

### Secrets Management
- GitHub token: Provided by Actions (`GITHUB_TOKEN`)
- No additional secrets required

### Permission Model
- Workflow has `contents: write` for commits
- Workflow has `issues: write` for comments
- Workflow has `pull-requests: write` for PRs

### Input Validation
- Project IDs validated (no path traversal)
- Branch names sanitized
- Comment bodies not executed (only parsed)

## Troubleshooting

### Issue: Workflow doesn't trigger
- **Check:** Issue has `somas:dev` label
- **Check:** Workflow file syntax is valid
- **Fix:** Re-label issue or check Actions tab for errors

### Issue: Agent doesn't respond
- **Check:** Comment includes correct @copilot mention
- **Check:** Output format is clearly specified
- **Fix:** Manually invoke with clearer prompt

### Issue: Artifacts not extracted
- **Check:** Code blocks use ````yaml` or ````markdown`
- **Check:** Code blocks are properly closed
- **Fix:** Adjust regex pattern or ask agent to retry

### Issue: PR not created
- **Check:** All stages completed
- **Check:** Branch exists and has commits
- **Fix:** Manually create PR from branch

## Example Complete Execution

See `EXAMPLE_EXECUTION.md` for a step-by-step walkthrough of a complete pipeline run from issue creation to merged PR.

---

**Last Updated:** 2026-01-21
**Version:** 1.0.0
**Status:** Production Ready
