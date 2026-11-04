# Specification: financial-closing-advisor-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [x] Read `product-requirements-document.md` and `intent.md` from the solution root for full context
- [x] Bootstrap agent code in `assets/financial-closing-advisor-agent/` using instructions from the `sap-agent-bootstrap` section (invoke from inside `assets/financial-closing-advisor-agent/`, use copy commands — do NOT create files manually)
- [x] Install dependencies, validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

The agent requires runtime skills for two complex, domain-specific workflow domains:

- [x] Create `assets/financial-closing-advisor-agent/app/skills/closing-task-analysis/SKILL.md`:
  - YAML frontmatter: `name: closing-task-analysis`, `description: Step-by-step instructions for analyzing AFC closing task statuses, resolving dependency chains, and identifying blockers`
  - Body: Instructions for how to retrieve, classify, and evaluate closing tasks; dependency resolution logic; blocker root-cause reasoning steps; corrective action recommendation patterns
  - Companion file: `references/task-status-classification.md` — status classification rules (completed/in-progress/blocked/pending) and escalation priority logic

- [x] Create `assets/financial-closing-advisor-agent/app/skills/escalation-advisor/SKILL.md`:
  - YAML frontmatter: `name: escalation-advisor`, `description: Instructions for evaluating deadline proximity, triggering escalation recommendations, and identifying task owners`
  - Body: Escalation threshold evaluation logic, deadline proximity alert rules, task owner resolution steps, escalation recommendation format
  - Companion file: `references/escalation-thresholds.md` — configurable escalation rules and deadline proximity alert definitions

---

## Data Dependencies

No data product ORD IDs. API integration via MCP servers created from REST specs.

**API Specs:**
- `specification/financial-closing-advisor-agent/api-specs/afc-scheduling-spi.json` — ORD ID: `sap.afc:apiResource:SSPIV1:v1`
- `specification/financial-closing-advisor-agent/api-specs/afc-task-provider-v2.json` — ORD ID: `sap.afc:apiResource:TaskProviderV2:v1`

---

## Project-Specific Tasks

### Task Retrieval & Status Classification (R1)

- [x] Implement tool `get_closing_tasks`: calls AFC Task Provider V2 `/tasks` endpoint with `modifiedAfter` set to beginning of current closing period; returns all tasks classified by status (READY→pending, RESERVED/IN_PROGRESS→in-progress, COMPLETED→completed, CANCELED/INACTIVE→blocked or cancelled)
- [x] Implement tool `get_task_details`: calls AFC Task Provider V2 `/tasks/{taskUrn}` to retrieve full task details including priority, due date, assignee, and custom attributes
- [x] Implement tool `get_task_definitions`: calls AFC Task Provider V2 `/taskDefinitions` to retrieve all available task types and their definitions
- [x] Implement tool `get_job_definitions`: calls AFC Scheduling SPI `/JobDefinition` to retrieve closing job definitions (task catalog)
- [x] Implement tool `get_job_status`: calls AFC Scheduling SPI `/Job/{ID}` to retrieve current job execution status
- [x] Implement tool `get_job_results`: calls AFC Scheduling SPI `/Job/{ID}/results` and `/JobResult/{ID}/messages` to retrieve job execution results and error messages
- [x] In `app/agent.py` system prompt: instruct the agent to classify tasks into four buckets — completed, in-progress, blocked (status CANCELED/INACTIVE or job with failed/completedWithError status), pending (READY with no start yet) — and always present a summary count before details

### Dependency Chain Evaluation (R2)

- [x] In `app/agent.py` system prompt: instruct the agent to load the `closing-task-analysis` skill when the user asks about task dependencies, blockers, or sequencing
- [x] System prompt instruction: "When evaluating the dependency chain, retrieve all task definitions first to understand task types and their standard sequence, then cross-reference with current task statuses to identify which pending/blocked tasks are waiting for an upstream in-progress or blocked task to complete. Present the dependency chain as an ordered sequence with the current bottleneck highlighted."
- [x] System prompt instruction: "When calling tools that support pagination, always set `$top` to a maximum of 100 items. Inform the user when this limit is applied."

### Next-Action Recommendations (R3)

- [x] In `app/agent.py` system prompt: instruct the agent to produce a prioritized, sequenced next-action list. Ranking logic: (1) tasks with VERY_HIGH or HIGH priority that are in-progress or pending with imminent due dates; (2) tasks blocking the most downstream tasks; (3) tasks assigned to the controller themselves
- [x] System prompt: "For each recommendation, include: task name, current status, reason for prioritization, suggested action (e.g. 'Review and complete', 'Investigate blocker', 'Reassign to available owner'), and estimated impact on the closing timeline."
- [x] System prompt: "IMPORTANT: You MUST use tools to retrieve live data. Never fabricate, guess, or invent task statuses or dependencies. Relay tool errors verbatim."

### Root Cause Analysis for Blocked Tasks (R4)

- [x] In `app/agent.py` system prompt: instruct the agent to load the `closing-task-analysis` skill when the user asks why a task is blocked
- [x] Implement tool `get_job_error_messages`: calls `/JobResult/{ID}/messages` filtering by `severity: error` to retrieve specific error messages for failed jobs
- [x] System prompt: "When a task is blocked, retrieve its job result messages to identify the root cause category: (A) Data error — missing or invalid input data; (B) System error — technical failure in execution; (C) Dependency error — required upstream task not yet completed; (D) Access error — user permissions or authorization issue. Present the root cause category, the specific error message, and a concrete corrective action for each category."

### Deadline Proximity Alerts and Escalation (R5)

