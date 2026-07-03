"""
AI Multi-Format File Query Tool
--------------------------------
Reads a .txt, .pdf, .docx, .csv, or .xlsx file and lets the user
ask natural language questions about its content, powered by the
Gemini API.

Requires the GOOGLE_API_KEY environment variable to be set.
"""

import os
from google import genai


def read_file(file_name):
    """Detects file type by extension and extracts its text content."""

    if file_name.endswith(".txt"):
        with open(file_name, "r", encoding="utf-8") as file:
            return file.read()

    elif file_name.endswith(".pdf"):
        from pypdf import PdfReader
        reader = PdfReader(file_name)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    elif file_name.endswith(".docx"):
        import docx
        doc = docx.Document(file_name)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

    elif file_name.endswith(".csv"):
        import csv
        with open(file_name, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            return list(reader)

    elif file_name.endswith(".xlsx"):
        import openpyxl
        workbook = openpyxl.load_workbook(file_name, read_only=True)
        sheet = workbook.active
        data = list(sheet.iter_rows(values_only=True))
        workbook.close()
        return data

    else:
        print("There is no support available for this file type yet.")
        exit()


def main():
    file_name = input("Enter file name (with extension): ")
    my_data = read_file(file_name)
    print("Data received successfully!")

    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

    query = input("What do you want to know about this file? ")

    prompt = f"""Neechay mera data diya gaya hai. Isay carefully read or
observe karo, aur user jo bhi question poochay uska well organized aur
simple way mein ans do, sirf isi data ke mutabiq.

User question: {query}

Data:
{my_data}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print("\nAI Response:")
    print(response.text)


if __name__ == "__main__":
    main()
