# API Discovery Results

## SAP SuccessFactors APIs (with ORD IDs — supported)

| API Name | Type | ORD ID | File Type | Spec File |
|----------|------|--------|-----------|-----------|
| Employee Profile | OData | `sap.sf:apiResource:ECEmployeeProfile:v1` | EDMX | `api-specs/ECEmployeeProfile.edmx` |
| Goal Plan (Performance and Goals PMGM) | OData | `sap.sf:apiResource:PerformanceandGoalsPMGM:v1` | EDMX | `api-specs/PerformanceandGoalsPMGM.edmx` |
| Continuous Performance Management | OData | `sap.sf:apiResource:PMGMContinuousPerformanceManagement:v1` | EDMX | `api-specs/PMGMContinuousPerformanceManagement.edmx` |

## SAP Sales Cloud V2 APIs (no ORD ID — not downloadable)

| API Name | Type | Notes |
|----------|------|-------|
| Sales Territory | OData | No ORD ID returned by discovery |
| Lead | OData | No ORD ID returned by discovery |
| Opportunity | OData | No ORD ID returned by discovery |
| Corporate Account | REST | No ORD ID returned by discovery |
| Account Service | REST | No ORD ID returned by discovery |
| Opportunity Service | REST | No ORD ID returned by discovery |

**Note:** CRM territory data tools will be mocked during local development. At deployment, real CRM API credentials and endpoint configuration are required to replace mock responses.
