# Claude is Work to Build this Project
"""
Content API endpoints - Three-mode content system
- Original: Raw markdown (no endpoint needed, served by Docusaurus)
- Summary: AI-generated summary (public, no auth)
- Personalized: User-specific content (auth required, streaming)
"""

import json
import time
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect, status
from fastapi.security import HTTPBearer
from pathlib import Path
from sqlalchemy.orm import Session
from typing import Optional, AsyncGenerator

from tutor_agent.core.database import get_db
from tutor_agent.models.user import User
from tutor_agent.schemas.content import (
    SummaryResponse,
    PersonalizedContentResponse,
    PersonalizedContentRequest,
    PreferencesUpdateRequest,
    PreferencesUpdateResponse,
    StreamingProgressEvent,
    StreamingCompleteEvent,
    StreamingErrorEvent,
)
from tutor_agent.services.cache.summary_cache import SummaryCacheManager
from tutor_agent.services.cache.personalization_cache import PersonalizationCacheManager
from tutor_agent.services.agent.olivia_agent import OLIVIAAgent

router = APIRouter()
security = HTTPBearer()

# Path to book source files
# Go up from content.py -> v1 -> api -> tutor_agent -> src -> Tutor-Agent -> project root
BOOK_SOURCE_PATH = Path(__file__).parent.parent.parent.parent.parent.parent / "book-source" / "docs"


# ============================================================================
# Authentication Dependency
# ============================================================================

async def get_current_user(
    credentials: HTTPBearer = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """Get current authenticated user from JWT token"""
    from tutor_agent.api.v1.auth import get_current_user as auth_get_current_user
    return await auth_get_current_user(credentials, db)


# ============================================================================
# Helper Functions
# ============================================================================

def load_original_content(page_path: str) -> str:
    """
    Load original lesson content from book-source

    Args:
        page_path: Relative path to the lesson (e.g.,
                  '01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything')

    Returns:
        Original markdown content

    Raises:
        HTTPException: If file not found
    """
    # Construct full file path
    file_path = BOOK_SOURCE_PATH / f"{page_path}.md"

    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lesson not found: {page_path}",
        )

    # Read file content
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract content after frontmatter
    parts = content.split("---", 2)
    if len(parts) >= 3:
        # Get body after frontmatter
        body = parts[2].strip()

        # Remove tab structure if present
        if '<TabItem value="original"' in body:
            start_marker = '<TabItem value="original"'
            end_marker = '</TabItem>'

            start_idx = body.find(start_marker)
            if start_idx != -1:
                content_start = body.find('>', start_idx) + 1
                content_end = body.find(end_marker, content_start)

                if content_end != -1:
                    original_content = body[content_start:content_end].strip()
                    return original_content

        return body

    return content


# ============================================================================
# Summary Endpoints (Public, No Auth)
# ============================================================================

@router.get("/summary/{page_path:path}", response_model=SummaryResponse)
async def get_summary(
    page_path: str,
    force_regenerate: bool = False,
    db: Session = Depends(get_db),
):
    """
    Get AI-generated summary for a specific page (PUBLIC endpoint)

    Flow:
    1. Check cache for existing summary
    2. If cache exists and force_regenerate=False, return cached
    3. Otherwise, generate new summary with OLIVIA
    4. Cache and return

    Args:
        page_path: Relative path from book-source/docs/ (e.g.,
                  "01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything")
        force_regenerate: Force new generation even if cached

    Returns:
        SummaryResponse with summary content
    """
    cache_manager = SummaryCacheManager(db)

    # Check cache
    if not force_regenerate:
        cached_summary = cache_manager.get(page_path)
        if cached_summary:
            return SummaryResponse(
                page_path=page_path,
                summary_content=cached_summary.summary_content,
                word_count=cached_summary.word_count,
                cached=True,
                generated_at=cached_summary.generated_at,
                model_version=cached_summary.model_version,
            )

    # Generate new summary
    try:
        # Load original content
        original_content = load_original_content(page_path)

        # Generate summary with OLIVIA
        olivia = OLIVIAAgent()

        # Create a simple "summary user" profile (conceptual learner, intermediate)
        from tutor_agent.models.user import (
            ProgrammingExperience,
            AIExperience,
            LearningStyle,
            PreferredLanguage,
        )

        class SummaryUser:
            """Mock user for summary generation (conceptual, balanced)"""
            id = 0
            email = "summary@system.internal"
            hashed_password = ""
            programming_experience = ProgrammingExperience.INTERMEDIATE
            ai_experience = AIExperience.BASIC
            learning_style = LearningStyle.CONCEPTUAL
            preferred_language = PreferredLanguage.ENGLISH

        summary_user = SummaryUser()

        # Generate summary (collecting all chunks)
        summary_instruction = """
        Create a concise summary (200-400 words) of the lesson content.
        Focus on:
        - Main concepts and key takeaways
        - Core ideas in simple language
        - Essential knowledge for understanding the topic

        DO NOT include code examples or diagrams.
        Keep it accessible for all skill levels.
        """

        summary_chunks = []
        async for chunk in olivia.generate_personalized_content_stream(
            original_content=original_content,
            user=summary_user,
            page_path=page_path,
            user_query=summary_instruction,
        ):
            summary_chunks.append(chunk)

        summary_content = "".join(summary_chunks).strip()
        word_count = len(summary_content.split())

        # Cache the summary
        cache_manager.set(
            page_path=page_path,
            summary_content=summary_content,
            model_version="gpt-4o-mini",
            word_count=word_count,
        )

        return SummaryResponse(
            page_path=page_path,
            summary_content=summary_content,
            word_count=word_count,
            cached=False,
            generated_at=datetime.utcnow(),
            model_version="gpt-4o-mini",
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lesson not found: {page_path}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate summary: {str(e)}",
        )


