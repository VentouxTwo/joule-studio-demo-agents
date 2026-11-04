# Getting Started with n8n Workflows in Joule Studio
**Estimated duration:** ~3 minutes
**Target audience:** SAP developers and business technologists exploring workflow automation in Joule Studio

---

## HOOK

Every business has processes that should be automatic — but aren't. [beat] Someone is manually checking blocked invoices, chasing approvals, copying data between systems. It's slow, it's error-prone, and honestly, it's the kind of work nobody should be doing by hand.

What if you could describe the process in plain language — and have it built for you?

Hey, I'm Michael, and I'm going to show you how to get started building n8n workflows inside Joule Studio. We'll connect to SAP, add logic, automate actions, and I'll show you how easy it is to keep extending it once it's running.

---

## SECTION: What is n8n in Joule Studio?

n8n is a workflow automation tool — it lets you build automated processes that connect apps, move data, and trigger actions based on your business logic. [beat] And inside Joule Studio, it's not just a standalone tool. It's wired directly into SAP's context, governance, and pre-built connectors. That means you get n8n's flexible canvas paired with everything SAP already knows about your business.

---

## SECTION: Build It With Intent

So let's build something real. We've got a problem: blocked invoices are sitting in S/4HANA, and the AP team is handling them manually — one by one. Let's fix that.

I'll describe what I want to Joule Studio: *"Resolve blocked invoices from S/4HANA and send resolution recommendations to the AP team in SAP Task Center."*

That's it. [beat] Joule's AI analyses that statement — grounded in your actual processes and system landscape — and generates a structured product requirements document. From there, Joule Studio writes the code for the n8n workflow automatically.

No blank canvas. No guessing where to start.

---

## SECTION: See the Workflow on the Canvas

Once it's generated, you can review the code — or just open it on the n8n canvas and see exactly how it works.

Here's what this workflow does: every weekday at 6am, it pulls a list of blocked invoices from S/4HANA. An AI agent checks each one against the relevant purchase orders and goods receipts. It makes a recommendation — approve or escalate — and sends that to the AP team as a task in SAP Task Center. The AP team reviews it, approves or rejects, right there. Done.

Now let's look at how that's actually built.

---

## SECTION: Understanding Nodes

Every workflow is made up of nodes. Each node does one specific thing: it receives input data, performs an action, and passes the result to the next step.

Every workflow starts with a **trigger node** — the thing that kicks everything off. Here it's a schedule: 6am every weekday. But triggers can also be a form submission, a webhook, or an SAP event like a Joule message.

Then you've got three types of nodes you'll use most:

**SAP nodes** — pre-built connectors for S/4HANA, SAP Task Center, and other SAP products. No custom integration work. They're just there.

**Flow nodes** — they branch the workflow based on your logic. If an invoice meets certain criteria, go this way. If not, go that way.

**Human review nodes** — these pause the workflow and ask a person to make a decision. Send a task to SAP Task Center, a message in Slack, an email in Outlook — whatever fits your team's process.

---

## SECTION: Extend It on the Canvas

Once the workflow is running, it's easy to keep building on it. Let's say you want a summary email sent to the team every time a batch of invoices gets released. [beat] Just drag in an action node, pick Gmail from the connector library — or any of the hundreds of other apps available — configure it, and you're done.

**Pro tip:** You don't even have to touch the canvas. Open Joule Studio chat, describe what you want to add, and it'll wire it up for you.

Let's do one more: if an invoice gets rejected, we want it logged in an Excel spreadsheet for tracking. I'll ask Joule — *"If an invoice is rejected, add it to our tracking spreadsheet."* [beat] There it is on the canvas.

---

## CLOSE

That's the shift n8n in Joule Studio makes possible — going from isolated processes and one-off automations to connected, agentic workflows that run your business in the background.

If you want to explore further, check out Joule Studio and start building for free. Thanks for watching!
