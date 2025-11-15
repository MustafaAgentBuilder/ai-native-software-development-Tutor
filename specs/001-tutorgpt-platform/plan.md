# Implementation Plan: TutorGPT - AI-Powered Book Learning Platform

**Branch**: `001-tutorgpt-platform` | **Date**: 2025-11-14 | **Last Updated**: 2025-11-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-tutorgpt-platform/spec.md`

**Note**: This plan defines HOW we'll build TutorGPT following Test-Driven Development and Agent-First Architecture principles.

**🔴 CRITICAL ARCHITECTURE UPDATE (2025-11-15)**:
- **Backend Architecture Changed**: Simple OpenAI API → RAG-Powered OLIVIA AI Agent
- **Required**: OpenAI Agents SDK (NOT `openai.chat.completions.create()`)
- **Required**: ChromaDB RAG with 2,026 pre-computed embeddings
- **Required**: WebSocket streaming for all agent responses
- **Required**: Conversation memory (last 7 messages per user)
- **Embeddings Location**: `Tutor-Agent/data/embeddings/` (19MB, already copied)
- **See**: `ARCHITECTURE_UPDATE.md` and `TASKS_UPDATE.md` for complete details

## Summary

TutorGPT transforms the "AI Native Software Development" book (Part 1) into an intelligent, personalized learning platform. The system provides three content views: Original (book content), Summary (pre-generated, public), and Personalized (user-specific, login required). An AI agent powered by OpenAI Agents SDK provides context-aware tutoring through four action buttons (Explain, Main Points, Example, Ask Tutor) and real-time WebSocket chat. The agent adapts responses based on user profile (programming experience, AI experience, learning style, preferred language) and learning journey (current page, completed chapters, concepts mastered/struggling). RAG (Retrieval-Augmented Generation) with pre-computed embeddings ensures factually accurate, context-rich responses within performance targets (<200ms summaries, <4s chat, <3s actions).

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, ChromaDB, WebSockets, Pydantic
**Storage**: PostgreSQL (user data, profiles, sessions), ChromaDB (book embeddings), Filesystem (generated summaries)
**Testing**: pytest with pytest-asyncio, pytest-cov (90%+ coverage mandate)
**Target Platform**: Linux/Windows server (backend), Web browser (frontend via enhanced Docusaurus)
**Project Type**: Web application (backend API + enhanced static site frontend)
**Performance Goals**: Summary <200ms, Personalized <5s (first)/<500ms (cached), Chat <4s, Actions <3s, WebSocket connect <1s
**Constraints**: Part 1 only (4 chapters), 100+ concurrent users support, Test coverage ≥90%, All features TDD-developed
**Scale/Scope**: ~107 lessons, 2,026 embedding chunks (19MB), 4 user profile dimensions, real-time bi-directional communication

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles Compliance

| Principle | Requirement | Plan Alignment | Status |
|-----------|-------------|----------------|--------|
| **I. Learner-First Always** | User experience over technical complexity | ✅ Three-tab interface prioritizes ease of use; performance targets ensure flow state | **PASS** |
| **II. TDD Mandatory** | 90%+ coverage, Red-Green-Refactor cycle | ✅ pytest-asyncio setup; TDD workflow for all components; coverage enforcement in CI/CD | **PASS** |
| **III. Agent-First Architecture** | AI capabilities drive architecture | ✅ OpenAI Agents SDK central; context-aware responses; RAG integration; specialized prompts per action type | **PASS** |
| **IV. Personalization Without Burden** | Minimal signup (4 questions), behavioral learning | ✅ Exactly 4 signup questions; learning journey tracking; adaptive responses based on behavior | **PASS** |
| **V. Real-Time by Default** | WebSocket foundation, streaming responses | ✅ WebSocket chat with streaming; live status; instant action button feedback | **PASS** |
| **VI. Performance as Feature** | <200ms summaries, <4s chat, 100+ concurrent users | ✅ Pre-generated summaries for instant load; caching strategies; connection pooling; load testing | **PASS** |
| **VII. Content Integrity** | Accuracy preservation, technical correctness | ✅ RAG with source attribution; 95% language accuracy target; fact validation against book content | **PASS** |
| **VIII. Privacy & Transparency** | User control, consent, data deletion | ✅ Clear consent for personalization; account deletion capability; secure JWT auth | **PASS** |

### Technology Stack Compliance

| Constitution Mandate | Plan Implementation | Status |
|---------------------|---------------------|--------|
| Python 3.11+ | ✅ Python 3.11+ specified | **PASS** |
| OpenAI Agents SDK | ✅ Core agent implementation uses OpenAI Agents SDK | **PASS** |
| FastAPI with async/await | ✅ FastAPI for all API endpoints with async handlers | **PASS** |
| WebSockets for real-time | ✅ WebSocket endpoints for chat and actions | **PASS** |
| pytest with async, 90%+ coverage | ✅ pytest-asyncio, pytest-cov with 90% threshold | **PASS** |
| UV package management | ✅ UV for dependency management (already in Tutor-Agent) | **PASS** |

### Architecture Pattern Compliance

| Pattern | Constitution Requirement | Plan Implementation | Status |
|---------|-------------------------|---------------------|--------|
| Agent Pattern | Orchestrator + Specialist agents | ✅ UniversalTutorAgent + specialized prompts for Explain/MainPoints/Example/AskTutor | **PASS** |
| Communication | WebSocket-first with RESTful fallback | ✅ WebSocket primary for chat/actions; REST for auth/content | **PASS** |
| State Management | Context-aware with memory persistence | ✅ User profile + learning journey in DB; conversation history; page context tracking | **PASS** |
| Error Handling | Graceful degradation with helpful messages | ✅ WebSocket reconnection; error boundaries; fallback to cached content | **PASS** |

### Quality Gates

✅ **All constitution checks PASSED** - Ready to proceed with Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/001-tutorgpt-platform/
├── spec.md              # Feature specification (WHAT) - ✅ Complete
├── plan.md              # Implementation plan (HOW) - 🔄 This file
├── checklists/
│   └── requirements.md  # Spec validation checklist - ✅ Complete
├── research.md          # Phase 0: Technology decisions & patterns (to be created)
├── data-model.md        # Phase 1: Database schema & entities (to be created)
├── quickstart.md        # Phase 1: Developer onboarding guide (to be created)
├── contracts/           # Phase 1: API contracts (OpenAPI specs) (to be created)
└── tasks.md             # Phase 2: Generated by /sp.tasks command (NOT in this command)
```

