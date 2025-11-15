# TutorGPT Constitution

## Mission Statement

**TutorGPT transforms static documentation into intelligent, personalized learning experiences.**

Every learner deserves an AI tutor that understands their unique background, adapts content to their experience level, responds instantly to questions, guides them through complex concepts, and celebrates their progress.

---

## Core Principles

### I. Learner-First Always (NON-NEGOTIABLE)

**Every decision serves the learner's success.**

- User experience takes priority over technical complexity
- Features must solve real learning problems
- Interface should feel intuitive, not intimidating
- Performance must be fast enough to maintain flow state
- Errors should be helpful, not frustrating

**NOT:**
- Building features because they're technically interesting
- Optimizing for developer convenience over user needs
- Adding complexity that confuses learners
- Accepting slow performance that breaks concentration

### II. Test-Driven Development (TDD) MANDATORY

**All code development follows TDD methodology - NO EXCEPTIONS.**

**TDD Cycle (Red-Green-Refactor):**
- **RED:** Write failing test that describes desired behavior
- **GREEN:** Write minimal code to make the test pass
- **REFACTOR:** Clean up code while keeping tests green
- **REPEAT:** Continue cycle for next feature/behavior

**Quality Gates:**
- Minimum 90% test coverage required
- Tests must run quickly (< 30 seconds full suite)
- Tests must be deterministic and stable
- Clear test names and descriptions
- Keep tests simple and focused

**Application Areas:**
- API Endpoints: Test request/response before implementation
- Agent Responses: Test agent behavior with various inputs
- Database Operations: Test data persistence and retrieval
- WebSocket Communication: Test real-time message flow
- Content Generation: Test personalization logic and outputs
- Authentication: Test security and user management flows

### III. Agent-First Architecture

**AI capabilities drive the technical architecture.**

- **Context-Aware:** Agent has access to all relevant user and content context
- **Stateful Conversations:** Maintain understanding across interactions
- **Proactive Intelligence:** Agent can initiate helpful interactions
- **Autonomous Decisions:** Agent chooses best teaching approach
- **Learning Capability:** System improves through user interactions
- **Test-Driven Agent Development:** All agent logic thoroughly tested

### IV. Personalization Without Burden

**The system learns about users by observing, not asking.**

- Minimal signup questions (only 4 essential ones)
- Agent adapts based on interaction patterns
- Learning preferences inferred from behavior
- Progressive personalization that improves over time
- Transparent about how personalization works

**NOT:**
- Overwhelming users with long surveys
- Requiring manual configuration of preferences
- Black-box personalization without explanation
- Personalization that feels intrusive

### V. Real-Time by Default

**Interactions feel live and responsive.**

- **WebSocket Foundation:** Real-time communication as primary interface
- **Streaming Responses:** Long responses stream as they generate
- **Live Status:** Show connection status and agent activity
- **Instant Feedback:** Immediate response to user actions
- **Background Processing:** Heavy operations don't block interface

### VI. Performance as Feature

**Speed and reliability are core features, not afterthoughts.**

**Performance Standards:**
- Summary tabs load instantly (under 200ms)
- Chat responses feel conversational (under 4 seconds)
- WebSocket connections are stable and reliable
- Personalized content generates within reasonable time
- System gracefully handles high concurrent load

**NOT:**
- Accepting slow performance as "good enough"
- Building features without considering performance impact
- Leaving optimization for "later"
- Ignoring user frustration with loading times

### VII. Content Integrity and Accuracy

**Generated content preserves technical accuracy while enhancing understanding.**

- Personalized content maintains factual correctness
- Agent explanations align with source material
- Code examples are runnable and best-practice
- Language translation preserves technical meaning
- Sources are clearly attributed and traceable

**NOT:**
- Simplifying content to the point of inaccuracy
- Adding personal opinions or biased interpretations
- Generating code that doesn't work
- Translating in ways that change technical meaning

### VIII. Privacy and Transparency

**Users control their data and understand how it's used.**

- Clear explanation of data collection and use
- User consent for personalization features
- Option to delete account and all data
- Transparent about AI model usage and limitations
- Secure handling of all personal information

---

## Technology Stack Requirements

### Required Technologies
- **Backend:** Python 3.11+ with OpenAI Agents SDK
- **API Framework:** FastAPI with async/await
- **Real-time:** WebSockets for live communication
- **Agent Framework:** OpenAI Agents SDK with MCP integration
- **Testing:** pytest with async support, 90%+ coverage
- **Package Management:** UV for dependency management

### Architecture Patterns
- **Agent Pattern:** Orchestrator + Specialist agents (teaching, summarization, Q&A)
- **Communication:** WebSocket-first with RESTful fallback
- **State Management:** Context-aware with memory persistence
- **Error Handling:** Graceful degradation with helpful messages

### AI Agent Principles (MANDATORY)

**All AI Interactions MUST Use OpenAI Agents SDK**
- ❌ **NEVER** use simple `openai.chat.completions.create()` calls
- ✅ **ALWAYS** use OpenAI Agents SDK with tools, handoffs, and structured outputs
- ✅ Agents MUST have tools, memory, and streaming capabilities

