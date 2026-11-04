# Task Status Classification Rules

## AFC Task Status → Closing Bucket Mapping

| AFC Task Status       | Closing Bucket | Controller Action Needed? |
|-----------------------|----------------|---------------------------|
| READY                 | Pending        | Monitor; action if overdue |
| RESERVED              | In-Progress    | No — being processed       |
| IN_PROGRESS           | In-Progress    | No — being processed       |
| FOR_RESUBMISSION      | In-Progress    | Check if snoozed too long  |
| COMPLETED             | Completed      | No action needed           |
| CANCELED              | Blocked        | Investigate root cause     |
| INACTIVE              | Blocked        | Investigate root cause     |

## AFC Job Status → Closing Bucket Mapping

| AFC Job Status          | Closing Bucket  | Controller Action Needed? |
|-------------------------|-----------------|---------------------------|
| requested               | In-Progress     | No                         |
| running                 | In-Progress     | No                         |
| completed               | Completed       | No                         |
| completedWithWarning    | Completed       | Review warnings            |
| completedWithError      | Blocked         | Investigate errors         |
| failed                  | Blocked         | Investigate errors         |
| cancelRequested         | Blocked         | Confirm cancellation intent|
| canceled                | Blocked         | Investigate root cause     |

## Escalation Priority Logic

Tasks are ranked for escalation in this order:
1. **Critical**: Blocked tasks with VERY_HIGH priority OR tasks past their due date
2. **High**: Blocked tasks with HIGH priority OR tasks within 24h of due date
3. **Medium**: Blocked tasks with MEDIUM priority OR in-progress tasks significantly delayed
4. **Low**: Pending tasks approaching due date

## Dependency Detection Rules

- If task B's task list has task A as a predecessor (earlier sequence), then B depends on A
- If A is blocked, B is at risk
- Downstream impact = count of all tasks that directly or transitively depend on a blocked task
