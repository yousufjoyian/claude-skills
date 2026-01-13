# File Creation Discipline (CONCEPT SKILL - Not Yet Implemented)

## The Problem This Would Solve

Claude creates files chaotically during work:
- Random locations (current directory, /tmp, Desktop)
- Poor naming (test.py, output.txt, data.csv)
- No organization structure
- Leaves temporary files everywhere
- User forced to clean up afterwards

## What It Would Do

**Before creating ANY file**, Claude would:

1. **Determine File Type**
   - Temporary/scratch file (delete after session)
   - Output/result file (keep, user needs this)
   - Source code (part of project structure)
   - Data file (needs organized storage)
   - Test file (goes in tests/ folder)

2. **Choose Appropriate Location**
   ```
   Project structure:
   ./
   ├── src/           # Source code
   ├── tests/         # Test files
   ├── data/          # Input data
   ├── output/        # Results/reports
   ├── scratch/       # Temporary files (gitignored)
   └── docs/          # Documentation
   ```

3. **Use Descriptive Names**
   - ❌ `test.py`
   - ✅ `test_user_authentication.py`

   - ❌ `output.txt`
   - ✅ `2024-11-02_analysis_results.txt`

   - ❌ `data.csv`
   - ✅ `customer_transactions_oct2024.csv`

4. **Ask Before Creating Project Structure**
   ```
   "I'm about to create several files for this analysis.
    Should I set up a project structure first?

    Proposed structure:
    ./dashcam-analysis/
    ├── scripts/       # Python analysis scripts
    ├── data/          # Input video files
    ├── output/        # Extracted frames, reports
    └── scratch/       # Temporary processing files

    Proceed? (y/n)"
   ```

5. **Announce File Creation**
   ```
   "Creating: ./output/2024-11-02_gps_timeline_report.txt"
   "Creating: ./scratch/temp_processing.json (will be deleted)"
   "Creating: ./src/video_analyzer.py"
   ```

6. **Clean Up Temporary Files**
   At end of session:
   ```
   "Session complete. I created 3 temporary files in ./scratch/:
   - temp_processing.json
   - intermediate_results.csv
   - debug_output.txt

   Delete these? (y/n)"
   ```

## Rules

### File Naming Convention
```
Format: {date}_{description}_{version}.{ext}

Examples:
- 2024-11-02_customer_analysis_v1.py
- 2024-11-02_sales_report_final.pdf
- 2024-11-02_debug_log.txt
```

### Location Policy

**Source Code:**
- Goes in `src/` or root if single-file project
- Never in /tmp or Downloads

**Test Files:**
- Goes in `tests/`
- Named: `test_{what_being_tested}.py`

**Output/Results:**
- Goes in `output/` or `results/`
- Dated and descriptive

**Temporary/Scratch:**
- Goes in `scratch/` or `/tmp/`
- Clearly marked as deletable
- Cleaned up before session end

**Data Files:**
- Goes in `data/` or `input/`
- Never overwrite originals

### Project Structure Decision Tree

```
Single file task (< 3 files)?
├─ Yes → Create in current directory with good names
└─ No → Propose project structure first

New project?
├─ Yes → Set up full structure before creating files
└─ No → Follow existing project structure

Multiple related files?
├─ Yes → Group in subfolder
└─ No → Current directory OK
```

## Example: Before and After

### ❌ WITHOUT This Skill

User: "Analyze this video for human detection"

Claude:
```bash
# Creates files randomly
python analyze.py         # Root directory
output.txt               # Root directory
test.py                  # Root directory
data.json                # Root directory
temp.mp4                 # Root directory (2GB!)
results_final.csv        # Root directory
results_final_v2.csv     # Root directory
```

Result: **7 files polluting root directory, unclear purpose, 2GB temp file left behind**

### ✅ WITH This Skill

User: "Analyze this video for human detection"

Claude:
```
I'll create a project structure for this analysis:

./human-detection/
├── src/
│   └── analyze_video.py
├── data/
│   └── input.mp4 (symlink to your video)
├── output/
│   └── 2024-11-02_detection_results.csv
└── scratch/
    └── temp_frames/ (deleted after processing)

Proceed? (y/n)
```

User: "y"

Claude:
```bash
mkdir -p human-detection/{src,data,output,scratch}
# Creates files in organized structure
# Announces each creation
# Cleans up scratch files at end
```

Result: **Clean project structure, clear organization, no pollution**

## Integration with Existing Workflows

### Works With Git
- Respects .gitignore
- Puts temp files in gitignored locations
- Creates .gitignore if project needs one

### Works With Existing Projects
```bash
# Detects existing structure
ls -la

# Finds: src/, tests/, data/ already exist
# Follows existing pattern instead of creating new structure
```

### Adapts to User Preferences
After a few sessions, learns your patterns:
- "You usually put scripts in ./scripts/"
- "You prefer YYYY-MM-DD naming"
- "You keep temp files in /tmp/"

## When to Use This Skill

**Auto-trigger for:**
- About to create 3+ files
- Creating any file outside current directory
- Creating files in user's home directory or Desktop
- About to generate large files (>100MB)

**Always active for:**
- File naming (enforce descriptive names)
- Location decisions (prevent chaos)
- Temporary file tracking (cleanup at end)

---

**This is what you ACTUALLY need.**

Your current file-organizer skill is a mop.
You need a skill that prevents the mess in the first place.
