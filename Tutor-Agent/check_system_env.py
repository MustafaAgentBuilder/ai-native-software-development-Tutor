#!/usr/bin/env python3
"""Check if OPENAI_API_KEY exists in system environment BEFORE loading .env"""
import os

print("=" * 80)
print("🔍 System Environment Variable Check")
print("=" * 80)

# Check BEFORE loading .env
openai_key_from_system = os.environ.get("OPENAI_API_KEY")

print("\n📊 OPENAI_API_KEY in system environment:")
if openai_key_from_system:
    if len(openai_key_from_system) > 20:
        masked = f"{openai_key_from_system[:10]}...{openai_key_from_system[-8:]}"
    else:
        masked = "***-key"
    print(f"   ⚠️  FOUND in system environment!")
    print(f"   Value (masked): {masked}")
    print(f"   Length: {len(openai_key_from_system)} characters")
    print("\n❌ PROBLEM: System environment variable is overriding your .env file!")
    print("   This is why the agent sees 'your-api-key' instead of the real key.")
    print("\n🔧 FIX: Remove the system environment variable:")
    print("   1. Open PowerShell as Administrator")
    print("   2. Run: [Environment]::SetEnvironmentVariable('OPENAI_API_KEY', $null, 'User')")
    print("   3. Run: [Environment]::SetEnvironmentVariable('OPENAI_API_KEY', $null, 'Machine')")
    print("   4. Close and reopen PowerShell")
    print("   5. Run: uv run python test_olivia_agent.py")
else:
    print("   ✅ NOT FOUND in system environment (good!)")
    print("   The .env file should be loaded correctly.")

print("\n💡 To check system env vars in PowerShell, run:")
print("   Get-ChildItem Env: | Where-Object {$_.Name -like '*OPENAI*'}")
print("=" * 80)
