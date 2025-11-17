# Claude is Work to Build this Project
<!-- Claude is Work to Build this Project -->
# Testing OLIVIA Agent Guide

Complete guide to test the RAG-powered OLIVIA AI tutor agent.

---

## Prerequisites

Before testing, make sure you have:

### 1. Dependencies Installed

```bash
cd Tutor-Agent
uv sync
```

### 2. Environment Setup

Create `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` and add your Google Gemini API key:

```env
GEMINI_API_KEY=your-actual-gemini-api-key-here
GEMINI_MODEL=gemini-2.0-flash-exp

# Other settings can stay as default for testing
JWT_SECRET_KEY=test-secret-key
DATABASE_URL=sqlite:///./data/tutorgpt.db
```

**Get your FREE Gemini API key:**
- Visit: https://ai.google.dev/gemini-api/docs/api-key
- Sign in with your Google account
- Create API key
- Gemini 2.0 Flash is FREE with high rate limits!

### 3. ChromaDB Embeddings

Make sure the book embeddings are generated:

```bash
# Check if embeddings exist
ls -lh Tutor-Agent/data/embeddings/

# If empty, you'll need to generate them (see SUMMARY_GENERATION_GUIDE.md)
```

---

## Testing Method 1: Standalone Python Script

### Quick Test (Recommended for Development)

Run the test script directly:

```bash
cd Tutor-Agent
uv run python test_olivia_agent.py
```

### What This Tests:

✅ OLIVIA agent initialization
✅ RAG search functionality
✅ Personalized content generation
✅ Streaming responses
✅ User profile adaptation

### Expected Output:

```
================================================================================
🤖 OLIVIA Agent Testing
================================================================================

✅ OpenAI API Key found
✅ OLIVIA Agent imported successfully

👤 Test User Profile:
   - Programming: intermediate
   - AI/ML: beginner
   - Learning Style: visual

================================================================================
📝 Test 1: Simple Question
================================================================================

Question: What is AI-Native Software Development?

OLIVIA Response:
--------------------------------------------------------------------------------
AI-Native Software Development is... [streaming response appears here]
--------------------------------------------------------------------------------
```

### Customize the Test:

Edit `test_olivia_agent.py` and change the mock user profile:

```python
class MockUser:
    def __init__(self):
        # Change these values!
        class ProgrammingExperience:
            value = "beginner"  # beginner, intermediate, advanced

        class AIExperience:
            value = "advanced"  # beginner, intermediate, advanced

        class LearningStyle:
            value = "hands-on"  # visual, hands-on, reading, auditory
```

---

## Testing Method 2: FastAPI Backend Endpoint

### Start the Backend Server:

```bash
cd Tutor-Agent
uv run python -m tutor_agent.main
```

You should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Test via Swagger UI (Interactive):

1. Open http://localhost:8000/api/docs
2. Find the **test-olivia** endpoint
3. Click "Try it out"
4. Enter your question:
   - `query`: "What is Claude Code?"
   - `page_path`: "02-AI-Tool-Landscape/05-claude-code-features-and-workflows" (optional)
5. Click "Execute"

### Test via cURL (Command Line):

```bash
curl -X POST "http://localhost:8000/api/v1/content/test-olivia" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is AI-Native Software Development?",
    "page_path": "01-Introducing-AI-Driven-Development"
  }'
```

### Test via Python Requests:

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/content/test-olivia",
    params={
        "query": "Explain Python type hints to me",
        "page_path": "04-Python-Fundamentals/14-data-types"
    }
)

print(response.json()["response"])
```

### Expected API Response:

```json
{
  "status": "success",
  "query": "What is AI-Native Software Development?",
  "page_path": "01-Introducing-AI-Driven-Development",
  "response": "AI-Native Software Development is a paradigm shift...",
  "user_profile": {
    "programming": "intermediate",
    "ai_experience": "beginner",
    "learning_style": "visual"
  },
  "note": "This is a test endpoint using a mock user profile"
}
```

---

## What to Test

### 1. Basic Question Answering

```python
Query: "What is Claude Code?"
Expected: OLIVIA should search the book and provide accurate info
```

### 2. RAG Search Verification

```python
Query: "What are the key features of uv package manager?"
Expected: OLIVIA should cite specific sections from the book
```

### 3. Personalization

```python
# Test with different user profiles
# Beginner should get simpler explanations
# Advanced should get deeper technical details
Query: "Explain async/await in Python"
```

### 4. Context Awareness

```python
# Provide page_path for better context
Query: "Give me an example of this concept"
page_path: "04-Python-Fundamentals/28-asyncio/01-asyncio-foundations"
```

### 5. Error Handling

```python
# Test with topic not in book
Query: "How do I build a rocket ship?"
Expected: OLIVIA should acknowledge it's not in the book content
```

---

## Troubleshooting

### ❌ Error: "GEMINI_API_KEY not found"

**Solution**: Create `.env` file with your Gemini API key

```bash
cd Tutor-Agent
cp .env.example .env
# Edit .env and add: GEMINI_API_KEY=your-key-here
```

Get your free key at: https://ai.google.dev/gemini-api/docs/api-key

### ❌ Error: "ModuleNotFoundError: No module named 'agents'"

**Solution**: Install dependencies

```bash
cd Tutor-Agent
uv sync
```

### ❌ Error: "ChromaDB collection not found"

**Solution**: Generate book embeddings first

```bash
cd Tutor-Agent
uv run python scripts/generate_summaries.py
```

### ❌ Slow responses

**Cause**: RAG search + Gemini API calls take time
**Normal**: 2-8 seconds for first response
**Tip**: `gemini-2.0-flash-exp` is already the fastest free model available!

---

## Understanding the Output

### When Testing via Script:

```
OLIVIA Response:
--------------------------------------------------------------------------------
AI-Native Software Development is a paradigm that treats AI as a first-class
citizen in the development process...
                                      ^^^^^^
                            Streamed in real-time
--------------------------------------------------------------------------------
```

### When Testing via API:

```json
{
  "response": "Full response here",  // ← Complete answer
  "query": "Your question",
  "page_path": "Context used",
  "user_profile": {...}  // ← How OLIVIA personalized
}
```

---

## Next Steps

After successful testing:

1. ✅ **Verify RAG is working**: Check that responses cite specific book sections
2. ✅ **Test personalization**: Try different user profiles
3. ✅ **Integrate with frontend**: Use the `/test-olivia` endpoint from your React app
4. ✅ **Add authentication**: Move to the full `/personalized` endpoint with user auth

---

## Production Considerations

⚠️ **Note**: The `/test-olivia` endpoint is for development/testing only!

For production:
- Use the authenticated `/personalized/{page_path}` endpoint
- Require JWT tokens
- Cache responses per user
- Monitor API usage (Gemini 2.0 Flash is FREE with generous rate limits!)

---

## Support

If you encounter issues:

1. Check the logs: `uv run python -m tutor_agent.main` (backend logs)
2. Verify Gemini API key is valid at https://aistudio.google.com/app/apikey
3. Ensure ChromaDB embeddings exist
4. Check Python version: `python --version` (should be 3.11+)
5. Test Gemini API directly: `curl https://generativelanguage.googleapis.com/v1beta/models?key=YOUR_API_KEY`

---

**Happy Testing! 🚀**

OLIVIA is ready to help your students learn AI-Native Software Development!
