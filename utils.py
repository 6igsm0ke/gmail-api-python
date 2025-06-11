import os
from docx import Document
import pandas as pd
import fitz

def get_file_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    known_types = {
        '.docx': 'docx',
        '.xlsx': 'xlsx',
        '.pdf': 'pdf',
        '.jpg': 'jpg',
        '.jpeg': 'jpeg',
        '.png': 'png',
        '.webp': 'webp',
        '.csv': 'csv',
    }
    return known_types.get(ext, 'unknown')

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs if para.text.strip()])

def extract_text_from_xlsx(file_path):  
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, header=None)
        else:
            df = pd.read_excel(file_path, header=None)
            df.fillna('', inplace=True)
        return '\n'.join(df.astype(str).agg(' | '.join, axis=1).tolist())
    except Exception as e:
        return f"Error while reading Excel or CSV file {e}"

def extract_text_from_pdf(file_path):
    text = ''
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
        return text