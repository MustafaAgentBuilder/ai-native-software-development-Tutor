#!/usr/bin/env python3
"""
Test script to verify BOOK_SOURCE_PATH resolution
"""

from pathlib import Path

# Simulate the path calculation from content.py
script_path = Path(__file__)  # This file is in Tutor-Agent/
repo_root = script_path.parent.parent  # Go up to repo root
book_source_path = repo_root / "book-source" / "docs"

print("=" * 60)
print("PATH RESOLUTION TEST")
print("=" * 60)
print(f"Script location: {script_path}")
print(f"Repo root: {repo_root}")
print(f"Book source path: {book_source_path}")
print(f"Book source exists: {book_source_path.exists()}")
print()

# Test specific lesson file
test_page_path = "01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything"
test_file = book_source_path / f"{test_page_path}.md"

print("=" * 60)
print("TEST LESSON FILE")
print("=" * 60)
print(f"Test page path: {test_page_path}")
print(f"Full file path: {test_file}")
print(f"File exists: {test_file.exists()}")
print()

if test_file.exists():
    print("✅ SUCCESS: Backend can find lesson files!")
else:
    print("❌ FAILED: Backend cannot find lesson files")
    print("\nListing directory contents:")
    parent_dir = test_file.parent
    if parent_dir.exists():
        print(f"\nFiles in {parent_dir}:")
        for f in parent_dir.iterdir():
            print(f"  - {f.name}")