### Source Code (repository root)

**Structure Decision**: Web application architecture with separate backend (FastAPI) and frontend (enhanced Docusaurus). This aligns with:
- Constitution requirement for FastAPI backend
- Existing book-source with Docusaurus
- Need for real-time WebSocket server (backend)
- Need for enhanced static site with React components (frontend)

```text
Tutor-Agent/                                    # Backend API (already initialized)
├── src/
│   └── tutor_agent/
│       ├── __init__.py
│       ├── main.py                            # FastAPI application entry point
│       ├── config/                            # ✅ Already created
│       │   ├── __init__.py
│       │   └── settings.py                    # Pydantic settings with .env
│       ├── models/                            # Database models (SQLAlchemy)
│       │   ├── __init__.py
│       │   ├── user.py                        # User + UserProfile models
│       │   ├── chat.py                        # ChatSession + ChatMessage models
│       │   └── content.py                     # GeneratedContent + PageContent models
│       ├── api/                               # API endpoints
│       │   ├── __init__.py
│       │   ├── v1/
│       │   │   ├── __init__.py
│       │   │   ├── auth.py                    # POST /auth/signup, /auth/login, /auth/refresh
│       │   │   ├── profile.py                 # GET/PUT /profile, GET /profile/journey
│       │   │   ├── content.py                 # GET /content/summary, /content/personalized
│       │   │   └── websocket.py               # WS /ws/chat, /ws/actions
│       │   └── deps.py                        # Dependency injection (get_db, get_current_user)
│       ├── services/                          # Business logic
│       │   ├── __init__.py
│       │   ├── agent/                         # AI agent implementation
│       │   │   ├── __init__.py
│       │   │   ├── universal_tutor.py         # UniversalTutorAgent class
│       │   │   ├── context_builder.py         # Build agent context from user/page/history
│       │   │   ├── prompts.py                 # Specialized prompts for each action type
│       │   │   └── response_formatter.py      # Format agent responses for different channels
│       │   ├── rag/                           # Retrieval-Augmented Generation
│       │   │   ├── __init__.py
│       │   │   ├── embeddings.py              # Load ChromaDB, search embeddings
│       │   │   └── retriever.py               # Multi-level retrieval (page/chapter/book)
│       │   ├── content_generator.py           # Summary & personalized content generation
│       │   ├── personalizer.py                # Adapt content based on user profile
│       │   ├── auth_service.py                # JWT token management, password hashing
│       │   └── learning_tracker.py            # Track user learning journey & behavior
│       ├── core/                              # Core utilities
│       │   ├── __init__.py
│       │   ├── database.py                    # SQLAlchemy engine, session factory
│       │   ├── security.py                    # JWT utilities, password hashing
│       │   ├── websocket_manager.py           # WebSocket connection management
│       │   └── cache.py                       # Caching utilities (Redis or in-memory)
│       └── utils/                             # Helper utilities
│           ├── __init__.py
│           ├── logging.py                     # Structured logging setup
│           └── exceptions.py                  # Custom exception classes
├── tests/                                     # Test suite (TDD - Red-Green-Refactor)
│   ├── __init__.py
│   ├── conftest.py                            # pytest fixtures
│   ├── unit/                                  # Unit tests (90%+ coverage target)
│   │   ├── test_models.py                     # Database model tests
│   │   ├── test_agent.py                      # Agent behavior tests
│   │   ├── test_rag.py                        # RAG retrieval tests
│   │   └── test_services.py                   # Service layer tests
│   ├── integration/                           # Integration tests
│   │   ├── test_api_auth.py                   # Authentication flow tests
│   │   ├── test_api_content.py                # Content generation tests
│   │   ├── test_websocket.py                  # WebSocket communication tests
│   │   └── test_agent_integration.py          # Agent + RAG + DB integration
│   └── e2e/                                   # End-to-end tests
│       ├── test_user_journey.py               # Complete user flow tests
│       └── test_performance.py                # Performance benchmark tests
├── scripts/                                   # Deployment & utility scripts
│   ├── generate_summaries.py                  # Pre-generate summaries for all Part 1 pages
│   ├── init_db.py                             # Database initialization
│   └── load_embeddings.py                     # Load ChromaDB from external path
├── data/                                      # Data files
│   ├── embeddings/                            # Symlink to embeddings (from external Tutor project)
│   └── generated_summaries/                   # Pre-generated summary cache
├── pyproject.toml                             # ✅ Already created (UV dependencies)
├── .env.example                               # ✅ Already created
├── .env                                       # Environment variables (gitignored)
└── README.md                                  # Project documentation

book-source/                                   # Frontend (Docusaurus - already exists)
├── docs/                                      # Original book content (Part 1-4)
│   ├── 01-Introducing-AI-Driven-Development/
│   ├── 02-AI-Tool-Landscape/
│   ├── 03-Markdown-Prompt-Context-Engineering/
│   └── 04-Python-Fundamentals/
├── src/
│   ├── components/                            # Custom React components
│   │   ├── TabSystem/                         # Three-tab interface
│   │   │   ├── TabContainer.tsx               # Tab switching logic
│   │   │   ├── OriginalTab.tsx                # Original book content display
│   │   │   ├── SummaryTab.tsx                 # Pre-generated summary display
│   │   │   └── PersonalizedTab.tsx            # Personalized content (login required)
│   │   ├── ActionButtons/                     # Four action buttons
│   │   │   ├── ActionButtonGroup.tsx          # Button group container
│   │   │   ├── ExplainButton.tsx              # Explain action
│   │   │   ├── MainPointsButton.tsx           # Main Points action
│   │   │   ├── ExampleButton.tsx              # Example action
│   │   │   └── AskTutorButton.tsx             # Ask Tutor action (opens chat)
│   │   ├── Chat/                              # Real-time chat interface
│   │   │   ├── ChatSidebar.tsx                # Collapsible chat sidebar
│   │   │   ├── MessageList.tsx                # Chat message display with streaming
│   │   │   ├── MessageInput.tsx               # Chat input with send button
│   │   │   └── TypingIndicator.tsx            # Agent typing indicator
│   │   ├── Auth/                              # Authentication UI
│   │   │   ├── LoginForm.tsx                  # Login form
│   │   │   ├── SignupForm.tsx                 # Signup with 4 personalization questions
│   │   │   └── AuthModal.tsx                  # Modal wrapper for auth forms
│   │   └── Profile/                           # User profile management
│   │       ├── ProfileView.tsx                # Display user profile
│   │       └── ProfileEdit.tsx                # Edit profile settings
│   ├── hooks/                                 # Custom React hooks
│   │   ├── useAuth.ts                         # Authentication state & actions
│   │   ├── useWebSocket.ts                    # WebSocket connection management
│   │   ├── useContent.ts                      # Content loading & caching
│   │   └── useLearningJourney.ts              # Learning progress tracking
│   ├── services/                              # Frontend services
│   │   ├── api.ts                             # REST API client (fetch wrapper)
│   │   ├── websocket.ts                       # WebSocket client
│   │   └── storage.ts                         # LocalStorage utilities
│   ├── types/                                 # TypeScript type definitions
│   │   ├── user.ts                            # User & UserProfile types
│   │   ├── content.ts                         # Content types
│   │   └── chat.ts                            # Chat message types
│   └── styles/                                # Custom styles
│       ├── components.module.css              # Component-specific styles
│       └── chat.module.css                    # Chat interface styles
├── docusaurus.config.js                       # Docusaurus configuration
├── sidebars.js                                # Sidebar navigation
└── package.json                               # Frontend dependencies
```

