"""
RAG (Retrieval-Augmented Generation) search tool for OLIVIA agent

This tool searches the book's ChromaDB embeddings to find relevant content
for answering user questions with accurate, contextual information.
"""

import chromadb
from agents import function_tool
from pathlib import Path
from typing import List, Dict, Optional
import os


class RAGSearchEngine:
    """
    Manages ChromaDB connection and multi-level search

    Search Levels:
    1. Page-level: Search within current page only
    2. Chapter-level: Search within current chapter
    3. Book-level: Search entire book
    """

    _instance = None

    def __init__(self):
        # Path to ChromaDB embeddings
        # __file__ is: Tutor-Agent/src/tutor_agent/services/agent/tools/rag_search.py
        # We need:     Tutor-Agent/data/embeddings
        current_file = Path(__file__)  # rag_search.py
        tutor_agent_root = current_file.parent.parent.parent.parent.parent.parent  # Go up 6 levels to Tutor-Agent/
        embeddings_path = tutor_agent_root / "data" / "embeddings"

        if not embeddings_path.exists():
            raise FileNotFoundError(
                f"ChromaDB embeddings not found at {embeddings_path}. "
                "Please run scripts/load_embeddings.py first."
            )

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=str(embeddings_path))

        # Create embedding function for 768-dimensional model (matches original embeddings)
        # The embeddings were created with a 768-dim model, likely 'all-mpnet-base-v2'
        from chromadb.utils import embedding_functions
        embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="sentence-transformers/all-mpnet-base-v2"  # 768 dimensions
        )

        # Get book content collection with correct embedding function
        try:
            self.collection = self.client.get_collection(
                name="book_content",
                embedding_function=embedding_function
            )
            print(f"✅ RAG Search Engine initialized with {self.collection.count()} embeddings")
        except Exception as e:
            raise RuntimeError(f"Failed to load book_content collection: {e}")

    @classmethod
    def get_instance(cls):
        """Get singleton instance"""
        if cls._instance is None:
            cls._instance = RAGSearchEngine()
        return cls._instance

    def search(
        self,
        query: str,
        current_page: Optional[str] = None,
        top_k: int = 3
    ) -> List[Dict]:
        """
        Multi-level RAG search

        Args:
            query: User's question or search query
            current_page: Current page path (e.g., "01-Introducing-AI-Driven-Development/01-ai-development-revolution")
            top_k: Number of results to return

        Returns:
            List of relevant content chunks with metadata:
            [
                {
                    "content": "...",
                    "page_path": "...",
                    "chunk_id": "...",
                    "distance": 0.23
                },
                ...
            ]
        """
        results = []

        # Level 1: Search current page if provided
        if current_page:
            page_results = self._search_with_filter(
                query,
                where={"page_path": {"$eq": current_page}},
                n_results=top_k
            )
            results.extend(page_results)

        # If we don't have enough results, search without filter (book-level)
        if len(results) < top_k:
            book_results = self._search_with_filter(
                query,
                where=None,
                n_results=top_k
            )

            # Add results that aren't already included
            existing_ids = {r["chunk_id"] for r in results}
            for result in book_results:
                if result["chunk_id"] not in existing_ids:
                    results.append(result)
                if len(results) >= top_k:
                    break

        return results[:top_k]

    def _search_with_filter(
        self,
        query: str,
        where: Optional[Dict] = None,
        n_results: int = 3
    ) -> List[Dict]:
        """Execute ChromaDB query with optional filter"""
        try:
            query_result = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where
            )

            # Format results
            formatted_results = []
            if query_result and query_result['documents']:
                for i, doc in enumerate(query_result['documents'][0]):
                    formatted_results.append({
                        "content": doc,
                        "page_path": query_result['metadatas'][0][i].get('page_path', 'unknown'),
                        "chunk_id": query_result['ids'][0][i],
                        "distance": query_result['distances'][0][i] if 'distances' in query_result else None
                    })

            return formatted_results

        except Exception as e:
            print(f"⚠️  RAG search error: {e}")
            return []


# ============================================================================
# Function Tool for OpenAI Agents SDK
# ============================================================================

def _search_book_content_impl(
    query: str,
    current_page: str = None
) -> str:
    """
    Implementation of book content search

    Args:
        query: The search query or question
        current_page: Current page path for context-aware search

    Returns:
        Formatted string with relevant book content and source references
    """
    # Get RAG engine instance
    try:
        engine = RAGSearchEngine.get_instance()
    except Exception as e:
        return f"⚠️ RAG search unavailable: {str(e)}"

    # Perform search
    results = engine.search(query, current_page=current_page, top_k=3)

    if not results:
        return f"No relevant content found for query: '{query}'"

    # Format results for agent
    formatted_output = []
    for i, result in enumerate(results, 1):
        source_info = f"[Source {i}: {result['page_path']}]"
        content = result['content']
        separator = "-" * 60

        formatted_output.append(f"{source_info}\n{content}\n{separator}")

    return "\n\n".join(formatted_output)


@function_tool
def search_book_content(
    query: str,
    current_page: str = None
) -> str:
    """
    Search the AI-Native Software Development book for relevant content.

    This tool performs semantic search across the book's content using embeddings
    to find the most relevant passages that can help answer questions or provide
    context.

    Args:
        query: The search query or question (e.g., "How do Python functions work?")
        current_page: Current page path for context-aware search (e.g., "04-Python-Fundamentals/03-functions")

    Returns:
        Formatted string with relevant book content and source references

    Example:
        >>> search_book_content("What is spec-driven development?")
        '''
        [From: 05-Spec-Driven-Development/01-fundamentals]
        Spec-Driven Development (SDD) is an approach where...

        [From: 05-Spec-Driven-Development/02-benefits]
        The key benefits of SDD include...
        '''
    """
    return _search_book_content_impl(query, current_page)


# ============================================================================
# Utility Functions
# ============================================================================

def test_rag_search():
    """Test function to verify RAG search is working"""
    print("🔍 Testing RAG Search Engine...\n")

    # Test query
    test_query = "What is AI-driven development?"
    print(f"Query: {test_query}\n")

    # Search (use implementation function directly for testing)
    result = _search_book_content_impl(test_query)
    print("Results:")
    print(result)
    print("\n✅ RAG Search Test Complete")


if __name__ == "__main__":
    # Run test
    test_rag_search()
