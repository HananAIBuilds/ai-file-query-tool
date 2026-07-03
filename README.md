# AI Multi-Format File Query Tool

A lightweight Python tool that lets you "chat" with your own files. Upload a `.txt`, `.pdf`, `.docx`, `.csv`, or `.xlsx` file, ask a question in plain language, and get an AI-generated answer based only on that file's content — powered by Google's Gemini API.

## Why I built this

Most tutorials teach AI concepts in isolation — API calls, prompt engineering, file handling — without connecting them into something usable. This project combines all three into a single working tool: it reads real data from multiple file formats, securely calls an LLM, and returns a context-aware answer, entirely from scratch.

## Features

- **Multi-format support**: reads `.txt`, `.pdf`, `.docx`, `.csv`, and `.xlsx` files
- **Natural language queries**: ask any question about the file's content in plain English or Roman Urdu
- **Secure API key handling**: key is loaded from an environment variable, never hardcoded
- **Graceful error handling**: unsupported file types exit cleanly with a clear message

## Tech Stack

- Python 3.13
- [Google Gemini API](https://ai.google.dev/) (`google-genai`)
- `pypdf` — PDF text extraction
- `python-docx` — Word document parsing
- `openpyxl` — Excel file parsing
- Built-in `csv` module — CSV parsing

## How It Works

1. User provides a file name (with extension).
2. The script detects the file type and extracts its text content using the appropriate library.
3. The user types a question about the file.
4. The extracted content + question are combined into a single prompt.
5. The prompt is sent to the Gemini API, and the model's answer is printed back to the user.

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/HananAIBuilds/-AI-file-query-tool.git
   cd AI-file-query-tool
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/) and set it as an environment variable:
   ```bash
   # Windows PowerShell
   $env:GOOGLE_API_KEY="your_api_key_here"

   # macOS/Linux
   export GOOGLE_API_KEY="your_api_key_here"
   ```

4. Run the script:
   ```bash
   python all_in_one.py
   ```

## Example

```
Enter file name (with extension): report.pdf
Data Received!!
What do you want to know in this file? Give me a 3-line summary
AI Response:
...
```

## Possible Future Improvements

- Add support for `.json` and image-based (scanned) PDFs via OCR
- Add a simple web interface (Streamlit)
- Chunk large files to handle documents beyond the model's context window
- Add automated tests

## Author

Abdul Hanan — BSIT student, Machine Learning & AI enthusiast
[GitHub](https://github.com/YOUR_USERNAME) · [LinkedIn](https://www.linkedin.com/in/abdul-hanan-0772952b4)
