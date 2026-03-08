import imaplib,os,platform,sys,time
import threading
from email.header import decode_header, make_header
import email
import smtplib

mail = None

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import textual
if len(sys.argv) > 1 and sys.argv[1] == "viewer":
    import os
    import sys, imaplib, email

    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")

    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")
    os.environ["PYWEBVIEW_GUI"] = "qt"
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
    from email.header import decode_header, make_header


    def fetch_email(email_id, address, password):
        mail = imaplib.IMAP4_SSL(IMAP_SERVERS[address.split("@")[1]])
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
        final = f'<p style="background-color: black; color: white;"><b>Subject: {data["Subject"]}</b><br>From: {data['From']}<br>To: {data['To']}<hr><br><br>{data['Content']}</p>'

        spawn_text(final, "email")


    email_id = sys.argv[2].encode()
    address = str(sys.argv[3])
    password = str(sys.argv[4])
    view_email(email_id, address, password)

    sys.exit()
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
def collect():

    mail.select('inbox')
    status, msg_data = mail.search(None, "ALL")
    email_ids = msg_data[0].split()
    emails = []
    if len(email_ids) < 500:
        with ThreadPoolExecutor(max_workers=7) as executor:
            emails = list(executor.map(fetch_email, email_ids[::-1]))
    else:
        with ThreadPoolExecutor(max_workers=7) as executor:
            emails = list(executor.map(fetch_email, email_ids[::-1][:500]))
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




emails_data = []

def search(subject):
    results = []
    for email in emails_data:
        if subject.lower() in email["Subject"].lower() or subject.lower() in email["From"].lower():
            results.append(email)
    return results

class CompactHorizontal(Horizontal):
    def on_mount(self):
        self.styles.height = "auto"
        self.styles.padding = 0
        self.styles.margin = 0

class CompactCollapsible(Collapsible):

    def on_mount(self):
        self.styles.margin = 1
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
            cmd = [sys.executable, "viewer", str(self.lemail["Id"]), address, password]
        else:
            cmd = [sys.executable, os.path.abspath(__file__), "viewer", str(self.lemail["Id"]), address, password]

        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)



class EmailLabel(Label):
    def on_mount(self):
        self.styles.width ="80%"
class SearchBar(Input):
    def on_mount(self):
        self.styles.width = "90%"
class LoginInput(Input):
    pass

#------------------LOGIN APP-------------------
class LoginApp(textual.app.App):
    BINDINGS = [("q", "quit", "Exit")]
    theme="atom-one-dark"
    CSS = """
        LoginInput {
            width: 30%;
        }
        CenterMiddle {
            align: center middle;
        }
        #login {
            margin-top: 3;
            align: center middle;
            
        }
        #login_label {
            margin-bottom: 3;
            text-style: bold;
        }
        Button {
            margin-left: 1;
        }
        
    """
    global mail
    def compose(self):
        global mail
        yield Header()
        if mail is None:
            with CenterMiddle():
                yield Label("[italic]Welcome to MailR, please log in to continue[/italic]", id="login_label", )
                yield LoginInput(placeholder="Username", id="username")
                yield LoginInput(placeholder="Password", id="password", password=True)

                yield Button("Login", id="login")
                yield Label("Hint: If you're using 2FA with Google go to https://myaccount.google.com/apppasswords")
                yield Label("", id="Suces")
        else:
            with CenterMiddle():
                yield Label("Login Succeeded! Loading emails...")
        yield Footer()
    def on_button_pressed(self, event):

        self._temp_address = self.query_one("#username", Input).value
        self._temp_password = self.query_one("#password", Input).value
        self.run_worker(self._login_worker, thread=True)


    def _login_worker(self):
        global mail,address,password,emails_data


        try:
            mail = imaplib.IMAP4_SSL(IMAP_SERVERS[self._temp_address.split("@")[1]])
            mail.login(self._temp_address, self._temp_password)
        except KeyError:
            self.call_from_thread(lambda: self.query_one("#Suces", Label).update("Sorry, that domain isn't supported."))
            mail = None
            return
        except:
            self.call_from_thread(lambda: self.query_one("#Suces", Label).update("Invalid username or password."))
            mail = None
            return
        address=self._temp_address
        password=self._temp_password
        self.call_from_thread(self.exit)


    def action_quit(self):
        sys.exit()
#------------------EMAIL APP---------------------
class MailR(textual.app.App):

    emails = reactive([], recompose=False)
    searched_emails = reactive([], recompose=False)

    def on_mount(self):
        global emails_data
        self.run_worker(self._refresh_worker,thread=True)

    BINDINGS = [("q", "quit", "Exit"), ("r", "refresh", "Refresh")]
    theme = "atom-one-dark"

    _refreshing = False
    def action_refresh(self):
        global emails_data
        if not self._refreshing:
            self._refreshing = True
            self.run_worker(self._refresh_worker,thread=True)
        emails_data = self.emails
    def _refresh_worker(self):
        global emails_data
        self.emails = collect()
        self._refreshing = False
        emails_data = self.emails


    def action_quit(self):
        sys.exit()
    def compose(self) -> textual.app.ComposeResult:
        yield Header()
        with TabbedContent():
#--------------------INBOX TAB--------------------------
            with TabPane(title="Inbox"):
                with VerticalScroll(id="inbox"):

                        for email in self.emails:
                            with CompactCollapsible(title=email["Subject"], collapsed=True):
                                yield CompactHorizontal(
                                    EmailLabel(f"From: {email['From']}\nTo: {email['To']}" ),

                                    EmailButton(email)

                                )
                        if self.emails == []:
                            yield Label("Emails are loading...", id="loadingding")
#------------------SEND EMAIL TAB------------------------------
            with TabPane(title="Send Email"):
                with VerticalScroll():
                    yield Input(placeholder="Subject", id="subject")
                    yield Input(placeholder="To", id="to")
                    yield BodyInput(placeholder="Body (HTML can be used)", id="body")
                yield Button("Send", action="app.send")
                yield Label("", id="Succes")
#-----------------------SEARCH TAB-----------------
            with TabPane(title="Search"):
                with CompactHorizontal():
                    yield SearchBar(placeholder="Enter search query", id="search_bar")
                    yield Button(label="Search", id="search_button", action="app.search")
                with VerticalScroll(id="search-results"):
                    for email in self.searched_emails:
                        with CompactCollapsible(title=email["Subject"], collapsed=True):
                            yield CompactHorizontal(

                                EmailLabel(f"From: {email['From']}\nTo: {email['To']}"),

                                EmailButton(email)

                            )
        yield Footer()

    def action_search(self):
        self.searched_emails = search(self.query_one("#search_bar", Input).value)

    async def watch_emails(self):

        try:
            scroll = self.query_one("#inbox", VerticalScroll)

        except:
            return
        children = list(scroll.query("*"))
        for child in children:
            await child.remove()
        for msg in self.emails:
            c = CompactCollapsible(CompactHorizontal(EmailLabel(f"From: {msg['From']}\nTo: {msg['To']}"), EmailButton(msg)) , title=msg["Subject"], collapsed=True)
            await scroll.mount(c)

    async def watch_searched_emails(self):
        try:
            scroll = self.query_one("#search-results", VerticalScroll)
        except:
            return

        children = list(scroll.query("*"))
        for child in children:
            await child.remove()
        for msg in self.searched_emails:
            c = CompactCollapsible(CompactHorizontal(EmailLabel(f"From: {msg['From']}\nTo: {msg['To']}"),EmailButton(msg)) , title=msg["Subject"], collapsed=True)
            await scroll.mount(c)




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
    LoginApp().run()
    MailR().run()
    clear()

