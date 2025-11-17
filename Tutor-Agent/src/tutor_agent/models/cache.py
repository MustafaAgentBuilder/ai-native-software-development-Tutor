# Claude is Work to Build this Project
"""
Cache models for storing generated content

This prevents re-generation and improves response times:
- Summary cache: Public summaries (no user tie)
- Personalized cache: User-specific content with profile snapshot
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index

from tutor_agent.models.base import Base


class SummaryCache(Base):
    """
    Cache for AI-generated summaries

    Summaries are public (not user-specific) and cached indefinitely.
    Regenerated only if content changes or manual refresh requested.
    """

    __tablename__ = "summary_cache"

    id = Column(Integer, primary_key=True, index=True)
    page_path = Column(String(500), unique=True, nullable=False, index=True)

    # Generated content
    summary_content = Column(Text, nullable=False)

    # Metadata
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    model_version = Column(String(50), nullable=True)  # e.g., "gpt-4o-mini"
    word_count = Column(Integer, nullable=True)  # For verification

    def __repr__(self):
        return f"<SummaryCache(page={self.page_path}, words={self.word_count})>"


class PersonalizedCache(Base):
    """
    Cache for personalized content per user per page

    Cache is valid only if user's profile matches the snapshot.
    Invalidated when user updates preferences.
    """

    __tablename__ = "personalized_cache"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    page_path = Column(String(500), nullable=False)

    # Generated content
    personalized_content = Column(Text, nullable=False)

    # Profile snapshot at generation time (for cache validation)
    programming_exp = Column(String(50), nullable=False)
    ai_exp = Column(String(50), nullable=False)
    learning_style = Column(String(50), nullable=False)
    language = Column(String(10), nullable=False)

    # Metadata
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    model_version = Column(String(50), nullable=True)

    # Composite index for fast lookups
    __table_args__ = (
        Index("idx_user_page", "user_id", "page_path"),
    )

    def __repr__(self):
        return f"<PersonalizedCache(user_id={self.user_id}, page={self.page_path})>"

    def is_valid_for_profile(
        self,
        programming_exp: str,
        ai_exp: str,
        learning_style: str,
        language: str
    ) -> bool:
        """Check if cached content matches current user profile"""
        return (
            self.programming_exp == programming_exp
            and self.ai_exp == ai_exp
            and self.learning_style == learning_style
            and self.language == language
        )
