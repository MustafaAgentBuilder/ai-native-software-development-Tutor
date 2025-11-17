# Frontend Analysis: book-source Directory

**Analysis Date**: 2025-11-17
**Purpose**: Understand current frontend structure and plan three-tab backend integration

---

## 📊 Current Frontend Stack

### Technology Stack
- **Framework**: Docusaurus 3.9.2 (React-based static site generator)
- **React**: Version 19.0.0
- **TypeScript**: ~5.6.2
- **Styling**: Tailwind CSS (PostCSS + Autoprefixer)
- **Build Tool**: Docusaurus CLI
- **Node**: >=20.0 required

### Package Dependencies
```json
{
  "@docusaurus/core": "^3.9.2",
  "@docusaurus/preset-classic": "^3.9.2",
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "clsx": "^2.0.0"
}
```

---

## 📁 Directory Structure

```
book-source/
├── src/
│   ├── components/
│   │   ├── SummaryTab/          ✅ EXISTS (needs update)
│   │   │   ├── index.tsx
│   │   │   └── styles.module.css
│   │   ├── quiz/
│   │   └── AnalyticsTracker.tsx
│   ├── theme/
│   │   ├── MDXComponents.tsx
│   │   └── Root.tsx
│   ├── css/
│   ├── pages/
│   ├── analytics/
│   └── utils/
├── static/
│   └── summaries/               ✅ 31 pre-generated summaries
│       └── 01-Introducing-AI-Driven-Development_*.md
├── docs/                        ✅ Book content (markdown files)
│   └── 01-Introducing-AI-Driven-Development/
│       └── 01-ai-development-revolution/
│           └── 01-moment_that_changed_everything.md
├── docusaurus.config.ts
├── sidebars.ts
├── package.json
└── tsconfig.json
```

---

## 🎯 Current Three-Tab Implementation

### How Tabs Work Now

**MDX File Structure** (`01-moment_that_changed_everything.md`):

```jsx
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import SummaryTab from '@site/src/components/SummaryTab';

<Tabs>
  <TabItem value="original" label="📖 Original" default>
    {/* Full markdown content here */}
  </TabItem>

  <TabItem value="summary" label="📝 Summary">
    <SummaryTab pagePath="01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything" />
  </TabItem>

  <TabItem value="personalized" label="✨ Personalized">
    *Login required for personalized content powered by OLIVIA AI Tutor*
  </TabItem>
</Tabs>
```

### Current Tab Behavior

#### 1. **Original Tab** ✅ Working
- **Status**: Fully functional
- **Source**: Raw markdown content embedded in MDX file
- **No changes needed**: This tab works perfectly as-is

#### 2. **Summary Tab** ⚠️ Needs Update
- **Current**: Loads from static files (`/static/summaries/`)
- **Current Code**: `src/components/SummaryTab/index.tsx`
  - Fetches: `/summaries/CHAPTER_PAGE.md`
  - Parses frontmatter (YAML) and markdown content
  - Shows: metadata badges, summary text, key concepts
  - Fallback: "Team Working on it" message if file missing

