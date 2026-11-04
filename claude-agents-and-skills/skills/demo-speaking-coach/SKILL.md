---
name: demo-speaking-coach
description: Produces a speaking coach document for a Joule Studio demo script. Takes a completed demo script and generates line-by-line delivery notes — pause points, pacing, tone, rhythm, and energy cues — saved as a separate Word document alongside the script. Use when the user wants delivery coaching, presentation tips, or a rehearsal guide for their demo.
metadata:
  version: 1.0.0
  author: tc
---

# Demo Speaking Coach

This skill reads a completed Joule Studio demo script and produces a separate speaking coach document with line-by-line delivery notes. The output is a rehearsal guide — not a rewrite of the script.

---

## Step 1 — Gather inputs

Ask the user for:
1. **Script file path** — the .docx demo script to coach
2. **Output path** — where to save the coaching document (default: same folder as the script)

If the user already provided these, skip asking and proceed.

---

## Step 2 — Read the script

Read the script file and extract every VO line row by row. Note:
- The opening hook
- Transition lines between sections
- Any lines describing a feature or benefit
- The closing outro

---

## Step 3 — Generate delivery notes

For each VO row, write a coaching note using the categories below. Keep each note to 1–3 short lines. Be specific and direct — write like a coach talking to a presenter, not a narrator describing them.

### Delivery note categories

**Pace**
- SLOW DOWN — use for complex ideas, key claims, or moments where the audience needs to absorb something
- SPEED UP — use for transitional filler or setup lines that don't carry weight
- STEADY — normal conversational pace

**Pause**
- PAUSE BEFORE — build anticipation before a big claim or reveal
- PAUSE AFTER — let a key point land before moving on
- NO PAUSE — keep momentum, don't let energy drop

**Tone**
- CONFIDENT — declarative, no upspeak, own the claim
- CONVERSATIONAL — warm, like you're talking to one person
- CURIOUS — lean in, like you're discovering something together with the audience
- URGENT — this matters, convey stakes
- LIGHT — easy, almost throw it away, don't oversell

**Energy**
- BUILD — energy increases through this line toward a payoff
- PEAK — this is the highest energy moment in this section, commit to it
- RELEASE — after a peak, drop energy slightly to give the audience a breath
- FLAT — deliberately understated for contrast

**Rhythm note** (optional, use when a line has a specific spoken cadence worth calling out)
- e.g. "Three short punchy sentences — hit each one separately, don't rush through them as one thought"
- e.g. "The comma is a breath, not a stop — keep it moving"

---

## Step 4 — Write the coaching document

Produce a Word document with a table. Three columns:

| VO (excerpt) | Delivery Notes | Why |
|---|---|---|

- **VO (excerpt)** — first 10–15 words of the line so the presenter can find it quickly
- **Delivery Notes** — pace + pause + tone + energy in short punchy lines
- **Why** — one sentence on why this delivery choice helps the demo land

### Section headers
Add a row before each demo section (Opening, IBD, Code/Deploy, Governance, Closing) as a shaded header row so the presenter can navigate the document during rehearsal.

### Overall pacing summary
At the top of the document, include a short paragraph (3–5 sentences) summarizing:
- The overall energy arc of the demo (where it builds, where it peaks, where it releases)
- The one or two moments that must land perfectly
- The most common mistake to avoid for this specific script

---

## Step 5 — Save and confirm

Save the file as `[original-script-name]-speaking-coach.docx` in the same folder as the script unless the user specified otherwise.

Tell the user:
- Where the file was saved
- How many VO rows were coached
- The top two delivery tips for this specific script

---

## Style rules for coaching notes

- Write in second person: "Slow down here", "Don't rush this", "Own this line"
- Be direct and specific — "SLOW DOWN, this is the key claim" beats "consider a slower pace"
- Never repeat the same note more than three times in a row — vary the coaching
- Flag the two or three most important moments in the whole script with ⭐ so the presenter knows where to focus rehearsal energy
- Do not rewrite or suggest changes to the VO — only coach the delivery of what's written
