---
name: lob-demo-script
description: Write a live demo walkthrough script from a recorded demo video. Takes a video file path and an optional use case doc. Extracts frames, reads the screen, and produces a 4-column Word document (Timestamp / Demo Action text / Demo Action screenshot / VO) matching the user's preferred style. Use when the user wants to "write a script from this video", "create a demo script", "match timing to the recording", or "script this demo video".
metadata:
  version: 1.0.0
  author: tc
---

# LoB Demo Script Writer

This skill writes a live presenter demo script by watching a recorded demo video frame by frame and matching VO to what is on screen. Output is a 4-column Word document with timestamps, demo actions, screenshots, and voiceover.

---

## Step 1 — Gather inputs

Ask the user for:
1. **Video file path** — the .mp4 recording of the demo
2. **Use case doc** (optional) — a markdown file describing the product/agent being demo'd
3. **Reference script** (optional) — an existing script to match style and language from
4. **Output path** — where to save the .docx

If the user already provided these in their message, skip asking and proceed.

---

## Step 2 — Extract frames

Run ffmpeg to extract one frame every 30 seconds:

```bash
mkdir -p /tmp/demo_frames
ffmpeg -i "<video_path>" -vf "fps=1/30" /tmp/demo_frames/frame_%04d.jpg -y
```

Then convert all JPEGs to PNG (python-docx cannot read ffmpeg JPEGs directly):

```python
from PIL import Image
import os
os.makedirs('/tmp/demo_frames_png', exist_ok=True)
for i in range(1, <total_frames+1>):
    src = f'/tmp/demo_frames/frame_{i:04d}.jpg'
    dst = f'/tmp/demo_frames_png/frame_{i:04d}.png'
    if os.path.exists(src):
        Image.open(src).save(dst, 'PNG')
```

Check total frame count with:
```bash
ls /tmp/demo_frames/ | wc -l
```

Frame numbering maps directly to timestamps: frame_0001 = 0:00, frame_0002 = 0:30, frame_0003 = 1:00, etc.

---

## Step 3 — Read all frames

Read every frame image using the Read tool before writing any VO. Build a complete picture of the full video flow first. Note:
- What screen/view is shown
- What text is visible in the main panel
- What the AI chat panel says (right side)
- What step of the process is active
- Any significant UI state changes

Group consecutive frames that show the same screen state — these can be consolidated into one row in the output.

---

## Step 4 — Write the script

Write a 4-column Word document table using the style rules below.

### Document format
- **Column 1: Timestamp** — e.g. 0:00, 0:30, 1:00
- **Column 2: Demo Action** — text description of what is on screen and what the presenter does
- **Column 3: Demo Action** — screenshot (leave blank for now, filled in Step 5)
- **Column 4: VO** — what the presenter says out loud

Consolidate rows where multiple frames show the same screen. The user's edited version had ~27 rows from a 42-frame (21-minute) video — aim for that density, not one row per frame.

### VO style rules (learned from user edits)

**Voice**
- First-person conversational: "I", "we", "let me" — not third-person narration
- Casual and natural, like someone talking through a demo live
- Short punchy sentences. Mix with natural spoken rhythm.
- Slightly informal is fine — matches how someone actually speaks on stage

**Opening**
- Name what we are building and the business problem in one punchy line
- Use a relatable everyday analogy for the waste/inefficiency problem (e.g. buying 4 cans of paint but only needing 2)
- Two or three sentences then "let's build it"
- Do NOT start with "Here we are in the Joule Work Browser" — jump straight into the action

**Clarifying questions section**
- One or two sentences max
- Just say it is asking follow-up questions, mention one specific example visible on screen
- Do not over-explain this feature

**PRD section**
- "This is the more detailed version of what we want to build, who it is for, and why we are building it"
- Call out what the agent actually does in plain language (3-4 key steps)
- Mention user personas and feature requirements are visible
- "It is a living document"

**Spec section**
- "The PRD is what we want to build. The spec is how we build it."
- Mention APIs listed, test suite planned
- Keep it to one short paragraph

**Code/file explorer section**
- Walk through what was generated — be specific (name the files, name the MCP servers)
- Call out the custom optimization/business logic as the heart of the solution — the thing that does not exist in SAP out of the box
- Mention prompt injection protection briefly — "protecting the agent from prompts that want to hijack it"
- Mention documentation lives inside the project alongside the code, version-controlled

**Testing section**
- Lead with the result: "X tests. X passed. Zero failures. 100%."
- Explain what those tests validated (optimization engine, approval gate, API connections)
- "That is the confidence you need before this goes anywhere near a production user"

**Deployment section**
- "And we are live. All five assets running."
- Mention managed runtime — no infrastructure to worry about
- Mention preview "Try Your Agent" environment
- Mention Traces and Logs for observability
- Mention identity/auth registration briefly — authorized users only, audit trail
- End with what the full production version could do beyond the MVP

**Wait/loading bridges**
- Use "While that loads, let me explain..." for slow steps
- During long processing waits, use the time to explain the business problem or what is being built and why it matters — don't just say "it's running"
- Vary the phrasing — don't repeat the same bridge too many times

**Closing**
- "That is a quick tour of Joule Studio and how to build useful line of business agents for your teams. Thanks for watching."

**What to avoid**
- No dashes as punctuation in VO
- No long polished paragraphs — the user will trim to match their speaking style
- No over-explaining benefits — one clear sentence beats three
- No "Let me show you a live example" setups — jump straight in
- No estimated duration or target audience header

---

## Step 5 — Insert screenshots

After saving the Word document, insert the PNG frames into Column 3 (Demo Action screenshot) of each row:

```python
import docx
from docx.shared import Inches
import os

doc = docx.Document('<output_path>')
table = doc.tables[0]

# Map rows to frames based on timestamp in column 0
# Row 1 = first data row. Frame number = row index (1-based).
# If rows were consolidated, map each row's timestamp to the nearest frame.
for row_idx in range(1, len(table.rows)):
    timestamp = table.rows[row_idx].cells[0].text.strip()
    # Convert timestamp to frame number: "0:00"=1, "0:30"=2, "1:00"=3, etc.
    if ':' in timestamp:
        parts = timestamp.split(':')
        total_seconds = int(parts[0]) * 60 + int(parts[1])
        frame_num = (total_seconds // 30) + 1
        frame_path = f'/tmp/demo_frames_png/frame_{frame_num:04d}.png'
        if os.path.exists(frame_path):
            cell = table.rows[row_idx].cells[2]  # Column 3 = screenshot column
            p = cell.add_paragraph()
            run = p.add_run()
            run.add_picture(frame_path, width=Inches(2.8))

doc.save('<output_path>')
```

---

## Step 6 — Confirm output

Tell the user:
- Where the file was saved
- How many rows / what timestamps were covered
- Any frames that were skipped or consolidated

---

## Notes

- The js-demo-script-writer agent produces a different format (two columns, no screenshots). Use THIS skill instead when the user has a video recording and wants frame-matched screenshots in the output.
- Always read ALL frames before writing VO — do not write section by section.
- If the video is very long (30+ minutes), extract at 1 frame per 60 seconds instead to keep it manageable.
- Keep the PNG frames in /tmp — they do not need to be saved permanently.
