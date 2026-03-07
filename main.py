import imaplib,os,platform,sys,time
import threading
from email.header import decode_header, make_header
import email
import smtplib



from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import textual

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
thread_local = threading.local()
def get_connection():
    if not hasattr(thread_local, 'mail'):
        thread_local.mail = imaplib.IMAP4_SSL(IMAP_SERVERS[address.split("@")[1]])
        thread_local.mail.login(address, password)
        thread_local.mail.select("inbox")
    return thread_local.mail

def fetch_email(email_id):
    mail = get_connection()
    status, msg = mail.fetch(email_id, '(BODY[HEADER.FIELDS (FROM TO SUBJECT)])')
    data = email.message_from_bytes(msg[0][1])
    return {
        "Id": int(email_id),
        "Subject": str(make_header(decode_header(data["Subject"]))),
        "From": str(make_header(decode_header(data["From"]))),
        "To": str(make_header(decode_header(data["To"])))
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

def send_mail(subject, to, msg):
    try:
        global address,password



        fr = address



        with smtplib.SMTP_SSL(SMTP_SERVERS[address.split("@")[1]]) as server:
            server.login(address, password)
            server.sendmail(fr, to, msg.as_string())

        return True
    except Exception:
        return False

import subprocess
from textual.widgets import *
from textual.containers import *


login()
clear()
email_amounts = None
while not isinstance(email_amounts, int):
    try:
        email_amounts = int(input("How many emails do you want to see?\n> "))
        clear()
    except ValueError:
        continue
clear()
print("Loading emails...")
emails_data = collect(email_amounts)
clear()
class CompactHorizontal(Horizontal):
    def on_mount(self):
        self.styles.height = "auto"
        self.styles.padding = 0
        self.styles.margin = 0

class CompactCollapsible(Collapsible):

    def on_mount(self):
        self.styles.margin = 0
class BodyInput(TextArea):
    def on_mount(self):
        self.styles.height= "80%"

class EmailButton(Button):
    def __init__(self, lemail):
        super().__init__(label="View full email")
        self.lemail = lemail

    def on_button_pressed(self, event):
        event.stop()
        event.prevent_default()
        if getattr(sys, 'frozen', False):
            subprocess.Popen([sys.executable, "--view_email", str(self.lemail["Id"]), address, password],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        else:
            subprocess.Popen([sys.executable, "view_email.py", str(self.lemail["Id"]), address, password],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
class EmailLabel(Label):
    def on_mount(self):
        self.styles.width ="80%"
class MailR(textual.app.App):
    emails = reactive(emails_data, recompose=True)



    BINDINGS = [("q", "quit", "Exit"), ("r", "refresh", "Refresh")]
    theme = "textual-dark"


    def action_refresh(self):
        self.run_worker(self._refresh_worker,thread=True)
    def _refresh_worker(self):
        self.emails = collect(email_amounts)


    def action_quit(self):
        sys.exit()
    def compose(self) -> textual.app.ComposeResult:
        yield Header()
        with TabbedContent():
            with TabPane(title="Inbox"):
                with VerticalScroll(id="inbox"):

                        for email in self.emails:
                            with CompactCollapsible(title=email["Subject"], collapsed=True):
                                yield CompactHorizontal(
                                    EmailLabel(f"From: {email['From']}\nTo: {email['To']}" ),

                                    EmailButton(email)

                                )
            with TabPane(title="Send Email"):
                with VerticalScroll():
                    yield Input(placeholder="Subject", id="subject")
                    yield Input(placeholder="To", id="to")
                    yield BodyInput(placeholder="Body (HTML can be used)", id="body")
                yield Button("Send", action="app.send")
                yield Label("", id="Succes")
        yield Footer()

    def action_send(self):
        subject = self.query_one("#subject", Input).value
        to = self.query_one("#to", Input).value
        body = self.query_one("#body", TextArea).text

        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = address
        msg["To"] = to
        msg.attach(MIMEText(body, "plain"))

        value = send_mail(subject, to, msg)
        if value:
            self.query_one("#Succes", Label).update("[green]Mail sent successfully")
        else:
            self.query_one("#Succes", Label).update("[red]Mail not sent")
        self.query_one("#subject", Input).value = ""
        self.query_one("#to", Input).value = ""
        self.query_one("#body", TextArea).clear()

if __name__ == "__main__":

    MailR().run()
    clear()

