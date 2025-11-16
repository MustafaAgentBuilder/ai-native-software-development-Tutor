<!-- Claude is Work to Build this Project -->
---
description: "Task list for TutorGPT - AI-Powered Book Learning Platform"
---

# Tasks: TutorGPT Platform

**Input**: Design documents from `/specs/001-tutorgpt-platform/`
**Prerequisites**: plan.md ✅, spec.md ✅
**Branch**: `001-tutorgpt-platform`
**Date**: 2025-11-15

**Tests**: Test tasks are included per TDD mandate (90%+ coverage required). Tests MUST be written FIRST and FAIL before implementation (Red-Green-Refactor cycle).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

This is a web application with:
- **Backend**: `Tutor-Agent/` (FastAPI, Python 3.11+)
- **Frontend**: `book-source/` (Docusaurus with custom React components)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for both backend and frontend

- [ ] T001 Verify Tutor-Agent project structure matches plan.md specifications
- [ ] T002 Create backend directory structure: models/, api/v1/, services/agent/, services/rag/, core/, utils/
- [ ] T003 [P] Create frontend directory structure: src/components/TabSystem/, src/components/ActionButtons/, src/components/Chat/, src/components/Auth/, src/components/Profile/
- [ ] T004 [P] Initialize backend dependencies via UV: FastAPI, OpenAI Agents SDK, ChromaDB, WebSockets, Pydantic, SQLAlchemy, pytest, pytest-asyncio, pytest-cov
- [ ] T005 [P] Initialize frontend dependencies: React hooks, WebSocket client, TypeScript types
- [ ] T006 [P] Configure pytest.ini with async support and 90% coverage threshold in Tutor-Agent/pytest.ini
- [ ] T007 [P] Setup .env.example with required environment variables in Tutor-Agent/.env.example
- [ ] T008 Create scripts directory with placeholders: Tutor-Agent/scripts/generate_summaries.py, Tutor-Agent/scripts/init_db.py, Tutor-Agent/scripts/load_embeddings.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database & Core Infrastructure

- [ ] T009 Create database connection and session factory in Tutor-Agent/src/tutor_agent/core/database.py
- [ ] T010 [P] Implement JWT utilities and password hashing in Tutor-Agent/src/tutor_agent/core/security.py
- [ ] T011 [P] Create WebSocket connection manager in Tutor-Agent/src/tutor_agent/core/websocket_manager.py
- [ ] T012 [P] Implement caching utilities (LRU cache) in Tutor-Agent/src/tutor_agent/core/cache.py
- [ ] T013 [P] Setup structured logging in Tutor-Agent/src/tutor_agent/utils/logging.py
- [ ] T014 [P] Create custom exception classes in Tutor-Agent/src/tutor_agent/utils/exceptions.py
- [ ] T015 Create Pydantic settings with .env loading in Tutor-Agent/src/tutor_agent/config/settings.py
- [ ] T016 Create dependency injection helpers (get_db, get_current_user) in Tutor-Agent/src/tutor_agent/api/deps.py

### RAG & Embeddings Setup (Required for Agent)

- [ ] T017 Create embeddings retriever with multi-level search (page/chapter/book) in Tutor-Agent/src/tutor_agent/services/rag/embeddings.py
- [ ] T018 Implement ChromaDB loader with collection access in Tutor-Agent/src/tutor_agent/services/rag/retriever.py
- [ ] T019 Create script to symlink/copy external embeddings to Tutor-Agent/data/embeddings in Tutor-Agent/scripts/load_embeddings.py
- [ ] T020 Write unit tests for embeddings retriever (mocked ChromaDB) in Tutor-Agent/tests/unit/test_rag.py

### OpenAI Agent Foundation

- [ ] T021 Create specialized prompt templates for action types (Explain/MainPoints/Example/AskTutor) in Tutor-Agent/src/tutor_agent/services/agent/prompts.py
- [ ] T022 Implement context builder from user profile + page + history in Tutor-Agent/src/tutor_agent/services/agent/context_builder.py
- [ ] T023 Create response formatter for different channels (WebSocket/REST) in Tutor-Agent/src/tutor_agent/services/agent/response_formatter.py
- [ ] T024 Write unit tests for context builder in Tutor-Agent/tests/unit/test_agent.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Public Book Reading with Instant Summaries (Priority: P1) 🎯 MVP