### External Dependencies (Pre-existing)

```text
P:\Ai native Book\ai-native-software-development\Tutor\
├── backend/
│   └── data/
│       └── embeddings/                        # Pre-computed ChromaDB embeddings
│           ├── chroma.sqlite3                 # 19MB database
│           └── d69c732b-0a21-4f5b-a437-47cea526907e/  # Vector index
└── EMBEDDINGS_GUIDE.md                        # Guide for reusing embeddings
```

**Integration Strategy**:
- Symlink or copy `P:\Ai native Book\...\Tutor\backend\data\embeddings` to `Tutor-Agent/data/embeddings`
- Load ChromaDB with `PersistentClient(path="./data/embeddings")`
- Collection name: `book_content` (2,026 chunks from 107 lessons)

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations detected.** All constitution checks passed. Architecture follows minimal complexity principles:
- Single backend project (Tutor-Agent)
- Direct SQLAlchemy models (no repository pattern needed at this scale)
- Single UniversalTutorAgent (no complex orchestration needed)
- Simple caching strategy (no distributed cache required for MVP)

---

## Phase 0: Research & Technology Decisions

**Goal**: Resolve all technical unknowns and document technology choices with rationale.

### Research Areas

1. **Agent Context Management**
   - **Question**: How to efficiently build agent context from user profile + page + history?
   - **Research**: OpenAI Agents SDK context injection patterns
   - **Decision point**: Context window management for 2,026 embedding chunks

