# Claude Skills & Workspace Config

This repo contains:
- **WORKSPACE.md** - Global Claude instructions (symlink to ~/local_workspaces/CLAUDE.md)
- **Skills** - Reusable automation skills for Claude agents

## Setup

```bash
# Clone to local_workspaces
git clone git@github.com:yousufjoyian/claude-skills.git ~/local_workspaces/skills

# Symlink global CLAUDE.md
ln -sf ~/local_workspaces/skills/WORKSPACE.md ~/local_workspaces/CLAUDE.md
```

## Skills

| Skill | Purpose |
|-------|---------|
| `onboard/` | Get up to speed on any project |
| `session-save/` | Save current session context |
| `project-init/` | Initialize project documentation |
| `triclaude/` | TriClaude-specific operations |
| `github/` | GitHub clone/pull operations |

## Standard Project Structure

Every project should have:
```
project/
├── .claude/
│   ├── PROJECT.md
│   ├── CONVENTIONS.md
│   ├── TROUBLESHOOTING.md
│   └── sessions/latest.md
└── CLAUDE.md
```
