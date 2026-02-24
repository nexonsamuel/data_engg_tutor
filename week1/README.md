# Week 1: PDF Summarizer & Resume Evaluator

An intelligent document processing system that uses LLMs to summarize PDFs and evaluate resumes with hiring-focused insights.

## Overview

This project demonstrates a production-ready multi-stage pipeline:
1. **Extract** - Parse text from PDF files using PyMuPDF
2. **Chunk** - Split text into token-safe chunks respecting model context windows
3. **Summarize** - Process each chunk with an LLM
4. **Evaluate** - Synthesize into a hiring evaluation
5. **Persist** - Save outputs with metadata (model used, timestamp)

## Features

- **Multiple Model Support** - Works with local (Mistral, Phi) and cloud models (GPT-4, Claude)
- **Intelligent Chunking** - Token-based splitting prevents context overflow
- **Dynamic Configuration** - All model settings in one place
- **Hiring-Focused Evaluation** - Specialized prompts for resume assessment
- **Environment Variables** - Secure API key management
- **Progress Feedback** - Rich console output with status updates
- **Error Handling** - Graceful failures with helpful messages
- **Timestamped Output** - Track when and with which model summaries were generated

## Project Structure

```
week1/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── ollama.sh                          # Setup script for local models
├── .env.example                       # API key template
│
├── data/                              # Input PDF files (create this folder)
├── output/                            # Generated summaries (auto-created)
│
├── examples/
│   └── run_summary.py                # Main entry point script
│
├── pdf_summarizer/
│   ├── __init__.py                   # Package initialization
│   ├── pdf_parser.py                 # PDF text extraction
│   ├── chunker.py                    # Token-based text chunking
│   ├── summarizer.py                 # Core pipeline orchestration
│   └── model_constants.py            # Centralized model configs
│
└── tests/
    ├── conftest.py                   # Pytest configuration
    └── test_summarizer.py            # Unit tests
```

## Quick Start

### 1. Set Up Environment

```bash
cd week1
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare Input Files

```bash
mkdir data
# Add your PDF files to the data/ folder
```

### 4. Start the Model Server

For **local models** (recommended - free and fast):
```bash
./ollama.sh mistral
```

This will:
- Check if Ollama is installed
- Pull the Mistral model (if not already downloaded)
- Start the Ollama server

For **cloud models**, create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
```

### 5. Run the Summarizer

```bash
python examples/run_summary.py
```

The script will:
- Find all PDFs in the `data/` folder
- Summarize each one using the configured model
- Save results to `output/` with metadata

## Supported Models

### Recommended (Local - Free)

| Model | Context | Quality | Speed | Size |
|-------|---------|---------|-------|------|
| **Mistral** | 8,192 | ⭐⭐⭐⭐⭐ | Fast | 4.1GB |
| Phi | 2,048 | ⭐⭐⭐ | Very Fast | 1.6GB |
| Neural Chat | 4,096 | ⭐⭐⭐⭐ | Fast | 4.2GB |

### Cloud Options (Paid)

| Model | Context | Quality | Speed |
|-------|---------|---------|-------|
| GPT-4 | 8,192 | ⭐⭐⭐⭐⭐ | Medium |
| GPT-4 Turbo | 128,000 | ⭐⭐⭐⭐⭐ | Medium |
| Claude 3 Opus | 200,000 | ⭐⭐⭐⭐⭐ | Medium |
| Claude 3 Sonnet | 200,000 | ⭐⭐⭐⭐ | Fast |

**Default:** Mistral (excellent quality-to-resource ratio)

## Usage Examples

### Basic Usage (Uses Mistral by default)

```bash
python examples/run_summary.py
```

### Programmatic Usage