2. **WebSocket Scaling**
   - **Question**: How to handle 100+ concurrent WebSocket connections efficiently?
   - **Research**: FastAPI WebSocket connection pooling, async patterns
   - **Decision point**: In-memory vs Redis for connection state

3. **Summary Pre-Generation**
   - **Question**: Best approach to generate and cache 107 summaries before deployment?
   - **Research**: Build-time generation vs deployment script
   - **Decision point**: Storage format (markdown files vs database vs JSON)

4. **Personalized Content Caching**
   - **Question**: Cache strategy for user-specific personalized content?
   - **Research**: Cache invalidation, TTL strategies, memory vs disk
   - **Decision point**: LRU cache size, per-user vs per-page caching

5. **Embeddings Integration**
   - **Question**: How to integrate pre-computed embeddings from external project?
   - **Research**: Symlink vs copy, collection access patterns
   - **Decision point**: Embedding search performance optimization

6. **Multi-Language Support**
   - **Question**: How to preserve technical terms in Urdu/Spanish/Hindi translations?
   - **Research**: LLM translation with technical term preservation prompts
   - **Decision point**: Pre-translate vs on-demand translation

**Output**: `research.md` documenting all decisions with rationale and alternatives considered.

---

## Phase 1: Data Model & API Contracts

**Goal**: Design database schema and API contracts from functional requirements.