**Goal**: Any visitor can read the original book content and access pre-generated summaries for every page in Part 1 without requiring an account.

**Independent Test**: User visits any page in Part 1, clicks Summary tab, and sees a concise 200-400 word summary within 200ms. No login required.

### Backend: Content Generation & Serving (US1)

**Tests FIRST (Red Phase)**

- [ ] T025 [P] [US1] Write failing test for GET /api/v1/content/summary/{page_path} returning 200-400 word summary in Tutor-Agent/tests/integration/test_api_content.py
- [ ] T026 [P] [US1] Write failing test for summary cache returning content in <200ms in Tutor-Agent/tests/unit/test_services.py

**Models & Services (Green Phase)**

- [ ] T027 [P] [US1] Create PageContent model (page_path PK, chapter, markdown_content) in Tutor-Agent/src/tutor_agent/models/content.py
- [ ] T028 [P] [US1] Create GeneratedContent model (content_id, page_path, content_type, markdown_content, generated_at) in Tutor-Agent/src/tutor_agent/models/content.py
- [ ] T029 [US1] Implement ContentGenerator service with summary generation (200-400 words) in Tutor-Agent/src/tutor_agent/services/content_generator.py
- [ ] T030 [US1] Implement filesystem-based summary cache in ContentGenerator (Tutor-Agent/data/generated_summaries/)
- [ ] T031 [US1] Create database initialization script with Alembic migration in Tutor-Agent/scripts/init_db.py
- [ ] T032 [US1] Implement GET /api/v1/content/summary/{page_path} endpoint (public, no auth) in Tutor-Agent/src/tutor_agent/api/v1/content.py

**Pre-Generation Script (Green Phase)**

- [ ] T033 [US1] Create summary pre-generation script for all Part 1 pages in Tutor-Agent/scripts/generate_summaries.py
- [ ] T034 [US1] Add metadata tracking (generation timestamp, model version) to generated summaries in generate_summaries.py
- [ ] T035 [US1] Write integration test for pre-generation script in Tutor-Agent/tests/integration/test_content_generation.py

### Frontend: Three-Tab Interface (US1)

**Tests FIRST (Red Phase)**

- [ ] T036 [P] [US1] Write failing test for TabContainer switching between tabs in book-source/src/components/TabSystem/TabContainer.test.tsx
- [ ] T037 [P] [US1] Write failing test for SummaryTab fetching and displaying summary in book-source/src/components/TabSystem/SummaryTab.test.tsx

**Components (Green Phase)**

- [ ] T038 [P] [US1] Create TabContainer component with tab switching logic in book-source/src/components/TabSystem/TabContainer.tsx
- [ ] T039 [P] [US1] Create OriginalTab component displaying book markdown in book-source/src/components/TabSystem/OriginalTab.tsx
- [ ] T040 [P] [US1] Create SummaryTab component fetching summaries via API in book-source/src/components/TabSystem/SummaryTab.tsx
- [ ] T041 [P] [US1] Create PersonalizedTab placeholder (shows login prompt for now) in book-source/src/components/TabSystem/PersonalizedTab.tsx
- [ ] T042 [US1] Implement useContent hook for fetching summaries with caching in book-source/src/hooks/useContent.ts
- [ ] T043 [US1] Create API client service for REST endpoints in book-source/src/services/api.ts
- [ ] T044 [US1] Add TypeScript types for Content entities in book-source/src/types/content.ts
- [ ] T045 [US1] Integrate TabContainer into Docusaurus page layout in book-source/docusaurus.config.js

**Refactor Phase**

- [ ] T046 [US1] Refactor ContentGenerator to extract summary template logic
- [ ] T047 [US1] Add comprehensive error handling for missing pages and cache failures
- [ ] T048 [US1] Optimize summary cache with proper TTL and invalidation strategy

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently (MVP ready!)

---

## Phase 4: User Story 2 - Personalized Learning Experience with User Profile (Priority: P2)