**What Needs to Change**:
```typescript
// CURRENT (static file loading):
const summaryPath = `/summaries/${summaryFilename}`;
const response = await fetch(summaryPath);
const content = await response.text();

// NEW (backend API call):
const apiUrl = `http://localhost:8000/api/v1/content/summary/${pagePath}`;
const response = await fetch(apiUrl);
const data = await response.json();
// Use: data.summary_content, data.word_count, data.model_version
```

#### 3. **Personalized Tab** ❌ Not Implemented
- **Current**: Just shows static text "Login required"
- **Needs**: Full PersonalizedTab component with:
  - Authentication check
  - Login modal trigger if not authenticated
  - API call to backend with JWT token
  - Display personalized content
  - Loading state with progress
  - Error handling

---

## 🚧 What Needs to be Built

### Priority 1: Update SummaryTab Component

**File**: `src/components/SummaryTab/index.tsx`

**Changes Required**:
1. Change from static file loading to backend API call
2. Update API endpoint: `GET /api/v1/content/summary/{page_path}`
3. Update response parsing (JSON instead of markdown)
4. Keep existing UI (metadata badges, summary text, key concepts)
5. Update "model_version" check (expect `"pre-generated-v1"`)

**API Response Format** (from backend):
```typescript
interface SummaryResponse {
  page_path: string;
  summary_content: string;
  word_count: number;
  cached: boolean;
  generated_at: string;
  model_version: "pre-generated-v1";  // Not AI-generated
}
```

---

### Priority 2: Create PersonalizedTab Component

**File**: `src/components/PersonalizedTab/index.tsx` (NEW)

**Requirements**:
1. Check if user is authenticated (useAuth hook)
2. If not authenticated:
   - Show login prompt/modal
   - "Sign up" and "Login" buttons
3. If authenticated:
   - Call backend API: `GET /api/v1/content/personalized/{page_path}`
   - Include JWT token in Authorization header
   - Show loading state (30-60s for first generation)
   - Display personalized content (markdown rendering)
   - Show profile badge (visual/practical learner, experience level)

**API Response Format** (from backend):
```typescript
interface PersonalizedContentResponse {
  page_path: string;
  personalized_content: string;  // Markdown adapted to user
  cached: boolean;
  generated_at: string;
  model_version: "gpt-4o-mini";  // AI-generated
  profile_snapshot: {
    programming_experience: string;
    ai_experience: string;
    learning_style: string;
    preferred_language: string;
  };
}
```

**Example UI**:
```
┌─────────────────────────────────────────┐
│  👤 Visual Learner | Intermediate      │
│  ✨ Personalized by OLIVIA             │
├─────────────────────────────────────────┤
│                                         │
│  [Personalized markdown content here]  │
│  - Includes Mermaid diagrams for        │
│    visual learners                      │
│  - Adapted language complexity          │
│                                         │
└─────────────────────────────────────────┘
```

---

### Priority 3: Authentication System

#### 3.1 SignupForm Component
**File**: `src/components/Auth/SignupForm.tsx` (NEW)

**Fields**:
1. Email (required)
2. Password (required, min 8 chars)
3. Programming Experience (select: beginner/intermediate/advanced)
4. AI/ML Experience (select: none/basic/intermediate/advanced)
5. Learning Style (select: visual/practical/theoretical/interactive)
6. Preferred Language (select: en/es/fr/de/zh/ja/etc.)

**API Call**: `POST /api/v1/auth/signup`
```typescript
interface SignupRequest {
  email: string;
  password: string;
  programming_experience: string;
  ai_experience: string;
  learning_style: string;
  preferred_language: string;
}

interface SignupResponse {
  message: string;
  user: {
    id: number;
    email: string;
    programming_experience: string;
    // ... other profile fields
  };
}
```

#### 3.2 LoginForm Component
**File**: `src/components/Auth/LoginForm.tsx` (NEW)

**Fields**:
1. Email
2. Password

**API Call**: `POST /api/v1/auth/login`
```typescript
interface LoginRequest {
  email: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
  token_type: "bearer";
  user: {
    id: number;
    email: string;
    programming_experience: string;
    // ... profile
  };
}
```

#### 3.3 AuthModal Component
**File**: `src/components/Auth/AuthModal.tsx` (NEW)

**Purpose**: Wrapper modal that shows SignupForm or LoginForm

**Features**:
- Toggle between signup/login views
- Close button
- "Already have an account?" / "Need an account?" links
- Success/error messages
- Auto-close on successful auth

---

### Priority 4: Hooks & Services

#### 4.1 useAuth Hook
**File**: `src/hooks/useAuth.ts` (NEW)

**Purpose**: Manage authentication state globally

**Features**:
```typescript
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

interface UseAuth {
  // State
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;

  // Actions
  login: (email: string, password: string) => Promise<void>;
  signup: (data: SignupRequest) => Promise<void>;
  logout: () => void;

  // Token management
  getToken: () => string | null;
}

// Usage:
const { user, isAuthenticated, login, logout } = useAuth();
```

**Storage**: LocalStorage for token persistence
**Auto-refresh**: Check token expiry on mount

#### 4.2 useContent Hook
**File**: `src/hooks/useContent.ts` (NEW)

**Purpose**: Fetch content from backend API

```typescript
interface UseContent {
  // Summary
  loadSummary: (pagePath: string) => Promise<SummaryResponse>;

  // Personalized (requires auth)
  loadPersonalized: (pagePath: string) => Promise<PersonalizedContentResponse>;

  // State
  isLoading: boolean;
  error: string | null;
}
```

#### 4.3 API Service
**File**: `src/services/api.ts` (NEW)

**Purpose**: Centralized API client

```typescript
class APIService {
  private baseURL = 'http://localhost:8000/api/v1';

  // Content
  async getSummary(pagePath: string): Promise<SummaryResponse>;
  async getPersonalized(pagePath: string, token: string): Promise<PersonalizedContentResponse>;

  // Auth
  async signup(data: SignupRequest): Promise<SignupResponse>;
  async login(email: string, password: string): Promise<LoginResponse>;

  // Profile
  async getProfile(token: string): Promise<User>;
  async updateProfile(token: string, updates: Partial<User>): Promise<User>;
}