### Data Model Design

Extract entities from spec and design relationships:

| Entity | Source | Key Attributes |
|--------|--------|----------------|
| User | FR-011 to FR-016 | email (unique), password_hash, full_name, created_at, last_login |
| UserProfile | FR-017 to FR-023 | user_id (FK), programming_experience, ai_experience, learning_style, preferred_language |
| LearningJourney | FR-024 to FR-030 | profile_id (FK), current_page_path, completed_chapters[], time_on_page_seconds, concepts_mastered[], concepts_struggling[] |
| ChatSession | FR-031 to FR-037 | user_id (FK), session_id (UUID), page_context_path, started_at, ended_at, is_active |
| ChatMessage | FR-038 to FR-044 | session_id (FK), role (user/assistant), content, message_type, rag_sources[], response_time_ms, created_at |
| GeneratedContent | FR-007 to FR-010 | content_id (UUID), user_id (FK, nullable for summaries), page_path, content_type (summary/personalized), markdown_content, generated_at, cached_until |
| PageContent | Implicit | page_path (PK), chapter, part, lesson_title, markdown_content, embedding_chunk_ids[] |

**Output**: `data-model.md` with ERD and detailed field descriptions.

### API Contracts

Generate OpenAPI specs from functional requirements:

**Authentication Endpoints** (from FR-011 to FR-016):
- `POST /api/v1/auth/signup` - Register with 4 personalization questions
- `POST /api/v1/auth/login` - Login with email/password
- `POST /api/v1/auth/refresh` - Refresh JWT token
- `POST /api/v1/auth/logout` - Logout (invalidate token)

**Profile Endpoints** (from FR-017 to FR-030):
- `GET /api/v1/profile` - Get current user profile
- `PUT /api/v1/profile` - Update profile settings
- `GET /api/v1/profile/journey` - Get learning journey data

**Content Endpoints** (from FR-001 to FR-010):
- `GET /api/v1/content/summary/{page_path}` - Get pre-generated summary (public)
- `GET /api/v1/content/personalized/{page_path}` - Get personalized content (auth required)

**WebSocket Endpoints** (from FR-031 to FR-055):
- `WS /api/v1/ws/chat` - Real-time chat with agent
- `WS /api/v1/ws/actions` - Action button responses (Explain/MainPoints/Example/AskTutor)

**Output**: `contracts/openapi.yaml` with complete API specification.

### Developer Quickstart

**Output**: `quickstart.md` with:
- Environment setup (UV, Python 3.11+, PostgreSQL)
- Database initialization
- Running tests
- Starting development server
- Frontend setup (Node.js, Docusaurus)

---

## Phase 2: Detailed Implementation Planning

*Note: This phase is executed by `/sp.plan`. Task generation happens with `/sp.tasks` command.*

### Architecture Decisions

#### 1. Agent Implementation (OpenAI Agents SDK)

**Decision**: Use OpenAI Agents SDK with specialized prompt templates per action type.

**Rationale**:
- Constitution mandates OpenAI Agents SDK
- SDK provides context management out-of-the-box
- Supports function calling for RAG integration
- Streaming responses for chat

**Implementation Pattern**:
```python
class UniversalTutorAgent:
    def __init__(self, openai_client, embeddings_retriever):
        self.client = openai_client
        self.retriever = embeddings_retriever
        self.prompts = PromptTemplates()  # Specialized prompts

    async def respond_to_action(
        self,
        action_type: ActionType,  # EXPLAIN | MAIN_POINTS | EXAMPLE | ASK_TUTOR
        user_profile: UserProfile,
        page_context: PageContent,
        chat_history: List[ChatMessage]
    ) -> AgentResponse:
        # 1. Build context from user profile + page + history
        context = self.build_context(user_profile, page_context, chat_history)

        # 2. Retrieve relevant embeddings via RAG
        rag_results = await self.retriever.search(
            query=self.prompts.get_rag_query(action_type, page_context),
            top_k=3
        )

        # 3. Select specialized prompt for action type
        prompt = self.prompts.get_action_prompt(
            action_type=action_type,
            context=context,
            rag_sources=rag_results,
            user_profile=user_profile  # For personalization
        )

        # 4. Stream response from agent
        async for chunk in self.client.stream_completion(prompt):
            yield chunk
```