```python
from pdf_summarizer import summarize_pdf

# Basic usage
summary, model = summarize_pdf("path/to/resume.pdf")
print(f"Evaluated with: {model}")
print(summary)

# With specific model
summary, model = summarize_pdf("path/to/resume.pdf", model="gpt-4")

# With custom safety factor (use more context per chunk)
summary, model = summarize_pdf(
    "path/to/resume.pdf",
    model="mistral",
    safety_factor=0.50  # Use 50% of context window instead of 30%
)
```

## Configuration

### Model Constants (`pdf_summarizer/model_constants.py`)

All model settings are centralized:

```python
MODEL_CONFIGS = {
    "mistral": {
        "name": "mistral",                      # Model identifier
        "base_url": "http://localhost:11434/v1", # API endpoint
        "api_key": "ollama",                    # API key (or env var)
        "context_window": 8192,                 # Token limit
        "provider": "ollama",                   # Provider type
        "encoding": "cl100k_base",              # Tiktoken encoding
    },
    # ... more models
}

DEFAULT_MODEL = "mistral"          # Default model to use
DEFAULT_SAFETY_FACTOR = 0.30       # Safety margin (30% of context window)
```

### Modifying Prompts

The evaluation prompts are in `summarizer.py`. Current prompts:

**Chunk Summarization:**
```python
"You are evaluating a Data Engineer candidate. Extract only: 
work experience, technical skills, cloud platforms, and key achievements. 
Be factual and concise."
```

**Final Evaluation:**
```python
"You are an AI Head of a data engineering team evaluating a candidate's 
resume for a Data Engineer position. Your job is to provide a crisp, 
professional evaluation..."
```

To customize for different roles, modify these prompts in `summarizer.py`.

## Output Format

Summaries are saved to `output/` with timestamps:

```
output/
├── Nexon_Samuel_summary_20250224_160339.txt
├── resume_summary_20250224_161505.txt
└── ...
```

Each file contains:
```
PDF: Nexon_Samuel.pdf
Generated: 2026-02-24 16:03:39
Model: mistral
================================================================================

[Evaluation text here, with sentences on separate lines...]
```

## Understanding Token Chunking

### Why Chunking?

LLMs have a **context window** - maximum tokens they can process:
- Mistral: 8,192 tokens
- GPT-4: 8,192 tokens
- Claude 3 Opus: 200,000 tokens

A large PDF might be 50,000+ tokens, exceeding the limit.

### How It Works

```
1. Read PDF (50,000 tokens)
   ↓
2. Split into chunks (safety_factor * context_window)
   - Mistral: 8,192 * 0.30 = 2,456 tokens per chunk
   ↓
3. Summarize each chunk independently
   ↓
4. Combine summaries into final output
```

### Tuning Safety Factor

```python
# Conservative (safer, smaller chunks)
safety_factor = 0.20  # Smaller chunks, safer

# Balanced (default)
safety_factor = 0.30  # Good middle ground

# Aggressive (use more context)
safety_factor = 0.50  # Larger chunks, may risk overflow
```

Higher safety factor = larger chunks = better context but higher risk.

## Key Architectural Decisions

### 1. Token-Based vs Character-Based Chunking
**Decision:** Token-based (using tiktoken)
**Why:** Different models have different tokenization rules. Character counts are unreliable.

### 2. Model Configuration Centralization
**Decision:** All model settings in `model_constants.py`
**Why:** Easy to add new models, change settings without code changes.

### 3. Encoding Parameter Passed to Chunker
**Decision:** `chunk_text_by_tokens()` accepts encoding parameter from config
**Why:** Different providers use different encodings (OpenAI vs Anthropic).

### 4. Hiring-Focused Prompts
**Decision:** Specialized system prompts for resume evaluation
**Why:** Generic prompts lead to hallucinations; specific context improves output quality.

## Testing

Run unit tests:

```bash
pytest tests/test_summarizer.py -v
```

Tests cover:
- Text chunking functionality
- Model validation
- PDF parsing

## Troubleshooting

### "Cannot connect to server at http://localhost:11434"
```bash
# Make sure Ollama is running
./ollama.sh mistral
```

