# Transcript: Shipping Your First Managed Agent — Claude Managed Agents Workshop

**Speaker:** Isabella He, Member of Technical Staff, Anthropic (Applied AI Team)

---

## Introduction

Hello everyone. It's great to see you all here today for our session on shipping your first managed agent.

My name is Isabella He. I'm a member of technical staff at Anthropic on the applied AI team. The applied AI team at Anthropic sits at the intersection of products, research, and our customers, which means I get to contribute internally to products at Anthropic like Claude Code and our cloud harnesses, as well as work externally with customers building on top of Claude and on top of our harnesses.

My goal today is to get you all hands-on with actually building on top of managed agents, understanding how the harness works under the hood, and getting you ready to actually ship your first incident response management agent.

---

## Agenda Overview

1. A quick refresher on Claude Managed Agents
2. How the harness works under the hood
3. Hands-on workshop — building a site reliability agent
4. Beyond the basics — what's next

Our team put a lot of thought into the architectural design of Claude Managed Agents to make sure it runs reliably for production-ready agents. Understanding the architecture means that when we get into the hands-on workshop, you'll understand what each of the primitives you're building actually means under the hood.

---

## How We Got Here: The Evolution of Claude's Developer APIs

### Messages API (2023)
When we first released Claude back in 2023, we released the Messages API alongside access to Claude. This provided raw model access to all Claude models — the very first way people could programmatically build on top of Claude. Essentially tokens in and tokens out.

This also meant that everyone building on top of Claude had to implement all the various primitives themselves: context management, the agent loop, compaction, and so on. When models were less intelligent in 2023, some of these primitives were simpler because agents could simply do less.

### Agent SDK
As model intelligence increased and agents started taking on more complex tasks and actions, the primitives around context management and tool calls became much more complex. That's when we moved to the Agent SDK — a harness that allows you to programmatically call Claude Code, one of our favorite agents at Anthropic.

Claude Code is an agent that has access to a computer and takes actions within a file system. The Agent SDK became a way to make Claude much more powerful by leveraging the power of Claude Code within a harness. However, developers still had to manage hosting and scaling on their own.

### Claude Managed Agents
That's when we evolved into Claude Managed Agents — the first harness to handle scaling and production-ready components on your behalf, provided by Anthropic. This includes:

- A purpose-built harness
- Sandboxing
- Observability
- Tool runtime
- Managed infrastructure

Developers can now focus on task and agent configuration and custom tool logic — the things that actually matter for bringing domain expertise to your agents — while handing off the basics of agent running to Anthropic.

---

## Why Harnesses Must Evolve Alongside Agents

We've seen people build 10 to 15 times faster to production with Claude Managed Agents.

Part of the reason we built Claude Managed Agents is that harnesses should evolve alongside your agents. For example, when we were building on top of Sonnet 4.5, we noticed a behavior called **context anxiety** — Sonnet 4.5 started wrapping up tasks early even when it still had room to spare in its context window. To manage that, we added mitigations in our harness to combat early stopping behavior.

When Opus 4.5 came out, that behavior went away entirely — making all that work essentially obsolete. The takeaway: it's a lot of work to maintain harnesses and make sure they evolve alongside your agents. With Claude Managed Agents, Anthropic handles all those complexities — compaction, caching, context anxiety, and other primitives — so you can focus on what actually matters.

---

## The Three Primary Resources in Claude Managed Agents

### 1. Agents Endpoint — The Brain
The persona and capabilities of your agent. Here you define the model, MCP servers, skills, and components the agent can leverage when running in the agent loop.

### 2. Environments — The Hands
The space and container where the agent actually takes action on your behalf. Think of the agent endpoint as the brain and the environment as the hands.

### 3. Sessions — The Connector
Sessions tie agents and environments together. A single session is spun up on an agent instance within an environment, connecting the two and streaming events back to the user.

A key design decision: **the agent loop runs server-side**. This means hosting, scaling, and durability are abstracted away. When you close your laptop or hit hard refresh, everything is maintained — you don't have to worry about reliability or turning your prototype into production.

---

