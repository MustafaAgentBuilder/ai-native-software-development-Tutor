#!/usr/bin/env python3
"""
Generate ChromaDB embeddings from book markdown files

This script:
1. Reads all markdown files from book-source/docs/
2. Splits them into chunks (with metadata)
3. Creates embeddings using sentence-transformers/all-mpnet-base-v2 (768 dimensions)
4. Stores in ChromaDB at Tutor-Agent/data/embeddings/
"""

import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
import re
from typing import List, Dict
import hashlib


def extract_metadata_from_path(file_path: Path, root_docs: Path) -> Dict[str, str]:
    """Extract chapter and part info from file path"""
    relative_path = file_path.relative_to(root_docs)
    parts = relative_path.parts

    # Example: 01-Introducing-AI-Driven-Development/index.md
    if len(parts) >= 2:
        chapter_dir = parts[0]
        # Extract chapter number and name
        match = re.match(r'(\d+)-(.*)', chapter_dir)
        if match:
            chapter_num, chapter_name = match.groups()
            chapter_name = chapter_name.replace('-', ' ')
            return {
                'chapter_number': chapter_num,
                'chapter_name': chapter_name,
                'chapter': f"Chapter {chapter_num}: {chapter_name}",
                'file_name': parts[-1]
            }

    # Preface or other top-level files
    return {
        'chapter_number': '0',
        'chapter_name': 'Preface',
        'chapter': 'Preface',
        'file_name': file_path.name
    }


def chunk_markdown(content: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Split markdown content into chunks with overlap

    Args:
        content: Markdown text
        chunk_size: Target characters per chunk
        overlap: Characters to overlap between chunks

    Returns:
        List of text chunks
    """
    # Split by paragraphs first (double newline)
    paragraphs = re.split(r'\n\n+', content)

    chunks = []
    current_chunk = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # If adding this paragraph exceeds chunk_size, save current chunk
        if len(current_chunk) + len(para) > chunk_size and current_chunk:
            chunks.append(current_chunk)

            # Start new chunk with overlap (last N characters from previous chunk)
            if len(current_chunk) > overlap:
                current_chunk = current_chunk[-overlap:] + "\n\n" + para
            else:
                current_chunk = para
        else:
            if current_chunk:
                current_chunk += "\n\n" + para
            else:
                current_chunk = para

    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def generate_embeddings():
    """Main function to generate embeddings from book source"""

    print("=" * 80)
    print("📚 Generating Book Embeddings for ChromaDB")
    print("=" * 80)

    # Paths
    script_path = Path(__file__).parent
    tutor_agent_root = script_path.parent  # Tutor-Agent/
    book_source_root = tutor_agent_root.parent / "book-source"
    docs_path = book_source_root / "docs"
    embeddings_path = tutor_agent_root / "data" / "embeddings"

    print(f"\n📁 Paths:")
    print(f"   Book source: {docs_path}")
    print(f"   Embeddings output: {embeddings_path}")

    # Verify book source exists
    if not docs_path.exists():
        print(f"\n❌ ERROR: Book source not found at {docs_path}")
        print("   Make sure you're running this from Tutor-Agent/scripts/")
        return False

    # Create embeddings directory
    embeddings_path.mkdir(parents=True, exist_ok=True)

    # Initialize ChromaDB
    print(f"\n🔌 Initializing ChromaDB...")
    client = chromadb.PersistentClient(path=str(embeddings_path))

    # Delete existing collection if it exists
    try:
        client.delete_collection(name="book_content")
        print("   ✅ Deleted existing 'book_content' collection")
    except:
        pass

    # Create embedding function (768-dimensional)
    print(f"\n🧠 Loading embedding model (all-mpnet-base-v2)...")
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    # Create collection
    collection = client.create_collection(
        name="book_content",
        embedding_function=embedding_function,
        metadata={"description": "AI-Native Software Development book embeddings"}
    )
    print("   ✅ Created 'book_content' collection")

    # Find all markdown files
    print(f"\n📖 Scanning for markdown files...")
    md_files = list(docs_path.rglob("*.md"))
    print(f"   Found {len(md_files)} markdown files")

    # Process each file
    total_chunks = 0
    documents = []
    metadatas = []
    ids = []

    for i, md_file in enumerate(md_files, 1):
        print(f"\n📄 Processing ({i}/{len(md_files)}): {md_file.relative_to(docs_path)}")

        # Read file
        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"   ⚠️  Error reading file: {e}")
            continue

        # Extract metadata
        metadata = extract_metadata_from_path(md_file, docs_path)

        # Chunk the content
        chunks = chunk_markdown(content, chunk_size=1000, overlap=200)
        print(f"   Split into {len(chunks)} chunks")

        # Add to batch
        for chunk_idx, chunk in enumerate(chunks):
            # Create unique ID using full path and chunk index
            # This ensures uniqueness across all files
            relative_path = str(md_file.relative_to(docs_path))
            chunk_id = hashlib.md5(
                f"{relative_path}_{chunk_idx}_{total_chunks}".encode()
            ).hexdigest()

            # Add metadata for this chunk
            chunk_metadata = metadata.copy()
            chunk_metadata['chunk_index'] = chunk_idx
            chunk_metadata['total_chunks'] = len(chunks)
            chunk_metadata['source_file'] = relative_path

            documents.append(chunk)
            metadatas.append(chunk_metadata)
            ids.append(chunk_id)
            total_chunks += 1

    # Add all documents to ChromaDB in smaller batches with progress
    print(f"\n💾 Storing {total_chunks} chunks in ChromaDB...")
    print(f"   This may take 20-30 minutes (generating embeddings on CPU)...")
    print(f"   Progress will be shown every 100 chunks...\n")

    # Use smaller batches (100) to show progress more frequently
    batch_size = 100
    total_batches = (len(documents) + batch_size - 1) // batch_size

    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i:i+batch_size]
        batch_metas = metadatas[i:i+batch_size]
        batch_ids = ids[i:i+batch_size]

        batch_num = i // batch_size + 1
        percentage = (i + len(batch_docs)) / len(documents) * 100

        collection.add(
            documents=batch_docs,
            metadatas=batch_metas,
            ids=batch_ids
        )
        print(f"   ✅ Batch {batch_num}/{total_batches} ({percentage:.1f}%) - Stored {i+len(batch_docs)}/{len(documents)} chunks")

    # Verify
    count = collection.count()
    print(f"\n✅ Success!")
    print(f"   Total documents in collection: {count}")
    print(f"   Collection name: book_content")
    print(f"   Embedding dimensions: 768 (all-mpnet-base-v2)")
    print(f"   Storage location: {embeddings_path}")

    # Test a search
    print(f"\n🧪 Testing search...")
    results = collection.query(
        query_texts=["What is AI-Native Software Development?"],
        n_results=3
    )

    if results['documents'] and len(results['documents'][0]) > 0:
        print(f"   ✅ Search working! Found {len(results['documents'][0])} results")
        print(f"   Sample result: {results['documents'][0][0][:100]}...")
    else:
        print(f"   ⚠️  Search returned no results")

    print("\n" + "=" * 80)
    print("✅ Embedding generation complete!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Run: uv run python diagnose_rag.py")
    print("2. Run: uv run python test_olivia_agent.py")

    return True


if __name__ == "__main__":
    success = generate_embeddings()
    exit(0 if success else 1)
