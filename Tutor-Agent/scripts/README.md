# Tutor-Agent Scripts

This directory contains utility scripts for setting up and managing the OLIVIA agent.

## generate_embeddings.py

Generates ChromaDB embeddings from the book markdown files.

### What it does:

1. Reads all markdown files from `book-source/docs/`
2. Splits them into 1000-character chunks with 200-character overlap
3. Generates 768-dimensional embeddings using `sentence-transformers/all-mpnet-base-v2`
4. Stores embeddings in `Tutor-Agent/data/embeddings/` ChromaDB

### Usage:

```bash
cd Tutor-Agent
uv run python scripts/generate_embeddings.py
```

### First time setup:

The script will automatically:
- Download the embedding model (sentence-transformers/all-mpnet-base-v2)
- Create the ChromaDB collection named "book_content"
- Process all markdown files and generate embeddings

**Time:** Takes 5-10 minutes depending on your hardware (CPU for embeddings, disk I/O for ChromaDB).

### Output:

```
📚 Generating Book Embeddings for ChromaDB
📁 Paths:
   Book source: .../book-source/docs
   Embeddings output: .../Tutor-Agent/data/embeddings

🔌 Initializing ChromaDB...
   ✅ Created 'book_content' collection

📖 Scanning for markdown files...
   Found 42 markdown files

📄 Processing (1/42): preface-agent-native.md
   Split into 25 chunks

💾 Storing 847 chunks in ChromaDB...
   ✅ Stored batch 1 (847 chunks)

✅ Success!
   Total documents in collection: 847
   Collection name: book_content
   Embedding dimensions: 768
```

### After running:

Verify embeddings work:
```bash
uv run python diagnose_rag.py
uv run python test_olivia_agent.py
```

### Troubleshooting:

**Error: "Book source not found"**
- Make sure you're in the `Tutor-Agent` directory when running the script
- Verify `book-source/docs/` exists with markdown files

**Error: "Collection already exists"**
- The script automatically deletes and recreates the collection
- If it fails, manually delete: `rm -rf data/embeddings/*` and run again

**Error: "Out of memory"**
- The script processes in batches of 5000 chunks
- If still failing, reduce `chunk_size` in the script from 1000 to 500
