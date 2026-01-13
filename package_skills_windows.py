#!/usr/bin/env python3
"""
Windows-compatible skill packager
Creates distributable zip files for Claude skills
"""

import sys
import zipfile
from pathlib import Path
import re


def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read and validate frontmatter
    content = skill_md.read_text(encoding='utf-8')
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter = match.group(1)

    # Check required fields
    if 'name:' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description:' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Extract name for validation
    name_match = re.search(r'name:\s*(.+)', frontmatter)
    if name_match:
        name = name_match.group(1).strip()
        # Check naming convention
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be hyphen-case"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' has invalid hyphen placement"

    # Extract and validate description
    desc_match = re.search(r'description:\s*(.+)', frontmatter)
    if desc_match:
        description = desc_match.group(1).strip()
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets"

    return True, "Skill is valid"


def package_skill(skill_path, output_dir):
    """Package a skill folder into a zip file"""
    skill_path = Path(skill_path).resolve()

    # Validate skill folder exists
    if not skill_path.exists():
        print(f"ERROR: Skill folder not found: {skill_path}")
        return None

    if not skill_path.is_dir():
        print(f"ERROR: Path is not a directory: {skill_path}")
        return None

    # Validate SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"ERROR: SKILL.md not found in {skill_path}")
        return None

    # Run validation before packaging
    print(f"Validating {skill_path.name}...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"VALIDATION FAILED: {message}")
        return None
    print(f"  {message}")

    # Determine output location
    skill_name = skill_path.name
    output_path = Path(output_dir).resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    zip_filename = output_path / f"{skill_name}.zip"

    # Create the zip file
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through the skill directory
            for file_path in skill_path.rglob('*'):
                if file_path.is_file():
                    # Calculate the relative path within the zip
                    arcname = file_path.relative_to(skill_path.parent)
                    zipf.write(file_path, arcname)

        print(f"SUCCESS: Packaged to {zip_filename}\n")
        return zip_filename

    except Exception as e:
        print(f"ERROR creating zip: {e}")
        return None


def main():
    if len(sys.argv) < 3:
        print("Usage: python package_skills_windows.py <skill-path> <output-dir>")
        print("   Or: python package_skills_windows.py ALL <output-dir>")
        sys.exit(1)

    skill_arg = sys.argv[1]
    output_dir = sys.argv[2]

    if skill_arg == "ALL":
        # Package all skills in the skills directory
        skills_dir = Path(__file__).parent
        skill_folders = [d for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]

        print(f"Found {len(skill_folders)} skills to package\n")

        success_count = 0
        failed_skills = []

        for skill_folder in sorted(skill_folders):
            result = package_skill(skill_folder, output_dir)
            if result:
                success_count += 1
            else:
                failed_skills.append(skill_folder.name)

        print(f"\n{'='*60}")
        print(f"SUMMARY: {success_count}/{len(skill_folders)} skills packaged successfully")
        if failed_skills:
            print(f"Failed skills: {', '.join(failed_skills)}")
        print(f"Output directory: {Path(output_dir).resolve()}")

    else:
        # Package single skill
        result = package_skill(skill_arg, output_dir)
        if not result:
            sys.exit(1)


if __name__ == "__main__":
    main()
