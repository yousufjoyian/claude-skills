# Visual Plan Skill

## Purpose
Generate structured, interactive plan visualizations for the Understanding Center (A2UI panel).

## Triggers
- "visualize plan", "show plan", "vplan"
- Automatically triggered when creating implementation plans with 3+ steps

## Output Format

Write HTML to the A2UI log file. The HTML must be wrapped in markers:
```
<!-- A2UI:START -->
<!DOCTYPE html>
<html>...</html>
<!-- A2UI:END -->
```

## Plan Visualization Template

```html
<!-- A2UI:START -->
<!DOCTYPE html>
<html>
<head>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: #0f172a;
  color: #e2e8f0;
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 13px;
  padding: 16px;
  min-height: 100vh;
}
.plan-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #334155;
}
.plan-header h1 {
  font-size: 16px;
  font-weight: 600;
  color: #f8fafc;
}
.plan-header .badge {
  font-size: 10px;
  padding: 2px 8px;
  border-radius: 12px;
  background: #3b82f6;
  color: white;
}

.section {
  margin-bottom: 20px;
}
.section-title {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #64748b;
  margin-bottom: 8px;
}

.objective {
  background: #1e293b;
  border-left: 3px solid #3b82f6;
  padding: 12px;
  border-radius: 0 8px 8px 0;
  color: #e2e8f0;
}

.task-list { list-style: none; }
.task-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 8px 12px;
  background: #1e293b;
  border-radius: 6px;
  margin-bottom: 4px;
}
.task-status {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 2px;
}
.task-status.done { background: #22c55e; color: white; }
.task-status.active { background: #3b82f6; color: white; }
.task-status.pending { background: #334155; color: #64748b; }
.task-text { flex: 1; }
.task-text.done { text-decoration: line-through; opacity: 0.6; }

.progress-bar {
  height: 8px;
  background: #334155;
  border-radius: 4px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #22c55e, #3b82f6);
  transition: width 0.3s ease;
}
.progress-text {
  margin-top: 8px;
  font-size: 12px;
  color: #94a3b8;
  text-align: center;
}
</style>
</head>
<body>
<div class="plan-header">
  <h1>Implementation Plan</h1>
  <span class="badge">In Progress</span>
</div>

<div class="section">
  <div class="section-title">Objective</div>
  <div class="objective">
    <!-- OBJECTIVE: Single sentence describing what we're achieving -->
  </div>
</div>

<div class="section">
  <div class="section-title">Tasks</div>
  <ul class="task-list">
    <li class="task-item">
      <span class="task-status done">✓</span>
      <span class="task-text done">Completed task</span>
    </li>
    <li class="task-item">
      <span class="task-status active">→</span>
      <span class="task-text">Active task</span>
    </li>
    <li class="task-item">
      <span class="task-status pending">○</span>
      <span class="task-text">Pending task</span>
    </li>
  </ul>
</div>

<div class="section">
  <div class="section-title">Progress</div>
  <div class="progress-bar">
    <div class="progress-fill" style="width: 60%"></div>
  </div>
  <div class="progress-text">3 of 5 tasks completed</div>
</div>
</body>
</html>
<!-- A2UI:END -->
```

## Usage Instructions

1. **Automatic Triggering**: When creating a plan with 3+ steps, auto-generate this visualization
2. **Fill in the sections**:
   - Objective: One clear sentence
   - Tasks: Each step with status (done/active/pending)
   - Progress: Calculate and display completion percentage

3. **Write to A2UI log**:
   The A2UI log path is in your session startup message.

## Design Guidelines

- **Dark theme**: Use #0f172a, #1e293b, #334155 backgrounds
- **Light text**: #e2e8f0, #f8fafc for content
- **Accent colors**:
  - Blue (#3b82f6) for active/primary
  - Green (#22c55e) for completed
  - Gray (#64748b) for pending
  - Red (#dc2626) for blockers
- **Keep it scannable**: Users should understand progress at a glance
- **Panel width**: ~400px, so design accordingly