# ============================================================================
# Personalized Content Endpoints (Auth Required)
# ============================================================================

@router.get("/personalized/{page_path:path}", response_model=PersonalizedContentResponse)
async def get_personalized_content(
    page_path: str,
    force_regenerate: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get personalized content for a specific lesson page (AUTH REQUIRED)

    Flow:
    1. Check cache for existing personalized content
    2. Validate cache (profile match)
    3. If cache valid and force_regenerate=False, return cached
    4. Otherwise, generate new personalized content with OLIVIA
    5. Cache and return

    Args:
        page_path: Relative path to lesson
        force_regenerate: Force new generation even if cached
        current_user: Authenticated user (from JWT token)

    Returns:
        PersonalizedContentResponse with adapted content
    """
    cache_manager = PersonalizationCacheManager(db)

    # Check cache
    if not force_regenerate:
        cached_content = cache_manager.get(current_user, page_path)
        if cached_content:
            return PersonalizedContentResponse(
                page_path=page_path,
                personalized_content=cached_content.personalized_content,
                cached=True,
                generated_at=cached_content.generated_at,
                model_version=cached_content.model_version,
                profile_snapshot={
                    "programming_experience": cached_content.programming_exp,
                    "ai_experience": cached_content.ai_exp,
                    "learning_style": cached_content.learning_style,
                    "preferred_language": cached_content.language,
                },
            )

    # Generate new personalized content
    try:
        # Load original content
        original_content = load_original_content(page_path)

        # Generate personalized version with OLIVIA
        olivia = OLIVIAAgent()

        # Collect all chunks
        content_chunks = []
        async for chunk in olivia.generate_personalized_content_stream(
            original_content=original_content,
            user=current_user,
            page_path=page_path,
            user_query=None,  # No specific query, just personalize the lesson
        ):
            content_chunks.append(chunk)

        personalized_content = "".join(content_chunks).strip()

        # Cache the content
        cache_manager.set(
            user=current_user,
            page_path=page_path,
            content=personalized_content,
            model_version="gpt-4o-mini",
        )

        return PersonalizedContentResponse(
            page_path=page_path,
            personalized_content=personalized_content,
            cached=False,
            generated_at=datetime.utcnow(),
            model_version="gpt-4o-mini",
            profile_snapshot={
                "programming_experience": current_user.programming_experience.value,
                "ai_experience": current_user.ai_experience.value,
                "learning_style": current_user.learning_style.value,
                "preferred_language": current_user.preferred_language.value,
            },
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lesson not found: {page_path}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate personalized content: {str(e)}",
        )


# ============================================================================
# WebSocket Streaming Endpoint (Real-Time Personalization)
# ============================================================================

@router.websocket("/ws/personalize/{page_path:path}")
async def websocket_personalize(
    websocket: WebSocket,
    page_path: str,
    db: Session = Depends(get_db),
):
    """
    WebSocket endpoint for real-time streaming of personalized content

    Flow:
    1. Client connects with JWT token in query params
    2. Server validates token and authenticates user
    3. Check cache first
    4. If cache exists, send immediately
    5. Otherwise, stream generation progress in real-time
    6. Send progress events during RAG search and generation
    7. Stream content chunks as they're generated
    8. Send complete event when done

    Query params:
        token: JWT authentication token

    WebSocket Events:
        - type: "progress" - Progress update
        - type: "chunk" - Content chunk
        - type: "complete" - Generation complete
        - type: "error" - Error occurred
    """
    await websocket.accept()

    try:
        # Get token from query params
        token = websocket.query_params.get("token")
        if not token:
            await websocket.send_json({
                "type": "error",
                "error": "Missing authentication token",
            })
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        # Authenticate user
        try:
            from tutor_agent.core.security import decode_access_token

            payload = decode_access_token(token)
            if payload is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            user = db.query(User).filter(User.id == int(user_id)).first()
            if not user or not user.is_active:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        except Exception:
            await websocket.send_json({
                "type": "error",
                "error": "Invalid or expired token",
            })
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        # Check cache first
        cache_manager = PersonalizationCacheManager(db)
        cached_content = cache_manager.get(user, page_path)

        if cached_content:
            # Send cached content immediately
            await websocket.send_json({
                "type": "progress",
                "message": "Loading cached content...",
                "progress": 100.0,
            })

            await websocket.send_json({
                "type": "complete",
                "full_content": cached_content.personalized_content,
                "generated_at": cached_content.generated_at.isoformat(),
                "model_version": cached_content.model_version,
                "cached": True,
            })

            await websocket.close()
            return

        # Generate new content with streaming
        start_time = time.time()

        # Progress: Loading original content
        await websocket.send_json({
            "type": "progress",
            "message": "Loading lesson content...",
            "progress": 10.0,
            "metadata": {"stage": "loading"}
        })

        original_content = load_original_content(page_path)

        # Progress: Initializing OLIVIA
        await websocket.send_json({
            "type": "progress",
            "message": "Initializing OLIVIA tutor...",
            "progress": 20.0,
            "metadata": {"stage": "initialization"}
        })

        olivia = OLIVIAAgent()

        # Progress: RAG search
        await websocket.send_json({
            "type": "progress",
            "message": f"Searching book content with RAG (adapting to {user.learning_style.value} learner)...",
            "progress": 30.0,
            "metadata": {"stage": "rag_search", "learning_style": user.learning_style.value}
        })

        # Progress: Generating personalized content
        await websocket.send_json({
            "type": "progress",
            "message": "Generating personalized content...",
            "progress": 40.0,
            "metadata": {"stage": "generation"}
        })

        # Stream content chunks
        content_chunks = []
        chunk_count = 0

        async for chunk in olivia.generate_personalized_content_stream(
            original_content=original_content,
            user=user,
            page_path=page_path,
            user_query=None,
        ):
            content_chunks.append(chunk)
            chunk_count += 1

            # Send chunk
            await websocket.send_json({
                "type": "chunk",
                "chunk": chunk,
                "progress": min(40.0 + (chunk_count * 2), 95.0),  # Progress from 40% to 95%
            })

        personalized_content = "".join(content_chunks).strip()

        # Cache the content
        await websocket.send_json({
            "type": "progress",
            "message": "Caching content for future visits...",
            "progress": 98.0,
            "metadata": {"stage": "caching"}
        })

        cache_manager.set(
            user=user,
            page_path=page_path,
            content=personalized_content,
            model_version="gpt-4o-mini",
        )

        # Send complete event
        generation_time_ms = int((time.time() - start_time) * 1000)

        await websocket.send_json({
            "type": "complete",
            "full_content": personalized_content,
            "generated_at": datetime.utcnow().isoformat(),
            "model_version": "gpt-4o-mini",
            "generation_time_ms": generation_time_ms,
            "cached": False,
        })

        await websocket.close()

    except WebSocketDisconnect:
        print(f"WebSocket disconnected for page: {page_path}")
    except FileNotFoundError:
        await websocket.send_json({
            "type": "error",
            "error": f"Lesson not found: {page_path}",
        })
        await websocket.close()
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "error": str(e),
            "details": "Failed to generate personalized content",
        })
        await websocket.close()


# ============================================================================
# Preferences Update Endpoint
# ============================================================================

@router.put("/preferences", response_model=PreferencesUpdateResponse)
async def update_preferences(
    request: PreferencesUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update user learning preferences (AUTH REQUIRED)

    When preferences are updated:
    1. Update user profile in database
    2. Invalidate ALL personalized content cache for this user
    3. Return updated profile

    Args:
        request: Preferences to update (only provided fields are updated)
        current_user: Authenticated user

    Returns:
        PreferencesUpdateResponse with success status and updated profile
    """
    try:
        # Track what changed
        changes = []

        # Update provided fields
        if request.programming_experience is not None:
            current_user.programming_experience = request.programming_experience
            changes.append("programming_experience")

        if request.ai_experience is not None:
            current_user.ai_experience = request.ai_experience
            changes.append("ai_experience")

        if request.learning_style is not None:
            current_user.learning_style = request.learning_style
            changes.append("learning_style")

        if request.preferred_language is not None:
            current_user.preferred_language = request.preferred_language
            changes.append("preferred_language")

        # Save changes
        db.commit()
        db.refresh(current_user)

        # Invalidate personalized content cache
        cache_manager = PersonalizationCacheManager(db)
        invalidated_count = cache_manager.invalidate_user(current_user.id)

        return PreferencesUpdateResponse(
            success=True,
            message=f"Updated preferences: {', '.join(changes)}",
            updated_profile={
                "programming_experience": current_user.programming_experience.value,
                "ai_experience": current_user.ai_experience.value,
                "learning_style": current_user.learning_style.value,
                "preferred_language": current_user.preferred_language.value,
            },
            cache_invalidated=True,
            invalidated_count=invalidated_count,
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update preferences: {str(e)}",
        )


# ============================================================================
# Cache Management Endpoints (Development/Admin)
# ============================================================================

@router.delete("/cache/personalized/{page_path:path}")
async def invalidate_personalized_cache(
    page_path: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Invalidate personalized content cache for a specific page

    Args:
        page_path: Page to invalidate cache for
        current_user: Authenticated user

    Returns:
        Success message
    """
    cache_manager = PersonalizationCacheManager(db)
    count = cache_manager.invalidate_page(page_path)

    return {
        "success": True,
        "message": f"Invalidated {count} cached entries for {page_path}",
    }


@router.delete("/cache/summary/{page_path:path}")
async def invalidate_summary_cache(
    page_path: str,
    db: Session = Depends(get_db),
):
    """
    Invalidate summary cache for a specific page (PUBLIC endpoint)

    Args:
        page_path: Page to invalidate cache for

    Returns:
        Success message
    """
    cache_manager = SummaryCacheManager(db)
    success = cache_manager.invalidate(page_path)

    return {
        "success": success,
        "message": f"Invalidated summary cache for {page_path}" if success else "Cache not found",
    }


@router.post("/test-olivia")
async def test_olivia_qa(
    query: str,
    page_path: str = "general",
    db: Session = Depends(get_db),
):
    """
    Test endpoint for OLIVIA Q&A (Development/Testing only)

    This endpoint allows testing OLIVIA's question answering capabilities
    without authentication. It creates a test user profile and streams
    OLIVIA's response.

    Args:
        query: User's question
        page_path: Current page context (optional)

    Returns:
        OLIVIA's response to the question

    Example:
        POST /api/v1/content/test-olivia?query=What is RAG?&page_path=chapter-1
    """
    from tutor_agent.models.user import (
        User,
        ProgrammingExperience,
        AIExperience,
        LearningStyle,
        PreferredLanguage,
    )
    from tutor_agent.services.agent.olivia_agent import get_olivia_agent

    # Create a test user profile (intermediate Python, basic AI, visual learner)
    test_user = User(
        id=999,  # Test user ID
        email="test@example.com",
        programming_experience=ProgrammingExperience.INTERMEDIATE,
        ai_experience=AIExperience.BASIC,
        learning_style=LearningStyle.VISUAL,
        preferred_language=PreferredLanguage.ENGLISH,
    )

    try:
        # Get OLIVIA agent
        olivia = get_olivia_agent()

        # Generate response using Q&A mode
        full_response = ""
        async for chunk in olivia.generate_personalized_content_stream(
            original_content="",  # Empty for Q&A mode
            user=test_user,
            page_path=page_path,
            user_query=query,  # This triggers Q&A mode
        ):
            full_response += chunk

        return {
            "query": query,
            "response": full_response,
            "page_context": page_path,
            "test_profile": "intermediate_visual_learner",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate response: {str(e)}",
        )
