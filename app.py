"""
AI Multi-Format File Query Tool — Streamlit Web App
-----------------------------------------------------
Upload a .txt, .pdf, .docx, .csv, or .xlsx file and ask questions
about its content, powered by the Gemini & Groq API 

Run locally with:
    streamlit run app.py

Deploy on Streamlit Community Cloud and add your GOOGLE_API_KEY, GROQ_API_KEY.
under Settings -> Secrets as:
    GOOGLE_API_KEY = "your_key_here"
    GROQ_API_KEY = "your_key_here"
"""

import streamlit as st
from google import genai
from groq import Groq


def read_file(uploaded_file):
    """Detects file type and extracts text content from an uploaded file object."""

    name = uploaded_file.name

    if name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")

    elif name.endswith(".pdf"):
        from pypdf import PdfReader
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    elif name.endswith(".docx"):
        import docx
        doc = docx.Document(uploaded_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

    elif name.endswith(".csv"):
        import csv
        import io
        text_stream = io.StringIO(uploaded_file.read().decode("utf-8"))
        reader = csv.reader(text_stream)
        return list(reader)

    elif name.endswith(".xlsx"):
        import openpyxl
        workbook = openpyxl.load_workbook(uploaded_file, read_only=True)
        sheet = workbook.active
        data = list(sheet.iter_rows(values_only=True))
        workbook.close()
        return data

    else:
        return None


def get_api_key():
    """Gets the Gemini API key from Streamlit secrets, or asks the user for it."""
    if "GOOGLE_API_KEY" in st.secrets:
        return st.secrets["GOOGLE_API_KEY"]
    return st.text_input("Enter your Gemini API key:", type="password")

def get_groq_api_key():
    """Gets the Groq API key from Streamlit secrets."""
    if "GROQ_API_KEY" in st.secrets:
        return st.secrets["GROQ_API_KEY"]
    return None  

def generate_response(prompt_text, google_api_key, groq_api_key):
    """Try Gemini first; if it fails (quota, network, etc.), fall back to Groq."""
    try:
        client = genai.Client(api_key=google_api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text
        )
        return response.text
    
    except Exception as e:
        print(f"Gemini failed, falling back to Groq. Error: {e}")
        
        if not groq_api_key:
            return "I apologize, the AI service (Gemini) is temporarily unavailable, and no backup is configured. Please try again shortly."
        
        try:
            groq_client = Groq(api_key=groq_api_key)
            groq_response = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt_text}]
            )
            return groq_response.choices[0].message.content
        
        except Exception as groq_error:
            print(f"Groq also failed. Error: {groq_error}")
            return "I apologize, our AI service is temporarily unavailable. Please try again in a moment."


# ---------- Streamlit UI ----------

st.set_page_config(page_title="AI File Query Tool", page_icon="📄")
st.title("📄 AI File Query Tool")
st.write("Upload your file here (.txt, .pdf, .docx, .csv, .xlsx) and Ask quries about it.")

api_key = get_api_key()
groq_api_key = get_groq_api_key() 

uploaded_file = st.file_uploader(
    "Select file",
    type=["txt", "pdf", "docx", "csv", "xlsx"]
)

query = st.text_input("What do you want to know about this file?")

if st.button("Ask"):
    if not api_key:
        st.error("First, enter your Gemini API key.")
    elif not uploaded_file:
        st.error("Upload ur file first.")
    elif not query:
        st.error("ask something.")
    else:
        with st.spinner("The file is being read, and a response is being generated using AI..."):
            my_data = read_file(uploaded_file)

            if my_data is None:
                st.error("This file type is not supported.")
            else:
                client = genai.Client(api_key=api_key)

                prompt = f"""My data is provided below. You carefully read and review it 
                and answer any questions asked by the user in a well-organized and simple manner, 
                strictly based on that data.
                Ensure that if the user does not select a specific language, your 'default' response is in plain English or Roman Urdu. 
                If the user desires a response in a different language, they will specify this in their query; otherwise, 
                your tone should be in plain English. However, if the user communicates in Roman Urdu, 
                the response should also be provided in Roman Urdu.

                User question: {query}

                Data:    {my_data}    
                                    """

                answer_text = generate_response(prompt, api_key, groq_api_key)
                st.subheader("AI Response:")
                st.write(answer_text)
