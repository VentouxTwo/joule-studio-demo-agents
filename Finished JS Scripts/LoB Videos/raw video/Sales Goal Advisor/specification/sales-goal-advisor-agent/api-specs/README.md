# API Specs

This directory contains the EDMX spec files for SAP SuccessFactors APIs used by the sales-goal-advisor-agent.

## Files

- `ECEmployeeProfile.edmx` — SAP SuccessFactors Employee Profile OData API (ORD ID: sap.sf:apiResource:ECEmployeeProfile:v1)
- `PerformanceandGoalsPMGM.edmx` — SAP SuccessFactors Goal Plan OData API (ORD ID: sap.sf:apiResource:PerformanceandGoalsPMGM:v1)  
- `PMGMContinuousPerformanceManagement.edmx` — SAP SuccessFactors Continuous Performance Management OData API (ORD ID: sap.sf:apiResource:PMGMContinuousPerformanceManagement:v1)

## Usage

These specs are inputs for the `mcp-translation-file` skill, which generates MCP translation files enabling the agent to call SuccessFactors APIs via MCP tools.

## CRM Integration Note

SAP Sales Cloud V2 APIs (territory, accounts, leads, opportunities, historical performance) did not return supported OData/REST ORD IDs via API discovery. During local development, CRM tool interactions will use mock data. The real CRM integration will be configured at deployment time.
