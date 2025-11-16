# Claude is Work to Build this Project
"""
Content API endpoints - Summaries, personalized content, and book content
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.security import HTTPBearer
from pathlib import Path
from sqlalchemy.orm import Session
from typing import Optional
import re

from tutor_agent.core.database import get_db
from tutor_agent.models.user import User, PersonalizedContent
from tutor_agent.schemas.auth import PersonalizedContentResponse
from tutor_agent.services.personalized_content import get_content_generator

router = APIRouter()
security = HTTPBearer()

# Path to summaries directory (relative to project root)
SUMMARIES_DIR = Path(__file__).parent.parent.parent.parent.parent / "book-source" / "summaries"

# Path to book source files
BOOK_SOURCE_PATH = Path(__file__).parent.parent.parent.parent.parent / "book-source" / "docs"

def normalize_page_path(page_path: str) -> str:
    """
    Normalize page path to match summary filename format

    Examples:
        "01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything.md"
        -> "01-Introducing-AI-Driven-Development_01-moment_that_changed_everything.md"
    """
    # Remove 'docs/' prefix if present
    page_path = page_path.replace('docs/', '')

    # Extract chapter and filename
    parts = page_path.split('/')
    if len(parts) < 2:
        return None

    chapter = parts[0]  # e.g., "01-Introducing-AI-Driven-Development"
    filename = parts[-1]  # e.g., "01-moment_that_changed_everything.md"

    # Create summary filename
    summary_filename = f"{chapter}_{filename}"

    return summary_filename

def find_summary_file(page_path: str) -> Optional[Path]:
    """Find summary file for given page path"""
    summary_filename = normalize_page_path(page_path)

    if not summary_filename:
        return None

    summary_path = SUMMARIES_DIR / summary_filename

    if summary_path.exists():
        return summary_path

    return None

def parse_summary_content(summary_path: Path) -> dict:
    """Parse summary markdown file and extract frontmatter + content"""
    try:
        content = summary_path.read_text(encoding='utf-8')

        # Split frontmatter and body
        parts = content.split('---', 2)
        if len(parts) < 3:
            # No frontmatter, treat whole content as summary
            return {
                "summary": content,
                "key_concepts": [],
                "metadata": {}
            }

        frontmatter = parts[1].strip()
        body = parts[2].strip()

        # Parse frontmatter (simple YAML parsing)
        metadata = {}
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()

        # Extract summary and key concepts from body
        summary_text = ""
        key_concepts = []

        # Split by headers
        sections = body.split('##')
        for section in sections:
            section = section.strip()
            if section.startswith('Summary'):
                # Extract summary content (remove header)
                summary_text = section.replace('Summary', '', 1).strip()
            elif section.startswith('Key Concepts'):
                # Extract bullet points
                lines = section.split('\n')[1:]  # Skip header line
                for line in lines:
                    line = line.strip()
                    if line.startswith('-'):
                        concept = line.lstrip('- ').strip()
                        if concept:
                            key_concepts.append(concept)

        return {
            "summary": summary_text,
            "key_concepts": key_concepts,
            "metadata": metadata
        }

    except Exception as e:
        print(f"Error parsing summary: {e}")
        return {
            "summary": "",
            "key_concepts": [],
            "metadata": {}
        }

@router.get("/summary")
async def get_summary(
    page_path: str = Query(..., description="Relative path to the page from book-source/docs/")
):
    """
    Get summary for a specific page

    Parameters:
    - page_path: Relative path from book-source/docs/, e.g.,
      "01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything.md"

    Returns:
    - Summary content with metadata and key concepts
    - OR "Team Working on it" message if summary doesn't exist yet
    """

    # Find summary file
    summary_path = find_summary_file(page_path)

    if not summary_path:
        # Summary doesn't exist yet
        return {
            "status": "pending",
            "message": "🔧 Team Working on it!",
            "summary": "Our team is currently preparing a summary for this page. Check back soon!",
            "key_concepts": [],
            "metadata": {
                "page_path": page_path,
                "generated": False
            }
        }

    # Parse and return summary
    parsed_data = parse_summary_content(summary_path)

    return {
        "status": "available",
        "message": "Summary available",
        **parsed_data,
        "metadata": {
            **parsed_data.get("metadata", {}),
            "page_path": page_path,
            "generated": True
        }
    }

@router.get("/summary/list")
async def list_available_summaries():
    """
    List all available summaries

    Returns:
    - List of all summary files with metadata
    """

    if not SUMMARIES_DIR.exists():
        return {
            "count": 0,
            "summaries": []
        }

    summaries = []
    for summary_file in SUMMARIES_DIR.glob("*.md"):
        parsed = parse_summary_content(summary_file)
        summaries.append({
            "filename": summary_file.name,
            "chapter": parsed["metadata"].get("chapter", "Unknown"),
            "original_path": parsed["metadata"].get("original_path", ""),
            "difficulty": parsed["metadata"].get("difficulty", ""),
            "read_time": parsed["metadata"].get("read_time", "")
        })

    return {
        "count": len(summaries),
        "summaries": sorted(summaries, key=lambda x: x["filename"])
    }


# ============================================================================
# Personalized Content Endpoints
# ============================================================================

async def get_current_user_from_token(
    credentials: HTTPBearer = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """Get current user from JWT token"""
    from tutor_agent.api.v1.auth import get_current_user
    return await get_current_user(credentials, db)


def load_original_content(page_path: str) -> str:
    """
    Load original lesson content from book-source

    Args:
        page_path: Relative path to the lesson (e.g., '01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything')

    Returns:
        Original markdown content

    Raises:
        HTTPException: If file not found
    """
    # Construct full file path
    file_path = BOOK_SOURCE_PATH / f"{page_path}.md"

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Lesson not found: {page_path}",
        )

    # Read file content
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract content after frontmatter and before tabs
    # Look for the end of frontmatter (second ---)
    parts = content.split("---", 2)
    if len(parts) >= 3:
        # Get body after frontmatter
        body = parts[2]

        # Remove tab structure if present
        # Content is between <TabItem value="original"...> and </TabItem>
        if '<TabItem value="original"' in body:
            # Extract original tab content
            start_marker = '<TabItem value="original"'
            end_marker = '</TabItem>'

            start_idx = body.find(start_marker)
            if start_idx != -1:
                # Find the end of the opening tag
                content_start = body.find('>', start_idx) + 1

                # Find the first </TabItem>
                content_end = body.find(end_marker, content_start)

                if content_end != -1:
                    # Extract just the original content
                    original_content = body[content_start:content_end].strip()
                    return original_content

        # If no tabs structure, return body as is
        return body.strip()

    return content


@router.get("/personalized/{page_path:path}", response_model=PersonalizedContentResponse)
async def get_personalized_content(
    page_path: str,
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    """
    Get personalized content for a specific lesson page

    Workflow:
    1. Check if cached personalized content exists for this user + page
    2. Validate cache (profile match)
    3. If cache valid, return cached content
    4. If cache invalid/missing, generate new personalized content
    5. Save to cache and return

    Args:
        page_path: Relative path to lesson (e.g., '01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything')
        current_user: Authenticated user (from JWT token)

    Returns:
        PersonalizedContentResponse with markdown content
    """
    # 1. Check for cached content
    cached_content = (
        db.query(PersonalizedContent)
        .filter(
            PersonalizedContent.user_id == current_user.id,
            PersonalizedContent.page_path == page_path,
        )
        .first()
    )

    # 2. Validate cache (check if profile matches)
    if cached_content:
        is_valid = (
            cached_content.programming_experience == current_user.programming_experience
            and cached_content.ai_experience == current_user.ai_experience
            and cached_content.learning_style == current_user.learning_style
            and cached_content.preferred_language == current_user.preferred_language
        )

        if is_valid:
            # Return cached content
            return PersonalizedContentResponse(
                page_path=page_path,
                markdown_content=cached_content.markdown_content,
                generated_at=cached_content.generated_at,
                cached=True,
                model_version=cached_content.model_version,
            )

        # Cache invalid (profile changed), delete old cache
        db.delete(cached_content)
        db.commit()

    # 3. Generate new personalized content
    try:
        # Load original content
        original_content = load_original_content(page_path)

        # Generate personalized version (with RAG-powered OLIVIA agent)
        generator = get_content_generator()
        personalized_markdown = generator.generate_personalized_content(
            original_content, current_user, page_path  # Pass page_path for RAG context
        )

        # 4. Save to cache
        new_cached_content = PersonalizedContent(
            user_id=current_user.id,
            page_path=page_path,
            markdown_content=personalized_markdown,
            generated_at=datetime.utcnow(),
            model_version=generator.model,
            # Snapshot profile for cache validation
            programming_experience=current_user.programming_experience,
            ai_experience=current_user.ai_experience,
            learning_style=current_user.learning_style,
            preferred_language=current_user.preferred_language,
        )

        db.add(new_cached_content)
        db.commit()
        db.refresh(new_cached_content)

        # 5. Return response
        return PersonalizedContentResponse(
            page_path=page_path,
            markdown_content=personalized_markdown,
            generated_at=new_cached_content.generated_at,
            cached=False,
            model_version=generator.model,
        )

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404, detail=f"Lesson not found: {page_path}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate personalized content: {str(e)}",
        )


# ============================================================================
# OLIVIA Agent Test Endpoint (Development Only)
# ============================================================================

@router.post("/test-olivia")
async def test_olivia_agent(
    query: str = Query(..., description="Question to ask OLIVIA"),
    page_path: Optional[str] = Query(None, description="Optional page context")
):
    """
    🧪 Test endpoint for OLIVIA agent (Development/Testing only)

    Test the RAG-powered OLIVIA agent without authentication.

    Args:
        query: Question to ask OLIVIA
        page_path: Optional page path for context

    Returns:
        OLIVIA's response with RAG-powered answer
    """
    try:
        from tutor_agent.services.agent.olivia_agent import OLIVIAAgent
        from tutor_agent.models.user import User
        from enum import Enum

        # Create mock user for testing
        class MockExperience(Enum):
            BEGINNER = "beginner"
            INTERMEDIATE = "intermediate"
            ADVANCED = "advanced"

        class MockUser:
            def __init__(self):
                self.id = 999
                self.email = "test@example.com"
                self.name = "Test User"
                self.programming_experience = type('obj', (object,), {'value': 'intermediate'})()
                self.ai_experience = type('obj', (object,), {'value': 'beginner'})()
                self.learning_style = type('obj', (object,), {'value': 'visual'})()
                self.preferred_language = type('obj', (object,), {'value': 'en'})()

        test_user = MockUser()

        # Initialize OLIVIA
        olivia = OLIVIAAgent()

        # Generate response (collecting streaming chunks)
        response_chunks = []
        async for chunk in olivia.generate_personalized_content_stream(
            original_content="",
            user=test_user,
            page_path=page_path or "test",
            user_query=query
        ):
            response_chunks.append(chunk)

        full_response = "".join(response_chunks)

        return {
            "status": "success",
            "query": query,
            "page_path": page_path,
            "response": full_response,
            "user_profile": {
                "programming": "intermediate",
                "ai_experience": "beginner",
                "learning_style": "visual"
            },
            "note": "This is a test endpoint using a mock user profile"
        }

    except Exception as e:
        import traceback
        return {
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }
