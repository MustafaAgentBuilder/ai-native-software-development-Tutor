# 🎯 RAG-Powered OLIVIA Agent - Complete Flow Diagrams

**Date**: 2025-11-15
**Purpose**: Visual flow diagrams for RAG agent architecture
**Review**: Please confirm these flows before implementation

---

## 📊 Current Embeddings Analysis

### What We Have:
```
Collection: book_content
Total Chunks: 2,026 embedded chunks
Embedding Model: 768-dimensional vectors (likely sentence-transformers)
Distance Metric: Cosine similarity

Metadata per chunk:
- file_path: Path to original markdown file
- chapter: Chapter name
- lesson: Lesson name
- heading: Section heading
- topics: Extracted keywords
- chunk_index: Position in document
- difficulty: beginner/intermediate/advanced
- content_type: text/heading/code
- chunk_size: Character count
```

### Coverage:
✅ **YES** - Embeddings cover the entire book content
✅ **YES** - Chunks are properly indexed with metadata
✅ **YES** - Searchable by chapter, lesson, topic, difficulty

### Do We Need More Embeddings?
**Answer**: **NO, current embeddings are sufficient!**

**Why**:
1. ✅ 2,026 chunks cover all book content
2. ✅ Rich metadata for precise filtering
3. ✅ Topics/keywords extracted for semantic search
4. ✅ Multiple granularities (headings, text, code)

**Future considerations** (not urgent):
- ⏳ Add embeddings for user-generated Q&A (after collecting data)
- ⏳ Add embeddings for code examples separately (optional optimization)
- ⏳ Re-embed if book content significantly updates

---

## 🔄 FLOW DIAGRAM 1: Personalized Content Generation (US2)

