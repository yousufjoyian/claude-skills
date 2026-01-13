# Project Init Skill

**Triggers:** "init project", "setup project docs", "initialize documentation", "create project structure"

## Purpose

Initialize the standard `.claude/` documentation structure for any project, enabling seamless agent onboarding.

## Standard Structure

```
project/
├── .claude/
│   ├── PROJECT.md          # Architecture, purpose, tech stack
│   ├── CONVENTIONS.md      # Code style, patterns, practices
│   ├── TROUBLESHOOTING.md  # Common issues and solutions
│   └── sessions/
│       ├── latest.md       # Current session context
│       └── archive/        # Historical sessions
├── CLAUDE.md               # Project-specific Claude instructions
└── [project files...]
```

## Protocol

### Step 1: Identify Project

```bash
# Determine project path
PROJECT_PATH=~/local_workspaces/<project>
PROJECT_NAME=<project>
```

### Step 2: Create Directory Structure

```bash
mkdir -p $PROJECT_PATH/.claude/sessions/archive
```

### Step 3: Analyze Project

Before writing docs, gather information:

```bash
# Check existing files
ls -la $PROJECT_PATH/
cat $PROJECT_PATH/README.md 2>/dev/null
cat $PROJECT_PATH/package.json 2>/dev/null | head -20

# Check git info
cd $PROJECT_PATH && git remote -v 2>/dev/null
cd $PROJECT_PATH && git log --oneline -5 2>/dev/null

# Identify tech stack
find $PROJECT_PATH -maxdepth 2 -name "*.json" -o -name "*.toml" -o -name "*.yaml" | head -10
```

### Step 4: Create PROJECT.md

Write to `$PROJECT_PATH/.claude/PROJECT.md`:

```markdown
# [Project Name]

## Overview
[1-2 sentence description of what this project does]

## Purpose
[Why this project exists, what problem it solves]

## Tech Stack
| Component | Technology |
|-----------|------------|
| Frontend  | [e.g., React, TypeScript] |
| Backend   | [e.g., Python, FastAPI] |
| Database  | [e.g., PostgreSQL] |
| Other     | [e.g., Docker, tmux] |

## Architecture

```
[ASCII diagram or description of how components connect]
```

## Key Files
| File/Directory | Purpose |
|----------------|---------|
| `src/` | [Description] |
| `scripts/` | [Description] |

## Getting Started

### Prerequisites
- [Requirement 1]
- [Requirement 2]

### Installation
```bash
[Installation commands]
```

### Running
```bash
[Run commands]
```

### Testing
```bash
[Test commands]
```

## External Dependencies
- [Service/API]: [What it's used for]

## Related Resources
- [Link to docs, designs, etc.]
```

### Step 5: Create CONVENTIONS.md

Write to `$PROJECT_PATH/.claude/CONVENTIONS.md`:

```markdown
# Conventions

## Code Style

### General
- [Indentation preference]
- [Line length limits]
- [Comment style]

### Naming
| Type | Convention | Example |
|------|------------|---------|
| Files | [style] | `userService.ts` |
| Functions | [style] | `getUserById` |
| Variables | [style] | `isLoading` |
| Constants | [style] | `MAX_RETRIES` |

### TypeScript/JavaScript
- [Specific conventions]

### Python
- [Specific conventions]

## File Organization
```
src/
├── components/   # React components
├── services/     # Business logic
├── utils/        # Helpers
└── types/        # TypeScript types
```

## Git Workflow
- Branch naming: `feature/`, `fix/`, `docs/`
- Commit format: `type: description`
- PR requirements: [if any]

## Testing
- Test file location: [pattern]
- Naming convention: `*.test.ts`
- Coverage requirements: [if any]

## Documentation
- Inline comments: [when to use]
- README updates: [when required]
- API docs: [how maintained]
```

### Step 6: Create TROUBLESHOOTING.md

Write to `$PROJECT_PATH/.claude/TROUBLESHOOTING.md`:

```markdown
# Troubleshooting

## Common Issues

### Issue: [Description]
**Symptom:** [What you see]
**Cause:** [Why it happens]
**Solution:**
```bash
[Fix commands]
```

### Issue: [Description]
**Symptom:** [What you see]
**Cause:** [Why it happens]
**Solution:** [Fix steps]

## Environment Setup Issues

### [Platform/Tool] Not Working
[Solution]

## Build/Runtime Errors

### Error: [Error message]
[Cause and fix]

## Known Limitations
- [Limitation 1]: [Workaround]
- [Limitation 2]: [Workaround]

## Debug Tips
- [Tip 1]
- [Tip 2]

## Getting Help
- Check: [where to look]
- Ask: [how to get help]
```

### Step 7: Create Root CLAUDE.md

Write to `$PROJECT_PATH/CLAUDE.md`:

```markdown
# Claude Instructions for [Project Name]

## Project Context
This is [brief description]. Located at `~/local_workspaces/[project]`.

## First Steps
1. Read `.claude/sessions/latest.md` for current context
2. Run `git status` to see current state
3. Review `.claude/PROJECT.md` for architecture

## Key Commands
```bash
# Build
[command]

# Test
[command]

# Run
[command]
```

## Important Files
- [file]: [why important]

## Constraints
- [Any limitations or things to avoid]

## Skills
Check `~/local_workspaces/skills/[project]/SKILL.md` for project-specific automation.
```

### Step 8: Create Initial Session

Write to `$PROJECT_PATH/.claude/sessions/latest.md`:

```markdown
# Session Handoff: [DATE]

## Summary
Initial project documentation created.

## Project Status
- Documentation: Initialized
- Ready for development

## Next Steps
1. Review and update PROJECT.md with accurate details
2. Add project-specific conventions
3. Document any known issues
```

### Step 9: Update .gitignore (Optional)

Add to `.gitignore` if session history should be local-only:

```
# Keep latest.md, ignore archive
.claude/sessions/archive/
```

### Step 10: Confirm to User

```
Project documentation initialized:

Created:
  .claude/PROJECT.md          - Edit with project details
  .claude/CONVENTIONS.md      - Edit with code style
  .claude/TROUBLESHOOTING.md  - Add known issues
  .claude/sessions/latest.md  - Current context
  CLAUDE.md                   - Agent instructions

Next: Review and update each file with accurate project information.
```

## Templates Quick Reference

All templates use placeholders:
- `[Project Name]` - Replace with actual name
- `[Description]` - Fill in details
- `[command]` - Add actual commands

## Maintenance

After initialization:
1. Agent should review and fill in accurate details
2. Update as project evolves
3. Use `session-save` to maintain context
