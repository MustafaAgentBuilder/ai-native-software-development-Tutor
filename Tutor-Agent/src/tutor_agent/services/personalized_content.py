"""
Personalized content generation service using OpenAI Agents SDK

This service uses the Six-Step Prompting Framework (ACILPR) and
adaptive prompting patterns to generate personalized learning content
tailored to each user's profile.
"""

from datetime import datetime
from typing import Optional
from openai import OpenAI
import os

from tutor_agent.models.user import (
    User,
    ProgrammingExperience,
    AIExperience,
    LearningStyle,
    PreferredLanguage,
)


class PersonalizedContentGenerator:
    """
    Generates personalized learning content using OpenAI API

    Uses adaptive prompting based on user's:
    - Programming experience level
    - AI/ML experience level
    - Preferred learning style
    - Preferred language
    """

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def generate_personalized_content(
        self, original_content: str, user: User
    ) -> str:
        """
        Generate personalized version of original content

        Args:
            original_content: The original lesson content (markdown)
            user: User object with learning profile

        Returns:
            Personalized markdown content
        """
        # Build adaptive prompt using Six-Step Framework
        system_prompt = self._build_system_prompt(user)
        user_prompt = self._build_user_prompt(original_content, user)

        # Call OpenAI API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,  # Creative but controlled
            max_tokens=2000,  # Limit response length
        )

        personalized_content = response.choices[0].message.content
        return personalized_content

    def _build_system_prompt(self, user: User) -> str:
        """
        Build system prompt using Six-Step Framework (ACILPR)

        1. Actor: Define who OLIVIA is
        2. Context: User's learning profile
        3. Instruction: How to personalize
        4. Limitations: Constraints
        5. Persona: Communication style
        6. Response Format: Output structure
        """
        # 1. ACTOR (Persona)
        actor = """You are OLIVIA, an AI-powered learning tutor specializing in AI-Native Software Development.
Your expertise includes programming, AI/ML, software architecture, and personalized education.
You adapt your teaching style to each learner's unique profile and needs."""

        # 2. CONTEXT (User Profile)
        context = f"""
Current Learner Profile:
- Programming Experience: {user.programming_experience.value.title()}
- AI/ML Experience: {user.ai_experience.value.title()}
- Learning Style: {user.learning_style.value.title()}
- Preferred Language: {user.preferred_language.value.upper()}
"""

        # 3. INSTRUCTION (Task)
        instruction = self._get_adaptive_instruction(user)

        # 4. LIMITATIONS (Constraints)
        limitations = """
Constraints:
- Keep content length similar to original (±20%)
- Preserve all code examples but adapt explanations
- Maintain markdown formatting
- Do NOT add emojis or excessive formatting
- Focus on clarity and learning outcomes
- Cite concepts from original when relevant
"""

        # 5. PERSONA (Communication Style)
        persona = self._get_adaptive_persona(user)

        # 6. RESPONSE FORMAT
        response_format = """
Structure your response as:

# [Title] - Personalized for You

[Adapted introduction based on user's experience level]

## Key Concepts
[Explain concepts using user's preferred learning style]

## Examples
[Code examples with annotations matching user's experience]

## Practice
[Exercises appropriate for user's level]

## Next Steps
[Recommendations based on user's profile]

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
            ai_instruction = "Build on basic AI knowledge. Introduce ML/LLM concepts progressively."
        elif user.ai_experience == AIExperience.INTERMEDIATE:
            ai_instruction = "Assume familiarity with ML basics. Focus on agent architectures and advanced patterns."
        else:  # ADVANCED
            ai_instruction = "Discuss cutting-edge techniques. Reference latest research. Explore complex architectures."

        # Adapt based on learning style
        if user.learning_style == LearningStyle.VISUAL:
            style_instruction = "Use descriptive explanations that paint mental pictures. Suggest diagrams and visual patterns."
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

    def _build_user_prompt(self, original_content: str, user: User) -> str:
        """Build the user prompt with original content"""

        return f"""Please personalize the following lesson content for the learner profile described in your system instructions.

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

Remember: This is for a {user.programming_experience.value} programmer with {user.ai_experience.value} AI experience who prefers {user.learning_style.value} learning.
"""


# Singleton instance
_generator_instance: Optional[PersonalizedContentGenerator] = None


def get_content_generator() -> PersonalizedContentGenerator:
    """Get singleton instance of content generator"""
    global _generator_instance
    if _generator_instance is None:
        _generator_instance = PersonalizedContentGenerator()
    return _generator_instance
