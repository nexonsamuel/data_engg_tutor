from openai import OpenAI
from rich.console import Console
from .pdf_parser import pdf_parser_func
from .chunker import chunk_text_by_tokens
from .model_constants import (
    MODEL_CONFIGS,
    DEFAULT_MODEL,
    DEFAULT_SAFETY_FACTOR,
)

console = Console()

def summarize_pdf(path, model=DEFAULT_MODEL, safety_factor=DEFAULT_SAFETY_FACTOR):
    """
    Summarize a PDF using specified model with dynamic token chunking.
    
    Args:
        path: Path to PDF file
        model: Model name (default: "tinyllama")
               Available: "tinyllama", "gpt-4", "gpt-4-turbo", "claude-3-sonnet", etc.
        safety_factor: Fraction of context window to use for chunks (default: 0.30)
    
    Returns:
        str: Final summary of the PDF
    
    Raises:
        ValueError: If model is not supported
    """
    # Validate model
    if model not in MODEL_CONFIGS:
        available = ", ".join(MODEL_CONFIGS.keys())
        console.print(
            f"[red]Error: Model '{model}' not supported.[/red]\n"
            f"[yellow]Available models: {available}[/yellow]"
        )
        raise ValueError(f"Model '{model}' not supported")
    
    config = MODEL_CONFIGS[model]
    
    # Calculate max_tokens dynamically
    max_tokens = int(config["context_window"] * safety_factor)
    
    # Initialize client
    client = OpenAI(
        base_url=config["base_url"],
        api_key=config["api_key"]
    )

    # Parse PDF
    console.print("[cyan]Parsing PDF...[/cyan]")
    pdf_text = pdf_parser_func(path)
    chunks = chunk_text_by_tokens(pdf_text, max_tokens=max_tokens, encoding=config["encoding"])
    console.print(f"[green]✓[/green] PDF parsed ({len(chunks)} chunks)\n")

    summaries = []

    # Summarize each chunk
    console.print(f"[cyan]Summarizing chunks using {model}...[/cyan]")
    for chunk in chunks:
        messages = [
            {
            "role": "system", 
            "content": "You are evaluating a Data Engineer candidate. Extract only: work experience, technical skills, cloud platforms, and key achievements. Be factual and concise."
            },
            {
            "role": "user", 
            "content": f"Summarize the relevant data engineering information from this text:\n\n{chunk}"
            }
        ]

        response = client.chat.completions.create(
            model=config["name"],
            messages=messages
        )
        summaries.append(response.choices[0].message.content)

    console.print(f"[green]✓[/green] All chunks summarized\n")

    # Combine summaries
    combined_summary = "\n".join(summaries)

    # Final summary
    console.print("[cyan]Creating final summary...[/cyan]")
    final_response = client.chat.completions.create(
        model=config["name"],
        messages=[
            {
            "role": "system", 
            "content": "You are an AI Head of a data engineering team evaluating a candidate's resume for a Data Engineer position. Your job is to provide a crisp, professional evaluation based on the information provided. Assess their: 1) Relevant experience, 2) Technical skills, 3) Cloud platform expertise, 4) Data pipeline/ETL knowledge, 5) Overall fit for the role. Be objective and constructive."
            },
            {
            "role": "user", 
            "content": f"Based on this candidate's information, provide a concise hiring evaluation for a Data Engineer role:\n\n{combined_summary}"
            }
        ]
    )

    console.print("[green]✓[/green] Summary complete\n")
    
    return final_response.choices[0].message.content, model