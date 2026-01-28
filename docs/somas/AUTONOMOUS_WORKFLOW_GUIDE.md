# SOMAS Autonomous Workflow Guide

## Overview

The SOMAS Autonomous Pipeline is designed to execute a complete software development lifecycle—from ideation to staging—without human intervention in the development environment. This guide details the workflow architecture, trigger mechanisms, and execution flow.

## Workflow Diagram

```mermaid
graph TD
    Start[User Creates Issue] -->|Label 'somas:dev'| Trigger[Trigger somas-dev-autonomous.yml]

    subgraph "GitHub Actions (Autonomous Mode)"
        Trigger --> Init[Initialize Pipeline]
        Init -->|Create Branch| Branch[somas/project-{id}]

        subgraph "Sequential Execution (somas/core/runner.py)"
            Planner[Stage 1: Planner] -->|Plan| Specifier[Stage 2: Specifier]
            Specifier -->|Spec| Simulator[Stage 3: Simulator]
            Simulator -->|Optimization| Architect[Stage 4: Architect]
            Architect -->|Design| Implementer[Stage 5: Implementer]
            Implementer -->|Code| Validator[Stage 6: Validator]
        end

        Validator -->|Success| Staging[Stage 7: Staging]
        Validator -->|Failure| Retry{Retry < 3?}
        Retry -->|Yes| Debugger[Debugger Agent]
        Debugger --> Validator
        Retry -->|No| Fail[Notify Human]
    end

    Staging -->|Create PR| PR[Pull Request]
    PR -->|Auto-Merge| DevBranch[Dev Branch]
    DevBranch -->|Request Approval| ProdGate[Production Gate]
    ProdGate -->|Human Approve| Main[Main Branch]
```

## Step-by-Step Instructions

### 1. Prerequisites

Before triggering the pipeline, ensure the **Personal Access Token (PAT)** is configured.

* **Why?** The default `GITHUB_TOKEN` cannot trigger cascading workflows or create PRs with your identity.
* **How?** See PAT Setup Guide.
* **Verify:** Ensure the secret `SOMAS_PAT` exists in Repository Settings > Secrets and variables > Actions.

### 2. Triggering the Pipeline

The pipeline is event-driven, triggered by specific labels on GitHub Issues.

1. **Create a New Issue**:
    * Use the **SOMAS Project Request** template.
    * Fill out the Title, Project Idea, Type, and Constraints.
    * *Tip: Be specific in the "Project Idea" section for better results.*

2. **Apply the Label**:
    * Add the label `somas:dev` to the issue.
    * *Note: The `somas-project` label is for the standard pipeline; `somas:dev` specifically targets the autonomous dev workflow.*

### 3. Autonomous Execution (What happens next)

Once labeled, the `SOMAS Autonomous Dev Pipeline` workflow starts:

1. **Initialization**:
    * The workflow checks out the repository using `SOMAS_PAT`.
    * It initializes a project structure in `.somas/projects/project-{id}/`.
    * A dedicated feature branch `somas/project-{id}` is created.

2. **Stage Execution**:
    * The `somas/core/runner.py` script executes stages sequentially.
    * **Planner**: Generates `initial_plan.md`.
    * **Specifier**: Creates `SPEC.md` (Requirements).
    * **Simulator**: Runs Monte Carlo simulations to optimize the execution plan.
    * **Architect**: Generates `ARCHITECTURE.md` and API specs.
    * **Implementer**: Generates code and tests in the `implementation/` directory.
    * **Validator**: Runs tests and security scans.

3. **Self-Healing**:
    * If validation fails, the **Debugger** agent is invoked automatically.
    * It attempts to fix the code and re-runs validation (up to 3 retries).

### 4. Completion & Review

Upon successful completion of Stage 6 (Validation):

1. **Pull Request**:
    * A Pull Request (PR) is automatically created from `somas/project-{id}` to the default branch.
    * The PR description contains a summary of all stages and artifacts.

2. **Dev Auto-Merge**:
    * In the `dev` environment, if all checks pass, the PR is set to auto-merge.

3. **Production Promotion**:
    * To promote to production, a human must review the merged code and approve the deployment to the `main` branch (if separate).

## Troubleshooting

### Workflow Doesn't Start

* **Check Labels**: Ensure `somas:dev` is spelled correctly.
* **Check Permissions**: Ensure the user adding the label has write access.

### Workflow Fails at "Checkout"

* **Check PAT**: The `SOMAS_PAT` might be expired or missing permissions. It requires `Contents: Read and write`.

### Pipeline Stalls

* **Check Logs**: Go to the **Actions** tab in GitHub and click on the running workflow.
* **Timeout**: The default timeout is 300 minutes (5 hours). If a project is too complex, it may time out.

### "Resource not accessible by integration"

* **Cause**: The workflow is trying to perform an action (like creating a PR) using `GITHUB_TOKEN` instead of `SOMAS_PAT`, or the PAT lacks permissions.
* **Fix**: Review the PAT Setup Guide.

## Reference Files

* **Workflow Definition**: `.github/workflows/somas-dev-autonomous.yml`
* **Pipeline Logic**: `somas/core/runner.py`
* **Agent Configs**: `.somas/agents/*.yml`
