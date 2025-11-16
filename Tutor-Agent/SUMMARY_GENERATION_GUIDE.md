<!-- Claude is Work to Build this Project -->
# OLIVIA Summary Generation Guide

This guide explains how to use OLIVIA (the AI tutor agent) to generate summaries for all Part 1 pages of the book.

## Prerequisites

1. **OpenAI API Key**: You need an OpenAI API key with access to GPT-4o-mini or GPT-4o

2. **UV Package Manager**: Already installed (used for dependency management)

## Setup

### 1. Configure API Key

Create a `.env` file in the `Tutor-Agent/` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 2. Install Dependencies

The script will auto-install dependencies, but you can manually install:

```bash
cd Tutor-Agent
uv add openai pydantic
```

## Usage

### Test with Single Page (Recommended First)

```bash
cd Tutor-Agent
uv run python scripts/generate_summaries.py --test
```

This will:
- Process one page as a test
- Show you the generated summary
- Display token usage and generation time
- Verify everything works before processing all pages

### Generate First 5 Summaries

```bash
uv run python scripts/generate_summaries.py --limit 5
```

### Generate All 177 Summaries

```bash
uv run python scripts/generate_summaries.py
```

**Expected Time**: ~5-10 minutes for all 177 pages
**Expected Cost**: ~$2-5 (using GPT-4o-mini)

### Regenerate Existing Summaries

```bash
uv run python scripts/generate_summaries.py --no-skip
```

## Output

Summaries are saved to: `Tutor-Agent/data/generated_summaries/`

Each page gets two files:
1. **Summary Markdown**: `<page-name>.md` with front matter and summary
2. **Metadata JSON**: `<page-name>.md.meta.json` with generation details

### Example Output

**Summary File** (`01-Introducing-AI-Driven-Development_01-ai-development-revolution_01-moment_that_changed_everything.md`):

```markdown
---
original: 01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything.md
chapter: 01-Introducing-AI-Driven-Development
generated_at: 2025-11-15T10:30:00
model: gpt-4o-mini
difficulty: beginner
read_time: 5 min
---

# Summary

This chapter introduces the revolutionary shift in software development...
(200-400 words)

## Key Concepts

- AI-driven development fundamentals
- The paradigm shift in coding
- Developer productivity transformation
```

**Metadata File** (`.meta.json`):

```json
{
  "page_path": "...",
  "chapter": "01-Introducing-AI-Driven-Development",
  "generated_at": "2025-11-15T10:30:00",
  "model_used": "gpt-4o-mini",
  "tokens_used": 856,
  "generation_time_ms": 1234
}
```

## OLIVIA Agent Details

The script uses the **OLIVIA** agent with:

- **Framework**: ACILPR (Actor, Context, Instruction, Limitations, Persona, Response Format)
- **Model**: GPT-4o-mini (fast and cost-effective)
- **Structured Output**: Pydantic models ensure consistent format
- **Cognitive Control**: Self-verification before output
- **Temperature**: 0.3 (low for consistency)
- **Word Limit**: Strict 200-400 words per summary

### OLIVIA's Capabilities

OLIVIA is specifically designed to:
- Analyze educational technical content
- Extract key concepts
- Generate pedagogically sound summaries
- Preserve technical accuracy
- Adapt to different difficulty levels
- Estimate reading time

## Monitoring Progress

The script shows real-time progress:

```
📝 [15/177] Processing: 02-AI-Tool-Landscape/05-claude-code-features/01-origin-story.md
   ✅ Summary saved: 02-AI-Tool-Landscape_05-claude-code-features_01-origin-story.md
   📊 Tokens: 623 | Time: 1456ms
   🎯 Difficulty: intermediate | Read time: 4 min
```

## Final Statistics

After completion, you'll see:

```
============================================================
📊 Summary Generation Complete!
============================================================
✅ Success: 175
❌ Failed: 0
⏭️  Skipped: 2
📊 Total pages: 177
🪙 Total tokens used: 98,456
⏱️  Total time: 287.45s
⚡ Avg time per page: 1641ms
============================================================
```

## Troubleshooting

### Error: "Incorrect API key provided"

**Solution**: Check that `OPENAI_API_KEY` in `.env` is correct and starts with `sk-`

### Error: "Rate limit exceeded"

**Solution**: The script has 0.5s delay between requests. If still hitting limits, increase the delay in the script.

### Error: "Module not found"

**Solution**: Reinstall dependencies:
```bash
uv sync
uv add openai pydantic
```

### Empty or Short Pages Skipped

This is normal. The script skips pages with less than 50 characters.

## Next Steps

After generating summaries:

1. **Review Sample Summaries**: Check a few generated summaries for quality
2. **Integrate with Frontend**: Update frontend to load summaries from this directory
3. **Create RAG Tool**: Set up embeddings for OLIVIA's RAG-based personalization
4. **Test Summary Tab**: Verify the three-tab interface loads summaries correctly

## Cost Estimation

Using GPT-4o-mini:
- Average tokens per page: ~500-800
- Cost: ~$0.01-0.02 per page
- Total for 177 pages: ~$2-5

## Related Files

- **Script**: `scripts/generate_summaries.py`
- **Output Directory**: `data/generated_summaries/`
- **Config**: `.env` (create from `.env.example`)
- **Tasks**: `../specs/001-tutorgpt-platform/tasks.md` (T033-T035)
