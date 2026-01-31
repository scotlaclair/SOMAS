# SOMAS Architecture Diagrams

Visual documentation of the SOMAS autonomous pipeline architecture.

## Table of Contents

- [Pipeline Flow Diagram](#pipeline-flow-diagram)
- [Agent Invocation Sequence](#agent-invocation-sequence)
- [State Management](#state-management)
- [Component Relationships](#component-relationships)
- [APO Integration](#apo-integration)
- [Triage System Flow](#triage-system-flow)

---

## Pipeline Flow Diagram

### 11-Stage Aether Lifecycle Pipeline

```mermaid
flowchart TB
    subgraph Input
        ISSUE[GitHub Issue]
    end

    subgraph "Stage 1-4: Planning"
        INTAKE["1. INTAKE<br/>Intake<br/>🎯"]
        SPECIFY["2. SPECIFY<br/>Specify<br/>📐"]
        PLAN["3. PLAN<br/>Plan<br/>🗺️"]
        DECOMPOSE["4. DECOMPOSE<br/>Decompose<br/>📏"]
    end

    subgraph "Stage 5-7: Implementation"
        IMPLEMENT["5. IMPLEMENT<br/>Implement<br/>⚙️"]
        VERIFY["6. VERIFY<br/>Verify<br/>💓"]
        INTEGRATE["7. INTEGRATE<br/>Integrate<br/>🔗"]
    end

    subgraph "Stage 8-11: Delivery"
        HARDEN["8. HARDEN<br/>Harden<br/>🏋️"]
        RELEASE["9. RELEASE<br/>Release<br/>🚀"]
        OPERATE["10. OPERATE<br/>Operate<br/>🎵"]
        ANALYZE["11. ANALYZE<br/>Analyze<br/>🧠"]
    end

    subgraph Output
        PR[Pull Request]
    end

    ISSUE --> INTAKE
    SIGNAL --> DESIGN
    DESIGN --> GRID
    GRID --> LINE
    LINE --> MCP
    MCP --> PULSE
    PULSE --> SYNAPSE
    SYNAPSE --> OVERLOAD
    OVERLOAD --> VELOCITY
    VELOCITY --> PR
    PR -.-> VIBE
    VIBE --> WHOLE
    WHOLE -.-> |Learning Loop| SIGNAL

    %% Feedback loops
    GRID -.-> |Feedback| DESIGN
    PULSE -.-> |Retry| MCP
```

### Stage Details

| Stage | Agent | Model | Purpose |
|-------|-------|-------|---------|
| SIGNAL | Planner | GPT-5.2 | Catch initial request |
| DESIGN | Specifier | Claude Sonnet 4.5 | Expand requirements |
| GRID | Simulator | Claude Sonnet 4.5 | Monte Carlo optimization |
| LINE | Decomposer | Claude Sonnet 4.5 | Atomic task breakdown |
| MCP | Coder | Claude Sonnet 4.5 | Code generation |
| PULSE | Validator | Claude Sonnet 4.5 | Testing and validation |
| SYNAPSE | Merger | Claude Sonnet 4.5 | Integration |
| OVERLOAD | Tester | Claude Sonnet 4.5 | Hardening |
| VELOCITY | Deployer | Claude Opus 4.5 | Release preparation |
| VIBE | Operator | Gemini 3 Pro | SLO monitoring |
| WHOLE | Analyzer | Claude Opus 4.5 | Learning loop |

---

## Agent Invocation Sequence

> **Note**: The sequence diagrams below provide a simplified, high-level view of agent interaction patterns. For a comprehensive list of all 20 specialized agents and their stage assignments in the 11-stage Aether Lifecycle, see the [Complete Agent Reference](#complete-agent-reference) section below and [WORKFLOW_DIAGRAM.md](../../WORKFLOW_DIAGRAM.md#complete-workflow-pipeline).

### Standard Stage Execution

```mermaid
sequenceDiagram
    participant W as Workflow
    participant O as Orchestrator
    participant A as Agent
    participant S as State Manager
    participant G as GitHub

    W->>O: Trigger stage
    O->>S: Get current state
    S-->>O: State + checkpoint
    O->>A: Invoke agent
    A->>A: Execute task
    A->>G: Create artifacts
    A-->>O: Return results
    O->>S: Create checkpoint
    O->>S: Log transition
    O->>G: Update issue
    O-->>W: Stage complete
```

### Self-Healing Validation

```mermaid
sequenceDiagram
    participant O as Orchestrator
    participant V as Validator
    participant D as Debugger
    participant S as State Manager
    participant H as Human

    O->>V: Run validation
    V-->>O: Validation failed

    loop Max 3 retries
        O->>D: Invoke debugger
        D->>D: Analyze failure
        D->>D: Apply fixes
        D-->>O: Fixes applied
        O->>V: Re-run validation
        alt Validation passes
            V-->>O: Success
        else Validation fails
            V-->>O: Failed
        end
    end

    alt All retries exhausted
        O->>S: Record dead letter
        O->>H: Escalate to human
    end
```

### Agent Handoff

```mermaid
sequenceDiagram
    participant A1 as Stage N Agent
    participant S as State Manager
    participant O as Orchestrator
    participant A2 as Stage N+1 Agent

    A1->>A1: Complete work
    A1->>S: Save artifacts
    A1-->>O: Stage complete
    O->>S: Create checkpoint
    O->>S: Log transition
    O->>A2: Invoke next agent
    A2->>S: Load previous artifacts
    A2->>A2: Begin work
```

### Complete Agent Reference

The 11-stage Aether Lifecycle pipeline utilizes 20 specialized agents across different stages:

| Stage | Agents | Role |
|-------|--------|------|
| **1. INTAKE** | Triage, Advisor | Issue classification and strategic guidance |
| **2. SPECIFY** | Specifier | Requirements specification (PRD) |
| **3. PLAN** | Simulator, Architect, Planner | Monte Carlo optimization, system design, task planning |
| **4. DECOMPOSE** | Decomposer | Atomic task breakdown |
| **5. IMPLEMENT** | Implementer, Copilot | Code generation and assistance |
| **6. VERIFY** | Tester, Debugger | Testing and self-healing fixes |
| **7. INTEGRATE** | Merger, Validator | Code integration and validation |
| **8. HARDEN** | Security | Security scanning and audits |
| **9. RELEASE** | Deployer | Deployment artifacts and release management |
| **10. OPERATE** | Operator | SLO monitoring and operational health |
| **11. ANALYZE** | Analyzer, Documenter | Metrics analysis and documentation |

**Additional Supporting Agents:**
- **Orchestrator**: Runtime engine managing state transitions
- **Requirements**: Extracts and manages functional requirements (used with Specifier)
- **Reviewer**: Static analysis and code reviews (quality gate)

> **Total**: 20 specialized autonomous agents working across the 11-stage pipeline.

For detailed stage-by-stage breakdown with timing estimates and artifacts, see [WORKFLOW_DIAGRAM.md](../../WORKFLOW_DIAGRAM.md#complete-workflow-pipeline).

---

## State Management

### State File Structure

```mermaid
classDiagram
    class StateJson {
        +String project_id
        +String current_stage
        +String status
        +Checkpoint[] checkpoints
        +Metrics metrics
        +RecoveryInfo recovery_info
        +Labels labels
    }

    class Checkpoint {
        +String id
        +String stage
        +DateTime timestamp
        +Object data
        +String status
    }

    class Metrics {
        +Int total_duration_seconds
        +Int agent_invocations
        +Int dead_letters
        +Float success_rate
    }

    class RecoveryInfo {
        +String last_successful_checkpoint
        +Boolean can_resume
        +Int retry_count
    }

    class DeadLetter {
        +String id
        +String checkpoint_id
        +String error
        +Object context
        +DateTime timestamp
    }

    class Transition {
        +String from_stage
        +String to_stage
        +DateTime timestamp
        +String reason
        +String agent
    }

    StateJson "1" --> "*" Checkpoint
    StateJson "1" --> "1" Metrics
    StateJson "1" --> "1" RecoveryInfo
```

### Checkpoint Flow

```mermaid
flowchart LR
    subgraph "State Persistence"
        STATE[(state.json)]
        DEAD[(dead_letters.json)]
        TRANS[(transitions.jsonl)]
    end

    subgraph "Operations"
        CREATE[Create Checkpoint]
        UPDATE[Update Checkpoint]
        RECOVER[Recover]
        LOG[Log Transition]
    end

    CREATE --> STATE
    UPDATE --> STATE
    LOG --> TRANS
    RECOVER --> STATE
    RECOVER --> DEAD
```

### File Locking

```mermaid
sequenceDiagram
    participant P1 as Process 1
    participant L as FileLock
    participant F as state.json
    participant P2 as Process 2

    P1->>L: Acquire lock
    L-->>P1: Lock acquired
    P1->>F: Read state
    F-->>P1: State data
    P2->>L: Acquire lock
    Note over P2,L: Blocked - waiting
    P1->>F: Write state
    P1->>L: Release lock
    L-->>P2: Lock acquired
    P2->>F: Read state
```

---

## Component Relationships

### Module Dependencies

```mermaid
graph TB
    subgraph "somas/"
        INIT[__init__.py]

        subgraph "core/"
            SM[state_manager.py]
            RN[runner.py]
            FL[feedback_loop.py]
            CB[circuit_breaker.py]
        end

        subgraph "agents/"
            CT[cost_tracker.py]
        end

        subgraph "analytics/"
            PM[poc_metrics.py]
        end

        subgraph "apo/"
            APO[APO Module]
        end
    end

    RN --> SM
    RN --> FL
    RN --> CB
    FL --> SM
    RN --> CT
    RN --> PM
    RN --> APO

    SM --> |filelock| EXT[External: filelock]
    SM --> |yaml| YAML[External: pyyaml]
```

### Configuration Hierarchy

```mermaid
graph TB
    CONFIG[.somas/config.yml]

    subgraph "Agent Configs"
        AG1[planner.yml]
        AG2[specifier.yml]
        AG3[simulator.yml]
        AGN[...24 agents]
    end

    subgraph "Stage Configs"
        ST1[specification.yml]
        ST2[simulation.yml]
        STN[...stages]
    end

    subgraph "APO Configs"
        MM[mental-models.yml]
        TA[task-analyzer.yml]
        CH[chains/]
    end

    CONFIG --> AG1
    CONFIG --> AG2
    CONFIG --> AG3
    CONFIG --> AGN
    CONFIG --> ST1
    CONFIG --> ST2
    CONFIG --> STN
    CONFIG --> MM
    CONFIG --> TA
    CONFIG --> CH
```

---

## APO Integration

### Task Analysis Flow

```mermaid
flowchart TB
    TASK[Task Received] --> ANALYZE[Task Analyzer]

    ANALYZE --> SCORE[Complexity Score]

    SCORE --> |< 2.0| SIMPLE[Simple Task]
    SCORE --> |2.0 - 3.5| MODERATE[Moderate Task]
    SCORE --> |3.5 - 5.0| COMPLEX[Complex Task]
    SCORE --> |> 5.0| NOVEL[Novel Task]

    SIMPLE --> FAST[Grok Code Fast]
    MODERATE --> SONNET[Claude Sonnet 4.5]
    COMPLEX --> OPUS[Claude Opus 4.5]
    NOVEL --> OPUS

    subgraph "Chain Selection"
        SIMPLE --> SEQ[Sequential]
        MODERATE --> SEQ
        COMPLEX --> DCR[Draft-Critique-Refine]
        NOVEL --> SD[Strategic Diamond]
    end
```

### Mental Model Selection

```mermaid
flowchart LR
    subgraph "Mental Models"
        FP[First Principles]
        INV[Inversion]
        SOT[Second-Order Thinking]
        OODA[OODA Loop]
        OR[Occam's Razor]
        STH[Six Thinking Hats]
        TOT[Tree of Thoughts]
    end

    subgraph "Agent Preferences"
        ARCH[Architect] --> FP
        ARCH --> OR
        SPEC[Specifier] --> INV
        SPEC --> SOT
        SIM[Simulator] --> TOT
        SIM --> OODA
        VAL[Validator] --> INV
        VAL --> STH
    end
```

### Quality Loop

```mermaid
flowchart TB
    START[Agent Output] --> CHECK{Quality Check}

    CHECK --> |Pass| DONE[Complete]
    CHECK --> |Fail| ITER{Iteration < 3?}

    ITER --> |Yes| REFINE[Refine Output]
    REFINE --> CHECK

    ITER --> |No| ESCALATE[Escalate to Human]
```

---

## Triage System Flow

### Request Classification

```mermaid
flowchart TB
    ISSUE[New Issue] --> TRIAGE[Triage Agent]

    TRIAGE --> CLASS{Classify}

    CLASS --> |Change| CHANGE[Change Request]
    CLASS --> |Enhancement| ENHANCE[Enhancement]
    CLASS --> |Question| QUESTION[Question]
    CLASS --> |Bug| BUG[Bug Report]

    CHANGE --> CONF{Confidence?}
    ENHANCE --> CONF
    QUESTION --> CONF
    BUG --> CONF

    CONF --> |>0.9| AUTO[Auto-Route]
    CONF --> |0.8-0.9| LOG[Route + Log]
    CONF --> |<0.8| HUMAN[Escalate to Human]

    AUTO --> ROUTE{Route To}
    LOG --> ROUTE

    ROUTE --> |Requirements| PLANNER[Planner Agent]
    ROUTE --> |Architecture| ARCHITECT[Architect Agent]
    ROUTE --> |Implementation| IMPLEMENTER[Implementer Agent]
    ROUTE --> |Question| ADVISOR[Advisor Agent]
    ROUTE --> |Backlog| BACKLOG[(Backlog)]
```

### Routing Decision Tree

```mermaid
flowchart TB
    INPUT[Triage Input] --> REQ{Adds Requirements?}

    REQ --> |Yes| PLANNER[Route to Planner]
    REQ --> |No| SCOPE{Changes Scope >10%?}

    SCOPE --> |Yes| PLANNER
    SCOPE --> |No| ARCH{Changes Architecture?}

    ARCH --> |Yes| ARCHITECT[Route to Architect]
    ARCH --> |No| BUG{Bug Fix?}

    BUG --> |Yes| IMPL[Route to Implementer]
    BUG --> |No| QUEST{Question?}

    QUEST --> |Yes| ADVISOR[Route to Advisor]
    QUEST --> |No| BACKLOG[Defer to Backlog]
```

---

## Rendering Diagrams

These diagrams use [Mermaid](https://mermaid.js.org/) syntax and can be rendered:

1. **GitHub**: Automatically renders in markdown files
2. **VS Code**: Use Mermaid preview extension
3. **CLI**: Use `mmdc` (Mermaid CLI)
   ```bash
   npx @mermaid-js/mermaid-cli mmdc -i architecture-diagrams.md -o diagrams/
   ```

---

## See Also

- [Developer Guide](developer-guide.md) - Technical details
- [Configuration Reference](configuration-reference.md) - All settings
- [README](README.md) - System overview
