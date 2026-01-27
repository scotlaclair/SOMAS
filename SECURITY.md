# Security Policy

## Supported Versions

We take security seriously in SOMAS (Self-Sovereign Orchestrated Multi-Agent System). The following versions are currently supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| < 1.0   | :x:                |

## Security Model

SOMAS is an AI-first SDLC that orchestrates multiple AI agents. Our security model addresses:

### 1. **Agent Security**
- **Input Validation**: All project IDs and user inputs are validated to prevent path traversal and injection attacks
- **Secrets Management**: Secrets are never hardcoded; we use GitHub Secrets and environment variables
- **Agent Isolation**: Each agent operates in isolated contexts with minimal permissions

### 2. **Pipeline Security**
- **Workflow Security**: GitHub Actions workflows use pinned versions and minimal permissions
- **Artifact Protection**: Generated artifacts are validated before storage
- **Code Injection Prevention**: All shell commands use proper quoting; JSON operations use Python (not bash/jq)

### 3. **Data Security**
- **No Sensitive Data Storage**: Project metadata contains no secrets or PII
- **Path Validation**: All file paths are validated before operations
- **Configuration Validation**: YAML/JSON configs are schema-validated

## Reporting a Vulnerability

**DO NOT** open a public issue for security vulnerabilities.

### How to Report

