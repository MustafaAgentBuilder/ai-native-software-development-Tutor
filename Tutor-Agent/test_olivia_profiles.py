#!/usr/bin/env python3
"""
Comprehensive OLIVIA Agent Testing with Multiple User Profiles

This tests OLIVIA's personalization across different:
- Programming experience levels (beginner, intermediate, advanced)
- AI/ML experience levels (beginner, intermediate, advanced)
- Learning styles (visual, text, hands-on)
"""

import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


async def test_olivia_with_profiles():
    """Test OLIVIA with different user profiles"""
    from tutor_agent.models.user import User, ProgrammingExperience, AIExperience, LearningStyle, PreferredLanguage
    from tutor_agent.services.agent.olivia_agent import OLIVIAAgent

    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ ERROR: OPENAI_API_KEY not found in environment!")
        print("   Get your OpenAI API key at:")
        print("   https://platform.openai.com/api-keys")
        return

    print("\n" + "=" * 80)
    print("🧪 OLIVIA Comprehensive Testing - Multiple User Profiles")
    print("=" * 80)

    # Define test user profiles
    test_profiles = [
        {
            "name": "Beginner Visual Learner",
            "user": User(
                id=1,
                email="beginner@test.com",
                hashed_password="test",
                programming_experience=ProgrammingExperience.BEGINNER,
                ai_experience=AIExperience.NONE,
                learning_style=LearningStyle.VISUAL,
                preferred_language=PreferredLanguage.ENGLISH
            ),
            "question": "What is a variable in Python?"
        },
        {
            "name": "Intermediate Hands-On Learner",
            "user": User(
                id=2,
                email="intermediate@test.com",
                hashed_password="test",
                programming_experience=ProgrammingExperience.INTERMEDIATE,
                ai_experience=AIExperience.BASIC,
                learning_style=LearningStyle.PRACTICAL,
                preferred_language=PreferredLanguage.ENGLISH
            ),
            "question": "How do I implement a REST API endpoint in FastAPI?"
        },
        {
            "name": "Advanced Text Learner",
            "user": User(
                id=3,
                email="advanced@test.com",
                hashed_password="test",
                programming_experience=ProgrammingExperience.ADVANCED,
                ai_experience=AIExperience.INTERMEDIATE,
                learning_style=LearningStyle.CONCEPTUAL,
                preferred_language=PreferredLanguage.ENGLISH
            ),
            "question": "Explain the architecture of the OpenAI Agents SDK"
        },
        {
            "name": "Advanced Visual AI Expert",
            "user": User(
                id=4,
                email="expert@test.com",
                hashed_password="test",
                programming_experience=ProgrammingExperience.ADVANCED,
                ai_experience=AIExperience.ADVANCED,
                learning_style=LearningStyle.VISUAL,
                preferred_language=PreferredLanguage.ENGLISH
            ),
            "question": "How does RAG work with ChromaDB embeddings?"
        }
    ]

    # Initialize OLIVIA
    olivia = OLIVIAAgent()
    print("✅ OLIVIA Agent initialized\n")

    # Test each profile
    for idx, profile in enumerate(test_profiles, 1):
        print("=" * 80)
        print(f"TEST {idx}/4: {profile['name']}")
        print("=" * 80)
        print(f"\n👤 User Profile:")
        print(f"   - Programming: {profile['user'].programming_experience}")
        print(f"   - AI/ML: {profile['user'].ai_ml_experience}")
        print(f"   - Learning Style: {profile['user'].learning_style}")
        print(f"   - Language: {profile['user'].preferred_language}")
        print(f"\n❓ Question: {profile['question']}")
        print(f"\n💬 OLIVIA Response:")
        print("-" * 80)

        try:
            # Generate personalized response
            response_text = ""
            async for chunk in olivia.generate_personalized_content_stream(
                user=profile['user'],
                user_message=profile['question'],
                page_path=None
            ):
                # Collect response chunks
                response_text += chunk
                # Show streaming (optional - comment out to see full response at once)
                # print(chunk, end="", flush=True)

            # Print full response
            print(response_text)
            print("-" * 80)

            # Analyze response characteristics
            print(f"\n📊 Response Analysis:")
            print(f"   - Length: {len(response_text)} characters")
            print(f"   - Has code examples: {'```' in response_text}")
            print(f"   - Has diagrams/visuals mention: {any(word in response_text.lower() for word in ['diagram', 'visual', 'image', 'chart'])}")
            print(f"   - Has hands-on exercises: {any(word in response_text.lower() for word in ['try', 'practice', 'exercise', 'implement'])}")
            print(f"   - Technical depth: {'advanced' if any(word in response_text.lower() for word in ['architecture', 'implementation', 'algorithm', 'optimization']) else 'moderate'}")

        except Exception as e:
            print(f"\n❌ Test Error: {e}")
            import traceback
            traceback.print_exc()

        print()  # Spacing between tests

    print("=" * 80)
    print("✅ All profile tests completed!")
    print("=" * 80)
    print("\n📝 Observations:")
    print("   - Check if responses adapt to experience level")
    print("   - Beginner responses should be simpler, more explanatory")
    print("   - Advanced responses should be more technical, concise")
    print("   - Visual learners should get diagrams/code examples")
    print("   - Hands-on learners should get exercises/practice tasks")
    print("   - Text learners should get detailed explanations")


if __name__ == "__main__":
    print("\n🚀 Starting OLIVIA Comprehensive Testing...")
    asyncio.run(test_olivia_with_profiles())
