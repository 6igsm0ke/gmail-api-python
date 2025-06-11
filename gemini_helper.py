import os
import google.generativeai as genai
from dotenv import load_dotenv
import mimetypes

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_gemini_reply(email_text, instruction="Reply to the email in a professional manner, addressing the main points and providing a concise response."):
    response = model.generate_content([
        {"role": "user", "parts": [{"text": instruction}]},
        {"role": "user", "parts": [{"text": email_text}]}
    ])
    return response.text.strip()

def generate_reply_with_attachment(email_text, attachment_path):
    with open(attachment_path, "rb") as f:
        file_data = f.read()

    mime_type, _ = mimetypes.guess_type(attachment_path)

    file_part = {
        "mime_type": mime_type or "application/octet-stream",
        "data": file_data
    }

    response = model.generate_content([
        {"role": "user", "parts": [{"text": "Прочти вложение и составь ответ."}]},
        {"role": "user", "parts": [{"text": email_text}]},
        {"role": "user", "parts": [file_part]}
    ])
    return response.text.strip()