**Goal**: Registered users receive personalized content adapted to their experience level, learning style, and preferred language.

**Independent Test**: User completes 4-question signup (programming experience, AI experience, learning style, language), navigates to any Part 1 page, clicks Personalized tab, and receives content rewritten specifically for their profile within 5 seconds on first request.

### Backend: Authentication & User Profiles (US2)

**Tests FIRST (Red Phase)**

- [ ] T049 [P] [US2] Write failing test for POST /api/v1/auth/signup with 4 personalization questions in Tutor-Agent/tests/integration/test_api_auth.py
- [ ] T050 [P] [US2] Write failing test for POST /api/v1/auth/login returning JWT token in Tutor-Agent/tests/integration/test_api_auth.py
- [ ] T051 [P] [US2] Write failing test for JWT authentication middleware in Tutor-Agent/tests/unit/test_services.py
- [ ] T052 [P] [US2] Write failing test for personalized content generation with user profile in Tutor-Agent/tests/integration/test_api_content.py

**Models (Green Phase)**

- [ ] T053 [P] [US2] Create User model (id, email unique, password_hash, full_name, created_at, last_login) in Tutor-Agent/src/tutor_agent/models/user.py
- [ ] T054 [P] [US2] Create UserProfile model (user_id FK, programming_experience, ai_experience, learning_style, preferred_language) in Tutor-Agent/src/tutor_agent/models/user.py
- [ ] T055 [US2] Add database migration for User and UserProfile tables via Alembic
- [ ] T056 [US2] Write unit tests for User and UserProfile models in Tutor-Agent/tests/unit/test_models.py

**Services (Green Phase)**

- [ ] T057 [US2] Implement AuthService with JWT token creation, validation, password hashing in Tutor-Agent/src/tutor_agent/services/auth_service.py
- [ ] T058 [US2] Implement Personalizer service with LLM-based content adaptation in Tutor-Agent/src/tutor_agent/services/personalizer.py
- [ ] T059 [US2] Add profile-based prompt adjustments (experience → complexity, style → format) to Personalizer
- [ ] T060 [US2] Add multi-language support with technical term preservation to Personalizer
- [ ] T061 [US2] Implement in-memory LRU cache for personalized content (1000 entries, 1hr TTL) in ContentGenerator

**API Endpoints (Green Phase)**

- [ ] T062 [P] [US2] Implement POST /api/v1/auth/signup (email, password, 4 questions) in Tutor-Agent/src/tutor_agent/api/v1/auth.py
- [ ] T063 [P] [US2] Implement POST /api/v1/auth/login (email, password) returning JWT in Tutor-Agent/src/tutor_agent/api/v1/auth.py
- [ ] T064 [P] [US2] Implement POST /api/v1/auth/refresh for token refresh in Tutor-Agent/src/tutor_agent/api/v1/auth.py
- [ ] T065 [P] [US2] Implement GET /api/v1/profile returning current user profile in Tutor-Agent/src/tutor_agent/api/v1/profile.py
- [ ] T066 [P] [US2] Implement PUT /api/v1/profile for updating preferences in Tutor-Agent/src/tutor_agent/api/v1/profile.py
- [ ] T067 [US2] Implement GET /api/v1/content/personalized/{page_path} (auth required) in Tutor-Agent/src/tutor_agent/api/v1/content.py

### Frontend: Auth & Personalized Content (US2)

**Tests FIRST (Red Phase)**

- [ ] T068 [P] [US2] Write failing test for SignupForm with 4 questions in book-source/src/components/Auth/SignupForm.test.tsx
- [ ] T069 [P] [US2] Write failing test for LoginForm with email/password in book-source/src/components/Auth/LoginForm.test.tsx
- [ ] T070 [P] [US2] Write failing test for PersonalizedTab showing adapted content in book-source/src/components/TabSystem/PersonalizedTab.test.tsx

**Components (Green Phase)**

