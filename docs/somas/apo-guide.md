# APO (Autonomous Prompt Optimization) Guide

## Table of Contents

1. [Introduction](#introduction)
2. [What is APO?](#what-is-apo)
3. [Mental Models Library](#mental-models-library)
4. [Task Analysis](#task-analysis)
5. [Chain Strategies](#chain-strategies)
6. [Integration with SOMAS](#integration-with-somas)
7. [Usage Examples](#usage-examples)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Introduction

APO (Autonomous Prompt Optimization) is a cognitive enhancement layer that sits on top of all SOMAS agents. It enables agents to:

- **Self-select** optimal mental models for any task
- **Reason explicitly** using structured cognitive frameworks
- **Verify quality** through systematic checks
- **Iterate** until output meets standards
- **Chain strategies** for complex multi-faceted problems

APO transforms agents from simple instruction-followers into sophisticated reasoners that think deeply about problems before responding.

### Why APO?

Without APO, agents often:
- Rush to solutions without deep thinking
- Apply pattern matching instead of reasoning
- Miss important edge cases or risks
- Produce inconsistent quality outputs
- Lack explicit reasoning trails

With APO, agents:
- Analyze tasks before acting
- Apply appropriate reasoning frameworks
- Think through multiple perspectives
- Verify outputs systematically
- Document reasoning for transparency

---

## What is APO?

APO is a **meta-cognitive framework** that provides:

### 1. Mental Models Library

A collection of 7 cognitive frameworks that agents can apply:

| Model | Category | When to Use |
|-------|----------|-------------|
| **First Principles** | Analytical | Novel problems, deep understanding needed |
| **Inversion (Pre-Mortem)** | Risk Analysis | Failure prevention, risk assessment |
| **Second-Order Thinking** | Strategic | Long-term consequences, strategic decisions |
| **OODA Loop** | Execution | Iterative tasks, rapid adaptation |
| **Occam's Razor** | Simplification | Choosing between solutions, avoiding complexity |
| **Six Thinking Hats** | Comprehensive | Balanced analysis, validation |
| **Tree of Thoughts** | Exploration | Complex problems, multiple solution paths |

### 2. Task Analyzer

Automatic classification system that:
- Detects task domain (technical, creative, strategic, analytical, risk)
- Assesses complexity (simple, moderate, complex, novel)
- Selects optimal mental model(s)
- Determines chain strategy

### 3. Base Prompt

Universal cognitive scaffolding that:
- Activates reasoning mode
- Provides verification checklist
- Enforces quality loops
- Prevents early answering

### 4. Chain Strategies

Methods for combining mental models:
- **Sequential**: Apply models one after another
- **Collision**: Force insights from contradictory perspectives
- **Draft-Critique-Refine**: Generate, analyze, improve
- **Parallel-Synthesis**: Apply multiple models, synthesize insights

---

## Mental Models Library

### First Principles Thinking

**Description**: Break down complex problems to fundamental truths, then reason up from axioms.

**Process**:
1. Identify current assumptions
2. Break down to fundamental truths
3. Question each assumption
4. Reconstruct from axioms
5. Generate new approaches

**When to Use**:
- Novel problems without precedent
- Need deep understanding
- Conventional approaches seem inadequate
- Architecture decisions
- Innovation required

**Example**:
```
Problem: Design authentication system

❌ Pattern Matching: "Everyone uses JWT, so we'll use JWT"

✅ First Principles:
- Fundamental truth: User must prove identity
- Fundamental truth: System must trust that proof
- Question: Why JWT? Why not certificates? Why not passwordless?
- Reconstruct: From identity proof requirement, evaluate ALL approaches
- Result: Select best approach for THIS context, not just "standard"
```

### Inversion (Pre-Mortem)

**Description**: Think backwards. Ask "How would this fail?" instead of "How do we succeed?"

**Process**:
1. Assume complete failure
2. Enumerate failure modes
3. Identify root causes
4. Assess probability and impact
5. Design preventions

**When to Use**:
- Risk assessment
- Security analysis
- Quality assurance
- Validation
- Specification review

**Example**:
```
Feature: User data export

❌ Optimistic: "Users can export their data. Done!"

✅ Inversion:
- Assume failure: "6 months from now, massive data breach from exports"
- Failure modes:
  * No authentication on export endpoint
  * Exports include other users' data
  * Exports stored unencrypted
  * No rate limiting (DoS)
- Preventions:
  * Add JWT auth
  * Strict user ID filtering
  * Encrypt exports at rest
  * Rate limit exports
```

### Second-Order Thinking

**Description**: Consider consequences of consequences. Ask "And then what?" at T+6mo and T+1yr.

**Process**:
1. Identify first-order effects
2. Project T+6mo effects
3. Project T+1yr effects
4. Consider compounding effects
5. Evaluate strategic fit

**When to Use**:
- Strategic decisions
- Technology selection
- API design
- Architecture choices
- Long-term planning

**Example**:
```
Decision: Adopt microservices architecture

❌ First-Order Only:
- Better separation of concerns ✓
- Independent deployment ✓

✅ Second-Order (T+6mo):
- Team splits into service teams
- Inter-team communication overhead increases
- Deployment complexity grows
- Debugging becomes harder

Second-Order (T+1yr):
- Need service mesh for observability
- Need DevOps specialists
- Different teams at different velocities
- Organizational changes required

Strategic Question: Are we prepared for second-order effects?
```

### OODA Loop

**Description**: Observe → Orient → Decide → Act → Loop. Rapid iteration for dynamic situations.

**Process**:
1. **Observe**: Gather current data
2. **Orient**: Analyze in context
3. **Decide**: Choose action
4. **Act**: Execute
5. **Loop**: Return to Observe

**When to Use**:
- Implementation tasks
- Debugging
- Optimization
- Iterative development
- Changing requirements

**Example**:
```
Task: Optimize slow database query

OBSERVE: Query takes 5s. Query plan shows full table scan on 1M rows.

ORIENT: No index on filter column. Filtering on 'created_at' frequently.

DECIDE: Add index on 'created_at' column.

ACT: CREATE INDEX idx_created_at ON table(created_at);

LOOP → OBSERVE: Query now 50ms. Success! ✓
Find next bottleneck. Repeat cycle.
```

### Occam's Razor

**Description**: Among competing solutions, prefer the simplest valid one.

**Process**:
1. List all viable solutions
2. Identify core requirements
3. Measure complexity
4. Eliminate unnecessary elements
5. Choose simplest valid solution

**When to Use**:
- Architecture decisions
- Implementation approach selection
- API design
- Debugging
- Refactoring

**Example**:
```
Problem: Store user preferences

❌ Complex Solution:
- NoSQL document store
- Caching layer
- Async update queue
- Event sourcing
- Versioning system

Core Requirements:
- Store key-value pairs per user
- Retrieve quickly
- Update occasionally

✅ Simple Solution (Occam's Razor):
- JSON column in existing user table
- Standard DB query (already fast)

Start simple. Add complexity only when requirements demand it.
```

### Six Thinking Hats

**Description**: Examine from six perspectives: Facts, Intuition, Caution, Benefits, Creativity, Process.

**Process**:
1. **White Hat** (Facts): What data exists?
2. **Red Hat** (Intuition): Gut feelings?
3. **Black Hat** (Caution): What could go wrong?
4. **Yellow Hat** (Benefits): What's the upside?
5. **Green Hat** (Creativity): Alternative approaches?
6. **Blue Hat** (Process): What comes next?

**When to Use**:
- Validation
- Complex decisions
- Requirement review
- Architecture review
- Comprehensive analysis

**Example**:
```
Decision: Adopt GraphQL for API

WHITE (Facts): 47 REST endpoints. Avg 6 calls per page. Team has no GraphQL exp.

RED (Intuition): Feels like it would simplify frontend. Worried about learning curve.

BLACK (Caution): Team inexperience, less mature ecosystem, harder debugging.

YELLOW (Benefits): Reduces over-fetching, self-documenting, better DX.

GREEN (Creativity): Could use GraphQL only for complex queries, REST for CRUD.

BLUE (Process): 1 week research, 2 week POC, then decide.
```

### Tree of Thoughts

**Description**: Generate multiple reasoning branches, evaluate, select best, recurse.

**Process**:
1. Generate branches (3-5 approaches)
2. Evaluate each branch
3. Select promising paths
4. Recurse on selected
5. Synthesize final solution

**When to Use**:
- Complex problem-solving
- Planning and simulation
- Algorithm design
- Architecture exploration
- Novel problems

**Example**:
```
Problem: Optimize task execution order

BRANCH 1: Dependency-based topological sort
  Sub-branch 1a: Kahn's algorithm
  Sub-branch 1b: DFS topological sort
  Evaluation: Valid order, but ignores duration

BRANCH 2: Critical path method
  Sub-branch 2a: Forward/backward pass
  Sub-branch 2b: Monte Carlo simulation ✓
  Evaluation: Optimizes duration, handles uncertainty

BRANCH 3: Constraint satisfaction
  Sub-branch 3a: Backtracking
  Sub-branch 3b: Simulated annealing
  Evaluation: Flexible but slow

SYNTHESIS: Branch 2b (Monte Carlo) best aligns with SOMAS requirements.
Handles uncertainty, optimizes duration, respects dependencies.
```

---

## Task Analysis

The Task Analyzer automatically classifies tasks and recommends mental models.

### Domain Detection

Tasks are classified into domains:

| Domain | Keywords | Recommended Models |
|--------|----------|-------------------|
| **Technical** | implement, code, debug, optimize | OODA, Occam's, First Principles |
| **Creative** | design, architecture, innovate | Tree of Thoughts, First Principles |
| **Strategic** | plan, roadmap, evaluate, decide | Second-Order, Six Hats, Tree of Thoughts |
| **Analytical** | analyze, review, validate, test | Inversion, Six Hats, Occam's |
| **Risk Assessment** | risk, security, vulnerability | Inversion, Second-Order, Six Hats |

### Complexity Assessment

Five factors contribute to complexity:

1. **Scope Size**: Lines of code, number of components
2. **Dependencies**: Internal and external dependencies
3. **Novelty**: Familiarity with problem type
4. **Ambiguity**: Clarity of requirements
5. **Risk**: Impact of errors

Complexity levels:
- **Simple**: 1-file change, clear requirements, low risk
- **Moderate**: Multi-file, some dependencies, moderate risk
- **Complex**: Multi-component, external deps, high risk
- **Novel**: Never done before, requires research

### Automatic Model Selection

The analyzer uses a scoring algorithm:

1. **Domain Match** (weight: 3.0): Does model fit domain?
2. **Complexity Match** (weight: 2.0): Right model for complexity?
3. **Risk Match** (weight: 2.5): Does model address risk level?
4. **Ambiguity Match** (weight: 2.0): Does model handle uncertainty?

Example:
```yaml
Task: "Implement user authentication API endpoint"

Analysis:
  domain: technical
  complexity: moderate
  risk: high (security implications)

Model Selection:
  primary: ooda_loop (technical + iterative)
  secondary: inversion (high risk requires failure analysis)
  
Chain: sequential (implement, then security review)
```

---

## Chain Strategies

When multiple mental models are needed, chain strategies combine them effectively.

### Sequential Chain

**Pattern**: Model1 → Model2 → Model3

**When**: Building on previous insights, progressive elaboration

**Example**:
```
Task: Design and implement caching strategy

Step 1: First Principles
- Understand fundamental caching requirements
- Identify core axioms

Step 2: Occam's Razor (building on step 1)
- Among solutions from step 1, choose simplest
- Eliminate unnecessary complexity

Result: Deep understanding (first principles) + simple solution (Occam's)
```

### Collision Chain

**Pattern**: Model1 ⟷ Model2 → Resolve Tension

**When**: Need innovation, breaking assumptions, synthesis from opposites

**Example**:
```
Task: Write security requirements

Model A: Inversion (pessimistic)
- List all failure modes
- Maximum security measures

Model B: Second-Order Thinking (long-term)
- Consider usability consequences
- Think about operational overhead

Collision: Extreme security vs. long-term practicality

Synthesis: Layered security with progressive disclosure
- Good default security
- Additional verification for high-value actions
- Balances both concerns
```

See: `.somas/apo/chains/collision.yml` for full protocol

### Strategic Diamond Chain

**Pattern**: Diverge → Explore → Converge → Commit

**When**: Multiple options exist, need exploration before decision

**Phases**:
1. **Diverge**: Generate many options (8-12)
2. **Explore**: Develop top 5-7 options
3. **Converge**: Systematically select best
4. **Commit**: Create implementation plan

**Example**:
```
Task: Select state management approach

Diverge: Redux, Context, Zustand, Jotai, MobX, Recoil, Props, URL-based

Explore: Develop top 5 with Six Hats analysis

Converge: Score against criteria, apply Occam's Razor, check second-order

Commit: Detailed design + implementation plan for winner
```

See: `.somas/apo/chains/strategic-diamond.yml` for full protocol

---

## Integration with SOMAS

### Agent-Model Mappings

Each SOMAS pipeline stage has recommended mental models:

| Stage | Primary Models | Secondary | Chain |
|-------|---------------|-----------|-------|
| **Specification** | Inversion, Second-Order | Six Hats | Collision |
| **Simulation** | Tree of Thoughts, OODA | First Principles | Sequential |
| **Architecture** | First Principles, Occam's | Second-Order | Strategic Diamond |
| **Implementation** | OODA, Occam's | First Principles | Sequential |
| **Validation** | Inversion, Six Hats | Second-Order | Collision |

### How Agents Use APO

1. **Agent receives task** from orchestrator
2. **Base prompt injected** (cognitive scaffolding)
3. **Task analyzer invoked** (automatic classification)
4. **Mental models loaded** from library
5. **Agent applies models** using recommended chain
6. **Verification performed** against quality criteria
7. **Output generated** with reasoning trail

### Configuration Files

```
.somas/apo/
├── mental-models.yml       # 7 mental model definitions
├── task-analyzer.yml       # Classification and selection
├── base-prompt.yml         # Universal cognitive scaffolding
└── chains/
    ├── collision.yml       # Collision protocol
    └── strategic-diamond.yml  # Diverge-converge pattern
```

### Enabling APO

APO is configured in `.somas/config.yml`:

```yaml
apo:
  enabled: true
  auto_model_selection: true
  require_reasoning_trail: true
  verification_required: true
  max_iterations: 3
```

---

## Usage Examples

### Example 1: Specification Stage

**Task**: Create specification for user authentication feature

**APO Process**:

```markdown
# TASK ANALYSIS
- Domain: analytical + risk_assessment
- Complexity: moderate
- Risk: high (security)
- Selected Models: inversion, second_order_thinking
- Chain Strategy: collision

# REASONING PROCESS

## Inversion Perspective
Assume authentication feature failed catastrophically.
Failure modes:
- Passwords stored in plaintext
- No session expiry
- CSRF vulnerabilities
- Brute force attacks possible
- Password reset vulnerable

Preventions:
- Hash passwords with bcrypt
- Session timeout: 30 minutes
- CSRF tokens required
- Rate limiting on login
- Secure password reset flow

## Second-Order Thinking Perspective
T+6mo: Auth system in production, handling 10K users
- Need password reset support
- Need session management
- Need audit logging

T+1yr: Growing to 100K users
- Performance of auth checks
- Scaling session storage
- Compliance requirements (GDPR, etc.)

Strategic considerations:
- OAuth integration in future?
- Multi-factor auth needed?
- Passwordless options?

## COLLISION & SYNTHESIS
Tension: Inversion wants maximum security now.
Second-order wants future flexibility.

Synthesis: Secure foundation with extensibility points
- Core: Secure bcrypt + sessions + rate limiting (inversion)
- Architecture: Abstract auth interface for future OAuth (second-order)
- Design: Plugin system for future MFA (second-order)

# SOLUTION
[Detailed specification incorporating both perspectives]

# VERIFICATION
✓ Addresses security failures (inversion)
✓ Considers long-term evolution (second-order)
✓ Concrete and actionable
✓ Confidence: high
```

### Example 2: Architecture Stage

**Task**: Design microservices architecture

**APO Process**:

```markdown
# TASK ANALYSIS
- Domain: creative
- Complexity: very_complex
- Risk: high
- Selected Models: first_principles, occams_razor
- Chain Strategy: strategic_diamond

# STRATEGIC DIAMOND

## DIVERGE (Generate 8 Options)
1. Monolith (single service)
2. Modular monolith (modules, single deployment)
3. Microservices (full decomposition)
4. Mini-services (3-5 larger services)
5. Serverless functions
6. Hybrid (monolith + separate services for specific needs)
7. Service-oriented architecture
8. Event-driven microservices

## EXPLORE (Develop Top 5)
[Detailed development of each with Six Hats]

## CONVERGE (Score & Select)
Scoring against criteria:
- Team size: 5 developers
- Domain complexity: moderate
- Deployment frequency: weekly
- Scalability needs: moderate

Winner: Modular Monolith

Rationale:
- First Principles: Core requirement is maintainability at this team size
- Occam's Razor: Simplest architecture that meets needs
- Second-Order: Can evolve to microservices if needed

## COMMIT (Implementation Plan)
[Detailed design for modular monolith]
```

### Example 3: Implementation Stage

**Task**: Implement caching layer

**APO Process**:

```markdown
# TASK ANALYSIS
- Domain: technical
- Complexity: moderate
- Risk: moderate
- Selected Models: ooda_loop, occams_razor
- Chain Strategy: sequential

# OODA LOOP ITERATION 1

OBSERVE: API response time 800ms, database queries taking 600ms

ORIENT: Multiple queries per request, no caching, queries are repeated

DECIDE: Implement in-memory cache for read queries

ACT: 
- Add Redis
- Cache GET requests
- TTL: 5 minutes

# OODA LOOP ITERATION 2

OBSERVE: Response time now 150ms for cached. Cache hit rate 70%.

ORIENT: Good improvement. 30% still slow (cache misses).

DECIDE: Warm cache on startup for common queries

ACT: Add cache warming script

# OCCAM'S RAZOR CHECK

Complex alternative: Multi-tier cache (memory + Redis + CDN)
Simple solution: Redis only with cache warming

Occam's: Redis is sufficient, meets requirements
No need for additional complexity unless hit rate drops below 60%

# VERIFICATION
✓ Response time improved 800ms → 150ms (cached)
✓ Simple solution (just Redis)
✓ Monitoring in place
✓ Confidence: high
```

---

## Best Practices

### Do's

1. **Always Analyze First**: Don't skip task analysis, even for "simple" tasks
2. **Document Reasoning**: Make your thought process explicit
3. **Follow Model Processes**: Each model has steps - follow them
4. **Verify Before Finalizing**: Run verification checklist
5. **Iterate When Needed**: Don't settle for first draft if verification fails
6. **Consider Multiple Perspectives**: Use collision chains for important decisions
7. **Keep It Simple**: Occam's Razor should influence most decisions
8. **Think Long-Term**: Second-order thinking for strategic choices
9. **Embrace Uncertainty**: Document assumptions and uncertainties
10. **Learn from Past**: Reference previous similar analyses

### Don'ts

1. **Don't Rush to Solutions**: Resist pattern matching without reasoning
2. **Don't Skip Verification**: Quality checks are mandatory
3. **Don't Mix Mental Models**: When applying a model, stay in that mode
4. **Don't Over-Complicate**: Not every task needs Tree of Thoughts
5. **Don't Ignore Failures**: Inversion is uncomfortable but valuable
6. **Don't Dismiss Intuition**: Red Hat (intuition) has value
7. **Don't Force Models**: If a model doesn't fit, use task analyzer
8. **Don't Exceed 3 Iterations**: If still failing, escalate to human
9. **Don't Hide Reasoning**: Always include reasoning trail
10. **Don't Forget Context**: Consider pipeline position and stage

### Model Selection Tips

**Use First Principles when**:
- Problem is novel or unprecedented
- Need deep understanding
- Conventional wisdom seems wrong
- Building fundamental architecture

**Use Inversion when**:
- Risk is high
- Security is critical
- Failure modes need identification
- Validation required

**Use Second-Order when**:
- Decision has long-term impact
- Technology selection
- API or interface design
- Strategic planning

**Use OODA Loop when**:
- Implementing or coding
- Debugging issues
- Optimizing performance
- Rapid iteration needed

**Use Occam's Razor when**:
- Multiple solutions available
- Simplicity matters
- Choosing between approaches
- Avoiding over-engineering

**Use Six Thinking Hats when**:
- Need comprehensive analysis
- Validation and review
- Balanced perspective required
- Complex decision-making

**Use Tree of Thoughts when**:
- Problem is complex
- Multiple solution paths exist
- Need exploration
- Planning or simulation

---

## Troubleshooting

### Problem: Model selection seems wrong

**Solution**: 
- Review task analysis
- Check domain classification
- Consider complexity assessment
- Override automatic selection if needed (document why)

### Problem: Collision chain produces weak synthesis

**Symptoms**: Feels like compromise, no breakthrough insight

**Solution**:
- Ensure both models fully developed
- Look for deeper tension
- Question more assumptions
- Try different model pair

### Problem: Verification keeps failing

**Symptoms**: Multiple iterations, still not passing

**Solution**:
- After 3 iterations, escalate to human
- May need different mental model
- Requirements may be unclear
- Problem may be more complex than assessed

### Problem: Taking too long

**Symptoms**: APO reasoning consuming excessive time

**Solution**:
- Check complexity assessment (may be over-thinking simple task)
- Use lighter models (OODA, Occam's) for simple tasks
- Set time budgets per complexity level
- Remember: simple tasks need simple reasoning

### Problem: Output lacks reasoning trail

**Symptoms**: Solution provided without showing work

**Solution**:
- Review base prompt requirements
- Ensure explicit model application
- Document each step
- Include verification section

### Problem: Chaining strategy unclear

**Symptoms**: Unsure how to combine models

**Solution**:
- Review chain strategy definitions
- Look at examples in chain YAML files
- Use collision for opposites
- Use sequential for building
- Use strategic diamond for decisions

---

## References

### Configuration Files

- Mental Models: `.somas/apo/mental-models.yml`
- Task Analyzer: `.somas/apo/task-analyzer.yml`
- Base Prompt: `.somas/apo/base-prompt.yml`
- Collision Chain: `.somas/apo/chains/collision.yml`
- Strategic Diamond: `.somas/apo/chains/strategic-diamond.yml`

### SOMAS Integration

- Main Config: `.somas/config.yml` (APO section)
- Agent Configs: `.somas/agents/*.yml`
- Stage Definitions: `.somas/stages/*.yml`

### Further Reading

- [SOMAS Documentation](README.md)
- [Copilot Guide](COPILOT_GUIDE.md)
- [Optimization Guide](optimization-guide.md)

---

## Feedback

APO is designed to evolve. As agents use these mental models:

- Success patterns are tracked
- Model effectiveness is measured
- Selection algorithm improves
- New models can be added

For questions or improvements to APO:
- Create an issue in the repository
- Tag @scotlaclair for APO-related discussions
- Contribute new mental models or chain strategies

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Maintained by**: SOMAS Core Team
