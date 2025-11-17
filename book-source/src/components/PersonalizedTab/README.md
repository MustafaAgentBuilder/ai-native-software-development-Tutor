# PersonalizedTab Component

AI-powered personalized learning feature powered by **OLIVIA AI Tutor** with user authentication and profile-based content adaptation.

## Features

✅ User authentication (signup + login)
✅ 4-question learning profile system
✅ Personalized content generation using OpenAI
✅ Content caching with profile-aware invalidation
✅ Adaptive prompting based on user profile
✅ JWT token management
✅ Beautiful UI with loading states

## Usage

### In MDX Pages

```mdx
---
title: "My Page Title"
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import SummaryTab from '@site/src/components/SummaryTab';
import PersonalizedTab from '@site/src/components/PersonalizedTab';

<Tabs>
  <TabItem value="original" label="📖 Original" default>
    # Original Content
    Full page content goes here...
  </TabItem>

  <TabItem value="summary" label="📝 Summary">
    <SummaryTab pagePath="01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything" />
  </TabItem>

  <TabItem value="personalized" label="✨ Personalized">
    <PersonalizedTab pagePath="01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything" />
  </TabItem>
</Tabs>
```

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `pagePath` | `string` | ✅ Yes | Relative path from `docs/` without `.md` extension |

## Components

### 1. PersonalizedTab (Main)
- Manages auth state
- Shows login/signup or personalized content
- Routes between auth forms and content display

### 2. LoginForm
- Email + password login
- Switch to signup
- Error handling

### 3. SignupForm
- Email, password, confirm password
- 4 profile questions:
  1. Programming Experience (beginner/intermediate/advanced)
  2. AI/ML Experience (none/basic/intermediate/advanced)
  3. Learning Style (visual/practical/conceptual/mixed)
  4. Preferred Language (en/es/fr/de/zh/ja)
- Optional: Full name
- Switch to login

### 4. PersonalizedContent
- Fetches personalized content from backend
- Shows loading state during generation
- Displays user profile summary
- Renders markdown content
- Shows cache status
- Logout button

## Backend Integration

### API Endpoints Used

**Authentication:**
- `POST /api/v1/auth/signup` - Create account
- `POST /api/v1/auth/login` - Get JWT token
- `GET /api/v1/auth/me` - Validate token

**Content:**
- `GET /api/v1/content/personalized/{page_path}` - Get personalized content

### Authentication Flow

```
User clicks "Personalized" tab
    ↓
NOT logged in? → Show login/signup form
    ↓
User fills form → API call → JWT token saved to localStorage
    ↓
Logged in? → Fetch personalized content → Display
    ↓
Content cached? → Return cached version
Content not cached? → Generate with OpenAI → Cache → Return
```

## Local Storage

| Key | Value | Description |
|-----|-------|-------------|
| `tutorgpt_token` | JWT string | Authentication token (7-day expiration) |
| `tutorgpt_user` | JSON object | User profile data |

## Styling

Uses CSS modules (`styles.module.css`) with Docusaurus theme variables.

**Key Classes:**
- `.authForm` - Login/signup container
- `.personalizedContainer` - Personalized content container
- `.markdownContent` - Rendered markdown
- `.loadingState` - Loading spinner
- `.errorState` - Error messages

## States

### 1. Not Authenticated
Shows login form by default, with option to switch to signup.

### 2. Signup Form
- Collects basic info (email, password)
- Asks 4 profile questions
- Creates account → Auto-login

### 3. Login Form
- Email + password
- Validates token on submit

### 4. Loading Personalized Content
- Shows spinner
- Displays "OLIVIA is personalizing..."
- Shows user profile summary

### 5. Personalized Content Loaded
- Displays user email + logout button
- Shows cache status badge
- Displays profile banner
- Renders personalized markdown
- Footer with OLIVIA attribution

### 6. Error State
- Shows error message
- Retry button

## Backend Requirements

**Environment Variables:**
```env
OPENAI_API_KEY=sk-...your-key...
OPENAI_MODEL=gpt-4o-mini
JWT_SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./data/tutorgpt.db
```

**Start Backend:**
```bash
cd Tutor-Agent
uv run python -m tutor_agent.main
```

Backend runs on `http://localhost:8000`

## Testing

### 1. Test Signup Flow
1. Navigate to any lesson page
2. Click "Personalized" tab
3. Click "Sign up" link
4. Fill in email, password, confirm password
5. Answer 4 profile questions
6. Click "Create Account"
7. Should auto-login and show personalized content

### 2. Test Login Flow
1. Navigate to any lesson page
2. Click "Personalized" tab
3. Enter email and password
4. Click "Log In"
5. Should show personalized content

### 3. Test Logout
1. While logged in, click "Logout" button
2. Should return to login form
3. localStorage should be cleared

### 4. Test Content Generation
1. Login and view personalized content
2. First time: Should take 10-20 seconds (generating)
3. Second time: Should load instantly (cached)
4. Change profile (requires backend update): Should regenerate

## Known Issues & Limitations

1. **No Profile Update UI**: Users can't change their profile after signup (requires new feature)
2. **No Password Reset**: Forgot password functionality not implemented
3. **No Regenerate Button**: Users can't manually request new personalized content
4. **Session Expiration**: Token expires after 7 days, no auto-refresh

## Future Enhancements

🔮 **Planned Features:**
- User profile settings page
- Password reset functionality
- Content regeneration button
- Progress tracking
- Real-time streaming (WebSocket)
- Interactive "Ask OLIVIA" feature
- Social auth (Google, GitHub)
- Multi-language UI (currently only content is translated)

## Technical Details

- **Framework**: React 19 + TypeScript
- **Styling**: CSS Modules with Docusaurus theme variables
- **State Management**: React Hooks (useState, useEffect)
- **Auth**: JWT tokens in localStorage
- **API Client**: Fetch API with custom service layer
- **Markdown Rendering**: react-markdown
- **Backend**: FastAPI + SQLAlchemy + OpenAI Agents SDK

## File Structure

```
src/components/PersonalizedTab/
├── index.tsx                  # Main component
├── LoginForm.tsx              # Login form
├── SignupForm.tsx             # Signup form with 4 questions
├── PersonalizedContent.tsx    # Content display
├── styles.module.css          # Styling
└── README.md                  # This file

src/services/
└── api.ts                     # API client

src/hooks/
└── useAuth.ts                 # Authentication hook
```

## Dependencies

```json
{
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "react-markdown": "^9.0.0"
}
```

## Support

For issues or questions:
- Check backend logs: `Tutor-Agent/` terminal
- Check browser console: F12 → Console
- Check localStorage: F12 → Application → Local Storage
- Verify backend is running: `http://localhost:8000/health`
- API docs: `http://localhost:8000/api/docs`

## Credits

Built with ❤️ by Claude AI Assistant
Powered by OLIVIA AI Tutor (OpenAI GPT-4o-mini)
