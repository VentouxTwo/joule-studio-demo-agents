# Joule Studio — L1 Messaging

## Intent

Everything starts with intent — made explicit, durable, and usable beyond the first conversation.

Turn business intent into solutions:
The core premise here is intent-based development. Instead of writing technical specifications from scratch, you describe the business outcome you want. Joule Studio then generates a complete artifact chain: a product requirements document, technical specs, code scaffolding, test artifacts, and a live working preview. The full cycle — from business idea to deployable code — takes as little as 15 minutes for a simple agent, or up to 90 minutes for a complex scenario. That compares to days or weeks with conventional development.



Teams describe the business outcome in plain language: what needs to change, who is affected, what success looks like. Joule Studio captures this as a clear problem statement that carries through the entire lifecycle.

The system then actively analyses that intent — asking clarifying questions and enriching it with real enterprise context: existing processes, architecture constraints, and domain knowledge. It draws on SAP assets including Signavio, LeanIX, domain models, and the SAP Knowledge Graph to ground intent in reality.

The SAP Knowledge Graph provides the business content to select the right APIs, surfaces available SAP APIs and MCP servers, and lets you add your own — giving you enterprise-ready business context from the start.

Teams choose how fast to move. Clear intent? Take the fast track straight to a PRD. Less defined? Joule Studio supports guided refinement so business and IT align before anything is built.

The same context flows from intent into the PRD and onward into development. Handover isn't a reset — it's a continuation.

---

## Product Requirements Document (PRD)

Intent becomes a shared plan — something everyone can align on.

Joule Studio generates a PRD that brings everything together: the problem being solved, target users, success measures, and key requirements. It becomes the single reference point for both business and technical teams.

Requirements are grounded in real enterprise context — system data, process knowledge, and architectural realities drawn from the SAP Knowledge Graph, SAP domain models, and LeanIX. Requirements reflect how the business actually runs, not how someone imagined it might.

The PRD stays traceable. Intent and business outcomes remain visible and revisitable as platforms evolve — making it a long-lived artefact, not a one-time handoff.

This phase also drives an early delivery decision: activate standard SAP capabilities, configure existing solutions, or build something new — an agent, a workflow, or an app.

Intent becomes explicit. Requirements become shared. Teams move forward with a plan that is grounded and actionable.

---

## Specification

Before anything gets built, get the blueprint right.

The PRD is still a plan. The specification turns it into an implementation-ready blueprint: scope, architecture, integrations, security, and the concrete tasks needed to ship. Execution is guided, not guessed.

The spec makes the domain explicit — defining key business objects, system contracts, interfaces, and attributes so behaviour stays consistent from build through testing. Mismatches are caught early, not late.

Two immediate payoffs:
- **Fewer rework loops** — tech choices, integration points, and task breakdown are locked in up front
- **Better output quality** — the build agent follows a real technical blueprint, not raw intent

Guardrails belong here too. Compliance and policy requirements go into the spec early so safety is built in, not bolted on.

Once the spec is solid, Joule Studio moves from planning to execution with far less churn. Code generation becomes predictable.

---

## Code Generation

The spec is locked. Now Joule Studio turns that blueprint into a working solution.

**SAP-aware code generation** — the build agent generates agents, workflows, and applications directly from the spec with SAP context built in: the right SAP Domain Models, the right integration approach, including SAP Integration Suite and n8n where orchestration is needed.

**Freedom of development setup** — no new toolchain required. Generate and edit in the tools developers already use. Output stays standard and portable — real code, not a proprietary artefact.

**Web edit or IDE handover** — iterate quickly in the web experience for speed, or switch into your preferred environment at any point: VS Code, Claude, Cline, or Cursor. No restart. No migration.

**Reviewable by default** — the full codebase is exposed in the editor. Teams can inspect, refactor, and version it in Git using normal engineering discipline.

Joule Studio accelerates implementation without hiding the work. You get speed, you keep control, and you move into testing with something concrete — not a black box.

---

## Testing

You have code. Now confirm it behaves as intended and holds up as a complete solution.

**End-to-end validation** — not isolated checks, but the whole path the user will actually run. Failures caught early are cheap to fix.

**Agent behaviour evaluation** — correctness for agents means more than "did it run." Joule Studio runs automated evaluations and surfaces behaviour and performance in a single test report: clear pass/fail signals, coverage, and behavioural checks — not a vague sense that it "seems fine."

**Targeted diagnosis** — results are broken down per component, making it straightforward to locate a failing subsystem and get back into iteration quickly.

Testing is the checkpoint that makes release predictable. Once testing is green, deployment is a controlled step forward, not a gamble.

---

## Deployment & Operations

Testing gives you the confidence to ship. Deployment makes it real.

**Proper software practices** — the full solution is versioned and pushed to GitHub: reviewable, repeatable, and portable across teams and toolchains.

**SAP managed runtime** — agents, n8n workflows, applications, and extensions deploy onto an SAP managed service. SAP handles scaling, monitoring, and day-to-day operations. Built-in security and compliance are included. Solutions are available immediately on deployment.

**Continuous visibility** — performance, cost, and usage are tracked in production so you can see what agents are doing and what they are costing as they run.

**Observability built in** — tracing, metrics, and logging let you observe behaviour, diagnose issues, and improve over time. Decisions, tool calls, and usage are fully traceable — exactly what teams need for production sign-off and ongoing optimisation.

**AI Agent Hub** — the central control point to discover, manage, and govern what is deployed across the lifecycle, with monitoring of performance, usage, and cost built into the model.

Deploy to an SAP managed runtime. Keep everything under version control. Get the observability needed to run, learn, and improve.
