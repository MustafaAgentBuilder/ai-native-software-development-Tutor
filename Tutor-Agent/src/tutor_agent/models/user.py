# Claude is Work to Build this Project
"""
User models for authentication and profile
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, Text
import enum

from tutor_agent.models.base import Base


class ProgrammingExperience(str, enum.Enum):
    """Programming experience levels"""
    BEGINNER = "beginner"  # Just starting or < 6 months
    INTERMEDIATE = "intermediate"  # 6 months - 2 years
    ADVANCED = "advanced"  # 2+ years


class AIExperience(str, enum.Enum):
    """AI/ML experience levels"""
    NONE = "none"  # No experience with AI
    BASIC = "basic"  # Used AI tools but not built with them
    INTERMEDIATE = "intermediate"  # Built some AI projects
    ADVANCED = "advanced"  # Regular AI/ML development


class LearningStyle(str, enum.Enum):
    """Preferred learning approaches"""
    VISUAL = "visual"  # Diagrams, charts, visual explanations
    PRACTICAL = "practical"  # Code examples, hands-on exercises
    CONCEPTUAL = "conceptual"  # Theory-first, deep explanations
    MIXED = "mixed"  # Combination of all approaches


class PreferredLanguage(str, enum.Enum):
    """Supported languages for content"""
    ENGLISH = "en"
    SPANISH = "es"        # Spanish
    FRENCH = "fr"         # French
    GERMAN = "de"         # German
    CHINESE = "zh"        # Chinese (Simplified)
    JAPANESE = "ja"       # Japanese
    RUSSIAN = "ru"        # Russian
    ARABIC = "ar"         # Arabic
    HINDI = "hi"          # Hindi
    URDU = "ur"           # Urdu
    PORTUGUESE = "pt"     # Portuguese
    ITALIAN = "it"        # Italian
    KOREAN = "ko"         # Korean
    TURKISH = "tr"        # Turkish
    # OLIVIA can teach in ANY language the LLM supports!


class User(Base):
    """User account with authentication and learning profile"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # Learning Profile (collected during signup)
    programming_experience = Column(SQLEnum(ProgrammingExperience), nullable=False)
    ai_experience = Column(SQLEnum(AIExperience), nullable=False)
    learning_style = Column(SQLEnum(LearningStyle), nullable=False)
    preferred_language = Column(SQLEnum(PreferredLanguage), nullable=False, default=PreferredLanguage.ENGLISH)

    # Optional profile fields
    full_name = Column(String(255), nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Integer, default=1, nullable=False)  # Using Integer for SQLite compatibility

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class PersonalizedContent(Base):
    """Cache for generated personalized content"""

    __tablename__ = "personalized_content"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)  # Foreign key to users.id
    page_path = Column(String(500), index=True, nullable=False)

    # Generated content
    markdown_content = Column(Text, nullable=False)

    # Metadata
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    model_version = Column(String(50), nullable=True)  # e.g., "gpt-4o-mini"

    # Profile snapshot at generation time (for cache invalidation)
    programming_experience = Column(SQLEnum(ProgrammingExperience), nullable=False)
    ai_experience = Column(SQLEnum(AIExperience), nullable=False)
    learning_style = Column(SQLEnum(LearningStyle), nullable=False)
    preferred_language = Column(SQLEnum(PreferredLanguage), nullable=False)

    def __repr__(self):
        return f"<PersonalizedContent(user_id={self.user_id}, page={self.page_path})>"

    @property
    def is_valid_for_profile(self, user: User) -> bool:
        """Check if cached content matches current user profile"""
        return (
            self.programming_experience == user.programming_experience
            and self.ai_experience == user.ai_experience
            and self.learning_style == user.learning_style
            and self.preferred_language == user.preferred_language
        )
