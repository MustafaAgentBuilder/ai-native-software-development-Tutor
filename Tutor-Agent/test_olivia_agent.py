# Claude is Work to Build this Project
"""
OLIVIA Agent Testing Script

Simple script to test the OLIVIA agent without running the full backend server.
Tests RAG functionality, personalization, and agent responses.
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Mock User class for testing
class MockUser:
    """Mock user object for testing"""
    def __init__(self):
        self.id = 1
        self.email = "test@example.com"
        self.name = "Test User"

        # Learning profile (customize these!)
        class ProgrammingExperience:
            value = "intermediate"
        class AIExperience:
            value = "beginner"
        class LearningStyle:
            value = "visual"
        class PreferredLanguage:
            value = "en"

        self.programming_experience = ProgrammingExperience()
        self.ai_experience = AIExperience()
        self.learning_style = LearningStyle()
        self.preferred_language = PreferredLanguage()


async def test_olivia_agent():
    """Test OLIVIA agent with sample queries"""
    print("=" * 80)
    print("🤖 OLIVIA Agent Testing")
    print("=" * 80)

    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ ERROR: OPENAI_API_KEY not found in environment!")
        print("   Please create a .env file with your OpenAI API key:")
        print("   OPENAI_API_KEY=sk-...")
        return

    print("\n✅ OpenAI API Key found")

    try:
        # Import OLIVIA agent
        from tutor_agent.services.agent.olivia_agent import OLIVIAAgent
        print("✅ OLIVIA Agent imported successfully")

        # Create mock user
        test_user = MockUser()
        print(f"\n👤 Test User Profile:")
        print(f"   - Programming: {test_user.programming_experience.value}")
        print(f"   - AI/ML: {test_user.ai_experience.value}")
        print(f"   - Learning Style: {test_user.learning_style.value}")

        # Initialize agent
        olivia = OLIVIAAgent()
        print("\n✅ OLIVIA initialized")

        # Test 1: Simple question
        print("\n" + "=" * 80)
        print("📝 Test 1: Simple Question")
        print("=" * 80)

        question1 = "What is AI-Native Software Development?"
        print(f"\nQuestion: {question1}")
        print("\nOLIVIA Response:")
        print("-" * 80)

        async for chunk in olivia.generate_personalized_content_stream(
            original_content="",
            user=test_user,
            page_path="01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything",
            user_query=question1
        ):
            print(chunk, end="", flush=True)

        print("\n" + "-" * 80)

        # Test 2: RAG-based question
        print("\n" + "=" * 80)
        print("📝 Test 2: RAG Search Question")
        print("=" * 80)

        question2 = "What are the key features of Claude Code mentioned in the book?"
        print(f"\nQuestion: {question2}")
        print("\nOLIVIA Response:")
        print("-" * 80)

        async for chunk in olivia.generate_personalized_content_stream(
            original_content="",
            user=test_user,
            page_path="02-AI-Tool-Landscape/05-claude-code-features-and-workflows",
            user_query=question2
        ):
            print(chunk, end="", flush=True)

        print("\n" + "-" * 80)

        # Test 3: Personalized explanation
        print("\n" + "=" * 80)
        print("📝 Test 3: Personalized Explanation Request")
        print("=" * 80)

        question3 = "Explain Python type hints to me"
        print(f"\nQuestion: {question3}")
        print(f"(This should be tailored to: {test_user.learning_style.value} learner)")
        print("\nOLIVIA Response:")
        print("-" * 80)

        async for chunk in olivia.generate_personalized_content_stream(
            original_content="",
            user=test_user,
            page_path="04-Python-Fundamentals",
            user_query=question3
        ):
            print(chunk, end="", flush=True)

        print("\n" + "-" * 80)

        print("\n" + "=" * 80)
        print("✅ All tests completed successfully!")
        print("=" * 80)

    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("   Make sure you've installed dependencies: uv sync")
    except Exception as e:
        print(f"\n❌ Test Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n🚀 Starting OLIVIA Agent Tests...\n")
    asyncio.run(test_olivia_agent())
