# Frontend + Backend Implementation Roadmap

**Date**: 2025-11-17
**Goal**: Complete three-mode content system with authentication, streaming, and caching

---

## 🎯 Feature Requirements

### Three Content Modes
Every page/lesson must have:
1. **Original** - Display markdown as-is (default view)
2. **Summarize** - Show AI-generated summary (no auth required)
3. **Personalize** - User-specific content (requires login)

### Authentication Flow
- Unauthenticated users see "Login/Signup" modal when clicking "Personalize"
- After auth, return to same page and generate personalized content
- Cache personalized content per user per page

### Streaming UI
- Real-time generation with progress indicators
- Show agent capabilities: "Analyzing learning style...", "Adapting difficulty..."
- Similar to Grok's streaming interface

### Performance Optimization
- Generate ONLY for current page (not entire book)
- Cache results in database
- Show cached version immediately on subsequent visits
- "Generate New Version" button to refresh

---

## 📁 File Structure

```
book-source/
├── src/
│   ├── components/
│   │   ├── TabSystem/
│   │   │   ├── ContentTabs.tsx           ← Main 3-tab component
│   │   │   ├── OriginalTab.tsx           ← Shows original markdown
│   │   │   ├── SummarizeTab.tsx          ← Shows AI summary
│   │   │   ├── PersonalizeTab.tsx        ← Shows personalized content
│   │   │   └── StreamingView.tsx         ← Real-time generation UI
│   │   ├── Auth/
│   │   │   ├── AuthModal.tsx             ← Login/Signup modal
│   │   │   ├── LoginForm.tsx
│   │   │   ├── SignupForm.tsx            ← 4-question profile
│   │   │   └── PreferenceModal.tsx       ← Update preferences
│   │   └── UI/
│   │       ├── LoadingSpinner.tsx
│   │       ├── ProgressIndicator.tsx     ← Agent progress UI
│   │       └── ErrorBoundary.tsx
│   ├── hooks/
│   │   ├── useAuth.ts                    ← Auth state management
│   │   ├── useContent.ts                 ← Fetch content (REST)
│   │   ├── useWebSocket.ts               ← Streaming connection
│   │   └── usePreferences.ts             ← User preferences
│   ├── services/
│   │   ├── api.ts                        ← REST client
│   │   ├── websocket.ts                  ← WebSocket client
│   │   └── cache.ts                      ← Local storage caching
│   ├── types/
│   │   ├── content.ts
│   │   ├── user.ts
│   │   └── streaming.ts
│   └── theme/
│       └── Root.tsx                      ← Global providers

Tutor-Agent/
├── src/tutor_agent/
│   ├── api/v1/
│   │   ├── content.py                    ← Content endpoints
│   │   │   GET /summary/{page_path}
│   │   │   GET /personalized/{page_path}
│   │   │   POST /personalized/regenerate
│   │   ├── auth.py                       ← Already exists
│   │   ├── preferences.py                ← NEW: Update preferences
│   │   │   PUT /preferences
│   │   │   GET /preferences
│   │   └── websocket.py                  ← NEW: Streaming
│   │       WS /ws/personalize/{page_path}
│   ├── services/
│   │   ├── cache/
│   │   │   ├── personalization_cache.py  ← Cache manager
│   │   │   └── summary_cache.py
│   │   └── agent/
│   │       └── olivia_agent.py           ← Already exists
│   └── models/
│       ├── user.py                       ← Already exists
│       └── cache.py                      ← NEW: Cache models
```

---

## 🔨 Implementation Steps

### Phase 1: Backend - Content Endpoints (2 hours)

#### T1.1: Create Summary Endpoint
```python
# Tutor-Agent/src/tutor_agent/api/v1/content.py

@router.get("/summary/{page_path:path}")
async def get_summary(page_path: str, db: Session = Depends(get_db)):
    """
    Get AI-generated summary for any page
    No authentication required
    Returns cached summary if exists, generates if new
    """
    pass
```

#### T1.2: Create Personalized Endpoint
```python
@router.get("/personalized/{page_path:path}")
async def get_personalized_content(
    page_path: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get personalized content for authenticated user
    Returns cached if profile matches, generates if changed
    """
    pass
```

#### T1.3: Create Streaming WebSocket
```python
# Tutor-Agent/src/tutor_agent/api/v1/websocket.py

@router.websocket("/ws/personalize/{page_path:path}")
async def personalize_stream(
    websocket: WebSocket,
    page_path: str,
    token: str,  # JWT from query param
    db: Session = Depends(get_db)
):
    """
    Stream personalized content generation in real-time
    Send progress updates: "Analyzing...", "Adapting...", etc.
    """
    pass
```

#### T1.4: Create Preferences Endpoint
```python
# Tutor-Agent/src/tutor_agent/api/v1/preferences.py

@router.put("/preferences")
async def update_preferences(
    prefs: PreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user's learning preferences
    Invalidates personalization cache
    """
    pass
```

