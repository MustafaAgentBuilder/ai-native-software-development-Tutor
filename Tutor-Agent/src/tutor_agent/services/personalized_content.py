"""
Personalized content generation service using OpenAI Agents SDK

This service uses OLIVIA agent with RAG capabilities for context-aware,
personalized learning content generation. Implements Six-Step Prompting
Framework (ACILPR) with real-time book content retrieval.
"""

from typing import Optional
import asyncio

from tutor_agent.models.user import User
from tutor_agent.services.agent.olivia_agent import get_olivia_agent


class PersonalizedContentGenerator:
    """
    Generates personalized learning content using OLIVIA agent

    Features:
    - RAG-powered responses using book embeddings
    - Adaptive prompting based on user profile
    - Streaming support for real-time generation
    - Context-aware personalization
    """

    def __init__(self):
        # Use OLIVIA agent instead of simple OpenAI client
        self.agent = get_olivia_agent()
        self.model = "gpt-4o-mini"  # For tracking purposes

    async def generate_personalized_content_async(
        self,
        original_content: str,
        user: User,
        page_path: str = None
    ) -> str:
        """
        Generate personalized content asynchronously with RAG

        Args:
            original_content: The original lesson content (markdown)
            user: User object with learning profile
            page_path: Current page path for RAG context

        Returns:
            Personalized markdown content
        """
        # Collect all chunks from streaming response
        full_content = ""
        async for chunk in self.agent.generate_personalized_content(
            original_content,
            user,
            page_path or "unknown"
        ):
            full_content += chunk

        return full_content

    def generate_personalized_content(
        self,
        original_content: str,
        user: User,
        page_path: str = None
    ) -> str:
        """
        Generate personalized content (synchronous wrapper)

        Args:
            original_content: The original lesson content (markdown)
            user: User object with learning profile
            page_path: Current page path for RAG context

        Returns:
            Personalized markdown content
        """
        # Run async function in event loop
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If loop is already running, create a new task
                import nest_asyncio
                nest_asyncio.apply()
            return loop.run_until_complete(
                self.generate_personalized_content_async(
                    original_content, user, page_path
                )
            )
        except RuntimeError:
            # If no event loop, create one
            return asyncio.run(
                self.generate_personalized_content_async(
                    original_content, user, page_path
                )
            )


# ============================================================================
# Singleton Instance
# ============================================================================

_generator_instance: Optional[PersonalizedContentGenerator] = None


def get_content_generator() -> PersonalizedContentGenerator:
    """Get singleton instance of content generator"""
    global _generator_instance
    if _generator_instance is None:
        _generator_instance = PersonalizedContentGenerator()
    return _generator_instance
