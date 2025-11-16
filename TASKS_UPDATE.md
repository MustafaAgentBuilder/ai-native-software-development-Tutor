<!-- Claude is Work to Build this Project -->
# ⚠️ TASKS.MD UPDATE - RAG Agent Architecture

**Date**: 2025-11-15
**Reason**: Architecture changed to RAG-powered OLIVIA AI Agent with WebSocket streaming

---

## 🔄 CHANGES TO APPLY

### 1. Update Phase 2: Foundational (Add New Tasks)

**Insert after T016**:

```markdown
###OLIVIA AI Agent Foundation (CRITICAL - Required for US2/US3/US4)

- [ ] T021 Create OLIVIA agent base class using OpenAI Agents SDK in Tutor-Agent/src/tutor_agent/services/agent/olivia_agent.py
- [ ] T022 Implement RAG search tool for agent (queries ChromaDB) in Tutor-Agent/src/tutor_agent/services/agent/tools/search_book_content.py
- [ ] T023 Implement user profile tool for agent in Tutor-Agent/src/tutor_agent/services/agent/tools/get_user_profile.py
- [ ] T024 Implement conversation history tool (last 7 messages) in Tutor-Agent/src/tutor_agent/services/agent/tools/get_conversation_history.py
- [ ] T025 Create ConversationMessage model (user_id, role, content, timestamp) in Tutor-Agent/src/tutor_agent/models/conversation.py
- [ ] T026 Create prompt templates using Six-Step Framework (ACILPR) in Tutor-Agent/src/tutor_agent/services/agent/prompts/six_step_template.py
- [ ] T027 Implement context builder (profile + page + history) in Tutor-Agent/src/tutor_agent/services/agent/context_builder.py
- [ ] T028 Write unit tests for OLIVIA agent tools (mocked dependencies) in Tutor-Agent/tests/unit/test_olivia_agent.py
- [ ] T029 Write integration test for agent with RAG in Tutor-Agent/tests/integration/test_agent_rag.py
```

### 2. Update Phase 2: Add WebSocket Streaming Tasks

**Insert after new OLIVIA tasks**:

```markdown
### WebSocket Streaming Infrastructure (Required for Live Generation UX)

- [ ] T030 Create WebSocket connection manager with room/channel support in Tutor-Agent/src/tutor_agent/core/websocket_manager.py
- [ ] T031 Implement WebSocket authentication middleware (JWT in query params) in Tutor-Agent/src/tutor_agent/core/websocket_auth.py
- [ ] T032 Create streaming response handler for agent output in Tutor-Agent/src/tutor_agent/services/agent/streaming.py
- [ ] T033 Implement WebSocket endpoint /ws/chat/{user_id} in Tutor-Agent/src/tutor_agent/api/v1/websocket.py
- [ ] T034 Create message queue for streaming chunks in Tutor-Agent/src/tutor_agent/core/message_queue.py
- [ ] T035 Write unit tests for WebSocket manager in Tutor-Agent/tests/unit/test_websocket.py
```

### 3. Update User Story 2 Tasks (Replace T057-T067)

**REMOVE**:
- T057-T067 (old simple OpenAI API approach)

**REPLACE WITH**:

```markdown
**Services (Green Phase) - RAG Agent Approach**

- [ ] T057 [US2] Implement PersonalizedContentService using OLIVIA agent in Tutor-Agent/src/tutor_agent/services/personalized_content_service.py
- [ ] T058 [US2] Configure OLIVIA agent for personalized content generation (not chat) in PersonalizedContentService
- [ ] T059 [US2] Implement conversation memory storage (last 7 messages per user) in Tutor-Agent/src/tutor_agent/services/conversation_service.py
- [ ] T060 [US2] Add streaming support via WebSocket for "Generating..." UX in PersonalizedContentService
- [ ] T061 [US2] Implement PersonalizedContent cache model (user_id, page_path, markdown, profile_snapshot) in Tutor-Agent/src/tutor_agent/models/content.py
- [ ] T062 [US2] Add cache invalidation when user profile changes in PersonalizedContentService

**API Endpoints (Green Phase) - WebSocket Approach**

- [ ] T063 [P] [US2] Implement POST /api/v1/auth/signup (email, password, 4 questions) in Tutor-Agent/src/tutor_agent/api/v1/auth.py
- [ ] T064 [P] [US2] Implement POST /api/v1/auth/login (email, password) returning JWT in Tutor-Agent/src/tutor_agent/api/v1/auth.py
- [ ] T065 [P] [US2] Implement GET /api/v1/auth/me returning current user profile in Tutor-Agent/src/tutor_agent/api/v1/auth.py
- [ ] T066 [P] [US2] Implement PUT /api/v1/profile for updating preferences in Tutor-Agent/src/tutor_agent/api/v1/profile.py
- [ ] T067 [US2] Implement WebSocket /ws/personalized/{page_path} with streaming generation in Tutor-Agent/src/tutor_agent/api/v1/websocket.py
- [ ] T068 [US2] Add REST fallback GET /api/v1/content/personalized/{page_path} (no streaming) in Tutor-Agent/src/tutor_agent/api/v1/content.py
```

### 4. Update User Story 2 Frontend Tasks (Update T076-T079)

**UPDATE**:

