import tiktoken

def chunk_text_by_tokens(text, max_tokens=500, encoding='cl100k_base'):
    """
    Split text into token-safe chunks for TinyLlama.
    """
    encoder = tiktoken.get_encoding(encoding)
    tokens = encoder.encode(text)
    chunks = []

    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk_text = encoder.decode(chunk_tokens)
        chunks.append(chunk_text)

    return chunks