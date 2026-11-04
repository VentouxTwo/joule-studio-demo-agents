# Product Requirements Document (PRD)

**Title:** Sales Rep Quarterly Goal Setting Agent
**Date:** 2026-10-01
**Owner:** Product Owner
**Solution Category:** AI Agent

## Product Purpose & Value Proposition

**Elevator Pitch:**
Sales representatives currently spend about 2 hours each quarter manually collecting CRM data and drafting development goals — without any data-driven guidance. This agent automates the entire process: it pulls territory data from the CRM system and the rep's profile and goals from SAP SuccessFactors, recommends relevant quarterly objectives, guides the rep through selection and refinement conversationally, and writes the confirmed goals directly into SuccessFactors.

**Business Need:**
Sales reps lack a structured, data-informed process for setting quarterly development goals. They must manually navigate multiple systems, interpret pipeline and activity data, and translate insights into SuccessFactors goals — a time-intensive and inconsistency-prone process. This agent eliminates that friction by serving as a guided, intelligent assistant that surfaces insights and turns them into actionable, system-recorded objectives.

**Expected Value:**
- Reduce quarterly goal-setting time per rep from 2 hours to 15 minutes
- Improve relevance of goals by grounding them in actual CRM territory and pipeline data
- Increase consistency and completeness of quarterly goals across the sales team

**Product Objectives:**
1. Automate CRM territory data retrieval and SuccessFactors profile loading per rep
2. Deliver data-driven goal recommendations across pipeline, activity, and growth dimensions
3. Enable conversational goal refinement and confirmation with zero manual system navigation
4. Write confirmed goals directly into SAP SuccessFactors on explicit rep approval

## Business Metrics

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Time to complete quarterly goal setting per sales rep | 2 hours | 15 minutes | Per quarter | Sales Performance Management / Goal Creation in SuccessFactors | user |

## Requirements

### Must-Have Requirements

**REQ-01**: Retrieve CRM Territory Data

- **Problem to Solve**: Reps have no easy way to get a consolidated view of their territory — accounts, leads, open opportunities, and historical performance — to inform goal setting.
- **User Story**: As a sales representative, I need the agent to automatically retrieve my territory's managed accounts, active leads, open opportunities, and historical sales performance so that I can base my quarterly goals on real data.
- **Acceptance Criteria**:
  - Given a rep session, when the agent is invoked, then it retrieves all managed accounts, leads, open opportunities, and prior-quarter sales performance for that rep's territory from the CRM system.
- **Maps to Objective**: Objective 1
- **Priority Rank**: 1

**REQ-02**: Fetch Rep Profile and Existing Goals from SAP SuccessFactors

- **Problem to Solve**: Reps must manually look up their own SuccessFactors profile and existing goals before they can set new ones, creating duplication risk and wasted time.
- **User Story**: As a sales representative, I need the agent to retrieve my current profile and existing quarterly goals from SAP SuccessFactors so that my new goals build on what is already recorded.
- **Acceptance Criteria**:
  - Given a rep session, when the agent is invoked, then it fetches the rep's employee profile and any existing goals from SAP SuccessFactors.
- **Maps to Objective**: Objective 1
- **Priority Rank**: 2

**REQ-03**: Recommend Goal Options Across Three Dimensions

- **Problem to Solve**: Reps lack structured guidance on which goals are most relevant to their territory and development stage, leading to generic or misaligned objectives.
- **User Story**: As a sales representative, I need the agent to recommend specific quarterly goal options across pipeline, activity, and growth dimensions based on my CRM data and SuccessFactors profile so that I can choose goals that are meaningful and attainable.
- **Acceptance Criteria**:
  - Given retrieved CRM and SuccessFactors data, when the agent presents recommendations, then it offers at least one goal option per dimension (pipeline, activity, growth) with a brief rationale tied to the rep's actual data.
- **Maps to Objective**: Objective 2
- **Priority Rank**: 3

**REQ-04**: Guide Conversational Goal Refinement

- **Problem to Solve**: A static list of suggestions is not enough — reps need to discuss, adjust targets, and clarify wording before committing to a goal.
- **User Story**: As a sales representative, I need to refine the suggested goals through a back-and-forth conversation with the agent so that the final goals accurately reflect my priorities and context.
- **Acceptance Criteria**:
  - Given goal recommendations, when the rep requests changes or asks questions, then the agent responds with updated suggestions, clarifications, or adjusted targets in a multi-turn dialogue until the rep signals readiness to confirm.
- **Maps to Objective**: Objective 3
- **Priority Rank**: 4

**REQ-05**: Create Confirmed Goals in SAP SuccessFactors

- **Problem to Solve**: Even after deciding on goals, reps must manually enter them into SuccessFactors, introducing delays and transcription errors.
- **User Story**: As a sales representative, I need the agent to create my confirmed goals in SAP SuccessFactors upon my explicit approval so that the goals are recorded without any manual data entry.
- **Acceptance Criteria**:
  - Given a rep's explicit confirmation, when the agent writes goals to SuccessFactors, then all confirmed goals appear in the rep's Goal Plan with correct titles, descriptions, and target dates; the agent confirms success to the rep.
  - The agent MUST NOT create goals without explicit rep confirmation in the same conversation.
- **Maps to Objective**: Objective 4
- **Priority Rank**: 5

## Solution Architecture

**Architecture Overview:**
A Python-based AI agent (A2A protocol) deployed on SAP BTP. The agent uses MCP (Model Context Protocol) tool integrations to communicate with SAP Sales Cloud V2 (CRM data) and SAP SuccessFactors (profile, goals read and write). The agent maintains multi-turn conversation state throughout the session.

