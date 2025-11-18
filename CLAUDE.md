# CLAUDE.md - AI Assistant Guide for LlamaIndex Repository

This document provides comprehensive guidance for AI assistants working with the LlamaIndex codebase. It explains the repository structure, development workflows, testing conventions, and key practices to follow.

## Table of Contents

- [Repository Overview](#repository-overview)
- [Repository Structure](#repository-structure)
- [Technology Stack](#technology-stack)
- [Development Setup](#development-setup)
- [Development Workflows](#development-workflows)
- [Testing Conventions](#testing-conventions)
- [Package Management](#package-management)
- [Custom Tooling](#custom-tooling)
- [Deployment Examples](#deployment-examples)
- [Code Conventions](#code-conventions)
- [CI/CD and Quality Gates](#cicd-and-quality-gates)
- [Common Tasks](#common-tasks)

## Repository Overview

**Project**: LlamaIndex - A data framework for LLM applications
**Repository Type**: Monorepo with 300+ independently versioned packages
**Python Versions**: 3.9, 3.10, 3.11, 3.12 (minimum 3.9)
**Package Manager**: `uv` (primary), `pip` (supported)
**Build System**: `hatchling`

### Key Characteristics

- **Monorepo Structure**: Single repository containing core package, 300+ integrations, 50+ packs, and utilities
- **Namespace Packages**: Clean import structure using `llama_index.core.*` and `llama_index.<category>.<name>`
- **Independent Versioning**: Each package has its own version and can be published separately
- **Modern Tooling**: Uses `uv` for package management, `ruff` for linting, `mypy` for type checking
- **Custom Development Tools**: Includes `llama-dev` CLI for monorepo management

## Repository Structure

```
llama_index/
├── llama-index-core/              # Core framework (required)
├── llama-index-integrations/      # Integration packages
│   ├── llms/                      # 102 LLM integrations
│   ├── embeddings/                # 70 embedding providers
│   ├── vector_stores/             # 77 vector database integrations
│   ├── readers/                   # 156 data loaders
│   ├── tools/                     # 63 tools
│   ├── callbacks/                 # 14 callback integrations
│   ├── graph_stores/              # 9 graph databases
│   ├── postprocessor/             # 27 postprocessors
│   ├── retrievers/                # 16 retrievers
│   └── [more categories...]
├── llama-index-packs/             # 50+ pre-built workflows
├── llama-index-utils/             # Utility packages
├── llama-index-cli/               # Command-line interface
├── llama-index-finetuning/        # Fine-tuning utilities
├── llama-index-experimental/      # Experimental features
├── llama-index-instrumentation/   # Observability tools
├── llama-datasets/                # 17+ evaluation datasets
├── llama-dev/                     # Custom monorepo CLI tool
├── deployment-examples/           # ⭐ Production deployment templates (CUSTOM)
├── docs/                          # Sphinx documentation
├── scripts/                       # Utility scripts
├── _llama-index/                  # Main wrapper package source
├── .github/workflows/             # CI/CD pipelines
├── pyproject.toml                 # Root project config
├── .pre-commit-config.yaml        # Pre-commit hooks
└── Makefile                       # Common tasks
```

### Core Package Structure

```
llama-index-core/llama_index/core/
├── base/                 # Base classes and abstractions
├── indices/              # Index implementations (VectorStoreIndex, etc.)
├── query_engine/         # Query engines
├── retrievers/           # Retriever implementations
├── vector_stores/        # Vector store abstractions
├── llms/                 # LLM base classes
├── embeddings/           # Embedding abstractions
├── node_parser/          # Document parsing and chunking
├── storage/              # Storage abstractions
├── workflow/             # Workflow system
├── ingestion/            # Data ingestion pipeline
├── postprocessor/        # Postprocessing components
└── _static/              # Cached data (NLTK, tiktoken)
```

## Technology Stack

### Core Dependencies

- **Data Validation**: `pydantic>=2.8.0`
- **Database**: `SQLAlchemy>=1.4.49`
- **HTTP Clients**: `httpx`, `aiohttp`
- **Tokenization**: `tiktoken>=0.7.0`
- **NLP**: `nltk>3.8.1`
- **Data Structures**: `numpy`, `networkx`
- **Retry Logic**: `tenacity`
- **File Systems**: `fsspec>=2023.5.0`

### Development Tools

- **Package Manager**: `uv` (fast, modern Python package manager)
- **Linter/Formatter**: `ruff==0.11.11`
- **Type Checker**: `mypy==1.11.0`
- **Code Formatter**: `black[jupyter]` (for docs)
- **Pre-commit**: `pre-commit==3.2.0`
- **Testing**: `pytest>=8.2.1`, `pytest-asyncio`, `pytest-mock`, `pytest-cov`

### Deployment Stack (in deployment-examples/)

- **Web Framework**: `fastapi>=0.115.0`
- **ASGI Server**: `uvicorn[standard]>=0.32.0`
- **Vector Store**: ChromaDB, Pinecone, or Qdrant
- **Database**: PostgreSQL
- **Cache**: Redis
- **PDF Parsing**: `llama-parse` (optional, advanced)
- **Containerization**: Docker + Docker Compose

## Development Setup

### Initial Setup (Global Environment)

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# OR
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows

# Clone repository
git clone https://github.com/run-llama/llama_index.git
cd llama_index

# Setup global environment (for pre-commit hooks)
uv sync

# Install pre-commit hooks
uv run -- pre-commit install
```

### Working on a Specific Package

```bash
# Navigate to the package you want to work on
cd llama-index-core
# OR
cd llama-index-integrations/llms/llama-index-llms-openai

# Run tests (automatically creates virtual environment)
uv run -- pytest

# Explicitly create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# The package is already installed in editable mode
# You can now make changes and run tests
```

## Development Workflows

### Creating a New Integration

1. **Fork and Clone**: Fork the repository and clone your fork
2. **Create Branch**: `git checkout -b your-feature-branch`
3. **Navigate to Category**: `cd llama-index-integrations/<category>/`
4. **Create Package**: Follow the template structure
5. **Implement Interface**: Implement required base class methods
6. **Add Tests**: Write tests with >50% coverage
7. **Update Documentation**: Add docstrings and README
8. **Test Locally**: `uv run -- pytest`
9. **Run Linters**: `uv run -- pre-commit run -a`
10. **Commit and Push**: Create pull request

### Namespace Import Pattern

```python
# Core imports include 'core' in the path
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.llms import LLM
from llama_index.core.embeddings import BaseEmbedding

# Integration imports do NOT include 'core'
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
```

### Making Changes to Core

```bash
cd llama-index-core

# Make your changes
# Add tests in tests/ directory

# Run tests
uv run -- pytest

# Run type checking
uv run -- mypy llama_index/core

# Run linting
uv run -- ruff check .
uv run -- ruff format .

# Run all pre-commit hooks
uv run -- pre-commit run -a
```

## Testing Conventions

### Test Organization

- **Location**: Each package has a `tests/` directory
- **Structure**: Tests mirror source code structure
- **Naming**: `test_<module_name>.py`
- **Markers**: Use `@pytest.mark.integration` for integration tests

### Test Execution

```bash
# Run all tests in current package
uv run -- pytest

# Run with coverage
uv run -- pytest --cov

# Run specific test file
uv run -- pytest tests/test_something.py

# Run integration tests
uv run -- pytest --integration

# Run with verbose output
uv run -- pytest -v
```

### Test Conventions

1. **Mock External Services**: Always mock API calls to external services
2. **Use Fixtures**: Leverage pytest fixtures for common setups
3. **Async Tests**: Use `@pytest.mark.asyncio` for async test functions
4. **Coverage Requirement**: Maintain >50% test coverage (enforced by CI)
5. **Environment Variables**: Tests set `IS_TESTING=1` automatically

### Common Test Patterns

```python
import pytest
from unittest.mock import Mock, patch

# Mock LLM for testing
@pytest.fixture
def mock_llm():
    llm = Mock()
    llm.complete.return_value = "mocked response"
    return llm

# Async test
@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result is not None

# Integration test
@pytest.mark.integration
def test_integration_with_real_api():
    # Only runs when --integration flag is used
    pass
```

## Package Management

### Using `uv`

```bash
# Sync dependencies for current package
uv sync

# Add a dependency
uv add package-name

# Add a dev dependency
uv add --dev package-name

# Run a command in the virtual environment
uv run -- <command>

# Update dependencies
uv lock --upgrade
```

### Package Structure

Each package must have:
- `pyproject.toml` - Package metadata and dependencies
- `README.md` - Package documentation
- `llama_index/<category>/<name>/` - Source code
- `tests/` - Test directory

### Versioning

- Packages are independently versioned
- Follow semantic versioning (MAJOR.MINOR.PATCH)
- Version is specified in `pyproject.toml`

## Custom Tooling

### llama-dev CLI

The repository includes a custom CLI tool for monorepo management.

```bash
# Install llama-dev (from repo root)
cd llama-dev
uv pip install -e .

# Get package information
llama-dev pkg info llama-index-core
llama-dev pkg info --all

# Execute commands across packages
llama-dev pkg exec --cmd "uv sync" --all

# Smart testing (only changed packages + dependents)
llama-dev test --base-ref main --workers 4
llama-dev test --base-ref main --workers 4 --cov
llama-dev test --base-ref main --fail-fast

# Test specific packages
llama-dev test --packages llama-index-core llama-index-llms-openai
```

### Makefile Commands

```bash
# Format code
make format

# Run linters
make lint

# Run tests (changed packages only)
make test

# Test core package
make test-core

# Watch documentation for live preview
make watch-docs
```

## Deployment Examples

### Custom Production Templates (deployment-examples/)

The `deployment-examples/` directory contains **production-ready deployment templates** with complete infrastructure:

**Contents**:
- `api_server.py` - Full FastAPI server (681 lines)
  - Document upload/ingestion
  - Query and chat endpoints (streaming support)
  - PDF parsing with LlamaParse
  - Health checks and background tasks
  - Comprehensive error handling

- Docker Infrastructure:
  - Multi-stage Dockerfile (Python 3.11-slim)
  - docker-compose.yml with full stack:
    - FastAPI app (port 8000)
    - ChromaDB vector store (port 8001)
    - PostgreSQL database (port 5433)
    - Redis cache (port 6379)
    - Nginx reverse proxy (production)

- Configuration:
  - `.env.example` - Comprehensive environment template (130+ lines)
  - `nginx.conf` - Reverse proxy configuration
  - `requirements.txt` - All dependencies

- Documentation:
  - `README.md` - Complete deployment guide
  - `QUICKSTART.md` - Step-by-step quick start
  - `DEPLOYMENT_GUIDE.md` - Comprehensive deployment guide
  - `PDF_PARSING_GUIDE.md` - Detailed PDF parsing guide

- Automation:
  - `Makefile` - 30+ commands for setup, testing, deployment
  - `start.sh` - Interactive setup script

### Using Deployment Examples

```bash
cd deployment-examples

# Quick start
./start.sh

# Or manual setup
cp .env.example .env
# Edit .env with your configuration

# Docker Compose
docker-compose up -d

# Production with Nginx
docker-compose --profile production up -d

# Check health
curl http://localhost:8000/health
```

## Code Conventions

### Style Guidelines

1. **Type Hints**: Required for all function signatures
2. **Docstrings**: Google-style docstrings for all public APIs
3. **Line Length**: Use best judgment, E501 not enforced
4. **Imports**: Organized with `ruff` (isort)
5. **Formatting**: Enforced by `ruff format`

### Type Checking

```python
# All functions must have type hints
def process_document(
    document: Document,
    chunk_size: int = 512,
    chunk_overlap: int = 128
) -> list[Node]:
    """Process a document into nodes.

    Args:
        document: The document to process.
        chunk_size: Size of each chunk.
        chunk_overlap: Overlap between chunks.

    Returns:
        List of processed nodes.
    """
    # Implementation
    pass
```

### Documentation Standards

```python
class CustomRetriever(BaseRetriever):
    """Custom retriever implementation.

    This retriever implements a custom algorithm for retrieving
    relevant nodes based on the query.

    Args:
        index: The index to retrieve from.
        similarity_top_k: Number of top results to return.

    Example:
        >>> retriever = CustomRetriever(index=index, similarity_top_k=5)
        >>> nodes = retriever.retrieve("query text")
    """

    def __init__(
        self,
        index: BaseIndex,
        similarity_top_k: int = 10,
    ) -> None:
        """Initialize the retriever."""
        self._index = index
        self._similarity_top_k = similarity_top_k
```

### Error Handling

```python
# Use specific exceptions
from llama_index.core.exceptions import (
    InvalidConfiguration,
    ServiceUnavailable,
)

def validate_config(config: dict) -> None:
    """Validate configuration."""
    if "api_key" not in config:
        raise InvalidConfiguration(
            "api_key is required in configuration"
        )
```

## CI/CD and Quality Gates

### Pre-commit Hooks

Automatically run on every commit:
- `ruff` - Linting and formatting
- `mypy` - Type checking
- `codespell` - Spell checking
- `prettier` - Markdown/JSON formatting
- Various file checks (YAML, trailing whitespace, etc.)

### GitHub Actions Workflows

- **Linting**: Runs on push/PR
- **Unit Tests**: Matrix testing (Python 3.9-3.12)
- **Type Checking**: mypy on core package
- **Coverage Check**: Enforces >50% coverage
- **Build Package**: Validates package building
- **Release**: Automated publishing

### Quality Requirements

1. **Test Coverage**: Minimum 50% (enforced)
2. **Type Hints**: Required for all functions
3. **Linting**: Must pass `ruff` checks
4. **Format**: Must pass `ruff format`
5. **Type Check**: Must pass `mypy` (for core)
6. **Spell Check**: Must pass `codespell`

## Common Tasks

### Adding a New Integration

```bash
# 1. Navigate to appropriate category
cd llama-index-integrations/llms/

# 2. Create new integration directory
mkdir llama-index-llms-mynewllm
cd llama-index-llms-mynewllm

# 3. Create structure (use existing integration as template)
mkdir -p llama_index/llms/mynewllm
mkdir tests

# 4. Create pyproject.toml
# Use another integration's pyproject.toml as template

# 5. Implement your integration
# llama_index/llms/mynewllm/__init__.py
# llama_index/llms/mynewllm/base.py

# 6. Write tests
# tests/test_mynewllm.py

# 7. Add README
# README.md

# 8. Test
uv run -- pytest

# 9. Run pre-commit
uv run -- pre-commit run -a

# 10. Submit PR
```

### Debugging Tests

```bash
# Run with print statements visible
uv run -- pytest -s

# Run with debugger
uv run -- pytest --pdb

# Run specific test
uv run -- pytest tests/test_file.py::test_function_name

# Run with verbose output
uv run -- pytest -vv
```

### Working with Documentation

```bash
# Navigate to docs
cd docs

# Install doc dependencies
uv sync

# Build documentation
make html

# Watch for changes (live reload)
make watch-docs

# Check for broken links
make linkcheck
```

### Running Integration Tests

```bash
# Set required environment variables
export OPENAI_API_KEY="your-key"

# Run integration tests
uv run -- pytest --integration

# Run specific integration
uv run -- pytest tests/integration/test_openai.py --integration
```

### Using the Deployment Template

```bash
cd deployment-examples

# Interactive setup
./start.sh

# Manual Docker setup
cp .env.example .env
# Edit .env with your API keys and configuration
docker-compose up -d

# Check logs
docker-compose logs -f app

# Run tests
make test

# Stop services
docker-compose down

# With volume cleanup
docker-compose down -v
```

### Making a Release (Maintainers)

```bash
# Update version in pyproject.toml
# Update CHANGELOG.md

# Commit changes
git add .
git commit -m "Release vX.Y.Z"

# Tag release
git tag vX.Y.Z
git push origin vX.Y.Z

# CI will automatically publish to PyPI
```

## Important Notes for AI Assistants

### When Working with This Repository

1. **Always use `uv`**: Prefer `uv run --` over direct command execution
2. **Navigate to package**: Always `cd` to the specific package before working
3. **Test coverage**: Ensure tests achieve >50% coverage
4. **Type hints**: Add type hints to all new functions
5. **Mock external services**: Never make real API calls in tests
6. **Follow namespace**: Use correct import patterns (`llama_index.core.*` vs `llama_index.<category>.*`)
7. **Check existing integrations**: Use similar integrations as templates
8. **Run pre-commit**: Always run before committing

### Common Pitfalls to Avoid

1. ❌ **Don't use Poetry**: The repo has migrated to `uv`
2. ❌ **Don't modify multiple packages**: Focus on one package at a time
3. ❌ **Don't skip tests**: Coverage is enforced by CI
4. ❌ **Don't commit without pre-commit**: Hooks will catch issues
5. ❌ **Don't make real API calls in tests**: Always mock
6. ❌ **Don't ignore type hints**: mypy is enforced
7. ❌ **Don't use old import patterns**: Follow namespace conventions

### Best Practices

1. ✅ **Use existing code as templates**: Look at similar integrations
2. ✅ **Write comprehensive docstrings**: Help users understand your code
3. ✅ **Add examples**: Include usage examples in docstrings and README
4. ✅ **Test edge cases**: Don't just test the happy path
5. ✅ **Keep it simple**: Prefer simple, readable code
6. ✅ **Follow existing patterns**: Consistency matters in a monorepo
7. ✅ **Document configuration**: Clearly document required settings

### deployment-examples/ Is Custom Work

The `deployment-examples/` directory is **custom production-ready infrastructure** added to this repository. It's not part of the standard LlamaIndex distribution. It provides:

- Complete FastAPI application template
- Docker orchestration with multiple services
- Comprehensive environment configuration
- Production deployment guides
- PDF parsing integration examples

Use this as a reference for building production LlamaIndex applications.

---

## Quick Reference

### Essential Commands

```bash
# Setup
uv sync                              # Install dependencies
uv run -- pre-commit install        # Install hooks

# Development
uv run -- pytest                    # Run tests
uv run -- pytest --cov              # With coverage
uv run -- ruff check .              # Lint
uv run -- ruff format .             # Format
uv run -- mypy .                    # Type check
uv run -- pre-commit run -a         # Run all hooks

# Monorepo Tools
llama-dev test --base-ref main      # Smart testing
llama-dev pkg info --all            # Package info

# Deployment
cd deployment-examples
./start.sh                          # Interactive setup
docker-compose up -d                # Start services
```

### Important Files

- `pyproject.toml` - Package configuration
- `.pre-commit-config.yaml` - Pre-commit hooks
- `Makefile` - Common tasks
- `deployment-examples/.env.example` - Deployment configuration template

### Key Resources

- Documentation: https://docs.llamaindex.ai/
- Contributing Guide: CONTRIBUTING.md
- LlamaHub: https://llamahub.ai/
- Discord: https://discord.gg/dGcwcsnxhU

---

**Last Updated**: 2025-11-18
**Repository**: https://github.com/run-llama/llama_index