export const apiService = new APIService();
```

---

## 🔧 Implementation Plan

### Phase 1: Update SummaryTab (1 hour)
1. ✅ Understand current SummaryTab code
2. Replace static file loading with API call
3. Update response parsing (JSON vs markdown)
4. Test with existing summaries
5. Verify cache behavior (instant second load)

### Phase 2: Auth System (2-3 hours)
1. Create useAuth hook with localStorage
2. Create SignupForm component
3. Create LoginForm component
4. Create AuthModal wrapper
5. Test signup → login flow

### Phase 3: PersonalizedTab (2 hours)
1. Create PersonalizedTab component
2. Integrate useAuth check
3. Call backend API with JWT
4. Render markdown content
5. Handle loading states (30-60s first gen)
6. Test with different user profiles

### Phase 4: Integration & Testing (1 hour)
1. Update MDX files to use new PersonalizedTab
2. Test all three tabs together
3. Verify separation of concerns:
   - Original: No AI
   - Summary: Pre-generated (no AI)
   - Personalized: OLIVIA AI only
4. Test authentication flow
5. Test cache behavior

**Total Estimated Time**: 6-7 hours

---

## 📝 File Changes Summary

### New Files to Create
```
src/
├── components/
│   ├── PersonalizedTab/
│   │   ├── index.tsx          (NEW)
│   │   └── styles.module.css  (NEW)
│   └── Auth/
│       ├── SignupForm.tsx     (NEW)
│       ├── LoginForm.tsx      (NEW)
│       └── AuthModal.tsx      (NEW)
├── hooks/
│   ├── useAuth.ts             (NEW)
│   └── useContent.ts          (NEW)
└── services/
    └── api.ts                 (NEW)
```

### Files to Update
```
src/
└── components/
    └── SummaryTab/
        └── index.tsx          (UPDATE - API integration)
```

### Files to Update (MDX)
```
docs/
└── **/*.md                    (UPDATE - add PersonalizedTab import)
```

---

## 🎯 Key Integration Points

### Backend API Endpoints (Already Working)

1. **Summary**: `GET /api/v1/content/summary/{page_path}`
   - Public (no auth)
   - Returns pre-generated summary
   - `model_version: "pre-generated-v1"`

2. **Personalized**: `GET /api/v1/content/personalized/{page_path}`
   - Requires JWT auth
   - Returns OLIVIA personalized content
   - `model_version: "gpt-4o-mini"`
   - Adapts to user profile

3. **Signup**: `POST /api/v1/auth/signup`
4. **Login**: `POST /api/v1/auth/login`

### CORS Configuration Needed

**Backend must allow**:
```python
# In Tutor-Agent FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Docusaurus dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🚀 Next Steps

1. **Start Backend Server** (if not running):
   ```bash
   cd Tutor-Agent
   uv run uvicorn tutor_agent.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start Frontend Dev Server**:
   ```bash
   cd book-source
   npm start
   # Opens http://localhost:3000
   ```

3. **Begin Implementation**:
   - Phase 1: Update SummaryTab
   - Phase 2: Auth system
   - Phase 3: PersonalizedTab
   - Phase 4: Integration

---

## ✅ Success Criteria

### Functional Requirements
- [ ] User can view Original tab (already works)
- [ ] User can view Summary tab (loads from backend API)
- [ ] User can sign up with 4-question profile
- [ ] User can log in
- [ ] User can view Personalized content (after login)
- [ ] Visual learners see Mermaid diagrams
- [ ] Content adapts to experience level
- [ ] Cached content loads instantly (<100ms)
- [ ] First-time generation shows progress

### Technical Requirements
- [ ] All API calls use centralized service
- [ ] Authentication state persists (localStorage)
- [ ] JWT token included in personalized requests
- [ ] Error handling on all API calls
- [ ] Loading states on all async operations
- [ ] Responsive design (mobile-friendly)
- [ ] TypeScript types for all API responses

---

## 🔍 Testing Strategy

### Unit Tests
- useAuth hook (login, logout, token management)
- API service (all endpoints)
- Component rendering (snapshot tests)

### Integration Tests
- Signup flow → Login → Personalized content
- Token expiry handling
- Cache invalidation on profile change

### Manual Testing
1. New user signup
2. Profile questions submission
3. Login with credentials
4. View personalized content
5. Switch between tabs
6. Logout and login again
7. Test with different profiles (beginner, advanced, visual, practical)

---

## 📚 References

- **Backend API Docs**: `Tutor-Agent/TESTING_THREE_TABS.md`
- **Backend Implementation**: `Tutor-Agent/src/tutor_agent/api/v1/content.py`
- **Current SummaryTab**: `book-source/src/components/SummaryTab/index.tsx`
- **Docusaurus Docs**: https://docusaurus.io/docs
- **React 19 Docs**: https://react.dev/

---

**Status**: Analysis complete. Ready to begin implementation.
**Next Action**: Create todo list and start Phase 1 (SummaryTab API integration)
