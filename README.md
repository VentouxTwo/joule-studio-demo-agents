# Joule Studio Demo Script Writer

This is a Claude Code agent that writes live demo scripts for Joule Studio presentations. Instead of starting from scratch before every demo, you describe your persona and industry vertical and the agent generates a structured voiceover script ready for a 10-minute live audience demo.

## What it does

The agent writes in a first-person, conversational presenter voice — short punchy sentences, natural spoken rhythm, nothing that sounds like it was read off a slide. It follows the Joule Studio product tour structure across three sections: Intent-Based Development, Reviewing and Deploying Code, and Governance and Testing.

It also includes a companion skill for generating scripts directly from recorded demo videos. Drop in an .mp4 file and it extracts frames, reads what's on screen, and produces a four-column Word document with timestamps, demo actions, screenshots, and voiceover matched to the recording.

## How to use it

Download the agent file and add it to your `~/.claude/agents/` folder. The skill goes in `~/.claude/skills/lob-demo-script/`. Open Claude Code and tell it:

- **Persona** — who is the main character in the demo story (e.g. a finance controller, an HR business partner, a supply chain manager)
- **Use case** — what business problem are they solving
- **Features** — which Joule Studio features you want to highlight
- **Length** — how long the demo needs to run (e.g. 3 minutes, 10 minutes)
- **Tone** — how you want it to sound (e.g. conversational, technical, executive-level)

The agent handles the rest and outputs a ready-to-use Word document.

## What's in this repo

- `claude-agents-and-skills/agents/js-demo-script-writer.md` — the demo script writer agent
- `claude-agents-and-skills/skills/lob-demo-script/SKILL.md` — the video-to-script skill
- Example scripts, messaging docs, and product reference materials used during script generation
