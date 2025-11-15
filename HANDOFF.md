# 🔄 Development Handoff Document - TutorGPT Personalized Learning

**Date**: 2025-11-15
**Feature**: User Story 2 - Personalized Learning Experience
**Status**: Backend Complete ✅ | Frontend Pending ⏳
**Next Agent**: Continue from "Frontend Implementation"

---

## 📋 Table of Contents
1. [What Was Completed](#what-was-completed)
2. [Architecture Overview](#architecture-overview)
3. [File Structure](#file-structure)
4. [Backend Implementation Details](#backend-implementation-details)
5. [What Needs To Be Done Next](#what-needs-to-be-done-next)
6. [How To Continue](#how-to-continue)
7. [Testing Instructions](#testing-instructions)
8. [API Documentation](#api-documentation)
9. [Important Notes](#important-notes)

---

## ✅ What Was Completed

### Backend (100% Complete)
- ✅ User authentication system (JWT-based)
- ✅ Database models for User and PersonalizedContent
- ✅ 4-question learning profile system
- ✅ Personalized content generation using OpenAI
- ✅ Adaptive prompting based on user profile
- ✅ Content caching with profile-aware invalidation
- ✅ API endpoints: signup, login, me, personalized content
- ✅ Database initialization (SQLite with migration path to PostgreSQL)

### Frontend (0% Complete - THIS IS YOUR TASK)
- ⏳ PersonalizedTab login/signup UI
- ⏳ Signup form with 4 profile questions
- ⏳ JWT token management
- ⏳ API integration
- ⏳ Personalized content display

---

## 🏗️ Architecture Overview

### System Flow
```
User Opens Book Page
    ↓
Clicks "Personalized" Tab
    ↓
NOT LOGGED IN? → Show Login/Signup Form
    ↓
User Fills 4 Questions:
    1. Programming Experience (Beginner/Intermediate/Advanced)
    2. AI/ML Experience (None/Basic/Intermediate/Advanced)
    3. Learning Style (Visual/Practical/Conceptual/Mixed)
    4. Preferred Language (EN/ES/FR/DE/ZH/JA)
    ↓
Backend Creates Account + JWT Token
    ↓
Frontend Stores JWT in localStorage
    ↓
LOGGED IN? → Fetch Personalized Content
    ↓
Backend Checks Cache:
    - Cache Valid? → Return Cached Content
    - Cache Invalid? → Generate New (OpenAI) → Cache → Return
    ↓
Display Personalized Markdown Content
```

### Tech Stack
- **Backend**: FastAPI + SQLAlchemy + OpenAI Agents SDK
- **Frontend**: React + TypeScript + Docusaurus
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Auth**: JWT (7-day expiration)
- **AI**: OpenAI API (gpt-4o-mini) with Six-Step Prompting Framework

---

## 📁 File Structure

### Backend Files (All Complete ✅)
```
Tutor-Agent/
├── src/tutor_agent/
│   ├── main.py                          # FastAPI app entry point
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py                  # Authentication endpoints
│   │       └── content.py               # Content + Personalized endpoints
│   ├── core/
│   │   ├── database.py                  # DB connection & session
│   │   └── security.py                  # JWT + password hashing
│   ├── models/
│   │   └── user.py                      # User & PersonalizedContent models
│   ├── schemas/
│   │   └── auth.py                      # Pydantic request/response schemas
│   └── services/
│       └── personalized_content.py      # OpenAI content generation
├── data/                                # SQLite database directory
├── .env.example                         # Environment variables template
└── pyproject.toml                       # Dependencies

Frontend Files (Need to Create ⏳)
book-source/
├── src/components/
│   └── PersonalizedTab/
│       ├── index.tsx                    # NEEDS UPDATE - Add login/signup
│       ├── LoginForm.tsx                # CREATE THIS - Login form
│       ├── SignupForm.tsx               # CREATE THIS - Signup with 4 questions
│       └── PersonalizedContent.tsx      # CREATE THIS - Display content
└── docs/                                # All lesson .md files (already have tabs)
```

---

## 🔧 Backend Implementation Details

### 1. Database Models (`Tutor-Agent/src/tutor_agent/models/user.py`)

**User Model**:
```python
class User(Base):
    __tablename__ = "users"

    # Authentication
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # 4-Question Learning Profile
    programming_experience = Column(SQLEnum(ProgrammingExperience))  # beginner/intermediate/advanced
    ai_experience = Column(SQLEnum(AIExperience))                    # none/basic/intermediate/advanced
    learning_style = Column(SQLEnum(LearningStyle))                  # visual/practical/conceptual/mixed
    preferred_language = Column(SQLEnum(PreferredLanguage))          # en/es/fr/de/zh/ja

    # Metadata
    full_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Integer, default=1)
```

**PersonalizedContent Model** (Cache):
```python
class PersonalizedContent(Base):
    __tablename__ = "personalized_content"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    page_path = Column(String(500), index=True)          # e.g., "01-Introducing-AI-Driven-Development/..."
    markdown_content = Column(Text)                       # Generated personalized content

    # Profile Snapshot (for cache invalidation)
    programming_experience = Column(SQLEnum(ProgrammingExperience))
    ai_experience = Column(SQLEnum(AIExperience))
    learning_style = Column(SQLEnum(LearningStyle))
    preferred_language = Column(SQLEnum(PreferredLanguage))

    generated_at = Column(DateTime, default=datetime.utcnow)
    model_version = Column(String(50))                    # e.g., "gpt-4o-mini"
```

**Cache Invalidation Logic**:
- Cache is valid ONLY if ALL 4 profile fields match current user profile
- If user changes ANY profile field → cache invalidated → regenerate content

### 2. Authentication System

**JWT Token**:
- Expiration: 7 days
- Payload: `{"sub": "<user_id>", "exp": <timestamp>}`
- Algorithm: HS256
- Secret: From `JWT_SECRET_KEY` environment variable

**Password Security**:
- Hashing: bcrypt (via passlib)
- Minimum length: 8 characters (enforced by Pydantic)

### 3. Personalized Content Generation

**Uses OpenAI Agents SDK + Six-Step Prompting Framework (ACILPR)**:

1. **Actor**: "You are OLIVIA, an AI tutor specializing in AI-Native Software Development"
2. **Context**: User's 4-question profile injected
3. **Instruction**: Adaptive based on experience level
   - Beginner: "Explain from first principles, define all terms"
   - Intermediate: "Build on fundamentals, balance theory/practice"
   - Advanced: "Focus on advanced patterns, assume strong knowledge"
4. **Limitations**: "Keep length similar, preserve code examples, no emojis"
5. **Persona**: Adaptive tone based on level (encouraging/challenging/technical)
6. **Response Format**: Structured markdown with sections

**Adaptive Prompting Examples**:

```python
# For Beginner + Visual Learning Style
"Explain concepts from first principles. Define all technical terms.
Use simple analogies. Use descriptive explanations that paint mental pictures."

# For Advanced + Practical Learning Style
"Focus on advanced patterns and best practices. Assume strong fundamentals.
Prioritize code examples and hands-on exercises. Show practical applications immediately."
```

### 4. API Endpoints

#### Authentication Endpoints (`/api/v1/auth`)

**POST /api/v1/auth/signup**
```json
Request:
{
  "email": "learner@example.com",
  "password": "securepassword123",
  "programming_experience": "intermediate",
  "ai_experience": "basic",
  "learning_style": "practical",
  "preferred_language": "en",
  "full_name": "Alex Johnson"  // optional
}

Response (201):
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "token_type": "bearer",
  "expires_in": 604800,  // 7 days in seconds
  "user": {
    "id": 1,
    "email": "learner@example.com",
    "programming_experience": "intermediate",
    "ai_experience": "basic",
    "learning_style": "practical",
    "preferred_language": "en",
    "full_name": "Alex Johnson",
    "created_at": "2025-11-15T12:00:00",
    "last_login": "2025-11-15T12:00:00",
    "is_active": true
  }
}
```

**POST /api/v1/auth/login**
```json
Request:
{
  "email": "learner@example.com",
  "password": "securepassword123"
}

Response (200): Same as signup response
```

**GET /api/v1/auth/me**
```json
Headers:
  Authorization: Bearer <jwt_token>

Response (200):
{
  "id": 1,
  "email": "learner@example.com",
  "programming_experience": "intermediate",
  // ... rest of user profile
}
```

#### Content Endpoints (`/api/v1/content`)

**GET /api/v1/content/personalized/{page_path}**
```json
Headers:
  Authorization: Bearer <jwt_token>

Example URL:
/api/v1/content/personalized/01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything

Response (200):
{
  "page_path": "01-Introducing-AI-Driven-Development/...",
  "markdown_content": "# A Moment That Changed Everything - Personalized for You\n\n...",
  "generated_at": "2025-11-15T12:30:00",
  "cached": false,  // true if served from cache
  "model_version": "gpt-4o-mini"
}
```

---

## 🎯 What Needs To Be Done Next

### Frontend Implementation (YOUR TASK)

#### Task 1: Update PersonalizedTab Component
**File**: `book-source/src/components/PersonalizedTab/index.tsx`

**Current State**:
```tsx
// Placeholder that says "Login required for personalized content"
```

**What You Need To Do**:
1. Check if user is logged in (JWT token in localStorage)
2. If NOT logged in → Show login/signup forms
3. If logged in → Fetch and display personalized content

**Pseudocode**:
```tsx
function PersonalizedTab({ pagePath }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [content, setContent] = useState(null);
  const [showSignup, setShowSignup] = useState(false);

  useEffect(() => {
    // Check if JWT token exists in localStorage
    const token = localStorage.getItem('tutorgpt_token');
    if (token) {
      // Validate token by calling /api/v1/auth/me
      validateToken(token);
    }
  }, []);

  if (!isLoggedIn) {
    return showSignup ? <SignupForm /> : <LoginForm />;
  }

  return <PersonalizedContent pagePath={pagePath} />;
}
```

#### Task 2: Create SignupForm Component
**File**: `book-source/src/components/PersonalizedTab/SignupForm.tsx` (CREATE NEW)

**Requirements**:
- Email input (required)
- Password input (required, min 8 chars)
- 4 Profile Questions (required):
  1. **Programming Experience**: Radio buttons (Beginner/Intermediate/Advanced)
  2. **AI/ML Experience**: Radio buttons (None/Basic/Intermediate/Advanced)
  3. **Learning Style**: Radio buttons (Visual/Practical/Conceptual/Mixed)
  4. **Preferred Language**: Dropdown (English/Spanish/French/German/Chinese/Japanese)
- Optional: Full Name
- Submit button
- Link to switch to Login form

**API Call**:
```typescript
const response = await fetch('http://localhost:8000/api/v1/auth/signup', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email,
    password,
    programming_experience,
    ai_experience,
    learning_style,
    preferred_language,
    full_name
  })
});

const data = await response.json();
localStorage.setItem('tutorgpt_token', data.access_token);
localStorage.setItem('tutorgpt_user', JSON.stringify(data.user));
```

#### Task 3: Create LoginForm Component
**File**: `book-source/src/components/PersonalizedTab/LoginForm.tsx` (CREATE NEW)

**Requirements**:
- Email input
- Password input
- Submit button
- Link to switch to Signup form

**API Call**: Same as signup but POST to `/api/v1/auth/login`

#### Task 4: Create PersonalizedContent Component
**File**: `book-source/src/components/PersonalizedTab/PersonalizedContent.tsx` (CREATE NEW)

**Requirements**:
- Fetch personalized content from `/api/v1/content/personalized/{pagePath}`
- Show loading state while fetching
- Render markdown content using Docusaurus markdown renderer
- Show error state if fetch fails
- Display cache status (optional)

**API Call**:
```typescript
const token = localStorage.getItem('tutorgpt_token');
const response = await fetch(`http://localhost:8000/api/v1/content/personalized/${pagePath}`, {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const data = await response.json();
// Render data.markdown_content
```

#### Task 5: Handle Token Expiration
- If API returns 401 Unauthorized → Clear localStorage → Show login form
- Implement auto-refresh or logout after 7 days

---

## 🚀 How To Continue

### Step 1: Verify Backend Is Running
```bash
cd "P:\Book Agent\ai-native-software-development\Tutor-Agent"

# Create .env file (copy from .env.example)
cp .env.example .env

# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-...your-key-here...

# Start backend server
uv run python -m tutor_agent.main
```

Backend will run on: `http://localhost:8000`
API Docs: `http://localhost:8000/api/docs`

### Step 2: Verify Frontend Is Running
```bash
cd "P:\Book Agent\ai-native-software-development\book-source"
npm start
```

Frontend will run on: `http://localhost:3000`

### Step 3: Create Frontend Components
Follow tasks 1-5 above in order.

### Step 4: Test Complete Flow
1. Open browser: `http://localhost:3000`
2. Navigate to any lesson page
3. Click "Personalized" tab
4. Fill signup form with 4 questions
5. Submit → Should get JWT token
6. Should see personalized content loading
7. Verify content is adapted to your profile

### Step 5: Test Caching
1. Refresh page → Should load from cache (faster)
2. Change user profile (you'll need to add a settings page OR re-signup)
3. Cache should invalidate → Generate new content

---

## 🧪 Testing Instructions

### Backend Testing (Already Works ✅)

**Test 1: Signup**
```bash
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "programming_experience": "intermediate",
    "ai_experience": "basic",
    "learning_style": "practical",
    "preferred_language": "en"
  }'
```

**Test 2: Login**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

**Test 3: Get User Profile**
```bash
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <token_from_login>"
```

**Test 4: Get Personalized Content**
```bash
curl "http://localhost:8000/api/v1/content/personalized/01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything" \
  -H "Authorization: Bearer <token>"
```

### Frontend Testing (You Need To Implement)
- Manual testing: Follow Step 4 above
- Unit tests: Create tests for each component
- Integration tests: Test full signup → login → content flow

---

## 📚 API Documentation

Full interactive API docs available at: `http://localhost:8000/api/docs`

### Authentication Flow
```
1. User signs up → POST /auth/signup → Returns JWT token
2. Frontend stores token in localStorage
3. Every API request includes: Authorization: Bearer <token>
4. Token expires after 7 days → User must login again
```

### Error Handling
```json
// 401 Unauthorized (invalid/expired token)
{
  "detail": "Invalid or expired token"
}

// 409 Conflict (email already exists)
{
  "detail": "User with this email already exists"
}

// 404 Not Found (lesson page doesn't exist)
{
  "detail": "Lesson not found: <page_path>"
}

// 500 Internal Server Error (OpenAI API failed)
{
  "detail": "Failed to generate personalized content: <error>"
}
```

---

## ⚠️ Important Notes

### Environment Variables Required
Create `.env` file in `Tutor-Agent/` directory:
```env
OPENAI_API_KEY=sk-...your-key-here...
OPENAI_MODEL=gpt-4o-mini
JWT_SECRET_KEY=your-super-secret-key-change-in-production
DATABASE_URL=sqlite:///./data/tutorgpt.db
```

### CORS Configuration
Backend allows requests from:
- `http://localhost:3000` (Docusaurus default)
- `http://localhost:3001` (Docusaurus alternative)

If you change frontend port, update `Tutor-Agent/src/tutor_agent/main.py` line 28.

### Database Location
SQLite database created at: `Tutor-Agent/data/tutorgpt.db`

Tables auto-created on first run:
- `users`
- `personalized_content`

### OpenAI API Costs
- Model: gpt-4o-mini (cheap, fast)
- Cost per page: ~$0.001-0.003
- Caching reduces costs significantly (content generated once per user+page+profile)

### Profile Question Labels
Use these EXACT values when creating forms:

**Programming Experience**:
- `beginner` - "Beginner (< 6 months)"
- `intermediate` - "Intermediate (6 months - 2 years)"
- `advanced` - "Advanced (2+ years)"

**AI/ML Experience**:
- `none` - "No experience with AI"
- `basic` - "Used AI tools but not built with them"
- `intermediate` - "Built some AI projects"
- `advanced` - "Regular AI/ML development"

**Learning Style**:
- `visual` - "Visual (diagrams, charts)"
- `practical` - "Practical (code examples, hands-on)"
- `conceptual` - "Conceptual (theory-first)"
- `mixed` - "Mixed (all approaches)"

**Preferred Language**:
- `en` - "English"
- `es` - "Spanish"
- `fr` - "French"
- `de` - "German"
- `zh` - "Chinese"
- `ja` - "Japanese"

---

## 🔍 Debugging Tips

### Backend Issues

**Problem**: "Module not found" errors
```bash
# Solution: Re-sync dependencies
cd Tutor-Agent
uv sync
```

**Problem**: "OpenAI API key not found"
```bash
# Solution: Check .env file exists and has OPENAI_API_KEY
cat .env | grep OPENAI_API_KEY
```

**Problem**: "Database locked" error
```bash
# Solution: Stop all running instances
pkill -f "tutor_agent.main"
rm data/tutorgpt.db  # WARNING: Deletes all data
```

### Frontend Issues

**Problem**: CORS errors
```bash
# Solution: Check backend allows your frontend origin
# Edit Tutor-Agent/src/tutor_agent/main.py line 28
```

**Problem**: 401 Unauthorized
```bash
# Solution: Token expired or invalid
# Clear localStorage and login again
localStorage.removeItem('tutorgpt_token');
localStorage.removeItem('tutorgpt_user');
```

---

## 📈 Next Features (Future Work)

After completing the current frontend implementation, consider:

1. **User Profile Settings Page**
   - Allow users to update their 4-question profile
   - Invalidate content cache on profile change

2. **Logout Functionality**
   - Clear localStorage
   - Redirect to login

3. **Remember Me / Auto-Login**
   - Store token with longer expiration
   - Auto-refresh tokens

4. **Content Regeneration Button**
   - Allow users to manually regenerate personalized content
   - Useful if they want a different explanation

5. **Loading Skeletons**
   - Better UX while content is generating
   - Progress indicator

6. **Error Boundaries**
   - Graceful error handling in React
   - Fallback UI

---

## 📞 Contact & Resources

**Repository**: `ai-native-software-development`
**Branch**: `main` (push your changes here)
**Backend Port**: 8000
**Frontend Port**: 3000

**Key Documentation**:
- OpenAI Agents SDK: https://openai.github.io/openai-agents-python
- FastAPI: https://fastapi.tiangolo.com
- Docusaurus: https://docusaurus.io
- React TypeScript: https://react-typescript-cheatsheet.netlify.app

---

## ✅ Checklist For Next Agent

Before you start coding:
- [ ] Read this entire document
- [ ] Verify backend runs: `cd Tutor-Agent && uv run python -m tutor_agent.main`
- [ ] Verify frontend runs: `cd book-source && npm start`
- [ ] Test backend API manually (use curl or Postman)
- [ ] Understand the 4-question profile system
- [ ] Review existing SummaryTab component (similar pattern)

Implementation order:
1. [ ] Create `LoginForm.tsx`
2. [ ] Create `SignupForm.tsx` with 4 questions
3. [ ] Update `PersonalizedTab/index.tsx` to handle auth state
4. [ ] Create `PersonalizedContent.tsx` to fetch & display
5. [ ] Test complete flow: signup → login → view personalized content
6. [ ] Handle edge cases: token expiration, errors, loading states
7. [ ] Git commit and push to main branch

---

## 🎉 Good Luck!

This handoff document contains everything you need to continue where I left off. The backend is solid and tested. Your job is to create the React frontend that brings this feature to life.

**Remember**:
- The backend is DONE and WORKS ✅
- You're building the UI layer
- Follow the API contracts exactly
- Test thoroughly before pushing

If you get stuck, refer to:
- API docs: `http://localhost:8000/api/docs`
- This document (HANDOFF.md)
- Existing SummaryTab component for patterns

**Happy Coding!** 🚀
