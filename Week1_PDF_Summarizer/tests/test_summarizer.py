"""
Unit tests for the PDF summarizer module.
"""

import sys
import pytest
from pathlib import Path

# Ensure the project root is in sys.path (backup for conftest.py)
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from pdf_summarizer import summarize_pdf, chunk_text_by_tokens, pdf_parser_func


class TestChunker:
    """Tests for the text chunking functionality."""
    
    def test_chunk_text_by_tokens(self):
        """Test that text is properly chunked by tokens."""
        sample_text = "Hello world. " * 100  # Repeat text to ensure multiple chunks
        chunks = chunk_text_by_tokens(sample_text, max_tokens=50)
        
        # Should create multiple chunks
        assert len(chunks) > 1
        assert all(isinstance(chunk, str) for chunk in chunks)
        assert all(len(chunk) > 0 for chunk in chunks)
    
    def test_chunk_text_single_chunk(self):
        """Test chunking with text smaller than max_tokens."""
        sample_text = "Short text."
        chunks = chunk_text_by_tokens(sample_text, max_tokens=500)
        
        # Should return one chunk
        assert len(chunks) == 1
        assert chunks[0] == sample_text


class TestModelValidation:
    """Tests for model configuration validation."""
    
    def test_invalid_model_raises_error(self):
        """Test that using an invalid model raises ValueError."""
        with pytest.raises(ValueError):
            # Use a mock PDF path - error should happen before file access
            summarize_pdf("fake_path.pdf", model="invalid_model")


class TestPDFParser:
    """Tests for PDF parsing functionality."""
    
    def test_pdf_parser_function_exists(self):
        """Test that pdf_parser_func is callable."""
        assert callable(pdf_parser_func)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])