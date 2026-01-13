#!/usr/bin/env python3
"""
Fix skills for claude.ai compatibility by removing invalid frontmatter fields.

Claude.ai only allows: name, description, license, allowed-tools, metadata
This script removes: when_to_use, version, languages, author, tags, etc.
"""

import re
import sys
from pathlib import Path


ALLOWED_FIELDS = {'name', 'description', 'license', 'allowed-tools', 'metadata'}


def fix_skill_frontmatter(skill_md_path):
    """Fix SKILL.md frontmatter to only include claude.ai-allowed fields"""

    skill_md_path = Path(skill_md_path)

    if not skill_md_path.exists():
        print(f"ERROR: {skill_md_path} not found")
        return False

    # Read file
    content = skill_md_path.read_text(encoding='utf-8')

    # Check for frontmatter
    if not content.startswith('---'):
        print(f"SKIP: {skill_md_path.parent.name} - No frontmatter")
        return True

    # Extract frontmatter and body
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not match:
        print(f"ERROR: {skill_md_path.parent.name} - Invalid frontmatter format")
        return False

    frontmatter = match.group(1)
    body = match.group(2)

    # Parse frontmatter lines
    lines = frontmatter.split('\n')
    new_lines = []
    removed_fields = []

    for line in lines:
        if ':' in line:
            field_name = line.split(':', 1)[0].strip()
            if field_name in ALLOWED_FIELDS:
                new_lines.append(line)
            else:
                removed_fields.append(field_name)
        else:
            # Keep non-field lines (like multi-line values)
            if new_lines:  # Only if we've started collecting fields
                new_lines.append(line)

    if not removed_fields:
        print(f"OK: {skill_md_path.parent.name} - Already compatible")
        return True

    # Reconstruct file
    new_frontmatter = '\n'.join(new_lines)
    new_content = f"---\n{new_frontmatter}\n---\n{body}"

    # Write back
    skill_md_path.write_text(new_content, encoding='utf-8')

    print(f"FIXED: {skill_md_path.parent.name} - Removed: {', '.join(removed_fields)}")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_for_claude_ai.py <skill-folder-or-ALL>")
        print("\nExamples:")
        print("  python fix_for_claude_ai.py debugging/systematic-debugging")
        print("  python fix_for_claude_ai.py ALL")
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "ALL":
        # Fix all skills
        skills_dir = Path(__file__).parent
        skill_files = list(skills_dir.glob('**/SKILL.md'))

        # Filter out skill-zips directory
        skill_files = [f for f in skill_files if 'skill-zips' not in f.parts]

        print(f"Found {len(skill_files)} SKILL.md files\n")

        success_count = 0
        for skill_file in sorted(skill_files):
            if fix_skill_frontmatter(skill_file):
                success_count += 1

        print(f"\n{'='*60}")
        print(f"SUMMARY: {success_count}/{len(skill_files)} skills processed")

    else:
        # Fix single skill
        skill_path = Path(arg)
        skill_md = skill_path / 'SKILL.md'

        if not skill_md.exists():
            print(f"ERROR: SKILL.md not found in {skill_path}")
            sys.exit(1)

        if fix_skill_frontmatter(skill_md):
            print("\nSUCCESS: Skill is now claude.ai compatible")
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
