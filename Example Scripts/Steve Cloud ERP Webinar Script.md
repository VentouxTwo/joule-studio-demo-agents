# Demo 1 — Invoice Watchdog Agent

Let me show you an example of an agent built with Joule Studio.

Here in Conversations, you can interact with your agents directly. Agents bring business process expertise and reliably execute multi-step tasks.

Let's use our Invoice Watchdog agent — it checks discrepancies between what a supplier billed on the invoice and what was on the purchase order.

We'll ask:

> "Show me invoices with billing issues last month."

It connects with your cloud ERP data and finds invoices where the billed amount does not match the purchase order. It investigates why. Maybe the price shifted. Maybe a quantity changed.

Based on your business context, it figures out the root causes and recommends what to do next. We can then ask the agent to resolve it for us.

> "Find invoices for supplier USSU-VSF85 in company code 1010 for fiscal year 2026."

This is a very common use case. Instead of manually checking yourself, let agents keep an eye on your work in your cloud ERP and take action — so you can prioritize your energy elsewhere.

---

# Demo 2 — Build with Intent

Thanks Steve. Now I'm in Joule Studio — this is where we build agents and workflows with intent-based development.

Let's build the supplier invoice agent I showed you earlier.

The core premise of intent-based development is that we simply type in a prompt and Joule Studio generates a solution for you.

> "Build me an agent that checks invoices and flags suppliers billing more than we agreed on, and provide a recommendation."

Joule Studio takes your intent and enriches it with your business context.

This makes Joule Studio different from other tools because your agent is grounded in how your cloud ERP works. It understands how it fits in your landscape, the semantics of your business data, and how your processes flow.

Joule Studio uses this information to generate more relevant and tailored solutions.

It also asks clarifying questions to refine the requirements and logic.

Afterwards, Joule Studio creates two documents for you — a Product Requirements Document to align on what we will be building, and a Specification to align on how we will be building it.

Then Joule Studio does the heavy lifting and turns that blueprint into working code.

---

# Demo 3 — Extensions

Let's look at extending our prebuilt line-of-business assistants. Like agents, you can access your assistants in the Conversations tab.

First let me show you how the assistant works out of the box, and then we can customize it.

We will use the Financial Closing Assistant. We'll upload our journal entry data and get the assistant to map it and create the journal entry proposal in S/4HANA.

However, we have custom business rules this agent needs to follow.

In Joule Studio we can extend this same agent with custom behavior. Select the journal entry agent in the catalog and enter your prompt.

Let's customize the agent by adding a check — if any amount exceeds €45, it will ask for your approval, and flag anything unusual.

Afterward, Joule Studio goes through the same intent-based development process I showed before.

Once created, you can see that these new capabilities have been added to our Joule assistant.

---

# Demo 4 — n8n Workflows

Here we are in the n8n visual canvas embedded in Joule Studio.

What is really powerful with n8n is that it connects your workflows with your agents to work together.

We can take our invoice agent we built earlier and make it more powerful by building out an end-to-end blocked invoice process.

Let me walk through this example. n8n has prebuilt connectors that pull a list of blocked invoices from S/4HANA.

Then we bring our invoice agent in to auto-approve invoices or send them to the accounts payable team to take a closer look.

They can review the invoice in SAP Task Center and approve or reject it with a single click — and the decision is written back to your cloud ERP.

Instead of isolated processes and agents, n8n provides one place to orchestrate both agentic and traditional, deterministic automations.

---

# Demo 5 — Governance

AI Agent Hub is where you get to see all your agents, models, and MCP servers in one place. Here we can dig into our tariff supply chain agent.

It makes it easy to manage the AI agent lifecycle and enforce your governance.

Once your agent is deployed, you can track what actions your agents are taking and how well they are performing.

So you can keep learning and improving your agents over time.
