---
name: git-commit
description: Smart git commit workflow with staging, message crafting, and safety checks
---

# Git Commit Skill

Smart commit workflow that stages changes, crafts commit messages, and handles edge cases safely.

## Triggers

- "commit"
- "commit changes"
- "git commit"
- "save my changes"
- "commit this"
- "commit and push" (includes automatic push to origin)

## What This Skill Does

1. **Analyzes Changes**: Shows what's modified, staged, and untracked
2. **Smart Staging**: Stages relevant files, excludes secrets
3. **Message Crafting**: Creates conventional commit messages
4. **Safety Checks**: Prevents dangerous operations
5. **Co-authoring**: Adds Claude co-author attribution
6. **Auto-Push**: If "commit and push" trigger used, pushes to origin after commit

## Workflow

### Step 1: Assess Current State

```bash
# Check working directory
git status

# See staged changes
git diff --cached --stat

# See unstaged changes
git diff --stat

# Recent commits for style reference
git log --oneline -5
```

### Step 2: Stage Changes

```bash
# Stage all modified/new files
git add -A

# Or stage specific files
git add <file1> <file2>
```

**Exclude from staging:**
- `.env`, `.env.*` - environment secrets
- `credentials.json`, `*_secret.json` - API keys
- `*.pem`, `*.key` - certificates
- `node_modules/`, `__pycache__/` - dependencies

If user tries to commit secrets, WARN:
> "Found potential secrets in staging: `.env`. Remove with `git reset HEAD .env` before committing."

### Step 3: Craft Commit Message

Use **Conventional Commits** format:

```
<type>(<scope>): <description>

[optional body]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

**Types:**
| Type | When to Use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructuring (no behavior change) |
| `docs` | Documentation only |
| `style` | Formatting, whitespace |
| `test` | Adding/fixing tests |
| `chore` | Build, config, dependencies |
| `perf` | Performance improvement |

**Examples:**
- `feat(auth): add OAuth2 login flow`
- `fix(api): handle null response from server`
- `refactor(utils): extract date formatting helpers`
- `docs(readme): add installation instructions`

### Step 4: Commit

```bash
git commit -m "$(cat <<'EOF'
feat(scope): short description

Optional longer explanation of what changed and why.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

### Step 5: Verify

```bash
# Confirm commit succeeded
git log -1 --stat

# Check status is clean
git status
```

### Step 6: Push (if "commit and push" trigger)

If the user said "commit and push", automatically push after successful commit:

```bash
git push origin main
```

Report the push result to user.

## Safety Rules

### NEVER Do These:
- `git commit --amend` on pushed commits
- `git push --force` without explicit user request
- Commit files matching secret patterns
- Skip pre-commit hooks (`--no-verify`)
- Commit to main/master without confirmation

### ALWAYS Do These:
- Read files before committing
- Show diff summary before committing
- Use HEREDOC for multi-line messages
- Verify commit succeeded after

## Handling Pre-Commit Hook Failures

If commit is rejected by hooks:

1. **Do NOT use `--no-verify`**
2. Read the hook output to understand the issue
3. Fix the issue (formatting, linting, tests)
4. Create a NEW commit (don't amend)
5. Stage the fixes and commit again

## Amend Rules

Only use `git commit --amend` when ALL conditions are met:
1. User explicitly requested amend
2. HEAD commit was created in this session
3. Commit has NOT been pushed to remote
4. Pre-commit hook auto-modified files that need including

## Example Session

**User**: "commit"

**Assistant**:
```
Let me check the current state...

$ git status
On branch main
Changes not staged for commit:
  modified:   src/App.tsx
  modified:   src/components/Header.tsx
Untracked files:
  src/utils/helpers.ts

$ git diff --stat
 src/App.tsx              | 15 +++++++++------
 src/components/Header.tsx |  8 +++++---

Recent commits:
abc1234 feat(ui): add dark mode toggle
def5678 fix(api): handle timeout errors

Staging all changes...
$ git add -A

Creating commit...
$ git commit -m "feat(components): improve header layout and add helpers

- Refactor App.tsx for cleaner structure
- Update Header component spacing
- Add new utility helpers module

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

[main 9a8b7c6] feat(components): improve header layout and add helpers
 3 files changed, 45 insertions(+), 12 deletions(-)
 create mode 100644 src/utils/helpers.ts

Done! Commit 9a8b7c6 created.
```

## Integration with GitHub Skill

- **"commit and push"** → This skill handles both commit AND push automatically
- **"commit"** alone → Local commit only, use "push" separately if needed
- **"push"** → triggers `github` skill for push-only operations

## Quick Reference

| Command | Action |
|---------|--------|
| "commit" | Full workflow (local only) |
| "commit and push" | Full workflow + push to origin |
| "commit these files" | Commit specific files |
| "amend" | Amend last commit (if safe) |
| "what changed" | Show diff without committing |
| "undo last commit" | `git reset --soft HEAD~1` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "nothing to commit" | Check if files are saved, or already committed |
| Pre-commit hook fails | Fix issues, stage, commit again (no amend) |
| Merge conflict | Resolve conflicts first, then commit |
| Detached HEAD | `git checkout main` first |
| Wrong branch | `git checkout <correct-branch>` |
