"""
Summary Generation Script for TutorGPT Platform
Generates 200-400 word summaries for all Part 1 pages using OLIVIA agent
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import asyncio

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from openai import AsyncOpenAI
    from pydantic import BaseModel, Field
except ImportError:
    print("Installing required dependencies...")
    os.system("uv add openai pydantic")
    from openai import AsyncOpenAI
    from pydantic import BaseModel, Field


# ============================================================================
# Configuration
# ============================================================================

BOOK_SOURCE_DIR = Path(__file__).parent.parent.parent / "book-source" / "docs"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "generated_summaries"
PART_1_CHAPTERS = [
    "01-Introducing-AI-Driven-Development",
    "02-AI-Tool-Landscape",
    "03-Markdown-Prompt-Context-Engineering",
    "04-Python-Fundamentals"
]

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================================
# Structured Output Models (Pydantic)
# ============================================================================

class BookPageSummary(BaseModel):
    """Structured summary output"""
    summary: str = Field(
        description="Concise summary (200-400 words) of the page content",
        min_length=200,
        max_length=2000
    )
    key_concepts: List[str] = Field(
        description="3-5 key concepts covered in this page",
        min_length=3,
        max_length=5
    )
    difficulty_level: str = Field(
        description="beginner, intermediate, or advanced"
    )
    estimated_read_time: int = Field(
        description="Estimated read time in minutes"
    )

class SummaryMetadata(BaseModel):
    """Metadata for generated summary"""
    page_path: str
    chapter: str
    original_file: str
    generated_at: str
    model_used: str
    tokens_used: int
    generation_time_ms: int


# ============================================================================
# OLIVIA Agent for Summary Generation
# ============================================================================

class OLIVIASummaryAgent:
    """
    OLIVIA - AI Tutor for Book Content Summarization

    Uses OpenAI Agents SDK patterns with proper prompt engineering (ACILPR)
    """

    def __init__(self, api_key: str = None):
        # Get API key from environment or parameter
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")

        self.client = AsyncOpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"  # Fast and cost-effective for summaries

        # ACILPR Framework - Complete Agent Instructions
        self.system_instructions = """
# OLIVIA - AI Tutor for Book Content Summarization

## Actor (Persona)
You are OLIVIA, an expert educational content analyst and AI tutor specializing
in technical education. You have deep expertise in:
- AI-driven software development
- Python programming and tools
- Learning science and pedagogy
- Technical writing and summarization

Your approach is precise, student-focused, and pedagogically sound.

## Context
You are creating summaries for the "AI Native Software Development" book.
Your summaries will be used by:
- Students learning AI-driven development
- Professionals transitioning to AI-first workflows
- Learners with varying experience levels (beginner to advanced)

These summaries appear in a three-tab interface (Original, Summary, Personalized).
The Summary tab provides quick understanding without reading full content.

## Instruction (Task)
For each book page provided:

1. **Read and Analyze**: Understand the complete content
2. **Identify Core Concepts**: Extract 3-5 key takeaways
3. **Generate Summary**: Create a 200-400 word summary that:
   - Captures main ideas and learning objectives
   - Preserves technical accuracy
   - Uses clear, accessible language
   - Maintains logical flow
   - Highlights practical applications
4. **Assess Difficulty**: Classify as beginner/intermediate/advanced
5. **Estimate Read Time**: Calculate original content read time

## Limitations (Constraints)
You MUST:
- Keep summaries between 200-400 words (strict)
- Preserve all technical terms exactly as written
- Cite specific examples from the content when relevant
- Maintain the author's intended meaning

You MUST NOT:
- Add information not in the original content
- Oversimplify to the point of losing accuracy
- Use jargon without context
- Exceed 400 words in summary

## Persona Traits
- Communication style: Clear, educational, encouraging
- Tone: Professional yet approachable
- Level of detail: Balanced - thorough but concise
- Decision-making: Evidence-based, pedagogically sound

## Response Format
Output MUST be valid JSON matching the BookPageSummary schema:
{
  "summary": "200-400 word summary here...",
  "key_concepts": ["Concept 1", "Concept 2", "Concept 3"],
  "difficulty_level": "beginner|intermediate|advanced",
  "estimated_read_time": <number in minutes>
}

## Cognitive Control (Self-Verification)
Before outputting, verify:
✓ Summary is 200-400 words
✓ All key concepts are from original content
✓ Technical terms are preserved
✓ JSON is valid and matches schema
✓ Difficulty level is appropriate
✓ Read time is realistic (avg 200 words/min)