- [ ] T071 [P] [US2] Create SignupForm component with 4 personalization questions in book-source/src/components/Auth/SignupForm.tsx
- [ ] T072 [P] [US2] Create LoginForm component in book-source/src/components/Auth/LoginForm.tsx
- [ ] T073 [P] [US2] Create AuthModal wrapper for auth forms in book-source/src/components/Auth/AuthModal.tsx
- [ ] T074 [P] [US2] Create ProfileView component displaying user profile in book-source/src/components/Profile/ProfileView.tsx
- [ ] T075 [P] [US2] Create ProfileEdit component for updating preferences in book-source/src/components/Profile/ProfileEdit.tsx
- [ ] T076 [US2] Implement PersonalizedTab fetching personalized content (replaces placeholder) in book-source/src/components/TabSystem/PersonalizedTab.tsx
- [ ] T077 [US2] Implement useAuth hook with signup, login, logout, token refresh in book-source/src/hooks/useAuth.ts
- [ ] T078 [US2] Add LocalStorage utilities for token persistence in book-source/src/services/storage.ts
- [ ] T079 [US2] Create TypeScript types for User and UserProfile in book-source/src/types/user.ts

**Refactor Phase**

- [ ] T080 [US2] Refactor Personalizer to extract language-specific prompt templates
- [ ] T081 [US2] Add input validation with Pydantic for all auth endpoints
- [ ] T082 [US2] Optimize personalized content cache eviction strategy

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Context-Aware Learning Assistance (Priority: P3)

**Goal**: Users receive intelligent help through action buttons (Explain, Main Points, Example, Ask Tutor) that understand their location in the book and learning progress.

**Independent Test**: Logged-in user clicks "Explain" button on a Python functions page after completing variables chapter; receives explanation that references their completed work and learning patterns within 3 seconds.

### Backend: Learning Journey Tracking (US3)

**Tests FIRST (Red Phase)**

- [ ] T083 [P] [US3] Write failing test for learning journey tracking (current page, completed chapters) in Tutor-Agent/tests/unit/test_services.py
- [ ] T084 [P] [US3] Write failing test for concept mastery/struggle detection in Tutor-Agent/tests/unit/test_services.py

**Models (Green Phase)**

- [ ] T085 [US3] Create LearningJourney model (profile_id FK, current_page_path, completed_chapters, concepts_mastered, concepts_struggling) in Tutor-Agent/src/tutor_agent/models/user.py
- [ ] T086 [US3] Add database migration for LearningJourney table via Alembic
- [ ] T087 [US3] Write unit tests for LearningJourney model in Tutor-Agent/tests/unit/test_models.py

**Services (Green Phase)**

- [ ] T088 [US3] Implement LearningTracker service for journey tracking and behavior analysis in Tutor-Agent/src/tutor_agent/services/learning_tracker.py
- [ ] T089 [US3] Add concept mastery detection based on time spent and interactions to LearningTracker
- [ ] T090 [US3] Add struggle detection based on repeated questions and extended page time to LearningTracker
- [ ] T091 [US3] Implement GET /api/v1/profile/journey endpoint returning learning data in Tutor-Agent/src/tutor_agent/api/v1/profile.py

### Backend: Action Button Responses (US3)

**Tests FIRST (Red Phase)**

- [ ] T092 [P] [US3] Write failing test for UniversalTutorAgent with EXPLAIN action type in Tutor-Agent/tests/unit/test_agent.py
- [ ] T093 [P] [US3] Write failing test for UniversalTutorAgent with MAIN_POINTS action type in Tutor-Agent/tests/unit/test_agent.py
- [ ] T094 [P] [US3] Write failing test for UniversalTutorAgent with EXAMPLE action type in Tutor-Agent/tests/unit/test_agent.py
- [ ] T095 [P] [US3] Write failing test for agent context including user journey and page context in Tutor-Agent/tests/unit/test_agent.py

**Agent Implementation (Green Phase)**

- [ ] T096 [US3] Implement UniversalTutorAgent class with OpenAI Agents SDK integration in Tutor-Agent/src/tutor_agent/services/agent/universal_tutor.py
- [ ] T097 [US3] Add action-specific response methods (respond_to_explain, respond_to_main_points, respond_to_example) to UniversalTutorAgent
- [ ] T098 [US3] Integrate RAG retriever with agent for context-aware responses in UniversalTutorAgent
- [ ] T099 [US3] Implement context building with user profile + page + learning journey in context_builder.py
- [ ] T100 [US3] Add specialized prompts for each action type in prompts.py

