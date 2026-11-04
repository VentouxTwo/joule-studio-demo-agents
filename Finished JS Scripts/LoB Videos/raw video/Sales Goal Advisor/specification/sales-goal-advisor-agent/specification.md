# Specification: sales-goal-advisor-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [x] Read `product-requirements-document.md` and `intent.md` at the solution root as input for this specification.
- [x] Bootstrap agent code in `assets/sales-goal-advisor-agent/` using the `sap-agent-bootstrap` skill instructions.
  - Agent name: `sales-goal-advisor-agent`
  - Agent description: `An AI agent that guides sales representatives through creating meaningful quarterly development objectives by retrieving CRM territory data and SAP SuccessFactors profile and goals, recommending goal options, and creating approved goals in SAP SuccessFactors.`
  - Run bootstrap from inside `assets/sales-goal-advisor-agent/`
- [x] Install dependencies: `pip install -r requirements.txt` (from `assets/sales-goal-advisor-agent/`)
- [x] Validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

This agent requires a runtime skill to handle the multi-step quarterly goal-setting workflow, because the flow involves sequential data retrieval, LLM-driven recommendation generation, iterative conversational refinement, and a guarded write operation — all of which exceed the complexity threshold for inline system prompt instructions.

- [x] Create `assets/sales-goal-advisor-agent/app/skills/goal-setting-workflow/SKILL.md` with:
  - YAML frontmatter: `name: goal-setting-workflow`, `description: Multi-step workflow for quarterly goal setting — retrieves CRM territory data and SuccessFactors profile, generates goal recommendations across pipeline/activity/growth dimensions, guides conversational refinement, and writes confirmed goals to SuccessFactors.`
  - Body: step-by-step instructions covering:
    1. Data retrieval phase (CRM accounts, leads, opportunities, performance + SF profile and existing goals)
    2. Goal recommendation generation across three dimensions (pipeline, activity, growth)
    3. Conversational refinement loop with the rep
    4. Explicit confirmation gate — the agent MUST NOT write goals without clear rep confirmation
    5. Goal creation in SuccessFactors + success acknowledgement
  - Error handling: if CRM data retrieval fails, continue with SuccessFactors data only and flag incomplete recommendations. If SF retrieval fails, halt and inform.

---

## Project-Specific Tasks

### CRM Territory Data Integration

- [x] Verify `specification/sales-goal-advisor-agent/api-specs/` contains the following spec files:
  - `ECEmployeeProfile.edmx` — SAP SuccessFactors Employee Profile API
  - `PerformanceandGoalsPMGM.edmx` — SAP SuccessFactors Goal Plan API
  - `PMGMContinuousPerformanceManagement.edmx` — SAP SuccessFactors Continuous Performance Management API
- [x] Note: No SAP Sales Cloud V2 API EDMX with an ORD ID was available via discovery. The CRM territory data tools (accounts, leads, opportunities, performance) will be represented in the agent with mock data patterns during local development. The MCP translation files for SuccessFactors APIs will provide the real integration path.

### SuccessFactors MCP Translation Files

- [x] Invoke the `mcp-translation-file` skill for each of the three downloaded EDMX specs in `specification/sales-goal-advisor-agent/api-specs/`:
  - `ECEmployeeProfile.edmx` → ORD ID: `sap.sf:apiResource:ECEmployeeProfile:v1`
  - `PerformanceandGoalsPMGM.edmx` → ORD ID: `sap.sf:apiResource:PerformanceandGoalsPMGM:v1`
  - `PMGMContinuousPerformanceManagement.edmx` → ORD ID: `sap.sf:apiResource:PMGMContinuousPerformanceManagement:v1`
- [x] After `mcp-translation-file` completes, invoke the `setup-solution` skill to register the MCP server assets.
- [x] Read the generated `asset.yaml` files for each MCP server asset and extract the exact ORD IDs. Use these verbatim in the agent's `asset.yaml` `requires` section.

### Agent System Prompt

- [x] Open `assets/sales-goal-advisor-agent/app/agent.py` and update the system prompt (`@prompt_section` / `get_system_prompt`) to include:
  - The agent's purpose: guiding sales reps through quarterly goal-setting
  - Instruction to load the `goal-setting-workflow` skill at the start of each session
  - Page size guard: always set `top` / `limit` to max 100 on tool calls that support pagination
  - Error relay: report tool errors verbatim without embellishment
  - Confirmation guard: NEVER create goals in SuccessFactors without explicit rep confirmation in the current session
  - Example: "To begin, I'll retrieve your territory data and SuccessFactors profile. Then I'll recommend quarterly goals across pipeline, activity, and growth dimensions."

### MCP Tool Wiring

- [x] Wire MCP tool loading in `agent.py` using `get_mcp_tools()` from the `mcp_tools` module — follow the canonical lazy-loading pattern from `guidelines-agent-python.md`.
- [x] Add all generated MCP server ORD IDs to the agent's `asset.yaml` under `requires` — one entry per MCP server.
- [x] Generate `mcp-mock.json` using the `mcp-mock-config` skill once MCP translation files and setup-solution are complete.

---

## Business Instrumentation

- [x] Implement structured logging and OpenTelemetry spans for all 5 milestones from the PRD:
  - `M1.achieved / M1.missed`: CRM territory data retrieved
  - `M2.achieved / M2.missed`: Rep profile and existing goals loaded from SuccessFactors
  - `M3.achieved / M3.missed`: Goal recommendations presented across pipeline/activity/growth
  - `M4.achieved / M4.missed`: Goals refined and confirmed by rep
  - `M5.achieved / M5.missed`: Goals created in SAP SuccessFactors Goal Plan
- [x] Extract all business logic from `stream()` into plain async helper methods to avoid `GeneratorExit` context errors with OpenTelemetry spans. Instrument those helpers.
- [x] Verify `bootstrap(app)` is called after `app = server.build()` in `main.py`.

---

## MCP Tool Integration

- [x] Verify `api-discovery-results.md` documents the API ORD IDs used.
- [x] After MCP translation files are generated and MCP server assets created, confirm these files exist for each API:
  ```
  specification/sales-goal-advisor-agent/mcps/*/api-spec.*
  specification/sales-goal-advisor-agent/mcps/*/translation.json
  specification/sales-goal-advisor-agent/mcps/*/.tool-list.json
  ```
- [x] Wire MCP loading as per `guidelines-agent-mcp.md` Path A.
- [x] Generate `mcp-mock.json` using `mcp-mock-config` skill.

---

## Testing

- [x] Ensure `conftest.py` only sets `IBD_TESTING=true`; agent uses mock MCP responses from `mcp-mock.json`
- [x] Write unit tests in `assets/sales-goal-advisor-agent/tests/` — one per MCP tool:
  - `test_get_employee_profile.py`
  - `test_get_existing_goals.py`
  - `test_create_goal.py`
  - `test_get_goal_plan_template.py`
  - `test_get_continuous_performance.py`
  - (Additional tests for any CRM tools discovered during integration)
- [x] Write one integration test exercising the full end-to-end agent flow:
  - Mock LLM returns canned responses
  - Mock MCP tools return test data (territory data, profile, goals)
  - Assert: agent presents goal recommendations, handles refinement, and creates goals on confirmation
  - Assert: agent does NOT create goals without explicit confirmation
- [x] Run `pytest` from `assets/sales-goal-advisor-agent/` (no args) — fix failures before proceeding
- [x] If coverage < 70%, add targeted tests until threshold is met
- [x] Run `pytest` again (no args) to generate final `test_report.json`
- [x] Verify `assets/sales-goal-advisor-agent/test_report.json` exists
