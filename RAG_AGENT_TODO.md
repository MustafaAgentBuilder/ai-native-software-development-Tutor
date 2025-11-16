<!-- Claude is Work to Build this Project -->
# 🤖 RAG-Powered OLIVIA Agent - Implementation TODO

**Status**: Ready to implement
**Embeddings**: ✅ Copied to `Tutor-Agent/data/embeddings/`
**Dependencies**: ✅ chromadb added to pyproject.toml (needs `uv sync`)

---

## 📋 Implementation Checklist

### Step 1: Install ChromaDB ⏳
```bash
cd Tutor-Agent
uv sync
```

### Step 2: Create RAG Service ⏳
**File**: `Tutor-Agent/src/tutor_agent/services/rag_service.py`

```python
"""
RAG (Retrieval Augmented Generation) service using Chrom