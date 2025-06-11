import re
import base64
import tempfile
from bs4 import BeautifulSoup
from gmail_api import init_gmail_service, get_email_message, get_email_message_details, send_email
from gemini_helper import *
from utils import get_file_type, extract_text_from_docx, extract_text_from_xlsx, extract_text_from_pdf

def extract_attachment_path_and_type(service, msg_id, parts):
    for part in parts:
        filename = part.get("filename")
        if filename and "attachmentId" in part.get("body", {}):
            attachment_id = part["body"]["attachmentId"]
            attachment = service.users().messages().attachments().get(
                userId="me",
                messageId=msg_id,
                id=attachment_id
            ).execute()

            file_data = base64.urlsafe_b64decode(attachment["data"])
            suffix = '.' + filename.split('.')[-1].lower() if '.' in filename else ''
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                tmp_file.write(file_data)
                tmp_path = tmp_file.name

            file_type = get_file_type(tmp_path)
            return tmp_path, file_type
    return None, None


def auto_reply_to_last_email():
    service = init_gmail_service("client-secret.json")
    messages = get_email_message(service, max_results=1)

    if not messages:
        print("❌ Message not found")
        return

    msg_id = messages[0]["id"]
    msg_details = get_email_message_details(service, msg_id)

    print(f"\n📥 Message: {msg_details['subject']}")
    print(f"✉️ From: {msg_details['sender']}")
    print(f"📄 Body:\n{msg_details['body'][:500]}...\n")

    soup = BeautifulSoup(msg_details["body"], "html.parser")
    plain_text = soup.get_text(separator="\n").strip()

    reply_text = ""

    if msg_details["has_attachments"]:
        try:
            full_msg = service.users().messages().get(userId="me", id=msg_id).execute()
            parts = full_msg["payload"].get("parts", [])
            attachment_path, file_type = extract_attachment_path_and_type(service, msg_id, parts)

            if attachment_path:
                if file_type in ['jpg', 'jpeg', 'png', 'webp']:
                    reply_text = generate_reply_with_attachment(plain_text, attachment_path)
                elif file_type == 'pdf':
                    text = extract_text_from_pdf(attachment_path)
                    reply_text = generate_gemini_reply(text)
                elif file_type == 'docx':
                    text = extract_text_from_docx(attachment_path)
                    reply_text = generate_gemini_reply(text)
                elif file_type in ['xlsx', 'csv']:
                    text = extract_text_from_xlsx(attachment_path)
                    reply_text = generate_gemini_reply(text)
                else:
                    reply_text = f"Unsupported file type: {file_type}"
            else:
                reply_text = "No valid attachment found."
        except Exception as e:
            print("Couldn't process attachment:", e)
            reply_text = "Error processing attachment. Please check manually."
    else:
        reply_text = generate_gemini_reply(plain_text)

    print(f"\nReply:\n{reply_text}\n")
    confirm = input("Do you want to send this reply? (yes/no): ").strip().lower()
    if confirm in ['yes', 'y']:
        sender_match = re.search(r"<(.+?)>", msg_details["sender"])
        sender_email = sender_match.group(1) if sender_match else msg_details["sender"]

        send_email(
            service,
            to=sender_email,
            subject="Re: " + msg_details["subject"],
            body=reply_text
        )
        print("Reply sent!")
    else:
        print("Reply cancelled.")

if __name__ == "__main__":
    auto_reply_to_last_email()