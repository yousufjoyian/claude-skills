---
name: synopsis
description: Generate a three-level synopsis with task, project, and roadmap views
---

# Synopsis Skill

Generate a **three-level synopsis** with tabbed navigation for task tracking, project overview, and roadmap.

## Trigger Phrases

- "show synopsis" - Display in A2UI panel only
- "synopsis" - Display in A2UI panel only
- "show status" - Display in A2UI panel only
- "session summary" - Display in A2UI panel only
- "export synopsis" - Display in A2UI AND save to project folder

## Export Location

Synopses are saved with unique timestamps (never overwritten):
```
<project>/.claude/synopses/synopsis_YYYYMMDD_HHMMSS.html
<project>/.claude/synopses/latest.html  (copy of most recent)
```

## Three-Level Structure

| Level | Button | Content |
|-------|--------|---------|
| 1. Current Task | 🎯 Task | What we're working on NOW - active feature, progress, blockers |
| 2. Project Overview | 📋 Project | Full project context - phases, architecture, components |
| 3. Roadmap | 🚀 Roadmap | Where the app is headed - vision, upcoming features |

## Feature States

| State | Icon | Color | Description |
|-------|------|-------|-------------|
| Planning | 📋 | Blue | Designing/researching |
| In Progress | 🔨 | Yellow | Actively coding |
| Testing | 🧪 | Purple | Verifying/debugging |
| Complete | ✅ | Green | Done, committed |
| Blocked | 🚫 | Red | Waiting on dependency |

## Content Guidelines

### Level 1: Current Task
- Active feature name and state
- Session progress (completed/active/pending)
- Files changed this session
- Key decisions made
- Blockers if any

### Level 2: Project Overview
- Project description and purpose
- Tech stack
- Development phases with status
- Key components/architecture
- Recent commits

### Level 3: Roadmap
- Project vision
- Upcoming features (prioritized)
- Long-term goals
- Known limitations to address

## Execution Steps

### Step 1: Gather Context

Read context files:
```bash
cat <project>/.claude/CONTEXT.md 2>/dev/null || echo "No context file"
cat <project>/.claude/reference/PROJECT.md 2>/dev/null || echo "No project file"
```

Check recent git changes:
```bash
git status --short
git log --oneline -5
```

### Step 2: Discover Active Terminal (CRITICAL)

**DO NOT use hardcoded terminal paths.** Query the API:

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
                print(f"SIDECAR_PORT={t.get('sidecarPort')}")
                print(f"A2UI_LOG=/home/yousuf/GoogleDrive/PROJECTS/.triclaude/runtime/terminals/{term_id}/a2ui_input.log")
