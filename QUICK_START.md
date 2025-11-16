<!-- Claude is Work to Build this Project -->
# 🚀 Quick Start for Next Developer

**⏱️ 5-Minute Onboarding Guide**

---

## 📖 Read These Files IN ORDER:

1. **START HERE** → `STATUS.md` (2 min read)
   - High-level overview
   - What's done vs. pending

2. **THEN READ** → `HANDOFF.md` (10 min read)
   - Complete implementation guide
   - API documentation
   - Step-by-step instructions

3. **FINALLY REVIEW** → `specs/001-tutorgpt-platform/tasks.md`
   - All user stories
   - Acceptance criteria

---

## ⚡ Get Running in 5 Minutes

### Step 1: Backend (2 min)
```bash
cd Tutor-Agent
cp .env.example .env
# Edit .env: Add OPENAI_API_KEY=sk-your-key-here
uv sync
uv run python -m tutor_agent.main
```
✅ Backend running on `http://localhost:8000`

### Step 2: Frontend (2 min)
```bash
cd book-source
npm install
npm start
```
✅ Frontend running on `http://localhost:3000`

### Step 3: Test (1 min)
- Open browser: `http://localhost:3000`
- Click any lesson → See 3 tabs (Original, Summary, Personalized)
- Summary tab works ✅
- Personalized tab shows "Login required" ⏳ ← **YOUR JOB**

---

## 🎯 Your Mission

**Build the PersonalizedTab frontend UI**

### What You Need To Create:
1. `book-source/src/components/PersonalizedTab/LoginForm.tsx`
2. `book-source/src/components/PersonalizedTab/SignupForm.tsx`
3. `book-source/src/components/PersonalizedTab/PersonalizedContent.tsx`
4. Update `book-source/src/components/PersonalizedTab/index.tsx`

### How It Should Work:
```
User clicks "Personalized" tab
  ↓
NOT logged in? → Show signup/login form
  ↓
User signs up → Answers 4 questions:
  1. Programming experience (beginner/intermediate/advanced)
  2. AI/ML experience (none/basic/intermediate/advanced)
  3. Learning style (visual/practical/conceptual/mixed)
  4. Preferred language (en/es/fr/de/zh/ja)
  ↓
Get JWT token → Store in localStorage
  ↓
Fetch personalized content from backend
  ↓
Display adapted markdown content
```

---

## 📋 Implementation Checklist

```
[ ] Create LoginForm.tsx
    - Email + password inputs
    - Call POST /api/v1/auth/login
    - Store JWT in localStorage

[ ] Create SignupForm.tsx
    - Email + password inputs
    - 4 profile questions (radio buttons + dropdown)
    - Call POST /api/v1/auth/signup
    - Store JWT in localStorage

[ ] Update PersonalizedTab/index.tsx
    - Check if user logged in (JWT in localStorage)
    - If not → Show LoginForm or SignupForm
    - If yes → Show PersonalizedContent

[ ] Create PersonalizedContent.tsx
    - Fetch from GET /api/v1/content/personalized/{page_path}
    - Include Authorization: Bearer {token} header
    - Display markdown content
    - Handle loading/error states

[ ] Test complete flow
    - Signup → Login → View personalized content
    - Logout → Login again
    - Token expiration handling
```

---

## 🔌 API Quick Reference

**Base URL**: `http://localhost:8000`

### Signup
```typescript
POST /api/v1/auth/signup
{
  email: string,
  password: string,
  programming_experience: "beginner" | "intermediate" | "advanced",
  ai_experience: "none" | "basic" | "intermediate" | "advanced",
  learning_style: "visual" | "practical" | "conceptual" | "mixed",
  preferred_language: "en" | "es" | "fr" | "de" | "zh" | "ja"
}
→ Returns: { access_token, user }
```

### Login
```typescript
POST /api/v1/auth/login
{ email: string, password: string }
→ Returns: { access_token, user }
```

### Get Personalized Content
```typescript
GET /api/v1/content/personalized/{page_path}
Headers: { Authorization: "Bearer {token}" }
→ Returns: { markdown_content, cached, generated_at }
```

**Full API docs**: `http://localhost:8000/api/docs`

---

## 🎨 UI Reference

Look at existing **SummaryTab** component for patterns:
- File: `book-source/src/components/SummaryTab/index.tsx`
- It fetches data, shows loading state, renders markdown
- Use similar approach for PersonalizedTab

---

## 🐛 Common Issues

**Backend won't start**:
```bash
# Missing OpenAI key
echo "OPENAI_API_KEY=sk-your-key" >> .env

# Missing dependencies
uv sync
```

**CORS errors**:
- Backend already allows `localhost:3000`
- If you change port, update `Tutor-Agent/src/tutor_agent/main.py` line 28

**401 Unauthorized**:
- Token expired (7 days)
- Clear localStorage and login again

---

## 💡 Pro Tips

1. **Use existing SummaryTab as template** - same fetch pattern
2. **Test backend with curl first** - verify APIs work
3. **Store user data in localStorage** - for profile display
4. **Handle token expiration** - clear storage on 401 errors
5. **Add loading skeletons** - better UX while fetching

---

## 📞 Need Help?

1. **Read HANDOFF.md** - It has EVERYTHING
2. **Check API docs** - `http://localhost:8000/api/docs`
3. **Review existing code** - SummaryTab component
4. **Test backend manually** - Use curl or Postman

---

## ✅ Definition of Done

Your work is complete when:
- [ ] User can sign up with 4 questions
- [ ] User can login
- [ ] User sees personalized content on any lesson page
- [ ] Content is different based on profile (test with different profiles)
- [ ] Logout works (clear localStorage)
- [ ] Token expiration handled gracefully
- [ ] No console errors
- [ ] Code is clean and commented

---

## 🎉 You Got This!

**Backend is DONE** ✅
**Your job**: Build the React UI

**Estimated time**: 4-6 hours
- LoginForm: 1 hour
- SignupForm: 2 hours (4 questions + validation)
- PersonalizedTab logic: 1 hour
- PersonalizedContent: 1 hour
- Testing + polish: 1 hour

**Start with**: LoginForm.tsx (easiest)
**Then**: SignupForm.tsx (most complex)
**Finally**: Wire everything together

Good luck! 🚀
