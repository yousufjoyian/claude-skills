---
name: synopsis
description: Generate a feature-focused synopsis for tracking and documentation
---

# Synopsis Skill

Generate a **feature-focused** synopsis that serves as lightweight feature management and documentation.

## Trigger Phrases

- "show synopsis" - Display in A2UI panel only
- "synopsis" - Display in A2UI panel only
- "show status" - Display in A2UI panel only
- "session summary" - Display in A2UI panel only
- "export synopsis" - Display in A2UI AND save to project folder

## Naming Convention

**Critical:** Synopsis should be labeled by the FEATURE being worked on, not just "Session Synopsis".

### Title Format
```
[Project] | [Feature Name]
```

Examples:
- `TriClaude | Fullscreen Shortcuts`
- `Tesseract | Voice Commands`
- `API Server | Rate Limiting`

### Export Filename Format
```
synopsis_[feature-slug]_[date].html
```

Examples:
- `synopsis_fullscreen-shortcuts_2026-01-17.html`
- `synopsis_voice-commands_2026-01-17.html`
- `synopsis_rate-limiting_2026-01-17.html`

## Feature States

Track the feature lifecycle with these states:

| State | Icon | Color | Description |
|-------|------|-------|-------------|
| Planning | 📋 | Blue | Designing/researching |
| In Progress | 🔨 | Yellow | Actively coding |
| Testing | 🧪 | Purple | Verifying/debugging |
| Complete | ✅ | Green | Done, committed |
| Blocked | 🚫 | Red | Waiting on dependency |

## What to Include

The synopsis should provide a comprehensive overview at the **feature/objective level**:

### 1. Current Goal
- What is the main objective of this session?
- What problem are we solving?

### 2. Progress Status
- What has been completed?
- What is currently in progress?
- What is remaining?

### 3. Key Decisions Made
- Important architectural or design decisions
- Trade-offs chosen

### 4. Files Changed
- List of files modified with brief descriptions
- New files created

### 5. Blockers/Issues
- Any current blockers
- Issues encountered and how they were resolved

### 6. Next Steps
- Immediate next actions
- Future considerations

## Execution Steps

### Step 1: Gather Context

Read the current context file if it exists:
```bash
cat <project>/.claude/CONTEXT.md 2>/dev/null || echo "No context file"
```

Check recent git changes:
```bash
git status --short
git log --oneline -5
```

### Step 2: Ensure Sidecar Running

Check sidecar is running (see a2ui-embed skill for details):
```bash
ss -tlnp | grep <sidecarPort>
```

Start if not running.

### Step 3: Generate Synopsis HTML

Write a comprehensive synopsis to the A2UI log. Use this template:

```bash
cat << 'A2UI_EOF' >> $A2UI_LOG
<!-- A2UI:START -->
<!DOCTYPE html>
<html>
<head>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #e2e8f0;
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 12px;
  padding: 16px;
  min-height: 100vh;
}
.header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #f59e0b;
}
.header h1 { font-size: 16px; color: #f59e0b; }
.timestamp { font-size: 10px; color: #64748b; }
.section { margin-bottom: 16px; }
.section-title {
  font-size: 11px;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.card {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 12px;
}
.goal-text { font-size: 14px; color: #f8fafc; line-height: 1.5; }
.status-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 0;
  border-bottom: 1px solid #334155;
}
.status-item:last-child { border-bottom: none; }
.status-done { color: #4ade80; }
.status-progress { color: #fbbf24; }
.status-pending { color: #64748b; }
.file-item {
  font-family: monospace;
  font-size: 11px;
  padding: 4px 8px;
  background: #0f172a;
  border-radius: 4px;
  margin: 4px 0;
  color: #22d3ee;
}
.decision {
  padding: 8px;
  border-left: 3px solid #8b5cf6;
  background: #1e1b4b;
  margin: 6px 0;
}
.next-step {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  background: #0f172a;
  border-radius: 6px;
  margin: 6px 0;
}
.step-num {
  background: #f59e0b;
  color: #0f172a;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 11px;
}
</style>
</head>
<body>
  <div class="header">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2">
      <rect x="3" y="3" width="18" height="18" rx="2"/>
      <path d="M3 9h18M9 21V9"/>
    </svg>
    <div>
      <h1>[PROJECT] | [FEATURE_NAME]</h1>
      <div class="timestamp">[FEATURE_STATE_ICON] [FEATURE_STATE] · [TIMESTAMP]</div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">🎯 Feature Goal</div>
    <div class="card">
      <div class="goal-text">[GOAL_DESCRIPTION]</div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">📊 Progress</div>
    <div class="card">
      <div class="status-item">
        <span class="status-done">✓</span>
        <span>[COMPLETED_TASK_1]</span>
      </div>
      <div class="status-item">
        <span class="status-progress">→</span>
        <span>[IN_PROGRESS_TASK]</span>
      </div>
      <div class="status-item">
        <span class="status-pending">○</span>
        <span>[PENDING_TASK]</span>
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">📁 Files Changed</div>
    <div class="card">
      <div class="file-item">[FILE_PATH] - [DESCRIPTION]</div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">💡 Key Decisions</div>
    <div class="card">
      <div class="decision">[DECISION_DESCRIPTION]</div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">🚀 Next Steps</div>
    <div class="card">
      <div class="next-step">
        <div class="step-num">1</div>
        <span>[NEXT_STEP_1]</span>
      </div>
      <div class="next-step">
        <div class="step-num">2</div>
        <span>[NEXT_STEP_2]</span>
      </div>
    </div>
  </div>
</body>
</html>
<!-- A2UI:END -->
A2UI_EOF
```

