import requests
from pathlib import Path
import sys
from datetime import datetime
from rich.console import Console

# Add parent folder to sys.path for imports
sys.path.append(str(Path(__file__).parent.parent))
from pdf_summarizer import summarize_pdf

console = Console()

# Check if Ollama/TinyLlama server is running
SERVER_URL = "http://localhost:11434/v1"

console.print("[cyan]Checking Ollama server...[/cyan]")

try:
    r = requests.get(f"{SERVER_URL}/models", timeout=2)
    r.raise_for_status()
    console.print("[green]✓ Server is running\n[/green]")
except requests.RequestException:
    console.print(
    f"[red]✗ Cannot connect to server at {SERVER_URL}[/red]\n"
    "[yellow]Make sure Ollama is running. You can start with the below command in the terminal:[/yellow]\n"
    "[cyan]./ollama.sh[/cyan]\n"
    )
    sys.exit(1)

# Path to the data folder
data_folder = Path(__file__).parent.parent / "data"

# Create output folder
output_folder = Path(__file__).parent.parent / "output"
output_folder.mkdir(exist_ok=True)

# Find all PDF files in the data folder
pdf_files = list(data_folder.glob("*.pdf"))
if not pdf_files:
    console.print(f"[red]No PDF files found in {data_folder}[/red]")
    sys.exit(1)

# Loop over each PDF and summarize
for pdf_path in pdf_files:
    console.print(f"\n[bold cyan]===== {pdf_path.name} =====[/bold cyan]\n")
    
    try:
        # summary = summarize_pdf(str(pdf_path))
        summary,model = summarize_pdf(str(pdf_path), model='mistral')
        console.print(f"[bold cyan]Summary:[/bold cyan]\n{summary}\n")
        
        # Save summary to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{pdf_path.stem}_summary_{timestamp}.txt"
        output_path = output_folder / output_filename
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"PDF: {pdf_path.name}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Model: {model}\n")
            f.write("=" * 80 + "\n\n")
            formatted_summary = summary.replace('. ', '.\n')
            f.write(formatted_summary)
        
        console.print(f"[green]✓ Summary saved to:[/green] {output_path}\n")
        console.print("=" * 80)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

console.print("[green]Done![/green]")