```
┌─────────────────────────────────────────────────────────────────────┐
│  USER REQUESTS PERSONALIZED CONTENT                                 │
│  Page: "Part 1 → Chapter 3 → Lesson 5"                             │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  FRONTEND (React)                                                   │
├─────────────────────────────────────────────────────────────────────┤
│  1. User clicks "Personalized" tab                                  │
│  2. Check: Is user logged in? (JWT in localStorage)                │
│     ├─ NO → Show Login/Signup Form                                 │
│     └─ YES → Continue                                               │
│  3. Open WebSocket connection:                                      │
│     ws://localhost:8000/ws/personalized/01-Introducing-.../05-..    │
│     ?token=eyJ0eXAiOiJKV1Qi...                                     │
│  4. Show UI: "✨ Generating your personalized content..."          │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  BACKEND - WebSocket Endpoint (/ws/personalized/{page_path})       │
├─────────────────────────────────────────────────────────────────────┤
│  1. Authenticate WebSocket (JWT from query param)                   │
│  2. Extract user_id from JWT                                        │
│  3. Parse page_path from URL                                        │
│  4. Call PersonalizedContentService.generate_streaming(...)         │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  PERSONALIZED CONTENT SERVICE                                       │
├─────────────────────────────────────────────────────────────────────┤
│  1. Check cache:                                                    │
│     ├─ EXISTS & profile matches → Stream cached content            │
│     └─ NO or profile changed → Generate new                        │
│                                                                     │
│  2. If generating new:                                              │
│     a) Get user profile (4 questions from DB)                       │
│     b) Get conversation history (last 7 messages)                   │
│     c) Build OLIVIA agent context                                   │
│     d) Call OLIVIA agent with streaming                             │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  OLIVIA AI AGENT (OpenAI Agents SDK)                                │
├─────────────────────────────────────────────────────────────────────┤
│  Agent Configuration:                                               │
│  - Name: "OLIVIA"                                                   │
│  - Instructions: Six-Step Prompting Framework (ACILPR)             │
│  - Tools: [search_book_content, get_user_profile, get_history]     │
│  - Model: gpt-4o-mini                                              │
│  - Streaming: ENABLED                                              │
│                                                                     │
│  Agent receives:                                                    │
│  - current_page_path: "01-Introducing-.../05-..."                  │
│  - user_profile: {programming: "intermediate", ai: "basic", ...}   │
│  - conversation_history: [last 7 messages]                         │
│  - task: "Generate personalized content for this page"             │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  TOOL 1: search_book_content(page_path, query)                     │
├─────────────────────────────────────────────────────────────────────┤
│  RAG Search Tool - Queries ChromaDB                                │
│                                                                     │
│  1. Parse page_path to extract:                                     │
│     - chapter: "01-Introducing-AI-Driven-Development"              │
│     - lesson: "05-beyond-code-changing-roles"                      │
│                                                                     │
│  2. Build search query:                                             │
│     - Semantic: "content about [page topic]"                        │
│     - Metadata filter: {                                            │
│         chapter: "01-Introducing-...",                              │
│         lesson: "05-beyond-code-...",                              │
│         content_type: ["text", "heading"]                           │
│       }                                                             │
│                                                                     │
│  3. Query ChromaDB:                                                 │
│     collection.query(                                               │
│       query_texts=[query],                                          │
│       where={metadata filters},                                     │
│       n_results=5  # Get top 5 most relevant chunks                │
│     )                                                               │
│                                                                     │
│  4. Return: Original page content (assembled from chunks)           │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  TOOL 2: get_user_profile(user_id)                                 │
├─────────────────────────────────────────────────────────────────────┤
│  Query database for user's 4-question profile:                     │
│  {                                                                  │
│    programming_experience: "intermediate",                          │
│    ai_experience: "basic",                                         │
│    learning_style: "practical",                                    │
│    preferred_language: "en"                                        │
│  }                                                                  │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  TOOL 3: get_conversation_history(user_id)                         │
├─────────────────────────────────────────────────────────────────────┤
│  Query ConversationMessage table:                                   │
│  - Filter: user_id = current_user                                   │
│  - Order: timestamp DESC                                            │
│  - Limit: 7 messages                                                │
│                                                                     │
│  Returns: [                                                         │
│    {role: "user", content: "...", timestamp: "..."},               │
│    {role: "assistant", content: "...", timestamp: "..."},          │
│    ...                                                              │
│  ]                                                                  │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  OLIVIA AGENT - REASONING & GENERATION                              │
├─────────────────────────────────────────────────────────────────────┤
│  Agent has all context:                                             │
│  ✅ Original page content (from RAG)                                │
│  ✅ User profile (from DB)                                          │
│  ✅ Conversation history (from DB)                                  │
│                                                                     │
│  Agent applies Six-Step Framework:                                  │
│                                                                     │
│  1. ACTOR: "You are OLIVIA, AI tutor for this student"             │
│  2. CONTEXT: Inject user profile + conversation + page info        │
│  3. INSTRUCTION: "Adapt this content to [user level]"              │
│  4. LIMITATIONS: "Keep length similar, preserve code"              │
│  5. PERSONA: Adapt tone (encouraging/challenging/technical)        │
│  6. RESPONSE FORMAT: Structured markdown                            │
│                                                                     │
│  Agent generates response using Runner.stream():                    │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STREAMING RESPONSE                                                 │
├─────────────────────────────────────────────────────────────────────┤
│  async for chunk in Runner.stream(agent, user_query):              │
│    1. Chunk received from OpenAI (SSE)                              │
│    2. Send to WebSocket: ws.send_json({"chunk": chunk})            │
│    3. Frontend appends to UI in real-time                           │
│                                                                     │
│  Result: User sees content appearing word-by-word                   │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  POST-GENERATION                                                    │
├─────────────────────────────────────────────────────────────────────┤
│  1. Save to cache (PersonalizedContent table):                      │
│     - user_id: 123                                                  │
│     - page_path: "01-Introducing-.../05-..."                       │
│     - markdown_content: [generated content]                         │
│     - profile_snapshot: {programming: "intermediate", ...}          │
│     - generated_at: [timestamp]                                     │
│                                                                     │
│  2. Save to conversation history:                                   │
│     - Add user message: "View personalized content for page X"     │
│     - Add assistant message: [generated content summary]            │
│     - Keep only last 7 messages (delete older)                      │
│                                                                     │
│  3. Send completion signal to WebSocket:                            │
│     ws.send_json({"type": "complete", "cached": false})            │
│                                                                     │
│  4. Close WebSocket connection                                      │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  FRONTEND - DISPLAY RESULT                                          │
├─────────────────────────────────────────────────────────────────────┤
│  1. Streaming complete                                              │
│  2. Hide "Generating..." message                                    │
│  3. Render final markdown content                                   │
│  4. Show action buttons (Explain, Main Points, Example, Ask Tutor) │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 FLOW DIAGRAM 2: Action Button Click (US3)

```
┌─────────────────────────────────────────────────────────────────────┐
│  USER HIGHLIGHTS TEXT & CLICKS "EXPLAIN" BUTTON                     │
│  Highlighted: "M-shaped developer"                                  │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  FRONTEND                                                           │
├─────────────────────────────────────────────────────────────────────┤
│  1. Capture highlighted text                                        │
│  2. Open WebSocket:                                                 │
│     ws://localhost:8000/ws/action?token=...                        │
│  3. Send action request:                                            │
│     {                                                               │
│       action: "explain",                                            │
│       text: "M-shaped developer",                                  │
│       page_path: "01-Introducing-.../05-m-shaped-developer",        │
│       context: [surrounding paragraph]                              │
│     }                                                               │
│  4. Show modal: "✨ OLIVIA is explaining..."                       │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  OLIVIA AGENT - ACTION MODE                                         │
├─────────────────────────────────────────────────────────────────────┤
│  Agent receives action request                                      │
│                                                                     │
│  Tools used:                                                        │
│  1. search_book_content("M-shaped developer") → Get context        │
│  2. get_user_profile(user_id) → Adapt explanation level           │
│  3. get_conversation_history(user_id) → Check prior questions     │
│                                                                     │
│  Agent applies action-specific prompt:                              │
│  - EXPLAIN: "Explain [text] in simple terms for [user level]"      │
│  - MAIN_POINTS: "List key takeaways from [text]"                   │
│  - EXAMPLE: "Provide practical example of [text]"                  │
│  - ASK_TUTOR: "Answer this question: [text]"                       │
│                                                                     │
│  Response streams to WebSocket                                      │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  FRONTEND DISPLAYS RESPONSE IN MODAL                                │
│  User sees explanation appear in real-time                          │
│  Modal closes, user continues reading                               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 FLOW DIAGRAM 3: Sidebar Chat (US4)

