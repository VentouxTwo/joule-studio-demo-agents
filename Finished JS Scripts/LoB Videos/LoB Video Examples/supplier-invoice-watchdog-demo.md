# Supplier Invoice Watchdog — Demo Script


---

## INTRO: Joule Work Browser

Here we are in the Joule Work Browser. This is your UI gateway to SAP. 

In conversations, you can interact with your agents directly .Check your spaces to surface key business data you pinned. And when you need to build something new, this is where you come to Joule Studio. You can build agents, worflow, data product,and extensions.

---

## SECTION: Describe the Intent

To build, we simply type in a prompt: 
*"Build me an agent that checks invoices and flags suppliers billing more than we agreed on. and provide a recommendation "*
Let's hit build.

---

## SECTION: Solution Description

Joule Studio gets to work. 

While that loads, let me explain what we are building.This agent check discrepancies between what a supplier billed on the invoice and what was on the purchase order. Maybe a price went up. Maybe a discount was applied. Maybe shipping changed or the quantity was different. Normally you would have to manually check through all those documents to figure out why. An agent is great at sorting through this information for us. 

---

## SECTION: Joule Studio Enriches Your Intent

You can see it is checking the Knoweldge graph to figure out the invoice process and what apps cover that process.

This is a huge differentiator for Joule Studio, becuase before I would need to write a very detailed prompt, read prompt engineering blogs and explain how your business works to get a useful response 

 But in Joule Studio understand how my businesss works already.  it has the SAP context to enrich / add on to your prompt. . So i don't  explain your business from scratch to get relevant results 

## SECTION: Clarifying Questions

If it needs clarification, Joule Studio asks follow-up questions to make sure it understands your intent and is connected to the right SAP S/4HANA data, or what are the KPIs.

---

## SECTION: Intent Document

It then takes your prompt and context and produces an intent document that shows what you are trying to solve. 

I like to think of it like a back of the napkin drawing. 
The goal is to make sure you and the AI are on teh same page. This is your chance to confirm that Joule Studio understood you correctly. 

## SECTION: From Intent to a Product Requirements Document

Once the intent is clear, let's get Joule Studio to produce a Product Requirements Document. This is a more detailed doc covering what it is, who it is for, and why we are building it. 

It keeps your business and development team aligned for what the solution and goals. And it is a living document — you can keep iterating and Joule Studio will kepp updating PRD along with it.

---

## SECTION: From PRD to Technical Specification
Joule Studio then translates the PRD into a technical specification. The PRD is what we want to build. The spec is how we build it. It is the blueprint defines the SAP APIs, logic, and agent configuration. 
---

## SECTION: The Generated Solution

Let's look at what Joule Studio built. It generated an agent for invoice analysis and an MCP server to connect to S/4HANA purchase orders and invoices. 

We can see and edit all the Python code right here. The `agent.py` file controls the logic — what instructions the agent follows, what it sends to the LLM, and what response it sends back to you. The skill files, like the invoice deviation skill, give the agent step-by-step instructions for doing a specific job. 

Once built this is going to be an MVP, there are lots of ways to keep working on this. 
You can iterate directly in the web-based editor or prompt joule to write it for you 
But you don't have to work here. We hand off to Claude Code and your preferred IDE like Visual Studio Code without losing context or progress.
---


## SECTION: See It Running

Let's test out the agent. We'll ask: *"Show me invoices with billing issues."*

The agent finds three invoices where the billed amount does not match the purchase order. For each one it investigates why. Maybe the price shifted. Maybe a quantity changed. It figures that out and gives you a recommendation on what to do next.

This is a basic demo example. A full agent would go further and be able to do more — emailing the supplier directly to learn more, triggering an approval workflow, or auto approve invoices. 

That is a quick tour of Joule Studio and I will take questions now. 
---

