# Save Context Skill

**Triggers:** "save context", "save session", "handoff", "end session"

## Purpose

Save current work state to `.claude/CONTEXT.md` by **MERGING** with existing context, not overwriting. Preserves project-level information while updating session-specific work.

## Output File

```
<project>/.claude/CONTEXT.md
```

## CRITICAL: Merge, Don't Overwrite

**NEVER** start from scratch. Always:
1. READ existing CONTEXT.md first
2. PRESERVE project-level sections (Goal, Project Overview, Key Components)
3. UPDATE session-specific sections (Recent Work, Changed This Session)
4. APPEND new decisions to existing ones

## Format (Strict Template)

```markdown
# <project> | YYYY-MM-DD HH:MM

## Goal
[Project's main purpose - preserve from existing unless project changed]

## Project Overview
[Brief description - preserve from existing, only update if fundamentally changed]
See `.claude/reference/PROJECT.md` for full architecture.

## Key Components
[Major parts of project - preserve from existing, add new components only]

## Recent Work (This Session)
- [x] Completed task from THIS session
- [→] Active: current task
- [ ] Next: upcoming task

## Changed This Session
- `path/file.ts` - what changed
- `path/new-file.ts` - NEW: purpose

## Key Decisions
[APPEND to existing decisions, don't replace]
- New decision: rationale (date if helpful)

## Blocked
- Issue → workaround
- [none] if no blockers

## Resume
Specific actionable next steps. 2-3 sentences max.
```

**CRITICAL:** The timestamp (YYYY-MM-DD HH:MM) determines which files need review on next session start.

## Protocol

### Step 1: Read Existing Context

```bash
cd ~/local_workspaces/<project>

# ALWAYS read existing context first
cat .claude/CONTEXT.md 2>/dev/null
```

**Extract and preserve:**
- Goal (unless project fundamentally changed)
- Project Overview section
- Key Components section
- Existing Key Decisions (append new ones)

### Step 2: Gather Session Information

```bash
# Check what changed THIS session
git status
git diff --stat

# Recent commits
git log --oneline -5
```

### Step 3: Archive Previous Context

```bash
mkdir -p ~/local_workspaces/<project>/.claude/history

if [ -f ~/local_workspaces/<project>/.claude/CONTEXT.md ]; then
    cp ~/local_workspaces/<project>/.claude/CONTEXT.md \
       ~/local_workspaces/<project>/.claude/history/$(date +%Y-%m-%d_%H%M).md
fi
```

### Step 4: Generate Merged CONTEXT.md

**DO:**
- Keep existing Goal, Project Overview, Key Components
- Replace "Recent Work" with THIS session's work only
- Replace "Changed This Session" with THIS session's changes
- APPEND new decisions to Key Decisions
- Update Resume with current next steps
- Update timestamp

**DON'T:**
- Delete project-level context
- Lose historical decisions
- Narrow scope to just current task

### Step 5: Confirm

```
Context saved: <project>/.claude/CONTEXT.md

Preserved:
- Goal: [goal]
- Project Overview: [kept/updated]
- Key Components: [count] items
- Existing Decisions: [count] preserved

Updated:
- Recent Work: [count] items from this session
- Changed: [count] files
- New Decisions: [count] added

Previous context archived to: .claude/history/YYYY-MM-DD_HHMM.md
```

### Step 6: Visualize Save (A2UI)

**ALWAYS send A2UI visualization after saving context.** Shows what was preserved and updated.

#### 6a. Discover Active Terminal

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
                print(f"A2UI_LOG=/home/yousuf/GoogleDrive/PROJECTS/.triclaude/runtime/terminals/{term_id}/a2ui_input.log")
