
# 🧹 JSONL Cleaner with LLM Enhancement

This Python script is a powerful tool designed to **clean**, **clarify**, and **enhance educational text data** (especially for Kenya's CBC Curriculum) stored in `.jsonl` (JSON Lines) format using an open-source **Language Model (LLM)** such as Google's `Flan-T5`.

---

## 📌 What Does This Script Do?

The script performs the following:

1. **Reads your `.jsonl` file** containing text fields like:
   ```json
   {"text": "The CBC intends to be more practical and student-based."}
   ```
2. **Cleans and rephrases each `text` entry** to make it:
   - Grammatically correct
   - Clear and easy to understand
   - More complete and contextually sound

3. **Uses an LLM (`flan-t5-base`)** to rephrase in batches to reduce memory use.

4. **Writes cleaned text** back to a `.jsonl` file.

---

## 📂 Example Input Format

Each line should be a JSON object with a `text` key:

```json
{"text": "To achieve the national educational goals the government through KICD developed..."}
{"text": "What are the 7 core competencies in CBC?"}
```

---

## 💻 Installation Guide

This project works on both **CPU** and **GPU (CUDA)**.

### 1. 📦 Install Python Packages

**Create a virtual environment (optional but recommended):**
```bash
python3 -m venv venv
source venv/bin/activate  # For Windows use: venv\Scripts\activate
```

**Install requirements:**

```bash
pip install torch transformers tqdm
```

> ✅ If you are using a GPU, `torch` will automatically detect CUDA if your drivers are set up properly. If not, follow below.

---

## ⚡ CUDA Support for GPU Acceleration (Optional)

To use **GPU**:
- Make sure your machine has **CUDA-compatible GPU**
- Install `torch` with CUDA support:

```bash
# For CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

For other versions, visit: [https://pytorch.org/get-started/locally](https://pytorch.org/get-started/locally)

---

## 🚀 How to Use the Script

1. Run the Python script:
```bash
python clean_jsonl_with_llm.py
```

2. The script will prompt you:
```
📂 Enter path to your .jsonl file:
💾 Enter output path:
```

3. It will start processing in batches and show a progress bar like:
```
🚀 Processing: 696it [25:45,  4.40s/it]
```

4. Once finished, it will save the cleaned data to your output file.

---

## 🔁 Sample Cleaning Prompt

The LLM is prompted like this:

> Fix and rephrase the following educational statement: "To achieve the national educational goals the government through KICD developed..."

This ensures the text is **polished** and **aligned with daset quality quality**.

---

## 🧠 Model Used

- `google/flan-t5-base` (you can replace it with any other model from Hugging Face)
- Runs on CPU and GPU
- Can be swapped for larger models like `flan-t5-large`, `zephyr`, or `mistral` for even better quality (at the cost of compute)

---

## 🧪 Customization Tips

- 🔢 **Batch Size**: Increase `batch_size = 8` to higher values like `16` or `32` if you have enough memory.
- ✍️ **Prompting**: You can customize the prompt in the script to better fit your domain.
- 🧠 **Model**: Replace `"google/flan-t5-base"` with any other Hugging Face model like:
  - `t5-base`
  - `HuggingFaceH4/zephyr-7b-beta` *(needs GPU or inference API)*
  - `mistralai/Mistral-7B-Instruct` *(heavier model)*

---

## 🛠 Dependencies Summary

| Package         | Purpose                          |
|----------------|----------------------------------|
| `transformers` | Load and run LLMs from HuggingFace |
| `torch`        | Backend for model execution       |
| `tqdm`         | Progress bars                     |
| `json`         | Reading `.jsonl` data             |

---

## 📣 Contributions & Feedback

Have improvements or want to customize for another curriculum? Feel free to fork and send a pull request!

---

## 📧 Contact

Developed with 💙 by [Kariuki James](mailto:jamexkarix54@gmail.com)  
📞 Phone: 0718845849
          **Kenya**

---

## 🧠 Coming Soon

- [ ] GUI version (Streamlit)
- [ ] Support for other file types (.csv, .txt)
- [ ] Hugging Face API integration
- [ ] Grammar-only mode vs. rewrite mode

---
