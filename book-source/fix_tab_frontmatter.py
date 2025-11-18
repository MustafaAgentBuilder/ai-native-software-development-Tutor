#!/usr/bin/env python3
"""
Script to fix frontmatter placement in tab-wrapped files.
Move frontmatter BEFORE tab imports and wrap only content in tabs.
"""

import os
import re
from pathlib import Path

DOCS_DIR = Path("docs")

def fix_file_tabs(file_path: Path) -> bool:
    """
    Fix tab structure to have frontmatter OUTSIDE tabs.

    Expected structure:
    ---
    frontmatter
    ---

    import statements

    <Tabs>
      <TabItem value="original">
        CONTENT
      </TabItem>
      ...
    </Tabs>
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if file has the tab imports
        if 'import Tabs from' not in content:
            return False  # File doesn't have tabs yet

        # Pattern to match:
        # 1. Tab imports
        # 2. <Tabs> opening
        # 3. <TabItem value="original"> opening
        # 4. Possible frontmatter ---...---
        # 5. Content
        # 6. Tab closings

        # Split by <TabItem value="original"
        if '<TabItem value="original"' not in content:
            return False

        parts = content.split('<TabItem value="original"', 1)
        if len(parts) < 2:
            return False

        before_original_tab = parts[0]
        after_original_tab = parts[1]

        # Extract frontmatter if it's INSIDE the tab
        frontmatter_pattern = r'^[^\n]*>\s*\n(---\n.*?\n---\n)'
        frontmatter_match = re.match(frontmatter_pattern, after_original_tab, re.DOTALL)

        if frontmatter_match:
            # Frontmatter is INSIDE tab - need to move it out
            frontmatter = frontmatter_match.group(1)

            # Remove frontmatter from after_original_tab
            after_original_tab_cleaned = after_original_tab[frontmatter_match.end():]

            # Find the closing tag position to extract label and default
            label_match = re.search(r'label="([^"]*)"', after_original_tab)
            default_match = re.search(r'\bdefault\b', after_original_tab[:100])

            label = label_match.group(1) if label_match else "📖 Original"
            default_attr = " default" if default_match else ""

            # Build correct structure
            new_content = frontmatter + "\n"
            new_content += before_original_tab  # imports and <Tabs>
            new_content += f'<TabItem value="original" label="{label}"{default_attr}>\n\n'
            new_content += after_original_tab_cleaned

            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"✅ FIXED: {file_path}")
            return True
        else:
            # Frontmatter already outside, or no frontmatter
            print(f"⏭️  OK: {file_path} (frontmatter already correct)")
            return False

    except Exception as e:
        print(f"❌ ERROR: {file_path} - {e}")
        return False

def main():
    """Fix all lesson files with tab frontmatter issues."""
    print("🔧 Fixing tab frontmatter placement...\n")

    lesson_files = []
    for md_file in DOCS_DIR.rglob("*.md"):
        if md_file.name.lower() not in ["readme.md"]:
            lesson_files.append(md_file)

    fixed_count = 0
    for file_path in sorted(lesson_files):
        if fix_file_tabs(file_path):
            fixed_count += 1

    print("\n" + "="*60)
    print(f"📊 Fixed {fixed_count} files")
    print("="*60)

if __name__ == "__main__":
    main()
