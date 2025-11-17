#!/usr/bin/env python3
# Claude is Work to Build this Project
"""
Quick script to verify .env file is loading correctly
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

print("=" * 80)
print("🔍 Environment Variable Check")
print("=" * 80)

# Check if .env file exists
if env_path.exists():
    print(f"\n✅ .env file found at: {env_path}")
    print(f"   File size: {env_path.stat().st_size} bytes")
else:
    print(f"\n❌ .env file NOT found at: {env_path}")
    print("   Please create it by copying .env.example")
    exit(1)

# Check OPENAI_API_KEY
openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    # Mask the key for security (show first 10 chars and last 4)
    if len(openai_key) > 14:
        masked_key = f"{openai_key[:10]}...{openai_key[-4:]}"
    else:
        masked_key = "***" + openai_key[-4:] if len(openai_key) > 4 else "***"

    print(f"\n✅ OPENAI_API_KEY is loaded!")
    print(f"   Key (masked): {masked_key}")
    print(f"   Key length: {len(openai_key)} characters")

    # Check if it's still the placeholder
    if "YOUR-OPENAI" in openai_key or "your-openai" in openai_key or "sk-YOUR" in openai_key:
        print("\n⚠️  WARNING: You're still using the placeholder!")
        print("   Replace 'sk-YOUR-OPENAI-API-KEY-HERE' with your actual API key")
        print("\n   Get your OpenAI API key at:")
        print("   https://platform.openai.com/api-keys")
        exit(1)

    print("\n✅ API key looks valid!")
    print("\n🎉 You're ready to test OLIVIA!")
    print("\nRun: uv run python test_olivia_agent.py")

else:
    print("\n❌ OPENAI_API_KEY is NOT loaded!")
    print("\nPossible issues:")
    print("  1. The key is not in .env file")
    print("  2. There are spaces around the = sign (remove them)")
    print("  3. The line is commented out (remove #)")
    print("\nYour .env file should have:")
    print("  OPENAI_API_KEY=sk-your-actual-key-here")
    print("  (NO SPACES around the = sign)")

    # Try to show what's in the .env file
    print("\n📄 Contents of .env file:")
    print("-" * 80)
    try:
        with open(env_path, 'r') as f:
            for i, line in enumerate(f, 1):
                if 'OPENAI_API_KEY' in line:
                    print(f"  Line {i}: {line.rstrip()}")
    except Exception as e:
        print(f"  Error reading file: {e}")
    print("-" * 80)
    exit(1)

print("=" * 80)
