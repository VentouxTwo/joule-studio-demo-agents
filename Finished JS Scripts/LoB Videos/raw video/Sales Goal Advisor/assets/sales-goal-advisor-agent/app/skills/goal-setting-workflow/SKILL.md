---
name: goal-setting-workflow
description: Multi-step workflow for quarterly goal setting — retrieves CRM territory data and SuccessFactors profile, generates goal recommendations across pipeline/activity/growth dimensions, guides conversational refinement, and writes confirmed goals to SuccessFactors.
---

# Quarterly Goal Setting Workflow

## When to Use This Skill

Load this skill at the start of any conversation where the user wants to create, review, or set their quarterly development goals.

## Overview

Guide the sales representative through a structured 5-step process:
1. Retrieve CRM territory data
2. Load their SuccessFactors profile and existing goals
3. Generate goal recommendations across three dimensions
4. Refine goals through conversation
5. Create confirmed goals in SuccessFactors

---

## Step 1: Retrieve CRM Territory Data

Use available CRM MCP tools to retrieve the following for the representative's territory:
- Managed accounts (list of accounts in their territory)
- Active leads
- Open opportunities (name, stage, value, expected close date)
- Historical sales performance (prior quarter: revenue vs. target, win rate, deal count)

**If CRM tools are unavailable or return errors:**
- Inform the rep: "I wasn't able to retrieve your CRM territory data. I'll continue with your SuccessFactors profile only — goal recommendations may be less precise."
- Continue to Step 2.

**Limit all paginated tool calls to top=100.**

---

## Step 2: Load SuccessFactors Profile and Existing Goals

Use SuccessFactors MCP tools to retrieve:
- The rep's employee profile (name, role, department, manager)
- Their existing goals from the Goal Plan (current quarter and any open goals)

**If SuccessFactors profile retrieval fails:**
- Halt. Inform the rep: "I wasn't able to load your SuccessFactors profile. This is required to proceed. Please check your connection and try again."
- Do NOT continue to goal recommendations.

---

## Step 3: Generate Goal Recommendations

Based on the data retrieved in Steps 1 and 2, generate at least one specific, measurable goal option per dimension:

### Pipeline Dimension
Focus on revenue targets and deal progression.
Examples:
- "Close [X] open opportunities worth $[Y] total by end of quarter"
- "Move [X] deals from Proposal to Negotiation stage"
- "Increase pipeline coverage ratio to [X]:1"

Ground recommendations in actual open opportunity data.

### Activity Dimension
Focus on sales activities and customer engagement.
Examples:
- "Conduct [X] discovery calls with net-new accounts per week"
- "Schedule [X] executive business reviews with top accounts"
- "Follow up on [X] stale leads older than 30 days"

Ground recommendations in lead and account data.

### Growth Dimension
Focus on skill development, market expansion, or account penetration.
Examples:
- "Expand into [X] new accounts in the territory"
- "Achieve [certification/training] relevant to product area"
- "Increase average deal size by [X]% through upsell conversations"

Ground recommendations in performance history and profile.

**Present all recommendations clearly with a brief data-backed rationale for each.**

---

## Step 4: Conversational Refinement

After presenting recommendations, engage the rep in a dialogue:

1. Ask which goals resonate and which don't fit their situation.
2. Allow the rep to request adjustments (change targets, swap dimensions, reword a goal).
3. Incorporate their feedback and re-present updated options.
4. Repeat until the rep explicitly confirms readiness to create the goals.

**Guidance:**
- Never assume confirmation. The rep must explicitly say something like "yes, create these", "confirmed", "go ahead", or equivalent.
- If the rep is undecided, offer to simplify (e.g., fewer goals) or adjust targets.
- If the rep wants to exit without creating goals, respect that — summarize what was discussed and offer to return later.

---

## Step 5: Create Goals in SAP SuccessFactors

**CRITICAL GATE: Only proceed after receiving clear, explicit rep confirmation in the current conversation.**

Acceptable confirmation phrases: "yes", "confirmed", "create them", "go ahead", "looks good", "do it", or equivalent.
If confirmation is ambiguous, ask: "Just to confirm — shall I create these goals in SuccessFactors now?"

For each confirmed goal:
1. Call the SuccessFactors Goal Plan MCP tool to create the goal.
2. Include: goal name, description, target date (end of current quarter), status = "In Progress".
3. Confirm success for each goal individually.

**If any goal creation fails:**
- Report the specific failure to the rep.
- Do NOT silently skip — inform them: "Goal '[name]' could not be created. Error: [message]. Would you like to retry?"
- Keep the confirmed goal list in context so the rep can retry without starting over.

**After all goals are created:**
- Summarize the goals created with a brief confirmation.
- Remind the rep they can view and manage them in SAP SuccessFactors.

---

## Error Handling Summary

| Situation | Action |
|-----------|--------|
| CRM data unavailable | Continue with SF data only; flag incomplete recommendations |
| SF profile retrieval fails | Halt and inform rep; do not proceed |
| SF goal creation fails | Report error; retain confirmed list; offer retry |
| Rep exits without confirming | Summarize discussion; do not create goals |
| Ambiguous confirmation | Ask explicitly before writing |