## Key Architectural Decision: Decoupling the Brain from the Hands

Previously, many agent harnesses coupled the agent loop tightly with tool execution. This design pattern makes sense for agents like Claude Code where you want the agent to access files and take action within a file system.

But we realized there are constraints with tightly coupled designs. By decoupling the hands from the brain:

**Security:** Credentials and security became a major concern when agents can access your file system. Decoupling adds distinct sandboxing — the agent can no longer access credentials without encryption.

**Latency:** Previously, spinning up containers for every session contributed additional latency. With decoupling, our teams saw over a **90% reduction in time to first token (TTFT)** for P95 latency metrics.

The power of this design decision comes through from the perspective of safety, reliability, latency, and everything else you care about when building production-ready agents.

---

## Hands-On Workshop: Building a Site Reliability Agent

### The Use Case

Many software engineers are familiar with the pain of incident response. You might get woken up at 3:00 a.m. when on call because a server or service goes down. For a human, this means diving into metrics, logs, and deployments to investigate what's going wrong.

What we're going to do is have an agent run on Claude Managed Agents to handle all of this — so when you get woken up at 3 a.m., you can hand it off to an agent. Or maybe you don't get woken up at all.

### Setup

Clone the workshop repository and navigate to the `ship-your-first-managed-agent` directory. Install requirements, copy the environment key into your `.env` file, add your Anthropic API key, and run the app:

```bash
git clone <repository-url>
cd ship-your-first-managed-agent
python -m venv venv && source venv/bin/activate  # Mac
pip install -r requirements.txt
cp .env.example .env
# Add your Anthropic API key to .env
streamlit run app.py
```

You'll have two files open: `agent.py` (incomplete) and `agent_complete.py`. We'll copy primitives from the completed file one by one to see how each piece composes the agent.

---

### Step 1: Define the Agent

The agent defines the persona and capabilities — the model, system prompt, and tools.

```python
# Define the SRE agent
agent = create_agent(
    model="claude-opus-4-7",
    system_prompt=system_prompt,
    tools=tools
)
```

The system prompt is intentionally simple — we're telling it that it's an SRE agent responsible for debugging incidents. It has access to tools like `get_metrics`, `get_recent_deploys`, `get_diff`, and `fetch_logs` — the same tools a developer would want when managing an incident response.

Once defined, the agent gets a unique identifier.

---

### Step 2: Define the Environment

The environment is where the agent does its work. We define the SRE agent to work within Anthropic's cloud with unrestricted networking access for this demo:

```python
environment = create_environment(
    type="anthropic_cloud",
    networking={"allowlist": ["*"]}
)
```

Claude Managed Agents is composable and customizable. The networking list is an allowlist — if you want the agent to only access specific sites and URLs, you can restrict it as much as you like.

We also recently released **Claude MCP Tunnels**, which give you the ability to run MCP servers within a private environment instead of the public network — another component for making agents production-ready and secure.

---

### Step 3: Upload Data and Context to the Agent

One of the first places we realized the power of giving an agent access to files was with Claude Code. Here we leverage the Files API by uploading metrics and logs to the agent so it can run code and process those files:

```python
# Attach log file as a resource for the agent
log_file = upload_file("logs/incident_logs.json")
```

**Context engineering is a huge portion of what makes an agent powerful.** This is where developers spend the majority of their time on top of primitives like Claude Managed Agents — managing what types of files are uploaded and how the agent processes them.

---

### Step 4: Create a Session

The session binds the agent and environment together and mounts the log:

```python
session = create_session(
    agent_id=agent.id,
    environment_id=environment.id,
    resources=[log_file]
)
```

This gives the agent the ability to start acting and interacting with the user.

---

### Step 5: Stream Responses

When Claude Managed Agents runs within a single session, instead of responding in tokens in and tokens out, it works in **units of events**. Events include things like user messages, agent tool calls, and agent responses. Every event can be logged from an observability perspective and streamed back to the user.

```python
for event in session.stream(user_message):
    # Handle event types: tool_call, agent_response, user_message
    display_event(event)
```

