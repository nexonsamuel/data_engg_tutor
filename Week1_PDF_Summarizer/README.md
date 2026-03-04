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
- **Jupyter Notebook Interface** - Interactive Day 1 example notebook

## Project Structure

```
week1/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── ollama.sh                          # Setup script for local models
├── .env.example                       # API key template
│
├── data/                              # Input PDF files
├── output/                            # Generated summaries
│
├── examples/
│   ├── day1.ipynb                    # Interactive Jupyter notebook (Day 1)
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

#### Option A: Interactive Jupyter Notebook (Recommended for Learning)

```bash
cd examples
jupyter notebook day1.ipynb
```

Then:
- Run Section 1: Imports (verify everything loads)
- Run Sections 2-4: Configuration and functions
- Run Section 5: Execute pipeline on your PDF
- Run Sections 6-7: View and save results
- Run Section 8: Advanced options (batch processing)

**Key Points:**
- Make sure your PDF is in `week1/data/`
- Results save to `week1/output/`
- Notebook uses relative paths (`../data/`, `../output/`)

#### Option B: Python Script (For Automation)

```bash
python examples/run_summary.py
```

The script will:
- Find all PDFs in the `data/` folder
- Summarize each one using the configured model
- Save results to `output/` with metadata

## Day 1 Jupyter Notebook Guide

### Running the Notebook

```bash
cd week1/examples
jupyter notebook day1.ipynb
```

### What Each Section Does

**Section 1: Setup & Dependencies**
- Imports all required libraries
- Sets up path for module imports: `from pdf_summarizer.pdf_parser import pdf_parser_func`
- Loads model configurations

**Section 2: Configuration & Constants**
- LLM_CONFIG - model and API settings
- CHUNKING_CONFIG - token limits
- PROMPTS - system prompts for summarization
- OUTPUT_DIR - where to save results

**Section 3: Utility Functions**
- `chunk_text_by_tokens()` - splits text by tokens
- `initialize_llm_client()` - creates LLM connection
- `call_llm()` - sends messages to LLM

**Section 4: Pipeline Functions**
- `summarize_pdf()` - main pipeline orchestration
- `save_results()` - saves with metadata and timestamps

**Section 5: Execute Pipeline**
- Runs complete pipeline on your PDF
- Shows step-by-step progress
- Displays final summary

**Section 6: Save & Display**
- Saves results to file
- Shows execution statistics

**Section 7: Format Output**
- Displays summary in formatted paragraphs

**Section 8: Advanced Options**
- `process_multiple_pdfs()` - batch process folder
- Placeholder for custom prompts

### Customization

**Change Model:**
```python
# In Section 2, modify:
LLM_CONFIG = MODEL_CONFIGS['mistral']  # or 'gpt-4', 'claude-3-sonnet'
```

**Adjust Chunk Size:**
```python
# In Section 2, modify:
'max_tokens': 1000  # Instead of 500
```

**Custom Prompts:**
```python
# In Section 2, modify PROMPTS dictionary:
PROMPTS['chunk_summarizer'] = "Your custom instructions..."
```

**Process Multiple PDFs:**
```python
# In Section 8, run:
all_results = process_multiple_pdfs('../data/')
```

## Supported Models

### Recommended (Local - Free)

| Model | Context | Quality | Speed | Size |
|-------|---------|---------|-------|------|
| **Mistral** | 8,192 | ⭐⭐⭐⭐⭐ | Fast | 4.1GB |
| Phi | 2,048 | ⭐⭐⭐ | Very Fast | 1.6GB |
| Neural Chat | 4,096 | ⭐⭐⭐⭐ | Fast | 4.2GB |
| TinyLLama | 2,048 | ⭐⭐ | Very Fast | 1.1GB |

### Cloud Options (Paid)

| Model | Context | Quality | Speed |
|-------|---------|---------|-------|
| GPT-4 | 8,192 | ⭐⭐⭐⭐⭐ | Medium |
| GPT-4 Turbo | 128,000 | ⭐⭐⭐⭐⭐ | Medium |
| Claude 3 Opus | 200,000 | ⭐⭐⭐⭐⭐ | Medium |
| Claude 3 Sonnet | 200,000 | ⭐⭐⭐⭐ | Fast |

**Default:** Mistral (excellent quality-to-resource ratio)

## Usage Examples

### Using Jupyter Notebook (Interactive)

```bash
cd examples
jupyter notebook day1.ipynb
# Then run each section sequentially
```

### Using Python Script (Batch)

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

In the Jupyter notebook (Section 2) or in `summarizer.py`:

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

To customize for different roles, modify these prompts in the notebook or `summarizer.py`.

## Output Format

Summaries are saved to `output/` with timestamps:

```
output/
├── nexon_samuel_summary.txt
├── resume_summary_20250225_160339.txt
└── ...
```

Each file contains:
```
================================================================================
PDF SUMMARIZATION RESULT
================================================================================

