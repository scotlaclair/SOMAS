# SOMAS Development Plan (2026)

**Project:** Self-Sovereign Orchestrated Multi-Agent System (SOMAS)
**Status:** 75% Complete
**Last Updated:** January 31, 2026
**Author:** SOMAS Development Team

---

## Executive Summary

SOMAS is an autonomous AI-driven software development pipeline with a solid foundation (~75% complete). The core infrastructure is production-ready (state management, circuit breaker, orchestration), but critical integrations and agent implementations remain incomplete.

**Key Stats:**
- **Lines of Code:** ~3,260 lines of core Python
- **Configuration:** ~1,000+ lines in config.yml
- **Documentation:** 20+ comprehensive markdown files
- **Test Coverage:** 70% with 1,075 lines of tests
- **Agent Configurations:** 22 agents (65% well-defined)
- **Pipeline Stages:** All 11 stages fully defined with quality gates

---

## Current State Assessment

### ✅ FULLY IMPLEMENTED (95%+)

1. **Core Infrastructure**
   - State Manager (1,008 lines) - Complete with atomic writes, file locking, path validation
   - Circuit Breaker (167 lines) - Full protection against runaway automation
   - Pipeline Orchestration - All 11 stages defined with timeouts and quality gates
   - Configuration System - 1000+ line config.yml with comprehensive settings

2. **Testing Foundation**
   - Comprehensive state manager tests (767 lines)
   - Circuit breaker tests
   - Path validation and security tests

3. **Analytics & Monitoring**
   - Task complexity analyzer with 5-dimensional scoring
   - Cost tracking (API usage, token counts)
   - POC metrics collection
   - APO (Autonomous Prompt Optimization) configuration

4. **GitHub Workflows**
   - 15+ GitHub Action workflows
   - Main pipeline orchestration
   - Comment-driven triggers
   - Security scanning (CodeQL, Semgrep)
   - Meta-capture for review recommendations

5. **Documentation**
   - CLAUDE.md (comprehensive AI assistant guide)
   - Architecture decision records (ADRs)
   - Configuration reference
   - Getting started guide
   - Operations runbook

### ⚠️ PARTIALLY IMPLEMENTED (50-80%)

1. **Agent System**
   - **11 Complete Agents:** security, documenter, deployer, reviewer, validator, tester, analyzer, implementer, architect, copilot, simulator
   - **8 Minimal Agents:** triage (69 lines), planner (229 lines), decomposer (130 lines), merger (154 lines), orchestrator (169 lines), coder (229 lines), operator (190 lines), debugger (0 LINES - EMPTY)
   - **2 Critical Gaps:** advisor (9 lines), specifier (48 lines)

2. **Prompt Templates**
   - Defined: 5/22 agents have prompt templates
   - Coverage: architect, specifier, advisor, triage, implementer
   - Missing: 17 of 22 agent-specific prompts

3. **Feedback Loop System**
   - Structure: ✓ Complete
   - Algorithms: ✗ Missing (3 TODO items)
     - Cycle detection for task dependencies
     - Graph traversal for orphaned nodes
     - Estimate validation against benchmarks
     - File I/O operations (2 TODOs)

4. **Runner Framework**
   - Configuration loading: ✓ Complete
   - Path/security validation: ✓ Complete
   - Agent invocation: ✗ TODO (line 271)

### ❌ NOT IMPLEMENTED

1. **LLM Integration Layer**
   - No OpenAI/Claude/Gemini API integration code
   - No model endpoint configuration
   - No token counting implementation
   - No response streaming
   - No fallback model handling

2. **GitHub API Integration**
   - No PR creation code
   - No issue commenting
   - No label management
   - No branch operations
   - No artifact uploads

3. **Individual Agent Logic**
   - No per-agent Python modules
   - Only YAML configurations exist
   - No specialized reasoning engines

---

## Completion Roadmap

### PHASE 1: Critical Infrastructure (Weeks 1-2)

**Objective:** Fix critical blockers and complete empty/minimal agents

