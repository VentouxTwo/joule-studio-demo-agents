# Escalation Thresholds and Deadline Proximity Alert Definitions

## Default Escalation Thresholds

| Urgency Level | Condition                                           |
|---------------|-----------------------------------------------------|
| Critical      | Task overdue (past dueAt) OR dueAt within 2 hours  |
| High          | Task dueAt within 24 hours                          |
| Medium        | Task dueAt within 48 hours                          |
| Low           | Task dueAt within 72 hours                          |

## Priority Override Rules

Tasks with VERY_HIGH priority are always treated as at least "High" urgency, regardless of due date.

## Escalation Contacts

Owner resolution priority:
1. `processor` field — user currently assigned and working the task
2. `recipientUsers` list — eligible users if task is unassigned
3. `recipientGroups` list — group responsible if no individual users listed
4. Closing Manager — fallback if none of the above are populated

## Configurable Parameters (set in SAP AFC)

The following are read from SAP AFC configuration:
- Closing calendar (fiscal period deadlines)
- Task ownership assignments (processor / recipientUsers)
- Custom escalation rules per task type

These cannot be modified by the agent — direct configuration changes to SAP AFC administration.
