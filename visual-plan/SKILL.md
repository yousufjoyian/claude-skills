# Visual Plan Skill

**Triggers:** "visualize plan", "show plan", "visual summary", "a2ui plan", "vplan"

## Purpose

Generate a visual A2UI summary of the current plan, progress, and understanding. Helps user see at a glance what Claude understands about the goal and status.

## When to Use

- User wants to verify Claude's understanding
- Complex multi-step task in progress
- Before starting implementation (confirm alignment)
- Midway through work (show progress)
- After planning phase (visualize the plan)

## A2UI Log Path

The path is **dynamic per-terminal**. Find it in your session startup message:

```
A2UI VISUALIZATION: Write HTML to /home/yousuf/GoogleDrive/PROJECTS/.triclaude/runtime/terminals/<terminal_id>/a2ui_input.log
```

Extract this path and use it for output.

## Protocol

### Step 1: Identify A2UI Path

Look in your system context for `A2UI VISUALIZATION:` line. Extract the path.

If not found, ask user or check:
```bash
ls -la /home/yousuf/GoogleDrive/PROJECTS/.triclaude/runtime/terminals/*/a2ui_input.log 2>/dev/null | head -1
```

### Step 2: Gather Context

From conversation and any available sources:
- **Goal**: What are we trying to achieve?
- **Status**: What's done, active, pending?
- **Structure**: Any architecture or file structure relevant?
- **Decisions**: Key choices made and why?
- **Blockers**: Any issues?
- **Next**: Immediate next steps?

### Step 3: Generate Visualization

Use the HTML template below. Adapt sections based on what's relevant.

### Step 4: Write to A2UI

```bash
cat << 'A2UI_EOF' >> $A2UI_LOG_PATH
<!-- A2UI:START -->
[HTML content]
<!-- A2UI:END -->
A2UI_EOF
```

## HTML Template