Generated: 2026-02-25T16:03:39.123456
Model: mistral
PDF: ../data/Nexon_Samuel.pdf
Chunks Processed: 3

================================================================================
FINAL SUMMARY
================================================================================

[Evaluation text here...]

================================================================================
CHUNK SUMMARIES
================================================================================

[CHUNK 1]
[Summary of chunk 1...]

[CHUNK 2]
[Summary of chunk 2...]
```

## Understanding Token Chunking

### Why Chunking?

LLMs have a **context window** - maximum tokens they can process:
- TinyLLama: 2,048 tokens
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

### 5. Multi-Stage Processing
**Decision:** Summarize chunks independently, then synthesize final output
**Why:** Preserves context better than single-pass summarization for large documents.

## Troubleshooting

### Ollama Connection Issues
```
Error: Connection refused
```
**Solution:** Make sure Ollama is running:
```bash
ollama serve
```

### Model Not Found
```
Error: Model 'mistral' not found
```
**Solution:** Pull the model first:
```bash
ollama pull mistral
```

### Python Module Not Found
```
ModuleNotFoundError: No module named 'pdf_summarizer'
```
**Solution (Jupyter):** Make sure Section 1 includes:
```python
import sys
from pathlib import Path

current_dir = Path.cwd()
week1_path = str(current_dir.parent)  # Go up to week1/
sys.path.insert(0, week1_path)
```

### PDF File Not Found
```
FileNotFoundError: [Errno 2] No such file or directory: '../data/file.pdf'
```
**Solution:** 
- Make sure PDF is in `week1/data/`
- Check file name matches exactly
- Use relative paths from `examples/` directory

## Development

### Running Tests

```bash
pytest tests/
```

### Adding a New Model

1. Add configuration to `pdf_summarizer/model_constants.py`:
```python
MODEL_CONFIGS['new-model'] = {
    'name': 'new-model',
    'base_url': '...',
    'api_key': '...',
    'context_window': 8192,
    'provider': 'provider_name',
    'encoding': 'cl100k_base'
}
```

2. Update in Jupyter notebook or use in code:
```python
summary, model = summarize_pdf('file.pdf', model='new-model')
```

### Modifying the Pipeline

Each component is modular:
- `pdf_parser.py` - Change PDF extraction logic
- `chunker.py` - Change chunking algorithm
- `summarizer.py` - Change summarization logic
- `model_constants.py` - Change model configs

## Performance Tips

1. **Use Mistral** - Better quality than TinyLLama, faster than GPT-4
2. **Adjust chunk size** - Larger chunks = better context but more processing
3. **Batch processing** - Process multiple PDFs in one notebook run
4. **Use local models** - Free and fast (Mistral > Phi > TinyLLama)

## References

- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Tiktoken GitHub](https://github.com/openai/tiktoken)
- [Ollama Documentation](https://ollama.ai/)

## License

This project is provided as-is for educational purposes.