<!-- Claude is Work to Build this Project -->
# 🏗️ ARCHITECTURE UPDATE - RAG-Powered OLIVIA Agent

**Date**: 2025-11-15
**Status**: ⚠️ CRITICAL - Backend Architecture Changed
**Action Required**: Update HANDOFF.md, QUICK_START.md, STATUS.md, specs, plan, constitution

---

## 🚨 IMPORTANT ARCHITECTURE CHANGE

### OLD Architecture (Simple OpenAI API):
```
User Request → API → Simple OpenAI Call → Response
```

### NEW Architecture (RAG-Powered AI Agent):
```
User Request → API → OLIVIA AI Agent → RAG Tool (ChromaDB) → Context → Agent Reasoning → Streaming Response
                                    ↓
                              Conversation Memory (last 7 msgs)
                                    ↓
                              User Profile Awareness
```

---

## ✅ What Was Added

1. **ChromaDB Embeddings** (19MB)
   - Location: `Tutor-Agent/data/embeddings/`
   - Contains: Book content embeddings for RAG
   - Format: ChromaDB SQLite database

2. **New Dependency**:
   - `chromadb>=0.4.0` added to `pyproject.toml`

3. **Architecture Shift**:
   - FROM: Simple `openai.chat.completions.create()` calls
   - TO: Full AI Agent with RAG, tools, memory, streaming

---

## 🎯 NEW Requirements (User Confirmed)

### 1. Use OpenAI Agents SDK (NOT Simple API)
**Mandatory**: ALL AI interactions MUST use OpenAI Agents SDK

```python
# ❌ OLD (Don't use this anymore):
response = openai.chat.completions.create(...)

# ✅ NEW (Required):
from agents import Agent, Runner

agent = Agent(name="OLIVIA", instructions="...", tools=[...])
result = await Runner.run(agent, user_query)
```

### 2. RAG with ChromaDB
**Mandatory**: Agent MUST use RAG to fetch relevant content

```python
@tool_decorator
def search_book_content(current_page_path: str, query: str) -> str:
    """
    Search book embeddings for relevant content

    Args:
        current_page_path: e.g., "01-Introducing-AI-Driven-Development/..."
        query: User's question or topic

    Returns:
        Relevant content from book embeddings
    """
    # Query ChromaDB
    # Return relevant chunks
```

### 3. Streaming Response
**Mandatory**: Content generation MUST stream

Frontend should show:
```
"✨ Generating your personalized content..."
[Content streams in word by word or chunk by chunk]
```

Backend must use:
```python
async for chunk in Runner.stream(agent, query):
    yield chunk
```

### 4. Conversation Memory
**Mandatory**: Remember last 7 messages per user

```python
class ConversationMemory:
    def __init__(self, user_id: int, max_messages: int = 7):
        self.user_id = user_id
        self.messages = deque(maxlen=max_messages)

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def get_context(self) -> List[Dict]:
        return list(self.messages)
```

### 5. Dual Purpose Agent
**Important**: Same agent will be used for:
- **Personalized Tab**: Generate adapted lesson content
- **Sidebar Chat** (future): Answer questions about book

Agent must:
- Know user's current page
- Know user's learning profile (4 questions)
- Use RAG to fetch relevant context
- Remember conversation history

### 6. Page-Specific Content Generation
**Behavior**:
- User on "Part 1 → Chapter 3 → Subtopic 5"
- Agent fetches ONLY that page's content from RAG
- Generates personalized version based on user profile
- Returns as streaming response

---

## 📋 Files That Need Updates

### 1. HANDOFF.md
**Section to Update**: "Backend Implementation Details"

**Add**:
```markdown
## OLIVIA AI Agent Architecture

### Agent Overview
OLIVIA (OpenAI Learning and Interactive Virtual Instructional Agent) is a RAG-powered AI tutor that:
- Uses OpenAI Agents SDK for reasoning and tool use
- Queries ChromaDB embeddings for relevant book content
- Adapts content to user's learning profile (4 questions)
- Remembers last 7 conversation messages
- Streams responses for live "generating..." UX

### Agent Tools
1. **search_book_content**: Query ChromaDB for relevant content
2. **get_user_profile**: Retrieve user's 4-question profile
3. **get_conversation_history**: Retrieve last 7 messages

### Agent Flow
1. User requests personalized content for page X
2. Agent searches RAG for page X content
3. Agent retrieves user profile (programming level, AI experience, etc.)
4. Agent retrieves last 7 messages (if any)
5. Agent generates personalized content using:
   - Original content (from RAG)
   - User profile (adaptation level)
   - Conversation context (continuity)
6. Agent streams response to frontend
```

**Update**: Architecture diagram to show RAG flow

### 2. QUICK_START.md
**Section to Add**:
```markdown
## 🧠 OLIVIA AI Agent

The backend uses a RAG-powered AI agent, not simple API calls.

**What this means**:
- Content is retrieved from embeddings (not hardcoded)
- Agent has tools to search, reason, and adapt
- Responses stream in real-time
- Conversation context is preserved

**Embeddings Location**: `Tutor-Agent/data/embeddings/` (19MB ChromaDB)
**Agent Implementation**: `Tutor-Agent/src/tutor_agent/services/olivia_agent.py`
```

### 3. STATUS.md
**Update "Completed Features" Section**:

```markdown
### 2. Personalized Learning Backend (70% Complete)
- ✅ User authentication (JWT with 7-day expiration)
- ✅ 4-question learning profile system
- ✅ Database models (User, PersonalizedContent)
- ✅ ChromaDB embeddings (19MB book content)
- ✅ chromadb dependency added
- ⏳ OLIVIA AI Agent with RAG (NEEDS IMPLEMENTATION)
- ⏳ Streaming response (NEEDS IMPLEMENTATION)
- ⏳ Conversation memory (NEEDS IMPLEMENTATION)
- ⏳ RAG tool for ChromaDB search (NEEDS IMPLEMENTATION)

**Current State**: Simple OpenAI API → **Must Upgrade** → AI Agent with RAG
```

