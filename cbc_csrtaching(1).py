# -*- coding: utf-8 -*-
"""CBC CSRTACHING.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1H2ev2O4HOA2Qg6iY-kVPRa9CVRw4jqQC
"""



"""# **DATA CLEANINING NOTEBOOK**"""

pip install beautifulsoup4 nltk

"""# **CLEANING**"""

import json
import re
import time
import os

# Function to clean the text (remove special characters, etc.)
def clean_text(text):
    print("🧹 Cleaning the text...")
    # Removing any non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII chars
    text = re.sub(r"[^a-zA-Z0-9.,!?/:;'’\-\s]", ' ', text)  # Remove unwanted characters
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize multiple spaces
    return text

# Function to fix incomplete sentences
def fix_incomplete_sentences(text):
    print("🧠 Fixing fragmented sentences...")
    # Basic sentence splitting using punctuation as delimiter
    sentences = re.split(r'(?<=[.!?])\s+', text)
    fixed_sentences = []

    i = 0
    while i < len(sentences):
        sentence = sentences[i].strip()
        # If the sentence is too short, try to combine with the next one
        if len(sentence.split()) < 4 or not sentence.endswith(('.', '?', '!')):
            if i + 1 < len(sentences):
                sentence += ' ' + sentences[i + 1]
                i += 1  # Skip next one
        fixed_sentences.append(sentence)
        i += 1

    return ' '.join(fixed_sentences)

# Batch processing function for large JSONL files
def process_jsonl_in_batches(input_file, output_file, batch_size=1000):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        batch = []
        for i, line in enumerate(infile, 1):
            try:
                data = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"⚠️ Error decoding line {i}: {e}")
                continue  # Skip invalid JSON lines

            original_text = data.get("text", "")

            if original_text:
                cleaned_text = clean_text(original_text)
                completed_text = fix_incomplete_sentences(cleaned_text)
                data["text"] = completed_text

            batch.append(data)

            # Write the batch to the output file when batch size is reached
            if len(batch) >= batch_size:
                for item in batch:
                    outfile.write(json.dumps(item, ensure_ascii=False) + '\n')
                batch.clear()  # Clear the batch
                print(f"✅ Batch {i//batch_size} processed...")

        # Write any remaining data in the last batch
        if batch:
            for item in batch:
                outfile.write(json.dumps(item, ensure_ascii=False) + '\n')

    print(f"\n🎉 Batch processing complete! Output saved to: {output_file}")

# === Prompt for file path ===
input_file_path = input("📂 Enter the path to your .jsonl file: ")
output_file_path = input("📂 Enter the path for the output .jsonl file: ")

if not os.path.exists(input_file_path):
    print("❌ Input file not found!")
    exit()

print("\n🚀 Starting batch processing...\n")
time.sleep(1)

process_jsonl_in_batches(input_file_path, output_file_path)



"""# **CLEANING WITH LLM MODEL**"""

!pip install spacy
!python -m spacy download en_core_web_sm

import json
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from tqdm import tqdm

# Load the model (you can replace with a different one)
model_name = "google/flan-t5-base"  # lightweight, works well for generation tasks
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Check for GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Function to clean/clarify a batch of text
def clarify_batch(texts, max_input_length=256, max_output_length=256):
    prompts = [f"Fix and rephrase the following educational statement: {t}" for t in texts]
    inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True, max_length=max_input_length).to(device)
    outputs = model.generate(**inputs, max_new_tokens=max_output_length)
    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return decoded

# === File Paths ===
input_file = input("📂 Enter path to your .jsonl file: ").strip()
output_file = input("💾 Enter output path: ").strip()

batch_size = 8  # can increase based on your system

# === Processing ===
print("\n🦾 Loading and cleaning using LLM...\n")
with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    batch = []
    lines = []

    for line in tqdm(infile, desc="🚀 Processing"):
        try:
            data = json.loads(line)
            text = data.get("text", "")
            if text:
                batch.append(text)
                lines.append(data)
        except json.JSONDecodeError:
            continue  # Skip bad lines

        if len(batch) >= batch_size:
            clarified = clarify_batch(batch)
            for i in range(len(clarified)):
                lines[i]['text'] = clarified[i]
                outfile.write(json.dumps(lines[i], ensure_ascii=False) + '\n')
            batch, lines = [], []

    # Final remaining batch
    if batch:
        clarified = clarify_batch(batch)
        for i in range(len(clarified)):
            lines[i]['text'] = clarified[i]
            outfile.write(json.dumps(lines[i], ensure_ascii=False) + '\n')

print("\n✅ LLM-based text refinement complete! Output saved to:", output_file)