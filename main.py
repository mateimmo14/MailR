import imaplib,os,platform,sys,time
from email.header import decode_header, make_header
import email,threading,tkinter
import smtplib
import inquirer
import bs4
import ttkthemes,tkinter as tk
from tkinter import scrolledtext
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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

def collect(amount):

    mail.select('inbox')
    status, msg_data = mail.search(None, "ALL")
    email_ids = msg_data[0].split()
    emails = []
    print(f"Total emails: {len(email_ids)}")
    i = 0
    for email_id in email_ids[::-1]:
        if i == amount:
            break
        status, msg = mail.fetch(email_id, '(RFC822)')
        msg = email.message_from_bytes(msg[0][1])
        body = ""
        if msg.is_multipart():

            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")
                    break
        else:
            body = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8")


        emails.append({
            "Id" : int(email_id),
            "Subject": str(make_header(decode_header(msg["Subject"]))),
            "From":str(make_header(decode_header(msg["From"]))),
            "To": str(make_header(decode_header(msg["To"])))  ,
            "Content": body

        })
        i += 1
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
        text = tk.scrolledtext.ScrolledText(widget)
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
        input(f"{e}\nAn error occurred\nPress any key to continue...")
        return
def spawn_text(text, title="popup"):
    max_width = 0
    for lines in text.split("\n"):
        if max_width < len(lines):
            max_width = len(lines)
    root = ttkthemes.ThemedTk(theme="equilux")
    root.title(title)
    lable = tk.Text(root, width=max_width if max_width > 700 else 700, height=500)
    lable.insert("1.0", text)
    lable.configure(state="disabled")

    lable.pack()
    root.mainloop()
def view_emails():
    try:
        clear()
        amount = int(input("Please enter the amount of emails you wish to see:\n> "))
        emails = collect(amount)
        clear()
        final = ""
        for message in emails:
            final += f"Id: {message["Id"]}\nSubject: {message['Subject']}\nFrom: {message['From']}\n\n"
        threading.Thread(target=spawn_text, args=(final, "emails")).start()
        clear()
    except:
        clear()
        input("An error occurred\nPress any key to continue...")
        return
def view_email():
    try:
        clear()
        mail.select('inbox')
        status, msg_data = mail.search(None, "ALL")
        email_ids = msg_data[0].split()
        email_id = int(input("Please enter the ID of the email you wish to view (Or enter -1 to view the latest email):\n> "))

        mail.select('inbox')
        if email_id == -1:
            email_id = len(email_ids)
        data = email.message_from_bytes(mail.fetch(str(email_id).encode(), '(RFC822)')[1][0][1])
        final = f"Subject: {data["Subject"]}\nFrom: {data['From']}\nTo: {data['To']}\n\n"
        if data.is_multipart():
            for part in data.walk():
                if part.get_content_type() == "text/plain":
                    final += part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")
                elif part.get_content_type() == "text/html":
                    final += bs4.BeautifulSoup(part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8"), "html.parser").get_text()
        else:

                final += bs4.BeautifulSoup(data.get_payload(decode=True).decode(data.get_content_charset() or "utf-8"), "html.parser").get_text()

        spawn_text(final, "Email")
    except Exception as e:
        clear()
        input(f"{e}\nAn error occurred\nPress any key to continue...")
        return
def main():
    login()
    clear()
    while True:


        decision = inquirer.prompt([
                inquirer.List('decision', message="Welcome to MailR! Please select an option from below", choices=["1)View inbox","2)Send email", "3)View email", "4)Exit"])
            ])['decision']
        #decision = int(input("1) View inbox\n2) Send email\n3) View email\n4) Exit\n> "))
        if decision[0] == '1':
            view_emails()
        if decision[0] == '2':
            send_mail()
        if decision[0] == '3':
            view_email()
        if decision[0] == '4':
            clear()
            sys.exit(0)
        clear()
if __name__ == "__main__":
    main()


