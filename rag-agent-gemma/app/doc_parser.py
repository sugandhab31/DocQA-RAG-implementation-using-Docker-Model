from PyPDF2 import PdfReader

def parse_document(file_path) -> str:
    reader = PdfReader(file_path)
    all_text = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            cleaned = " ".join(text.split())
            all_text.append()
    return " ".join(all_text)