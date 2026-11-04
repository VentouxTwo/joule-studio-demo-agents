---
name: escalation-advisor
description: Instructions for evaluating deadline proximity, triggering escalation recommendations, and identifying task owners for financial closing tasks in SAP AFC.
---

# Escalation Advisor Skill

## When to Use This Skill

Load this skill when the user asks about:
- Tasks approaching or past their deadlines
- Which tasks need escalation
- Who owns a specific task
- Overdue closing activities
- Escalation recommendations

## Escalation Threshold Evaluation Steps

1. Retrieve all tasks from `/tasks` for the current period.
2. Filter tasks by their `dueAt` field to identify:
   - **Overdue**: `dueAt` is in the past AND status is not COMPLETED or CANCELED
   - **Critical**: `dueAt` within the next 2 hours
   - **At Risk**: `dueAt` within the next 24 hours
3. For each at-risk or overdue task, retrieve full task details from `/tasks/{taskUrn}` to get owner information.
4. Identify the responsible owner from `recipientUsers` or `processor` on the task.
5. If `processor` is set, that user currently owns the task.
6. If only `recipientUsers` is set, the task is unassigned within a group.

## Escalation Recommendation Format

Present each escalation recommendation as:

```
ESCALATION REQUIRED
Task: [Task Name / Subject]
Due: [Due Date/Time]
Status: [Current Status]
Priority: [AFC Priority]
Current Owner: [processor or recipientUsers list]
Urgency: [Critical / High / Medium]
Recommended Action: [specific action for the controller]
```

## Recommended Actions by Scenario

| Scenario | Recommended Action |
|----------|-------------------|
| Task overdue, owner unresponsive | Escalate to closing manager; reassign task to backup owner |
| Task approaching deadline, in-progress | Contact owner directly; offer support to unblock |
| Task blocked by upstream error | Fix upstream blocker first; owner cannot proceed until resolved |
| Task not yet started, due soon | Notify owner immediately; confirm they are aware of deadline |
| Task with VERY_HIGH priority, any status | Prioritize regardless of due date; treat as critical path |

## Important Rules

- Escalation execution requires controller confirmation — NEVER autonomously send notifications.
- Always present escalation recommendations as options for the controller to act on.
- Report tool errors verbatim; do not invent owner information.
- If `dueAt` is null for a task, note that no deadline is set but still flag if status is blocked.
