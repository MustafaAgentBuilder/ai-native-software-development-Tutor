# Claude is Work to Build this Project
"""
Personalization cache manager

Handles storage and retrieval of personalized content with profile validation.
"""

from typing import Optional
from sqlalchemy.orm import Session

from tutor_agent.models.cache import PersonalizedCache
from tutor_agent.models.user import User


class PersonalizationCacheManager:
    """
    Manages personalized content cache

    Features:
    - Get cached content if profile matches
    - Store new personalized content with profile snapshot
    - Invalidate cache when user changes preferences
    - Automatic cache validation
    """

    def __init__(self, db: Session):
        self.db = db

    def get(self, user: User, page_path: str) -> Optional[PersonalizedCache]:
        """
        Get cached personalized content for user and page

        Returns:
            Cached PersonalizedCache object if exists and profile matches, None otherwise
        """
        # Find cached entry
        cached = (
            self.db.query(PersonalizedCache)
            .filter(
                PersonalizedCache.user_id == user.id,
                PersonalizedCache.page_path == page_path
            )
            .first()
        )

        if not cached:
            return None

        # Validate cache against current profile
        if cached.is_valid_for_profile(
            programming_exp=user.programming_experience.value,
            ai_exp=user.ai_experience.value,
            learning_style=user.learning_style.value,
            language=user.preferred_language.value
        ):
            return cached

        # Cache invalid (profile changed) - delete it
        self.db.delete(cached)
        self.db.commit()
        return None

    def set(
        self,
        user: User,
        page_path: str,
        content: str,
        model_version: str = "gpt-4o-mini"
    ) -> PersonalizedCache:
        """
        Store personalized content with profile snapshot

        Args:
            user: User object with current profile
            page_path: Page identifier
            content: Generated personalized content
            model_version: Model used for generation

        Returns:
            Created cache entry
        """
        # Check if entry exists
        existing = (
            self.db.query(PersonalizedCache)
            .filter(
                PersonalizedCache.user_id == user.id,
                PersonalizedCache.page_path == page_path
            )
            .first()
        )

        if existing:
            # Update existing
            existing.personalized_content = content
            existing.programming_exp = user.programming_experience.value
            existing.ai_exp = user.ai_experience.value
            existing.learning_style = user.learning_style.value
            existing.language = user.preferred_language.value
            existing.model_version = model_version
            cached = existing
        else:
            # Create new
            cached = PersonalizedCache(
                user_id=user.id,
                page_path=page_path,
                personalized_content=content,
                programming_exp=user.programming_experience.value,
                ai_exp=user.ai_experience.value,
                learning_style=user.learning_style.value,
                language=user.preferred_language.value,
                model_version=model_version
            )
            self.db.add(cached)

        self.db.commit()
        self.db.refresh(cached)
        return cached

    def invalidate_user(self, user_id: int) -> int:
        """
        Delete all cached content for a user

        Called when user updates their preferences.

        Args:
            user_id: User ID to invalidate

        Returns:
            Number of entries deleted
        """
        count = (
            self.db.query(PersonalizedCache)
            .filter(PersonalizedCache.user_id == user_id)
            .delete()
        )
        self.db.commit()
        return count

    def invalidate_page(self, page_path: str) -> int:
        """
        Delete all cached content for a specific page

        Called when page content is updated.

        Args:
            page_path: Page identifier

        Returns:
            Number of entries deleted
        """
        count = (
            self.db.query(PersonalizedCache)
            .filter(PersonalizedCache.page_path == page_path)
            .delete()
        )
        self.db.commit()
        return count

    def get_user_cache_stats(self, user_id: int) -> dict:
        """Get cache statistics for a user"""
        count = (
            self.db.query(PersonalizedCache)
            .filter(PersonalizedCache.user_id == user_id)
            .count()
        )

        return {
            "total_cached_pages": count,
            "user_id": user_id
        }