#### 1.1 Complete Agent Configurations
- [ ] **debugger.yml** - Create full 300+ line configuration (currently 0 lines)
  - Role: Test failure analysis and code repair
  - Responsibilities: Parse test failures, identify root causes, suggest fixes
  - Quality checks: Code syntax validation, test pass verification
  - Fallback models: Claude Sonnet 4.5, Grok Fast

- [ ] **advisor.yml** - Expand from 9 to 150+ lines
  - Role: Strategic guidance and feasibility analysis
  - Responsibilities: Risk assessment, complexity analysis, task prioritization
  - APO integration: Task complexity analysis for agent selection
  - Output format: JSON with risk scores and recommendations

- [ ] **specifier.yml** - Expand from 48 to 200+ lines
  - Role: Requirements specification generation
  - Responsibilities: PRD creation, requirement validation, ambiguity resolution
  - Quality gates: No TBD terms, all testable, security requirements defined
  - Error handling: Escalate conflicting requirements

#### 1.2 Implement Graph Algorithms in Feedback Loop
- [ ] Cycle detection algorithm (feedback_loop.py:250)
  - Detect circular dependencies in task graph
  - Prevent infinite feedback loops
  - Surface problematic dependencies

- [ ] Graph traversal for orphaned nodes (feedback_loop.py:265)
  - Find unreachable tasks
  - Identify disconnected components
  - Validate task connectivity

- [ ] Estimate validation (feedback_loop.py:280)
  - Validate duration estimates against historical data
  - Flag unrealistic estimates
  - Suggest revisions based on complexity

- [ ] File I/O operations (feedback_loop.py:299, 317)
  - Read current specification
  - Write revised specifications
  - Maintain audit trail

#### 1.3 Implement Agent Invocation in Runner
- [ ] Add actual LLM API calls (runner.py:271)
  - Load agent configuration
  - Prepare prompt and context
  - Call selected model
  - Handle responses and errors
  - Retry with fallback models

### PHASE 2: LLM & GitHub Integration (Weeks 3-4)

**Objective:** Connect SOMAS to external services (LLMs and GitHub)

#### 2.1 Create LLM Integration Layer
- [ ] Create `somas/llm/` module structure
  - `base.py` - Abstract LLM interface
  - `openai.py` - OpenAI API integration
  - `anthropic.py` - Claude API integration
  - `google.py` - Gemini API integration
  - `xai.py` - Grok API integration

- [ ] Implement token counting
  - Token budget per stage
  - Cost optimization
  - Fallback to smaller models when needed

- [ ] Implement response handling
  - Streaming responses for long outputs
  - Error handling and retries
  - Model-specific response parsing
  - JSON extraction for structured output

- [ ] Model endpoint configuration
  - Load from environment variables
  - Support multiple API keys
  - Rate limiting per endpoint
  - Fallback routing logic

#### 2.2 Create GitHub API Integration
- [ ] Create `somas/github/` module
  - `client.py` - GitHub API wrapper
  - `pr.py` - PR operations
  - `issue.py` - Issue operations
  - `labels.py` - Label management
  - `artifacts.py` - Artifact handling

- [ ] Implement PR operations
  - Create PR from feature branch
  - Update PR description
  - Add reviewers
  - Merge strategy (auto-merge on success)

- [ ] Implement issue operations
  - Add comments with agent decisions
  - Update issue state
  - Link related issues
  - Create sub-tasks

- [ ] Implement label management
  - Create labels per stage
  - Auto-label PRs
  - Track label lifecycle

### PHASE 3: Agent Completion (Weeks 5-6)

**Objective:** Create prompt templates and expand agent configurations

#### 3.1 Create Missing Prompt Templates
- [ ] Create templates for remaining 17 agents:
  - **Implement:** `planner`, `decomposer`, `tester`, `security`, `merger`, `validator`
  - **Verify:** Matching agent responsibility definitions
  - **Structure:** Follow existing template pattern (task, context, quality criteria)

#### 3.2 Create Per-Agent Python Modules
- [ ] Create `somas/agents/` Python implementations:
  - Base agent class with common patterns
  - Per-agent specialized logic modules
  - Shared utilities (prompt loading, response parsing)

#### 3.3 Expand Minimal Agent Configurations
- [ ] Bring all agents to 150+ line minimum
  - Add detailed responsibility descriptions
  - Define input/output formats
  - Specify quality checks
  - Add error handling

### PHASE 4: Testing & Validation (Weeks 7-8)

**Objective:** Comprehensive testing of all components

#### 4.1 Integration Tests
- [ ] Test runner with LLM integration
- [ ] Test GitHub API operations
- [ ] Test stage transitions with all agents
- [ ] Test circuit breaker limits

#### 4.2 End-to-End Tests
- [ ] Full pipeline execution simulation
- [ ] Multi-stage feedback loops
- [ ] Error recovery scenarios
- [ ] Performance benchmarks

#### 4.3 Agent-Specific Tests
- [ ] Test each agent's prompt template
- [ ] Validate output formats
- [ ] Test quality gate enforcement
- [ ] Test fallback behavior

### PHASE 5: Documentation & Operationalization (Weeks 9-10)

**Objective:** Complete documentation and operational guides

#### 5.1 Documentation
- [ ] Agent playbook for each agent type
- [ ] API integration guides
- [ ] Model selection strategy documentation
- [ ] Troubleshooting guides for common failures

#### 5.2 Monitoring & Observability
- [ ] Set up structured logging
- [ ] Metrics collection for all stages
- [ ] Dashboard configuration
- [ ] Alert thresholds and escalation

#### 5.3 Deployment Procedures
- [ ] Deployment checklist
- [ ] Rollout strategy
- [ ] Canary testing procedures
- [ ] Rollback procedures

---

## Priority Matrix

### CRITICAL (Blocks all progress)
1. **debugger.yml completion** - Empty agent blocks verify stage
2. **LLM integration** - No way to invoke agents without this
3. **GitHub integration** - Can't interact with issues/PRs
4. **Agent invocation in runner** - Framework needs actual execution

### HIGH (Blocks specific workflows)
1. **advisor.yml expansion** - Affects intake stage quality
2. **specifier.yml expansion** - Affects specification quality
3. **Feedback loop graph algorithms** - Affects planning optimization
4. **Prompt templates** - Affects agent output quality

### MEDIUM (Improves completeness)
1. **Integration tests** - Ensures components work together
2. **Agent Python modules** - Enables specialized logic
3. **E2E tests** - Validates full pipeline
4. **Monitoring setup** - Enables operational visibility

### LOW (Polish & optimization)
1. **Expanded minimal agents** - Nice-to-have details
2. **Documentation expansion** - Helpful but not blocking
3. **Performance optimization** - For future scale-up
4. **Advanced APO features** - For enhanced capability

---

## Implementation Sequence

**Recommended order for maximum efficiency:**

1. **Complete agent configs** (all 3) - Small, high-impact
2. **Implement agent invocation** - Enables testing
3. **Create LLM integration** - Required for execution
4. **Create GitHub integration** - Enables issue/PR management
5. **Implement graph algorithms** - Optimizes planning
6. **Create prompt templates** - Improves agent quality
7. **Add integration tests** - Validates everything works
8. **Documentation pass** - Makes it operationalizable

---

## Resource Requirements

### Development Effort
- **Phase 1 (Critical agents & algorithms):** 40 hours
- **Phase 2 (LLM & GitHub):** 60 hours
- **Phase 3 (Agents & templates):** 50 hours
- **Phase 4 (Testing):** 40 hours
- **Phase 5 (Documentation):** 30 hours

**Total:** ~220 hours (~5.5 weeks at 40 hrs/week)

### Dependencies
- OpenAI API key (for GPT models)
- Claude API key (for Claude models)
- Gemini API key (for Gemini models)
- Grok API key (for Grok models)
- GitHub token with repo admin permissions
- Python 3.11+
- Standard packages: filelock, pyyaml, requests, httpx (for async)