## Export Button in Synopsis HTML

The synopsis HTML should include an export button that saves to the project folder via API.

Add this button and script to the HTML header section:

```html
<button id="exportBtn" onclick="exportSynopsis()" style="
  position: fixed;
  top: 12px;
  right: 12px;
  background: #f59e0b;
  color: #0f172a;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
">
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>
  </svg>
  Export
</button>

<script>
async function exportSynopsis() {
  const btn = document.getElementById('exportBtn');
  btn.textContent = 'Saving...';
  try {
    const html = document.documentElement.outerHTML;
    const res = await fetch('http://' + location.hostname + ':7690/api/save-synopsis', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        projectPath: '[PROJECT_PATH]',  // Replace with actual project path
        html: html
      })
    });
    const data = await res.json();
    if (data.success) {
      btn.textContent = '✓ Saved';
      btn.style.background = '#4ade80';
    } else {
      btn.textContent = 'Error';
      btn.style.background = '#ef4444';
    }
  } catch (e) {
    btn.textContent = 'Error';
    btn.style.background = '#ef4444';
  }
  setTimeout(() => {
    btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg> Export';
    btn.style.background = '#f59e0b';
  }, 2000);
}
</script>
```

**Important:** Replace `[PROJECT_PATH]` with the actual project path (e.g., `/home/yousuf/local_workspaces/triclaude`)

## Key Guidelines

1. **Name by feature** - Title should identify the feature, not just "Session Synopsis"
2. **Track feature state** - Always show Planning/In Progress/Testing/Complete/Blocked
3. **Be comprehensive** - Include all sections, even if some are brief
4. **Use actual data** - Pull from CONTEXT.md, git status, and conversation context
5. **Keep it scannable** - Use icons, colors, and clear hierarchy
6. **Timestamp it** - Always include when the synopsis was generated
7. **Export with feature name** - Filename should include feature slug

## Export File Location

When exporting, save to:
```
<project>/.claude/synopsis_[feature-slug]_[date].html
```

Also keep a `synopsis.html` symlink or copy pointing to the latest export for quick access.

## Example Output Structure

```
[Project] | [Feature Name]
✅ Complete · 2026-01-17
├── Feature Goal: [What this feature does]
├── Progress
│   ├── ✓ Completed: [List]
│   ├── → In Progress: [Current]
│   └── ○ Pending: [Remaining]
├── Files Changed
│   └── [file:line] - [what changed]
├── Key Decisions
│   └── [Decision with rationale]
└── Next Steps
    ├── 1. [Immediate action]
    └── 2. [Follow-up action]
```

## Feature Management Benefits

By naming synopses after features:
- **History** - Browse `.claude/` folder to see all features worked on
- **Documentation** - Each synopsis documents a feature's implementation
- **Handoff** - New sessions can review past feature synopses for context
- **Tracking** - See feature states at a glance (Complete, In Progress, etc.)
