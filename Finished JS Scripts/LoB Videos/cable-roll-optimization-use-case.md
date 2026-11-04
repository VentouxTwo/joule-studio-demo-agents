# Cable Roll Optimization Agent — Use Case

## Overview

A construction firm building a data center faces one of the most cable-intensive projects in the industry. Hundreds of work orders, dozens of cable specifications, and custom lengths on every run make manual cable roll planning slow, error-prone, and wasteful.

The Cable Roll Optimization Agent reads work order requirements from SAP S/4HANA, checks available batch stock across all storage locations, and recommends the single roll or combination of rolls that fulfills each work order with the least offcut waste. All recommendations are presented to the planner for review and approval before any SAP data is modified.

---

## The Scenario

A production planner receives a batch of work orders that need to be fulfilled. Each order specifies:
- Cable type and material
- Required length and technical specification
- Deadline

The planner needs to figure out which physical cable rolls in the warehouse to assign to which work orders — in a way that minimizes leftover offcuts. Doing this manually is complex because there can be dozens of partial rolls across multiple warehouse locations, some expiring soon or lacking required certifications, and combining two partial rolls for one order might save waste but introduces splicing complexity.

---

## Pain Points

### 1. The Planning Process is Manual and Slow
A planner manually cross-references work orders against available cable stock in SAP or a spreadsheet — one by one. On a large data center project with hundreds of cable runs, this can eat up hours every day, and it still relies heavily on the planner's experience and memory.

### 2. No Visibility Across Locations
Cable stock is spread across site warehouses, regional depots, and supplier yards. Planners often don't know what's where — so they order new stock while rolls sit unused elsewhere. The material exists, but the visibility doesn't.

### 3. Offcut Waste is Guesswork
When a 500m roll covers a 340m job, the 160m offcut goes back to the rack with no systematic tracking. Over time the warehouse fills with short rolls nobody knows how to use, and they eventually get scrapped — pure material cost with no return.

These three compound each other: slow manual planning means less time to think about offcuts, poor location visibility means planners default to ordering new rather than searching, and untracked offcuts quietly drain project margin every single day.

---

## What the Agent Does

1. **Reads work order requirements** from SAP S/4HANA — cable material, required length, and specification
2. **Checks batch stock** across all storage locations to find available cable rolls
3. **Runs an optimization engine** to recommend the single roll or combination of rolls that fulfills the work order with the least offcut waste
4. **Handles stock shortages** — if local stock is insufficient, it identifies rolls at other locations and recommends raising a stock transfer order
5. **Human-in-the-loop** — all recommendations go to a planner for review and approval before any SAP data is changed
6. **Configurable** — supports thresholds for acceptable waste, location priority rules, and batch selection criteria like expiry date and certificate status

---

## Benefits

| Benefit | Description |
|---|---|
| Reduced material waste | Optimization engine minimizes offcuts on every work order |
| Faster planning | What took a planner hours now takes minutes |
| Better stock utilization | Uses up partial rolls before they expire or get scrapped |
| Cross-location visibility | Surfaces stock the planner might not have known existed |
| Human accountability | Planner reviews and approves before SAP is touched |
| Configurable rules | Adapts to site-specific waste thresholds and location priorities |

---

## Business Impact

| Pain Point | Business Cost | Agent Resolution |
|---|---|---|
| Manual planning | Planner time, slow throughput | Automated recommendation in minutes |
| No cross-location visibility | Unnecessary procurement spend | Live stock check across all locations |
| Untracked offcuts | Direct material waste, scrapped rolls | Systematic waste minimization per work order |
