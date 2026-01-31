# Setting Up Autonomous Workflow Execution

This guide explains how to enable fully autonomous execution of SOMAS workflows using direct LLM API integration.

## Overview

SOMAS can operate in two modes:

1. **Comment-Driven Mode** (Default): Relies on GitHub Copilot responding to `@copilot somas-*` mentions in issue comments
2. **Autonomous Mode** (Enhanced): Uses direct LLM API calls to execute the entire pipeline without GitHub Copilot dependency

## Prerequisites

### Required

- GitHub repository with SOMAS installed
- Python 3.11+
- API key from at least one LLM provider:
  - **OpenAI API Key** (for GPT-4o) - Recommended
  - **Anthropic API Key** (for Claude models) - Alternative

### Optional

- GitHub Actions runner with sufficient resources (2GB+ RAM recommended for full pipeline)

## Setup Instructions

### Step 1: Obtain LLM API Keys

#### Option A: OpenAI (Recommended)

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key (starts with `sk-...`)
4. Estimated cost: $0.50-$2.00 per project execution (GPT-4o pricing)

#### Option B: Anthropic

1. Go to [Anthropic Console](https://console.anthropic.com/settings/keys)
2. Create a new API key
3. Copy the key (starts with `sk-ant-...`)
4. Estimated cost: $1.00-$3.00 per project execution (Claude pricing)

#### Option C: Both (Best)

Using both providers gives the system flexibility to use the best model for each agent.

### Step 2: Add API Keys to GitHub Secrets

1. Navigate to your repository on GitHub
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secrets:

   **For OpenAI:**
   - Name: `OPENAI_API_KEY`
   - Value: `sk-...` (your OpenAI API key)

   **For Anthropic:**
   - Name: `ANTHROPIC_API_KEY`
   - Value: `sk-ant-...` (your Anthropic API key)

5. Click **Add secret**

### Step 3: Verify Dependencies

Ensure your `requirements.txt` includes the LLM client libraries:

```txt
# SOMAS Core Dependencies
pyyaml
filelock

# LLM API Integration (for autonomous mode)
openai>=1.0.0
anthropic>=0.18.0
```

These are already included if you're using the latest version.

### Step 4: Enable Autonomous Workflow

There are two ways to trigger autonomous execution:

#### Method 1: Label-Based Trigger (Automatic)

Add the label `somas:autonomous` to any issue with `somas-project` label:

1. Create a new issue using the "🤖 SOMAS Project Request" template
2. After issue creation, add the label `somas:autonomous`
3. The enhanced workflow will automatically start

#### Method 2: Manual Workflow Dispatch

1. Go to **Actions** → **SOMAS Project - Autonomous Execution (Enhanced)**
2. Click **Run workflow**
3. Enter the issue number
4. Optionally select a starting stage
5. Click **Run workflow**

## Usage

### Creating a New Project (Autonomous Mode)

1. **Create Issue**: Use the "🤖 SOMAS Project Request" template
2. **Add Label**: Add `somas:autonomous` label to the issue
3. **Wait**: The workflow will:
   - Initialize project structure
   - Create feature branch `somas/project-{issue_number}`
   - Invoke planning agent via direct API call
   - Generate `initial_plan.yml`
   - Commit artifacts
   - Post progress comment
   - Continue through stages 2-11 automatically

4. **Review**: Once complete, review the generated PR

### Monitoring Progress

#### In GitHub Actions

1. Go to **Actions** tab
2. Click on the running workflow
3. View logs for each stage
4. Check for ✅ success indicators or ❌ errors

#### In Issue Comments

The workflow posts updates after each stage:

```markdown
## ✅ Stage 1 Complete: Planning (SIGNAL)

**Project:** project-123

The planning agent has completed the initial analysis.

**Generated Artifact:**
- `initial_plan.yml` - Project plan with features, tech stack, and risk assessment

**Next Stage:** Specification (DESIGN) - Detailed requirements documentation

**Branch:** `somas/project-123`
```

### Fallback Behavior

If API keys are not configured or API calls fail, the system automatically falls back to comment-driven mode:

```markdown
## 🔄 Autonomous Execution Unavailable

Direct LLM API integration is not available. This could be due to:
- Missing API keys (OPENAI_API_KEY or ANTHROPIC_API_KEY)
- Missing dependencies (openai or anthropic packages)

**Falling back to comment-driven orchestration:**

@copilot somas-planner

Please analyze the project request...
```

## Workflow Files

| File | Purpose |
|------|---------|
| `.github/workflows/somas-autonomous-enhanced.yml` | Enhanced autonomous workflow with direct API integration |
| `.github/workflows/somas-orchestrator.yml` | Comment-driven orchestration (fallback) |
| `.github/workflows/somas-dev-autonomous.yml` | Original autonomous workflow (placeholder) |

## Architecture

### Autonomous Mode Flow

```
Issue Created with somas:autonomous label
    ↓
Initialize Project (Job 1)
    ↓
Create Feature Branch
    ↓
Stage 1: Planning (Job 2)
    ├─ Load AgentInvoker
    ├─ Check API keys available
    ├─ Load project request
    ├─ Invoke planner agent via OpenAI/Anthropic API
    ├─ Parse response for YAML code blocks
    ├─ Save initial_plan.yml
    ├─ Commit to branch
    └─ Post progress comment
    ↓
Stage 2: Specification (Job 3)
    ├─ Load initial_plan.yml
    ├─ Invoke specifier agent
    ├─ Save SPEC.md
    └─ Continue...
    ↓
... (Stages 3-11) ...
    ↓
Create Pull Request
```

### Fallback Mode Flow

```
Issue Created
    ↓
Initialize Project
    ↓
Post @copilot somas-planner comment
    ↓
Wait for Copilot response (requires manual Copilot assignment)
    ↓
Parse Copilot comment for artifacts
    ↓
Continue...
```

## Cost Considerations

### OpenAI (GPT-4o)

**Per Project Execution (Estimated):**
- Input tokens: ~50,000 tokens @ $2.50/1M = $0.125
- Output tokens: ~30,000 tokens @ $10.00/1M = $0.300
- **Total per project: ~$0.50**

**Monthly Costs:**
- 10 projects/month: ~$5
- 50 projects/month: ~$25
- 100 projects/month: ~$50

### Anthropic (Claude 3.5 Sonnet)

**Per Project Execution (Estimated):**
- Input tokens: ~50,000 tokens @ $3.00/1M = $0.150
- Output tokens: ~30,000 tokens @ $15.00/1M = $0.450
- **Total per project: ~$0.60**

**Monthly Costs:**
- 10 projects/month: ~$6
- 50 projects/month: ~$30
- 100 projects/month: ~$60

### GitHub Copilot (Comment-Driven Mode)

- Included in GitHub Copilot subscription ($10-$20/user/month)
- No per-request costs
- Limited by comment response time and manual assignment requirement

## Troubleshooting

### Issue: "No LLM API keys available"

**Cause:** API keys not set in repository secrets or not accessible to workflow.

**Solution:**
1. Verify secrets are created: Settings → Secrets and variables → Actions
2. Check secret names are exactly `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
3. Ensure workflow has `secrets` permission

### Issue: "OpenAI API Error: Insufficient quota"

**Cause:** API key has no credits or usage limit reached.

**Solution:**
1. Check OpenAI account billing
2. Add payment method or increase usage limits
3. Alternatively, add Anthropic API key as fallback

### Issue: "Anthropic API Error: Authentication failed"

**Cause:** Invalid or expired API key.

**Solution:**
1. Generate new API key from Anthropic Console
2. Update `ANTHROPIC_API_KEY` secret in GitHub
3. Re-run workflow

### Issue: Agent produces invalid artifacts

**Cause:** LLM response doesn't match expected format.

**Solution:**
1. Check workflow logs for full response
2. Verify agent prompt templates in `.github/agents/*.md`
3. Adjust temperature in `.somas/config.yml` (lower = more deterministic)

### Issue: Workflow times out

**Cause:** LLM API response taking too long or rate limiting.

**Solution:**
1. Check API provider status page
2. Add retry logic (future enhancement)
3. Fall back to comment-driven mode

## Security Considerations

### API Key Safety

✅ **DO:**
- Store API keys in GitHub Secrets
- Use repository secrets (not environment secrets for public repos)
- Rotate keys periodically
- Use separate keys for dev/prod if needed

❌ **DON'T:**
- Hardcode API keys in workflow files
- Commit API keys to repository
- Share API keys between projects unnecessarily
- Use personal API keys for organizational projects

### Input Validation

The `AgentInvoker` class includes security measures:

- **Project ID validation**: Prevents path traversal (must match `project-\d+`)
- **Filename validation**: Prevents directory escape attempts
- **Path resolution**: Ensures artifacts stay within project directory

### Rate Limiting

Consider adding rate limits to prevent abuse:

```yaml
# In workflow
- name: Check Rate Limit
  run: |
    # Check number of runs in last hour
    # Exit if threshold exceeded
```

## Advanced Configuration

### Custom Agent Models

Edit `.somas/config.yml` to change which model each agent uses:

```yaml
agents:
  providers:
    openai:
      model: "gpt-4o"  # Can change to gpt-4-turbo, etc.
      temperature: 0.3
  
  agent_configs:
    planner:
      provider: "openai"
    specifier:
      provider: "anthropic"  # Use Claude for specification
```

### Temperature Tuning

Adjust creativity vs. determinism per agent:

```yaml
agents:
  providers:
    openai:
      temperature: 0.1  # Very deterministic (code generation)
    anthropic:
      temperature: 0.5  # More creative (documentation)
```

### Timeout Configuration

Extend timeout for large projects:

```yaml
jobs:
  stage-planning:
    timeout-minutes: 30  # Default is usually 360 (6 hours)
```

## Next Steps

1. **Test with Small Project**: Create a simple project to verify setup
2. **Monitor Costs**: Track API usage in provider dashboards
3. **Refine Prompts**: Adjust agent prompts in `.github/agents/*.md` for better results
4. **Add More Stages**: Extend workflow to include all 11 stages
5. **Implement Retries**: Add error handling and retry logic for API failures

## Related Documentation

- [Workflow Integration Guide](./COPILOT_WORKFLOW_INTEGRATION.md) - Detailed architecture explanation
- [Agent Catalog](./.github/agents/README.md) - Complete list of agents and their roles
- [State Manager](../somas/core/state_manager.py) - State persistence implementation
- [Agent Invoker](../somas/core/agent_invoker.py) - LLM API integration

## Support

For issues or questions:

1. Check [Troubleshooting](#troubleshooting) section above
2. Review workflow logs in GitHub Actions
3. Create an issue with label `workflow-support`
4. Include relevant error messages and workflow run ID

---

**Version:** 1.0.0  
**Last Updated:** 2024-01-31  
**Maintainer:** SOMAS Core Team
