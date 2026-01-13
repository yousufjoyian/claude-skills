# Claude.ai Upload Priority Guide

## ✅ Fixed for Claude.ai Compatibility

All 35 skills have been updated to only use allowed frontmatter fields:
- ✅ `name`
- ✅ `description`
- ✅ `license` (optional)
- ✅ `allowed-tools` (optional)
- ✅ `metadata` (optional)

**Removed fields:** `when_to_use`, `version`, `languages`, `author`, `tags`, `dependencies`

---

## 🎯 Upload Priority (For Personal Use)

### **Phase 1: Test the System (Upload 1-3 skills first)**

Upload these to verify claude.ai skill system works as expected:

1. **verification-before-completion.zip** ⭐⭐⭐
   - Simple, no dependencies
   - Stops Claude from claiming "done" without checking
   - Universal benefit across all tasks

2. **systematic-debugging.zip** ⭐⭐⭐
   - Behavioral change: find root cause before fixing
   - Applicable whenever debugging anything
   - Prevents symptom-fixing

3. **audio-transcriber.zip** ⭐⭐
   - Complex skill with scripts/references
   - Tests if your dashcam workflows actually work
   - Will reveal if script paths/dependencies are issues

**STOP HERE** - Use Claude for 2-3 days with just these 3 skills. Observe:
- Does Claude actually reference them automatically?
- Do the scripts work or fail due to path/dependency issues?
- Is there noticeable context overhead?

---

### **Phase 2: Your Core Workflows (Upload 5-8 more)**

Based on what you actually use Claude for daily:

#### **If you code regularly:**
4. **test-driven-development.zip**
5. **defense-in-depth.zip**
6. **root-cause-tracing.zip**

#### **If you work with dashcam data:**
7. **dashcam-sync.zip** - File management
8. **gps-timeline-analyzer.zip** - Location analysis
9. **human-extractor.zip** - Video processing
10. **motion-sampler.zip** - Frame extraction

#### **If you work with documents:**
11. **pdf.zip** - Most universal
12. **docx.zip** - Word documents
13. **xlsx.zip** - Spreadsheets
14. **pptx.zip** - Presentations

---

### **Phase 3: Nice-to-Have (Upload as needed)**

#### **Testing Skills:**
- **testing-anti-patterns.zip** - Avoid common test mistakes
- **condition-based-waiting.zip** - Reliable async tests

#### **Meta/Builder Skills:**
- **skill-creator.zip** - If building more skills
- **mcp-builder.zip** - If building MCP servers
- **markdown-to-epub.zip** - If converting docs to ebooks

#### **Utility Skills:**
- **file-organizer.zip**
- **image-enhancer.zip**
- **video-downloader.zip**
- **youtube-transcript.zip**
- **csv-data-summarizer.zip**
- **playwright-skill.zip** - Browser automation

#### **Other Debugging:**
- **using-tmux-for-interactive-commands.zip**
- **internal-comms.zip**

---

### **Phase 4: Advanced (Optional)**

#### **Problem-Solving Frameworks:**
⚠️ These are abstract thinking aids, not automatic workflows. You'll need to consciously invoke them.

- **when-stuck.zip** - Dispatch to right technique
- **collision-zone-thinking.zip** - Force concept collisions
- **inversion-exercise.zip** - Flip assumptions
- **meta-pattern-recognition.zip** - Spot universal patterns
- **scale-game.zip** - Test at extremes
- **simplification-cascades.zip** - Find unifying insights
- **tracing-knowledge-lineages.zip** - Understand idea evolution

#### **Controversial:**
- **using-skills.zip** - Meta-skill about using skills
  - Could be useful to remind Claude to check skills before tasks
  - Or could be redundant overhead
  - Upload LAST, only if you notice Claude ignoring your other skills

---

## 🚨 Critical Questions to Answer

After uploading Phase 1 (3 skills), test and document:

### **1. Discovery/Activation**
- ❓ Does Claude automatically detect when to use each skill?
- ❓ Or do you need to manually say "use the debugging skill"?
- ❓ Can you see which skills are active in a conversation?

### **2. Script Execution**
- ❓ Do skills with `scripts/` folders work in claude.ai?
- ❓ Do paths like `G:\My Drive\...` work or fail?
- ❓ Are Python dependencies (torch, faster-whisper, etc.) available?

### **3. Context Overhead**
- ❓ With 3 skills loaded, are responses noticeably slower?
- ❓ What happens if you load all 35 skills?

### **4. Real-World Usage**
- ❓ Did verification-before-completion actually prevent a mistake?
- ❓ Did systematic-debugging change how Claude approached a bug?
- ❓ Are the skills being used or ignored?

---

## 📊 My Predictions

**What will work:**
- ✅ verification-before-completion (simple behavioral change)
- ✅ systematic-debugging (structured workflow)
- ✅ Document skills (if you avoid script dependencies)

**What might fail:**
- ❌ Dashcam skills with hardcoded paths (`G:\My Drive\...`)
- ❌ Skills requiring GPU/CUDA (human-extractor, audio-transcriber)
- ❌ Skills with custom dependencies not in claude.ai environment

**What might be ignored:**
- 😴 Problem-solving frameworks (too abstract to auto-trigger)
- 😴 using-skills (meta-enforcement without infrastructure)

---

## 🎯 Recommended First Upload

**Start with just this ONE skill:**

### `verification-before-completion.zip`

**Why:**
1. Simplest test case
2. No dependencies, no scripts
3. Clear behavioral change you can observe
4. Universal benefit

**Upload it, then ask Claude to:**
- "Fix this Python function to handle edge cases"
- Watch if Claude actually runs tests before saying "done"

**If it works:** Claude will verify before claiming success ✅
**If it doesn't:** You know the skill system needs debugging ❌

Then decide whether to upload more.

---

## 📁 Location
All claude.ai-compatible skills are in:
```
G:\My Drive\PROJECTS\skills\skill-zips-claude-ai\
```

Each zip is ready to upload to https://claude.ai/settings/capabilities

---

**Next Step:** Upload `verification-before-completion.zip` and report back what happens!
