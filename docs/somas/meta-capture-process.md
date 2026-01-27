# SOMAS Meta-Capture Process

## Overview

The SOMAS Meta-Capture Process automatically extracts, categorizes, and routes valuable recommendations from PR review comments to ensure institutional knowledge is preserved and made actionable.

---

## The Problem

SOMAS PRs and reviews routinely contain rich, high-signal recommendations about:
- Architecture decisions
- Configuration improvements  
- Process enhancements
- Testing strategies
- Security considerations
- Performance optimizations

These insights risk being lost in PR comments after merge, reducing project memory and strategic evolution.

---

## The Solution

An automated meta-process that:

1. **Scans** merged PR comments for structured recommendations
2. **Categorizes** items by priority (Must Address Soon, Should Consider, Future Enhancement)
3. **Routes** recommendations to appropriate artifacts:
   - **Must Address Soon** → Create follow-up issues with `somas:follow-up` label
   - **Should Consider** → Add to `.somas/backlog.md`
   - **Future Enhancements** → Add to `.somas/roadmap.md`
4. **Preserves** context with links back to source PR and comments
5. **Prevents** duplicates using idempotent markers

**Note:** For architectural decisions that warrant an ADR, use the manual meta-capture template to document the decision in `.somas/architecture/ADRs/` following the guidelines in the ADR README.

---

## How It Works

### 1. Structured Recommendations in PR Reviews

When reviewing a PR, use this structured format in your comments:

```markdown
## Recommendations

### Must Address Soon
- Recommendation that needs immediate follow-up
- Another critical item to address

### Should Consider  
- Item worth considering for backlog
- Improvement idea for future consideration

### Future Enhancement
- Long-term enhancement opportunity
- Strategic improvement for roadmap
```

### 2. Automatic Processing on PR Merge

When a PR with `somas:approved` or `somas:reviewed` label is merged:

1. The `somas-meta-capture` workflow triggers
2. Scans all PR comments for `## Recommendations` sections
3. Parses priority sections (Must Address Soon, Should Consider, Future Enhancement)
4. Routes each item appropriately:
   - Creates GitHub issues for "Must Address Soon" items
   - Appends to backlog file for "Should Consider" items  
   - Appends to roadmap file for "Future Enhancement" items
5. Commits updates to backlog/roadmap files
6. Posts summary comment on PR with marker to prevent re-processing

### 3. Manual Meta-Capture

For recommendations that need more detailed handling:

1. Create a new file using the meta-capture template:
   ```bash
   cp .somas/templates/meta-capture.md \
      .somas/captures/meta-capture-PR-XX-YYYY-MM-DD.md
   ```

2. Fill in the template with recommendation details

3. Route according to the template's guidance:
   - Create follow-up issue
   - Generate ADR
   - Update backlog/roadmap
   - Assign owner

---

## Recommendation Categories

### Must Address Soon

**Criteria:**
- Blocks or significantly impacts production readiness
- Security or critical bug fix
- Breaks user workflow or experience
- Architectural flaw that compounds over time

**Routing:** Automatic GitHub issue creation with `somas:follow-up` label

**Example:**
```markdown
### Must Address Soon
- Add circuit breaker state persistence to avoid thundering herd on restart
- Implement rate limiting to prevent API abuse
```

### Should Consider

**Criteria:**
- Valuable improvement but not urgent
- Process enhancement
- Code quality improvement
- Technical debt reduction opportunity

**Routing:** Added to `.somas/backlog.md` for future consideration

**Example:**
```markdown
### Should Consider
- Refactor configuration loading to reduce duplication
- Add more comprehensive error messages
```

### Future Enhancement

**Criteria:**
- Long-term strategic improvement
- Performance optimization opportunity
- Feature expansion possibility
- Research and development idea

**Routing:** Added to `.somas/roadmap.md` for strategic planning

**Example:**
```markdown
### Future Enhancement
- Monte Carlo simulation with adaptive sampling
- Multi-region deployment support
```

---

## Artifacts and Storage

### Follow-up Issues

**Location:** GitHub Issues  
**Label:** `somas:follow-up`, `somas:change`  
**Format:**
```markdown
## Follow-up from PR #XX

**Source:** [PR URL]
**Review Comment:** [Comment URL]
**Reviewer:** @username

### Recommendation
[Recommendation text]

### Context
[PR context and background]

### Next Steps
- [ ] Review and validate priority
- [ ] Determine implementation approach  
- [ ] Assign to appropriate stage
- [ ] Execute through SOMAS pipeline
```

### Backlog File

**Location:** `.somas/backlog.md`  
**Purpose:** Track items worth considering but not yet scheduled  
**Organization:** By category (Architecture, Testing, Documentation, etc.)

### Roadmap File

**Location:** `.somas/roadmap.md`  
**Purpose:** Track future enhancements and strategic direction  
**Organization:** By release version (v0.2.x, v0.3.x, v1.0+)

### Architecture Decision Records

**Location:** `.somas/architecture/ADRs/`  
**Naming:** `ADR-XXX-[slug].md`  
**Purpose:** Document significant architectural decisions

