#!/usr/bin/env python3
"""Diagnose RAG search engine and ChromaDB connection"""
import sys
from pathlib import Path

print("=" * 80)
print("🔍 RAG Search Engine Diagnostic")
print("=" * 80)

# Check 1: ChromaDB embeddings directory
print("\n📁 Step 1: Checking ChromaDB embeddings directory...")
current_file = Path(__file__)
tutor_agent_root = current_file.parent
embeddings_path = tutor_agent_root / "data" / "embeddings"

print(f"   Current file: {current_file}")
print(f"   Tutor-Agent root: {tutor_agent_root}")
print(f"   Expected embeddings path: {embeddings_path}")
print(f"   Exists: {embeddings_path.exists()}")

if not embeddings_path.exists():
    print("\n❌ ERROR: ChromaDB embeddings directory not found!")
    print("   This is why RAG search doesn't work.")
    print("\n🔧 FIX: You need to generate the embeddings first.")
    print("   The embeddings should be at: Tutor-Agent/data/embeddings/")
    print("\n   Looking for alternative locations...")

    # Check if embeddings exist elsewhere
    alternative_paths = [
        tutor_agent_root.parent / "data" / "embeddings",  # One level up
        tutor_agent_root.parent / "book-source" / "data" / "embeddings",
        Path("P:/Book Agent/ai-native-software-development-Tutor/data/embeddings"),
    ]

    for alt_path in alternative_paths:
        if alt_path.exists():
            print(f"   ✅ Found embeddings at: {alt_path}")
            print(f"      Files: {list(alt_path.glob('*'))[:5]}")

    sys.exit(1)

print(f"   ✅ Directory exists!")
print(f"   Files in directory: {list(embeddings_path.glob('*'))[:10]}")

# Check 2: Try to connect to ChromaDB
print("\n🔌 Step 2: Connecting to ChromaDB...")
try:
    import chromadb
    client = chromadb.PersistentClient(path=str(embeddings_path))
    print("   ✅ ChromaDB connected successfully!")

    # List collections
    collections = client.list_collections()
    print(f"\n   📚 Collections found: {len(collections)}")
    for col in collections:
        print(f"      - {col.name}: {col.count()} documents")

    if len(collections) == 0:
        print("\n   ❌ ERROR: No collections found in ChromaDB!")
        print("      The embeddings directory exists but is empty.")

except Exception as e:
    print(f"   ❌ ERROR connecting to ChromaDB: {e}")
    sys.exit(1)

# Check 3: Try to initialize RAGSearchEngine
print("\n🔧 Step 3: Initializing RAG Search Engine...")
try:
    from tutor_agent.services.agent.tools.rag_search import RAGSearchEngine

    rag = RAGSearchEngine()
    print("   ✅ RAG Search Engine initialized!")
    print(f"   Collection: {rag.collection.name}")
    print(f"   Document count: {rag.collection.count()}")

except Exception as e:
    print(f"   ❌ ERROR initializing RAG Search Engine: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Check 4: Try a simple search using RAG directly
print("\n🔍 Step 4: Testing RAG search...")
try:
    # Test search using the RAG search engine directly
    query = "What is AI-Native Software Development?"
    results = rag._search_with_filter(query, where=None, n_results=3)

    if results and len(results) > 0:
        print("   ✅ RAG search executed successfully!")
        print(f"   Found {len(results)} results")
        print(f"   First result preview: {results[0]['content'][:200]}...")
        print(f"   Metadata: {results[0].get('metadata', {})}")
    else:
        print("   ⚠️  Search returned no results")

except Exception as e:
    print(f"   ❌ ERROR executing RAG search: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Check 5: Verify tool is registered with agent
print("\n🤖 Step 5: Checking if tool is registered with OLIVIA agent...")
try:
    from tutor_agent.services.agent.olivia_agent import OLIVIAAgent

    olivia = OLIVIAAgent()
    tools = olivia.tools

    print(f"   ✅ OLIVIA has {len(tools)} tools registered:")
    for tool in tools:
        print(f"      - {tool.name}: {tool.description[:60]}...")

    # Check if search_book_content is in the list
    tool_names = [t.name for t in tools]
    if "search_book_content" in tool_names:
        print("\n   ✅ search_book_content tool is registered!")
    else:
        print("\n   ❌ ERROR: search_book_content tool NOT found in agent tools!")

except Exception as e:
    print(f"   ❌ ERROR checking agent tools: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("✅ Diagnostic complete!")
print("=" * 80)
