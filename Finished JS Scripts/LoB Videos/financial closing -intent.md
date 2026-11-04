# Financial Closing Advisor Agent

AI agent supporting financial controllers during the financial closing cycle.

## Business challenge

Financial controllers need real-time visibility into the status, priority, and sequence of all closing tasks across the organization. Today, identifying blocked or at-risk tasks requires manual review of SAP Financial Closing Cockpit data, which is time-consuming and error-prone. Controllers lack automated guidance on which tasks to act on next, and escalation of blocked tasks is slow and reactive.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Time to identify blocked/at-risk closing tasks | ~2 hours (manual review) | < 15 minutes | Per closing cycle | Financial Close Monitoring | user |
| % of closing tasks completed on schedule | Unknown | 95% | Per period-end | Task Sequencing & Execution | user |
| Controller time spent on status reporting | ~3 hours/close | < 30 minutes | Per closing cycle | Closing Coordination | user |
| Escalation response time for blocked tasks | Same day or next day | < 2 hours | Per closing cycle | Escalation Management | user |

## Key Milestones

| Milestone | Condition |
|-----------|-----------|
| Closing cycle initiated | Agent detects new closing period opened in SAP Advanced Financial Closing |
| Task status snapshot retrieved | Agent retrieves and classifies all tasks (completed, in-progress, blocked, pending) |
| Dependency chain evaluated | Agent resolves task sequence and identifies upstream blockers |
| Next-action recommendations delivered | Agent presents prioritized action list with reasoning to the controller |
| Escalation triggered | Agent identifies tasks breaching deadline thresholds and notifies task owners or escalation contacts |

## Business Architecture (RBA)

### End-to-End Process

Finance (Record to Report)

### Process Hierarchy

```
Finance (E2E)
└── Record to Report (generic)
    └── Perform accounting and financial close (generic) (BPS-413)
        └── Perform financial closing
```

### Summary

The agent maps to the "Perform accounting and financial close" sub-process within the Record to Report E2E process. It augments SAP Advanced Financial Closing by adding AI-driven monitoring, dependency analysis, and next-action guidance for financial controllers.

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Webhook API ORD ID | Data Product ORD ID | Gap? | Notes / assumptions |
|------------------------|------------------------|------------|-------------------|--------------------|--------------------|---------------------|------|---------------------|
| Retrieve closing task status from SAP AFC | SAP Advanced Financial Closing — Local/Group Financial Closing (SC6170, SC6171, SC6172, SC6173) | `sap.afc:apiResource:SSPIV1:v1` | — | — | — | — | Yes | No MCP server; requires direct REST API integration |
| Task Center integration (task retrieval/update) | SAP Advanced Financial Closing — Task Provider V2 | `sap.afc:apiResource:TaskProviderV2:v1` | — | — | — | — | Yes | No MCP server; direct API call needed |
| User/ownership management | SAP Advanced Financial Closing — SCIM V2 | `sap.afc:apiResource:SCIMV2:v1` | — | — | — | — | No | Standard SCIM; used for task owner lookup |
| AI-driven dependency chain evaluation & next-action recommendations | None — custom agent reasoning required | — | — | — | — | — | Yes | Core differentiating capability; built in Python agent |
| Root cause identification and corrective action suggestions | None — custom agent reasoning required | — | — | — | — | — | Yes | LLM reasoning over task context and error signals |
| Closing calendar, task ownership, escalation configuration | SAP Advanced Financial Closing (standard config) | `sap.afc:apiResource:SSPIV1:v1` | — | — | — | — | No | Configurable via AFC standard; agent reads config |
| Deadline proximity alerts and escalation notifications | Partially in AFC; full logic requires custom agent | — | — | — | — | — | Maybe | Agent augments AFC alerts with priority-aware escalation |

### Key findings

- SAP Advanced Financial Closing (AFC) is the primary system of record; its REST API (Scheduling Service Provider Interface) covers task retrieval, status, and configuration needs.
- No MCP servers exist for AFC APIs — direct REST integration via the agent's tool layer is required.
- The core intelligence (dependency chain evaluation, next-action ranking, root-cause reasoning) is a gap not covered by any standard SAP product and must be built as custom agent logic.
- Task ownership and user management can leverage the standard SCIM V2 API provided by AFC.
- Escalation and deadline alerting partially exists in AFC; the agent will extend this with AI-driven priority assessment and proactive notification.

## Recommendations

### Financial Closing Advisor — AI Agent

#### Executive Summary

Python AI agent integrating with SAP AFC to guide controllers through the close.

#### Recommended Solution

A pro-code Python AI agent (A2A protocol) that connects to SAP Advanced Financial Closing via its REST APIs. The agent retrieves all closing tasks, classifies them by status, evaluates the dependency chain, and recommends the next actions to the financial controller with clear reasoning. It identifies root causes of blocked tasks and suggests corrective actions. Configuration for closing calendar, task ownership, escalation thresholds, and deadline proximity is read from SAP AFC.

#### Recommended solution category

AI Agent

#### Intent fit
92%
