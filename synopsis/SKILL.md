---
name: synopsis
description: Generate a manager-focused synopsis explaining recent work at multiple levels
---

# Synopsis Skill

Generate a **manager-focused synopsis** that explains the most recent work clearly. Written for an intelligent person who isn't deep in the technical details but wants to understand what happened and why it matters.

## Trigger Phrases

- "show synopsis" - Display in A2UI panel
- "synopsis" - Display in A2UI panel
- "show status" - Display in A2UI panel
- "session summary" - Display in A2UI panel
- "export synopsis" - Display AND save to project folder

## Core Principle

**Pretend you're explaining to your manager.** They're smart but not in the weeds. Lead with:
1. What just happened (the headline)
2. What changed (plain English)
3. Why it matters (impact/value)
4. Technical details (optional, for those who want to dig in)

## Three-Level Structure

| Tab | Purpose | Tone |
|-----|---------|------|
| What Changed | List of changes with clear descriptions | Plain English, action-focused |
| Why It Matters | Business/practical impact | Value-oriented, benefits |
| Technical | Code details, files, implementation | For devs who want specifics |

## Writing Guidelines

### DO:
- Lead with the most recent task as a hero banner
- Use plain English: "Fixed the save button" not "Resolved HTTP/HTTPS protocol mismatch"
- Show impact with arrows: "→ Now works on mobile"
- Keep each item to 1-2 sentences
- Group related changes together

### DON'T:
- Start with old context or project overview
- Use jargon without explanation
- List files without saying what changed
- Assume reader knows the codebase
- Bury the current task under history

## Execution Steps

### Step 1: Identify Current Task

What did we JUST do? This is the hero. Pull from:
- Current conversation (most recent work)
- What the user asked for
- What was actually implemented

### Step 2: Gather Supporting Context

```bash
cat <project>/.claude/CONTEXT.md 2>/dev/null
git status --short
git log --oneline -3
```

### Step 3: Discover Active Terminal

```bash
python3 << 'PY'
import json, urllib.request
data = json.loads(urllib.request.urlopen("http://localhost:7690/api/projects").read())
active_proj_id = data.get('activeProjectId')
for p in data.get('projects', []):
    if p.get('id') == active_proj_id:
        term_id = p.get('activeTerminalId')
        for t in p.get('terminals', []):
            if t.get('id') == term_id:
                print(f"TERMINAL_ID={term_id}")
                print(f"A2UI_LOG=/home/yousuf/GoogleDrive/PROJECTS/.triclaude/runtime/terminals/{term_id}/a2ui_input.log")
PY
```

### Step 4: Generate Synopsis HTML

