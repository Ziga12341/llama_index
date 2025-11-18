# PDF Parsing with LlamaIndex

LlamaIndex provides multiple ways to parse PDFs, including LLM-powered parsing for complex documents.

## PDF Parsing Options

### 1. Simple PDF Parsing (Basic - Free)
Uses PyPDF to extract text from simple PDFs

### 2. LlamaParse (Advanced - LLM-powered)
Uses LLMs to parse complex PDFs with:
- Tables and structured data
- Forms and checkboxes
- Charts and figures
- Multi-column layouts
- Headers and footers
- Complex formatting

### 3. Other Parsers
- Unstructured.io
- PDFPlumber
- PyMuPDF

---

## Quick Start: Simple PDF Parsing

### Already Works in the Deployment!

The FastAPI server already supports PDF upload:

```bash
# Upload a PDF
curl -X POST http://localhost:8000/upload \
  -F "file=@document.pdf"

# Index it
curl -X POST http://localhost:8000/ingest

# Query it
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is in this PDF?"}'
```

### Python Example

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Automatically parses PDFs in the directory
documents = SimpleDirectoryReader("./data").load_data()

# Create index
index = VectorStoreIndex.from_documents(documents)

# Query
query_engine = index.as_query_engine()
response = query_engine.query("Summarize the PDF")
print(response)
```

---

## Advanced: LlamaParse (LLM-Powered PDF Parsing)

### Why LlamaParse?

**Better for complex PDFs:**
- ✅ Tables → Extracted accurately as markdown
- ✅ Forms → Parsed with structure
- ✅ Multi-column → Handled correctly
- ✅ Charts/Images → Described with vision
- ✅ Headers/Footers → Preserved or removed
- ✅ Complex layouts → Understood contextually

### Setup

1. **Get API Key:**
   - Sign up at https://cloud.llamaindex.ai/
   - Get your LlamaParse API key
   - Free tier: 1,000 pages/day

2. **Install:**
```bash
pip install llama-parse
```

3. **Configure:**
```bash
# Add to .env
LLAMA_CLOUD_API_KEY=llx-your-key-here
```

### Basic Usage

```python
from llama_parse import LlamaParse

# Initialize parser
parser = LlamaParse(
    api_key="llx-your-key",
    result_type="markdown",  # or "text"
    verbose=True
)

# Parse PDF
documents = parser.load_data("document.pdf")

# Use with LlamaIndex
from llama_index.core import VectorStoreIndex
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("Extract all tables from the PDF")
print(response)
```

### Advanced Configuration

```python
from llama_parse import LlamaParse

parser = LlamaParse(
    api_key="llx-your-key",
    result_type="markdown",

    # Parsing options
    num_workers=4,  # Parallel processing
    verbose=True,
    language="en",

    # Advanced features
    parsing_instruction="""
        Extract all tables and preserve their structure.
        Pay special attention to financial data.
        Ignore headers and footers.
    """,

    # Premium features (paid plans)
    premium_mode=True,  # Better accuracy
    gpt4o_mode=True,    # Use GPT-4o for parsing
    continuous_mode=True,  # For continuous monitoring
)

# Parse single PDF
documents = parser.load_data("financial_report.pdf")

# Parse multiple PDFs
documents = parser.load_data([
    "report1.pdf",
    "report2.pdf",
    "report3.pdf"
])
```

### With Custom Instructions

```python
# For financial documents
parser = LlamaParse(
    api_key="llx-your-key",
    result_type="markdown",
    parsing_instruction="""
        This is a financial statement.
        Extract all tables with numbers precisely.
        Maintain column alignment.
        Separate different financial years clearly.
    """
)

# For forms
parser = LlamaParse(
    api_key="llx-your-key",
    result_type="markdown",
    parsing_instruction="""
        This is a filled form.
        Extract field names and their values.
        Preserve checkbox states.
        Maintain the form structure.
    """
)

