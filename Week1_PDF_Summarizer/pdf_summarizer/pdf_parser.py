import fitz  # PyMuPDF

def pdf_parser_func(path):
    """Extract text from PDF using PyMuPDF."""
    text = ""
    doc = fitz.open(path)
    for page in doc:
        text += page.get_text()
    return text