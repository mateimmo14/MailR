import imaplib,os,platform,sys,time
from email.header import decode_header, make_header
import email,threading,tkinter
import smtplib,json
import inquirer
from textual.layouts.vertical import VerticalLayout

os.environ["PYWEBVIEW_GUI"] = "qt"
import ttkthemes,tkinter as tk
from tkinter import scrolledtext
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import textual
import webview

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

SMTP_SERVERS = {
    "gmail.com": "smtp.gmail.com",
    "outlook.com": "smtp-mail.outlook.com",
    "hotmail.com": "smtp-mail.outlook.com",
    "live.com": "smtp-mail.outlook.com",
    "yahoo.com": "smtp.mail.yahoo.com",
    "yahoo.co.uk": "smtp.mail.yahoo.com",
    "icloud.com": "smtp.mail.me.com",
    "me.com": "smtp.mail.me.com",
    "aol.com": "smtp.aol.com",
    "protonmail.com": "smtp.protonmail.com",
    "zoho.com": "smtp.zoho.com",
    "gmx.com": "mail.gmx.com",
    "gmx.net": "mail.gmx.net",
    "gmx.de": "mail.gmx.net",
    "mail.com": "smtp.mail.com",
    "yandex.com": "smtp.yandex.com",
    "yandex.ru": "smtp.yandex.ru",
    "fastmail.com": "smtp.fastmail.com",
    "fastmail.fm": "smtp.fastmail.com",
    "tutanota.com": "smtp.tutanota.com",
    "office365.com": "smtp.office365.com",
}
import getpass
def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
def login():
    global mail,address,password
    clear()
    address = input("Please enter your email address:\n> ")
    password = getpass.getpass("Please enter your password:\n> ")
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVERS[address.split("@")[1]])


        mail.login(address,password)
    except (imaplib.IMAP4.error, smtplib.SMTPAuthenticationError) as e:
        clear()
        if str(e) == '[AUTHENTICATIONFAILED] Invalid credentials (Failure)':
            print("Invalid credentials. Please try again.\nHint: If you have 2FA on your email account, go to \033]8;;https://myaccount.google.com/apppasswords\033\\\033[94mhttps://myaccount.google.com/apppasswords\033[0m\033]8;;\033\\ and create a app password and use it here to sign in")
            time.sleep(2)
        elif str(e) == "LOGIN command error: BAD [b'Not enough arguments provided 5c2dc8763939e-495dbdb4356mb40785970122']":
            print("Invalid credentials. Please try again.\nHint: If you have 2FA on your email account, go to \033]8;;https://myaccount.google.com/apppasswords\033\\\033[94mhttps://myaccount.google.com/apppasswords\033[0m\033]8;;\033\\ and create a app password and use it here to sign in")
            time.sleep(2)
        else:
            print("Invalid credentials. Please try again.\nHint: If you have 2FA on your email account, go to \033]8;;https://myaccount.google.com/apppasswords\033\\\033[94mhttps://myaccount.google.com/apppasswords\033[0m\033]8;;\033\\ and create a app password and use it here to sign in")
            input("Press any key to continue...")
        return login()
    except KeyError:
        input("Sorry, that domain isn't supported!\nPress any key to continue...")
        return login()

def fetch_email(email_id):
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
        "Id": int(email_id),
        "Subject": str(make_header(decode_header(data["Subject"]))),
        "From": str(make_header(decode_header(data["From"]))),
        "To": str(make_header(decode_header(data["To"]))),
        "Content": html_body if html_body else f"<pre>{plain_body}</pre>"

    }

from concurrent.futures import ThreadPoolExecutor
def collect(amount):

    mail.select('inbox')
    status, msg_data = mail.search(None, "ALL")
    email_ids = msg_data[0].split()
    emails = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        emails = list(executor.map(fetch_email, email_ids[::-1][:amount]))
    return emails

def send_mail():
    try:
        global address,password,cancelled
        clear()
        msg = MIMEMultipart()
        subject = input("Subject: ")
        fr = address
        to = input("To: ")
        clear()
        #-----enter text window----

        cancelled = [False]

        widget = ttkthemes.ThemedTk(theme="equilux")
        widget.geometry("700x500")
        widget.title("Mail Content")
        text = scrolledtext.ScrolledText(widget)
        def rais():
            global cancelled
            clear()
            widget.destroy()
            input("Process aborted\nPress any key to continue...")
            cancelled=[True]
        def submit():
            msg["Subject"] = subject
            msg["From"] = fr
            msg["To"] = to
            msg.attach(MIMEText(text.get("1.0", "end-1c"), "plain"))
            widget.destroy()

        submit = tk.Button(widget, command=submit, text="Submit")
        exi = tk.Button(widget, command=rais, text="Exit", )
        text.pack()
        submit.pack(pady=20)
        exi.pack(padx=20)

        print("Submit the content to continue...")
        widget.mainloop()
        if not cancelled[0]:

            with smtplib.SMTP_SSL(SMTP_SERVERS[address.split("@")[1]]) as server:
                server.login(address, password)
                server.sendmail(msg["From"], msg["To"], msg.as_string())
        clear()
    except Exception as e:
        clear()
        input(f"An error occurred\nPress any key to continue...")
        return

import subprocess
from textual.widgets import *
from textual.containers import *
login()
class CompactHorizontal(Horizontal):
    def on_mount(self):
        self.styles.height = "auto"
        self.styles.padding = 0
        self.styles.margin = 0
class CompactCollapsible(Collapsible):

    def on_mount(self):
        self.styles.margin = 0
        self.styles.padding = 0
class EmailButton(Button):
    def __init__(self, lemail):
        super().__init__(label="View full email")
        self.lemail = lemail
    def on_button_pressed(self, event):
        event.prevent_default()
        if getattr(sys, 'frozen', False):
            subprocess.Popen([sys.executable, "--view_email", str(self.lemail["Id"]), address, password],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        else:
            subprocess.Popen([sys.executable, "view_email.py", str(self.lemail["Id"]), address, password],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

class MailR(textual.app.App):

    emails = collect(10)

    BINDINGS = [("q", "quit", "Exit")]
    theme = "textual-dark"

    def action_quit(self):
        sys.exit()
    def compose(self) -> textual.app.ComposeResult:
        yield Header()
        with TabbedContent():
            with TabPane(title="Inbox"):
                with VerticalScroll():

                        for email in self.emails:
                            with CompactCollapsible(title=email["Subject"], collapsed=True):
                                yield CompactHorizontal(
                                    Label(f"From: {email['From']}\nTo: {email['To']}"),
                                    EmailButton(email)
                                )

        yield Footer()

if __name__ == "__main__":

    MailR().run()