PY
```

#### 6b. Generate A2UI Visualization

**Two-tab view:**
- **This Session**: What was updated in the current save
- **Full Context**: Complete accumulated project context

```bash
cat << 'A2UI_EOF' >> $A2UI_LOG
<!-- A2UI:START -->
<!DOCTYPE html>
<html>
<head>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;color:#e2e8f0;font-family:system-ui;font-size:11px;padding:0}
.header{padding:12px 14px;border-bottom:1px solid #334155;display:flex;align-items:center;gap:10px}
.icon{font-size:20px}
h1{font-size:14px;color:#f8fafc}
.badge{background:#166534;color:#4ade80;padding:4px 10px;border-radius:12px;font-size:10px;font-weight:600;margin-left:auto}
.tabs{display:flex;gap:6px;padding:10px 14px;background:#1e293b;border-bottom:1px solid #334155}
.tab{padding:8px 14px;border-radius:6px;cursor:pointer;font-size:11px;font-weight:500;background:#0f172a;color:#94a3b8;border:1px solid #334155;transition:all 0.2s}
.tab:hover{background:#334155;color:#e2e8f0}
.tab.active{background:#3b82f6;color:#fff;border-color:#3b82f6}
.content{padding:14px;display:none;overflow-y:auto;max-height:calc(100vh - 140px)}
.content.active{display:block}
.card{background:#1e293b;border:1px solid #334155;border-radius:8px;padding:12px;margin-bottom:12px}
.label{font-size:9px;color:#64748b;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px}
.goal{color:#f8fafc;font-size:12px;font-weight:500}
.item{display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid #334155}
.item:last-child{border:none}
.done{color:#4ade80}
.active-item{color:#fbbf24}
.pending{color:#64748b}
.file{font-family:monospace;font-size:10px;color:#a78bfa;padding:3px 0}
.decision{padding:6px 8px;border-left:3px solid #8b5cf6;background:#1e1b4b;margin:4px 0;font-size:10px}
.stats{display:flex;gap:12px;flex-wrap:wrap}
.stat{background:#0f172a;padding:6px 10px;border-radius:6px;text-align:center}
.stat-val{font-size:14px;font-weight:600;color:#60a5fa}
.stat-label{font-size:9px;color:#64748b;margin-top:2px}
.resume{background:#14532d;border:1px solid #22c55e;border-radius:6px;padding:10px;color:#86efac;font-size:11px}
.component{padding:8px;background:#0f172a;border-radius:6px;margin:4px 0}
.comp-name{color:#22d3ee;font-weight:500}
.comp-desc{color:#94a3b8;font-size:10px}
.ts{color:#64748b;font-size:10px;margin-top:12px;text-align:center}
.buttons{display:flex;gap:8px;padding:14px}
.btn{flex:1;padding:10px;border:none;border-radius:6px;font-size:11px;font-weight:600;cursor:pointer}
.btn-session{background:#8b5cf6;color:#fff}
.btn-full{background:#f59e0b;color:#0f172a}
</style>
</head>
<body>

<div class="header">
<span class="icon">💾</span>
<h1>Context Saved</h1>
<span class="badge">✓ Merged</span>
</div>

<div class="tabs">
<div class="tab active" onclick="showTab('session')">📝 This Session</div>
<div class="tab" onclick="showTab('full')">📚 Full Context</div>
</div>

<!-- TAB 1: THIS SESSION -->
<div id="session" class="content active">
<div class="card">
<div class="label">What Changed</div>
<div class="goal">[SESSION_SUMMARY]</div>
</div>

<div class="card">
<div class="label">Tasks Completed</div>
[SESSION_WORK_ITEMS]
</div>

<div class="card">
<div class="label">Files Modified</div>
[SESSION_FILES]
</div>

<div class="card">
<div class="label">New Decisions</div>
[SESSION_DECISIONS]
</div>

<div class="card">
<div class="label">Stats</div>
<div class="stats">
<div class="stat"><div class="stat-val">[COMPLETED_COUNT]</div><div class="stat-label">completed</div></div>
<div class="stat"><div class="stat-val">[FILES_COUNT]</div><div class="stat-label">files</div></div>
<div class="stat"><div class="stat-val">[NEW_DECISIONS_COUNT]</div><div class="stat-label">new decisions</div></div>
</div>
</div>
</div>

<!-- TAB 2: FULL CONTEXT -->
<div id="full" class="content">
<div class="card">
<div class="label">Project</div>
<div class="goal">[PROJECT_NAME]</div>
<div style="color:#94a3b8;font-size:10px;margin-top:4px">[GOAL]</div>
</div>

<div class="card">
<div class="label">Key Components</div>
[KEY_COMPONENTS]
</div>

<div class="card">
<div class="label">All Decisions</div>
[ALL_DECISIONS]
</div>

<div class="card">
<div class="label">Resume Instructions</div>
<div class="resume">[RESUME_TEXT]</div>
</div>

<div class="card">
<div class="label">Context History</div>
<div style="color:#94a3b8;font-size:10px">Archived: .claude/history/[ARCHIVE_FILENAME]</div>
</div>
</div>

<div class="ts">[TIMESTAMP]</div>

<div class="buttons">
<button class="btn btn-session" onclick="exportSession()">📝 Export Session</button>
<button class="btn btn-full" onclick="exportFull()">📚 Export Full</button>
</div>

<script>
function showTab(id) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.content').forEach(c => c.classList.remove('active'));
  document.querySelector('.tab[onclick*="'+id+'"]').classList.add('active');
  document.getElementById(id).classList.add('active');
}

function doExport(btn, label) {
  btn.textContent = 'Saving...';
  btn.disabled = true;
  window.parent.postMessage({
    type: 'save-synopsis',
    projectPath: '[PROJECT_PATH]',
    html: document.documentElement.outerHTML
  }, '*');
  window.addEventListener('message', function handler(e) {
    if (e.data?.type === 'save-synopsis-result') {
      window.removeEventListener('message', handler);
      btn.textContent = e.data.success ? '✓ Saved!' : 'Error';
      btn.style.background = e.data.success ? '#22c55e' : '#ef4444';
      setTimeout(() => {
        btn.textContent = label;
        btn.style.background = label.includes('Session') ? '#8b5cf6' : '#f59e0b';
        btn.disabled = false;
      }, 2000);
    }
  });
}

function exportSession() {
  showTab('session');
  setTimeout(() => doExport(event.target, '📝 Export Session'), 100);
}

function exportFull() {
  showTab('full');
  setTimeout(() => doExport(event.target, '📚 Export Full'), 100);
}
</script>

</body>
</html>
<!-- A2UI:END -->
A2UI_EOF
```

**Replace placeholders:**

*This Session tab:*
- `[SESSION_SUMMARY]` → Brief description of what was done
- `[SESSION_WORK_ITEMS]` → Tasks as `<div class="item"><span class="done">✓</span> Task</div>`
- `[SESSION_FILES]` → Files as `<div class="file">path/file.ts - change</div>`
- `[SESSION_DECISIONS]` → New decisions as `<div class="decision">Decision made</div>`
- `[COMPLETED_COUNT]` → Tasks completed this session
- `[FILES_COUNT]` → Files changed this session
- `[NEW_DECISIONS_COUNT]` → Decisions added this session

*Full Context tab:*
- `[PROJECT_NAME]` → Project folder name
- `[GOAL]` → Project goal
- `[KEY_COMPONENTS]` → Components as `<div class="component"><span class="comp-name">Name</span>: <span class="comp-desc">desc</span></div>`
- `[ALL_DECISIONS]` → All decisions as `<div class="decision">Decision</div>`
- `[RESUME_TEXT]` → Resume instructions
- `[ARCHIVE_FILENAME]` → Archived context filename

*Common:*
- `[TIMESTAMP]` → Current time
- `[PROJECT_PATH]` → Absolute path for export

## Example: Merging Context

**Existing CONTEXT.md:**
```markdown
# myproject | 2026-01-17 14:00

## Goal
Build a CLI tool for managing dotfiles

## Project Overview
Cross-platform dotfile manager with backup and sync. See PROJECT.md.

## Key Components
- **CLI**: Python Click at `src/cli/`
- **Sync**: rsync wrapper at `src/sync/`

## Recent Work (This Session)
- [x] Added backup command
- [→] Active: testing restore

## Key Decisions
- Click over argparse (better UX)
- YAML config over JSON (comments allowed)
```

**After saving new session (added restore feature):**
```markdown
# myproject | 2026-01-18 10:30

## Goal
Build a CLI tool for managing dotfiles

## Project Overview
Cross-platform dotfile manager with backup and sync. See PROJECT.md.

## Key Components
- **CLI**: Python Click at `src/cli/`
- **Sync**: rsync wrapper at `src/sync/`
- **Restore**: New restore engine at `src/restore/`

## Recent Work (This Session)
- [x] Implemented restore command
- [x] Added conflict resolution UI
- [→] Active: writing tests for restore

## Changed This Session
- `src/restore/engine.py` - NEW: restore logic
- `src/cli/commands.py` - added restore subcommand
- `tests/test_restore.py` - NEW: restore tests

## Key Decisions
- Click over argparse (better UX)
- YAML config over JSON (comments allowed)
- Interactive conflict resolution over auto-overwrite (safer)

## Blocked
- [none]

## Resume
Restore command implemented with conflict UI. Need to finish tests
in test_restore.py, then update README with restore docs.
```

Notice:
- Goal, Overview preserved exactly
- Key Components got ONE new item added
- Recent Work replaced (only THIS session)
- Key Decisions APPENDED (new decision added)

## What to Preserve vs Replace

| Section | Action |
|---------|--------|
| Goal | PRESERVE (unless project changed) |
| Project Overview | PRESERVE |
| Key Components | PRESERVE + ADD new ones |
| Recent Work | REPLACE (this session only) |
| Changed This Session | REPLACE (this session only) |
| Key Decisions | PRESERVE + APPEND new |
| Blocked | REPLACE (current state) |
| Resume | REPLACE (current next steps) |

## What NOT to Include

- Code snippets (reference files instead)
- Full error messages (summarize)
- Conversation history (just outcomes)
- Speculation about future work
- Work from previous sessions in "Recent Work"