### 4. specs/001-tutorgpt-platform/plan.md
**Add Section**: "AI Agent Architecture"

```markdown
## AI Agent Architecture

### OLIVIA Agent Design

**Agent Name**: OLIVIA (OpenAI Learning and Interactive Virtual Instructional Agent)

**Agent Capabilities**:
1. RAG-based content retrieval from book embeddings
2. User profile-aware content adaptation
3. Conversation memory (7 messages)
4. Streaming response generation
5. Tool use for search and context gathering

**Tools**:
- `search_book_content(page_path, query)` - Query ChromaDB
- `get_user_profile(user_id)` - Retrieve learning profile
- `get_conversation_history(user_id)` - Retrieve last 7 messages

**Prompting Strategy**: Six-Step Framework (ACILPR)
1. Actor: "You are OLIVIA, an AI tutor..."
2. Context: User profile + current page + conversation history
3. Instruction: Generate personalized content
4. Limitations: Keep length similar, preserve code examples
5. Persona: Adaptive based on user level
6. Response Format: Markdown with sections

**Technology**:
- OpenAI Agents SDK (`agents` package)
- ChromaDB for vector search
- SQLAlchemy for conversation storage
- FastAPI streaming responses
```

### 5. specs/001-tutorgpt-platform/spec.md
**Update User Story 2**:

```markdown
## User Story 2: Personalized Learning Experience

### Requirements Update

**AI Agent (MANDATORY)**:
- Use OpenAI Agents SDK (NOT simple API calls)
- Implement RAG with ChromaDB embeddings
- Stream responses ("Generating..." UX)
- Remember last 7 conversation messages

**Agent Behavior**:
1. User requests personalized content for page
2. Agent uses RAG tool to fetch page content
3. Agent retrieves user's 4-question profile
4. Agent adapts content to user's level
5. Agent streams response

**Acceptance Criteria**:
- [ ] OLIVIA agent implemented using OpenAI Agents SDK
- [ ] RAG tool queries ChromaDB embeddings
- [ ] Content streams to frontend (not blocking)
- [ ] Conversation memory persists last 7 messages
- [ ] Agent adapts to user profile (beginner/intermediate/advanced)
- [ ] Same agent works for both personalized content + chat
```

### 6. .specify/memory/constitution.md
**Add Section**: "AI Agent Principles"

```markdown
## AI Agent Principles

### Agent-First Development
- ALL AI interactions MUST use OpenAI Agents SDK
- NO simple `openai.chat.completions.create()` calls
- Agents MUST have tools, memory, and streaming

### RAG Requirements
- All content generation MUST use RAG (not hallucination)
- ChromaDB embeddings are source of truth for book content
- Agent MUST search embeddings before generating

### Streaming Responses
- ALL agent responses MUST stream (not blocking)
- Frontend MUST show "Generating..." state
- Use `Runner.stream()` for async streaming

### Conversation Memory
- Remember last 7 messages per user
- Store in database (User-Message table)
- Include in agent context on each request

### Agent Tools (Mandatory)
Every agent MUST have:
1. RAG search tool
2. User profile retrieval tool
3. Conversation history tool
```

---

## 🔧 Implementation TODO

### Priority 1: Core Agent (NEXT CODING SESSION)
1. Create `services/rag_service.py` - ChromaDB search
2. Create `services/olivia_agent.py` - AI Agent with tools
3. Create `models/conversation.py` - Message storage
4. Update `services/personalized_content.py` - Use agent instead of API

### Priority 2: Streaming
5. Update `api/v1/content.py` - Add streaming endpoint
6. Implement `StreamingResponse` in FastAPI

### Priority 3: Memory
7. Create conversation storage in database
8. Implement 7-message memory retrieval

### Priority 4: Frontend (LATER)
9. Update frontend to handle streaming
10. Show "Generating..." animation

---

## ⚠️ Breaking Changes

### For Next Developer

**OLD CODE (Don't Use)**:
```python
# services/personalized_content.py (OUTDATED)
response = self.client.chat.completions.create(
    model=self.model,
    messages=[...],
)
```

**NEW CODE (Required)**:
```python
# services/olivia_agent.py (NEW)
from agents import Agent, Runner, tool_decorator

agent = Agent(
    name="OLIVIA",
    instructions="...",
    tools=[search_book_content, get_user_profile],
)

async for chunk in Runner.stream(agent, user_query):
    yield chunk
```

---

## 📚 Required Reading

Before implementing:
1. Read `C:\Users\USER\.claude\skills\openai-agents-expert.md`
2. Read `C:\Users\USER\.claude\skills\Prompt-&-Context-Engineering-Skill.md`
3. Review ChromaDB docs: https://docs.trychroma.com/
4. Review OpenAI Agents SDK: https://openai.github.io/openai-agents-python

---

## ✅ Update Checklist

- [ ] Update HANDOFF.md with RAG agent architecture
- [ ] Update QUICK_START.md with agent info
- [ ] Update STATUS.md with new completion %
- [ ] Update specs/001-tutorgpt-platform/plan.md
- [ ] Update specs/001-tutorgpt-platform/spec.md
- [ ] Update .specify/memory/constitution.md
- [ ] Create detailed RAG_AGENT_TODO.md
- [ ] Commit and push all documentation updates

---

**This document supersedes any previous architecture descriptions. RAG-powered OLIVIA agent is now the required approach.**
