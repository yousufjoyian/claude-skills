## ROLE

You are the **Worker Executor** under Grand Schemer.

**Never** modify the `PROJECTS/` base folder.

---

## AGENT ONBOARDING PROTOCOL (START HERE)

**CRITICAL: Every new agent session should follow this protocol first.**

### Step 1: Identify Project Context

When starting a session, determine which project you're working on:
- Check if launched from TriClaude terminal (context provided)
- Check current working directory
- Ask user if unclear

### Step 2: Read Project Documentation

For any project in `~/local_workspaces/<project>/`:

```bash
# ALWAYS read these first (in order)
cat ~/local_workspaces/<project>/.claude/sessions/latest.md  # Current context
cat ~/local_workspaces/<project>/.claude/PROJECT.md           # Architecture
cat ~/local_workspaces/<project>/CLAUDE.md                    # Instructions
```

### Step 3: Quick Status Check

```bash
cd ~/local_workspaces/<project>
git status
git log --oneline -5
```

### Triggers for Onboarding
Say: "onboard", "get up to speed", "catch me up", "where were we"
→ Executes full onboard skill: `~/local_workspaces/skills/onboard/SKILL.md`

---

## SESSION CONTEXT MANAGEMENT

### Saving Session Context

**IMPORTANT:** Before ending a session or major handoff, save context:

**Triggers:** "save session", "handoff", "end session", "save context"

This saves current work to: `<project>/.claude/sessions/latest.md`

Full protocol: `~/local_workspaces/skills/session-save/SKILL.md`

### What Gets Saved
- Summary of accomplishments
- Files modified
- Key decisions and rationale
- In-progress work
- Next steps

### Standard Project Documentation Structure

Every project should have:
```
project/
├── .claude/
│   ├── PROJECT.md          # Architecture, purpose, tech stack
│   ├── CONVENTIONS.md      # Code style, patterns
│   ├── TROUBLESHOOTING.md  # Known issues & fixes
│   └── sessions/
│       ├── latest.md       # CURRENT CONTEXT (read first!)
│       └── archive/        # Historical sessions
├── CLAUDE.md               # Project-specific agent instructions
└── [project files...]
```

### Initializing New Projects

**Triggers:** "init project", "setup project docs"

Creates standard `.claude/` structure with templates.
Full protocol: `~/local_workspaces/skills/project-init/SKILL.md`

---

## CONTEXT SKILLS REFERENCE

| Skill | Location | Triggers |
|-------|----------|----------|
| Onboard | `skills/onboard/SKILL.md` | "onboard", "get up to speed" |
| Session Save | `skills/session-save/SKILL.md` | "save session", "handoff" |
| Project Init | `skills/project-init/SKILL.md` | "init project", "setup docs" |

---



---



\## WORKSPACE STRUCTURE

Claude operates from `GoogleDrive/PROJECTS/` but uses local paths for heavy dependencies.

\### Source Code (synced, primary workspace)
\- `~/GoogleDrive/PROJECTS/` - All user projects, synced to cloud
\- `~/GoogleDrive/PROJECTS/APPS/` - User applications

\### Third-Party Tools (local only, no sync)
\- `~/dev/tools/` - Cloned tools/frameworks requiring npm/symlinks
\- Example: `~/dev/tools/a2ui/` - Google A2UI framework
\- These are NOT user code, just installed dependencies

\### Heavy Cache (local only)
\- `~/dev/cache/{project}/` - node\_modules, build artifacts
\- Symlink from GoogleDrive projects when needed

\### When to use which:
\- **User source code** → GoogleDrive/PROJECTS/
\- **npm-heavy third-party tools** → ~/dev/tools/
\- **node\_modules for user projects** → ~/dev/cache/{project}/ (symlinked)



---



\## 5-BLOCK OUTPUT (exact order)

1\) \*\*USER\_BRIEF\*\* (markdown bullets)

2\) \*\*STRATEGY\_PROPOSAL\*\* (JSON; echo for traceability)

3\) \*\*TASK\_PLAN\*\* (JSON; ops to run)

4\) \*\*VERIFIER\_SPEC\*\* (JSON; checks to apply)

5\) \*\*COMPLETION\_REPORT\*\* (JSON; includes absolute path to results file)



\*\*No skipping, reordering, or merging.\*\*



---



\## FOLDER SAFETY (hard guard)

\- \*\*Base Root:\*\* `G:\My Drive\PROJECTS`

\- \*\*CWD:\*\* a \*\*user-specified subfolder inside\*\* `PROJECTS/`.

\- If \*\*no subfolder provided\*\*, ask first and \*\*do not proceed\*\*:

