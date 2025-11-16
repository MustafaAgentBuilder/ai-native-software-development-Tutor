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

# Check GEMINI_API_KEY
gemini_key = os.getenv("GEMINI_API_KEY")
if gemini_key:
    # Mask the key for security (show first 10 chars and last 4)
    if len(gemini_key) > 14:
        masked_key = f"{gemini_key[:10]}...{gemini_key[-4:]}"
    else:
        masked_key = "***" + gemini_key[-4:] if len(gemini_key) > 4 else "***"

    print(f"\n✅ GEMINI_API_KEY is loaded!")
    print(f"   Key (masked): {masked_key}")
    print(f"   Key length: {len(gemini_key)} characters")

    # Check if it's still the placeholder
    if "PASTE_YOUR" in gemini_key or "your_gemini" in gemini_key:
        print("\n⚠️  WARNING: You're still using the placeholder!")
        print("   Replace 'PASTE_YOUR_GEMINI_API_KEY_HERE' with your actual API key")
        print("\n   Get your FREE Gemini API key at:")
        print("   https://ai.google.dev/gemini-api/docs/api-key")
        exit(1)

    print("\n✅ API key looks valid!")
    print("\n🎉 You're ready to test OLIVIA!")
    print("\nRun: uv run python test_olivia_agent.py")

else:
    print("\n❌ GEMINI_API_KEY is NOT loaded!")
    print("\nPossible issues:")
    print("  1. The key is not in .env file")
    print("  2. There are spaces around the = sign (remove them)")
    print("  3. The line is commented out (remove #)")
    print("\nYour .env file should have:")
    print("  GEMINI_API_KEY=your-actual-key-here")
    print("  (NO SPACES around the = sign)")

    # Try to show what's in the .env file
    print("\n📄 Contents of .env file:")
    print("-" * 80)
    try:
        with open(env_path, 'r') as f:
            for i, line in enumerate(f, 1):
                if 'GEMINI_API_KEY' in line:
                    print(f"  Line {i}: {line.rstrip()}")
    except Exception as e:
        print(f"  Error reading file: {e}")
    print("-" * 80)
    exit(1)

print("=" * 80)