### Tools Required
- Python 3.11+
- Git
- GitHub CLI (gh)
- Docker (for agent sandboxing - future)

---

## Success Criteria

### Completion Milestones

- [ ] **M1 (Week 2):** All 3 incomplete agents complete, graph algorithms implemented
- [ ] **M2 (Week 4):** Full LLM and GitHub integration operational
- [ ] **M3 (Week 6):** All 22 agents have complete templates and Python modules
- [ ] **M4 (Week 8):** 90%+ test coverage with integration and E2E tests passing
- [ ] **M5 (Week 10):** Full documentation complete, monitoring operational

### Quality Gates

- [ ] All core tests passing (state manager, circuit breaker, runner)
- [ ] Integration tests covering all agent invocation paths
- [ ] E2E tests for complete 11-stage pipeline
- [ ] No critical security vulnerabilities (CodeQL, Semgrep passing)
- [ ] Code coverage > 80% for core modules
- [ ] All API contracts documented
- [ ] Operations runbook complete with SLO definitions

---

## Known Blockers & Constraints

### Technical Blockers
1. **No LLM integration code** - Blocks all agent execution
2. **Empty debugger.yml** - Blocks verify stage
3. **Missing graph algorithms** - Blocks plan optimization

### External Constraints
1. **API availability** - Depends on multiple LLM providers
2. **Rate limits** - Need to implement backoff strategy
3. **Token budgets** - Need cost optimization for large projects

### Architectural Decisions Pending
1. **Agent sandboxing** - Docker vs direct execution?
2. **Caching strategy** - How to cache LLM responses?
3. **Error recovery** - Auto-retry vs human escalation?
4. **Feedback loop depth** - How many iterations before escalation?

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| LLM API failures | Medium | High | Implement multi-provider fallbacks |
| Token budget exceeded | Low | Medium | Cost tracking and optimization |
| Feedback loops don't converge | Medium | High | Implement cycle detection and limits |
| GitHub API rate limits | Low | Medium | Implement caching and batching |
| Test coverage gaps | Medium | Medium | Comprehensive E2E test suite |
| Agent output parsing failures | High | Medium | Structured output format enforcement |

---

## Future Roadmap (Post-Completion)

### v0.2.0 (Next Release)
- [ ] Docker sandboxing for agent execution
- [ ] Advanced APO mental models library
- [ ] Multi-project orchestration
- [ ] Distributed execution support

### v0.3.0
- [ ] Custom agent plugin system
- [ ] Advanced caching and memoization
- [ ] Predictive pipeline optimization
- [ ] Human-in-the-loop refinement workflows

### v1.0.0
- [ ] Production-grade deployment
- [ ] SLA-based execution tuning
- [ ] Enterprise authentication (SAML/OAuth)
- [ ] Advanced analytics and learning

---

## Getting Started

### For Contributors

1. **Read** this plan and CLAUDE.md
2. **Choose** a task from the priority matrix
3. **Create** a feature branch: `git checkout -b claude/implement-[feature]-Xm1mg`
4. **Follow** the implementation sequence
5. **Test** thoroughly with both unit and integration tests
6. **Document** changes in PRs and update CLAUDE.md if needed
7. **Push** to branch and request review

### For Code Review

- Ensure all new code has tests
- Verify security patterns (path validation, input sanitization)
- Check that error handling is specific (not bare except)
- Validate atomic write operations for file modifications
- Confirm API contracts are documented

---

## Related Documents

- **CLAUDE.md** - AI assistant development guide
- **.somas/config.yml** - System configuration reference
- **docs/somas/operations-runbook.md** - Operational procedures
- **.somas/backlog.md** - Future work items
- **.somas/roadmap.md** - Strategic roadmap

---

## Version History

| Date | Version | Status | Changes |
|------|---------|--------|---------|
| 2026-01-31 | 1.0 | DRAFT | Initial comprehensive plan document |
| TBD | 1.1 | - | Updates as work progresses |