```bash
cat << 'A2UI_EOF' >> $A2UI_LOG
<!-- A2UI:START -->
<!DOCTYPE html>
<html>
<head>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;color:#e2e8f0;font-family:system-ui;font-size:12px;padding:16px;line-height:1.5}
.hero{background:linear-gradient(135deg,#1e3a5f,#0f172a);padding:16px;border-radius:10px;border-left:4px solid #3b82f6;margin-bottom:16px}
.hero h1{font-size:15px;color:#f8fafc;margin-bottom:8px}
.hero p{color:#94a3b8;font-size:13px}
.status{display:inline-block;padding:3px 10px;border-radius:12px;font-size:10px;font-weight:600;margin-bottom:8px}
.status.done{background:#22c55e;color:#0f172a}
.status.active{background:#f59e0b;color:#0f172a}
.status.blocked{background:#ef4444;color:#fff}
.tabs{display:flex;gap:6px;margin-bottom:14px}
.tab{padding:8px 14px;border-radius:6px;cursor:pointer;font-size:11px;font-weight:500;background:#1e293b;color:#94a3b8;border:none;transition:all 0.2s}
.tab:hover{background:#334155}
.tab.active{background:#3b82f6;color:#fff}
.content{display:none}
.content.active{display:block}
.section{background:#1e293b;border-radius:8px;padding:14px;margin-bottom:12px}
.section h2{font-size:11px;color:#94a3b8;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;display:flex;align-items:center;gap:8px}
.section h2 span{font-size:14px}
.item{padding:10px 12px;background:#0f172a;border-radius:6px;margin-bottom:8px}
.item:last-child{margin-bottom:0}
.item-title{font-weight:600;color:#f8fafc;margin-bottom:4px}
.item-desc{color:#94a3b8;font-size:11px}
.impact{color:#4ade80;font-size:11px;margin-top:6px}
.tech{font-family:monospace;font-size:10px;color:#64748b;background:#1e293b;padding:2px 6px;border-radius:3px}
.pending{border-left:3px solid #f59e0b}
.export-btn{width:100%;margin-top:12px;padding:12px;background:#f59e0b;color:#0f172a;border:none;border-radius:6px;font-size:11px;font-weight:600;cursor:pointer}
.export-btn:hover{background:#fbbf24}
</style>
</head>
<body>

<!-- HERO: Most recent task, front and center -->
<div class="hero">
<span class="status done">✓ JUST COMPLETED</span>
<!-- Or use: <span class="status active">→ IN PROGRESS</span> -->
<!-- Or use: <span class="status blocked">⚠ BLOCKED</span> -->
<h1>[TASK_HEADLINE]</h1>
<p>[ONE_SENTENCE_SUMMARY - plain English, what did we do and why]</p>
</div>

<div class="tabs">
<div class="tab active" onclick="showTab('what')">What Changed</div>
<div class="tab" onclick="showTab('why')">Why It Matters</div>
<div class="tab" onclick="showTab('details')">Technical</div>
</div>

<!-- TAB 1: What Changed - Plain English -->
<div id="what" class="content active">
<div class="section">
<h2><span>🔧</span> Changes Made</h2>

<div class="item">
<div class="item-title">[CHANGE_1_TITLE]</div>
<div class="item-desc">[Plain English description - what does this do for the user?]</div>
<div class="impact">→ [Practical benefit]</div>
</div>

<div class="item">
<div class="item-title">[CHANGE_2_TITLE]</div>
<div class="item-desc">[Description]</div>
<div class="impact">→ [Benefit]</div>
</div>

</div>

<!-- Show pending items if any -->
<div class="section pending">
<h2><span>📋</span> Still Pending</h2>
<div class="item">
<div class="item-title">[PENDING_ITEM]</div>
<div class="item-desc">[What still needs to be done]</div>
</div>
</div>
</div>

<!-- TAB 2: Why It Matters - Impact/Value -->
<div id="why" class="content">
<div class="section">
<h2><span>💡</span> Why This Matters</h2>

<div class="item">
<div class="item-title">[BENEFIT_1_TITLE]</div>
<div class="item-desc">[Explain the value - what problem does this solve? Who benefits?]</div>
</div>

<div class="item">
<div class="item-title">[BENEFIT_2_TITLE]</div>
<div class="item-desc">[Another angle on the value]</div>
</div>

</div>
</div>

<!-- TAB 3: Technical - For those who want details -->
<div id="details" class="content">
<div class="section">
<h2><span>⚙️</span> Technical Details</h2>

<div class="item">
<div class="item-title">Files Modified</div>
<div class="item-desc"><span class="tech">[file1.ts]</span> <span class="tech">[file2.py]</span></div>
</div>

<div class="item">
<div class="item-title">What Was Wrong</div>
<div class="item-desc">[Root cause in technical terms]</div>
</div>

<div class="item">
<div class="item-title">How It Was Fixed</div>
<div class="item-desc">[Technical solution - function names, approach]</div>
</div>

</div>
</div>

<button class="export-btn" onclick="exportSynopsis()">📥 Save This Synopsis</button>

<script>
function showTab(id) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.content').forEach(c => c.classList.remove('active'));
  event.target.classList.add('active');
  document.getElementById(id).classList.add('active');
}

function getApiUrl() {
  try {
    const p = window.parent.location;
    return p.protocol === 'https:'
      ? p.protocol + '//' + p.host + '/api/save-synopsis'
      : 'http://' + p.hostname + ':7690/api/save-synopsis';
  } catch(e) { return 'http://localhost:7690/api/save-synopsis'; }
}

async function exportSynopsis() {
  const btn = document.querySelector('.export-btn');
  btn.textContent = 'Saving...'; btn.disabled = true;
  try {
    const res = await fetch(getApiUrl(), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ projectPath: '[PROJECT_PATH]', html: document.documentElement.outerHTML })
    });
    const data = await res.json();
    btn.textContent = data.success ? '✓ Saved!' : 'Error: ' + (data.error || 'failed');
    btn.style.background = data.success ? '#22c55e' : '#ef4444';
  } catch (e) {
    btn.textContent = 'Error: ' + e.message;
    btn.style.background = '#ef4444';
  }
  setTimeout(() => { btn.textContent = '📥 Save This Synopsis'; btn.style.background = '#f59e0b'; btn.disabled = false; }, 3000);
}
</script>
</body>
</html>
<!-- A2UI:END -->
A2UI_EOF
```

## Example: Good vs Bad

### BAD (old style):
```
Project: TriClaude
Status: Complete
Files Changed:
- src/services/consigliereService.ts
- skills/synopsis/SKILL.md
Recent Commits: 6be15c3, 5e91989
```
*Problem: Doesn't tell me what happened or why I should care*

### GOOD (new style):
```
✓ JUST COMPLETED
Fixed Synopsis Export Button

The export button was failing on HTTPS. Updated it to
detect the connection type and route correctly.

What Changed:
• Smart URL Detection
  Button now works on both localhost and mobile
  → Export works everywhere now

Why It Matters:
• Mobile Access Fixed
  When accessing from phone via Tailscale, export was broken
```
*Better: I know what happened, what changed, and why it matters*

## Export Location

Synopses save to:
```
<project>/.claude/synopses/synopsis_YYYYMMDD_HHMMSS.html
```

## HTTPS Note

The `getApiUrl()` function handles both:
- **HTTP** (localhost:3001): Direct call to port 7690
- **HTTPS** (Tailscale:3443): Routes through Caddy proxy at `/api/*`
