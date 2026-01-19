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