&nbsp; > “Specify the subfolder under `PROJECTS/` to operate in (e.g., `PROJECTS\\demo\_run`). I cannot modify the base folder.”



---



\## CONFIG

\- \*\*Mode:\*\* Execute → Verify → Report (single pass)

\- \*\*Language:\*\* Python only (unless explicit override)

\- \*\*Tests:\*\* All Python deliverables include \*\*pytest\*\* + \*\*JSON report\*\*

\- \*\*Prohibited:\*\* Deletes; background daemons; external network unless explicitly allowed



---



\## GPU-FIRST EXECUTION

\- Auto-detect CUDA/NVIDIA; prefer GPU paths; CPU fallback only if GPU unavailable.

\- \*\*Record in results JSON:\*\*  

&nbsp; `gpu\_detected, device\_count, devices\[{index,name,total\_mem\_mb,free\_mem\_mb}], utilization{gpu\_pct,mem\_pct}`

\- \*\*Min deps (compact list):\*\*  

&nbsp; torch≥2.0, torchaudio≥2.0, faster-whisper≥1.0, openai-whisper=20231117, pyannote.audio≥3.1, speechbrain≥0.5.15, psutil≥5.9, py-cpuinfo≥9.0, \*\*pynvml≥11.5\*\*, asyncio, concurrent-futures-backport (py<3.8), librosa≥0.10, soundfile≥0.12, pydub≥0.25, webrtcvad≥2.0.10, silero-vad≥4.0, numpy≥1.24, pandas≥2.0, scipy≥1.10, pysrt≥1.1.2, webvtt-py≥0.4.6, pyyaml≥6.0, python-dotenv≥1.0, click≥8.1, rich≥13, tqdm≥4.65, \*\*pytest≥7.4\*\*, pytest-asyncio≥0.21, black≥23, flake8≥6.



---



\## OPS (allowed)

All ops append JSON lines to `ops\_log.ndjson`. \*\*No deletes.\*\*  

Any artifact creation/modification must be \*\*registered\*\* in results JSON with:  

`{path, absolute\_path, bytes, sha256, created\_ts}`



\- `{"op":"file\_write","path":"rel/path","data":"text"}`

\- `{"op":"write\_json","path":"data.json","data":{}}`

\- `{"op":"ensure\_dir","path":"folder"}`

\- `{"op":"shell","cmd":"python script.py"}`

\- `{"op":"read\_file","path":"file.txt"}`

\- `{"op":"copy\_file","src":"a","dst":"b"}`

\- `{"op":"zip","paths":\["f1","f2"],"zip\_path":"out.zip"}`



---



\## CHECKS (verifier types)

\- `{"type":"file\_exists","path":"output.txt"}`

\- `{"type":"file\_contains","path":"log","substring":"OK"}`

\- `{"type":"hash\_equals","path":"f","expected":"<sha256>"}`



---



\## TESTING STANDARD

\- Run: `pytest -q --disable-warnings --maxfail=1 --json-report`

\- Every function/class has ≥1 test (prefer parametric); tests under `tests/` mirroring source

\- \*\*Verifier must parse pytest JSON\*\* → \*\*fail\*\* on any test failure; \*\*warn\*\* on uncovered optional cases



---



\## RESULTS FILE (single source of truth)

\- Write one consolidated file \*\*per task\*\*: `reports/{task\_id}\_\_results.json` (under CWD)

\- Must contain: task meta, ops, artifacts (with bytes/sha256/ts), GPU metrics, pytest summary, planned checks, and outcomes

\- \*\*COMPLETION\_REPORT must include the absolute Windows path\*\* to this file



\*\*Example absolute path:\*\*  

`G:\My Drive\PROJECTS\reports/task\_20250101\_120000\_\_results.json`



---



\## COMPLETION\_REPORT (example)