**Key Components:**

- **Sales Goal Advisor Agent**: Core Python A2A agent. Orchestrates data retrieval, recommendation generation, conversational flow, and goal creation.
- **CRM MCP Tools**: MCP tool set generated from SAP Sales Cloud V2 APIs — covers territory, accounts, leads, opportunities, and historical performance.
- **SuccessFactors MCP Tools**: MCP tool set generated from SAP SuccessFactors APIs — covers employee profile read, goal plan read, and goal creation/write.

**Integration Points:**

- SAP Sales Cloud V2: read territory data (accounts, leads, opportunities, historical performance) — quarterly, on-demand per session
- SAP SuccessFactors: read employee profile and existing goals; write confirmed goals to Goal Plan — on-demand per session

### Agent Extensibility & Instrumentation

**Agent Extensibility:**
- The agent is designed with extension points to allow future capabilities to be added without restructuring core logic.
- Extensible areas: additional goal dimensions (e.g., learning and development), integration with additional CRM or HR systems, and customizable goal templates per sales role or region.

**Business Step Instrumentation:**
- All business logic steps are instrumented with structured log statements for observability.
- Log pattern: `[MILESTONE_ID].[achieved|missed]: [description]`
- See the Milestones section for the full log statement definitions per step.

### Automation & Agent Behaviour

**Automation Level:** Autonomous agent with human-in-the-loop confirmation gate

**Actions the agent performs without human approval:**
- Retrieve CRM territory data (accounts, leads, opportunities, historical performance)
- Fetch rep profile and existing goals from SAP SuccessFactors
- Generate and present goal recommendations
- Engage in multi-turn goal refinement dialogue

**Actions that require human review or approval:**
- Writing goals to SAP SuccessFactors — requires explicit rep confirmation in the same conversation session

**Model or engine used:** Large language model via SAP Generative AI Hub

**Knowledge & data sources accessed:**

- SAP Sales Cloud V2: territory accounts, leads, open opportunities, historical sales performance (read-only)
- SAP SuccessFactors: employee profile, existing Goal Plan entries (read); Goal Plan (write on confirmation)

**Tools or connectors invoked:**

- `get_territory_accounts` (CRM MCP tool): retrieves managed accounts for the rep's territory — read-only
- `get_territory_leads` (CRM MCP tool): retrieves active leads in the territory — read-only
- `get_open_opportunities` (CRM MCP tool): retrieves open opportunities in the territory — read-only
- `get_sales_performance_history` (CRM MCP tool): retrieves prior-quarter sales performance metrics — read-only
- `get_employee_profile` (SuccessFactors MCP tool): fetches rep profile data — read-only
- `get_existing_goals` (SuccessFactors MCP tool): fetches existing quarterly goals from Goal Plan — read-only
- `create_goal` (SuccessFactors MCP tool): creates a new goal in the rep's Goal Plan — **write, requires explicit rep confirmation**

**Guardrails & fail-safes:**

- The agent MUST NOT create or modify goals in SuccessFactors without a clear, explicit confirmation from the rep in the current session.
- If CRM data retrieval fails, the agent informs the rep and continues with available SuccessFactors data, flagging that recommendations may be incomplete.
- If SuccessFactors profile retrieval fails, the agent halts and informs the rep before proceeding.
- If goal creation fails, the agent reports the failure, preserves the confirmed goal list in the session, and guides the rep to retry.
- The agent does not store or retain session data beyond the active conversation.

## Milestones

### M1: Territory Data Retrieved

- **Description**: The agent has successfully fetched all relevant CRM territory data for the rep's session.
- **Achieved when**: Managed accounts, leads, open opportunities, and historical sales performance are all retrieved from the CRM without error.
- **Log on achievement**: `M1.achieved: CRM territory data retrieved successfully for rep session`
- **Log on miss**: `M1.missed: CRM territory data retrieval failed or returned incomplete results`

### M2: Rep Profile Loaded

- **Description**: The agent has loaded the rep's current employee profile and existing goals from SAP SuccessFactors.
- **Achieved when**: Employee profile and Goal Plan entries are successfully fetched from SuccessFactors.
- **Log on achievement**: `M2.achieved: SuccessFactors profile and existing goals loaded for rep`
- **Log on miss**: `M2.missed: SuccessFactors profile or goals retrieval failed`

### M3: Goal Options Presented

- **Description**: The agent has generated and presented goal recommendations to the rep across pipeline, activity, and growth dimensions.
- **Achieved when**: At least one goal option per dimension is presented to the rep with a data-backed rationale.
- **Log on achievement**: `M3.achieved: Goal recommendations presented across all three dimensions`
- **Log on miss**: `M3.missed: Goal recommendations could not be generated — insufficient data`

### M4: Goals Refined and Confirmed

- **Description**: The rep has reviewed, refined as needed, and explicitly confirmed the final set of goals through the conversational flow.
- **Achieved when**: Rep sends explicit confirmation of the selected and adjusted goals.
- **Log on achievement**: `M4.achieved: Rep confirmed final goal set — ready for SuccessFactors write`
- **Log on miss**: `M4.missed: Session ended without rep confirmation of goals`

### M5: Goals Created in SAP SuccessFactors

- **Description**: All confirmed goals have been successfully written to the rep's Goal Plan in SAP SuccessFactors.
- **Achieved when**: All confirmed goals are created via the SuccessFactors API and the agent receives a success response for each.
- **Log on achievement**: `M5.achieved: All confirmed goals successfully created in SuccessFactors Goal Plan`
- **Log on miss**: `M5.missed: One or more goals failed to create in SuccessFactors`
