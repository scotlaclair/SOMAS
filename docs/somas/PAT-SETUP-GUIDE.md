# Personal Access Token (PAT) Setup Guide for SOMAS Autonomy

## Overview

By default, GitHub Actions workflows use the automatic `GITHUB_TOKEN`, which has important limitations:

- **Cannot trigger other workflows** - Prevents cascade execution
- **Cannot act with user permissions** - Appears as GitHub bot
- **May cause approval blocks** - Some operations require user-level access

To enable **true autonomous operation**, you need to create a **Fine-grained Personal Access Token (PAT)**.

## Why This Matters

Without a PAT, SOMAS cannot:

- Automatically trigger the next stage workflow after completing one
- Create issues or PRs that trigger workflow automations
- Perform operations that require your user-level permissions

With a PAT, SOMAS gains full autonomous capability to:

- Execute the entire 7-stage pipeline without manual intervention
- Create issues/PRs that trigger other workflows
- Act with your permissions for protected operations

## Setup Instructions

### 1. Create the Fine-grained Token

1. Go to GitHub Settings: **Settings** → **Developer settings** → **Personal access tokens** → **Fine-grained tokens**
2. Click **"Generate new token"**

### 2. Configure Token Settings

**Token Name (GitHub display only, can be any descriptive label):** `SOMAS-Autonomous`

This token name is just for your reference in GitHub and does **not** need to match the repository secret name. Later, when you add this token as a GitHub secret, be sure to name the secret **exactly** `SOMAS_PAT`.

**Repository access:** Select "Only select repositories"

- Choose: `scotlaclair/SOMAS`

**Permissions:**

```
Repository Permissions:
  - Contents: Read and write
  - Issues: Read and write
  - Pull requests: Read and write
  - Workflows: Read and write
  - Actions: Read and write
  - Metadata: Read-only (automatic)
```

**Expiration:** Choose based on your preference

- 90 days (recommended for testing)
- 1 year (for production use)
- No expiration (requires admin privileges, use cautiously)

### 3. Generate and Copy Token

1. Click **"Generate token"**
2. **IMPORTANT:** Copy the token immediately (you won't see it again!)
3. Store it securely

### 4. Add Token to Repository Secrets

1. Go to your repository: `https://github.com/scotlaclair/SOMAS`
2. Navigate to: **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Configure:
   - **Name:** `SOMAS_PAT`
   - **Value:** Paste the token you copied
5. Click **"Add secret"**

### 5. Workflow Configuration

The SOMAS workflows are designed to work with `SOMAS_PAT` to enable autonomous execution and cascading workflow triggers.

**Workflow pattern:**

```yaml
- uses: actions/checkout@v4
  with:
    token: ${{ secrets.SOMAS_PAT || secrets.GITHUB_TOKEN }}
```

This pattern ensures:

- Uses `SOMAS_PAT` when available (autonomous mode with workflow triggering)
- Falls back to `GITHUB_TOKEN` if not configured (standard mode)

**Note:** Workflow updates to utilize PAT for cascading workflow execution will be implemented in a future enhancement. Setting up the PAT now ensures it's ready when those updates are made.

## Verification

After setup, verify the token works:

1. Create a test SOMAS project issue
2. Add the `somas:start` label
3. Watch the pipeline execute
4. Check that stages automatically trigger each other

You should see:

- ✅ Workflows triggering subsequent workflows
- ✅ PRs created with your username (not "github-actions[bot]")
- ✅ No manual approval required for stage transitions

## Security Best Practices

### Token Security

- ✅ Use Fine-grained tokens (not Classic tokens)
- ✅ Limit to single repository
- ✅ Use minimum required permissions
- ✅ Set expiration dates
- ✅ Rotate tokens regularly
- ❌ Never commit tokens to code
- ❌ Never share tokens

### Access Control

- Only grant to repositories you fully control
- Review token permissions quarterly
- Revoke unused tokens immediately
- Monitor token usage in audit log

### If Token is Compromised

1. Go to Settings → Developer settings → Personal access tokens
2. Find the compromised token
3. Click **"Revoke"** immediately
4. Generate a new token
5. Update repository secret with new token
6. Review audit logs for unauthorized activity

## Troubleshooting

### Token Not Working

**Problem:** Workflows still can't trigger each other

**Solutions:**

1. Verify token name is exactly `SOMAS_PAT` (case-sensitive)
2. Check token hasn't expired
3. Confirm all required permissions are granted
4. Verify token has access to the repository

### Permission Denied Errors

**Problem:** "Resource not accessible by integration"

**Solutions:**

1. Check token has required permission (Contents, Issues, PRs, Workflows)
2. Verify repository access is granted
3. Ensure token hasn't been revoked
4. Try regenerating the token

### Workflows Using Wrong Token

**Problem:** PRs still show "github-actions[bot]"

**Solutions:**

1. Check workflows are using `${{ secrets.SOMAS_PAT }}`
2. Verify secret is correctly named `SOMAS_PAT`
3. Restart failed workflow runs to pick up new token

## Cost

**Free** - No additional cost for Fine-grained PATs

## Time Required

**15 minutes** for initial setup

## Related Documentation

- [GitHub Fine-grained PAT Documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-fine-grained-personal-access-token)
- [GitHub Actions Authentication](https://docs.github.com/en/actions/security-guides/automatic-token-authentication)
- [SOMAS Autonomous Pipeline](../AUTONOMOUS_PIPELINE_SUMMARY.md)

## Summary

| Feature | GITHUB_TOKEN | SOMAS_PAT |
|---------|--------------|-----------|
| Trigger workflows | ❌ No | ✅ Yes |
| User attribution | ❌ Bot only | ✅ Your username |
| Protected operations | ❌ Limited | ✅ Full access |
| Setup time | 0 min (automatic) | 15 min (manual) |
| Security | ✅ Automatic | ✅ Scoped permissions; ⚠️ Manual rotation |
| Expiration | Never | Yes (configurable) |

**Recommendation:** Set up `SOMAS_PAT` for true autonomous operation, but maintain good security practices.