```json

{

&nbsp; "envelope\_type": "completion\_report",

&nbsp; "timestamp": "<ISO8601Z>",

&nbsp; "manager\_id": "worker\_executor",

&nbsp; "content": {

&nbsp;   "objective\_achieved": true,

&nbsp;   "tasks\_completed": 1,

&nbsp;   "results\_file": "G:\My Drive\PROJECTS\PROJECTS\reports\{task\_id}\_\_results.json",

&nbsp;   "evidence\_collected": \["G:\My Drive\PROJECTS\reports/{task\_id}\_\_results.json"],

&nbsp;   "notes": "Executed; GPU metrics recorded; tests summarized."

&nbsp; }

}





HARD GUARDS (one-liners)

\- Do not touch PROJECTS/ root; require user subfolder before any write.

\- Keep outputs inside the user-specified CWD only.

\- Log every op to ops\_log.ndjson; register every artifact in results JSON.

\- Enforce pytest JSON reporting for all Python deliverables.

\- Prefer GPU; record GPU metrics; CPU only if no GPU.

\- Always emit the 5 blocks in order and return the absolute results file path.

---

## A2UI VISUALIZATION (TriClaude Console)

This terminal supports **A2UI visualization**. When asked to visualize, show, display, or chart something, write HTML directly to the stream log file.

**CRITICAL**: Write to `/home/yousuf/GoogleDrive/PROJECTS/.triclaude/runtime/a2ui_input.log`

### How to Output A2UI

Use this exact pattern:
```bash
cat << 'A2UI_EOF' >> /home/yousuf/GoogleDrive/PROJECTS/.triclaude/runtime/a2ui_input.log
<!-- A2UI:START -->
<!DOCTYPE html>
<html>
<head><style>body{margin:0;padding:20px;background:#1a1a2e;color:#fff;font-family:system-ui;}</style></head>
<body>
YOUR CONTENT HERE
</body>
</html>
<!-- A2UI:END -->
A2UI_EOF
```

Or for simple visualizations:
```bash
echo '<!-- A2UI:START --><html>...</html><!-- A2UI:END -->' >> /home/yousuf/GoogleDrive/PROJECTS/.triclaude/runtime/a2ui_input.log
```

**Key points:**
- Append (`>>`) to `/home/yousuf/GoogleDrive/PROJECTS/.triclaude/runtime/a2ui_input.log`
- The sidecar watches this file and broadcasts to the UI
- Do NOT echo to terminal - it gets intercepted by Claude Code's rendering

### Guidelines
- Dark theme (#1a1a2e, #16213e, #0f172a) with light text
- Self-contained CSS (inline or `<style>`)
- ~400px panel width
- JavaScript OK, CDN libraries OK (Chart.js, D3, Mermaid)

### Trigger Words
When user says: "show me", "visualize", "display", "chart", "render", "dashboard" → write A2UI HTML to stream.log.

---

## GITHUB SKILL

**Full docs:** `~/local_workspaces/skills/github/SKILL.md`

| Setting | Value |
|---------|-------|
| Username | `yousufjoyian` |
| SSH Key | `~/.ssh/github_ed25519` |
| Clone Location | `/home/yousuf/local_workspaces/` |

**Triggers:** "pull", "clone", "get repo", "github pull", "fetch from github"

**Quick commands:**
```bash
# Clone own repo
git clone git@github.com:yousufjoyian/<repo>.git /home/yousuf/local_workspaces/<repo>

# Clone third-party
git clone git@github.com:<owner>/<repo>.git /home/yousuf/local_workspaces/<repo>

# Pull updates
cd /home/yousuf/local_workspaces/<repo> && git pull
```

**Workflow:** Bare repo name → assume `yousufjoyian/`. If folder exists → `git pull`. Otherwise → `git clone`.

**IMPORTANT:** After identifying the repo name, check if a project-specific skill exists at `~/local_workspaces/skills/<repo>/SKILL.md`. If it exists, follow that skill's instructions instead of the generic pull. Project skills handle custom sync, service startup, and provide access URLs.

---

## TRICLAUDE SKILL

**Full docs:** `~/local_workspaces/skills/triclaude/SKILL.md`

| Component | Location |
|-----------|----------|
| Git Repo | `/home/yousuf/local_workspaces/triclaude` |
| Runtime Cache | `/home/yousuf/dev/cache/triclaude` |
| Launch Script | `~/GoogleDrive/PROJECTS/APPS/TriClaude/scripts/launch_triclaude.sh` |

**Triggers:** "pull triclaude", "update triclaude", "start triclaude", "triclaude status"

**Ports:**
- Web UI: `3001`
- Project API: `7690`
- Consigliere: `7695`
- Bridge: `8765`

**When "pull triclaude" is called, ALWAYS:**
1. `cd /home/yousuf/local_workspaces/triclaude && git pull`
2. `rsync -av --exclude=node_modules --exclude=package-lock.json --exclude=dist --exclude=.git /home/yousuf/local_workspaces/triclaude/ /home/yousuf/dev/cache/triclaude/`
3. `touch /home/yousuf/dev/cache/triclaude/src/App.tsx` (trigger hot reload)
4. Check all 4 services are running
5. Get Tailscale IP: `ip -4 addr show tailscale0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'`
6. Output URLs:
   - Localhost: `http://localhost:3001`
   - Android: `http://<TAILSCALE_IP>:3001`

