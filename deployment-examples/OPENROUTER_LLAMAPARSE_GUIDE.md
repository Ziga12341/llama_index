# OpenRouter + LlamaParse Integration Guide

This guide shows you how to use **OpenRouter** for LLM responses and **LlamaParse** for advanced PDF parsing with vision capabilities.

## Table of Contents

- [Overview](#overview)
- [Why This Combination?](#why-this-combination)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Advanced PDF Parsing](#advanced-pdf-parsing)
- [Model Selection](#model-selection)
- [Cost Comparison](#cost-comparison)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

---

## Overview

### What You Get

✅ **OpenRouter**: Access to 200+ AI models from a single API
- GPT-4, Claude 3.5 Sonnet, Llama 3.1, Gemini, Mistral, and more
- Unified API for all models
- Competitive pricing
- No vendor lock-in

✅ **LlamaParse**: Advanced PDF parsing with vision
- Extract tables accurately as markdown
- Parse forms and structured data
- Describe images, charts, and diagrams with vision models
- Handle complex multi-column layouts
- Custom parsing instructions

---

## Why This Combination?

### Problem 1: Basic PDF Parsing Struggles
**Simple PDF parsers (PyPDF) fail with:**
- ❌ Tables become garbled text
- ❌ Multi-column layouts are scrambled
- ❌ Forms lose structure
- ❌ Images and charts are ignored

**Solution: LlamaParse**
- ✅ Uses vision-capable LLMs to understand document structure
- ✅ Converts tables to proper markdown
- ✅ Describes images and charts
- ✅ Preserves document hierarchy

### Problem 2: Expensive OpenAI API Costs
**OpenAI API pricing:**
- GPT-4: $30/1M input tokens
- Limited model choices
- No access to Claude, Llama, etc.

**Solution: OpenRouter**
- 200+ models at competitive prices
- GPT-4 Turbo: $10/1M input tokens (3x cheaper!)
- Access to Claude 3.5 Sonnet, Llama 3.1 70B, and more
- Switch models anytime without code changes

### Why Not Use OpenRouter for PDF Parsing Too?

You *could* use vision models through OpenRouter to parse PDFs manually, but:

- **LlamaParse** is purpose-built for document parsing
- It handles batch processing, pagination, and caching
- Custom parsing instructions are optimized
- Free tier: 1,000 pages/day
- Only $0.003 per page after that

**Recommendation**: Use OpenRouter for queries/chat + LlamaParse for PDF parsing

---

## Quick Start

### 1. Get API Keys

#### OpenRouter (for LLM)
```bash
# 1. Go to https://openrouter.ai/keys
# 2. Sign up (free)
# 3. Create an API key
# 4. Add $5 credits (you get ~500K GPT-4-turbo tokens)
```

#### LlamaParse (for PDF parsing)
```bash
# 1. Go to https://cloud.llamaindex.ai/
# 2. Sign up (free)
# 3. Go to API Keys section
# 4. Create an API key
# Free tier: 1,000 pages/day
```

#### OpenAI (optional, for embeddings)
```bash
# Optional: Get from https://platform.openai.com/api-keys
# You can use OpenRouter for embeddings too, but OpenAI embeddings are excellent
```

### 2. Configure Environment

```bash
cd deployment-examples

# Copy example config
cp .env.example .env

# Edit .env with your keys
nano .env
```

**Required settings in `.env`:**

```bash
# Use OpenRouter for LLM
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-your-openrouter-key-here

# Optional: OpenAI for embeddings (or use OpenRouter)
OPENAI_API_KEY=sk-your-openai-key-here

# Enable LlamaParse for advanced PDF parsing
LLAMA_CLOUD_API_KEY=llx-your-llamaparse-key-here
USE_LLAMA_PARSE=true

# Choose your model (see Model Selection below)
LLM_MODEL=openai/gpt-4-turbo
```

### 3. Install Dependencies

```bash
# Install all dependencies including OpenRouter and LlamaParse
pip install -r requirements.txt

# Or with Docker
docker-compose up --build -d
```

### 4. Start the Server

```bash
# Without Docker
uvicorn api_server:app --reload --port 8000

# With Docker
docker-compose up -d

# Check health
curl http://localhost:8000/health
```

---

## Configuration

### Environment Variables

```bash
# ========================================
# LLM Provider Selection
# ========================================
LLM_PROVIDER=openrouter  # "openrouter" or "openai"

# ========================================
# API Keys
# ========================================
OPENROUTER_API_KEY=sk-or-v1-...  # Required if LLM_PROVIDER=openrouter
OPENAI_API_KEY=sk-...             # Optional (for embeddings)
LLAMA_CLOUD_API_KEY=llx-...       # Required for advanced PDF parsing

# ========================================
# Model Configuration
# ========================================
LLM_MODEL=openai/gpt-4-turbo      # See Model Selection section
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=512

EMBEDDING_MODEL=text-embedding-3-small  # OpenAI embeddings (recommended)

# ========================================
# PDF Parsing
# ========================================
USE_LLAMA_PARSE=true  # Enable advanced PDF parsing
```

### Model Configuration Priority

**For LLM (queries/chat):**
1. ✅ **Recommended**: OpenRouter (access to 200+ models)
2. Alternative: OpenAI direct (if you already have credits)

**For Embeddings:**
1. ✅ **Recommended**: OpenAI embeddings (`text-embedding-3-small`)
   - Best quality
   - Very affordable ($0.13/1M tokens)
2. Alternative: OpenRouter embeddings

**For PDF Parsing:**
1. ✅ **Recommended**: LlamaParse (purpose-built, vision support)
2. Alternative: Simple parser (free, but basic)

---

## Advanced PDF Parsing

### Using the API

#### Parse a PDF with Vision (Default)

```bash
# Upload and parse PDF with LlamaParse
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@financial_report.pdf" \
  -F "parsing_instruction=Extract all tables and describe any charts or images" \
  -F "use_llamaparse=true"
```

**Response:**
```json
{
  "status": "success",
  "filename": "financial_report.pdf",
  "num_pages": 15,
  "parser_used": "llamaparse",
  "content": [
    "# Financial Report Q4 2024\n\n## Revenue Table\n\n| Quarter | Revenue | Growth |\n|---------|---------|--------|\n| Q3      | $1.2M   | +15%   |\n| Q4      | $1.5M   | +25%   |\n\n## Growth Chart\n[Image description: Bar chart showing quarterly revenue growth from Q1 to Q4, with Q4 showing the highest bar at $1.5M]",
    "..."
  ],
  "metadata": [...]
}
```

### Custom Parsing Instructions

```bash
# For financial documents
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@financial_statement.pdf" \
  -F "parsing_instruction=Extract all tables with numbers precisely. Maintain column alignment. Describe any charts or graphs in detail. Ignore page numbers and headers." \
  -F "use_llamaparse=true"

# For forms
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@application_form.pdf" \
  -F "parsing_instruction=Extract field names and their values. Preserve checkbox states. Describe any signature fields or images." \
  -F "use_llamaparse=true"

# For research papers
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@research_paper.pdf" \
  -F "parsing_instruction=Preserve citations and references. Extract figures and their captions. Describe any diagrams or charts. Maintain section hierarchy." \
  -F "use_llamaparse=true"
```

### Python Example

```python
import requests

# Parse PDF with custom instructions
with open("financial_report.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/parse-pdf",
        files={"file": f},
        data={
            "parsing_instruction": "Extract all financial tables. Describe any charts or graphs with specific numbers.",
            "use_llamaparse": True
        }
    )

result = response.json()
print(f"Parsed {result['num_pages']} pages using {result['parser_used']}")

# Print content
for i, page_content in enumerate(result['content']):
    print(f"\n--- Page {i+1} ---")
    print(page_content[:500])  # First 500 chars
```

### Full Workflow: Parse + Index + Query

```python
import requests

# 1. Parse PDF with vision
with open("financial_report.pdf", "rb") as f:
    parse_response = requests.post(
        "http://localhost:8000/parse-pdf",
        files={"file": f},
        data={"parsing_instruction": "Extract all tables and describe charts"}
    )

print(f"✅ Parsed: {parse_response.json()['filename']}")

# 2. Upload for indexing
with open("financial_report.pdf", "rb") as f:
    upload_response = requests.post(
        "http://localhost:8000/upload",
        files={"file": f}
    )

print("✅ Uploaded for indexing")

# 3. Index the documents
ingest_response = requests.post("http://localhost:8000/ingest")
print("✅ Indexed documents")

# 4. Query using OpenRouter LLM
query_response = requests.post(
    "http://localhost:8000/query",
    json={
        "query": "What was the revenue in Q4? Describe the trend shown in the growth chart.",
        "stream": False
    }
)

print("\n📊 Answer:")
print(query_response.json()['response'])
```

---

## Model Selection

### Popular OpenRouter Models

#### Best Overall: GPT-4 Turbo
```bash
LLM_MODEL=openai/gpt-4-turbo
```
- **Cost**: $10/1M input tokens (3x cheaper than OpenAI direct)
- **Quality**: Excellent
- **Speed**: Fast
- **Best for**: Production, balanced cost/quality

#### Best Value: Llama 3.1 70B
```bash
LLM_MODEL=meta-llama/llama-3.1-70b-instruct
```
- **Cost**: $0.52/1M input tokens (60x cheaper!)
- **Quality**: Very good
- **Speed**: Very fast
- **Best for**: High volume, cost-sensitive applications

#### Best Reasoning: Claude 3.5 Sonnet
```bash
LLM_MODEL=anthropic/claude-3.5-sonnet
```
- **Cost**: $15/1M input tokens
- **Quality**: Excellent reasoning and analysis
- **Speed**: Fast
- **Best for**: Complex analysis, technical documents

#### Vision Support: GPT-4o
```bash
LLM_MODEL=openai/gpt-4o
```
- **Cost**: $5/1M input tokens
- **Quality**: Excellent with vision
- **Speed**: Very fast
- **Best for**: Documents with images/charts

#### Budget Option: Mixtral 8x7B
```bash
LLM_MODEL=mistralai/mixtral-8x7b-instruct
```
- **Cost**: $0.54/1M input tokens
- **Quality**: Good
- **Speed**: Very fast
- **Best for**: Simple queries, high volume

### Full Model List

See all available models and pricing: https://openrouter.ai/models

### Switching Models

**No code changes needed!** Just update `.env`:

```bash
# Try different models
LLM_MODEL=openai/gpt-4-turbo
# LLM_MODEL=anthropic/claude-3.5-sonnet
# LLM_MODEL=meta-llama/llama-3.1-70b-instruct
# LLM_MODEL=google/gemini-pro-1.5

# Restart server
docker-compose restart app
```

---

## Cost Comparison

### Scenario: Processing 100 Financial PDFs

**Assumptions:**
- 100 PDFs, 10 pages each = 1,000 pages
- 1,000 queries with 2K input + 500 output tokens each

#### Option 1: OpenAI Direct + Simple Parser
```
LLM (GPT-4):
  Input:  2M tokens × $30  = $60
  Output: 0.5M tokens × $60 = $30
PDF Parsing (Simple): Free
TOTAL: $90

❌ Tables are garbled
❌ Images ignored
```

#### Option 2: OpenAI Direct + LlamaParse
```
LLM (GPT-4):
  Input:  2M tokens × $30  = $60
  Output: 0.5M tokens × $60 = $30
PDF Parsing (LlamaParse):
  1,000 pages × $0.003 = $3
TOTAL: $93

✅ Perfect table extraction
✅ Image descriptions
```

#### Option 3: OpenRouter + LlamaParse (Recommended!)
```
LLM (GPT-4 Turbo via OpenRouter):
  Input:  2M tokens × $10  = $20
  Output: 0.5M tokens × $30 = $15
PDF Parsing (LlamaParse):
  1,000 pages × $0.003 = $3
TOTAL: $38 (59% SAVINGS!)

✅ Perfect table extraction
✅ Image descriptions
✅ 3x cheaper LLM costs
```

#### Option 4: OpenRouter (Budget) + LlamaParse
```
LLM (Llama 3.1 70B via OpenRouter):
  Input:  2M tokens × $0.52  = $1.04
  Output: 0.5M tokens × $0.80 = $0.40
PDF Parsing (LlamaParse):
  1,000 pages × $0.003 = $3
TOTAL: $4.44 (95% SAVINGS!)

✅ Perfect table extraction
✅ Image descriptions
✅ 60x cheaper LLM costs
```

### LlamaParse Free Tier

**Free tier: 1,000 pages/day**

Perfect for:
- Development and testing
- Small projects (<30K pages/month)
- Daily document processing

**After free tier: $0.003/page**
- 1,000 pages: $3
- 10,000 pages: $30
- 100,000 pages: $300

---

## Examples

### Example 1: Financial Report Analysis

```bash
# Parse financial report with table extraction
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@quarterly_report.pdf" \
  -F "parsing_instruction=Extract all financial tables precisely. Describe any charts showing trends or comparisons."

# Index it
curl -X POST http://localhost:8000/upload -F "file=@quarterly_report.pdf"
curl -X POST http://localhost:8000/ingest

# Query with OpenRouter (using Claude for financial analysis)
export LLM_MODEL=anthropic/claude-3.5-sonnet

curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Compare revenue growth between Q3 and Q4. What does the trend chart indicate?"
  }'
```

### Example 2: Research Paper with Diagrams

```bash
# Parse research paper, describe diagrams
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@research_paper.pdf" \
  -F "parsing_instruction=Preserve all citations. Extract figures and describe diagrams in detail. Maintain equation formatting."

# Query with GPT-4o (has vision understanding)
export LLM_MODEL=openai/gpt-4o

curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain the methodology shown in Figure 2 and how it relates to the results in Table 3."
  }'
```

### Example 3: Form Extraction

```bash
# Parse filled form
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@application_form.pdf" \
  -F "parsing_instruction=Extract all field names and their filled values. Note checkbox states. Describe any signature or image fields."

# Use budget model for simple extraction
export LLM_MODEL=meta-llama/llama-3.1-70b-instruct

curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the applicant name, email, and which checkboxes were selected?"
  }'
```

### Example 4: Invoice Processing (Batch)

```python
import requests
import glob

# Process all invoices
for pdf_path in glob.glob("invoices/*.pdf"):
    print(f"Processing {pdf_path}...")

    # Parse with LlamaParse
    with open(pdf_path, "rb") as f:
        response = requests.post(
            "http://localhost:8000/parse-pdf",
            files={"file": f},
            data={
                "parsing_instruction": "Extract invoice number, date, total amount, and itemized charges table.",
                "use_llamaparse": True
            }
        )

    result = response.json()

    # Upload for indexing
    with open(pdf_path, "rb") as f:
        requests.post("http://localhost:8000/upload", files={"file": f})

# Index all
requests.post("http://localhost:8000/ingest")

# Query with budget model (Llama 3.1 70B)
response = requests.post(
    "http://localhost:8000/query",
    json={"query": "What is the total amount across all invoices? Which vendor had the highest charges?"}
)

print(response.json()['response'])
```

---

## Troubleshooting

### LlamaParse Issues

#### Issue: "LLAMA_CLOUD_API_KEY not set"
```bash
# Check your .env file
cat .env | grep LLAMA_CLOUD_API_KEY

# Make sure it's set
export LLAMA_CLOUD_API_KEY=llx-your-key-here

# Restart server
docker-compose restart app
```

#### Issue: "LlamaParse quota exceeded"
```bash
# Free tier: 1,000 pages/day
# Solution: Wait 24 hours or upgrade plan

# Or use simple parser temporarily
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@document.pdf" \
  -F "use_llamaparse=false"
```

#### Issue: Tables not extracted properly
```bash
# Add specific parsing instructions
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@document.pdf" \
  -F "parsing_instruction=CRITICAL: Convert ALL tables to markdown format. Preserve all rows and columns exactly. Do not summarize."
```

### OpenRouter Issues

#### Issue: "Invalid API key"
```bash
# Verify your key
curl https://openrouter.ai/api/v1/auth/key \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"

# Should return: {"data": {"label": "..."}}
```

#### Issue: "Insufficient credits"
```bash
# Check balance
curl https://openrouter.ai/api/v1/auth/key \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"

# Add credits at https://openrouter.ai/credits
```

#### Issue: "Model not available"
```bash
# Check available models
curl https://openrouter.ai/api/v1/models

# Use a different model
LLM_MODEL=openai/gpt-4-turbo  # Usually available
```

### Embedding Issues

#### Issue: "OpenAI embeddings not working with OpenRouter"
```bash
# Option 1: Add OpenAI API key for embeddings only
OPENAI_API_KEY=sk-your-openai-key

# Option 2: Use local embeddings (free, but slower)
# TODO: Add local embedding configuration
```

### Performance Issues

#### Slow PDF parsing
```bash
# LlamaParse can be slow for large PDFs (30-60 seconds)
# This is normal - it's using vision models to understand structure

# For faster parsing, use simple parser for basic PDFs
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@simple_document.pdf" \
  -F "use_llamaparse=false"
```

#### Slow query responses
```bash
# Use a faster model
LLM_MODEL=openai/gpt-4-turbo  # Fast
# or
LLM_MODEL=meta-llama/llama-3.1-70b-instruct  # Very fast

# Or reduce chunk size for faster retrieval
CHUNK_SIZE=512
SIMILARITY_TOP_K=3
```

---

## Summary

### Setup Checklist

- [ ] Get OpenRouter API key (https://openrouter.ai/keys)
- [ ] Get LlamaParse API key (https://cloud.llamaindex.ai/)
- [ ] Get OpenAI API key (optional, for embeddings)
- [ ] Update `.env` with all keys
- [ ] Set `LLM_PROVIDER=openrouter`
- [ ] Set `USE_LLAMA_PARSE=true`
- [ ] Choose your model in `LLM_MODEL`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Start server: `docker-compose up -d`
- [ ] Test: `curl http://localhost:8000/health`

### What You Get

✅ Access to 200+ AI models via OpenRouter
✅ Advanced PDF parsing with vision via LlamaParse
✅ Table extraction as structured markdown
✅ Image and chart descriptions
✅ 3x-60x cost savings compared to OpenAI direct
✅ No vendor lock-in - switch models anytime

### Cost Comparison

| Setup | LLM Cost (1M tokens) | PDF Parsing (1K pages) | Total |
|-------|---------------------|------------------------|-------|
| OpenAI Direct + Simple | $30 | Free | $30 (❌ poor quality) |
| OpenAI Direct + LlamaParse | $30 | $3 | $33 |
| **OpenRouter + LlamaParse** | **$10** | **$3** | **$13** ✅ |
| OpenRouter Budget + LlamaParse | $0.52 | $3 | $3.52 ✅✅✅ |

### Next Steps

1. **Start with the Quick Start** section above
2. **Test with a sample PDF** that has tables or images
3. **Experiment with different models** - no code changes needed!
4. **Customize parsing instructions** for your specific documents
5. **Monitor costs** at https://openrouter.ai/activity

### Resources

- OpenRouter Models: https://openrouter.ai/models
- OpenRouter Pricing: https://openrouter.ai/models (click any model)
- LlamaParse Docs: https://docs.llamaindex.ai/en/stable/module_guides/loading/connector/llama_parse/
- LlamaParse Pricing: https://cloud.llamaindex.ai/pricing

---

**Questions?** Open an issue or check the main documentation.

**Last Updated**: 2025-11-18
