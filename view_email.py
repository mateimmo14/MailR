import os
import sys,imaplib,email
sys.stdout=open(os.devnull, "w")
sys.stderr=open(os.devnull, "w")
IMAP_SERVERS = {
    "gmail.com": "imap.gmail.com",
    "outlook.com": "imap-mail.outlook.com",
    "hotmail.com": "imap-mail.outlook.com",
    "live.com": "imap-mail.outlook.com",
    "yahoo.com": "imap.mail.yahoo.com",
    "yahoo.co.uk": "imap.mail.yahoo.com",
    "icloud.com": "imap.mail.me.com",
    "me.com": "imap.mail.me.com",
    "aol.com": "imap.aol.com",
    "protonmail.com": "imap.protonmail.com",
    "zoho.com": "imap.zoho.com",
    "gmx.com": "imap.gmx.com",
    "gmx.net": "imap.gmx.net",
    "gmx.de": "imap.gmx.net",
    "mail.com": "imap.mail.com",
    "yandex.com": "imap.yandex.com",
    "yandex.ru": "imap.yandex.ru",
    "fastmail.com": "imap.fastmail.com",
    "fastmail.fm": "imap.fastmail.com",
    "tutanota.com": "imap.tutanota.com",
    "office365.com": "outlook.office365.com",
}
import webview
from email.header import decode_header,make_header
def fetch_email(email_id, address, password):
    mail= imaplib.IMAP4_SSL(IMAP_SERVERS[address.split("@")[1]])
    mail.login(address, password)
    mail.select("inbox")
    status, msg = mail.fetch(email_id, '(RFC822)')
    data = email.message_from_bytes(msg[0][1])
    final = ""
    html_body = ""
    plain_body = ""
    if data.is_multipart():

        for part in data.walk():
            if part.get_content_type() == "text/html" and not html_body:
                html_body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")
            elif part.get_content_type() == "text/plain" and not html_body:
                plain_body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")


    else:
        if data.get_content_type() == "text/html" and not html_body:
            html_body = data.get_payload(decode=True).decode(data.get_content_charset() or "utf-8")
        elif data.get_content_type() == "text/plain" and not html_body:
            plain_body = data.get_payload(decode=True).decode(data.get_content_charset() or "utf-8")

    mail.logout()
    return {
        "Id": int(email_id.decode()),
        "Subject": str(make_header(decode_header(data["Subject"]))),
        "From": str(make_header(decode_header(data["From"]))),
        "To": str(make_header(decode_header(data["To"]))),
        "Content": html_body if html_body else f"<pre>{plain_body}</pre>"

    }

def spawn_text(text, title="popup"):

    webview.create_window(title, html=text, )
    webview.start()
def view_email(email_id, address, password):

    data = fetch_email(email_id, address, password)
    final = f"<b>Subject: {data["Subject"]}</b><br>From: {data['From']}<br>To: {data['To']}<hr><br><br>{data['Content']}"



    spawn_text(final, "email")
email_id = sys.argv[1].encode()
address = str(sys.argv[2])
password = str(sys.argv[3])
view_email(email_id, address, password)

