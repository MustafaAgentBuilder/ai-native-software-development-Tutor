#!/usr/bin/env python3
"""
Script to add three-tab system to all lesson .md files that don't have it yet.
Skips README.md files and files that already have tabs.
"""

import os
import re
from pathlib import Path

# Paths
DOCS_DIR = Path("docs")
SCRIPT_DIR = Path(__file__).parent

# Tab template to insert after frontmatter
TAB_TEMPLATE = """
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import SummaryTab from '@site/src/components/SummaryTab';
import PersonalizedTab from '@site/src/components/PersonalizedTab';

<Tabs>
  <TabItem value="original" label="📖 Original" default>

"""

TAB_CLOSING = """
  </TabItem>

  <TabItem value="summary" label="📝 Summary">
    <SummaryTab pagePath="{page_path}" />
  </TabItem>

  <TabItem value="personalized" label="✨ Personalized">
    <PersonalizedTab pagePath="{page_path}" />
  </TabItem>
</Tabs>
"""

def extract_page_path(file_path: Path) -> str:
    """
    Extract page path for Summary/Personalized components.
    Example: docs/01-Chapter/02-section/03-lesson.md -> 01-Chapter/02-section/03-lesson
    """
    relative_path = file_path.relative_to(DOCS_DIR)
    # Remove .md extension
    path_without_ext = str(relative_path).replace(".md", "")
    return path_without_ext

def has_tabs(content: str) -> bool:
    """Check if file already has tab imports."""
    return "import Tabs from '@theme/Tabs'" in content

def is_readme(file_path: Path) -> bool:
    """Check if file is a README."""
    return file_path.name.lower() in ["readme.md", "_category_.yml"]

def extract_frontmatter(content: str) -> tuple[str, str]:
    """
    Extract frontmatter and content.
    Returns: (frontmatter_with_delimiters, rest_of_content)
    """
    # Match YAML frontmatter between --- delimiters
    frontmatter_pattern = r'^(---\n.*?\n---\n)'
    match = re.match(frontmatter_pattern, content, re.DOTALL)

    if match:
        frontmatter = match.group(1)
        rest = content[len(frontmatter):]
        return frontmatter, rest
    else:
        # No frontmatter
        return "", content

def add_tabs_to_file(file_path: Path) -> bool:
    """
    Add three-tab system to a single file.
    Returns True if file was modified, False otherwise.
    """
    try:
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already has tabs
        if has_tabs(content):
            print(f"⏭️  SKIP: {file_path} (already has tabs)")
            return False

        # Extract frontmatter
        frontmatter, body = extract_frontmatter(content)

        # Get page path for component
        page_path = extract_page_path(file_path)

        # Build new content
        new_content = frontmatter + TAB_TEMPLATE + body + "\n" + TAB_CLOSING.format(page_path=page_path)

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"✅ ADDED: {file_path}")
        return True

    except Exception as e:
        print(f"❌ ERROR: {file_path} - {e}")
        return False

def find_lesson_files(docs_dir: Path) -> list[Path]:
    """Find all .md lesson files (excluding README.md)."""
    lesson_files = []

    for md_file in docs_dir.rglob("*.md"):
        if not is_readme(md_file):
            lesson_files.append(md_file)

    return sorted(lesson_files)

def main():
    """Main execution."""
    print("🚀 Starting tab injection process...\n")

    # Find all lesson files
    lesson_files = find_lesson_files(DOCS_DIR)
    print(f"📚 Found {len(lesson_files)} lesson files\n")

    # Process each file
    modified_count = 0
    skipped_count = 0
    error_count = 0

    for file_path in lesson_files:
        result = add_tabs_to_file(file_path)
        if result:
            modified_count += 1
        elif result is False:
            skipped_count += 1
        else:
            error_count += 1

    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY:")
    print(f"   ✅ Modified: {modified_count} files")
    print(f"   ⏭️  Skipped:  {skipped_count} files (already had tabs)")
    print(f"   ❌ Errors:   {error_count} files")
    print(f"   📚 Total:    {len(lesson_files)} files")
    print("="*60)

    if modified_count > 0:
        print("\n✅ Tab injection complete! Please review the changes.")
    else:
        print("\n✅ All files already have tabs!")

if __name__ == "__main__":
    main()