1. **GitHub Security Advisories** (Preferred):
   - Navigate to the [Security tab](https://github.com/scotlaclair/SOMAS/security/advisories)
   - Click "Report a vulnerability"
   - Fill in the details using the template below

2. **Email**: scotlaclair@github.com
   - Subject: `[SECURITY] SOMAS Vulnerability Report`
   - Include details as per template below

### Report Template

```
**Vulnerability Type**: [e.g., Path Traversal, Code Injection, etc.]

**Affected Component**: [e.g., workflow file, agent configuration, etc.]

**Severity**: [Critical/High/Medium/Low]

**Description**: 
[Detailed description of the vulnerability]

**Steps to Reproduce**:
1. 
2. 
3. 

**Impact**:
[What can an attacker achieve?]

**Suggested Fix**:
[If you have ideas for remediation]

**Environment**:
- Python Version:
- OS:
- Relevant configuration:
```

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: 
  - Critical: 1-7 days
  - High: 7-14 days
  - Medium: 14-30 days
  - Low: 30-90 days

## Security Best Practices for Contributors

### When Contributing Code

1. **Input Validation**
   ```python
   # ✅ GOOD: Validate project IDs with strict pattern
   import re
   from pathlib import Path
   
   def validate_project_id(project_id: str) -> bool:
       """
       Validate project ID to prevent path traversal and injection attacks.
       
       SECURITY: Project IDs must match pattern 'project-\\d+' only.
       This prevents:
       - Path traversal (../../../etc/passwd)
       - Command injection (project-1; rm -rf /)
       - Directory escape (project-1/../../)
       """
       if not re.match(r'^project-\d+$', project_id):
           raise ValueError(f"Invalid project ID format: {project_id}")
       return True
   
   def get_safe_project_path(project_id: str, base_dir: Path) -> Path:
       """Safely construct project path with validation."""
       validate_project_id(project_id)
       
       base_path = Path(base_dir).resolve()
       project_path = (base_path / project_id).resolve()
       
       # Verify path stays within base directory using pathlib
       try:
           project_path.relative_to(base_path)
       except ValueError:
           # Avoid logging potentially malicious input
           raise ValueError("Path traversal attempt detected")
       
       return project_path
   ```

   ```python
   # ❌ BAD: No validation
   project_path = f"projects/{user_input}/"  # Vulnerable to path traversal
   ```

2. **Secrets Management**
   ```yaml
   # ✅ GOOD: Use GitHub Secrets
   env:
     API_KEY: ${{ secrets.OPENAI_API_KEY }}
   ```

   ```yaml
   # ❌ BAD: Hardcoded secrets
   env:
     API_KEY: "sk-1234567890abcdef"  # Never do this!
   ```

3. **Command Execution**
   ```python
   # ✅ GOOD: Use subprocess with list arguments
   import subprocess
   subprocess.run(['git', 'add', filename], check=True)
   ```

   ```bash
   # ❌ BAD: Shell injection risk
   git add $FILENAME  # Vulnerable if FILENAME contains malicious input
   ```

4. **JSON/YAML Processing**
   ```python
   # ✅ GOOD: Use Python libraries
   import json
   data = json.loads(input_string)
   ```

   ```bash
   # ❌ BAD: Using jq in bash (harder to validate)
   echo "$INPUT" | jq '.field'  # Risky
   ```

5. **Safe Environment Variable Usage in Workflows**
   ```yaml
   # ✅ GOOD: Use Python for safe processing of user input
   - name: Safe Shell Usage
     env:
       USER_INPUT: ${{ github.event.issue.title }}
     run: |
       # Use Python to safely process user input
       python3 <<'PYTHON'
       import os
       import json
       title = os.environ.get("USER_INPUT", "")
       # Now title is a safe Python string, not shell-interpolated
       print(f"Title: {json.dumps(title)}")
       PYTHON
   ```

   ```yaml
   # ❌ BAD: Direct shell interpolation
   - name: Unsafe Shell Usage
     env:
       TITLE: ${{ github.event.issue.title }}
     run: |
       echo "Title: $TITLE"  # Shell injection possible
   ```

## Input Validation Security

### Project ID Validation

All project IDs MUST match the pattern `^project-\d+$`. This is enforced by 
`StateManager._validate_project_id()` in `somas/core/state_manager.py`.

**Never** use raw user input (issue titles, PR descriptions, comments) for:
- File paths or directory names
- Shell command arguments without proper escaping
- Branch names without sanitization

### Safe Patterns

| Context | Unsafe | Safe |
|---------|--------|------|
| Shell | `echo $TITLE` | Use Python with `os.environ` |
| Python | `os.system(f"cmd {title}")` | `subprocess.run(["cmd", title])` |
| Paths | `Path(user_input)` | `validate_project_id(input)` then `_get_safe_project_path()` |
| JSON | String concatenation | `json.dumps(value)` |
| Workflow | `${{ github.event.issue.title }}` in shell | Pass as env var, process with Python |

### Defense-in-Depth Strategy

SOMAS implements multiple layers of security:

1. **Validation Layer**: Strict regex validation of project IDs (`^project-\d+$`)
2. **Path Resolution Layer**: Resolve symlinks and relative paths to absolute paths
3. **Boundary Check Layer**: Verify resolved paths stay within base directory
4. **Safe Processing Layer**: Use Python for JSON/environment variable processing

### Audit Checklist

When reviewing code or workflows:

- [ ] All `github.event.issue.title` usages pass through safe processing
- [ ] All `github.event.issue.body` usages pass through safe processing
- [ ] All environment variables with user input are processed via Python
- [ ] Project ID validation called before path construction
- [ ] Path traversal check after path construction (use `_get_safe_project_path()`)
- [ ] No direct shell interpolation of user input

### Security Checklist for PRs

Before submitting a PR, ensure:

- [ ] All user inputs are validated
- [ ] No secrets or API keys in code
- [ ] No use of `eval()`, `exec()`, or similar dangerous functions
- [ ] File paths are validated before operations
- [ ] SQL queries use parameterization (if applicable)
- [ ] Dependencies are from trusted sources
- [ ] Shell commands use proper quoting/escaping
- [ ] Error messages don't leak sensitive information

## Security Features

### Enabled GitHub Security Features

- ✅ **Dependabot Alerts**: Automated vulnerability scanning for dependencies
- ✅ **Dependabot Security Updates**: Automatic PR creation for security fixes
- ✅ **Code Scanning (CodeQL)**: Static analysis for security vulnerabilities
- ✅ **Secret Scanning**: Prevents accidental secret commits
- ✅ **Branch Protection**: Requires reviews and checks before merging

### Security Workflows

1. **CodeQL Analysis** (`.github/workflows/codeql-analysis.yml`)
   - Scans Python code for security issues
   - Runs on push and PR
   - Analyzes shell scripts for command injection

2. **Dependency Review** (`.github/workflows/dependency-review.yml`)
   - Blocks PRs with vulnerable dependencies
   - Checks license compliance

3. **Secret Scanning**
   - Push protection enabled
   - Scans commit history

## Known Security Considerations

### AI Agent Risks

1. **Prompt Injection**: While SOMAS uses structured prompts, malicious project descriptions could attempt prompt injection
   - **Mitigation**: Template-based prompts with validation

2. **Resource Exhaustion**: Large/complex projects could consume excessive AI tokens
   - **Mitigation**: Token limits and cost monitoring

3. **Data Leakage**: AI agents process project data
   - **Mitigation**: Never include secrets in project specs; use environment variables

### Workflow Risks

1. **Third-party Actions**: We use GitHub-verified actions with pinned versions
2. **Token Permissions**: Workflows use minimal `GITHUB_TOKEN` permissions

## Security Updates

Security updates are announced via:
- GitHub Security Advisories
- Repository Security tab
- Release notes (for public disclosures post-fix)

## Compliance

SOMAS follows:
- **OWASP Top 10**: We address common web application security risks
- **CWE Top 25**: Mitigation for most dangerous software weaknesses
- **GitHub Security Best Practices**: Following official GitHub security recommendations

## Questions?

For non-sensitive security questions, open a discussion in [GitHub Discussions](https://github.com/scotlaclair/SOMAS/discussions).

For security-related bug bounty or vulnerability disclosure, follow the reporting process above.

---

**Last Updated**: 2026-01-22 12:21:06  
**Security Contact**: scotlaclair@github.com