If any check fails, FIX before outputting.
"""

    async def generate_summary(
        self,
        page_content: str,
        page_path: str
    ) -> tuple[BookPageSummary, SummaryMetadata]:
        """
        Generate summary using OLIVIA agent with OpenAI

        Returns:
            (summary_data, metadata)
        """
        start_time = datetime.now()

        # Create prompt with context
        user_prompt = f"""
Page Path: {page_path}

Content to Summarize:
{page_content}

Generate a comprehensive yet concise summary following all instructions.
"""

        try:
            # Call OpenAI with structured output
            response = await self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_instructions},
                    {"role": "user", "content": user_prompt}
                ],
                response_format=BookPageSummary,
                temperature=0.3,  # Low for consistency
                max_tokens=1000
            )

            # Extract summary data
            summary_data = response.choices[0].message.parsed

            # Calculate metadata
            generation_time = (datetime.now() - start_time).total_seconds() * 1000
            metadata = SummaryMetadata(
                page_path=page_path,
                chapter=self._extract_chapter(page_path),
                original_file=page_path,
                generated_at=datetime.now().isoformat(),
                model_used=self.model,
                tokens_used=response.usage.total_tokens,
                generation_time_ms=int(generation_time)
            )

            return summary_data, metadata

        except Exception as e:
            print(f"❌ Error generating summary for {page_path}: {e}")
            raise

    def _extract_chapter(self, page_path: str) -> str:
        """Extract chapter from path"""
        for chapter in PART_1_CHAPTERS:
            if chapter in page_path:
                return chapter
        return "unknown"


# ============================================================================
# File System Operations
# ============================================================================

def find_all_part1_pages() -> List[Path]:
    """Find all markdown pages in Part 1"""
    pages = []

    for chapter in PART_1_CHAPTERS:
        chapter_dir = BOOK_SOURCE_DIR / chapter
        if chapter_dir.exists():
            # Find all .md files, excluding READMEs and quizzes
            md_files = chapter_dir.rglob("*.md")
            for md_file in md_files:
                if md_file.name.lower() not in ["readme.md", "readme"]:
                    if "quiz" not in md_file.name.lower():
                        pages.append(md_file)

    return sorted(pages)


def read_page_content(page_path: Path) -> str:
    """Read markdown content from file"""
    try:
        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"❌ Error reading {page_path}: {e}")
        return ""


def save_summary(
    summary: BookPageSummary,
    metadata: SummaryMetadata,
    original_path: Path
) -> Path:
    """Save summary and metadata to files"""
    # Create filename from original path
    relative_path = original_path.relative_to(BOOK_SOURCE_DIR)
    safe_name = str(relative_path).replace("/", "_").replace("\\", "_")

    # Save summary markdown
    summary_file = OUTPUT_DIR / f"{safe_name}"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"---\n")
        f.write(f"original: {metadata.page_path}\n")
        f.write(f"chapter: {metadata.chapter}\n")
        f.write(f"generated_at: {metadata.generated_at}\n")
        f.write(f"model: {metadata.model_used}\n")
        f.write(f"difficulty: {summary.difficulty_level}\n")
        f.write(f"read_time: {summary.estimated_read_time} min\n")
        f.write(f"---\n\n")
        f.write(f"# Summary\n\n")
        f.write(f"{summary.summary}\n\n")
        f.write(f"## Key Concepts\n\n")
        for concept in summary.key_concepts:
            f.write(f"- {concept}\n")

    # Save metadata JSON
    metadata_file = OUTPUT_DIR / f"{safe_name}.meta.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata.model_dump(), f, indent=2)

    return summary_file


# ============================================================================
# Main Execution
# ============================================================================

async def generate_all_summaries(
    limit: int = None,
    skip_existing: bool = True
) -> Dict[str, int]:
    """
    Generate summaries for all Part 1 pages

    Args:
        limit: Maximum number of pages to process (None = all)
        skip_existing: Skip pages that already have summaries

    Returns:
        Statistics dictionary
    """
    print("🚀 OLIVIA Summary Generation Starting...")
    print(f"📂 Book source: {BOOK_SOURCE_DIR}")
    print(f"💾 Output directory: {OUTPUT_DIR}")
    print()

    # Initialize OLIVIA
    olivia = OLIVIASummaryAgent()

    # Find all pages
    all_pages = find_all_part1_pages()
    total_pages = len(all_pages)

    if limit:
        all_pages = all_pages[:limit]
        print(f"📊 Processing {len(all_pages)} of {total_pages} pages (limit={limit})")
    else:
        print(f"📊 Processing all {total_pages} pages")

    print()

    # Statistics
    stats = {
        "total": len(all_pages),
        "success": 0,
        "failed": 0,
        "skipped": 0,
        "total_tokens": 0,
        "total_time_ms": 0
    }

    # Process each page
    for idx, page_path in enumerate(all_pages, 1):
        relative_path = page_path.relative_to(BOOK_SOURCE_DIR)
        safe_name = str(relative_path).replace("/", "_").replace("\\", "_")
        output_file = OUTPUT_DIR / safe_name

        # Skip if exists
        if skip_existing and output_file.exists():
            print(f"⏭️  [{idx}/{len(all_pages)}] Skipping (exists): {relative_path}")
            stats["skipped"] += 1
            continue

        print(f"📝 [{idx}/{len(all_pages)}] Processing: {relative_path}")

        try:
            # Read content
            content = read_page_content(page_path)
            if not content or len(content) < 50:
                print(f"   ⚠️  Skipping empty/too short page")
                stats["skipped"] += 1
                continue

            # Generate summary
            summary, metadata = await olivia.generate_summary(
                page_content=content,
                page_path=str(relative_path)
            )

            # Save to files
            saved_path = save_summary(summary, metadata, page_path)

            # Update stats
            stats["success"] += 1
            stats["total_tokens"] += metadata.tokens_used
            stats["total_time_ms"] += metadata.generation_time_ms

            print(f"   ✅ Summary saved: {saved_path.name}")
            print(f"   📊 Tokens: {metadata.tokens_used} | Time: {metadata.generation_time_ms}ms")
            print(f"   🎯 Difficulty: {summary.difficulty_level} | Read time: {summary.estimated_read_time} min")
            print()

            # Small delay to respect rate limits
            await asyncio.sleep(0.5)

        except Exception as e:
            print(f"   ❌ Failed: {e}")
            stats["failed"] += 1
            print()
            continue

    # Print final statistics
    print("=" * 60)
    print("📊 Summary Generation Complete!")
    print("=" * 60)
    print(f"✅ Success: {stats['success']}")
    print(f"❌ Failed: {stats['failed']}")
    print(f"⏭️  Skipped: {stats['skipped']}")
    print(f"📊 Total pages: {stats['total']}")
    print(f"🪙 Total tokens used: {stats['total_tokens']:,}")
    print(f"⏱️  Total time: {stats['total_time_ms'] / 1000:.2f}s")
    if stats['success'] > 0:
        print(f"⚡ Avg time per page: {stats['total_time_ms'] / stats['success']:.0f}ms")
    print("=" * 60)

    return stats


async def test_single_page():
    """Test with a single page"""
    print("🧪 Testing OLIVIA with a single page...")

    pages = find_all_part1_pages()
    if not pages:
        print("❌ No pages found!")
        return

    test_page = pages[0]
    print(f"📄 Test page: {test_page.name}")

    olivia = OLIVIASummaryAgent()
    content = read_page_content(test_page)

    if content:
        summary, metadata = await olivia.generate_summary(
            page_content=content,
            page_path=str(test_page.relative_to(BOOK_SOURCE_DIR))
        )

        print("\n✅ Summary Generated:")
        print(f"\nSummary ({len(summary.summary.split())} words):")
        print(summary.summary)
        print(f"\nKey Concepts: {', '.join(summary.key_concepts)}")
        print(f"Difficulty: {summary.difficulty_level}")
        print(f"Read Time: {summary.estimated_read_time} min")
        print(f"\nTokens: {metadata.tokens_used}")
        print(f"Generation Time: {metadata.generation_time_ms}ms")


# ============================================================================
# CLI Interface
# ============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate summaries for Part 1 pages using OLIVIA agent"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test with a single page first"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of pages to process"
    )
    parser.add_argument(
        "--no-skip",
        action="store_true",
        help="Regenerate even if summary exists"
    )

    args = parser.parse_args()

    if args.test:
        asyncio.run(test_single_page())
    else:
        asyncio.run(generate_all_summaries(
            limit=args.limit,
            skip_existing=not args.no_skip
        ))