PY
```

### Step 3: Verify Sidecar Running

```bash
ss -tlnp | grep <sidecarPort>
```

If NOT running, start it:
```bash
cd ~/GoogleDrive/PROJECTS/APPS/TriClaude/scripts
nohup python3 a2ui_sidecar.py --port <sidecarPort> --log <A2UI_LOG> > /tmp/sidecar_<sidecarPort>.log 2>&1 &
```

### Step 4: Generate Three-Level Synopsis HTML

```bash
cat << 'A2UI_EOF' >> $A2UI_LOG
<!-- A2UI:START -->
<!DOCTYPE html>
<html>
<head>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;color:#e2e8f0;font-family:system-ui;font-size:11px;padding:0}
.header{padding:12px 14px;border-bottom:1px solid #334155}
h1{font-size:14px;color:#f8fafc;margin-bottom:4px}
.ts{font-size:10px;color:#64748b}
.tabs{display:flex;gap:6px;padding:10px 14px;background:#1e293b;border-bottom:1px solid #334155}
.tab{padding:8px 14px;border-radius:6px;cursor:pointer;font-size:11px;font-weight:500;background:#0f172a;color:#94a3b8;border:1px solid #334155;transition:all 0.2s}
.tab:hover{background:#334155;color:#e2e8f0}
.tab.active{background:#3b82f6;color:#fff;border-color:#3b82f6}
.content{padding:14px;display:none;overflow-y:auto;max-height:calc(100vh - 120px)}
.content.active{display:block}
.sec{margin-bottom:14px}
.sec-t{font-size:10px;color:#94a3b8;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px}
.card{background:#1e293b;border:1px solid #334155;border-radius:8px;padding:10px}
.row{display:flex;align-items:center;gap:8px;padding:5px 0;border-bottom:1px solid #334155}
.row:last-child{border:none}
.done{color:#4ade80}
.act{color:#fbbf24}
.pend{color:#64748b}
.file{font-family:monospace;font-size:10px;color:#22d3ee;background:#0f172a;padding:3px 6px;border-radius:4px;margin:3px 0;display:block}
.dec{padding:6px 8px;border-left:3px solid #8b5cf6;background:#1e1b4b;margin:4px 0;font-size:11px}
.badge{background:#166534;color:#4ade80;padding:3px 8px;border-radius:10px;font-family:monospace;font-size:10px;display:inline-block;margin:2px 4px 2px 0}
.phase{padding:8px 10px;border-radius:6px;margin-bottom:6px;display:flex;align-items:center;gap:8px}
.phase.done{background:#14532d;border-left:3px solid #22c55e}
.phase.active{background:#1e3a5f;border-left:3px solid #3b82f6}
.phase.pending{background:#1e293b;border-left:3px solid #475569}
.roadmap-item{padding:10px;background:#1e293b;border-radius:6px;margin-bottom:8px;border-left:3px solid #f59e0b}
.roadmap-item.next{border-left-color:#22c55e}
.roadmap-item.future{border-left-color:#8b5cf6}
.priority{font-size:9px;padding:2px 6px;border-radius:4px;margin-left:auto}
.priority.high{background:#7f1d1d;color:#fca5a5}
.priority.med{background:#78350f;color:#fcd34d}
.priority.low{background:#1e3a5f;color:#93c5fd}
.vision{background:linear-gradient(135deg,#1e1b4b,#0f172a);padding:12px;border-radius:8px;border:1px solid #4c1d95;margin-bottom:14px}
.vision-title{color:#a78bfa;font-size:12px;font-weight:600;margin-bottom:6px}
</style>
</head>
<body>

<div class="header">
<h1>[PROJECT] | [FEATURE_NAME]</h1>
<div class="ts">[STATE_ICON] [STATE] · [TIMESTAMP]</div>
</div>

<div class="tabs">
<div class="tab active" onclick="showTab('task')">🎯 Task</div>
<div class="tab" onclick="showTab('project')">📋 Project</div>
<div class="tab" onclick="showTab('roadmap')">🚀 Roadmap</div>
</div>

<!-- LEVEL 1: CURRENT TASK -->
<div id="task" class="content active">
<div class="sec">
<div class="sec-t">Current Focus</div>
<div class="card">[CURRENT_TASK_DESCRIPTION]</div>
</div>

<div class="sec">
<div class="sec-t">Session Progress</div>
<div class="card">
<div class="row"><span class="done">✓</span> [COMPLETED_TASK]</div>
<div class="row"><span class="act">→</span> [ACTIVE_TASK]</div>
<div class="row"><span class="pend">○</span> [PENDING_TASK]</div>
</div>
</div>

<div class="sec">
<div class="sec-t">Files Changed</div>
<div class="card">
<span class="file">[FILE_PATH] - [DESCRIPTION]</span>
</div>
</div>

<div class="sec">
<div class="sec-t">Key Decisions</div>
<div class="card">
<div class="dec">[DECISION]</div>
</div>
</div>

<button id="exportBtn" onclick="exportSynopsis()" style="
  width:100%;margin-top:8px;padding:10px;background:#f59e0b;color:#0f172a;
  border:none;border-radius:6px;font-size:11px;font-weight:600;cursor:pointer;
">📥 Export Synopsis</button>
</div>

<!-- LEVEL 2: PROJECT OVERVIEW -->
<div id="project" class="content">
<div class="sec">
<div class="sec-t">About</div>
<div class="card">[PROJECT_DESCRIPTION]<br><br><strong>Stack:</strong> [TECH_STACK]</div>
</div>

<div class="sec">
<div class="sec-t">Development Phases</div>
<div class="phase done"><span class="done">✓</span> [COMPLETED_PHASE]</div>
<div class="phase active"><span class="act">→</span> [ACTIVE_PHASE]</div>
<div class="phase pending"><span class="pend">○</span> [PENDING_PHASE]</div>
</div>

<div class="sec">
<div class="sec-t">Key Components</div>
<div class="card">
<div class="row">[COMPONENT_1]</div>
<div class="row">[COMPONENT_2]</div>
<div class="row">[COMPONENT_3]</div>
</div>
</div>

<div class="sec">
<div class="sec-t">Recent Commits</div>
<div class="card">
<span class="badge">[HASH1]</span> [MSG1]<br>
<span class="badge">[HASH2]</span> [MSG2]<br>
<span class="badge">[HASH3]</span> [MSG3]
</div>
</div>
</div>

<!-- LEVEL 3: ROADMAP -->
<div id="roadmap" class="content">
<div class="vision">
<div class="vision-title">🎯 Vision</div>
[PROJECT_VISION]
</div>

<div class="sec">
<div class="sec-t">Up Next</div>
<div class="roadmap-item next">
<div><strong>[NEXT_FEATURE]</strong><br><span style="color:#94a3b8">[NEXT_DESCRIPTION]</span></div>
<span class="priority high">High</span>
</div>
</div>

<div class="sec">
<div class="sec-t">Upcoming</div>
<div class="roadmap-item">
<div><strong>[UPCOMING_1]</strong><br><span style="color:#94a3b8">[UPCOMING_1_DESC]</span></div>
<span class="priority med">Medium</span>
</div>
<div class="roadmap-item future">
<div><strong>[UPCOMING_2]</strong><br><span style="color:#94a3b8">[UPCOMING_2_DESC]</span></div>
<span class="priority low">Low</span>
</div>
</div>

<div class="sec">
<div class="sec-t">Known Limitations</div>
<div class="card">
<div class="row"><span style="color:#f87171">!</span> [LIMITATION_1]</div>
<div class="row"><span style="color:#f87171">!</span> [LIMITATION_2]</div>
</div>
</div>
</div>

<script>
function showTab(id) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.content').forEach(c => c.classList.remove('active'));
  document.querySelector('.tab[onclick*="'+id+'"]').classList.add('active');
  document.getElementById(id).classList.add('active');
}

async function exportSynopsis() {
  const btn = document.getElementById('exportBtn');
  btn.textContent = 'Saving...';
  btn.disabled = true;
  try {
    const res = await fetch('http://' + location.hostname + ':7690/api/save-synopsis', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ projectPath: '[PROJECT_PATH]', html: document.documentElement.outerHTML })
    });
    const data = await res.json();
    btn.textContent = data.success ? '✓ Saved!' : 'Error';
    btn.style.background = data.success ? '#22c55e' : '#ef4444';
  } catch (e) {
    btn.textContent = 'Error';
    btn.style.background = '#ef4444';
  }
  setTimeout(() => {
    btn.textContent = '📥 Export Synopsis';
    btn.style.background = '#f59e0b';
    btn.disabled = false;
  }, 2000);
}
</script>
</body>
</html>
<!-- A2UI:END -->
A2UI_EOF
```

## Filling In Content

### Level 1 (Task) - Pull from:
- Current conversation context
- CONTEXT.md "Status" and "Changed" sections
- Git status for modified files
- Session decisions

### Level 2 (Project) - Pull from:
- PROJECT.md or CONTEXT.md "Project Overview"
- ARCHITECTURE.md if exists
- Package.json for stack info
- Git log for recent commits

### Level 3 (Roadmap) - Pull from:
- PROJECT.md "Roadmap" or "Future" sections
- TODO.md if exists
- GitHub issues if accessible
- User's stated goals from conversation

## HTTPS/Tailscale Note

When accessing via HTTPS (e.g., `https://100.102.109.74:3443/`):
- Browser connects to `wss://host:(sidecarPort + 1000)`
- WSS proxy (wss-proxy.cjs) must be running
- Proxy forwards 8897 → 7897, 8899 → 7899, etc.

## Export Button (Optional)

Add to header for saving:

```html
<button id="exportBtn" onclick="exportSynopsis()" style="
  position:absolute;top:12px;right:12px;background:#f59e0b;color:#0f172a;
  border:none;padding:6px 10px;border-radius:4px;font-size:10px;font-weight:bold;cursor:pointer;
">Export</button>
```

## Key Guidelines

1. **Always discover active terminal** - Never use hardcoded paths
2. **Verify sidecar running** - Start if needed before sending
3. **Default to Task tab** - Most relevant for active work
4. **Keep each level focused** - Don't duplicate content across tabs
5. **Use actual data** - Pull from CONTEXT.md, PROJECT.md, git, conversation
6. **Roadmap from PROJECT.md** - Or ask user if not documented

## Troubleshooting

**Synopsis not appearing:**
1. Check active terminal: `curl -s http://localhost:7690/api/projects`
2. Verify sidecar: `ss -tlnp | grep <sidecarPort>`
3. Check WSS proxy log: `tail ~/dev/cache/triclaude/wss-proxy.log`
4. For HTTPS: ensure WSS proxy running on sidecarPort + 1000