```
┌─────────────────────────────────────────────────────────────────────┐
│  USER OPENS SIDEBAR CHAT & ASKS QUESTION                            │
│  "What's the difference between agents and LLMs?"                   │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  FRONTEND - Sidebar Chat Component                                  │
├─────────────────────────────────────────────────────────────────────┤
│  1. Open persistent WebSocket:                                      │
│     ws://localhost:8000/ws/chat?token=...                          │
│  2. Send message:                                                   │
│     {                                                               │
│       type: "user_message",                                         │
│       content: "What's the difference between agents and LLMs?",    │
│       current_page: "01-Introducing-.../03-..."                    │
│     }                                                               │
│  3. Show typing indicator: "OLIVIA is typing..."                   │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  OLIVIA AGENT - CHAT MODE                                           │
├─────────────────────────────────────────────────────────────────────┤
│  Agent in conversational mode                                       │
│                                                                     │
│  Tools used:                                                        │
│  1. search_book_content(query="agents vs LLMs")                    │
│     → Searches ALL book content semantically                        │
│     → Returns top 5 relevant chunks                                 │
│                                                                     │
│  2. get_user_profile(user_id)                                      │
│     → Adapts answer to user's level                                │
│                                                                     │
│  3. get_conversation_history(user_id)                              │
│     → Gets last 7 messages for context                              │
│     → Enables follow-up questions                                   │
│                                                                     │
│  4. get_current_page_context(page_path)                            │
│     → Knows what page user is on                                    │
│     → Can reference current lesson                                  │
│                                                                     │
│  Agent generates conversational response                            │
│  Streams back to WebSocket                                          │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  FRONTEND - Chat UI Updates                                         │
│  - Message appears word-by-word                                     │
│  - Can cite book sections                                           │
│  - User can ask follow-up questions                                 │
│  - Conversation persists (last 7 messages)                          │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ RAG TOOL ARCHITECTURE

### Tool: search_book_content()

```python
@tool_decorator
def search_book_content(
    page_path: Optional[str] = None,
    query: Optional[str] = None,
    search_scope: str = "page"  # "page" | "chapter" | "book"
) -> str:
    """
    Search book content using RAG (ChromaDB)

    Args:
        page_path: Specific page to search (e.g., "01-Introducing-.../05-...")
        query: Semantic search query
        search_scope: How broad to search
            - "page": Only current page (DEFAULT for personalized content)
            - "chapter": Current chapter
            - "book": Entire book (for chat questions)

    Returns:
        Relevant content chunks assembled into markdown

    Examples:
        # Get specific page content
        search_book_content(
            page_path="01-Introducing-.../05-...",
            search_scope="page"
        )

        # Semantic search across chapter
        search_book_content(
            query="What are agents?",
            page_path="01-Introducing-...",  # Infer chapter
            search_scope="chapter"
        )

        # Search entire book (chat mode)
        search_book_content(
            query="How to deploy with Docker?",
            search_scope="book"
        )
    """

    # Parse page_path to extract chapter/lesson
    metadata_filter = build_filter(page_path, search_scope)

    # Query ChromaDB
    results = chromadb_collection.query(
        query_texts=[query] if query else None,
        where=metadata_filter,
        n_results=5 if search_scope == "page" else 10
    )

    # Assemble chunks into coherent content
    content = assemble_chunks(results)

    return content
