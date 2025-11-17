#!/usr/bin/env python3
"""
Test OLIVIA's Visual Learning Enhancements

Tests that visual learners receive:
- Mermaid diagrams (mind maps, flowcharts)
- Visual code structure
- ASCII diagrams
- Descriptive visual explanations
"""

import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


async def test_visual_learning():
    """Test OLIVIA with visual learner profile"""
    from tutor_agent.models.user import User
    from tutor_agent.services.agent.olivia_agent import OLIVIAAgent

    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ ERROR: OPENAI_API_KEY not found in environment!")
        return

    print("\n" + "=" * 80)
    print("🎨 OLIVIA Visual Learning Enhancement Test")
    print("=" * 80)

    # Create visual learner profile (using correct field names from User model)
    from tutor_agent.models.user import ProgrammingExperience, AIExperience, LearningStyle, PreferredLanguage

    visual_learner = User(
        id=999,  # Test ID
        email="visual@test.com",
        hashed_password="test",  # Not used in tests
        programming_experience=ProgrammingExperience.INTERMEDIATE,
        ai_experience=AIExperience.BASIC,
        learning_style=LearningStyle.VISUAL,
        preferred_language=PreferredLanguage.ENGLISH
    )

    # Initialize OLIVIA
    olivia = OLIVIAAgent()
    print("\n✅ OLIVIA Agent initialized")
    print(f"\n👤 Test Profile: Intermediate/Visual Learner")

    # Test questions that should trigger visual diagrams
    test_questions = [
        {
            "question": "Explain how RAG (Retrieval-Augmented Generation) works",
            "expects": "flowchart showing RAG pipeline steps"
        },
        {
            "question": "What is the architecture of the OpenAI Agents SDK?",
            "expects": "component diagram showing agent architecture"
        },
        {
            "question": "How do Python decorators work?",
            "expects": "visual representation of decorator wrapping"
        }
    ]

    for idx, test in enumerate(test_questions, 1):
        print("\n" + "=" * 80)
        print(f"📊 Test {idx}/3: {test['question']}")
        print("=" * 80)
        print(f"\n🎯 Expected: {test['expects']}")
        print(f"\n💬 OLIVIA Response:")
        print("-" * 80)

        try:
            response_text = ""
            async for chunk in olivia.generate_personalized_content_stream(
                user=visual_learner,
                user_message=test['question'],
                page_path=None
            ):
                response_text += chunk
                # Uncomment to see streaming:
                # print(chunk, end="", flush=True)

            # Print full response
            print(response_text)
            print("-" * 80)

            # Analyze visual elements
            has_mermaid = "```mermaid" in response_text
            has_code = "```python" in response_text or "```" in response_text
            has_ascii = any(symbol in response_text for symbol in ["├", "└", "│", "─", "→", "┌", "┐"])
            visual_words = sum(1 for word in ["diagram", "visual", "flow", "graph", "chart", "map"]
                             if word in response_text.lower())

            print(f"\n📊 Visual Analysis:")
            print(f"   ✅ Has Mermaid diagram: {has_mermaid}")
            print(f"   ✅ Has code examples: {has_code}")
            print(f"   ✅ Has ASCII diagrams: {has_ascii}")
            print(f"   📈 Visual vocabulary count: {visual_words} words")

            if has_mermaid:
                print(f"   🎉 SUCCESS: Visual learner received diagram!")
            else:
                print(f"   ⚠️  No Mermaid diagram found (may need regeneration)")

        except Exception as e:
            print(f"\n❌ Test Error: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 80)
    print("✅ Visual Learning Tests Complete!")
    print("=" * 80)
    print("\n📝 Key Observations:")
    print("   - Visual learners should receive Mermaid diagrams")
    print("   - Diagrams visualize concepts like flowcharts, mind maps")
    print("   - Code examples show clear structure")
    print("   - Descriptive visual language used throughout")
    print("\n💡 Mermaid diagrams render in:")
    print("   - GitHub markdown")
    print("   - Docusaurus")
    print("   - VS Code markdown preview")
    print("   - Most modern markdown viewers")


if __name__ == "__main__":
    print("\n🚀 Starting Visual Learning Enhancement Test...")
    asyncio.run(test_visual_learning())
