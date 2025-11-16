# Claude is Work to Build this Project
"""
Authentication and user profile schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from tutor_agent.models.user import (
    ProgrammingExperience,
    AIExperience,
    LearningStyle,
    PreferredLanguage,
)


# ============================================================================
# Request Schemas
# ============================================================================

class SignupRequest(BaseModel):
    """User signup with 4-question learning profile"""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")

    # 4-Question Learning Profile
    programming_experience: ProgrammingExperience = Field(
        ..., description="Programming experience level"
    )
    ai_experience: AIExperience = Field(..., description="AI/ML experience level")
    learning_style: LearningStyle = Field(..., description="Preferred learning style")
    preferred_language: PreferredLanguage = Field(
        default=PreferredLanguage.ENGLISH, description="Preferred content language"
    )

    # Optional fields
    full_name: Optional[str] = Field(None, description="User's full name")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "learner@example.com",
                "password": "securepassword123",
                "programming_experience": "intermediate",
                "ai_experience": "basic",
                "learning_style": "practical",
                "preferred_language": "en",
                "full_name": "Alex Johnson",
            }
        }


class LoginRequest(BaseModel):
    """User login credentials"""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")

    class Config:
        json_schema_extra = {
            "example": {"email": "learner@example.com", "password": "securepassword123"}
        }


# ============================================================================
# Response Schemas
# ============================================================================

class TokenResponse(BaseModel):
    """JWT token response"""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(
        default=60 * 60 * 24 * 7, description="Token expiration in seconds (7 days)"
    )


class UserProfile(BaseModel):
    """User profile information (excluding password)"""

    id: int
    email: str
    full_name: Optional[str]

    # Learning Profile
    programming_experience: ProgrammingExperience
    ai_experience: AIExperience
    learning_style: LearningStyle
    preferred_language: PreferredLanguage

    # Metadata
    created_at: datetime
    last_login: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True  # Enable ORM mode for SQLAlchemy models


class AuthResponse(BaseModel):
    """Combined authentication response with token and user profile"""

    access_token: str
    token_type: str = "bearer"
    expires_in: int = 60 * 60 * 24 * 7
    user: UserProfile


# ============================================================================
# Personalized Content Schemas
# ============================================================================

class PersonalizedContentRequest(BaseModel):
    """Request for personalized content generation"""

    page_path: str = Field(..., description="Path to the book page (e.g., '01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything')")


class PersonalizedContentResponse(BaseModel):
    """Personalized content response"""

    page_path: str
    markdown_content: str
    generated_at: datetime
    cached: bool = Field(
        ..., description="Whether content was served from cache or freshly generated"
    )
    model_version: Optional[str] = None

    class Config:
        from_attributes = True