```

---

## 📊 METADATA FILTERING STRATEGY

### Scenario 1: Personalized Content (Specific Page)
```python
page_path = "01-Introducing-AI-Driven-Development/05-m-shaped-developer"

filter = {
    "chapter": "01-Introducing-AI-Driven-Development",
    "lesson": "05-m-shaped-developer",
    "content_type": {"$in": ["text", "heading"]}  # Exclude code blocks
}

# Returns: ONLY content from that specific lesson page
```

### Scenario 2: Action Button "Explain" (Context Search)
```python
highlighted_text = "M-shaped developer"

# Semantic search with light filtering
results = collection.query(
    query_texts=[highlighted_text],
    where={"content_type": {"$in": ["text", "heading"]}},
    n_results=3
)

# Returns: Most relevant chunks explaining the term
```

### Scenario 3: Chat Question (Broad Search)
```python
question = "How do I deploy FastAPI?"

# Search entire book semantically
results = collection.query(
    query_texts=[question],
    where={"topics": {"$contains": "deployment"}},  # Optional topic filter
    n_results=10
)

# Returns: All relevant deployment content across book
```

---

## ✅ EMBEDDING SUFFICIENCY CHECKLIST

| Requirement | Current Status | Notes |
|-------------|----------------|-------|
| **Book Content Coverage** | ✅ COMPLETE | 2,026 chunks cover all content |
| **Metadata Richness** | ✅ EXCELLENT | chapter, lesson, topics, difficulty, etc. |
| **Granularity** | ✅ GOOD | Headings, text, code separated |
| **Search Performance** | ✅ READY | Cosine similarity with 768-dim vectors |
| **Page-Specific Retrieval** | ✅ POSSIBLE | chapter + lesson metadata |
| **Semantic Search** | ✅ ENABLED | Query by meaning, not just keywords |
| **Topic Filtering** | ✅ AVAILABLE | Extracted keywords per chunk |

**Conclusion**: **Current embeddings are SUFFICIENT. No new embeddings needed for MVP!**

---

## 🎯 NEXT STEPS (Confirm These Flows)

### If you approve these flows, we'll implement:

1. ✅ **RAG Service** (`services/rag_service.py`)
   - Connects to ChromaDB
   - Implements search_book_content tool
   - Handles metadata filtering

2. ✅ **OLIVIA Agent** (`services/agent/olivia_agent.py`)
   - Uses OpenAI Agents SDK
   - Has 3 tools: RAG search, user profile, conversation history
   - Implements Six-Step prompting

3. ✅ **WebSocket Endpoints** (`api/v1/websocket.py`)
   - `/ws/personalized/{page_path}` - Personalized content streaming
   - `/ws/action` - Action button responses
   - `/ws/chat` - Sidebar chat

4. ✅ **Conversation Memory** (`models/conversation.py` + `services/conversation_service.py`)
   - Store messages in DB
   - Retrieve last 7 per user
   - Auto-cleanup old messages

5. ✅ **Streaming Handler** (`services/agent/streaming.py`)
   - Receives chunks from OpenAI
   - Sends to WebSocket
   - Handles errors/disconnections

---

## 🤔 PLEASE CONFIRM

**Before I start coding, please review these flows and confirm**:

1. ✅ **RAG search strategy** - Page-specific vs semantic search approach
2. ✅ **WebSocket streaming** - Used for all 3 scenarios (personalized, actions, chat)
3. ✅ **No new embeddings needed** - 2,026 chunks are sufficient
4. ✅ **Tool architecture** - search_book_content with flexible scope parameter
5. ✅ **Conversation memory** - Last 7 messages stored in DB

**If anything needs correction, please guide me. Otherwise, I'll proceed with implementation!** 🚀
