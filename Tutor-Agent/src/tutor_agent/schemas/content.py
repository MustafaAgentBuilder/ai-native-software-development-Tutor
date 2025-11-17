# Claude is Work to Build this Project
"""
Content schemas for summary and personalized content
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from tutor_agent.models.user import (
    ProgrammingExperience,
    AIExperience,
    LearningStyle,
    PreferredLanguage,
)


# ============================================================================
# Summary Schemas
# ============================================================================

class SummaryResponse(BaseModel):
    """Response for summary content"""

    page_path: str = Field(..., description="Path to the book page")
    summary_content: str = Field(..., description="AI-generated summary (200-400 words)")
    word_count: int = Field(..., description="Word count of summary")
    cached: bool = Field(..., description="Whether served from cache")
    generated_at: datetime = Field(..., description="When summary was generated")
    model_version: Optional[str] = Field(None, description="AI model used for generation")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "page_path": "01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything",
                "summary_content": "This chapter introduces the revolutionary impact of AI on software development...",
                "word_count": 245,
                "cached": True,
                "generated_at": "2025-11-17T10:30:00Z",
                "model_version": "gpt-4o-mini"
            }
        }


# ============================================================================
# Personalized Content Schemas
# ============================================================================

class PersonalizedContentResponse(BaseModel):
    """Response for personalized content"""

    page_path: str = Field(..., description="Path to the book page")
    personalized_content: str = Field(..., description="User-specific adapted content")
    cached: bool = Field(..., description="Whether served from cache")
    generated_at: datetime = Field(..., description="When content was generated")
    model_version: Optional[str] = Field(None, description="AI model used")

    # Profile snapshot (for transparency)
    profile_snapshot: dict = Field(..., description="User profile used for personalization")

    class Config:
        from_attributes = True


class PersonalizedContentRequest(BaseModel):
    """Request to regenerate personalized content"""

    page_path: str = Field(..., description="Path to the book page")
    force_regenerate: bool = Field(
        default=False,
        description="Force regeneration even if cache exists"
    )


# ============================================================================
# Preferences Update Schemas
# ============================================================================

class PreferencesUpdateRequest(BaseModel):
    """Request to update user learning preferences"""

    programming_experience: Optional[ProgrammingExperience] = Field(
        None, description="Updated programming experience level"
    )
    ai_experience: Optional[AIExperience] = Field(
        None, description="Updated AI/ML experience level"
    )
    learning_style: Optional[LearningStyle] = Field(
        None, description="Updated learning style preference"
    )
    preferred_language: Optional[PreferredLanguage] = Field(
        None, description="Updated preferred language"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "programming_experience": "advanced",
                "learning_style": "visual"
            }
        }


class PreferencesUpdateResponse(BaseModel):
    """Response after updating preferences"""

    success: bool = Field(..., description="Whether update was successful")
    message: str = Field(..., description="Status message")
    updated_profile: dict = Field(..., description="Updated user profile")
    cache_invalidated: bool = Field(
        ...,
        description="Whether personalized content cache was cleared"
    )
    invalidated_count: int = Field(
        default=0,
        description="Number of cached items invalidated"
    )


# ============================================================================
# WebSocket Streaming Schemas
# ============================================================================

class StreamingProgressEvent(BaseModel):
    """Progress event during content generation"""

    type: str = Field(..., description="Event type: 'progress', 'chunk', 'complete', 'error'")
    message: Optional[str] = Field(None, description="Progress message")
    chunk: Optional[str] = Field(None, description="Content chunk (for type='chunk')")
    progress: Optional[float] = Field(None, description="Progress percentage (0-100)")
    metadata: Optional[dict] = Field(None, description="Additional metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "type": "progress",
                "message": "Searching book content with RAG...",
                "progress": 25.0,
                "metadata": {"stage": "rag_search"}
            }
        }


class StreamingCompleteEvent(BaseModel):
    """Final event when streaming completes"""

    type: str = Field(default="complete", description="Event type")
    full_content: str = Field(..., description="Complete generated content")
    generated_at: datetime = Field(..., description="Generation timestamp")
    model_version: str = Field(..., description="AI model used")
    total_tokens: Optional[int] = Field(None, description="Total tokens used")
    generation_time_ms: Optional[int] = Field(None, description="Generation time in milliseconds")


class StreamingErrorEvent(BaseModel):
    """Error event during streaming"""

    type: str = Field(default="error", description="Event type")
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Detailed error information")