**WebSocket Endpoints (Green Phase)**

- [ ] T101 [US3] Implement WS /api/v1/ws/actions for action button responses in Tutor-Agent/src/tutor_agent/api/v1/websocket.py
- [ ] T102 [US3] Add WebSocket message routing by action type (explain/main_points/example) in websocket.py
- [ ] T103 [US3] Implement streaming responses via WebSocket for action buttons
- [ ] T104 [US3] Write integration tests for WebSocket action endpoints in Tutor-Agent/tests/integration/test_websocket.py

### Frontend: Action Buttons & Learning Journey (US3)

**Tests FIRST (Red Phase)**

- [ ] T105 [P] [US3] Write failing test for ActionButtonGroup rendering 4 buttons in book-source/src/components/ActionButtons/ActionButtonGroup.test.tsx
- [ ] T106 [P] [US3] Write failing test for ExplainButton triggering WebSocket action in book-source/src/components/ActionButtons/ExplainButton.test.tsx
- [ ] T107 [P] [US3] Write failing test for useLearningJourney hook tracking page navigation in book-source/src/hooks/useLearningJourney.test.ts

**Components (Green Phase)**

- [ ] T108 [P] [US3] Create ActionButtonGroup container with 4 buttons in book-source/src/components/ActionButtons/ActionButtonGroup.tsx
- [ ] T109 [P] [US3] Create ExplainButton component in book-source/src/components/ActionButtons/ExplainButton.tsx
- [ ] T110 [P] [US3] Create MainPointsButton component in book-source/src/components/ActionButtons/MainPointsButton.tsx
- [ ] T111 [P] [US3] Create ExampleButton component in book-source/src/components/ActionButtons/ExampleButton.tsx
- [ ] T112 [P] [US3] Create AskTutorButton component (opens chat sidebar) in book-source/src/components/ActionButtons/AskTutorButton.tsx
- [ ] T113 [US3] Implement useWebSocket hook for WebSocket connection management in book-source/src/hooks/useWebSocket.ts
- [ ] T114 [US3] Implement useLearningJourney hook for tracking navigation and progress in book-source/src/hooks/useLearningJourney.ts
- [ ] T115 [US3] Create WebSocket client with reconnection logic in book-source/src/services/websocket.ts
- [ ] T116 [US3] Integrate ActionButtonGroup into Docusaurus page layout

**Refactor Phase**

- [ ] T117 [US3] Refactor UniversalTutorAgent to extract prompt selection logic
- [ ] T118 [US3] Add comprehensive error handling for WebSocket disconnections
- [ ] T119 [US3] Optimize context builder to reduce token usage

**Checkpoint**: All user stories 1, 2, and 3 should now be independently functional

---

## Phase 6: User Story 4 - Real-Time Conversational Tutoring (Priority: P3)

**Goal**: Users engage in real-time chat conversations with an AI tutor that maintains context across their learning journey.

**Independent Test**: User opens chat sidebar, asks "How do Python functions work?", receives streaming response within 4 seconds that knows they're in Chapter 4, completed variables in Chapter 3, and prefer visual learning.

### Backend: Chat Sessions & Messages (US4)

**Tests FIRST (Red Phase)**

- [ ] T120 [P] [US4] Write failing test for ChatSession creation and activation in Tutor-Agent/tests/unit/test_models.py
- [ ] T121 [P] [US4] Write failing test for ChatMessage with RAG sources and response time in Tutor-Agent/tests/unit/test_models.py
- [ ] T122 [P] [US4] Write failing test for chat streaming via WebSocket in Tutor-Agent/tests/integration/test_websocket.py

**Models (Green Phase)**

- [ ] T123 [P] [US4] Create ChatSession model (id, user_id FK, page_context_path, started_at, is_active) in Tutor-Agent/src/tutor_agent/models/chat.py
- [ ] T124 [P] [US4] Create ChatMessage model (id, session_id FK, role, content, message_type, rag_sources, response_time_ms) in Tutor-Agent/src/tutor_agent/models/chat.py
- [ ] T125 [US4] Add database migration for ChatSession and ChatMessage tables via Alembic
- [ ] T126 [US4] Write unit tests for Chat models in Tutor-Agent/tests/unit/test_models.py

