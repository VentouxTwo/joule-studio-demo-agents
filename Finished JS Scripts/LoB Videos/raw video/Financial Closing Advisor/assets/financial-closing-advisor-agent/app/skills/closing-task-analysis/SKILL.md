---
name: closing-task-analysis
description: Step-by-step instructions for analyzing SAP AFC closing task statuses, resolving dependency chains, identifying blockers, and recommending corrective actions for financial controllers.
---

# Closing Task Analysis Skill

## When to Use This Skill

Load this skill when the user asks about:
- Current status of closing tasks
- Which tasks are blocked or at risk
- Task dependencies and sequencing
- Root cause of a blocked task
- What to do next in the closing cycle

## Task Status Classification

Map SAP AFC task and job statuses to these four buckets:

| AFC Task Status       | Closing Bucket |
|-----------------------|----------------|
| READY                 | Pending        |
| RESERVED              | In-Progress    |
| IN_PROGRESS           | In-Progress    |
| FOR_RESUBMISSION      | In-Progress    |
| COMPLETED             | Completed      |
| CANCELED              | Blocked        |
| INACTIVE              | Blocked        |

| AFC Job Status            | Closing Bucket |
|---------------------------|----------------|
| requested / running       | In-Progress    |
| completed / completedWithWarning | Completed |
| completedWithError / failed | Blocked      |
| cancelRequested / canceled  | Blocked      |

## Dependency Chain Evaluation Steps

1. Retrieve all task definitions from `/taskDefinitions` to understand the standard task catalog and ordering.
2. Retrieve all tasks from `/tasks` for the current period.
3. Classify each task using the status table above.
4. For each blocked or in-progress task, check if any pending tasks have it as a logical prerequisite (same task list, earlier sequence number or dependency flag).
5. Present the dependency chain as an ordered list, highlighting the first blocker in the chain.
6. If a task is blocked by a failed job, retrieve the job result messages from `/JobResult/{ID}/messages` to identify the specific error.

## Root Cause Categories

When a task is blocked, determine the root cause category:

| Category         | Indicators                                           | Corrective Action Pattern                              |
|------------------|------------------------------------------------------|--------------------------------------------------------|
| A: Data Error    | Error message mentions missing field, invalid value, no data found | Identify the missing/invalid data field; ask controller to verify source data |
| B: System Error  | Error message mentions timeout, connection, internal error | Check system availability; retry after system recovery |
| C: Dependency Error | Upstream task status is not "completed"; job not yet triggered | Identify and complete the upstream task first |
| D: Access Error  | Error message mentions authorization, permission denied, no access | Identify required role/permission; escalate to system admin |

## Next-Action Recommendation Format

For each recommendation, present:
1. **Task Name** — the AFC task description
2. **Current Status** — Blocked / In-Progress / Pending
3. **Priority** — VERY_HIGH / HIGH / MEDIUM / LOW (from AFC task priority)
4. **Reason for Prioritization** — why this task needs attention now
5. **Suggested Action** — e.g., "Investigate Data Error in job XYZ", "Complete upstream task ABC first", "Reassign to available owner"
6. **Downstream Impact** — number of tasks waiting on this one

## Important Rules

- Always retrieve live data using tools before making any assessment.
- Never guess task statuses or dependency relationships.
- If tool calls fail, report the error verbatim and stop.
- Present recommendations in priority order: Critical (VERY_HIGH, overdue) > High > Medium > Low.
