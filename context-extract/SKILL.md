---
name: context-extract
description: Extract conversation context as raw and AI-summarized formats, save locally and commit to git
---

# Context Extract Skill

Extracts current conversation context in multiple formats for continuity and AI ingestion.

## Triggers

- "extract context"
- "save conversation"
- "export context"
- "dump context"
- "context snapshot"

## Purpose

Capture the full conversation context in two formats:
1. **Raw**: Complete conversation for reference/debugging
2. **Summary**: AI-optimized digest for future session bootstrap

Both are saved locally AND committed to git for persistence.

## Output Structure

```
<project>/.claude/context/
├── raw/
│   └── YYYY-MM-DD_HHMM_raw.md       # Full conversation
├── summary/
│   └── YYYY-MM-DD_HHMM_summary.md   # AI-optimized digest
└── latest/
    ├── raw.md                        # Symlink/copy to most recent
    └── summary.md                    # Symlink/copy to most recent
```

## Workflow

### Step 1: Identify Project & Timestamp

```bash
PROJECT=$(basename $(pwd))
TIMESTAMP=$(date +%Y-%m-%d_%H%M)
CONTEXT_DIR=~/local_workspaces/$PROJECT/.claude/context

mkdir -p $CONTEXT_DIR/{raw,summary,latest}
```

### Step 2: Extract Raw Context

Create `raw/YYYY-MM-DD_HHMM_raw.md`:

```markdown
# Raw Conversation Context
**Project:** <project-name>
**Extracted:** YYYY-MM-DD HH:MM
**Session Duration:** [estimate from first to last message]

---

## Conversation Transcript

### User [HH:MM]
[Exact user message]

### Assistant [HH:MM]
[Exact assistant response - can be summarized if very long]

### User [HH:MM]
[...]

---

## Files Touched This Session

| File | Operations | Final State |
|------|------------|-------------|
| `path/file.ts` | read, edit | modified |
| `path/new.md` | created | new |

## Commands Executed

```bash
# Sequential list of bash commands run
git status
npm test
...
```

## Tool Usage Summary

| Tool | Count | Purpose |
|------|-------|---------|
| Read | 5 | File inspection |
| Edit | 12 | Code changes |
| Bash | 8 | Git, tests |
| Grep | 3 | Search |
```

### Step 3: Generate AI Summary

Create `summary/YYYY-MM-DD_HHMM_summary.md`:

```markdown
# Context Summary for AI Bootstrap
**Project:** <project-name>
**Generated:** YYYY-MM-DD HH:MM

## Quick Context (Read This First)

[2-3 sentences: What project is this, what was the user trying to accomplish, and what's the current state]

## Session Goals

1. **Primary:** [Main objective]
2. **Secondary:** [Additional tasks if any]

## What Was Accomplished

- [Concrete outcome 1]
- [Concrete outcome 2]
- [etc.]

## Key Decisions & Rationale

| Decision | Why | Impact |
|----------|-----|--------|
| Chose X over Y | [Reason] | [Files/areas affected] |

## Current Codebase State

### Modified Files (This Session)
```
path/to/file1.ts  - [one-line description of change]
path/to/file2.md  - [one-line description of change]
```

### New Files Created
```
path/to/new-file.ts - [purpose]
```

### Deleted Files
```
(none this session)
```

## Technical Context

### Architecture Notes
[Any architectural decisions or patterns established]

### Dependencies Added/Changed
[Package changes if any]

### Environment Requirements
[Any env vars, services, or setup needed]

## Open Items

### In Progress
- [ ] [Task description] - [current state]

### Blocked
- [ ] [Task] - [blocker description]

### Deferred
- [ ] [Task] - [reason deferred]

## Next Actions (Priority Order)

1. **[Action]** - [why this is next]
2. **[Action]** - [context]
3. **[Action]** - [context]

## Warnings / Gotchas

- [Anything the next agent should be careful about]
- [Known issues or quirks discovered]

## Reproduction Commands

```bash
# To restore this state:
cd ~/local_workspaces/<project>
git checkout <branch>
git pull

# To continue where we left off:
[specific command if applicable]
```

---
*This summary was auto-generated. Raw transcript available at: raw/YYYY-MM-DD_HHMM_raw.md*
```

### Step 4: Update Latest Pointers

