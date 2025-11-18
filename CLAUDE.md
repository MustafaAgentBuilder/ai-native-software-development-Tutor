# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**TutorGPT Platform** - AI-powered personalized learning platform for the "AI Native Software Development" book. This is a full-stack application featuring an **AI tutor agent (OLIVIA)** powered by OpenAI Agents SDK with RAG (Retrieval-Augmented Generation) capabilities.

### Core Value Proposition
Transforms static book documentation into intelligent, personalized learning experiences through three content delivery modes:
1. **Original Tab**: Raw markdown content (no AI processing)
2. **Summary Tab**: Pre-generated concise summaries (200-400 words, no real-time AI)
3. **Personalized Tab**: Real-time AI-generated content adapted to each student's profile via OLIVIA agent

## Architecture Overview

### High-Level System Design

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Docusaurus)                     │
│  book-source/ - React + TypeScript + Docusaurus             │
│  - Three-tab system for each lesson                          │
│  - WebSocket client for streaming responses                  │
│  - Authentication UI with 4-question signup                   │
└──────────────────────┬───────────────────────────────────────┘
                       │ REST API + WebSockets
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND (FastAPI)                           │
│  Tutor-Agent/ - Python 3.11+ with async/await               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Layer (FastAPI)                                 │  │
│  │  - /api/v1/auth/* - Authentication (JWT)            │  │
│  │  - /api/v1/content/* - Content endpoints            │  │
│  │  - WebSocket streaming for personalized generation  │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 ▼                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  OLIVIA AI Agent (OpenAI Agents SDK)                │  │
│  │  - RAG-powered with ChromaDB (5480 book chunks)     │  │
│  │  - Profile-aware personalization                     │  │
│  │  - Tool: search_book_content()                       │  │
│  │  - Six-Step Prompting Framework (ACILPR)            │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 ▼                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Data Layer                                          │  │
│  │  - SQLite (dev) / PostgreSQL (prod)                 │  │
│  │  - User profiles with 4-question learning data      │  │
│  │  - Personalized content cache                        │  │
│  │  - Summary cache                                     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- Python 3.11+ with `uv` package manager
- FastAPI with async/await for high concurrency
- OpenAI Agents SDK for OLIVIA tutor agent
- ChromaDB for vector embeddings (RAG)
- SQLAlchemy ORM with SQLite/PostgreSQL
- JWT authentication with 7-day expiration
- WebSocket streaming for real-time responses

**Frontend:**
- Docusaurus 3.9.2 (React-based documentation framework)
- TypeScript for type safety
- React 19 with modern hooks
- WebSocket client for streaming
- LocalStorage for JWT token management

**AI & RAG:**
- OpenAI Agents SDK (not simple API calls)
- gpt-4o-mini model for personalization
- ChromaDB with 768-dim embeddings
- 5480 document chunks from book content
- Sentence-transformers for embedding generation

## Common Commands

### Backend Development

```bash
# Navigate to backend directory
cd Tutor-Agent

# First-time setup: Install dependencies
uv sync

# Create .env file from example
cp .env.example .env
# IMPORTANT: Edit .env and add your OPENAI_API_KEY

# Run backend server (development mode with auto-reload)
uv run python -m tutor_agent.main
# Server runs on http://localhost:8000
# API docs at http://localhost:8000/api/docs

# Run tests
uv run pytest
uv run pytest -v  # verbose output
uv run pytest --cov  # with coverage report

# Run specific test file
uv run python test_three_tabs.py
uv run python test_backend_comprehensive.py
uv run python test_olivia_profiles.py

# Code quality checks
uv run ruff check .  # linting
uv run black .  # formatting
uv run mypy src/  # type checking

# Database operations
# Database is auto-created on first run at data/tutorgpt.db
# To reset database: delete data/tutorgpt.db and restart server
```

### Frontend Development

```bash
# Navigate to frontend directory
cd book-source

# First-time setup
npm install

# Run development server
npm start
# Opens http://localhost:3000

# Build for production
npm run build

# Serve production build locally
npm run serve

# Type checking
npm run typecheck

# Clear Docusaurus cache (if seeing stale content)
npm run clear
```

### Testing Workflows

```bash
# Test backend API manually
cd Tutor-Agent

# 1. Test signup
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@test.com",
    "password": "securepass123",
    "programming_experience": "intermediate",
    "ai_experience": "basic",
    "learning_style": "visual",
    "preferred_language": "en"
  }'

# 2. Test login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "student@test.com", "password": "securepass123"}'
# Save the "access_token" from response

# 3. Test personalized content (replace TOKEN with actual JWT)
curl http://localhost:8000/api/v1/content/personalized/01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything \
  -H "Authorization: Bearer TOKEN"

# 4. Test original content (no auth required)
curl http://localhost:8000/api/v1/content/original/01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything

# 5. Test summary content (no auth required)
curl http://localhost:8000/api/v1/content/summary/01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything
```

## Critical Architectural Decisions

### 1. Three-Tab Content Strategy

**Decision**: Separate content into three distinct tabs with different processing levels

**Rationale**:
- **Original Tab**: Zero latency, pure file serving for readers who want unmodified content
- **Summary Tab**: Pre-generated during build, instant delivery, no API costs
- **Personalized Tab**: Real-time AI generation, highest value, gated behind authentication

**Implementation**:
- Each tab has its own endpoint and processing pipeline
- Clear separation of concerns prevents AI overhead on simple content
- Caching strategy differs per tab (summary = static files, personalized = database cache with profile validation)

### 2. OLIVIA Agent Architecture (OpenAI Agents SDK)

**Decision**: Use OpenAI Agents SDK with RAG instead of simple API calls

**Rationale**:
- **Tool Use**: Agent can search book embeddings before generating (prevents hallucination)
- **Conversation Memory**: Maintains context across interactions
- **Streaming**: Better UX with progressive content delivery
- **Extensibility**: Easy to add more tools (calculate, search web, run code)

**Critical Implementation Details**:
```python
# services/agent/olivia_agent.py
from agents import Agent, Runner

# Agent initialization with tools
agent = Agent(
    name="OLIVIA",
    instructions=six_step_prompt,  # ACILPR framework
    tools=[search_book_content],
)

# Streaming execution
async for chunk in Runner.stream(agent, user_query):
    yield chunk
```

**WARNING**: Do NOT use simple `openai.chat.completions.create()` - always use the Agent SDK

### 3. Profile-Aware Cache Invalidation

**Decision**: Cache personalized content per user+page+profile snapshot

**Rationale**:
- Personalized content generation is expensive (30-60s, OpenAI API costs)
- User profile changes should trigger regeneration
- Multiple users on same page should have separate caches

**Implementation**:
- `PersonalizedCache` model stores profile snapshot (programming_experience, ai_experience, learning_style, preferred_language)
- Cache lookup checks: `user_id == current_user AND page_path == requested_page AND profile_snapshot == current_profile`
- Profile mismatch → invalidate cache → regenerate content

### 4. WebSocket Streaming for Personalized Content

**Decision**: Use WebSocket for personalized content generation instead of HTTP polling

**Rationale**:
- Generation takes 30-60 seconds (slow for synchronous HTTP)
- Students need progress feedback ("Searching book...", "Generating content...", "80% complete...")
- Streaming chunks provides better perceived performance

**WebSocket Events**:
```typescript
// Progressive events during generation
{ type: "progress", message: "Searching book content...", percentage: 20 }
{ type: "chunk", content: "# Personalized for You\n\n" }
{ type: "chunk", content: "Based on your visual learning style..." }
{ type: "complete", full_content: "..." }
```

### 5. Four-Question Profile System

**Decision**: Collect exactly 4 questions during signup, no more

**Rationale**:
- Balances personalization power with user friction
- Each question maps to specific prompting strategies
- More questions = higher dropout rate

**Questions & Their Impact**:
1. **Programming Experience** (beginner/intermediate/advanced)
   - Beginner: "Explain from first principles, define all terms"
   - Advanced: "Focus on advanced patterns, assume strong fundamentals"

2. **AI/ML Experience** (none/basic/intermediate/advanced)
   - None: "Introduce AI concepts gently, explain terminology"
   - Advanced: "Deep dive into architectures, discuss trade-offs"

3. **Learning Style** (visual/practical/conceptual/mixed)
   - Visual: Generate Mermaid diagrams, use ASCII art, structured layouts
   - Practical: Prioritize code examples, hands-on exercises
   - Conceptual: Theory-first explanations, mental models

4. **Preferred Language** (en/es/fr/de/zh/ja/ru/ar/hi/ur + more)
   - Translates explanations while preserving technical English terms

## Key Code Locations

### Backend Critical Files

```
Tutor-Agent/src/tutor_agent/
├── main.py                               # FastAPI app entry, CORS config, router includes
├── api/v1/
│   ├── auth.py                           # JWT authentication endpoints (signup, login, me)
│   └── content.py                        # Content endpoints (original, summary, personalized)
│                                         # WebSocket streaming endpoint for personalized
├── core/
│   ├── database.py                       # SQLAlchemy engine, session management, init_db()
│   └── security.py                       # JWT creation/verification, password hashing
├── models/
│   ├── base.py                           # Shared SQLAlchemy Base
│   ├── user.py                           # User model with 4-question profile
│   └── cache.py                          # SummaryCache and PersonalizedCache models
├── schemas/
│   ├── auth.py                           # Pydantic schemas for auth requests/responses
│   └── content.py                        # Pydantic schemas for content responses
├── services/
│   ├── agent/
│   │   ├── olivia_agent.py               # OLIVIA AI Agent with Six-Step Prompting
│   │   └── tools/
│   │       └── rag_search.py             # ChromaDB RAG search tool
│   ├── cache/
│   │   ├── summary_cache.py              # Summary cache manager
│   │   └── personalization_cache.py      # Personalized content cache manager
│   └── personalized_content.py           # Personalized content service (uses OLIVIA)
└── config/
    └── settings.py                       # Environment variables, settings management
```

### Frontend Critical Files

```
book-source/
├── docusaurus.config.ts                  # Docusaurus configuration
├── src/
│   ├── components/
│   │   ├── PersonalizedTab/
│   │   │   ├── index.tsx                 # Main PersonalizedTab component
│   │   │   ├── LoginForm.tsx             # Login form UI
│   │   │   ├── SignupForm.tsx            # Signup with 4-question profile
│   │   │   └── PersonalizedContent.tsx   # Displays personalized markdown
│   │   └── SummaryTab/
│   │       └── index.tsx                 # Summary tab component (reference implementation)
│   ├── hooks/
│   │   └── useAuth.ts                    # Authentication state management hook
│   └── services/
│       └── api.ts                        # API client for backend communication
└── docs/
    └── 04-Python-Fundamentals/           # Example book content directory
        ├── 01-variables.md               # Lesson pages with tab system
        └── ...
```

### Data Storage

```
Tutor-Agent/
├── data/
│   ├── embeddings/                       # ChromaDB embeddings (5480 chunks, 19MB)
│   │   └── chroma.sqlite3                # ChromaDB SQLite database
│   └── tutorgpt.db                       # Application SQLite database (auto-created)
│                                         # Tables: users, personalized_content, summary_cache

book-source/
└── static/
    └── summaries/                        # Pre-generated summaries (31 .md files)
```

## Important Patterns and Conventions

### 1. Six-Step Prompting Framework (ACILPR)

**Used in**: `services/agent/olivia_agent.py`

Every prompt to OLIVIA follows this structure:
```
1. Actor: "You are OLIVIA, an AI tutor specializing in..."
2. Context: User profile, current page, conversation history
3. Instruction: "Generate personalized content based on..."
4. Limitations: "Preserve code examples, no emojis, similar length to original"
5. Persona: Adaptive tone (encouraging for beginners, technical for advanced)
6. Response Format: Structured markdown template
```

### 2. Cache Validation Strategy

**Pattern**: Triple-key cache with profile snapshot validation

```python
# Cache lookup logic
def get_cached_content(user_id, page_path, current_profile):
    cache = db.query(PersonalizedCache).filter(
        PersonalizedCache.user_id == user_id,
        PersonalizedCache.page_path == page_path
    ).first()

    if cache and cache.profile_matches(current_profile):
        return cache.content  # Cache hit
    else:
        return None  # Cache miss or profile mismatch → regenerate
```

**When cache invalidates**:
- User changes any of the 4 profile fields
- Page content is updated (future: add version tracking)
- Manual cache clear via API

### 3. Error Handling Standards

**API Errors** follow this structure:
```python
from fastapi import HTTPException

# Authentication errors
raise HTTPException(status_code=401, detail="Invalid credentials")
raise HTTPException(status_code=401, detail="Token expired")

# Content errors
raise HTTPException(status_code=404, detail="Page not found")
raise HTTPException(status_code=500, detail="AI generation failed")

# Validation errors (handled by Pydantic automatically)
```

**Frontend Error Display**:
```typescript
try {
  const response = await fetch(url, options);
  if (!response.ok) {
    const error = await response.json();
    setError(error.detail || "An error occurred");
  }
} catch (err) {
  setError("Network error. Please try again.");
}
```

### 4. Async/Await Patterns

**Backend (FastAPI)**:
```python
# All route handlers should be async
@router.get("/personalized/{page_path}")
async def get_personalized_content(
    page_path: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    content = await personalization_service.generate(page_path, current_user)
    return content
```

**Frontend (React)**:
```typescript
// Use async functions in useEffect
useEffect(() => {
  const fetchContent = async () => {
    try {
      const data = await apiClient.get(`/personalized/${pagePath}`);
      setContent(data);
    } catch (err) {
      setError(err);
    }
  };
  fetchContent();
}, [pagePath]);
```

## Development Workflow

### Adding a New Feature

1. **Specification First** (following Spec-Driven Development)
   ```bash
   # Create spec in specs/00X-feature-name/
   - spec.md    # WHAT we're building (user stories, requirements)
   - plan.md    # HOW we'll build it (architecture, decisions)
   - tasks.md   # Concrete implementation tasks
   ```

2. **TDD Cycle** (from `.specify/memory/constitution.md`)
   ```
   RED → GREEN → REFACTOR

   - Write failing test first
   - Implement minimal code to pass
   - Refactor while keeping tests green
   - Minimum 90% test coverage required
   ```

3. **Backend Implementation**
   ```bash
   # 1. Create models (if needed)
   Tutor-Agent/src/tutor_agent/models/new_model.py

   # 2. Create schemas
   Tutor-Agent/src/tutor_agent/schemas/new_schema.py

   # 3. Create service logic
   Tutor-Agent/src/tutor_agent/services/new_service.py

   # 4. Create API endpoint
   Tutor-Agent/src/tutor_agent/api/v1/new_endpoint.py

   # 5. Include router in main.py
   app.include_router(new_endpoint.router, prefix="/api/v1/new")

   # 6. Write tests
   Tutor-Agent/test_new_feature.py
   ```

4. **Frontend Implementation**
   ```bash
   # 1. Create component
   book-source/src/components/NewFeature/index.tsx

   # 2. Create API client function
   book-source/src/services/api.ts (add new method)

   # 3. Create hook if needed
   book-source/src/hooks/useNewFeature.ts

   # 4. Integrate into pages
   ```

5. **Testing & Validation**
   ```bash
   # Backend tests
   cd Tutor-Agent
   uv run pytest

   # Manual API testing
   # See "Testing Workflows" section above

   # Frontend testing
   cd book-source
   npm start
   # Manual testing in browser
   ```

### Database Migrations

**Current**: Auto-migration via SQLAlchemy `init_db()`

```python
# core/database.py
def init_db():
    Base.metadata.create_all(bind=engine)
```

**For Production**: Use Alembic for versioned migrations
```bash
# Future: When deploying to production
alembic init alembic
alembic revision --autogenerate -m "Add new table"
alembic upgrade head
```

## Environment Variables

**Required** (create `Tutor-Agent/.env`):
```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-...your-key...
OPENAI_MODEL=gpt-4o-mini

# JWT Authentication
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production

# Database Configuration
DATABASE_URL=sqlite:///./data/tutorgpt.db
# For PostgreSQL: postgresql://user:password@localhost:5432/tutorgpt

# Application Settings
APP_NAME=TutorGPT
APP_VERSION=0.1.0
DEBUG=true

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

**CRITICAL**: Never commit `.env` file. Always use `.env.example` as template.

## Performance Considerations

### 1. Content Generation Times

- **Original Tab**: <100ms (instant file read)
- **Summary Tab**: <50ms (static file from disk)
- **Personalized Tab**:
  - First generation: 30-60 seconds (AI generation + RAG search)
  - Cached: <100ms (database lookup)

**Optimization**: Aggressive caching with profile validation reduces repeated AI calls

### 2. Database Queries

**Use composite indexes** for frequent queries:
```python
# models/cache.py
__table_args__ = (
    Index('ix_personalized_user_page', 'user_id', 'page_path'),
)
```

**Current indexes**:
- `users.email` (unique)
- `personalized_content.user_id + page_path` (composite)
- `summary_cache.page_path` (unique)

### 3. WebSocket Connection Limits

FastAPI with uvicorn can handle ~1000 concurrent WebSocket connections per process.

**Scaling strategy** (future):
```
nginx (load balancer)
  ├── uvicorn worker 1 (1000 connections)
  ├── uvicorn worker 2 (1000 connections)
  └── uvicorn worker 3 (1000 connections)
= 3000 concurrent students
```

## Security Best Practices

### 1. Authentication

- **JWT Expiration**: 7 days (not too short to annoy users, not too long to risk security)
- **Password Hashing**: argon2-cffi (more secure than bcrypt on Python 3.11+)
- **Token Storage**: localStorage (frontend) - acceptable for learning platform, consider httpOnly cookies for higher security

### 2. API Protection

```python
# Dependency injection for auth
from fastapi import Depends
from tutor_agent.core.security import get_current_user

@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    # current_user is guaranteed to be authenticated
    pass
```

### 3. Input Validation

**Use Pydantic schemas** for all API inputs:
```python
class SignupRequest(BaseModel):
    email: EmailStr  # Validates email format
    password: str = Field(min_length=8)  # Enforces minimum length
    programming_experience: ProgrammingExperience  # Enum validation
```

### 4. CORS Configuration

```python
# main.py - restrict origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Development
        "https://yourapp.com"     # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Troubleshooting Common Issues

### Backend won't start

**Error**: "No module named 'tutor_agent'"
```bash
# Solution: Ensure you're in Tutor-Agent directory
cd Tutor-Agent
uv sync
uv run python -m tutor_agent.main
```

**Error**: "OPENAI_API_KEY not found"
```bash
# Solution: Create .env file
cp .env.example .env
# Edit .env and add your key
```

**Error**: "Database locked"
```bash
# Solution: SQLite doesn't support concurrent writes
# For production, switch to PostgreSQL in .env:
DATABASE_URL=postgresql://user:pass@localhost:5432/tutorgpt
```

### Frontend issues

**Error**: "Failed to fetch" or CORS errors
```bash
# Solution 1: Ensure backend is running on port 8000
cd Tutor-Agent
uv run python -m tutor_agent.main

# Solution 2: Check CORS origins in Tutor-Agent/src/tutor_agent/main.py
# Ensure your frontend port is allowed
```

**Error**: "401 Unauthorized" on personalized content
```bash
# Solution: Check JWT token in localStorage
# 1. Open browser DevTools → Application → Local Storage
# 2. Look for 'auth_token' or 'access_token'
# 3. If missing or expired, login again
```

### AI Generation issues

**Error**: "OpenAI API rate limit exceeded"
```bash
# Solution: Add retry logic or wait
# Check OpenAI dashboard for rate limits
```

**Error**: "ChromaDB collection not found"
```bash
# Solution: Ensure embeddings directory exists
cd Tutor-Agent/data/embeddings
ls chroma.sqlite3  # Should exist

# If missing, regenerate embeddings (see docs)
```

## Testing Strategy

### Backend Testing

**Test Pyramid**:
```
                 /\
                /  \  E2E Tests (10%)
               /────\
              /      \  Integration Tests (30%)
             /────────\
            /          \  Unit Tests (60%)
           /────────────\
```

**Test Files**:
- `test_three_tabs.py` - Tests three-tab separation of concerns
- `test_backend_comprehensive.py` - Integration tests (22 tests)
- `test_olivia_profiles.py` - Tests OLIVIA personalization with different profiles
- `test_visual_learning.py` - Tests visual learner diagram generation
- `test_multilanguage.py` - Tests language translation accuracy

**Run all tests**:
```bash
cd Tutor-Agent
uv run pytest -v --cov
```

### Frontend Testing

**Manual Testing Checklist**:
- [ ] Signup with 4 questions
- [ ] Login with created account
- [ ] View Original tab (instant load)
- [ ] View Summary tab (instant load)
- [ ] View Personalized tab (requires login, shows adapted content)
- [ ] Logout and verify token cleared
- [ ] Login again and verify cached personalized content loads instantly

### End-to-End Testing Script

```bash
# See IMPLEMENTATION_STATUS.md "Demo Script" section
# Test Scenario 1: Beginner Visual Learner
# Test Scenario 2: Advanced Hands-On Learner
```

## Deployment

### Backend Deployment (Railway/Render/Fly.io)

```bash
# 1. Set environment variables in platform dashboard:
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=...production-secret...

# 2. Deploy command (example for Railway)
# Railway auto-detects Python and runs:
uvicorn tutor_agent.main:app --host 0.0.0.0 --port $PORT
```

### Frontend Deployment (Vercel/Netlify)

```bash
# 1. Build command:
cd book-source && npm run build

# 2. Publish directory:
book-source/build

# 3. Environment variables:
REACT_APP_API_URL=https://your-backend.railway.app
```

## Project Status

**Last Updated**: 2025-11-17

**Completion Status**:
- ✅ **Backend**: 100% complete
  - Three-tab content system
  - OLIVIA AI agent with RAG
  - User authentication with JWT
  - Profile-aware caching
  - WebSocket streaming

- ✅ **Frontend**: 80% complete
  - PersonalizedTab component implemented
  - Three-tab system working
  - Authentication UI complete
  - WebSocket client integrated

- ⏳ **Testing**: 90% complete
  - Backend comprehensive test suite
  - Manual end-to-end tests documented
  - Automated frontend tests pending

**See**: `IMPLEMENTATION_STATUS.md` for detailed status and next steps

## Key Documentation Files

- `README.md` - Project overview and vision
- `IMPLEMENTATION_STATUS.md` - Current implementation status, testing results
- `API_TESTING_GUIDE.md` - Comprehensive API testing instructions
- `HANDOFF.md` - Complete implementation guide for frontend
- `QUICK_START.md` - 5-minute onboarding guide
- `TESTING_THREE_TABS.md` - Three-tab testing manual
- `specs/001-tutorgpt-platform/spec.md` - Feature specification
- `specs/001-tutorgpt-platform/plan.md` - Architecture and design decisions
- `.specify/memory/constitution.md` - Project principles and standards

## Contributing Guidelines

### Code Style

**Python** (enforced by ruff + black):
```python
# Use type hints
async def get_user(user_id: int) -> User:
    return await db.get(User, user_id)

# Use descriptive names
user_profile = get_user_profile(user_id)  # Good
up = gup(uid)  # Bad

# Docstrings for all public functions
def personalize_content(page_path: str, user: User) -> str:
    """
    Generate personalized content for a page based on user profile.

    Args:
        page_path: Path to book page (e.g., "01-Chapter/01-Section")
        user: User object with learning profile

    Returns:
        Personalized markdown content adapted to user's level
    """
```

**TypeScript** (enforced by tsc):
```typescript
// Use interfaces for object shapes
interface UserProfile {
  programmingExperience: string;
  aiExperience: string;
  learningStyle: string;
  preferredLanguage: string;
}

// Use async/await, not .then()
const fetchUser = async (id: string): Promise<User> => {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
};
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
feat: add WebSocket streaming for personalized content
fix: resolve cache invalidation on profile update
docs: update API testing guide with WebSocket examples
test: add comprehensive three-tab separation tests
refactor: extract OLIVIA prompt building to separate service
```

### Pull Request Process

1. Create feature branch: `git checkout -b feat/your-feature`
2. Write tests first (TDD)
3. Implement feature
4. Ensure all tests pass: `uv run pytest`
5. Update documentation if needed
6. Submit PR with clear description

## AI Agent Development Guidelines

**MANDATORY**: When building AI features, ALWAYS:

1. **Read these skills first**:
   - `C:\Users\USER\.claude\skills\openai-agents-expert.md`
   - `C:\Users\USER\.claude\skills\Prompt-&-Context-Engineering-Skill.md`

2. **Use OpenAI Agents SDK**, not simple API calls:
   ```python
   # ✅ Correct
   from agents import Agent, Runner
   agent = Agent(name="OLIVIA", tools=[...])
   result = await Runner.run(agent, query)

   # ❌ Wrong
   openai.chat.completions.create(...)
   ```

3. **Always use RAG** for book-related questions:
   ```python
   @tool_decorator
   def search_book_content(query: str) -> str:
       """Search book embeddings"""
       results = chroma_collection.query(query_texts=[query], n_results=3)
       return format_results(results)
   ```

4. **Stream responses** for better UX:
   ```python
   async for chunk in Runner.stream(agent, query):
       yield chunk
   ```

5. **Use Six-Step Prompting (ACILPR)** for all prompts:
   - Actor, Context, Instruction, Limitations, Persona, Response Format

## Useful Resources

- **OpenAI Agents SDK**: https://openai.github.io/openai-agents-python
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Docusaurus Docs**: https://docusaurus.io
- **ChromaDB Docs**: https://docs.trychroma.com
- **SQLAlchemy ORM**: https://docs.sqlalchemy.org/en/20/
- **Pydantic**: https://docs.pydantic.dev
- **React Hooks**: https://react.dev/reference/react

## Contact & Support

**Maintainer**: Mustafa Adeel
**Email**: mustafaadeel989@gmail.com
**GitHub**: [MustafaAgentBuilder/ai-native-software-development-Tutor](https://github.com/MustafaAgentBuilder/ai-native-software-development-Tutor)

---

**This project follows Spec-Driven Development (SDD) methodology. All features start with specs, progress through planning, and implement with TDD (Test-Driven Development) for 90%+ test coverage.**
