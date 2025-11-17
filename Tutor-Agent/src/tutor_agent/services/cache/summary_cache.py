# Claude is Work to Build this Project
"""
Summary cache manager

Handles storage and retrieval of AI-generated summaries (public, no user tie).
"""

from typing import Optional
from sqlalchemy.orm import Session

from tutor_agent.models.cache import SummaryCache


class SummaryCacheManager:
    """
    Manages public summary cache

    Features:
    - Get cached summary by page path
    - Store new summaries
    - Invalidate when content changes
    """

    def __init__(self, db: Session):
        self.db = db

    def get(self, page_path: str) -> Optional[str]:
        """
        Get cached summary for a page

        Args:
            page_path: Page identifier

        Returns:
            Cached summary content or None
        """
        cached = (
            self.db.query(SummaryCache)
            .filter(SummaryCache.page_path == page_path)
            .first()
        )

        return cached.summary_content if cached else None

    def set(
        self,
        page_path: str,
        summary_content: str,
        model_version: str = "gpt-4o-mini",
        word_count: Optional[int] = None
    ) -> SummaryCache:
        """
        Store summary for a page

        Args:
            page_path: Page identifier
            summary_content: Generated summary (200-400 words)
            model_version: Model used for generation
            word_count: Word count for verification

        Returns:
            Created/updated cache entry
        """
        # Check if exists
        existing = (
            self.db.query(SummaryCache)
            .filter(SummaryCache.page_path == page_path)
            .first()
        )

        if not word_count:
            word_count = len(summary_content.split())

        if existing:
            # Update
            existing.summary_content = summary_content
            existing.model_version = model_version
            existing.word_count = word_count
            cached = existing
        else:
            # Create
            cached = SummaryCache(
                page_path=page_path,
                summary_content=summary_content,
                model_version=model_version,
                word_count=word_count
            )
            self.db.add(cached)

        self.db.commit()
        self.db.refresh(cached)
        return cached

    def invalidate(self, page_path: str) -> bool:
        """
        Delete cached summary for a page

        Args:
            page_path: Page identifier

        Returns:
            True if deleted, False if not found
        """
        count = (
            self.db.query(SummaryCache)
            .filter(SummaryCache.page_path == page_path)
            .delete()
        )
        self.db.commit()
        return count > 0

    def get_stats(self) -> dict:
        """Get cache statistics"""
        count = self.db.query(SummaryCache).count()

        return {
            "total_cached_summaries": count
        }
