#!/usr/bin/env python3
"""
Test OpenAI API connection to diagnose SSL/network issues
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("=" * 60)
print("OpenAI Connection Diagnostic Test")
print("=" * 60)

# Load environment
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"✓ API Key loaded: {api_key[:20]}..." if api_key else "✗ API Key NOT found")
print()

# Test 1: Basic OpenAI client connection
print("=" * 60)
print("Test 1: Basic OpenAI Client Connection")
print("=" * 60)

try:
    from openai import OpenAI
    client = OpenAI(
        api_key=api_key,
        timeout=30.0,  # 30 second timeout
    )

    print("✓ OpenAI client initialized")

    # Try a simple completion
    print("Attempting simple API call...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say 'hello'"}],
        max_tokens=10
    )
    print(f"✓ API call successful!")
    print(f"Response: {response.choices[0].message.content}")

except Exception as e:
    print(f"✗ OpenAI client test FAILED: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()

print()

# Test 2: OpenAI Agents SDK
print("=" * 60)
print("Test 2: OpenAI Agents SDK Connection")
print("=" * 60)

try:
    from agents import Agent, Runner

    # Set API key in environment
    os.environ["OPENAI_API_KEY"] = api_key

    print("✓ Agents SDK imported")

    # Create simple agent
    agent = Agent(
        name="TestAgent",
        instructions="You are a test agent. Say hello.",
        model="gpt-4o-mini"
    )

    print("✓ Agent created")
    print("Attempting agent run...")

    # Run agent with timeout
    import asyncio

    async def test_agent():
        result = Runner.run_streamed(agent, input="Say hello")
        response = ""
        async for event in result.stream_events():
            if hasattr(event, 'data') and hasattr(event.data, 'delta'):
                if hasattr(event.data.delta, 'text'):
                    response += event.data.delta.text
        return response

    response = asyncio.run(test_agent())
    print(f"✓ Agent run successful!")
    print(f"Response: {response}")

except Exception as e:
    print(f"✗ Agents SDK test FAILED: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()

print()
print("=" * 60)
print("Diagnostic Complete")
print("=" * 60)
print()
print("If tests failed with SSL/timeout errors, try:")
print("1. Check your internet connection")
print("2. Check if firewall/antivirus is blocking OpenAI")
print("3. Try using a VPN if OpenAI is blocked in your region")
print("4. Check proxy settings if you're behind a corporate firewall")
