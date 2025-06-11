import os
import email
from email import policy
from email.parser import BytesParser
from gemini_helper import generate_gemini_reply
from send_email import send_email
from bs4 import BeautifulSoup
from gmail_api import init_gmail_service    

def extract_eml_content(eml_path):
    with open(eml_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    subject = msg['subject']
    sender = msg['from']

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == 'text/plain':
                body = part.get_content()
                break
            elif content_type == 'text/html':
                html = part.get_content()
                soup = BeautifulSoup(html, 'html.parser')
                body = soup.get_text()
                break
    else:
        body = msg.get_content()

    return sender, subject, body


def reply_to_eml(eml_path):
    sender, subject, body = extract_eml_content(eml_path)
    print(f"📨 Parsed .eml: {subject} from {sender}\n")

    reply = generate_gemini_reply(body)

    service = init_gmail_service("client-secret.json")
    confirm = input("Do you want to send the reply? (yes/no): ").strip().lower()
    if confirm in ['yes', 'y']:
        
        send_email(
            service,
            to=sender,
            subject="Re: " + subject,
            body=reply
        )

        print("Reply sent!")
    else:
        print("Reply cancelled.")


if __name__ == "__main__":
    eml_file_path = input("Enter path to .eml file: ").strip()
    if os.path.exists(eml_file_path):
        reply_to_eml(eml_file_path)
    else:
        print("File not found.")