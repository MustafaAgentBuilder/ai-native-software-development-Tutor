# Testing the Three-Tab System

This guide shows you how to test all three tabs manually or with the automated test suite.

## Quick Start: Automated Testing

**Run the comprehensive test suite:**
```bash
cd Tutor-Agent
python3 test_three_tabs.py
```

This will:
- ✅ Test Original tab (raw content, no AI)
- ✅ Test Summary tab (pre-generated, no AI)
- ✅ Test Personalize tab (OLIVIA AI, requires auth)
- ✅ Verify separation of concerns
- ✅ Show detailed results with pass/fail status

---

## Manual Testing with cURL

### Prerequisites

1. **Start the backend server:**
```bash
cd Tutor-Agent
uv run uvicorn tutor_agent.main:app --reload --host 0.0.0.0 --port 8000
```

2. **Verify server is running:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","service":"TutorGPT API"}
```

---

## Tab 1: Original Content (NO AI)

**Test the Original endpoint:**
```bash
curl -s http://localhost:8000/api/v1/content/original/01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything | jq
```

**Expected Response:**
```json
{
  "page_path": "01-Introducing-AI-Driven-Development/...",
  "content": "# A Moment That Changed Everything\n\n...",
  "frontmatter": {},
  "source": "original",
  "ai_processed": false  // ← CRITICAL: Must be false (no AI)
}
```

**Verification Checklist:**
- [ ] `ai_processed` is `false`
- [ ] `source` is `"original"`
- [ ] `content` contains full lesson markdown (>5000 chars)
- [ ] Response is instant (<100ms)

---

## Tab 2: Summary (Pre-Generated, NO AI)

**Clear cache first (to test fresh load):**
```bash
curl -X DELETE http://localhost:8000/api/v1/content/cache/summary/01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything
```

**Test the Summary endpoint:**
```bash
curl -s http://localhost:8000/api/v1/content/summary/01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything | jq
```

**Expected Response:**
```json
{
  "page_path": "01-Introducing-AI-Driven-Development/...",
  "summary_content": "# Summary\n\nThis opening lesson establishes...",
  "word_count": 348,
  "cached": false,
  "generated_at": "2025-11-15",
  "model_version": "pre-generated-v1"  // ← CRITICAL: Must be pre-generated-v1 (no AI)
}
```

**Verification Checklist:**
- [ ] `model_version` is `"pre-generated-v1"` (not gpt-4o-mini)
- [ ] `word_count` is 200-500 (good summary length)
- [ ] `summary_content` contains markdown summary
- [ ] Second request is instant (<50ms) due to caching

**Test caching:**
```bash
# Second request should be instant
time curl -s http://localhost:8000/api/v1/content/summary/01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything > /dev/null
```

---

## Tab 3: Personalize (OLIVIA AI - Auth Required)

### Step 1: Create Test User

```bash
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test.visual@example.com",
    "password": "Test123!",
    "programming_experience": "intermediate",
    "ai_experience": "basic",
    "learning_style": "visual",
    "preferred_language": "en"
  }'
```

### Step 2: Login and Get Token

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test.visual@example.com",
    "password": "Test123!"
  }' | jq -r '.access_token'
```

**Save the token:**
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Step 3: Test Personalized Content

```bash
curl -s http://localhost:8000/api/v1/content/personalized/01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything \
  -H "Authorization: Bearer $TOKEN" | jq
```

**Expected Response:**
```json
{
  "page_path": "01-Introducing-AI-Driven-Development/...",
  "personalized_content": "## A Moment That Changed Everything...",
  "cached": false,
  "generated_at": "2025-11-17T13:00:00",
  "model_version": "gpt-4o-mini",  // ← CRITICAL: AI model (not pre-generated)
  "profile_snapshot": {
    "programming_experience": "intermediate",
    "ai_experience": "basic",
    "learning_style": "visual",
    "preferred_language": "en"
  }
}
```

**Verification Checklist:**
- [ ] `model_version` is `"gpt-4o-mini"` (AI-generated)
- [ ] `profile_snapshot` matches user profile
- [ ] Content is >2000 chars (comprehensive personalization)
- [ ] For visual learners: contains Mermaid diagrams (```mermaid)
- [ ] For practical learners: contains code examples
- [ ] First generation takes 30-60s (AI processing)
- [ ] Second request is instant (<100ms) due to caching

**Test caching:**
```bash
# Second request should be instant
time curl -s http://localhost:8000/api/v1/content/personalized/01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything \
  -H "Authorization: Bearer $TOKEN" | jq '.cached'
# Should return: true
```

---

## Verification: Separation of Concerns

**CRITICAL CHECKS:**

1. **Original Tab NEVER uses AI:**
   ```bash
   # Should ALWAYS return false
   curl -s http://localhost:8000/api/v1/content/original/01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything | jq '.ai_processed'
   ```

2. **Summary Tab NEVER uses AI:**
   ```bash
   # Should ALWAYS return "pre-generated-v1"
   curl -s http://localhost:8000/api/v1/content/summary/01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything | jq '.model_version'
   ```

3. **Personalize Tab is the ONLY tab using AI:**
   ```bash
   # Should return "gpt-4o-mini" (AI model)
   curl -s http://localhost:8000/api/v1/content/personalized/01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything \
     -H "Authorization: Bearer $TOKEN" | jq '.model_version'
   ```

---

## Testing Different User Profiles

### Test Visual Learner (Should Include Mermaid Diagrams)

```bash
# Create visual learner
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "visual.learner@test.com",
    "password": "Test123!",
    "programming_experience": "beginner",
    "ai_experience": "none",
    "learning_style": "visual",
    "preferred_language": "en"
  }'

