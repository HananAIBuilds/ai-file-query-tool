"""
AI Multi-Format File Query Tool — Streamlit Web App
-----------------------------------------------------
Upload a .txt, .pdf, .docx, .csv, or .xlsx file and ask questions
about its content, powered by the Gemini API.

Run locally with:
    streamlit run app.py

Deploy on Streamlit Community Cloud and add your GOOGLE_API_KEY
under Settings -> Secrets as:
    GOOGLE_API_KEY = "your_key_here"
"""

import streamlit as st
from google import genai


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
    return st.text_input("Apni Gemini API key daalein:", type="password")


# ---------- Streamlit UI ----------

st.set_page_config(page_title="AI File Query Tool", page_icon="📄")
st.title("📄 AI File Query Tool")
st.write("Apni file upload karein (.txt, .pdf, .docx, .csv, .xlsx) aur us ke baray mein sawal poochein.")

api_key = get_api_key()

uploaded_file = st.file_uploader(
    "File chunein",
    type=["txt", "pdf", "docx", "csv", "xlsx"]
)

query = st.text_input("Aap kya jaanna chahte hain is file se?")

if st.button("Puchein"):
    if not api_key:
        st.error("Pehle apni Gemini API key daalein.")
    elif not uploaded_file:
        st.error("Pehle koi file upload karein.")
    elif not query:
        st.error("Koi sawal likhein.")
    else:
        with st.spinner("File padhi ja rahi hai aur AI se jawab liya ja raha hai..."):
            my_data = read_file(uploaded_file)

            if my_data is None:
                st.error("Yeh file type support nahi hai.")
            else:
                client = genai.Client(api_key=api_key)

                prompt = f"""Neechay mera data diya gaya hai. Isay carefully read aur
observe karo, aur user jo bhi question poochay uska well organized aur
simple andaz mein jawab do, sirf isi data ke mutabiq.

User question: {query}

Data:
{my_data}
"""

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                st.subheader("AI Response:")
                st.write(response.text)
