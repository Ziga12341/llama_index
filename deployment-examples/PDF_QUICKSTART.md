# PDF Parsing Quick Start

Parse PDFs with LlamaIndex in 5 minutes!

## Option 1: Simple PDF Parsing (Free, Works Now)

Your deployment already supports PDFs out of the box!

### Upload and Parse

```bash
# Upload PDF
curl -X POST http://localhost:8000/upload \
  -F "file=@document.pdf"

# Index it
curl -X POST http://localhost:8000/ingest

# Query it!
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Summarize this PDF"}'
```

### Parse PDF and See Content

```bash
# Parse without LlamaParse (simple, free)
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@document.pdf" \
  -F "use_llamaparse=false"
```

**Response:**
```json
{
  "status": "success",
  "filename": "document.pdf",
  "num_pages": 5,
  "content": ["Page 1 text...", "Page 2 text...", ...],
  "parser_used": "simple"
}
```

## Option 2: LlamaParse (Better for Tables/Forms)

For complex PDFs with tables, forms, charts, etc.

### Setup (2 minutes)

1. **Get API Key:**
   - Go to https://cloud.llamaindex.ai/
   - Sign up (free tier: 1,000 pages/day)
   - Get your API key (starts with `llx-`)

2. **Install LlamaParse:**
```bash
# Uncomment in requirements.txt
llama-parse>=0.5.0

# Install
pip install llama-parse
# OR rebuild Docker
docker-compose down && docker-compose up --build -d
```

3. **Add API Key:**
```bash
# Add to .env
LLAMA_CLOUD_API_KEY=llx-your-key-here
```

### Use It

```bash
# Parse with LlamaParse (LLM-powered)
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@financial_report.pdf" \
  -F "use_llamaparse=true"

# With custom instructions
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@report.pdf" \
  -F "use_llamaparse=true" \
  -F "parsing_instruction=Extract all tables precisely and preserve formatting"
```

**Response:**
```json
{
  "status": "success",
  "filename": "financial_report.pdf",
  "num_pages": 10,
  "content": [
    "# Page 1\n\n| Revenue | $100K |\n| Profit | $25K |",
    "# Page 2\n\n..."
  ],
  "parser_used": "llamaparse"
}
```

## Python Examples

### Simple Parsing

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Parse PDF
documents = SimpleDirectoryReader(
    input_files=["document.pdf"]
).load_data()

# Create index and query
index = VectorStoreIndex.from_documents(documents)
response = index.as_query_engine().query("What's in this PDF?")
print(response)
```

### LlamaParse

```python
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex
import os

# Parse with LlamaParse
parser = LlamaParse(
    api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
    result_type="markdown",
    parsing_instruction="Extract all tables"
)

documents = parser.load_data("financial_report.pdf")

# Query
index = VectorStoreIndex.from_documents(documents)
response = index.as_query_engine().query("What are the revenues?")
print(response)
```

### Using the Example Script

```bash
# Simple parsing
python pdf_parser_example.py document.pdf --method simple

# LlamaParse
python pdf_parser_example.py document.pdf --method llamaparse

# Parse and query
python pdf_parser_example.py document.pdf \
  --query "What are the main topics?" \
  --method llamaparse \
  --instruction "Focus on extracting structured data"

# Compare both methods
python pdf_parser_example.py document.pdf --method compare
```

## When to Use Each Method

### Simple Parser (PyPDF)
✅ **Use for:**
- Plain text PDFs
- Simple documents
- Fast processing needed
- Free/unlimited usage

❌ **Avoid for:**
- PDFs with tables
- Forms
- Multi-column layouts
- Complex formatting

### LlamaParse
✅ **Use for:**
- Financial reports (tables)
- Forms and surveys
- Research papers (citations, figures)
- Invoices and receipts
- Multi-column layouts
- Charts and diagrams

❌ **Avoid for:**
- Simple text-only PDFs (wasteful)
- Very high volume (costs add up)
- When offline access needed

## Real-World Examples

### Financial Report
```bash
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@quarterly_report.pdf" \
  -F "parsing_instruction=Extract all financial tables with precise numbers. Maintain column alignment."
```

### Research Paper
```bash
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@research_paper.pdf" \
  -F "parsing_instruction=Preserve citations, extract figures with captions, maintain section hierarchy."
```

### Invoice
```bash
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@invoice.pdf" \
  -F "parsing_instruction=Extract line items with quantities and prices. Identify total amount."
```

### Form
```bash
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@application_form.pdf" \
  -F "parsing_instruction=Extract field names and values. Preserve checkbox states."
```

## Complete Workflow

### 1. Parse PDF
```bash
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@report.pdf" \
  > parsed_content.json
```

### 2. Upload for Indexing
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@report.pdf"
```

### 3. Index
```bash
curl -X POST http://localhost:8000/ingest
```

### 4. Query
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the key findings?"}'
```

## Troubleshooting

### "LlamaParse not available"
- Install: `pip install llama-parse`
- Set API key: `export LLAMA_CLOUD_API_KEY=llx-...`
- Rebuild Docker if using containers

### "Simple parser not extracting tables correctly"
- Use LlamaParse instead
- Tables in PDFs need LLM understanding

### "Parsing takes too long"
- LlamaParse uses APIs (slower but more accurate)
- Use simple parser for quick results
- Process in background for large PDFs

### "Cost concerns"
- Free tier: 1,000 pages/day
- Use simple parser for plain text PDFs
- Reserve LlamaParse for complex documents
- ~$0.003 per page on paid plans

## Pricing

- **Free tier:** 1,000 pages/day (perfect for testing)
- **Paid:** $0.003/page (~$3 for 1,000 pages)
- **Simple parser:** Always free!

## Tips

1. **Start with simple parser** - It's free and often good enough
2. **Use LlamaParse for tables** - Much better extraction
3. **Add specific instructions** - Gets better results
4. **Cache results** - Don't re-parse same PDFs
5. **Batch process** - More efficient for multiple PDFs

## Next Steps

- See [PDF_PARSING_GUIDE.md](PDF_PARSING_GUIDE.md) for complete documentation
- Try the example script: `python pdf_parser_example.py --help`
- Check API docs: http://localhost:8000/docs

Happy PDF parsing! 📄✨
