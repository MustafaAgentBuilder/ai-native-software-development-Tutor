#!/usr/bin/env python3
"""Show the actual content of .env file to debug loading issues"""
from pathlib import Path

env_path = Path(__file__).parent / ".env"

print("=" * 80)
print("📄 .env File Content Viewer")
print("=" * 80)
print(f"\n📍 File location: {env_path}")
print(f"📏 File exists: {env_path.exists()}")

if env_path.exists():
    content = env_path.read_text(encoding='utf-8')
    print(f"📦 File size: {len(content)} bytes")
    print("\n📝 File content:")
    print("-" * 80)
    print(content)
    print("-" * 80)

    # Parse and show each line
    print("\n🔍 Parsed lines:")
    for i, line in enumerate(content.split('\n'), 1):
        line_stripped = line.strip()
        if line_stripped and not line_stripped.startswith('#'):
            if '=' in line_stripped:
                key, value = line_stripped.split('=', 1)
                if 'KEY' in key or 'SECRET' in key:
                    # Mask sensitive values
                    if len(value) > 20:
                        masked = f"{value[:10]}...{value[-8:]}"
                    else:
                        masked = "***-key" if len(value) < 20 else f"{value[:4]}...{value[-4:]}"
                    print(f"   Line {i}: {key} = {masked} (length: {len(value)})")
                else:
                    print(f"   Line {i}: {key} = {value}")
else:
    print("❌ .env file not found!")

print("=" * 80)
