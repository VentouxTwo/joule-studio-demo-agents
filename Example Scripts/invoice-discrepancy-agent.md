# Demo 1: 
Let me shou you an example of an agent built with Joule Studio 

Here in conversations, you can interact with your agents directly. Agents business process expertise that reliably execute multistep tasks

Let's use our invoice watchdog agent agent checks discrepancies between what a supplier billed on the invoice and what was on the purchase order

. We'll ask:

> "show me invoices with billing issues last m."

It connects with your cloud erp data and the agent finds  invoices where the billed amount does not match the purchase order. It investiage why. Maybe the price shifted. Maybe a quantity changed. 

Based on your business context, tt figures that out the root causes and recommends what to do next
 we can then ask the agent to resolve it for us. 

> " Find invoices for supplier USSU-VSF85 in company code 1010 for fiscal year 2026"

This is a very common use case because Instead of  having manually checking yourself, let agents  keep an eye on your work in your cloud erp and take action while you can prioirtize your energy elsewhere 

# Invoice Discrepancy Agent — Demo Script

---

## Describe the Intent
Thanks Steve, Now i'm in Joule Studio . here is where we can build agents and workflwos with intent based developent

 Let's build the supplier invoice agent I showed you earlier. 

 The core premise of intent based development is:

 we simply type in a prompt and Joule Studio generates a solution for you. 
 
> "Build me an agent that checks invoices and flags suppliers billing more than we agreed on, and provide a recommendation."


---

## Joule Studio Enriches Your Intent

Joule Studio takes your intent and enriches it with your business context 

This makes Joule Studio different from other tools because your agent is grounded in how your cloud erp work. 

  it understands how it fits in your landscape, semantics of your business data, and how your processes flows 

Joule Studio uses this information more relevant and tailored solutions 

Joule Studio also asks clarifying questions to refine the requirements and logic

Afterwards, Joule Studio creates two documentations for you 

 a Product requirements document to align on  what we will be building 
and a specifcation to align on how we will be building it

Now Joule Studio does the heavy lifting and turns that blueprint into working code.

# demo 3-extensions
Let's look at extending out prebuilt line of business assistants. Like agents you can access you assitants in the conversations tab. 

First let me show you how the assistant works out of the box and then we can customize it. 

We will use Financial Closing Assistant  We'll upload our journal entry data and getthe assistnatn to map it and create the journal entry proposal in S/4HANA. 

However, we have custom business rules this agent needs to follow.  

In Joule Studio we can extend this same agent with custom behavior. Select the Jounry entry agent in the catalog and enter your prompt.

Let's customize the agent by adding a check if any amount exceeds €45 and asks for your approval, the agent will also flag anything unusual.

Afterward, Joule Studio goes through the same intent based development process as I showed before. 

Once created, you can see that these new capabilites have been added to our Joule assistnat  




# demo 4-n8n

Here we are in the n8n visual canvas embedded in Joule Studio.

What is really powerful with n8n is that it connects your workflows with your agents to work together

We can take our invoice agent we made earlier and make it more powerful by building out an end to end blocked invoive processs 

Let me walkthrough this example: n8n has prebuilt connectors that pull a list of blocked invoices from S/4HANA. 

Then we bring our invoice agent to auto approve invoics or send to the account payable team to take a closer look

They can review the invoice in SAP Task Center and approve or reject it with a single click and the decision is written back your cloud erp. 

Instead of isolated processes and agents. 
n8n provides one place to orchestrate both agentic and traditional, deterministic automations 

# demo 5-goverance 

AI Agent Hub is where you get to see all your agents, models, and MCP servers in one place. Here, we can dig into our tarriff supply chain agent. 

It makes it easy to can manage the ai agent lifecycle and enforance your governance. 

Once your agent is deployed, you can track what actions your agents are doing and how well they are performing.

So you can learning and keep improving on your agents 






