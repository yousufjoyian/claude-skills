# Save Context Skill

**Triggers:** "save context", "save session", "handoff", "end session"

## Purpose

Save current work state to `.claude/CONTEXT.md` for seamless continuation in future sessions.

## Output File

```
<project>/.claude/CONTEXT.md
```

## Format (Strict Template)

```markdown
# <project> | YYYY-MM-DD

## Goal
[Current objective - one line max]

## Status
- [x] Completed task
- [→] Active: current task description
- [ ] Next: upcoming task

## Changed
- `path/file.ts:line` - what changed
- `path/new-file.ts` - NEW: purpose

## Decided
- Topic: decision (why in parentheses)

## Blocked
- Issue description → workaround if any
- [none] if no blockers

## Resume
Specific actionable instructions to continue. Reference exact files
and line numbers. 2-3 sentences max.
```

## Token Budget

| Section | Target | Notes |
|---------|--------|-------|
| Header | ~10 | Project name + date |
| Goal | ~15 | One line |
| Status | ~40 | 3-5 items |
| Changed | ~50 | File references only |
| Decided | ~60 | Key choices with rationale |
| Blocked | ~20 | Or "[none]" |
| Resume | ~50 | Actionable steps |
| **Total** | **~250** | Max ~300 |

## Writing Rules

1. **One line per item** - forces concision
2. **Reference, don't embed** - `file.ts:123` not code blocks
3. **Decisions WITH rationale** - "X over Y (because Z)"
4. **Status symbols** - `[x]` done, `[→]` active, `[ ]` pending
5. **Resume is actionable** - specific next steps, not vague "continue work"

## Protocol

### Step 1: Identify Project

```bash
# Use current working directory
pwd
# Or ask user if ambiguous
```

### Step 2: Gather Information

```bash
cd ~/local_workspaces/<project>

# Check what changed
git status
git diff --stat

# Recent commits
git log --oneline -5

# Current branch
git branch --show-current
```

### Step 3: Archive Previous Context (if exists)

```bash
mkdir -p ~/local_workspaces/<project>/.claude/history

if [ -f ~/local_workspaces/<project>/.claude/CONTEXT.md ]; then
    mv ~/local_workspaces/<project>/.claude/CONTEXT.md \
       ~/local_workspaces/<project>/.claude/history/$(date +%Y-%m-%d_%H%M).md
fi
```

### Step 4: Generate CONTEXT.md

Write the file using the strict template above. Be concise.

### Step 5: Confirm

```
Context saved: <project>/.claude/CONTEXT.md

Summary:
- Goal: [goal]
- Status: [x] done, [→] active, [ ] pending counts
- Files: [count] changed

Previous context archived to: .claude/history/YYYY-MM-DD_HHMM.md
```

## Example Output

```markdown
# triclaude | 2026-01-16

## Goal
Implement token-efficient context save system for session continuity

## Status
- [x] Added save button to ShortcutBar
- [x] Updated session-save skill format
- [→] Active: updating root CLAUDE.md with auto-read
- [ ] Next: migrate existing latest.md to CONTEXT.md

## Changed
- `src/components/ShortcutBar.tsx:3` - added Save icon import
- `src/components/ShortcutBar.tsx:20` - added save context shortcut
- `skills/session-save/SKILL.md` - REWRITE: new CONTEXT.md format

## Decided
- Single CONTEXT.md over multiple files (token efficiency)
- Manual save button over auto-save (user control)
- ~250 token budget (efficient but complete)

## Blocked
- [none]

## Resume
ShortcutBar now has blue save button sending "save context".
Next: update root CLAUDE.md to auto-read .claude/CONTEXT.md on
session start. Then restructure triclaude/.claude/ folder.
```

## What NOT to Include

- Code snippets (reference files instead)
- Full error messages (summarize)
- Conversation history (just outcomes)
- Speculation about future work
- Timestamps beyond the date
