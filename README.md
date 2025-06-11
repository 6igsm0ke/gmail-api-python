# 📬 Gmail API Auto-Reply with Gemini 1.5

This project automatically replies to the most recent Gmail message using the **Gemini 1.5 Flash** model. It also supports replying to standalone `.eml` files.

## 🚀 Features

* 📩 Reads the latest email from your Gmail inbox
* 🔁 Automatically generates a response using Gemini 1.5 Flash
* ✍️ Sends a reply to the sender
* 📎 Parses `.docx` and `.xlsx` attachments (if present)
* 📨 Supports standalone `.eml` files as input

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/6igsm0ke/gmail-api-python.git
cd gmail-api-python
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Gmail API

* Go to [Google Cloud Console](https://console.cloud.google.com/)
* Create a project and enable Gmail API
* Create OAuth2 credentials (Desktop App)
* Download the `client-secret.json` file and place it in the project root

## 📄 Scripts

### ▶️ `auto_reply.py`

Reads the last message in your Gmail inbox and replies with a Gemini-generated answer.

### ▶️ `reply_from_eml.py`

Reads a local `.eml` file and replies to the sender using Gmail API.

### 📦 Utility Files

* `gemini_helper.py`: wraps Gemini API calls
* `gmail_api.py`: initializes Gmail API
* `send_email.py`: handles sending email via Gmail API
* `utils.py`: reads `.docx`, `.xlsx` attachments

## ✅ Usage

### Auto-reply to Last Gmail

```bash
python auto_reply.py
```

### Reply to `.eml` File

```bash
python reply_from_eml.py
```

Then provide the path to your `.eml` file.

## 📚 Requirements

See `requirements.txt`.

## 🔐 Security

This project uses OAuth2 flow. Credentials are securely stored in `token.json` (auto-generated).

---

Made with ❤️ by 6igsm0ke