```markdown
**Components (Green Phase) - WebSocket Streaming**

- [ ] T076 [US2] Implement PersonalizedTab with WebSocket streaming UI in book-source/src/components/TabSystem/PersonalizedTab.tsx
- [ ] T077 [US2] Create StreamingContent component showing "Generating..." animation in book-source/src/components/TabSystem/StreamingContent.tsx
- [ ] T078 [US2] Implement useWebSocket hook for real-time streaming in book-source/src/hooks/useWebSocket.ts
- [ ] T079 [US2] Create WebSocket service for connection management in book-source/src/services/websocket.ts
- [ ] T080 [US2] Implement useAuth hook with signup, login, logout in book-source/src/hooks/useAuth.ts
- [ ] T081 [US2] Add LocalStorage utilities for token persistence in book-source/src/services/storage.ts
- [ ] T082 [US2] Create TypeScript types for streaming messages in book-source/src/types/websocket.ts
```

### 5. Add New User Story 2 Refactor Phase

**ADD**:

```markdown
**Refactor Phase - Agent Optimization**

- [ ] T083 [US2] Optimize OLIVIA agent prompt for faster generation (<5s)
- [ ] T084 [US2] Add error recovery in streaming (handle disconnections)
- [ ] T085 [US2] Implement conversation memory cleanup (delete old messages >7)
- [ ] T086 [US2] Add telemetry for agent performance monitoring
- [ ] T087 [US2] Optimize RAG retrieval (reduce ChromaDB query time)
```

### 6. Update User Story 3 Tasks (Action Buttons)

**UPDATE T103-T110 to use WebSocket**:

```markdown
**Backend: OLIVIA Agent Actions (US3)**

- [ ] T103 [US3] Configure OLIVIA agent for 4 action types (Explain/MainPoints/Example/AskTutor) in Tutor-Agent/src/tutor_agent/services/agent/action_handler.py
- [ ] T104 [US3] Implement action-specific prompts for each button in Tutor-Agent/src/tutor_agent/services/agent/prompts/actions.py
- [ ] T105 [US3] Add highlighted text context to agent tools in Tutor-Agent/src/tutor_agent/services/agent/tools/get_highlighted_text.py
- [ ] T106 [US3] Implement WebSocket /ws/action with action type parameter in Tutor-Agent/src/tutor_agent/api/v1/websocket.py
- [ ] T107 [US3] Add conversation tracking for action responses (append to history) in ConversationService
- [ ] T108 [US3] Create ActionResponse model (user_id, action_type, input_text, response, timestamp) in Tutor-Agent/src/tutor_agent/models/action.py
```

### 7. Update User Story 4 Tasks (Sidebar Chat)

**UPDATE T118-T125 to use WebSocket**:

```markdown
**Backend: OLIVIA Agent Chat (US4)**

- [ ] T118 [US4] Configure OLIVIA agent for conversational chat mode in Tutor-Agent/src/tutor_agent/services/agent/chat_handler.py
- [ ] T119 [US4] Implement chat-specific prompts with conversation continuity in Tutor-Agent/src/tutor_agent/services/agent/prompts/chat.py
- [ ] T120 [US4] Add RAG search with semantic similarity for chat questions in OLIVIA chat tools
- [ ] T121 [US4] Implement WebSocket /ws/chat with bi-directional messaging in Tutor-Agent/src/tutor_agent/api/v1/websocket.py
- [ ] T122 [US4] Add typing indicators via WebSocket events in WebSocketManager
- [ ] T123 [US4] Implement conversation persistence (save all messages) in ConversationService
- [ ] T124 [US4] Create ChatMessage model with references to book pages in Tutor-Agent/src/tutor_agent/models/chat.py
```

---

## 📝 NEW TASK SUMMARY

### Total New Tasks Added: ~30
### Tasks Modified: ~15
### Architecture: Simple API → RAG Agent + WebSocket Streaming

### Key Changes:
1. ✅ OLIVIA AI Agent (OpenAI Agents SDK) instead of simple API
2. ✅ RAG search tool queries ChromaDB embeddings
3. ✅ WebSocket streaming for live "Generating..." UX
4. ✅ Conversation memory (last 7 messages)
5. ✅ Six-Step Prompting Framework (ACILPR)
6. ✅ Dual-purpose agent (personalized content + chat)

### Dependencies Flow:
```
Phase 2 (Foundational) → MUST complete OLIVIA agent + WebSocket
    ↓
Phase 3 (US1) → Summaries (unchanged)
    ↓
Phase 4 (US2) → Personalized content (uses OLIVIA + WebSocket)
    ↓
Phase 5 (US3) → Action buttons (uses OLIVIA + WebSocket)
    ↓
Phase 6 (US4) → Chat (uses OLIVIA + WebSocket)
```

---

## 🔧 IMPLEMENTATION NOTES

### For Next Developer:

1. **Read Skills First**:
   - `C:\Users\USER\.claude\skills\openai-agents-expert.md`
   - `C:\Users\USER\.claude\skills\Prompt-&-Context-Engineering-Skill.md`

2. **ChromaDB Embeddings**:
   - Location: `Tutor-Agent/data/embeddings/` ✅ Already copied
   - Size: 19MB
   - Collection ID: `d69c732b-0a21-4f5b-a437-47cea526907e`

3. **WebSocket vs REST**:
   - Use WebSocket for streaming (personalized content, actions, chat)
   - Use REST for auth, profile, static summaries
   - JWT in WebSocket query params: `/ws/chat?token=...`

4. **Testing Strategy**:
   - Mock ChromaDB in unit tests
   - Mock OpenAI in unit tests
   - Use real ChromaDB in integration tests
   - Use real OpenAI (with rate limits) in E2E tests

5. **Performance Targets**:
   - Personalized content: <5s first generation, <200ms cached
   - Action buttons: <3s response time
   - Chat: <2s per message
   - RAG search: <500ms query time

---

**Apply these changes to specs/001-tutorgpt-platform/tasks.md**
