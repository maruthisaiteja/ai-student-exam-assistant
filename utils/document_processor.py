import PyPDF2

def extract_text_from_file(uploaded_file):
    """
    Extracts text from uploaded PDF or TXT file.
    Returns string containing the extracted text.
    """
    if uploaded_file.name.lower().endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.lower().endswith(".txt"):
        return extract_text_from_txt(uploaded_file)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or TXT file.")

def extract_text_from_pdf(file_obj):
    try:
        reader = PyPDF2.PdfReader(file_obj)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

def extract_text_from_txt(file_obj):
    try:
        return file_obj.getvalue().decode("utf-8")
    except Exception as e:
        raise Exception(f"Error reading TXT: {str(e)}")
