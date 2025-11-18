# How to Use This PDF Parser

## Quick Start (3 Steps)

### 1. Start the Application
```bash
cd deployment-examples
docker-compose up -d
```

### 2. Upload & Parse PDF
```bash
# Upload your PDF
curl -X POST http://localhost:8000/upload -F "file=@your-document.pdf"

# Index it
curl -X POST http://localhost:8000/ingest

# Query it
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Summarize this document"}'
```

### 3. Done! 🎉

---

## Two Parsing Methods

### Method 1: Simple Parser (FREE - Works Now)
**Best for:** Plain text PDFs, simple documents

```bash
# Parse and view content
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@document.pdf" \
  -F "use_llamaparse=false"
```

### Method 2: LlamaParse (ADVANCED - Better Quality)
**Best for:** Tables, forms, complex layouts

**Setup (one-time):**
1. Get free API key: https://cloud.llamaindex.ai/ (1,000 pages/day free)
2. Add to `.env` file:
   ```
   LLAMA_CLOUD_API_KEY=llx-your-key-here
   ```
3. Restart: `docker-compose restart`

**Use:**
```bash
# Parse complex PDF with tables
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@financial-report.pdf" \
  -F "use_llamaparse=true" \
  -F "parsing_instruction=Extract all tables precisely"
```

---

## Common Use Cases

### Financial Reports
```bash
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@report.pdf" \
  -F "parsing_instruction=Extract all financial tables with precise numbers"
```

### Forms
```bash
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@form.pdf" \
  -F "parsing_instruction=Extract field names and values. Preserve checkbox states"
```

### Research Papers
```bash
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@paper.pdf" \
  -F "parsing_instruction=Preserve citations and extract figures with captions"
```

---

## Complete Workflow

```bash
# 1. Parse to see content
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@document.pdf" > content.json

# 2. Upload for searching
curl -X POST http://localhost:8000/upload -F "file=@document.pdf"

# 3. Index
curl -X POST http://localhost:8000/ingest

# 4. Query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the key findings?"}'
```

---

## API Documentation
Visit: http://localhost:8000/docs

## When to Use Each Method

| Feature | Simple Parser | LlamaParse |
|---------|--------------|------------|
| Cost | Free | 1,000 pages/day free |
| Speed | Fast | Slower (API) |
| Tables | Poor | Excellent |
| Forms | Poor | Excellent |
| Plain Text | Good | Good |
| Offline | Yes | No |

## Tips

1. **Start simple** - Try the free parser first
2. **Use LlamaParse for tables** - Much better extraction
3. **Add instructions** - Tell it what to focus on
4. **Check the API docs** - http://localhost:8000/docs has all endpoints

For detailed guides, see:
- `PDF_QUICKSTART.md` - Quick examples
- `PDF_PARSING_GUIDE.md` - Complete documentation
