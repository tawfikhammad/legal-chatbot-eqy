import PyPDF2

def is_scanned(pdf_path):

    is_scanned = True
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)

        for page_num in range(len(reader.pages)):
            text = reader.pages[page_num].extract_text()
            if text and text.strip():  
                is_scanned = False
                break
    return is_scanned