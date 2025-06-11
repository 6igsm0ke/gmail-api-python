import os
from docx import Document
import pandas as pd

def get_file_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.docx':
        return 'docx'
    elif ext == '.xlsx':
        return 'xlsx'
    else:
        return 'unknown'

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs if para.text.strip()])

def extract_text_from_xlsx(file_path):
    try:
        df = pd.read_excel(file_path, header=None)
        df.fillna('', inplace=True)  # заменить NaN на пустую строку
        return '\n'.join(df.astype(str).agg(' | '.join, axis=1).tolist())
    except Exception as e:
        return f"Ошибка при чтении Excel файла: {e}"
