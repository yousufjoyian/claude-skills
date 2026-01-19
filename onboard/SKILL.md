# Onboard Skill

**Triggers:** "onboard", "get up to speed", "catch me up", "where were we"

## Purpose

Quickly onboard to any project by reading CONTEXT.md and presenting current state.

## Protocol

### Step 1: Identify Project

Determine which project to onboard to:
- If in a TriClaude terminal: use the project from terminal context
- If user specifies: use that project
- If ambiguous: ask user

### Step 2: Read Context (MANDATORY)

```bash
# THE ONE FILE - contains everything needed
cat ~/local_workspaces/<project>/.claude/CONTEXT.md
```

This ~250 token file has: goal, status, changed files, decisions, blockers, resume instructions.

### Step 3: Check What Changed Since Context

The CONTEXT.md header includes a timestamp: `# <project> | YYYY-MM-DD HH:MM`

```bash
cd ~/local_workspaces/<project>

# Find files modified AFTER context was saved
CONTEXT_FILE=".claude/CONTEXT.md"
echo "Files modified since context was saved:"
find src/ -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.py" \) -newer "$CONTEXT_FILE" 2>/dev/null

# Quick git status
git status
git log --oneline -3
```

**Decision logic:**
- **No files modified after context** → Trust CONTEXT.md, ready to work
- **Files modified** → Read only those specific changed files
- **Many files modified** → Someone else worked on project, full exploration needed

### Step 4: Present Summary

Output a concise summary:

```
## Project: <name>

**Goal:** [from CONTEXT.md]

**Status:**
- [x] Done: [count] tasks
- [→] Active: [current task]
- [ ] Next: [upcoming]

**Recent:** [from git log]

**Ready to continue.** [Resume instructions from CONTEXT.md]
```

## Only Read More If Needed

| File | When to Read |
|------|--------------|
| **Files modified after CONTEXT.md** | ALWAYS - these have changes not in context |
| `reference/PROJECT.md` | If confused about architecture |
| `reference/CONVENTIONS.md` | If writing new code |
| `reference/TROUBLESHOOTING.md` | If hitting known issues |
| Root `CLAUDE.md` | If exists and project-specific |

**Key principle:** If no files were modified after CONTEXT.md was saved, you have complete context. Skip exploration and start working.

## If CONTEXT.md Missing

If `.claude/CONTEXT.md` doesn't exist:

1. Check for legacy `.claude/sessions/latest.md` (migrate if found)
2. Inform user: "No context file found."
3. Offer: "Run 'init project' to set up standard structure?"
4. Proceed with basic exploration:
   - Read README.md if exists
   - Check package.json
   - Scan directory structure

## Example Output

```
## Project: triclaude

**Goal:** Implement token-efficient context save system

**Status:**
- [x] Done: 5 tasks (save button, skill update, folder restructure)
- [→] Active: sync changes to runtime cache
- [ ] Next: test save button end-to-end

**Recent:**
- f566c95 v4.2.0: Per-terminal A2UI, text-based consigliere
- 7f03549 feat: Add fullscreen mode

**Ready to continue.** ShortcutBar has new blue save button.
Need to test it sends "save context" correctly.
```