```html
<!-- A2UI:START -->
<!DOCTYPE html>
<html>
<head>
<style>
* { box-sizing: border-box; }
body {
  margin: 0;
  padding: 16px;
  background: #0f172a;
  color: #e2e8f0;
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 12px;
  line-height: 1.5;
}
.header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #334155;
}
.header-icon { font-size: 20px; }
.header h1 {
  margin: 0;
  font-size: 14px;
  color: #60a5fa;
  font-weight: 600;
}
.timestamp {
  margin-left: auto;
  color: #64748b;
  font-size: 10px;
}

.section {
  margin-bottom: 16px;
}
.section-title {
  font-size: 11px;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.goal-box {
  background: linear-gradient(135deg, #1e3a5f 0%, #1e293b 100%);
  border: 1px solid #3b82f6;
  border-radius: 8px;
  padding: 12px;
  color: #93c5fd;
  font-weight: 500;
}

.status-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.status-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  background: #1e293b;
  border-radius: 6px;
}
.status-icon {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  flex-shrink: 0;
}
.status-done { background: #166534; color: #4ade80; }
.status-active { background: #1d4ed8; color: #60a5fa; }
.status-pending { background: #334155; color: #94a3b8; }
.status-text { flex: 1; }
.status-active-row { border: 1px solid #3b82f6; }

.structure-box {
  background: #1e293b;
  border-radius: 8px;
  padding: 12px;
  font-family: 'SF Mono', Consolas, monospace;
  font-size: 11px;
}
.folder { color: #fbbf24; }
.file { color: #34d399; }
.highlight { color: #f472b6; }
.dim { color: #64748b; }

.decisions-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.decision-item {
  background: #1e293b;
  border-left: 3px solid #a78bfa;
  padding: 8px 12px;
  border-radius: 0 6px 6px 0;
}
.decision-what { color: #e2e8f0; }
.decision-why { color: #94a3b8; font-size: 11px; margin-top: 2px; }

.next-box {
  background: linear-gradient(135deg, #14532d 0%, #1e293b 100%);
  border: 1px solid #22c55e;
  border-radius: 8px;
  padding: 12px;
  color: #86efac;
}

.blockers-box {
  background: linear-gradient(135deg, #7f1d1d 0%, #1e293b 100%);
  border: 1px solid #ef4444;
  border-radius: 8px;
  padding: 12px;
  color: #fca5a5;
}

.progress-bar {
  height: 6px;
  background: #334155;
  border-radius: 3px;
  overflow: hidden;
  margin-top: 8px;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #22c55e 0%, #3b82f6 100%);
  border-radius: 3px;
}
</style>
</head>
<body>

<div class="header">
  <span class="header-icon">📋</span>
  <h1>Plan Summary</h1>
  <span class="timestamp"><!-- TIMESTAMP --></span>
</div>

<!-- GOAL SECTION -->
<div class="section">
  <div class="section-title">Goal</div>
  <div class="goal-box">
    <!-- GOAL_TEXT -->
  </div>
</div>

<!-- STATUS SECTION -->
<div class="section">
  <div class="section-title">Status</div>
  <div class="status-list">
    <!-- STATUS_ITEMS -->
    <!-- Example:
    <div class="status-item">
      <span class="status-icon status-done">✓</span>
      <span class="status-text">Completed task description</span>
    </div>
    <div class="status-item status-active-row">
      <span class="status-icon status-active">→</span>
      <span class="status-text">Active task description</span>
    </div>
    <div class="status-item">
      <span class="status-icon status-pending">○</span>
      <span class="status-text">Pending task description</span>
    </div>
    -->
  </div>
  <div class="progress-bar">
    <div class="progress-fill" style="width: <!-- PROGRESS_PERCENT -->%;"></div>
  </div>
</div>

<!-- STRUCTURE SECTION (optional - include if relevant) -->
<div class="section">
  <div class="section-title">Structure</div>
  <div class="structure-box">
    <!-- STRUCTURE_CONTENT -->
  </div>
</div>

<!-- DECISIONS SECTION (optional - include if decisions were made) -->
<div class="section">
  <div class="section-title">Decisions</div>
  <div class="decisions-list">
    <!-- DECISION_ITEMS -->
    <!-- Example:
    <div class="decision-item">
      <div class="decision-what">Chose X over Y</div>
      <div class="decision-why">Because of Z</div>
    </div>
    -->
  </div>
</div>

<!-- NEXT SECTION -->
<div class="section">
  <div class="section-title">Next</div>
  <div class="next-box">
    <!-- NEXT_TEXT -->
  </div>
</div>

<!-- BLOCKERS SECTION (only if blockers exist) -->
<!--
<div class="section">
  <div class="section-title">Blockers</div>
  <div class="blockers-box">
    BLOCKER_TEXT
  </div>
</div>
-->

</body>
</html>
<!-- A2UI:END -->
```

## Section Guidelines

| Section | When to Include | Content |
|---------|-----------------|---------|
| Goal | Always | One clear sentence |
| Status | Always | Done/Active/Pending items |
| Structure | If architecture matters | Folder trees, component diagrams |
| Decisions | If choices were made | What + why (brief) |
| Next | Always | Immediate actionable step |
| Blockers | Only if blocked | Issue + workaround if any |

## Adaptation Examples

### Simple Task (3 sections)
- Goal, Status, Next

### Architecture Work (5 sections)
- Goal, Status, Structure, Decisions, Next

### Debugging (4 sections)
- Goal, Status, Structure (showing where issue is), Next

### Blocked (4 sections)
- Goal, Status, Blockers, Next (workaround)

## Visual Style Rules

1. **Dark theme**: Background `#0f172a`, cards `#1e293b`
2. **Status colors**: Done=green, Active=blue, Pending=gray
3. **Accent borders**: Use colored left borders for emphasis
4. **Progress bar**: Show visual completion percentage
5. **Monospace**: For code/structure, use `SF Mono, Consolas`
6. **Compact**: ~400px width, no wasted space

## Example Output

When user says "visualize plan" during a feature implementation:

```
📋 Plan Summary                           10:45 AM

GOAL
Add user authentication to the application

STATUS
✓ Set up auth provider
✓ Create login form component
→ Implement token storage
○ Add protected routes
○ Create logout functionality

[████████░░░░░░░░] 40%

DECISIONS
• JWT over sessions — stateless, scales better
• localStorage over cookies — simpler CORS

NEXT
Implement token storage in AuthContext using localStorage
```

## Confirm Output

After writing to A2UI, confirm:
```
Visual plan sent to A2UI panel.
```
