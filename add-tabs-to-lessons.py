# Claude is Work to Build this Project
#!/usr/bin/env python3
"""
Script to add tabs (Original, Summary, Personalized) to all Part 1 lesson pages
"""

import os
import re
from pathlib import Path

# Base directory
DOCS_DIR = Path(r"P:\Book Agent\ai-native-software-development\book-source\docs\01-Introducing-AI-Driven-Development")

# Tab template to add after frontmatter
TABS_HEADER = """
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import SummaryTab from '@site/src/components/SummaryTab';

<Tabs>
  <TabItem value="original" label="📖 Original" default>

"""

TABS_FOOTER = """
  </TabItem>

  <TabItem value="summary" label="📝 Summary">

<SummaryTab pagePath="{page_path}" />

  </TabItem>

  <TabItem value="personalized" label="✨ Personalized">

*Login required for personalized content powered by OLIVIA AI Tutor*

  </TabItem>
</Tabs>
"""

def get_page_path(file_path):
    """Convert file path to page path for SummaryTab component"""
    # Example: docs/01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything.md
    # -> 01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything

    parts = file_path.parts
    # Find the index of '01-Introducing-AI-Driven-Development'
    try:
        idx = parts.index('01-Introducing-AI-Driven-Development')
        path_parts = parts[idx:]
        # Remove .md extension from last part
        path_parts = list(path_parts)
        path_parts[-1] = path_parts[-1].replace('.md', '')
        return '/'.join(path_parts)
    except ValueError:
        return None

def has_tabs_already(content):
    """Check if file already has tabs"""
    return 'import Tabs from' in content or '<Tabs>' in content

def add_tabs_to_file(file_path):
    """Add tabs to a single markdown file"""
    print(f"Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has tabs
    if has_tabs_already(content):
        print(f"  ✓ Already has tabs, skipping")
        return False

    # Split frontmatter and content
    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"  ✗ No frontmatter found, skipping")
        return False

    frontmatter = f"---{parts[1]}---"
    body = parts[2]

    # Get page path for SummaryTab
    page_path = get_page_path(Path(file_path))
    if not page_path:
        print(f"  ✗ Could not determine page path, skipping")
        return False

    # Build new content
    new_content = frontmatter + TABS_HEADER + body + TABS_FOOTER.format(page_path=page_path)

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  ✓ Added tabs successfully")
    return True

def main():
    """Process all lesson files"""

    # Find all markdown files
    all_files = list(DOCS_DIR.rglob('*.md'))

    # Filter out README files and quiz files
    lesson_files = [
        f for f in all_files
        if f.name.lower() != 'readme.md'
        and 'quiz' not in f.name.lower()
    ]

    print(f"Found {len(lesson_files)} lesson files to process\n")

    success_count = 0
    for file_path in sorted(lesson_files):
        if add_tabs_to_file(file_path):
            success_count += 1
        print()

    print(f"\n{'='*60}")
    print(f"✓ Successfully added tabs to {success_count} files")
    print(f"✓ Skipped {len(lesson_files) - success_count} files")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
