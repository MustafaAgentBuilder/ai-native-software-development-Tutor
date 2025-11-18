"""
Fix MDX compilation errors caused by curly braces in markdown files.
"""
import re
from pathlib import Path

def fix_curly_braces_in_file(file_path: Path):
    """Fix curly braces in markdown files that cause MDX parsing errors."""
    content = file_path.read_text(encoding='utf-8')
    original_content = content

    # Pattern to match code blocks (we should NOT modify these)
    code_block_pattern = r'```[\s\S]*?```'

    # Find all code blocks
    code_blocks = list(re.finditer(code_block_pattern, content))

    # Track if file was modified
    modified = False

    # Check if there are inline code sections with curly braces outside code blocks
    # that are NOT properly escaped

    # For f-strings in inline code, ensure they're in proper code blocks
    # The issue is MDX tries to parse {...} as JSX expressions

    # The real fix: ensure all Python code with curly braces is in fenced code blocks
    # Let's check lines mentioned in errors

    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        # Check for problematic patterns
        if '{' in line and '}' in line:
            # Skip if in YAML frontmatter (between ---)
            in_frontmatter = False
            for j in range(i):
                if lines[j].strip() == '---':
                    in_frontmatter = not in_frontmatter

            if not in_frontmatter:
                # Check if this line is in a code block
                in_code_block = False
                for block in code_blocks:
                    block_start_line = content[:block.start()].count('\n') + 1
                    block_end_line = content[:block.end()].count('\n') + 1
                    if block_start_line <= i <= block_end_line:
                        in_code_block = True
                        break

                # If not in code block and contains curly braces, this might be the issue
                if not in_code_block and  not line.strip().startswith('#'):
                    print(f"Line {i}: {line[:100]}")

    return modified

# Fix the problematic files
files_to_fix = [
    Path("docs/04-Python-Fundamentals/15-operators-keywords-variables/02-comparison-operators.md"),
    Path("docs/04-Python-Fundamentals/16-strings-type-casting/03-f-string-formatting.md"),
    Path("docs/04-Python-Fundamentals/17-control-flow-loops/01-making-decisions-with-conditionals.md"),
    Path("docs/04-Python-Fundamentals/19-set-frozenset-gc/02-set-operations.md"),
]

for file_path in files_to_fix:
    if file_path.exists():
        print(f"\n=== Checking {file_path.name} ===")
        fix_curly_braces_in_file(file_path)
