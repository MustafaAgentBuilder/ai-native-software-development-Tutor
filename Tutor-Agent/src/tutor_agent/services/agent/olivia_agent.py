# Claude is Work to Build this Project
"""
OLIVIA Agent (OpenAI Learning and Interactive Virtual Instructional Agent)

RAG-powered AI tutor using OpenAI GPT-4o-mini with OpenAI Agents SDK streaming support.
Implements Six-Step Prompting Framework (ACILPR) with real-time RAG.
"""

import asyncio
import os
from typing import Any, AsyncGenerator, Dict, Optional

from agents import (
    Agent,
    AsyncOpenAI,
    ItemHelpers,
    OpenAIChatCompletionsModel,
    Runner,
    set_tracing_disabled,
)
from dotenv import load_dotenv

from tutor_agent.models.user import User
from tutor_agent.services.agent.tools import search_book_content

# Load environment variables
load_dotenv()

# Disable extra tracing for cleaner output
set_tracing_disabled(True)


class OLIVIAAgent:
    """
    OLIVIA - AI tutor agent with RAG capabilities

    Features:
    - Personalized content generation based on user profile
    - RAG-powered responses using book embeddings
    - Streaming for real-time user feedback
    - Context-aware based on learning journey
    """

    def __init__(self):
        """Initialize OLIVIA agent with OpenAI model and tools"""
        self.agent = None  # Will be created per-user for personalization

        # Create OpenAI API provider
        self.openai_provider = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        # Set up the chat completion model with GPT-4o-mini
        self.model = OpenAIChatCompletionsModel(
            model="gpt-4o-mini",  # Fast, cheap, and perfect function calling support
            openai_client=self.openai_provider,
        )

    def _create_personalized_agent(
        self, user: User, page_path: Optional[str] = None
    ) -> Agent:
        """
        Create a personalized agent instance for specific user

        Args:
            user: User object with learning profile
            page_path: Current page path for context

        Returns:
            Configured Agent instance
        """
        # Build personalized instructions using Six-Step Framework (ACILPR)
        instructions = self._build_personalized_instructions(user, page_path)

        # Create agent with RAG tool using Gemini model
        agent = Agent(
            name="OLIVIA",
            instructions=instructions,
            tools=[search_book_content],  # RAG search tool
            model=self.model,  # Gemini 2.0 Flash model
        )

        return agent

    def _build_personalized_instructions(
        self, user: User, page_path: Optional[str] = None
    ) -> str:
        """
        Build agent instructions using Six-Step Framework (ACILPR)

        1. Actor: Define who OLIVIA is
        2. Context: User's learning profile and current location
        3. Instruction: How to personalize and use tools
        4. Limitations: Constraints
        5. Persona: Communication style
        6. Response Format: Output structure
        """
        # 1. ACTOR
        actor = """You are OLIVIA, an AI-powered learning tutor specializing in AI-Native Software Development.
Your expertise includes programming, AI/ML, software architecture, and personalized education.
You adapt your teaching style to each learner's unique profile and needs."""

        # 2. CONTEXT (User Profile + Current Location)
        context = f"""
Current Learner Profile:
- Programming Experience: {user.programming_experience.value.title()}
- AI/ML Experience: {user.ai_experience.value.title()}
- Learning Style: {user.learning_style.value.title()}
- Preferred Language: {user.preferred_language.value.upper()}
"""
        if page_path:
            context += f"\nCurrent Page: {page_path}"

        # 3. INSTRUCTION (Adaptive Teaching + Tool Usage)
        instruction = self._get_adaptive_instruction(user)
        instruction += """

IMPORTANT - Tool Usage:
- ALWAYS use the search_book_content tool to find relevant information from the book
- Reference specific sections/chapters when answering
- Provide accurate, fact-based responses grounded in the book content
- If asked about topics not covered in the book, acknowledge this clearly
"""

        # 4. LIMITATIONS
        limitations = """
Constraints:
- Keep content length appropriate (2-4 paragraphs for explanations)
- Preserve technical accuracy - never simplify at the expense of correctness
- Do NOT add emojis or excessive formatting
- Focus on clarity and learning outcomes
- Always cite book sections when using information from them
"""

        # 5. PERSONA (Communication Style)
        persona = self._get_adaptive_persona(user)

        # 6. RESPONSE FORMAT
        response_format = """
When generating personalized content:
1. Start with a brief introduction adapted to user's level
2. Explain key concepts using their preferred learning style
3. Provide examples appropriate for their experience
4. End with practical next steps or exercises

Use markdown formatting. Be clear and concise.
"""

        # Combine all parts
        return f"""{actor}

{context}

{instruction}

{limitations}

{persona}

{response_format}
"""

    def _get_adaptive_instruction(self, user: User) -> str:
        """Generate adaptive instruction based on user profile"""
        from tutor_agent.models.user import (
            AIExperience,
            LearningStyle,
            ProgrammingExperience,
        )

        # Adapt based on programming experience
        if user.programming_experience == ProgrammingExperience.BEGINNER:
            prog_instruction = "Explain concepts from first principles. Define all technical terms. Use simple analogies."
        elif user.programming_experience == ProgrammingExperience.INTERMEDIATE:
            prog_instruction = "Build on foundational knowledge. Introduce some advanced concepts. Balance theory and practice."
        else:  # ADVANCED
            prog_instruction = "Focus on advanced patterns and best practices. Assume strong fundamentals. Dive deep into nuances."

        # Adapt based on AI experience
        if user.ai_experience == AIExperience.NONE:
            ai_instruction = "Introduce AI concepts gently. Explain all AI terminology. Focus on practical applications."
        elif user.ai_experience == AIExperience.BASIC:
            ai_instruction = (
                "Build on basic AI knowledge. Introduce ML/LLM concepts progressively."
            )
        elif user.ai_experience == AIExperience.INTERMEDIATE:
            ai_instruction = "Assume familiarity with ML basics. Focus on agent architectures and advanced patterns."
        else:  # ADVANCED
            ai_instruction = "Discuss cutting-edge techniques. Reference latest research. Explore complex architectures."

        # Adapt based on learning style
        if user.learning_style == LearningStyle.VISUAL:
            style_instruction = """Use visual representations heavily:
- Create Mermaid diagrams (flowcharts, mind maps, sequence diagrams) to visualize concepts
- Use code examples with clear visual structure
- Describe spatial/visual relationships between components
- Include ASCII diagrams or tables when helpful
- Paint mental pictures with descriptive language

Example Mermaid syntax to use:
```mermaid
graph TD
    A[Concept] --> B[Sub-concept 1]
    A --> C[Sub-concept 2]
    B --> D[Detail]
```
Always include at least one visual diagram for complex topics."""
        elif user.learning_style == LearningStyle.PRACTICAL:
            style_instruction = "Prioritize code examples and hands-on exercises. Show practical applications immediately."
        elif user.learning_style == LearningStyle.CONCEPTUAL:
            style_instruction = "Explain underlying theory and principles first. Connect concepts to mental models."
        else:  # MIXED
            style_instruction = "Balance theory, visuals, and practical examples. Use multiple teaching approaches."

        return f"""
Task: Transform the original lesson content into a personalized version for THIS specific learner.

Adaptation Guidelines:
- Programming Level: {prog_instruction}
- AI Knowledge: {ai_instruction}
- Learning Style: {style_instruction}
- Language: Use {user.preferred_language.value.upper()} throughout

Your goal is to make this content maximally effective for THIS learner's profile.
"""

    def _get_adaptive_persona(self, user: User) -> str:
        """Generate adaptive persona based on user profile"""
        from tutor_agent.models.user import LearningStyle, ProgrammingExperience

        # Beginners need encouraging tone
        if user.programming_experience == ProgrammingExperience.BEGINNER:
            tone = "Be encouraging and patient. Celebrate small wins. Reduce jargon."
        elif user.programming_experience == ProgrammingExperience.INTERMEDIATE:
            tone = "Be supportive and challenging. Push them to grow. Introduce advanced topics gradually."
        else:
            tone = "Be direct and technical. Engage as a peer. Challenge assumptions."

        # Adjust verbosity based on learning style
        if user.learning_style == LearningStyle.CONCEPTUAL:
            verbosity = "detailed and thorough"
        elif user.learning_style == LearningStyle.PRACTICAL:
            verbosity = "concise and action-oriented"
        else:
            verbosity = "balanced"

        return f"""
Communication Style:
- Tone: {tone}
- Level of detail: {verbosity}
- Approach: Adaptive and learner-centered
"""

    async def generate_personalized_content_stream(
        self,
        original_content: str,
        user: User,
        page_path: str,
        user_query: Optional[str] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Generate personalized content OR answer questions with streaming

        This is the main streaming method that handles both:
        1. Content personalization (when user_query is None)
        2. Q&A interactions (when user_query is provided)

        Args:
            original_content: Original lesson content (can be empty for Q&A)
            user: User object with learning profile
            page_path: Current page path for context
            user_query: Optional direct question from user

        Yields:
            Content chunks as they're generated

        Example:
            # Q&A mode
            async for chunk in agent.generate_personalized_content_stream(
                "", user, "path", user_query="What is Python?"
            ):
                print(chunk, end='', flush=True)

            # Content personalization mode
            async for chunk in agent.generate_personalized_content_stream(
                original_content, user, "path"
            ):
                print(chunk, end='', flush=True)
        """
        # Create personalized agent
        agent = self._create_personalized_agent(user, page_path)

        # Build prompt based on mode
        if user_query:
            # Q&A Mode - Answer user's question
            prompt = f"""The learner asked: "{user_query}"

Please answer this question:
1. Use the search_book_content tool to find relevant information from the book
2. Adapt your explanation to the learner's profile (see your instructions)
3. Provide accurate, book-grounded responses
4. If the topic isn't in the book, acknowledge this and provide general guidance

Provide a helpful, personalized response."""

        else:
            # Content Personalization Mode
            prompt = f"""Please personalize the following lesson content for the learner profile in your instructions.

ORIGINAL LESSON CONTENT:
---
{original_content}
---

Generate a personalized version that:
1. Matches the learner's experience level
2. Adapts to their learning style
3. Uses their preferred language
4. Maintains all key learning objectives
5. Preserves code examples but adapts explanations

Remember: Use the search_book_content tool to find related concepts if needed.
"""

        # Stream response from agent
        result = Runner.run_streamed(agent, input=prompt)

        full_response = ""
        async for event in result.stream_events():
            # Skip raw response events (too granular)
            if event.type == "raw_response_event":
                # Extract text delta for streaming
                if hasattr(event, "data") and hasattr(event.data, "delta"):
                    if hasattr(event.data.delta, "text"):
                        chunk = event.data.delta.text
                        full_response += chunk
                        yield chunk

            elif event.type == "run_item_stream_event":
                # Handle completed items (tool calls, messages)
                if event.item.type == "tool_call_item":
                    # Tool was called (RAG search)
                    pass  # Silent, no need to print

                elif event.item.type == "tool_call_output_item":
                    # Tool output received
                    pass  # Silent

                elif event.item.type == "message_output_item":
                    # Message completed
                    message_text = ItemHelpers.text_message_output(event.item)
                    if message_text and message_text not in full_response:
                        full_response += message_text
                        yield message_text

            elif event.type == "agent_updated_stream_event":
                # Agent changed (e.g., handoff)
                pass  # Silent

        # Ensure we return something even if no streaming occurred
        if not full_response:
            full_response = "Error: No content generated"
            yield full_response

    async def generate_personalized_content(
        self, original_content: str, user: User, page_path: str
    ) -> AsyncGenerator[str, None]:
        """
        Generate personalized content with streaming (legacy method)

        This is a wrapper around generate_personalized_content_stream for backwards compatibility.

        Args:
            original_content: Original lesson content (markdown)
            user: User object with learning profile
            page_path: Current page path

        Yields:
            Content chunks as they're generated

        Example:
            async for chunk in agent.generate_personalized_content(content, user, path):
                print(chunk, end='', flush=True)
        """
        async for chunk in self.generate_personalized_content_stream(
            original_content, user, page_path, user_query=None
        ):
            yield chunk


# ============================================================================
# Singleton Instance
# ============================================================================

_olivia_instance: Optional[OLIVIAAgent] = None


def get_olivia_agent() -> OLIVIAAgent:
    """Get singleton instance of OLIVIA agent"""
    global _olivia_instance
    if _olivia_instance is None:
        _olivia_instance = OLIVIAAgent()
    return _olivia_instance


# ============================================================================
# Test Function
# ============================================================================


async def test_olivia_agent():
    """Test OLIVIA agent with sample user"""
    from tutor_agent.models.user import (
        AIExperience,
        LearningStyle,
        PreferredLanguage,
        ProgrammingExperience,
        User,
    )

    print("🤖 Testing OLIVIA Agent...\n")

    # Create test user
    test_user = User(
        email="test@example.com",
        programming_experience=ProgrammingExperience.BEGINNER,
        ai_experience=AIExperience.NONE,
        learning_style=LearningStyle.VISUAL,
        preferred_language=PreferredLanguage.EN,
    )

    # Sample content
    original_content = """
# Python Functions

Functions are reusable blocks of code that perform specific tasks.

```python
def greet(name):
    return f"Hello, {name}!"
```
"""

    # Generate personalized content
    agent = get_olivia_agent()
    print("Generating personalized content...\n")
    print("-" * 60)

    async for chunk in agent.generate_personalized_content(
        original_content, test_user, "04-Python-Fundamentals/03-functions"
    ):
        print(chunk, end="", flush=True)

    print("\n" + "-" * 60)
    print("\n✅ OLIVIA Agent Test Complete")


if __name__ == "__main__":
    # Run test
    asyncio.run(test_olivia_agent())