- [x] In `app/agent.py` system prompt: instruct the agent to load the `escalation-advisor` skill when the user asks about at-risk tasks, overdue items, or escalation
- [x] Implement tool `get_tasks_near_deadline`: uses `get_closing_tasks` output filtered by `dueAt` within configurable threshold (default: tasks due within 24 hours or already overdue)
- [x] System prompt: "When surfacing escalation recommendations, retrieve the task's `recipientUsers` or `recipientGroups` from the task details to identify the responsible owner. Present the escalation recommendation as: task name, due date, current owner, recommended escalation action, and urgency level (critical/high/medium)."
- [x] System prompt: "Escalation execution requires controller confirmation. Surface escalation recommendations; do not execute them autonomously."

### Closing Configuration Support (R6)

- [x] Implement tool `get_capabilities`: calls AFC Scheduling SPI `/Capabilities` to retrieve the scheduling system capabilities and application URL
- [x] Implement tool `get_task_provider_capabilities`: calls AFC Task Provider V2 `/capabilities` to retrieve task provider capabilities
- [x] In `app/agent.py` system prompt: "When asked about closing calendar configuration or system setup, use the capabilities tools to retrieve current system configuration. Refer the user to the SAP Advanced Financial Closing administration UI for changes to task ownership and escalation thresholds."

### Agent System Prompt Assembly

- [x] In `app/agent.py`, assemble the full system prompt with:
  - Role definition: "You are a Financial Closing Advisor Agent. You help financial controllers monitor and manage the financial closing cycle using SAP Advanced Financial Closing."
  - Tool usage instruction: "IMPORTANT: You MUST use tools to retrieve live data. Never fabricate, guess, or invent data. Relay tool errors verbatim without adding suggestions."
  - Pagination instruction: "When calling tools that support pagination, always set the page size parameter (`$top`, `top`) to a maximum of 100."
  - Error instruction: "If a tool returns an error, report the error message exactly as received."
  - Skill loading instruction: "Load the `closing-task-analysis` skill for dependency chain evaluation and root cause analysis. Load the `escalation-advisor` skill for deadline and escalation queries."

---

## MCP Tool Integration

- [x] Invoke `mcp-translation-file` skill for `specification/financial-closing-advisor-agent/api-specs/afc-scheduling-spi.json` (ORD ID: `sap.afc:apiResource:SSPIV1:v1`, type: `openapi-v3`)
- [x] Invoke `mcp-translation-file` skill for `specification/financial-closing-advisor-agent/api-specs/afc-task-provider-v2.json` (ORD ID: `sap.afc:apiResource:TaskProviderV2:v1`, type: `openapi-v3`)
- [x] Invoke `setup-solution` skill to create MCP server assets for both translation files
- [x] Read the generated `asset.yaml` files for both MCP server assets and copy their exact `ordId` values (do NOT invent or infer ORD IDs)
- [x] Wire MCP tool loading in `agent.py` using `get_mcp_tools()` from the `mcp_tools` module
- [x] Add both MCP server dependencies to `asset.yaml` under `requires` using the exact ORD IDs from the generated assets
- [x] Generate `mcp-mock.json` using the `mcp-mock-config` skill

---

## Business Instrumentation

- [x] Implement structured logging and OpenTelemetry spans for all 5 milestones from the PRD:
  - M1: `[M1.achieved]: Financial closing cycle detected — period {period_id} opened` / `[M1.missed]: No active closing cycle found in SAP AFC`
  - M2: `[M2.achieved]: Task snapshot complete — {n} tasks retrieved, {n_blocked} blocked` / `[M2.missed]: Task retrieval failed or returned empty result for period {period_id}`
  - M3: `[M3.achieved]: Dependency chain evaluated — {n_blockers} blocking chains identified` / `[M3.missed]: Dependency evaluation incomplete — insufficient task data`
  - M4: `[M4.achieved]: Recommendations delivered — {n} actions recommended` / `[M4.missed]: No recommendations generated — all tasks completed or no actionable items`
  - M5: `[M5.achieved]: Escalation surfaced for {n} tasks — owners identified` / `[M5.missed]: No tasks breached escalation thresholds at this time`
- [x] Extract business logic from `stream()` into a plain async helper `_run_agent()` and instrument that method with OpenTelemetry spans (use decorator form `@tracer.start_as_current_span("name")` on regular async methods)
- [x] Verify `bootstrap(app)` is called after `app = server.build()` in `main.py`

---

## Testing

- [x] `conftest.py` only sets `IBD_TESTING=true`
- [x] Write unit tests in `assets/financial-closing-advisor-agent/tests/`:
  - `test_get_closing_tasks.py` — mocked AFC Task Provider response; validates status classification
  - `test_get_task_details.py` — mocked single task retrieval; validates field mapping
  - `test_get_job_definitions.py` — mocked job definition list
  - `test_get_job_status.py` — mocked job status response; validates status enum mapping
  - `test_get_job_error_messages.py` — mocked error message retrieval; validates error severity filtering
  - `test_get_tasks_near_deadline.py` — mocked tasks with `dueAt` values; validates deadline proximity filtering
  - `test_get_capabilities.py` — mocked capabilities endpoint
- [x] Write one integration test: end-to-end agent invocation with mocked LLM responses and mocked MCP tools, simulating a "What should I do next for the current closing cycle?" query; assert at least one recommendation is returned
- [x] Run `pytest` from `assets/financial-closing-advisor-agent/` (no args); if coverage < 70%, add targeted tests
- [x] Run `pytest` again (no args) to generate final `test_report.json`
- [x] Verify `test_report.json` exists in `assets/financial-closing-advisor-agent/`
