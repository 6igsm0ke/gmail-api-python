from pathlib import Path
from gmail_api import init_gmail_service, send_email

client_secret_file = 'client_secret.json'

service = init_gmail_service(client_secret_file)

to_address = 'qosbayevadilet@gmail.com'
email_subject = 'Test Email' 
email_body = 'This is a test email sent using the Gmail API.'

response_email_sent = send_email(
    service,
    to_address,
    email_subject,
    email_body,
    body_type='plain',
)

print(response_email_sent)