#!/usr/bin/env python3
"""
Remove first-line HTML comment before frontmatter so Docusaurus can parse it correctly.
Docusaurus requires frontmatter to start on LINE 1.
"""

import re
from pathlib import Path

DOCS_DIR = Path("docs")

def fix_frontmatter_position(file_path: Path) -> bool:
    """Move frontmatter to line 1 by removing preceding HTML comment."""
    try:
        content = file_path.read_text(encoding='utf-8')

        # Check if file starts with HTML comment followed by frontmatter
        if not content.startswith('<!-- Claude'):
            return False

        original_content = content

        # Pattern: HTML comment on line 1, then frontmatter delimiter on line 2
        # We want to remove the HTML comment line
        pattern = r'^<!--[^\n]+-->\r?\n'

        content = re.sub(pattern, '', content, count=1)

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
    print("🔧 Moving frontmatter to line 1 in all lesson files...\n")

    fixed_count = 0
    for md_file in DOCS_DIR.rglob("*.md"):
        if md_file.name.lower() not in ["readme.md"]:
            if fix_frontmatter_position(md_file):
                fixed_count += 1

    print(f"\n{'='*60}")
    print(f"📊 Fixed {fixed_count} files")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
