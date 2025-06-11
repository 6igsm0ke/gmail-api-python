from gmail_api import init_gmail_service, get_email_message, get_email_message_details
client_secret_file = 'client_secret.json'

service = init_gmail_service(client_secret_file)
messages = get_email_message(service, max_results=5)

print(messages)


for msg in messages:
    details = get_email_message_details(service, msg['id'])
    if details:
        print(f"Subject: {details['subject']}")
        print(f"From: {details['sender']}")
        print(f"Recipients: {details['recipients']}")
        print(f"Body: {details['body'][:100]}")
        print(f"Snippet: {details['snippet']}")
        print(f"Has Attachments: {details['has_attachments']}")
        print(f"Date: {details['date']}")
        print(f"Starred: {details['star']}")
        print(f"Labels: {details['label']}")
        print('-' * 80)
        