**Agent Context Structure** (inspired by your examples):
```python
{
    "student_name": user.full_name,
    "current_page": "/docs/03-git/02-branching.md",
    "progress": {
        "completed_chapters": ["Chapter 1", "Chapter 2"],
        "time_on_current_page": 300,  # seconds
        "concepts_mastered": ["git add", "git commit"],
        "concepts_struggling": ["git merge"]
    },
    "profile": {
        "programming_experience": "beginner",
        "ai_experience": "no_experience",
        "learning_style": "visual",
        "preferred_language": "en"
    },
    "behavior": {
        "scrolls": 3,
        "highlights": ["def keyword"],
        "questions_asked": 2
    }
}
```

#### 2. RAG Implementation (ChromaDB)

**Decision**: Use pre-computed ChromaDB embeddings with multi-level retrieval.

**Rationale**:
- Embeddings already exist (2,026 chunks, 19MB)
- ChromaDB HNSW index provides fast search (<100ms)
- Multi-level retrieval (page → chapter → book) improves context relevance

**Implementation Pattern**:
```python
class EmbeddingsRetriever:
    def __init__(self, chromadb_path: str):
        self.client = chromadb.PersistentClient(path=chromadb_path)
        self.collection = self.client.get_collection(name="book_content")

    async def search(
        self,
        query: str,
        current_page: str,
        top_k: int = 5
    ) -> List[RAGResult]:
        # Level 1: Search current page only
        page_results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
            where={"page_path": current_page}
        )

        # Level 2: If insufficient results, search current chapter
        if len(page_results['documents'][0]) < 3:
            chapter = self.extract_chapter(current_page)
            chapter_results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
                where={"chapter": chapter}
            )
            page_results = self.merge_results(page_results, chapter_results)

        # Level 3: If still insufficient, search entire book
        if len(page_results['documents'][0]) < 3:
            book_results = self.collection.query(
                query_texts=[query],
                n_results=top_k
            )
            page_results = self.merge_results(page_results, book_results)

        return self.format_results(page_results)
```

#### 3. WebSocket Architecture

**Decision**: FastAPI WebSocket with connection manager pattern.

**Rationale**:
- FastAPI has built-in WebSocket support
- Connection manager tracks active connections per user
- Enables server-side message broadcasting
- Handles reconnection gracefully

**Implementation Pattern**:
```python
class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    async def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_message(self, user_id: str, message: dict):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(message)

    async def stream_response(self, user_id: str, agent_response_stream):
        """Stream agent response chunks to user"""
        async for chunk in agent_response_stream:
            await self.send_message(user_id, {
                "type": "chunk",
                "content": chunk,
                "timestamp": datetime.utcnow().isoformat()
            })

        # Send final message indicating completion
        await self.send_message(user_id, {"type": "complete"})
```

#### 4. Content Caching Strategy

**Decision**: Two-tier caching - Filesystem for summaries, In-memory LRU for personalized content.

**Rationale**:
- Summaries are static (same for all users) → disk cache
- Personalized content varies per user → memory cache with TTL
- Avoid database queries for frequently accessed content

**Implementation Pattern**:
```python
class ContentCache:
    def __init__(self, summary_dir: Path, cache_size: int = 1000):
        self.summary_dir = summary_dir
        self.personalized_cache = LRU(max_size=cache_size)  # In-memory

    async def get_summary(self, page_path: str) -> Optional[str]:
        """Get pre-generated summary from filesystem"""
        cache_file = self.summary_dir / f"{page_path.replace('/', '_')}.md"
        if cache_file.exists():
            return cache_file.read_text()
        return None

    async def get_personalized(
        self,
        page_path: str,
        user_id: str
    ) -> Optional[str]:
        """Get personalized content from in-memory cache"""
        cache_key = f"{user_id}:{page_path}"
        return self.personalized_cache.get(cache_key)

    async def set_personalized(
        self,
        page_path: str,
        user_id: str,
        content: str,
        ttl_seconds: int = 3600  # 1 hour
    ):
        """Cache personalized content with TTL"""
        cache_key = f"{user_id}:{page_path}"
        self.personalized_cache.set(cache_key, content, ttl=ttl_seconds)
```

