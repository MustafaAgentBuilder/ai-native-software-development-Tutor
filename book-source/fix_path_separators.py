#!/usr/bin/env python3
"""
Fix path separators in all MDX files - change backslashes to forward slashes in pagePath props.
"""

import re
from pathlib import Path

DOCS_DIR = Path("docs")

def fix_path_separators(file_path: Path) -> bool:
    """Fix path separators in pagePath props."""
    try:
        content = file_path.read_text(encoding='utf-8')

        if 'pagePath=' not in content:
            return False

        original_content = content

        # Pattern: pagePath="path\with\backslashes"
        # Replace backslashes with forward slashes
        pattern = r'(pagePath=")([^"]+)(")'

        def replace_backslashes(match):
            prefix = match.group(1)
            path = match.group(2)
            suffix = match.group(3)
            # Replace all backslashes with forward slashes
            fixed_path = path.replace('\\', '/')
            return f"{prefix}{fixed_path}{suffix}"

        content = re.sub(pattern, replace_backslashes, content)

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
    print("🔧 Fixing path separators in all lesson files...\n")

    fixed_count = 0
    for md_file in DOCS_DIR.rglob("*.md"):
        if md_file.name.lower() not in ["readme.md"]:
            if fix_path_separators(md_file):
                fixed_count += 1

    print(f"\n{'='*60}")
    print(f"📊 Fixed {fixed_count} files")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
