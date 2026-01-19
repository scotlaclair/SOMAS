# Pull Request

## Description

<!-- Provide a clear and concise description of the changes in this PR -->

## Type of Change

<!-- Mark the relevant option with an 'x' -->

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Security fix

## Related Issues

<!-- Link to related issues using #issue_number -->

Fixes #
Related to #

## Changes Made

<!-- List the specific changes made in this PR -->

- 
- 
- 

## Testing

<!-- Describe the testing you've done -->

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] E2E tests added/updated
- [ ] Manual testing performed
- [ ] All tests passing

### Test Coverage

- Previous coverage: ___%
- New coverage: ___%

## SOMAS Agent Assignments

This PR is part of the SOMAS pipeline. The following specialized agents (with their optimized AI models) are assigned to different review aspects:

### Automated Reviews

- [ ] **Architecture Review** - @copilot somas-architect *(Claude 3.7 Sonnet - System Design)*
  - Verify architectural consistency with ARCHITECTURE.md
  - Check design patterns are correctly applied
  - Validate component boundaries and dependencies

- [ ] **Code Review** - @copilot somas-reviewer *(o1 - Logic Analysis)*
  - Identify logic flaws and edge cases
  - Verify requirements coverage
  - Check code quality and maintainability

- [ ] **Security Review** - @copilot somas-security *(o1 - Adversarial Analysis)*
  - Scan for OWASP Top 10 vulnerabilities
  - Verify input validation and sanitization
  - Check authentication and authorization logic

- [ ] **Test Coverage** - @copilot somas-tester *(GPT-4o - High-Volume Testing)*
  - Verify test coverage meets 80% minimum
  - Check edge cases are tested
  - Validate test quality and assertions

- [ ] **Documentation** - @copilot somas-documenter *(Gemini 2.0 Flash - Context-Aware Docs)*
  - Verify documentation is complete and accurate
  - Check API documentation is updated
  - Ensure inline comments are clear

- [ ] **Performance Analysis** - @copilot somas-optimizer *(o1 - Algorithmic Optimization)*
  - Analyze algorithmic complexity
  - Identify performance bottlenecks
  - Verify performance requirements are met

### Manual Reviews

- [ ] **Human Review** - [@reviewer-username]
  - Final approval required before merge

## Multi-Model Advantage

💡 **SOMAS uses specialized AI models for each review type**:
- **o1** for deep reasoning (security, code review, optimization)
- **Claude 3.7 Sonnet** for architecture and code quality
- **Gemini 2.0 Flash** for comprehensive documentation with full repo context
- **GPT-4o** for fast, high-volume test generation

This multi-model approach ensures each aspect is reviewed by the AI model best suited for that specific cognitive task.

## Checklist

<!-- Mark completed items with an 'x' -->

### Code Quality
- [ ] Code follows project style guidelines
- [ ] Self-review of code performed
- [ ] Comments added for complex logic
- [ ] No commented-out code or debug statements
- [ ] No TODOs left without tracking issues

### Security
- [ ] No secrets or credentials in code
- [ ] Input validation implemented
- [ ] Output sanitization implemented
- [ ] Authentication/authorization checked
- [ ] Dependencies scanned for vulnerabilities

### Documentation
- [ ] README updated (if needed)
- [ ] API documentation updated (if needed)
- [ ] Inline code comments added for complex logic
- [ ] CHANGELOG updated (if applicable)
- [ ] Architecture docs updated (if applicable)

### Testing
- [ ] Unit tests cover new code
- [ ] Integration tests added (if needed)
- [ ] E2E tests added (if needed)
- [ ] All existing tests pass
- [ ] Manual testing completed

### Performance
- [ ] No obvious performance issues
- [ ] Database queries optimized
- [ ] Caching implemented where appropriate
- [ ] Performance tests added (if needed)

## Screenshots/Recordings

<!-- If applicable, add screenshots or recordings to demonstrate the changes -->

## Deployment Notes

<!-- Any special considerations for deployment? -->

- [ ] Database migrations required
- [ ] Configuration changes required
- [ ] Environment variables added/changed
- [ ] Third-party service configuration needed
- [ ] Deployment documentation updated

## Rollback Plan

<!-- How can this change be rolled back if issues are found? -->

## Additional Context

<!-- Add any other context about the PR here -->

---

## For Reviewers

### Review Focus Areas

1. **Correctness**: Does the code do what it's supposed to do?
2. **Security**: Are there any security vulnerabilities?
3. **Performance**: Are there any performance concerns?
4. **Maintainability**: Is the code easy to understand and modify?
5. **Testing**: Is the code adequately tested?

### SOMAS Agent Review Instructions

To invoke specific agent reviews, comment on this PR:

```
@copilot somas-security perform security analysis of authentication changes

@copilot somas-optimizer analyze performance of the new search algorithm

@copilot somas-reviewer review error handling logic in UserService.js
```

Each agent uses a specialized AI model optimized for its domain:
- Security analysis uses **o1** for adversarial thinking
- Architecture review uses **Claude 3.7 Sonnet** for structural consistency  
- Performance analysis uses **o1** for algorithmic complexity reasoning
- Documentation uses **Gemini 2.0 Flash** for full-repository context