#### 5. Personalization Engine

**Decision**: Template-based personalization with LLM rewriting.

**Rationale**:
- User profile dimensions map to specific prompt adjustments
- Programming experience → complexity level
- Learning style → presentation format (visual/hands-on/theoretical)
- Preferred language → translation with technical term preservation
- AI experience → jargon usage

**Implementation Pattern** (inspired by your context examples):
```python
class Personalizer:
    def __init__(self, llm_client):
        self.client = llm_client

    async def personalize_content(
        self,
        original_content: str,
        user_profile: UserProfile,
        page_context: PageContent
    ) -> str:
        # Build personalization instructions
        instructions = []

        # Programming experience adaptation
        if user_profile.programming_experience == "beginner":
            instructions.append(
                "Use simple analogies and step-by-step explanations. "
                "Relate new concepts to everyday experiences."
            )
        elif user_profile.programming_experience == "expert":
            instructions.append(
                "Focus on architectural implications and advanced patterns. "
                "Skip basic explanations."
            )

        # Learning style adaptation
        if user_profile.learning_style == "visual":
            instructions.append(
                "Include visual analogies, diagrams descriptions, "
                "and structured layouts with headings."
            )
        elif user_profile.learning_style == "hands_on":
            instructions.append(
                "Emphasize practical examples with runnable code. "
                "Provide exercises and hands-on tasks."
            )
        elif user_profile.learning_style == "theoretical":
            instructions.append(
                "Focus on underlying principles and design patterns. "
                "Explain the 'why' behind technical decisions."
            )

        # Language preference
        if user_profile.preferred_language != "en":
            instructions.append(
                f"Translate content to {user_profile.preferred_language}, "
                f"but preserve all technical terms in English with explanations."
            )

        # Generate personalized content
        prompt = f"""Rewrite the following educational content with these personalization instructions:

{chr(10).join(f"- {inst}" for inst in instructions)}

Original Content:
{original_content}

Personalized Content (maintain technical accuracy):"""

        response = await self.client.generate(prompt)
        return response.content
```

#### 6. Database Schema (PostgreSQL + SQLAlchemy)

**Decision**: SQLAlchemy ORM with async support, Alembic for migrations.

**Schema**:
```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

-- User profiles table
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    programming_experience VARCHAR(50) NOT NULL,
    ai_experience VARCHAR(50) NOT NULL,
    learning_style VARCHAR(50) NOT NULL,
    preferred_language VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Learning journey table
CREATE TABLE learning_journeys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    current_page_path VARCHAR(500),
    completed_chapters JSONB DEFAULT '[]',
    time_on_page_seconds INTEGER DEFAULT 0,
    concepts_mastered JSONB DEFAULT '[]',
    concepts_struggling JSONB DEFAULT '[]',
    total_pages_visited INTEGER DEFAULT 0,
    total_time_seconds INTEGER DEFAULT 0,
    last_activity TIMESTAMP DEFAULT NOW()
);

-- Chat sessions table
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    page_context_path VARCHAR(500),
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    message_count INTEGER DEFAULT 0
);

-- Chat messages table
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL,  -- 'user' or 'assistant'
    content TEXT NOT NULL,
    message_type VARCHAR(50),  -- 'chat', 'explain', 'main_points', 'example', 'ask_tutor'
    rag_sources JSONB,
    response_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Generated content table
CREATE TABLE generated_content (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,  -- NULL for summaries
    page_path VARCHAR(500) NOT NULL,
    content_type VARCHAR(50) NOT NULL,  -- 'summary' or 'personalized'
    markdown_content TEXT NOT NULL,
    generated_at TIMESTAMP DEFAULT NOW(),
    cached_until TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_learning_journeys_profile_id ON learning_journeys(profile_id);
CREATE INDEX idx_chat_sessions_user_id ON chat_sessions(user_id);
CREATE INDEX idx_chat_sessions_active ON chat_sessions(user_id, is_active);
CREATE INDEX idx_chat_messages_session_id ON chat_messages(session_id);
CREATE INDEX idx_generated_content_lookup ON generated_content(user_id, page_path, content_type);
```

