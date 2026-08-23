import PyPDF2 #type: ignore
import os
import re

def read_pdf(file_path):
    """
    Reads text from a PDF file page by page.
    Skips unreadable or empty pages automatically.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for i, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text and not is_gibberish(page_text):
                    text += page_text + "\n"
            except Exception as e:
                print(f"Warning: Failed to read page {i}: {e}")
    if not text.strip():
        raise ValueError("The PDF contains no readable or valid text.")
    return text.strip()

def is_gibberish(text):
    """
    Returns True if text looks like gibberish: 
    mostly symbols, random chars, or empty after cleanup.
    """
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Remove symbols
    words = cleaned.split()
    # If there are almost no alphanumeric words, it's likely junk
    return len(words) < 5 or sum(c.isalpha() for c in cleaned) / (len(cleaned) + 1) < 0.3

def save_summary(summary, output_path="summary.txt"):
    """
    Saves the summary text to a specified file path.
    Defaults to 'summary.txt'.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary.strip())
    print(f"\nSummary saved to: {output_path}")