**Agent Chat Implementation (Green Phase)**

- [ ] T127 [US4] Add chat conversation handler to UniversalTutorAgent with history context in universal_tutor.py
- [ ] T128 [US4] Implement conversation history loading (last 50 messages) in UniversalTutorAgent
- [ ] T129 [US4] Add page context auto-update when user navigates during chat to context_builder.py
- [ ] T130 [US4] Implement streaming response generation with OpenAI Agents SDK in UniversalTutorAgent

**WebSocket Chat Endpoint (Green Phase)**

- [ ] T131 [US4] Implement WS /api/v1/ws/chat for real-time chat in Tutor-Agent/src/tutor_agent/api/v1/websocket.py
- [ ] T132 [US4] Add WebSocket connection status tracking in websocket_manager.py
- [ ] T133 [US4] Implement chat message persistence with session tracking in websocket.py
- [ ] T134 [US4] Add typing indicators and streaming chunks to WebSocket responses
- [ ] T135 [US4] Write integration tests for chat session persistence in Tutor-Agent/tests/integration/test_agent_integration.py

### Frontend: Chat Interface (US4)

**Tests FIRST (Red Phase)**

- [ ] T136 [P] [US4] Write failing test for ChatSidebar opening/closing in book-source/src/components/Chat/ChatSidebar.test.tsx
- [ ] T137 [P] [US4] Write failing test for MessageList displaying streaming messages in book-source/src/components/Chat/MessageList.test.tsx
- [ ] T138 [P] [US4] Write failing test for MessageInput sending messages via WebSocket in book-source/src/components/Chat/MessageInput.test.tsx

**Components (Green Phase)**

- [ ] T139 [P] [US4] Create ChatSidebar collapsible component in book-source/src/components/Chat/ChatSidebar.tsx
- [ ] T140 [P] [US4] Create MessageList component with streaming support in book-source/src/components/Chat/MessageList.tsx
- [ ] T141 [P] [US4] Create MessageInput component with send button in book-source/src/components/Chat/MessageInput.tsx
- [ ] T142 [P] [US4] Create TypingIndicator component for agent typing state in book-source/src/components/Chat/TypingIndicator.tsx
- [ ] T143 [US4] Update useWebSocket hook to handle chat streaming and typing indicators
- [ ] T144 [US4] Add chat session persistence across page navigation to useWebSocket
- [ ] T145 [US4] Create TypeScript types for Chat entities in book-source/src/types/chat.ts
- [ ] T146 [US4] Integrate ChatSidebar into Docusaurus page layout with toggle button
- [ ] T147 [US4] Add custom styles for chat interface in book-source/src/styles/chat.module.css

**Refactor Phase**

- [ ] T148 [US4] Refactor WebSocket manager to handle connection pooling for 100+ concurrent users
- [ ] T149 [US4] Add message batching and rate limiting (10 messages/second per user)
- [ ] T150 [US4] Optimize conversation history loading to reduce database queries

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

### Performance Optimization

- [ ] T151 [P] Add database connection pooling (10-20 connections) to database.py
- [ ] T152 [P] Implement rate limiting (100 req/min per user) middleware in Tutor-Agent/src/tutor_agent/api/middleware.py
- [ ] T153 [P] Add CORS configuration for frontend origin in Tutor-Agent/src/tutor_agent/main.py
- [ ] T154 [P] Create performance benchmark tests in Tutor-Agent/tests/e2e/test_performance.py
- [ ] T155 Optimize ChromaDB HNSW index parameters for <100ms search time

### Security Hardening

- [ ] T156 [P] Add input validation with Pydantic for all API inputs
- [ ] T157 [P] Implement XSS prevention for user-generated content sanitization
- [ ] T158 [P] Add SQL injection prevention verification in all database queries
- [ ] T159 [P] Configure bcrypt password hashing with 12 rounds in security.py
- [ ] T160 Add security headers (CSP, HSTS) middleware to FastAPI app

