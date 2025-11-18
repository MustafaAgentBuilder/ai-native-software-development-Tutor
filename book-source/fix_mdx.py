#!/usr/bin/env python3
"""
Fix MDX frontmatter placement - move frontmatter BEFORE imports
"""

import re
from pathlib import Path

DOCS_DIR = Path("docs")

def fix_file(file_path: Path) -> bool:
    """Fix a single file by moving frontmatter before imports."""
    try:
        content = file_path.read_text(encoding='utf-8')

        # Check if file has tab imports
        if 'import Tabs from' not in content:
            return False

        # Find frontmatter (<!-- comment -->\n---\n...---\n)
        frontmatter_pattern = r'(<!--.*?-->\s*---\s*.*?\s*---\s*)'
        frontmatter_match = re.search(frontmatter_pattern, content, re.DOTALL)

        if not frontmatter_match:
            return False  # No frontmatter found

        frontmatter = frontmatter_match.group(1)
        frontmatter_start = frontmatter_match.start()

        # Check if frontmatter is AFTER imports (the problem)
        imports_pattern = r'^(import Tabs from)'
        imports_match = re.search(imports_pattern, content, re.MULTILINE)

        if imports_match and imports_match.start() < frontmatter_start:
            # Frontmatter is AFTER imports - need to fix

            # Remove frontmatter from current location
            content_without_frontmatter = content[:frontmatter_start] + content[frontmatter_match.end():]

            # Add frontmatter at the very beginning
            fixed_content = frontmatter + "\n" + content_without_frontmatter

            # Write back
            file_path.write_text(fixed_content, encoding='utf-8')
            print(f"✅ FIXED: {file_path}")
            return True
        else:
            print(f"⏭️  OK: {file_path}")
            return False

    except Exception as e:
        print(f"❌ ERROR: {file_path} - {e}")
        return False

def main():
    """Fix all MD files."""
    print("🔧 Fixing frontmatter placement in all lesson files...\n")

    fixed_count = 0
    for md_file in DOCS_DIR.rglob("*.md"):
        if md_file.name.lower() not in ["readme.md"]:
            if fix_file(md_file):
                fixed_count += 1

    print(f"\n{'='*60}")
    print(f"📊 Fixed {fixed_count} files")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
