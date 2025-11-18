#!/usr/bin/env python3
"""
Fix all MDX files with list items immediately before </TabItem> closing tags.
MDX requires a blank line between list items and closing tags.
"""

import re
from pathlib import Path

DOCS_DIR = Path("docs")

def fix_tab_spacing(file_path: Path) -> bool:
    """Fix spacing before </TabItem> tags in a single file."""
    try:
        content = file_path.read_text(encoding='utf-8')

        # Check if file has tabs
        if '</TabItem>' not in content:
            return False

        original_content = content

        # Pattern 1: list item followed by blank lines and indented </TabItem>
        # Replace with: list item + single blank line + non-indented </TabItem>
        pattern1 = r'(^[-*]\s+.+$)\n+\s+(</TabItem>)'
        content = re.sub(pattern1, r'\1\n\n\2', content, flags=re.MULTILINE)

        # Pattern 2: list item followed by multiple blank lines and non-indented </TabItem>
        # Replace with: list item + single blank line + </TabItem>
        pattern2 = r'(^[-*]\s+.+$)\n\n\n+(</TabItem>)'
        content = re.sub(pattern2, r'\1\n\n\2', content, flags=re.MULTILINE)

        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            print(f"✅ FIXED: {file_path}")
            return True
        else:
            return False

    except Exception as e:
        print(f"❌ ERROR: {file_path} - {e}")
        return False

def main():
    """Fix all MD files."""
    print("🔧 Fixing tab spacing in all lesson files...\\n")

    fixed_count = 0
    for md_file in DOCS_DIR.rglob("*.md"):
        if md_file.name.lower() not in ["readme.md"]:
            if fix_tab_spacing(md_file):
                fixed_count += 1

    print(f"\\n{'='*60}")
    print(f"📊 Fixed {fixed_count} files")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
