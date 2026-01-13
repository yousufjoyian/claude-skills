# Onboard Skill

**Triggers:** "onboard", "get up to speed", "catch me up", "what's the context", "where were we"

## Purpose

Quickly onboard to any project by reading standardized documentation and presenting a summary.

## Protocol

When triggered, execute these steps IN ORDER:

### Step 1: Identify Project

Determine which project to onboard to:
- If user specifies: use that project
- If in a TriClaude terminal: use the project from the terminal's context
- If ambiguous: ask user

### Step 2: Read Project Documentation

Read these files in order (skip if doesn't exist):

```bash
# Core project docs
cat ~/local_workspaces/<project>/.claude/PROJECT.md
cat ~/local_workspaces/<project>/.claude/CONVENTIONS.md
cat ~/local_workspaces/<project>/CLAUDE.md

# Current session context (MOST IMPORTANT)
cat ~/local_workspaces/<project>/.claude/sessions/latest.md
```

### Step 3: Quick Codebase Scan

```bash
# Get structure overview
ls -la ~/local_workspaces/<project>/
find ~/local_workspaces/<project> -name "*.md" -type f 2>/dev/null | head -10

# Check git status
cd ~/local_workspaces/<project> && git status && git log --oneline -5
```

### Step 4: Present Summary

Output a concise summary:

```
## Project: <name>

**Purpose:** [1-2 sentences from PROJECT.md]

**Stack:** [Key technologies]

**Current State:** [From sessions/latest.md]
- Last worked on: [date]
- In progress: [tasks]
- Next steps: [priorities]

**Recent Changes:**
[From git log]

**Ready to continue.** What would you like to work on?
```

## If Documentation Missing

If `.claude/` directory doesn't exist:

1. Inform user: "This project doesn't have standard documentation yet."
2. Offer: "Would you like me to initialize it? (run `init project`)"
3. Proceed with basic exploration:
   - Read any existing README.md
   - Check package.json or equivalent
   - Scan directory structure

## Quick Reference

| File | Purpose | Priority |
|------|---------|----------|
| `sessions/latest.md` | Current context | **READ FIRST** |
| `PROJECT.md` | Architecture overview | High |
| `CONVENTIONS.md` | Code style | Medium |
| `TROUBLESHOOTING.md` | Known issues | As needed |
| Root `CLAUDE.md` | Agent instructions | High |

## Example Output

```
## Project: triclaude

**Purpose:** Multi-terminal console with Claude voice advisor for managing multiple projects simultaneously.

**Stack:** React, TypeScript, Vite, Python (backend), tmux, ttyd

**Current State:**
- Last session: 2026-01-13
- Completed: Fixed instruction delivery, added loading spinners
- In progress: None
- Next: Testing GitHub integration

**Recent Changes:**
- cd79fa9 v3.1.0: Add loading indicators, GitHub integration
- d991642 v3.0.0: Restore project picker

**Ready to continue.** What would you like to work on?
```
