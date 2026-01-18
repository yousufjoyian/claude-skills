---
name: synopsis
description: Generate a comprehensive session synopsis in the A2UI panel
---

# Synopsis Skill

Generate a comprehensive visual synopsis of the current session in the A2UI panel.

## Trigger Phrases

- "show synopsis"
- "synopsis"
- "show status"
- "session summary"

## What to Include

The synopsis should provide a comprehensive overview at the **goal/objective level**:

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
      <h1>Session Synopsis</h1>
      <div class="timestamp">Generated: [TIMESTAMP]</div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">🎯 Current Goal</div>
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

## Key Guidelines

1. **Be comprehensive** - Include all sections, even if some are brief
2. **Use actual data** - Pull from CONTEXT.md, git status, and conversation context
3. **Keep it scannable** - Use icons, colors, and clear hierarchy
4. **Timestamp it** - Always include when the synopsis was generated
5. **Focus on objectives** - This is goal-level, not task-level detail

## Example Output Structure

```
Session Synopsis
├── Current Goal: [Main objective]
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
