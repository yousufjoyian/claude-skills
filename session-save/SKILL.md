# Session Save Skill

**Triggers:** "save session", "save context", "handoff", "end session", "wrap up", "save progress"

## Purpose

Capture current session context and save it so the next agent can continue seamlessly.

## Protocol

### Step 1: Identify Project

Determine which project's session to save:
- If user specifies: use that project
- If working directory is clear: use current project
- If ambiguous: ask user

### Step 2: Create Session Directory

```bash
mkdir -p ~/local_workspaces/<project>/.claude/sessions/archive
```

### Step 3: Archive Previous Session (if exists)

```bash
# Move current latest.md to archive with timestamp
if [ -f ~/local_workspaces/<project>/.claude/sessions/latest.md ]; then
    mv ~/local_workspaces/<project>/.claude/sessions/latest.md \
       ~/local_workspaces/<project>/.claude/sessions/archive/$(date +%Y-%m-%d_%H%M).md
fi
```

### Step 4: Generate Session Summary

Create `latest.md` with this template:

```markdown
# Session Handoff: YYYY-MM-DD

## Summary
[1-2 sentence summary of what was accomplished this session]

## Original Goal
[What the user initially asked for]

## Completed Tasks
- [x] Task 1: Brief description
- [x] Task 2: Brief description

## In Progress
- [ ] Task (if any incomplete work)

## Files Modified

| File | Change Summary |
|------|----------------|
| `path/to/file` | What was changed |

## Key Decisions Made
- **Decision:** [What was decided]
  - **Rationale:** [Why]

## Technical Notes
[Any implementation details the next agent should know]

## Known Issues / Blockers
- Issue: Description and workaround if any

## Next Steps (Priority Order)
1. Highest priority task
2. Next task
3. Future consideration

## Environment State
- Branch: [current git branch]
- Services running: [if applicable]
- Build status: [if applicable]

## Handoff Notes
[Anything else the next agent should know that's not captured above]
```

### Step 5: Write the File

```bash
# Write to latest.md
cat > ~/local_workspaces/<project>/.claude/sessions/latest.md << 'EOF'
[Generated content]
EOF
```

### Step 6: Confirm to User

```
Session context saved to:
  ~/local_workspaces/<project>/.claude/sessions/latest.md

Summary:
- [X] tasks completed
- [Y] files modified
- Next agent can run "onboard" to continue

Previous session archived to:
  .claude/sessions/archive/YYYY-MM-DD_HHMM.md
```

## Content Guidelines

### What to Include
- Actual accomplishments (not intentions)
- Files that were ACTUALLY modified (verify with git status)
- Decisions with rationale
- Blockers and workarounds found
- Specific next steps

### What NOT to Include
- Sensitive data (API keys, passwords)
- Verbose code snippets (reference files instead)
- Conversation transcript (summarize instead)
- Speculation about future work

### Gathering Information

To generate accurate content, check:

```bash
# What files changed?
cd ~/local_workspaces/<project> && git status && git diff --stat

# What was the recent work?
git log --oneline -10

# Any running services?
ps aux | grep -E "python|node|ttyd" | grep -v grep
```

## Example Session Save

```markdown
# Session Handoff: 2026-01-13

## Summary
Fixed Claude instruction delivery system and added loading indicators to TriClaude UI.

## Original Goal
User reported "Launch Claude" wasn't delivering project instructions to new Claude sessions.

## Completed Tasks
- [x] Diagnosed ttyd binding issue (was using -i 0.0.0.0 on NixOS)
- [x] Rewrote instruction delivery to use tmux load-buffer instead of send-keys
- [x] Added loading spinners to Launch Claude/Terminal buttons
- [x] Made ShortcutBar collapsible
- [x] Committed v3.1.0 to GitHub

## Files Modified

| File | Change Summary |
|------|----------------|
| `src/App.tsx` | Added `launching` state, Loader2 spinner |
| `src/components/ShortcutBar.tsx` | Added collapse/expand with `isExpanded` state |
| `scripts/project_api.py` | Rewrote instruction delivery, removed -i flag from ttyd |

## Key Decisions Made
- **Decision:** Use tmux load-buffer/paste-buffer for instruction delivery
  - **Rationale:** Avoids shell escaping issues with multi-line text
- **Decision:** Remove `-i 0.0.0.0` from ttyd command
  - **Rationale:** NixOS has binding issues with explicit interface specification

## Next Steps
1. Test instruction delivery with fresh Claude launch
2. Consider adding backend scripts to git repo
3. Create standardized project documentation

## Handoff Notes
The backend scripts (project_api.py) are in GoogleDrive, not the triclaude git repo.
```

## Git Integration (Optional)

After saving session, optionally commit:

```bash
cd ~/local_workspaces/<project>
git add .claude/sessions/latest.md
git commit -m "docs: Update session context $(date +%Y-%m-%d)"
```