```bash
# Copy (not symlink for git compatibility)
cp $CONTEXT_DIR/raw/${TIMESTAMP}_raw.md $CONTEXT_DIR/latest/raw.md
cp $CONTEXT_DIR/summary/${TIMESTAMP}_summary.md $CONTEXT_DIR/latest/summary.md
```

### Step 5: Git Commit

```bash
cd ~/local_workspaces/$PROJECT

# Stage context files
git add .claude/context/

# Commit with descriptive message
git commit -m "$(cat <<'EOF'
docs(context): Extract session context YYYY-MM-DD

- Raw conversation transcript
- AI-optimized summary for bootstrap
- Files modified: [count]
- Commands run: [count]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"

# Push if remote exists
git push origin $(git branch --show-current) 2>/dev/null || echo "Push skipped (no remote or offline)"
```

### Step 6: Confirm to User

```
Context extracted successfully!

Local:
  Raw:     .claude/context/raw/2026-01-16_1430_raw.md
  Summary: .claude/context/summary/2026-01-16_1430_summary.md
  Latest:  .claude/context/latest/{raw,summary}.md

Git:
  Commit: abc1234 - docs(context): Extract session context
  Pushed: origin/main

Next agent bootstrap:
  cat .claude/context/latest/summary.md
```

## Summary Generation Guidelines

### What to Include

**In Raw:**
- Complete conversation flow (can truncate very long outputs)
- All file paths touched
- All commands run
- Tool usage patterns
- Errors encountered and how resolved

**In Summary:**
- Distilled goals and outcomes
- Decisions with rationale (critical for AI continuity)
- Current state (what exists now)
- Clear next steps
- Warnings and gotchas

### What NOT to Include

- Sensitive data (API keys, passwords, tokens)
- Large code blocks (reference file paths instead)
- Redundant conversation turns
- Personal information
- Speculation or uncertain information

### AI Bootstrap Optimization

The summary should allow a new AI agent to:
1. Understand project context in <30 seconds
2. Know what was already tried
3. Avoid repeating mistakes
4. Continue seamlessly without asking "what were we doing?"

## Integration with Other Skills

| Skill | Relationship |
|-------|--------------|
| `session-save` | Focus on project handoff; context-extract is more comprehensive |
| `onboard` | Reads `context/latest/summary.md` during bootstrap |
| `git-commit` | Used internally for committing context files |

## Automation Options

### Auto-extract on Session End
Add to your shell profile or TriClaude:
```bash
# Trigger on "goodbye", "done for now", "end session"
alias bye='echo "extract context" | claude-send'
```

### Scheduled Extraction
```bash
# Every 2 hours during active sessions
*/120 * * * * [ -f /tmp/claude-active ] && echo "extract context" | claude-send
```

## Shortcut

In TriClaude ShortcutBar, the context extract button:
- Icon: `FileOutput` (lucide)
- Color: `purple`
- Sends: `extract context`

## Example Summary Output

```markdown
# Context Summary for AI Bootstrap
**Project:** triclaude
**Generated:** 2026-01-16 14:30

## Quick Context (Read This First)

TriClaude is a multi-terminal React app for managing Claude Code sessions. This session added a git commit skill and shortcut bar button. User wants comprehensive context extraction next.

## Session Goals

1. **Primary:** Add git-commit skill with smart staging and conventional commits
2. **Secondary:** Add shortcut bar button for commit trigger

## What Was Accomplished

- Created `skills/git-commit/SKILL.md` with full commit workflow
- Added GitCommit button to ShortcutBar.tsx (green, sends "commit")
- Updated WORKSPACE.md with git skills section
- Cross-linked github skill to git-commit skill

## Key Decisions & Rationale

| Decision | Why | Impact |
|----------|-----|--------|
| Separate git-commit from github skill | Separation of concerns - local vs remote | Two focused skills |
| Use GitCommit lucide icon | Clear visual meaning | ShortcutBar.tsx |
| Green color for commit button | Indicates "positive" action | UI consistency |

## Current Codebase State

### Modified Files (This Session)
```
skills/git-commit/SKILL.md - NEW: full commit workflow skill
skills/WORKSPACE.md - Added git skills section
skills/github/SKILL.md - Added cross-reference to git-commit
triclaude/src/components/ShortcutBar.tsx - Added commit button
```

## Next Actions (Priority Order)

1. **Create context-extract skill** - user requested
2. **Add context shortcut to bar** - purple FileOutput icon
3. **Test full workflow** - commit + context extract

---
*Raw transcript: raw/2026-01-16_1430_raw.md*
```
