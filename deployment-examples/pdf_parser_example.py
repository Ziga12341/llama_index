"""
PDF Parsing Example with LlamaIndex

Demonstrates both simple and LLM-powered PDF parsing
"""

import os
from pathlib import Path
from typing import Optional
import argparse


def parse_pdf_simple(pdf_path: str):
    """
    Parse PDF using simple method (PyPDF)
    Free and fast, but limited for complex PDFs
    """
    print("\n" + "="*60)
    print("METHOD 1: Simple PDF Parsing (PyPDF)")
    print("="*60)

    from llama_index.core import SimpleDirectoryReader

    # Parse PDF
    print(f"Parsing: {pdf_path}")
    documents = SimpleDirectoryReader(
        input_files=[pdf_path]
    ).load_data()

    print(f"✅ Parsed {len(documents)} page(s)")

    # Show extracted content
    for i, doc in enumerate(documents):
        print(f"\n--- Page {i+1} Preview (first 300 chars) ---")
        print(doc.text[:300])
        print("...")

    return documents


def parse_pdf_llamaparse(pdf_path: str, parsing_instruction: Optional[str] = None):
    """
    Parse PDF using LlamaParse (LLM-powered)
    Better for complex PDFs with tables, forms, etc.
    """
    print("\n" + "="*60)
    print("METHOD 2: LlamaParse (LLM-Powered)")
    print("="*60)

    try:
        from llama_parse import LlamaParse
    except ImportError:
        print("❌ llama-parse not installed")
        print("Install with: pip install llama-parse")
        return None

    # Check API key
    api_key = os.getenv("LLAMA_CLOUD_API_KEY")
    if not api_key:
        print("❌ LLAMA_CLOUD_API_KEY not set")
        print("\nTo use LlamaParse:")
        print("1. Sign up at https://cloud.llamaindex.ai/")
        print("2. Get your API key")
        print("3. Set: export LLAMA_CLOUD_API_KEY=llx-your-key")
        return None

    # Initialize parser
    parser = LlamaParse(
        api_key=api_key,
        result_type="markdown",  # Get markdown output
        parsing_instruction=parsing_instruction,
        verbose=True
    )

    # Parse PDF
    print(f"Parsing: {pdf_path}")
    print("⏳ This may take a moment (using LLM)...")

    documents = parser.load_data(pdf_path)

    print(f"✅ Parsed {len(documents)} page(s)")

    # Show extracted content
    for i, doc in enumerate(documents):
        print(f"\n--- Page {i+1} (Markdown) ---")
        print(doc.text[:500])
        print("...")

        if doc.metadata:
            print(f"Metadata: {doc.metadata}")

    return documents


def create_index_and_query(documents, query: str):
    """
    Create index from documents and run a query
    """
    print("\n" + "="*60)
    print("Creating Index and Querying")
    print("="*60)

    from llama_index.core import VectorStoreIndex, Settings
    from llama_index.llms.openai import OpenAI
    from llama_index.embeddings.openai import OpenAIEmbedding

    # Check OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set")
        print("Set: export OPENAI_API_KEY=sk-your-key")
        return

    # Configure LLM
    Settings.llm = OpenAI(model="gpt-4", api_key=os.getenv("OPENAI_API_KEY"))
    Settings.embed_model = OpenAIEmbedding(api_key=os.getenv("OPENAI_API_KEY"))

    # Create index
    print("Creating vector index...")
    index = VectorStoreIndex.from_documents(documents)

    # Query
    print(f"\nQuery: {query}")
    query_engine = index.as_query_engine()
    response = query_engine.query(query)

    print(f"\n📝 Response:")
    print(response)

    # Show sources
    if hasattr(response, 'source_nodes'):
        print(f"\n📚 Sources used:")
        for i, node in enumerate(response.source_nodes):
            print(f"\n  Source {i+1}:")
            print(f"  {node.node.text[:200]}...")
            print(f"  Score: {node.score:.3f}")


def compare_parsers(pdf_path: str):
    """
    Compare simple vs LlamaParse side by side
    """
    print("\n" + "="*60)
    print("COMPARISON: Simple vs LlamaParse")
    print("="*60)

    # Simple parser
    print("\n1️⃣  Simple Parser Output:")
    simple_docs = parse_pdf_simple(pdf_path)

    # LlamaParse
    print("\n2️⃣  LlamaParse Output:")
    llama_docs = parse_pdf_llamaparse(
        pdf_path,
        parsing_instruction="Extract all tables and preserve formatting as markdown"
    )

    if simple_docs and llama_docs:
        print("\n" + "="*60)
        print("COMPARISON SUMMARY")
        print("="*60)
        print(f"Simple Parser: {len(simple_docs)} pages")
        print(f"LlamaParse:    {len(llama_docs)} pages")
        print("\nSimple Parser: Good for plain text PDFs")
        print("LlamaParse:    Better for tables, forms, complex layouts")


def main():
    parser = argparse.ArgumentParser(
        description="Parse PDFs with LlamaIndex",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simple parsing
  python pdf_parser_example.py document.pdf --method simple

  # LlamaParse (LLM-powered)
  python pdf_parser_example.py document.pdf --method llamaparse

  # Compare both methods
  python pdf_parser_example.py document.pdf --method compare

  # Parse and query
  python pdf_parser_example.py document.pdf --query "What are the main topics?"

  # Custom parsing instruction
  python pdf_parser_example.py financial.pdf \\
    --method llamaparse \\
    --instruction "Extract all financial tables precisely"
        """
    )

    parser.add_argument(
        "pdf_path",
        help="Path to PDF file"
    )

    parser.add_argument(
        "--method",
        choices=["simple", "llamaparse", "compare"],
        default="simple",
        help="Parsing method (default: simple)"
    )

    parser.add_argument(
        "--query",
        help="Query to run after parsing"
    )

    parser.add_argument(
        "--instruction",
        help="Custom parsing instruction for LlamaParse"
    )

    args = parser.parse_args()

    # Check if PDF exists
    if not os.path.exists(args.pdf_path):
        print(f"❌ PDF not found: {args.pdf_path}")
        return

    print(f"📄 PDF: {args.pdf_path}")
    print(f"📊 Method: {args.method}")

    # Parse based on method
    documents = None

    if args.method == "simple":
        documents = parse_pdf_simple(args.pdf_path)

    elif args.method == "llamaparse":
        documents = parse_pdf_llamaparse(args.pdf_path, args.instruction)

    elif args.method == "compare":
        compare_parsers(args.pdf_path)
        return

    # Run query if provided
    if args.query and documents:
        create_index_and_query(documents, args.query)

    print("\n✅ Done!")


if __name__ == "__main__":
    # If run without arguments, show help
    import sys
    if len(sys.argv) == 1:
        print("PDF Parsing Example")
        print("="*60)
        print("\nUsage: python pdf_parser_example.py <pdf_file> [options]")
        print("\nQuick start:")
        print("  1. Place a PDF in the data/ folder")
        print("  2. Run: python pdf_parser_example.py data/sample.pdf")
        print("\nFor more options: python pdf_parser_example.py --help")
        print("\n" + "="*60)
    else:
        main()