---

### Phase 2: Backend - Caching Layer (1 hour)

#### T2.1: Create Cache Models
```python
# Tutor-Agent/src/tutor_agent/models/cache.py

class PersonalizedContentCache(Base):
    __tablename__ = "personalized_cache"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    page_path = Column(String(500))
    content = Column(Text)

    # Profile snapshot (for cache invalidation)
    programming_exp = Column(String(50))
    ai_exp = Column(String(50))
    learning_style = Column(String(50))
    language = Column(String(10))

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_user_page', 'user_id', 'page_path'),
    )
```

#### T2.2: Implement Cache Manager
```python
# Tutor-Agent/src/tutor_agent/services/cache/personalization_cache.py

class PersonalizationCache:
    def get(self, user: User, page_path: str) -> Optional[str]:
        """Get cached content if profile matches"""

    def set(self, user: User, page_path: str, content: str):
        """Store personalized content with profile snapshot"""

    def invalidate_user(self, user_id: int):
        """Clear all cache for user (when preferences change)"""

    def is_valid(self, cached: PersonalizedContentCache, user: User) -> bool:
        """Check if cached content matches current profile"""
```

---

### Phase 3: Frontend - Tab System (3 hours)

#### T3.1: Create ContentTabs Component
```tsx
// book-source/src/components/TabSystem/ContentTabs.tsx

export default function ContentTabs({ pageContent, pagePath }) {
  const [activeTab, setActiveTab] = useState('original');
  const { user, isAuthenticated } = useAuth();
  const [showAuthModal, setShowAuthModal] = useState(false);

  const handleTabChange = (tab: 'original' | 'summarize' | 'personalize') => {
    if (tab === 'personalize' && !isAuthenticated) {
      setShowAuthModal(true);
      return;
    }
    setActiveTab(tab);
  };

  return (
    <div className="content-tabs">
      <TabList>
        <Tab active={activeTab === 'original'} onClick={() => handleTabChange('original')}>
          Original
        </Tab>
        <Tab active={activeTab === 'summarize'} onClick={() => handleTabChange('summarize')}>
          Summarize
        </Tab>
        <Tab active={activeTab === 'personalize'} onClick={() => handleTabChange('personalize')}>
          Personalize
        </Tab>
      </TabList>

      <TabPanels>
        {activeTab === 'original' && <OriginalTab content={pageContent} />}
        {activeTab === 'summarize' && <SummarizeTab pagePath={pagePath} />}
        {activeTab === 'personalize' && <PersonalizeTab pagePath={pagePath} user={user} />}
      </TabPanels>

      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        returnPath={pagePath}
      />
    </div>
  );
}
```

#### T3.2: Create PersonalizeTab with Streaming
```tsx
// book-source/src/components/TabSystem/PersonalizeTab.tsx

export default function PersonalizeTab({ pagePath, user }) {
  const { cachedContent, isLoading } = useContent(`/personalized/${pagePath}`);
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamedContent, setStreamedContent] = useState('');
  const [progress, setProgress] = useState<string[]>([]);

  const generateNew = async () => {
    setIsStreaming(true);
    const ws = new WebSocket(`ws://api/ws/personalize/${pagePath}?token=${getToken()}`);

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === 'progress') {
        setProgress(prev => [...prev, data.message]);
      } else if (data.type === 'content') {
        setStreamedContent(prev => prev + data.chunk);
      } else if (data.type === 'complete') {
        setIsStreaming(false);
      }
    };
  };

  if (isStreaming) {
    return <StreamingView progress={progress} content={streamedContent} />;
  }

  if (cachedContent) {
    return (
      <div>
        <button onClick={generateNew}>Generate New Version</button>
        <Markdown>{cachedContent}</Markdown>
      </div>
    );
  }

  return <button onClick={generateNew}>Generate Personalized Content</button>;
}
```

#### T3.3: Create StreamingView Component
```tsx
// book-source/src/components/TabSystem/StreamingView.tsx

export default function StreamingView({ progress, content }) {
  return (
    <div className="streaming-view">
      <div className="progress-sidebar">
        <h4>🤖 OLIVIA is working...</h4>
        {progress.map((msg, i) => (
          <div key={i} className="progress-step">
            {msg}
          </div>
        ))}
      </div>

      <div className="content-preview">
        <Markdown>{content}</Markdown>
        <div className="typing-cursor">▊</div>
      </div>
    </div>
  );
}
```

---

### Phase 4: Frontend - Authentication (2 hours)

#### T4.1: AuthModal with Signup Form
```tsx
// book-source/src/components/Auth/AuthModal.tsx