This is crucial for both user experience (users see things as they come through, not just when Claude finishes an entire task) and observability. Claude Managed Agents has a built-in console for looking at everything the agent is doing.

---

### Step 6: Define Local Tools

The agent is defined server-side, but it needs local tools to take action on your infrastructure:

```python
tools = [
    get_metrics,
    get_recent_deploys,
    get_diff,
    fetch_logs
]
```

The execution of the agent is completely separate from the agent loop — tool execution runs locally on your laptop or infrastructure while the agent loop runs in Anthropic's managed infrastructure.

---

### Step 7: Session Management and Deletion

```python
def delete_session(session_id):
    session.delete(session_id)
```

From a security perspective, if you want to make sure nothing is retained for sessions you don't want in the cloud, you can proactively manage how sessions are deleted. Once deleted, they are removed from every log as well.

---

### Live Demo Results

After asking the agent to debug an incident, it:

1. Ran sandbox commands to check logs
2. Called `get_recent_deploys` to review recent deployments
3. Called `get_metrics` to pull performance data
4. Streamed all tool calls and responses in real time

**The agent's finding:** The incident was caused by database pool exhaustion. A commit by Alice that refactored the order summary builder introduced a query that exhausted pool resources. The agent ruled out other causes and provided recommended remediation actions.

---

## Key Concepts Recap

### Sessions Speak in Events, Not Tokens
Instead of request/response pairs, events are appended to logs. This makes it easy to resume a session, review everything from a log perspective, and — when the brain is separated from the hands — restart a container without restarting the entire agent loop.

### Local Tool Execution, Cloud Agent Loop
Tools execute locally or in your own infrastructure. The agent loop runs in Anthropic's managed cloud. With **bring your own compute**, you can swap out where the agent executes its tools — from a JSON file locally all the way to a Datadog client in production, using the same wire protocol.

### Session State Management
Sessions move through states: **idle → running → rescheduling → terminated**. The agent can restart from a reliability and resumability perspective. You can also trigger state transitions via webhooks — when an external event comes in, the agent can resume a session or kickstart a specific state based on that event.

### Everything Lives in the Cloud
Conversations persist when you hard refresh. Sessions are maintained without any database management on your part. Going from prototype to production doesn't require wiring up where the agent is stored.

---

## Beyond the Basics: Advanced Features

### Sub-Agents (Multi-Agent)
An orchestrator agent spins up context with sub-agents, each handling tasks with their own context windows and contributing back to the main agent. Enables parallelization and better context management.

### Memory & Dreaming
For self-improving agents that learn from user corrections and remember preferences. **Dreaming** means Claude can look through its own memory logs, determine what to keep, and memorize which parts of user preferences and corrections to retain for future sessions.

### Outcomes
Define a rubric for your agent's desired outcomes. Instead of just executing tool calls, the agent figures out along the way which tool calls it needs to make to reach the final result you defined.

### Vaults
Secure credential management per user per session. Credentials are stored on a separate endpoint with encryption, separate from what the agent can access. No need to set up your own secret stores.

### Additional Features
- **Webhooks** — trigger agent actions based on external events
- **Fine-grained permission policies**
- **MCP server controls** — recently released new MCP server controls
- **Console Agent Builder** — built-in observability dashboard and agent configuration directly in the developer console

---

## What We Accomplished Today

Starting from an empty agent built on a few primitives, we:

1. Defined the agent — persona, capabilities, model
2. Gave the agent an environment
3. Gave the agent data and context to operate over
4. Created a session — combining agent and environment
5. Streamed responses to the user
6. Implemented local tools
7. Added session deletion

And within a Streamlit app, we saw how all of these primitives come together to present a working agent to users.

All of compaction, caching, and tool calling was handled by Claude Managed Agents. You can all leave here knowing you built something that will save future developers hours of being woken up at 3:00 a.m. to handle incidents.

---

## Resources

- Claude Managed Agents documentation: [docs.anthropic.com](https://docs.anthropic.com)
- Workshop repository: available via the session QR code
- Next session: **Dreaming** — self-improving agents and memory built into the harness

---

*End of transcript.*
