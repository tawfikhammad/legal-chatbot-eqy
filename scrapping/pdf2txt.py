import pytesseract
from io import BytesIO
import re
import pdfplumber
from pdf2image import convert_from_path
from bidi.algorithm import get_display
import warnings
warnings.filterwarnings("ignore")

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'


# clean the text extracted from scanned pdf
def clean_text(text):
    chars_to_remove = ['\u200F', '\u200E']  
    patterns_to_replace = [r'[0-9٠١٢٣٤٥٦٧٨٩]',  
                            r'[()/؟»|!]']
        
    # Remove unwanted characters
    for char in chars_to_remove:
        text = text.replace(char, '')

    # Replace patterns with spaces
    for pattern in patterns_to_replace:
        text = re.sub(pattern, ' ', text)
    
    return text

# extract text from scanned pdf 
def extractt_Spdf(file, language='arabic'):
    pages = convert_from_path(file, 500)
    text = ''
    image_counter = 1

    for page in pages:
        page_text = pytesseract.image_to_string(page,  lang= language[:3])
        page_text = page_text.replace("-\n", "")
        text += page_text
        image_counter += 1

        text = clean_text(text)

    return text


# extract text from native pdf 
# adjust the text extracted from pdf
def adjusttext(text):
    def reverse_line(line):
        parts = re.split(r'(\d+|[()])', line)
        print(parts)
        reversed_parts = [part[::-1] if not (part.isdigit() or part in "()") else part for part in parts]
        
        return ''.join(reversed_parts)
    
    lines = text.splitlines()
    reversed_lines = [reverse_line(line) for line in lines]
    return '\n'.join(reversed_lines)


def extractt_Npdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as f:
        pdf_file = BytesIO(f.read())

    with pdfplumber.open(pdf_file) as pdf_document:
        for page in pdf_document.pages:
            page_text = page.extract_text() or ""
            text += page_text
    
    text = get_display(text)
    # text = adjusttext(text)
    return text