# For research papers
parser = LlamaParse(
    api_key="llx-your-key",
    result_type="markdown",
    parsing_instruction="""
        This is a research paper.
        Preserve citations and references.
        Extract figures and their captions.
        Maintain section hierarchy.
    """
)
```

---

## Integration with FastAPI Server

### Updated api_server.py with LlamaParse

Add this to the imports:
```python
from llama_parse import LlamaParse
import os
```

Add configuration:
```python
# In startup_event() function
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
USE_LLAMA_PARSE = os.getenv("USE_LLAMA_PARSE", "false").lower() == "true"

if USE_LLAMA_PARSE:
    if not LLAMA_CLOUD_API_KEY:
        logger.warning("LLAMA_CLOUD_API_KEY not set, falling back to simple parsing")
    else:
        logger.info("LlamaParse enabled for PDF parsing")
```

Add new endpoint:
```python
@app.post("/parse-pdf")
async def parse_pdf_with_llm(
    file: UploadFile = File(...),
    parsing_instruction: Optional[str] = None
):
    """
    Parse PDF using LlamaParse (LLM-powered)

    Returns parsed content as markdown
    """
    if not LLAMA_CLOUD_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="LlamaParse not configured. Set LLAMA_CLOUD_API_KEY."
        )

    try:
        # Save uploaded file temporarily
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Parse with LlamaParse
        parser = LlamaParse(
            api_key=LLAMA_CLOUD_API_KEY,
            result_type="markdown",
            parsing_instruction=parsing_instruction,
            verbose=True
        )

        documents = parser.load_data(temp_path)

        # Clean up
        os.remove(temp_path)

        # Return parsed content
        return {
            "status": "success",
            "filename": file.filename,
            "num_pages": len(documents),
            "content": [doc.text for doc in documents],
            "metadata": [doc.metadata for doc in documents]
        }

    except Exception as e:
        logger.error(f"Error parsing PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Complete Example: PDF with Tables

### Python Script

```python
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex
import os

# Initialize parser
parser = LlamaParse(
    api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
    result_type="markdown",
    parsing_instruction="""
        Extract all tables and preserve formatting.
        Convert tables to markdown format.
    """
)

# Parse PDF with tables
print("Parsing PDF...")
documents = parser.load_data("financial_report.pdf")

# See what was parsed
print("\n=== Parsed Content ===")
for i, doc in enumerate(documents):
    print(f"\nPage {i+1}:")
    print(doc.text[:500])  # First 500 chars

# Create searchable index
print("\nCreating index...")
index = VectorStoreIndex.from_documents(documents)

# Query the tables
query_engine = index.as_query_engine()

print("\n=== Querying ===")
questions = [
    "What are the total revenues?",
    "Extract the income statement table",
    "What was the profit margin in Q4?",
    "Compare revenue between 2023 and 2024"
]

for question in questions:
    print(f"\nQ: {question}")
    response = query_engine.query(question)
    print(f"A: {response}")
```

---

## Using with the API Server

### 1. Update .env

```bash
# Add to .env
LLAMA_CLOUD_API_KEY=llx-your-key-here
USE_LLAMA_PARSE=true
```

### 2. Update requirements.txt

```bash
# Add to requirements.txt
llama-parse>=0.5.0
```

### 3. Rebuild Docker

```bash
docker-compose down
docker-compose up --build -d
```

### 4. Use the API

```bash
# Parse PDF with LlamaParse
curl -X POST http://localhost:8000/parse-pdf \
  -F "file=@financial_report.pdf" \
  -F "parsing_instruction=Extract all financial tables precisely"

# Regular upload (uses simple parser)
curl -X POST http://localhost:8000/upload \
  -F "file=@document.pdf"

# Index and query
curl -X POST http://localhost:8000/ingest
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the key financial metrics?"}'
```

---

## Comparison: Simple vs LlamaParse

### Simple PDF Parser (PyPDF)
```python
from llama_index.core import SimpleDirectoryReader

# Pros:
# ✅ Free
# ✅ Fast
# ✅ No API key needed
# ✅ Works offline

# Cons:
# ❌ Poor table extraction
# ❌ Struggles with complex layouts
# ❌ No understanding of structure
# ❌ Multi-column issues

documents = SimpleDirectoryReader("data").load_data()
```

**Output Example:**
```
Revenue 100,000 Expenses 75,000 Profit 25,000
[Tables appear as unstructured text]
```

### LlamaParse
```python
from llama_parse import LlamaParse

# Pros:
# ✅ Excellent table extraction
# ✅ Handles complex layouts
# ✅ Understands document structure
# ✅ Custom parsing instructions
# ✅ Vision for charts/images

# Cons:
# ❌ Requires API key
# ❌ Costs money (after free tier)
# ❌ Slower (API calls)
# ❌ Requires internet

parser = LlamaParse(api_key="llx-...")
documents = parser.load_data("report.pdf")
```

**Output Example:**
```markdown
| Metric    | Amount   |
|-----------|----------|
| Revenue   | $100,000 |
| Expenses  | $75,000  |
| Profit    | $25,000  |
```

---

## Pricing

### Free Tier
- 1,000 pages per day
- Perfect for testing and small projects

### Paid Plans
- Starter: $0.003 per page
- Professional: Volume discounts
- Enterprise: Custom pricing

### Cost Examples
- 100-page report: $0.30
- 1,000 pages/month: ~$3
- 10,000 pages/month: ~$30 (with discounts)

---

## Best Practices

### 1. Choose the Right Parser

**Use Simple Parser for:**
- Plain text PDFs
- Simple documents
- High volume / cost sensitive
- Fast processing needed

**Use LlamaParse for:**
- PDFs with tables
- Forms and structured data
- Complex layouts
- High accuracy needed

### 2. Optimize Parsing

```python
# Batch process multiple PDFs
parser = LlamaParse(
    api_key="llx-...",
    num_workers=4,  # Parallel processing
    verbose=False   # Reduce output
)

files = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
all_documents = parser.load_data(files)
```

### 3. Cache Results

```python
import pickle

# Parse once, save results
documents = parser.load_data("large_report.pdf")
with open("parsed_cache.pkl", "wb") as f:
    pickle.dump(documents, f)

# Load from cache later
with open("parsed_cache.pkl", "rb") as f:
    documents = pickle.load(f)
```

### 4. Use Parsing Instructions

```python
# Be specific
parser = LlamaParse(
    api_key="llx-...",
    parsing_instruction="""
        - Extract ALL tables as markdown
        - Preserve numeric precision
        - Ignore page numbers and headers
        - Separate each section clearly
    """
)
```

---

## Troubleshooting

### LlamaParse API Key Issues
```python
import os

# Check if key is set
api_key = os.getenv("LLAMA_CLOUD_API_KEY")
if not api_key:
    print("❌ LLAMA_CLOUD_API_KEY not set")
else:
    print(f"✅ API key found: {api_key[:10]}...")
```

### Large PDFs
```python
# For very large PDFs, process in chunks
from llama_parse import LlamaParse

parser = LlamaParse(
    api_key="llx-...",
    num_workers=8,  # More parallel workers
    verbose=True     # Monitor progress
)

# Or split PDF first
from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader("huge.pdf")
# Process 50 pages at a time
```

### Table Extraction Not Working
```python
# Add specific instructions
parser = LlamaParse(
    api_key="llx-...",
    result_type="markdown",
    parsing_instruction="""
        THIS IS CRITICAL:
        - Every table must be converted to markdown format
        - Preserve all rows and columns exactly
        - Maintain alignment and spacing
        - Do not summarize or skip any data
    """
)
```

---

## Summary

**For your deployment:**

1. **Simple PDFs** → Already works! Just upload and query
2. **Complex PDFs** → Add LlamaParse for better results
3. **Production** → Mix both: LlamaParse for complex, simple for basic

**Next Steps:**
1. Try with a simple PDF (works now)
2. Get LlamaParse API key for complex PDFs
3. Add parsing instructions for your specific use case
4. Build your PDF analysis application!
