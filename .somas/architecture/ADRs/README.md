# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records for the SOMAS project. ADRs document significant architectural and design decisions made throughout the project lifecycle.

---

## What is an ADR?

An Architecture Decision Record (ADR) is a document that captures an important architectural decision made along with its context and consequences.

### When to Create an ADR

Create an ADR when:
- Making a significant architectural choice
- Selecting between competing design alternatives
- Establishing system-wide patterns or conventions
- Making technology or framework selections
- Defining security, performance, or scalability approaches
- Documenting process or workflow decisions that affect the system

### When NOT to Create an ADR

Don't create an ADR for:
- Minor implementation details
- Obvious or standard industry practices
- Temporary workarounds
- Personal coding preferences

---

## ADR Format

Each ADR follows this structure:

```markdown
# ADR-XXX: [Decision Title]

**Status:** Proposed | Accepted | Deprecated | Superseded  
**Date:** YYYY-MM-DD  
**Deciders:** [Names or roles]  
**Source:** [PR #XX, Issue #YY, or Planning Session]

## Context

[Describe the issue or situation requiring a decision]

## Decision

[State the decision that was made]

## Rationale

[Explain why this decision was chosen]

## Alternatives Considered

### Alternative 1: [Name]
[Description, pros, cons, why not chosen]

### Alternative 2: [Name]
[Description, pros, cons, why not chosen]

## Consequences

### Positive
- Benefit 1
- Benefit 2

### Negative
- Trade-off 1
- Trade-off 2

### Neutral
- Side effect 1

## Implementation

[How this decision will be implemented]

## Related

- Related ADR: ADR-XXX
- Related Issue: #XX
- Related PR: #YY
```

---

## Naming Convention

ADRs are numbered sequentially and use kebab-case slugs:

```
ADR-001-initial-agent-architecture.md
ADR-002-circuit-breaker-implementation.md
ADR-003-state-persistence-strategy.md
```

---

## ADR Lifecycle

1. **Proposed** - Decision is suggested and under discussion
2. **Accepted** - Decision is approved and should be followed
3. **Deprecated** - Decision is outdated but kept for historical context
4. **Superseded** - Replaced by a newer ADR (reference the superseding ADR)

---

## Creating an ADR

### Manual Creation

1. Determine the next ADR number by checking existing files
2. Create a new file: `ADR-XXX-[slug].md`
3. Fill in the template with decision details
4. Commit and create PR for review

### Via Meta-Capture Process

ADRs can be automatically created from PR review recommendations:
1. PR review includes architectural recommendation
2. Meta-capture process routes it to ADR creation
3. ADR template is generated with recommendation content
4. Owner reviews, refines, and merges

---

## Index of ADRs

### Active ADRs

*No ADRs yet. ADRs will be added as architectural decisions are made.*

### Deprecated ADRs

*None yet.*

---

## Best Practices

1. **Keep it concise** - ADRs should be readable in 5-10 minutes
2. **Focus on "why"** - The rationale is more important than the details
3. **Document alternatives** - Show what was considered and why it wasn't chosen
4. **Include consequences** - Both positive and negative outcomes
5. **Link to sources** - Reference PRs, issues, or discussions
6. **Update status** - Mark as deprecated or superseded when appropriate
7. **Review before merge** - Get team feedback on significant decisions

---

## Related Documentation

- `.somas/templates/meta-capture.md` - Template for capturing recommendations
- `.somas/architecture/` - Architecture documentation and diagrams
- `docs/somas/COPILOT_GUIDE.md` - Guide for Copilot integration
- `.github/workflows/somas-meta-capture.yml` - Workflow for automated ADR creation

---

## References

- [ADR GitHub Organization](https://adr.github.io/)
- [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [Architecture Decision Records at Thoughtworks](https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records)
