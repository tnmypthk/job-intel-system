from gmail_helper import get_gmail_service

print("Opening browser for Google authentication...")
service = get_gmail_service()
print("Authentication successful — token saved.")
print("You can now run: streamlit run app.py")