# Get token and test personalized content
# Expected: Content should contain ```mermaid diagrams
```

### Test Practical Learner (Should Include Code Examples)

```bash
# Create practical learner
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "practical.learner@test.com",
    "password": "Test123!",
    "programming_experience": "advanced",
    "ai_experience": "intermediate",
    "learning_style": "practical",
    "preferred_language": "en"
  }'

# Get token and test personalized content
# Expected: Content should contain code examples (```python, ```javascript)
```

---

## Performance Benchmarks

**Expected Loading Times:**

| Tab | First Load | Cached Load | AI Processing |
|-----|-----------|-------------|---------------|
| **Original** | <100ms | <50ms | ❌ None |
| **Summary** | <200ms | <50ms | ❌ None |
| **Personalize** | 30-60s | <100ms | ✅ AI generation |

**Test loading performance:**
```bash
# Test Original tab speed
time curl -s http://localhost:8000/api/v1/content/original/01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything > /dev/null

# Test Summary tab speed (cached)
time curl -s http://localhost:8000/api/v1/content/summary/01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything > /dev/null

# Test Personalize tab speed (cached)
time curl -s http://localhost:8000/api/v1/content/personalized/01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything \
  -H "Authorization: Bearer $TOKEN" > /dev/null
```

---

## Troubleshooting

### Server Not Responding

```bash
# Check if server is running
curl http://localhost:8000/health

# If not running, start it:
cd Tutor-Agent
uv run uvicorn tutor_agent.main:app --reload --host 0.0.0.0 --port 8000
```

### Summary Returns AI Model Version

If summary endpoint returns `"model_version": "gpt-4o-mini"` instead of `"pre-generated-v1"`:

```bash
# Clear the cache
curl -X DELETE http://localhost:8000/api/v1/content/cache/summary/[page_path]

# Request again - should load from pre-generated file
curl http://localhost:8000/api/v1/content/summary/[page_path]
```

### Authentication Failed

```bash
# Verify token is valid
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"

# If expired, login again to get new token
```

### Pre-Generated Summary Not Found

If you get `404: Pre-generated summary not found`:

```bash
# Check if summary file exists
ls -la /home/user/ai-native-software-development-Tutor/book-source/static/summaries/

# Available summaries (31 files):
# - 01-Introducing-AI-Driven-Development_01-moment_that_changed_everything.md
# - 01-Introducing-AI-Driven-Development_01-billion-dollar-question.md
# - etc.
```

---

## Success Criteria

✅ **All three tabs working correctly when:**

1. **Original Tab:**
   - Returns `"ai_processed": false`
   - Content is >5000 chars
   - Response is instant (<100ms)

2. **Summary Tab:**
   - Returns `"model_version": "pre-generated-v1"`
   - Word count is 200-500
   - Second request is instant (<50ms)

3. **Personalize Tab:**
   - Returns `"model_version": "gpt-4o-mini"`
   - Profile snapshot matches user
   - Visual learners get Mermaid diagrams
   - Practical learners get code examples
   - Cached requests are instant (<100ms)

4. **Separation of Concerns:**
   - Original tab NEVER calls OLIVIA
   - Summary tab NEVER calls OLIVIA
   - Personalize tab is the ONLY tab using AI

---

## Next Steps: Frontend Integration

Once backend tests pass, implement in your React frontend:

```javascript
// Original Tab
const loadOriginalContent = async (pageId) => {
  const response = await fetch(`/api/v1/content/original/${pageId}`)
  const data = await response.json()
  // Verify: data.ai_processed === false
  renderMarkdown(data.content)
}

// Summary Tab
const loadSummary = async (pageId) => {
  const response = await fetch(`/api/v1/content/summary/${pageId}`)
  const data = await response.json()
  // Verify: data.model_version === "pre-generated-v1"
  renderSummary(data.summary_content)
}

// Personalize Tab
const loadPersonalized = async (pageId, token) => {
  if (!token) {
    showLoginModal()
    return
  }

  const response = await fetch(`/api/v1/content/personalized/${pageId}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  const data = await response.json()
  // Verify: data.model_version === "gpt-4o-mini"
  renderPersonalized(data.personalized_content)
}
```

---

**Ready to test? Run the automated suite:**
```bash
cd Tutor-Agent
python3 test_three_tabs.py
```