#### 7. Testing Strategy (TDD Mandatory)

**Decision**: pytest with async support, 90%+ coverage enforced in CI/CD.

**Test Structure**:
```
tests/
├── unit/                    # Fast, isolated tests
│   ├── test_models.py       # Database model tests
│   ├── test_agent.py        # Agent behavior tests (mocked LLM)
│   ├── test_rag.py          # RAG retrieval tests (mocked ChromaDB)
│   └── test_services.py     # Service layer tests
├── integration/             # Tests with real dependencies
│   ├── test_api_auth.py     # Auth flow with real DB
│   ├── test_websocket.py    # WebSocket with real connections
│   └── test_agent_integration.py  # Agent + RAG + DB
└── e2e/                     # End-to-end user flows
    ├── test_user_journey.py # Complete user flows
    └── test_performance.py  # Performance benchmarks
```

**TDD Workflow Example** (for Agent implementation):
```python
# RED: Write failing test first
async def test_agent_adapts_response_to_beginner():
    """Test that agent simplifies response for beginner users"""
    agent = UniversalTutorAgent(mock_llm, mock_retriever)

    user_profile = UserProfile(
        programming_experience="beginner",
        learning_style="visual"
    )
    page_context = PageContent(path="/docs/04-python/03-functions.md")

    response = await agent.respond_to_action(
        action_type=ActionType.EXPLAIN,
        user_profile=user_profile,
        page_context=page_context,
        chat_history=[]
    )

    # Assertions for beginner adaptation
    assert "analogy" in response.content.lower()
    assert "step-by-step" in response.content.lower()
    assert len(response.content.split()) < 500  # Concise for beginners

# GREEN: Implement minimal code to pass
# ... implement UniversalTutorAgent.respond_to_action()

# REFACTOR: Clean up while keeping tests green
# ... optimize context building, extract methods, improve readability
```

### Performance Optimizations

1. **Summary Pre-Generation**: Generate all 107 summaries during deployment, cache to filesystem
2. **Connection Pooling**: PostgreSQL connection pool (10-20 connections)
3. **Embedding Search**: HNSW index provides O(log n) search
4. **Content Caching**: LRU cache for personalized content (1000 entries)
5. **WebSocket Pooling**: Reuse connections, async message handling
6. **Database Indexing**: Indexes on foreign keys and frequent lookups

### Security Measures

1. **JWT Authentication**: Short-lived access tokens (15min), refresh tokens (7 days)
2. **Password Hashing**: bcrypt with salt (12 rounds)
3. **Rate Limiting**: 100 requests/minute per user, 10 WebSocket messages/second
4. **Input Validation**: Pydantic models for all API inputs
5. **SQL Injection Prevention**: SQLAlchemy parameterized queries
6. **XSS Prevention**: Sanitize all user-generated content
7. **CORS Configuration**: Whitelist frontend origin only

---

## Next Steps

After completing this plan document:

1. ✅ **Phase 0 Complete**: Create `research.md` with all technology decisions documented
2. ✅ **Phase 1 Complete**: Create `data-model.md`, `contracts/`, and `quickstart.md`
3. ⏭️ **Run `/sp.tasks`**: Generate testable tasks from this plan
4. ⏭️ **Implementation**: Execute tasks using TDD (Red-Green-Refactor)

---

## Appendix: Key References

- **Specification**: [spec.md](./spec.md)
- **Constitution**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md)
- **Embeddings Guide**: `P:\Ai native Book\...\Tutor\EMBEDDINGS_GUIDE.md`
- **Existing Embeddings**: `P:\Ai native Book\...\Tutor\backend\data\embeddings`
- **Agent Context Examples**: Provided in user input (Sarah/Ahmad/Maria/Jennifer/Carlos scenarios)