**RAG Requirements (Retrieval-Augmented Generation)**
- ALL content generation MUST use RAG (not hallucination)
- ChromaDB embeddings are the source of truth for book content
- Agent MUST search embeddings before generating responses
- Responses MUST include source attribution where applicable

**Streaming Responses (Real-Time Communication)**
- ALL agent responses MUST stream (not blocking)
- Frontend MUST show "Generating..." state during streaming
- Use `Runner.stream()` for async streaming
- WebSocket is the primary communication channel

**Conversation Memory (Context Preservation)**
- Remember last 7 messages per user (stored in database)
- Include conversation history in agent context on each request
- Store in `conversation_messages` table with user_id + timestamps
- Memory retrieval MUST be fast (<50ms)

**Agent Tools (Mandatory for OLIVIA)**

Every agent MUST have at minimum these three tools:

1. **RAG Search Tool** (`search_book_content`)
   - Queries ChromaDB for relevant content
   - Supports scoped search (page/chapter/book)
   - Returns top-k chunks with metadata and source attribution

2. **User Profile Retrieval Tool** (`get_user_profile`)
   - Fetches user's 4-question profile
   - Programming experience, AI experience, learning style, language
   - Used for content personalization

3. **Conversation History Tool** (`get_conversation_history`)
   - Retrieves last 7 messages for context
   - Enables conversation continuity
   - Prevents repetitive responses

**Six-Step Prompting Framework (ACILPR)**

All agent prompts MUST follow this structure:

1. **Actor**: Define who the agent is (e.g., "You are OLIVIA, an AI tutor...")
2. **Context**: Provide user profile + current page + conversation history
3. **Instruction**: Clearly state what needs to be done
4. **Limitations**: Define constraints and boundaries
5. **Persona**: Set communication style based on user level
6. **Response Format**: Specify output structure (markdown, JSON, etc.)

**Performance Targets**
- RAG search: <500ms
- Personalized content generation: <5s (first), <200ms (cached)
- Action button responses: <3s
- Chat responses: <4s
- WebSocket connection: <1s

---

## Development Workflow

### Feature Development Process

1. **Specification First**
   - Write clear `spec.md` defining WHAT we're building
   - Include user stories, success criteria, constraints
   - Get approval before proceeding

2. **Planning Phase**
   - Create `plan.md` defining HOW we'll build it
   - Architecture decisions with rationale
   - Technology choices with tradeoffs
   - ADR creation for significant decisions

3. **Task Breakdown**
   - Generate `tasks.md` with testable tasks
   - Each task has acceptance criteria
   - Include test cases for validation
   - Dependency ordering

4. **TDD Implementation**
   - **RED:** Write failing test first
   - **GREEN:** Implement minimal code to pass
   - **REFACTOR:** Clean up while tests stay green
   - **COMMIT:** Small, atomic commits with clear messages

5. **Quality Gates**
   - All tests passing (90%+ coverage)
   - Code passes linting (ruff, black, mypy)
   - Performance benchmarks met
   - Security checks passed
   - Documentation updated

### Code Review Requirements
- All changes require peer review
- Tests must be included with code
- Performance impact assessed
- Security implications considered
- Documentation updated

---

## Quality Standards

### Functional Quality
- Features work correctly and reliably
- Agent responses are factually correct
- Same inputs produce consistent outputs
- Graceful error handling
- Cross-platform compatibility

### Performance Quality
- Chat responses under 4 seconds
- Summary generation under 200ms
- 99.9% uptime with graceful recovery
- Supports 100+ concurrent learners
- Optimal resource usage

### User Experience Quality
- Intuitive navigation without explanation
- Clean, modern design that aids comprehension
- Accessible (screen readers, keyboard navigation)
- Mobile-friendly responsive design
- Clear guidance when errors occur

### Content Quality
- Technical information is correct and up-to-date
- Explanations are clear at appropriate level
- Topics covered thoroughly without overwhelming
- Code samples work and illustrate concepts
- Content respects diverse backgrounds

---

## Governance

### Constitutional Authority
- This constitution supersedes all other development practices
- All features, code, and decisions must align with these principles
- Deviations require documented justification and approval
- Amendments require team consensus and version update

### Enforcement
- All PRs must demonstrate compliance with principles
- Code reviews verify adherence to TDD and quality standards
- Architecture decisions must align with Agent-First principle
- Performance benchmarks must be met before merge
- Learner-First principle guides all feature prioritization

### Amendment Process
- Proposals must be documented with rationale
- Team discussion and consensus required
- Impact assessment on existing systems
- Version increment and changelog update
- Communication to all stakeholders

---

**Version**: 1.1.0 | **Ratified**: 2025-11-14 | **Last Amended**: 2025-11-15

---

*"The best teacher is one who suggests rather than dogmatizes, and inspires their listener with the wish to teach themselves." - Edward Bulwer-Lytton*

*"In the age of AI, the greatest teaching tool is one that adapts to each student's mind." - TutorGPT Team*
