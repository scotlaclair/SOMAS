# Example PR Review with Structured Recommendations

This document provides example PR review comments with structured recommendations that will be automatically captured by the SOMAS meta-capture process.

---

## Example 1: Circuit Breaker Implementation Review

**Context:** PR adding circuit breaker functionality to the SOMAS pipeline

```markdown
Great work on implementing the circuit breaker! The core functionality looks solid. Here are some observations and recommendations:

### Code Review

✅ **Strengths:**
- Clean implementation of the circuit breaker pattern
- Good test coverage for happy path scenarios
- Clear configuration structure

⚠️ **Issues:**
- State is in-memory only (will reset on restart)
- No metrics/monitoring integration
- Edge case: concurrent state transitions not thread-safe

## Recommendations

### Must Address Soon
- Add circuit breaker state persistence to avoid thundering herd on restart
- Fix race condition in state transition logic (use locks or atomic operations)
- Document circuit breaker threshold decisions in an ADR

### Should Consider
- Add Prometheus/OpenTelemetry metrics for circuit breaker state changes
- Implement exponential backoff for retry attempts
- Add configuration validation on startup

### Future Enhancement
- Support distributed circuit breaker coordination across replicas
- Add circuit breaker dashboard for monitoring
- Implement adaptive threshold adjustment based on error patterns
```

---

## Example 2: JSON State Persistence Review

**Context:** PR adding JSON-based state persistence for pipeline artifacts

```markdown
Thanks for tackling state persistence! The JSON approach is a good starting point. Review feedback below:

### Code Review

✅ **Strengths:**
- Simple, readable format
- Easy to debug and inspect manually
- Good use of atomic writes

⚠️ **Issues:**
- No schema validation (could lead to corruption)
- Missing migration strategy for schema changes
- Large state files could impact performance

## Recommendations

### Must Address Soon
- Add JSON schema validation on read/write to prevent corruption
- Implement state migration strategy for backward compatibility
- Add error handling for corrupted state files

### Should Consider
- Add compression for large state files (gzip or similar)
- Consider alternative storage backends (Redis, SQLite) for production
- Implement state file versioning
- Add state size limits and warnings

### Future Enhancement
- State snapshotting for point-in-time recovery
- State replication for high availability
- Incremental state updates instead of full rewrites
```

---

## Example 3: Configuration Refactoring Review

**Context:** PR refactoring configuration management

```markdown
Nice refactor! Configuration is much cleaner. A few thoughts:

### Code Review

✅ **Strengths:**
- Centralized configuration in `.somas/config.yml`
- Type-safe configuration access
- Good separation of concerns

⚠️ **Issues:**
- Configuration reload requires restart
- No validation of required fields at startup
- Secrets management needs improvement

## Recommendations

### Must Address Soon
- Add configuration validation on startup with clear error messages
- Move secrets to GitHub Secrets or environment variables
- Document all configuration options in config file comments

### Should Consider
- Support hot-reload of non-critical configuration
- Add configuration schema validation (JSON Schema or similar)
- Create configuration migration guide for users
- Add configuration defaults for optional fields

### Future Enhancement
- Dynamic configuration reload without restart
- Configuration versioning and rollback
- Multi-environment configuration support (dev/staging/prod)
```

---

## Example 4: Testing Enhancement Review

**Context:** PR improving test coverage

```markdown
Excellent test additions! Coverage is much better now.

### Code Review

✅ **Strengths:**
- Good coverage of edge cases
- Clear test descriptions
- Fast execution time

⚠️ **Issues:**
- Integration tests missing
- Mock setup is duplicated across tests
- Some tests are flaky

## Recommendations

### Must Address Soon
- Fix flaky tests in `test_simulation.py` (timing-dependent)
- Add integration tests for end-to-end pipeline flow

### Should Consider
- Create test fixtures for common mock setups
- Add performance regression tests
- Document testing strategy in CONTRIBUTING.md
- Add tests for error scenarios and retries

### Future Enhancement
- Add property-based testing for complex algorithms
- Add mutation testing to verify test quality
- Create visual regression tests for UI components
```

---

## Example 5: Security Enhancement Review

**Context:** PR adding input validation

```markdown
Good security improvements! Input validation is critical.

### Code Review

✅ **Strengths:**
- Proper validation of project IDs
- Use of allowlists instead of denylists
- Clear error messages

⚠️ **Issues:**
- SQL injection risk in search functionality
- XSS risk in error message rendering
- Rate limiting not implemented

## Recommendations

### Must Address Soon
- Fix SQL injection vulnerability in search (use parameterized queries)
- Escape user input in error messages to prevent XSS
- Add rate limiting to API endpoints

### Should Consider
- Add CSRF protection for state-changing operations
- Implement input size limits
- Add security headers (CSP, X-Frame-Options, etc.)
- Create security documentation and threat model

### Future Enhancement
- Add security audit logging
- Implement anomaly detection for suspicious patterns
- Add automated security testing in CI/CD
```

---

## Tips for Writing Structured Recommendations

### Do's ✅

- **Be Specific**: Each recommendation should be clear and actionable
- **Provide Context**: Explain why the recommendation matters
- **Categorize Correctly**: Use appropriate priority level
- **Link Examples**: Reference similar patterns or previous PRs
- **Include Rationale**: Explain the impact of not addressing

### Don'ts ❌

- **Avoid Vague Recommendations**: "Improve performance" is too vague
- **Don't Mix Priorities**: Don't put minor issues in "Must Address Soon"
- **Don't Skip Context**: Explain why it matters, not just what to do
- **Don't Forget Trade-offs**: Mention if there are downsides to consider

---

## How Recommendations Are Processed

1. **Parsing**: The meta-capture workflow scans PR comments for `## Recommendations` sections
2. **Routing**:
   - "Must Address Soon" → Creates GitHub issues with `somas:follow-up` label
   - "Should Consider" → Adds to `.somas/backlog.md`
   - "Future Enhancement" → Adds to `.somas/roadmap.md`
3. **Preservation**: All items link back to source PR and comment for context
4. **Idempotency**: Marker prevents duplicate processing

---

## Related Documentation

- [Meta-Capture Process](../docs/somas/meta-capture-process.md) - Complete guide
- [Meta-Capture Template](meta-capture.md) - Manual capture template
- [Backlog File](../backlog.md) - Backlog tracking
- [Roadmap File](../roadmap.md) - Roadmap planning
- [ADR Directory](../architecture/ADRs/) - Architecture decision records

---

**Note:** Use this structured format in PR reviews to ensure valuable insights are captured and made actionable through the SOMAS meta-capture process.