export default function AuthModal({ isOpen, onClose, returnPath }) {
  const [mode, setMode] = useState<'login' | 'signup'>('login');

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <h2>Please {mode === 'login' ? 'Login' : 'Sign Up'} to Access Personalized Content</h2>

      {mode === 'login' ? (
        <LoginForm onSuccess={() => {
          onClose();
          // Refresh page to trigger personalization
        }} />
      ) : (
        <SignupForm
          onSuccess={() => {
            onClose();
            // Refresh to trigger personalization
          }}
        />
      )}

      <button onClick={() => setMode(mode === 'login' ? 'signup' : 'login')}>
        {mode === 'login' ? 'Create Account' : 'Already have account?'}
      </button>
    </Modal>
  );
}
```

#### T4.2: SignupForm with 4 Questions
```tsx
// book-source/src/components/Auth/SignupForm.tsx

export default function SignupForm({ onSuccess }) {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    programming_experience: '',
    ai_experience: '',
    learning_style: '',
    preferred_language: 'en'
  });

  return (
    <form onSubmit={handleSignup}>
      <input type="email" name="email" required />
      <input type="password" name="password" required />

      <h3>Personalization Questions</h3>

      <select name="programming_experience" required>
        <option value="">Programming Experience?</option>
        <option value="beginner">Beginner (< 6 months)</option>
        <option value="intermediate">Intermediate (6mo - 2yr)</option>
        <option value="advanced">Advanced (2+ years)</option>
      </select>

      <select name="ai_experience" required>
        <option value="">AI/ML Experience?</option>
        <option value="none">No experience</option>
        <option value="basic">Used AI tools</option>
        <option value="intermediate">Built AI projects</option>
        <option value="advanced">Regular AI development</option>
      </select>

      <select name="learning_style" required>
        <option value="">Learning Style?</option>
        <option value="visual">Visual (diagrams, charts)</option>
        <option value="practical">Hands-on (code, exercises)</option>
        <option value="conceptual">Theory-first</option>
        <option value="mixed">Mixed</option>
      </select>

      <select name="preferred_language" required>
        <option value="en">English 🇬🇧</option>
        <option value="es">Español 🇪🇸</option>
        <option value="ur">اردو 🇵🇰</option>
        {/* All 14 languages */}
      </select>

      <button type="submit">Create Account & Personalize</button>
    </form>
  );
}
```

---

### Phase 5: Integration & Testing (1 hour)

#### T5.1: Integrate ContentTabs into Docusaurus
```tsx
// book-source/src/theme/MDXContent.tsx

import ContentTabs from '@/components/TabSystem/ContentTabs';

export default function MDXContent({ children }) {
  const { pathname } = useLocation();
  const content = children.toString(); // Get raw markdown

  return (
    <ContentTabs
      pageContent={content}
      pagePath={pathname}
    />
  );
}
```

#### T5.2: Add Global Auth Provider
```tsx
// book-source/src/theme/Root.tsx

import { AuthProvider } from '@/hooks/useAuth';

export default function Root({ children }) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
}
```

---

## 🎯 Success Criteria

### Original Tab
- ✅ Shows markdown content as-is
- ✅ Default view on page load
- ✅ Syntax highlighting works

### Summarize Tab
- ✅ Generates 200-400 word summary
- ✅ No auth required
- ✅ Cached after first generation
- ✅ Loads in < 200ms from cache

### Personalize Tab
- ✅ Shows auth modal if not logged in
- ✅ Streams generation with progress indicators
- ✅ Caches result for user profile
- ✅ Shows "Generate New" button for cached content
- ✅ Adapts to user preferences

### Performance
- ✅ Summary generation: < 5s
- ✅ Personalization generation: < 8s
- ✅ Cached content load: < 200ms
- ✅ WebSocket connection: < 1s

---

## 📊 Database Schema

```sql
-- Already exists
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  programming_experience VARCHAR(50) NOT NULL,
  ai_experience VARCHAR(50) NOT NULL,
  learning_style VARCHAR(50) NOT NULL,
  preferred_language VARCHAR(10) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- NEW: Personalization cache
CREATE TABLE personalized_cache (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  page_path VARCHAR(500) NOT NULL,
  content TEXT NOT NULL,
  programming_exp VARCHAR(50) NOT NULL,
  ai_exp VARCHAR(50) NOT NULL,
  learning_style VARCHAR(50) NOT NULL,
  language VARCHAR(10) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  INDEX idx_user_page (user_id, page_path)
);

-- NEW: Summary cache
CREATE TABLE summary_cache (
  id INTEGER PRIMARY KEY,
  page_path VARCHAR(500) UNIQUE NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🚀 Deployment Checklist

- [ ] Database migrations run
- [ ] Environment variables set
- [ ] WebSocket endpoint configured
- [ ] CORS configured for WebSocket
- [ ] Frontend build includes new components
- [ ] Auth flow tested end-to-end
- [ ] Caching works correctly
- [ ] Streaming UI tested
- [ ] Performance benchmarks met

---

**Total Estimated Time**: 9-10 hours
**Priority**: High (MVP feature)
**Dependencies**: Backend OLIVIA agent (✅ Complete)
