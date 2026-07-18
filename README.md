# AI Multi-Format File Query Tool

A lightweight Python tool that lets you "chat" with your own files. Upload a `.txt`, `.pdf`, `.docx`, `.csv`, or `.xlsx` file, ask a question in plain language, and get an AI-generated answer based only on that file's content, powered by Google's Gemini API, with automatic fallback to Groq if Gemini is unavailable.

## Why I built this

Most tutorials teach AI concepts in isolation, API calls, prompt engineering, file handling, without connecting them into something usable. This project combines all three into a single working tool: it reads real data from multiple file formats, securely calls an LLM, and returns a context-aware answer, entirely from scratch.

## Features

- **Multi-format support**: reads `.txt`, `.pdf`, `.docx`, `.csv`, and `.xlsx` files
- **Natural language queries**: ask any question about the file's content in plain English or Roman Urdu
- **Automatic LLM fallback**: if Gemini is unavailable (e.g. free-tier quota exceeded), the tool automatically retries the request with Groq (Llama 3.1) instead of crashing or showing an error
- **Secure API key handling**: keys are loaded from environment variables / Streamlit secrets, never hardcoded
- **Graceful error handling**: unsupported file types exit cleanly with a clear message, and if both LLM providers fail, the user gets a friendly message instead of a crash

## Tech Stack

- Python 3.13
- [Google Gemini API](https://ai.google.dev/) (`google-genai`), primary LLM
- [Groq API](https://groq.com/) (`groq`), fallback LLM (Llama 3.1 8B Instant)
- `pypdf`, PDF text extraction
- `python-docx`, Word document parsing
- `openpyxl`, Excel file parsing
- Built-in `csv` module, CSV parsing

## How It Works

1. User provides a file name (with extension).
2. The script detects the file type and extracts its text content using the appropriate library.
3. The user types a question about the file.
4. The extracted content + question are combined into a single prompt.
5. The prompt is sent to the Gemini API. If Gemini fails for any reason (rate limit, quota, network issue), the tool automatically retries the same prompt with Groq instead.
6. The model's answer is printed/displayed back to the user, the fallback happens transparently, without interrupting the experience.

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/HananAIBuilds/ai-file-query-tool.git
   cd ai-file-query-tool
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/), and a free Groq API key from [Groq Console](https://console.groq.com/keys), then set them as environment variables:
   ```bash
   # Windows PowerShell
   $env:GOOGLE_API_KEY="your_gemini_api_key_here"
   $env:GROQ_API_KEY="your_groq_api_key_here"

   # macOS/Linux
   export GOOGLE_API_KEY="your_gemini_api_key_here"
   export GROQ_API_KEY="your_groq_api_key_here"
   ```

   > `GROQ_API_KEY` is optional, the tool works with only `GOOGLE_API_KEY` set, but without it there's no automatic fallback if Gemini's quota runs out.

4. Run the script:
   ```bash
   python all_in_one.py
   ```

   Or launch the Streamlit web app:
   ```bash
   streamlit run app.py
   ```

## Deploying on Streamlit Community Cloud

Add both keys under **Settings → Secrets**:
```
GOOGLE_API_KEY = "your_gemini_api_key_here"
GROQ_API_KEY = "your_groq_api_key_here"
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
- Chunk large files to handle documents beyond the model's context window
- Add automated tests

## Live Demo

🔗 Try it here: [ai-file-query-tool.streamlit.app](https://ai-file-query-tool.streamlit.app/)

Upload a file, ask a question, get an instant AI-generated answer, no setup required.

## Author

Abdul Hanan, BSIT student, Machine Learning & AI enthusiast
[GitHub](https://github.com/HananAIBuilds/) · [LinkedIn](https://www.linkedin.com/in/abdul-hanan-0772952b4?utm_source=share_via&utm_content=profile&utm_medium=member_android)
