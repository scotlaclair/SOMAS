# SOMAS Autonomous Mode Guide

## Current Status: Limited Autonomy

SOMAS is designed for autonomous operation but currently has limitations that require manual intervention.

## How SOMAS Is Designed to Work

The system has two main workflows:

1. **somas-orchestrator.yml** - Comment-driven orchestration
2. **somas-pipeline.yml** - Staged pipeline execution

### The Design Intent

```
Issue Created → Label Added → Initialize Project → Invoke Agents → Parse Responses → Advance Pipeline
```

### The Reality

The orchestrator posts comments like `@copilot somas-planner` expecting GitHub Copilot to respond automatically. **This doesn't work** because:

1. **Copilot Coding Agent doesn't respond to @mentions** - It must be assigned to issues
2. **No automated assignment mechanism** - Someone must manually assign Copilot
3. **Response parsing expects specific formats** - Manual Copilot responses may not match

## How to Use SOMAS Today

### Option 1: Manual Copilot Assignment (Recommended)

1. Create an issue with the `somas:dev` label
2. Wait for SOMAS to post the initialization comment
3. **Manually assign Copilot** to the issue (click "Assignees" → select `@copilot`)
4. Copilot will create a PR with its implementation
5. Use the PR for review, don't expect comment-based responses

### Option 2: Use the Pipeline Directly

1. Create an issue with the `somas-project` label
2. The pipeline workflow runs through stages automatically
3. Note: Uses simulated/template outputs, not actual LLM calls

### Option 3: Comment-Based (Manual)

1. After SOMAS posts an `@copilot somas-*` comment
2. Manually respond with the expected YAML format
3. The orchestrator will parse your response and advance

## Known Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| Copilot doesn't auto-respond to @mentions | Blocks autonomy | Manually assign Copilot to issues |
| Simulated execution plans | Generic outputs | Implement actual LLM API calls |
| No LLM integration in runner.py | Placeholder only | Use Copilot via issue assignment |
| Two competing workflows | Confusion | Use only `somas:dev` OR `somas-project`, not both |

## Making SOMAS Truly Autonomous

To achieve full autonomy, the system needs:

### 1. Copilot Auto-Assignment (GitHub Feature Request)

Currently, there's no way to automatically assign Copilot to issues. GitHub would need to support:
- Webhook-triggered Copilot assignment
- Or Copilot responding to @mentions in comments

### 2. Direct LLM API Integration

Implement actual API calls in `somas/core/runner.py`:

```python
# Instead of waiting for Copilot comments, call APIs directly
def invoke_agent(agent_name: str, context: dict) -> str:
    config = load_agent_config(agent_name)

    if config['provider'] == 'openai':
        return call_openai_api(config, context)
    elif config['provider'] == 'anthropic':
        return call_anthropic_api(config, context)
    # etc.
```

### 3. Unified Workflow

Merge orchestrator and pipeline into a single coherent flow:
- Pipeline handles stage progression
- Each stage invokes LLM APIs directly
- Remove dependency on comment-based responses

## Environment Variables Required

For direct LLM integration, you would need:

```yaml
# In repository secrets
OPENAI_API_KEY: "sk-..."
ANTHROPIC_API_KEY: "sk-ant-..."
GOOGLE_AI_API_KEY: "..."
```

## Recommended Usage Pattern

Until full autonomy is implemented:

```bash
# 1. Create issue with description
gh issue create --title "Feature: Add user authentication" --body "..." --label "somas:dev"

# 2. Wait for SOMAS initialization comment
# 3. Assign Copilot manually
gh issue edit <number> --add-assignee "@copilot"

# 4. Copilot creates PR
# 5. Review and merge PR
```

## Architecture Decision

The current architecture chose comment-based orchestration to:
- Maintain transparency (all agent interactions visible in issue comments)
- Allow human oversight at each stage
- Support multiple AI providers via comments

The tradeoff is that it requires either:
- GitHub to support auto-responding Copilot
- Or manual intervention to trigger each stage

## Future Improvements

1. **Workflow Dispatch Trigger**: Add manual dispatch to trigger specific stages
2. **API-First Mode**: Add flag to use direct API calls instead of comments
3. **Hybrid Mode**: Use APIs for execution, post summaries as comments
4. **Copilot Webhook**: Monitor for new issues and auto-assign Copilot via API

## Related Files

- `.github/workflows/somas-orchestrator.yml` - Comment-driven orchestration
- `.github/workflows/somas-pipeline.yml` - Staged pipeline
- `somas/core/runner.py` - Agent execution framework
- `.somas/config.yml` - System configuration