### "No PDF files found"
```bash
mkdir data
# Add PDF files to the data/ folder
```

### "Model not found" error
```bash
# Pull the model first
ollama pull mistral

# Or use the setup script
./ollama.sh mistral
```

### API Key errors (for cloud models)
- Verify `.env` file exists in `week1/`
- Check API key is correct
- Ensure you have sufficient API credits

### Token limit exceeded
```python
# Option 1: Reduce safety factor
safety_factor=0.20  # Smaller chunks

# Option 2: Use model with larger context
model="gpt-4-turbo"  # 128,000 tokens

# Option 3: Split PDF manually into smaller files
```

## Performance Metrics

**Example: Summarizing a 2-page resume (500 tokens)**

| Model | Time | Quality | Cost |
|-------|------|---------|------|
| Mistral | 5-10s | Excellent | Free |
| Phi | 3-5s | Good | Free |
| GPT-3.5 | 2-3s | Excellent | $0.01 |
| GPT-4 | 3-5s | Best | $0.10 |

## Best Practices

1. **Start with local models** (Mistral/Phi) for testing
2. **Use default safety_factor (0.30)** unless you have a reason to change it
3. **Test with small PDFs first** before processing large batches
4. **Monitor output quality** - adjust prompts if results are poor
5. **Batch process** multiple documents to amortize setup overhead
6. **Keep API keys secure** - never commit `.env` to git

## Data Engineering Concepts Demonstrated

1. **ETL Pipeline** - Extract (PDF) → Transform (chunk) → Load (summarize)
2. **Handling Large Data** - Breaking data into manageable chunks
3. **Provider Abstraction** - Supporting multiple LLM backends
4. **Configuration Management** - Centralized settings
5. **Error Handling** - Graceful failures with helpful messages
6. **Pipeline Orchestration** - Coordinating multiple API calls
7. **Metadata Tracking** - Recording which model/parameters were used

## Future Enhancements

- [ ] Support DOCX, PPTX documents
- [ ] Batch processing with progress bar
- [ ] Custom prompts per role (Data Scientist, ML Engineer, etc.)
- [ ] Web UI for drag-and-drop resumesor upload
- [ ] Vector embeddings for semantic similarity
- [ ] Database storage for summaries
- [ ] Comparison mode (evaluate multiple candidates)
- [ ] Export to PDF/CSV formats

## Requirements

- Python 3.8+
- 4GB RAM minimum
- For local models: Ollama installed (https://ollama.ai)
- For cloud models: API keys from OpenAI/Anthropic

## Dependencies

```
PyMuPDF==1.23.1        # PDF text extraction
openai==1.33.0         # LLM API client
tiktoken==0.4.0        # Token counting
rich==13.6.0           # Beautiful console output
python-dotenv==1.0.0   # Environment variables
pytest                 # Testing (dev only)
```

## Common Use Cases

### 1. Resume Screening
```python
summary, model = summarize_pdf("resume.pdf", model="mistral")
# Output: Hiring evaluation with strengths/gaps
```

### 2. Document Analysis
```python
summary, model = summarize_pdf("research_paper.pdf", model="gpt-4")
# Output: Key findings and insights
```

### 3. Content Extraction
```python
summary, model = summarize_pdf("contract.pdf", model="claude-3-opus")
# Output: Contract terms and obligations
```

## Learning Resources

- **Token Counting:** Understanding how LLMs count text
  - Read: https://platform.openai.com/tokenizer
  - Practice: Use `tiktoken` library

- **Context Windows:** Why models have limits
  - Read: Model documentation on official sites
  - Experiment: Try different safety factors

- **Prompt Engineering:** How to get better outputs
  - Test: Modify system prompts in `summarizer.py`
  - Iterate: See how different instructions change results

## License

Educational project for teaching data engineering concepts.

## Author

Created for comprehensive data engineering education focusing on real-world LLM applications.
