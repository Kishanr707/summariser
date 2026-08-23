from transformers import BartTokenizer, BartForConditionalGeneration #type: ignore
import torch #type: ignore

# Load model and tokenizer
model_name = 'facebook/bart-large-cnn'
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

def chunk_text(text, max_tokens=512):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        tokenized_len = len(tokenizer.encode(" ".join(current_chunk), truncation=False))
        if tokenized_len >= max_tokens:
            chunks.append(" ".join(current_chunk[:-1]))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks



def summarize_text(text, level):
    if level == 1:  # High (shortest)
        max_length = 100
        min_length = 30
    elif level == 2:  # Medium
        max_length = 200
        min_length = 60
    elif level == 3:  # Low (most detailed)
        max_length = 300
        min_length = 100
    else:
        raise ValueError("Invalid summary level.")

    chunks = chunk_text(text)
    print(f"[DEBUG] Chunks created: {len(chunks)}")
    summaries = []

    for chunk in chunks:
        inputs = tokenizer([chunk], return_tensors='pt', max_length=1024, truncation=True)
        summary_ids = model.generate(
            inputs['input_ids'],
            num_beams=4,
            length_penalty=2.0,
            max_length=max_length,
            min_length=min_length,
            early_stopping=True
        )
        chunk_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(chunk_summary)

    return "\n\n".join(summaries)