For architectural recommendations, create an ADR:
```bash
# Determine next ADR number
ls .somas/architecture/ADRs/ADR-*.md | wc -l

# Create new ADR
touch .somas/architecture/ADRs/ADR-XXX-decision-title.md
```

See `.somas/architecture/ADRs/README.md` for ADR template and guidelines.

---

## Workflow Details

### Trigger Conditions

The workflow triggers when:
- A PR is closed with `merged == true`
- PR has label `somas:approved` OR `somas:reviewed`

### Idempotency

The workflow prevents duplicate processing by:
1. Checking for marker comment: `<!-- SOMAS_RECOMMENDATIONS_CAPTURED:XX -->`
2. Skipping processing if marker exists
3. Adding marker after successful processing

### Permissions Required

- `contents: write` - To commit backlog/roadmap updates
- `issues: write` - To create follow-up issues  
- `pull-requests: read` - To read PR comments

---

## Best Practices

### For Reviewers

1. **Use structured format** - Include `## Recommendations` header with priority sections
2. **Be specific** - Each recommendation should be clear and actionable
3. **Provide context** - Explain why the recommendation matters
4. **Categorize appropriately** - Use correct priority level
5. **Link to examples** - Reference similar patterns or previous PRs

### For PR Authors

1. **Request reviews** - Add `somas:reviewed` label to trigger meta-capture
2. **Respond to recommendations** - Comment on whether you agree with categorization
3. **Track follow-ups** - Monitor created issues and roadmap updates

### For Maintainers

1. **Review captured items** - Periodically review backlog and roadmap
2. **Promote items** - Convert backlog items to issues when ready to work
3. **Archive obsolete items** - Clean up superseded or outdated recommendations
4. **Update ADRs** - Keep architecture decisions current

---

## Integration with SOMAS Pipeline

### Issue Creation Flow

When a follow-up issue is created:

1. Issue gets `somas:follow-up` and `somas:change` labels
2. SOMAS triage agent can pick it up automatically
3. Routes to appropriate stage (planning/architecture/implementation)
4. Executes through standard SOMAS pipeline

### Backlog Management

Items in backlog can be promoted:

```bash
# Create issue from backlog item
gh issue create \
  --title "[ENHANCE] <item-title>" \
  --label "somas:enhance" \
  --body "From backlog: <item-description>"
```

### Roadmap Planning

Roadmap items inform:
- Release planning discussions
- Feature prioritization
- Resource allocation
- Strategic direction

---

## Examples

### Example 1: Circuit Breaker State Persistence (PR #28)

**Review Comment:**
```markdown
## Recommendations

### Must Address Soon
- Add circuit breaker state persistence to avoid thundering herd on restart
- Document circuit breaker threshold decisions in ADR

### Future Enhancement
- Support distributed circuit breaker coordination across replicas
```

**Meta-Capture Output:**
- Issue #XX created: "[CHANGE] Add circuit breaker state persistence"
- ADR-002 template created: "Circuit Breaker Thresholds"
- Roadmap updated with distributed coordination item

### Example 2: JSON State Persistence (PR #26)

**Review Comment:**
```markdown
## Recommendations

### Must Address Soon
- Add schema validation for JSON state files
- Implement state migration strategy for schema changes

### Should Consider
- Add compression for large state files
- Consider alternative storage backends (Redis, SQLite)

### Future Enhancement
- State snapshotting for point-in-time recovery
- State replication for high availability
```

**Meta-Capture Output:**
- 2 Issues created for schema validation and migration
- 2 Backlog items for compression and alternative backends
- 2 Roadmap items for snapshotting and replication

---

## Troubleshooting

### Recommendations Not Captured

**Check:**
1. Does PR have `somas:approved` or `somas:reviewed` label?
2. Was PR actually merged (not just closed)?
3. Is `## Recommendations` header present in comments?
4. Are priority sections formatted correctly (`### Must Address Soon`, etc.)?

**Solution:** Add label and re-trigger workflow, or manually process recommendations

### Duplicate Processing

**Check:**
1. Look for marker comment: `<!-- SOMAS_RECOMMENDATIONS_CAPTURED:XX -->`

**Solution:** Workflow should prevent duplicates automatically; if duplicates occur, check workflow logs

### Issues Not Created

**Check:**
1. Workflow logs in Actions tab
2. API rate limits or permissions

**Solution:** Review workflow execution logs and verify GitHub token permissions

---

## Related Documentation

- `.somas/templates/meta-capture.md` - Template for manual capture
- `.somas/architecture/ADRs/README.md` - ADR guidelines and template
- `.somas/backlog.md` - Backlog tracking file
- `.somas/roadmap.md` - Roadmap planning file
- `docs/somas/COPILOT_GUIDE.md` - Copilot integration guide
- `.github/workflows/somas-meta-capture.yml` - Automation workflow

---

## Future Improvements

Potential enhancements to the meta-capture process:

- AI-powered categorization of recommendations
- Natural language parsing for unstructured recommendations
- Integration with project management tools
- Automated ADR generation from architectural recommendations
- Metrics dashboard for recommendation tracking
- Recommendation impact analysis

---

**Note:** This meta-process ensures that valuable insights from PR reviews are preserved, routed appropriately, and made actionable, improving SOMAS project memory and strategic evolution.