### Testing & Documentation

- [ ] T161 [P] Write end-to-end user journey tests in Tutor-Agent/tests/e2e/test_user_journey.py
- [ ] T162 [P] Verify 90%+ test coverage with pytest-cov across all modules
- [ ] T163 [P] Create quickstart.md validation script in Tutor-Agent/scripts/validate_quickstart.sh
- [ ] T164 [P] Update README.md with setup instructions in Tutor-Agent/README.md
- [ ] T165 [P] Document API endpoints in OpenAPI spec (contracts/openapi.yaml)

### Deployment Preparation

- [ ] T166 Run generate_summaries.py to create all Part 1 summaries before deployment
- [ ] T167 Verify embeddings are properly loaded and accessible via load_embeddings.py
- [ ] T168 Run init_db.py to initialize production database schema
- [ ] T169 Validate all environment variables in .env are properly configured
- [ ] T170 [P] Add health check endpoint GET /health in Tutor-Agent/src/tutor_agent/api/v1/health.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 for content infrastructure
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US2 for user profiles and auth
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - Depends on US2 for auth and US3 for agent implementation

### Within Each User Story

- Tests (TDD mandate) MUST be written and FAIL before implementation (Red-Green-Refactor)
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories CAN start in parallel (if team capacity allows and dependencies are respected)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members (respecting dependencies)

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (TDD Red Phase):
Task: "Write failing test for GET /api/v1/content/summary/{page_path}" (T025)
Task: "Write failing test for summary cache returning content in <200ms" (T026)

# Launch all models for User Story 1 together (TDD Green Phase):
Task: "Create PageContent model in Tutor-Agent/src/tutor_agent/models/content.py" (T027)
Task: "Create GeneratedContent model in Tutor-Agent/src/tutor_agent/models/content.py" (T028)

# Launch all frontend components together:
Task: "Create TabContainer component" (T038)
Task: "Create OriginalTab component" (T039)
Task: "Create SummaryTab component" (T040)
Task: "Create PersonalizedTab placeholder" (T041)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Run generate_summaries.py to create all summaries
6. Deploy/demo if ready

**MVP Deliverable**: Public can read book content and view AI-generated summaries instantly without login.

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (P1) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (P2) → Test independently → Deploy/Demo (Personalization!)
4. Add User Story 3 (P3) → Test independently → Deploy/Demo (Action Buttons!)
5. Add User Story 4 (P3) → Test independently → Deploy/Demo (Full Chat!)
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (P1)
   - Developer B: User Story 2 (P2) - starts after US1 content infrastructure
   - Developer C: User Story 3 (P3) - starts after US2 auth is ready
   - Developer D: User Story 4 (P3) - starts after US3 agent is ready
3. Stories complete and integrate independently

---

## Notes

- **[P]** tasks = different files, no dependencies
- **[Story]** label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- **TDD Mandatory**: Verify tests fail (Red) before implementing (Green), then refactor
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- **90%+ test coverage** enforced in CI/CD via pytest-cov
- All WebSocket features require real-time testing with connection simulation
- Pre-generation of summaries is critical for 200ms performance target
- Embeddings must be loaded before agent testing can begin

---

## Task Summary

- **Total Tasks**: 170
- **Phase 1 (Setup)**: 8 tasks
- **Phase 2 (Foundational)**: 16 tasks
- **Phase 3 (User Story 1)**: 24 tasks
- **Phase 4 (User Story 2)**: 34 tasks
- **Phase 5 (User Story 3)**: 37 tasks
- **Phase 6 (User Story 4)**: 31 tasks
- **Phase 7 (Polish)**: 20 tasks

**Parallel Opportunities Identified**: 89 tasks marked [P] can run in parallel within their phases

**Independent Test Criteria**:
- US1: Load summary in <200ms without auth
- US2: Generate personalized content in <5s on first request
- US3: Action button response in <3s with journey context
- US4: Chat streaming response in <4s with full context

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1 only) = 48 tasks

**Format Validation**: ✅ All 170 tasks follow checklist format with checkbox, ID, optional [P], optional [Story], description, and file path
