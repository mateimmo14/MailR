import imaplib,os,platform,sys,time
from email.header import decode_header, make_header
import email,threading,tkinter as tk
import smtplib
from tkinter import scrolledtext
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
def login():
    global mail,address,password
    clear()
    address = input("Please enter your email address:\n> ")
    password = input("Please enter your password:\n> ")
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')


        mail.login(address,password)
    except (imaplib.IMAP4.error, smtplib.SMTPAuthenticationError) as e:
        clear()
        if str(e) == b'[AUTHENTICATIONFAILED] Invalid credentials (Failure)':
            print("Invalid credentials. Please try again.\nHint: If you have 2FA on your email account, go to \033]8;;https://myaccount.google.com/apppasswords\033\\\033[94mhttps://myaccount.google.com/apppasswords\033[0m\033]8;;\033\\ and create a app password and use it here to sign in")
            time.sleep(2)
        elif str(e) == "LOGIN command error: BAD [b'Not enough arguments provided 5c2dc8763939e-495dbdb4356mb40785970122']":
            print("Invalid credentials. Please try again.\nHint: If you have 2FA on your email account, go to \033]8;;https://myaccount.google.com/apppasswords\033\\\033[94mhttps://myaccount.google.com/apppasswords\033[0m\033]8;;\033\\ and create a app password and use it here to sign in")
            time.sleep(2)
        else:
            print("Invalid credentials. Please try again.\nHint: If you have 2FA on your email account, go to \033]8;;https://myaccount.google.com/apppasswords\033\\\033[94mhttps://myaccount.google.com/apppasswords\033[0m\033]8;;\033\\ and create a app password and use it here to sign in")
            input("Press any key to continue...")
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
        global address,password
        clear()
        msg = MIMEMultipart()
        msg["Subject"] = input("Subject: ")
        msg["From"] = address
        msg["To"] = input("To: ")
        clear()
        #-----enter text window----

        widget = tk.Tk()
        widget.geometry("700x500")
        widget.title("Mail content")
        text = tk.scrolledtext.ScrolledText(widget)

        def submit():

            msg.attach(MIMEText(text.get("1.0", "end-1c"), "plain"))
            widget.destroy()

        submit = tk.Button(widget, command=submit, text="Submit")
        text.pack()
        submit.pack(pady=20)
        print("Submit the content to continue...")
        widget.mainloop()


        with smtplib.SMTP_SSL('smtp.gmail.com') as server:
            server.login(address, password)
            server.sendmail(msg["From"], msg["To"], msg.as_string())
        clear()
    except:
        clear()
        input("An error occured\nPress any key to continue...")
        return
def spawn_text(text, title="popup"):
    max_width = 0
    for lines in text.split("\n"):
        if max_width < len(lines):
            max_width = len(lines)
    root = tk.Tk()
    root.title(title)
    lable = tk.Text(root, width=max_width)
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
        input("An error occured\nPress any key to continue...")
        return
def view_email():
    try:
        clear()
        email_id = int(input("Please enter the id of the email you wish to view:\n> "))

        mail.select('inbox')
        data = email.message_from_bytes(mail.fetch(str(email_id).encode(), '(RFC822)')[1][0][1])
        final = f"Subject: {data["Subject"]}\nFrom: {data['From']}\nTo: {data['To']}\n\n"
        if data.is_multipart():
            for part in data.walk():
                if part.get_content_type() == "text/plain":
                    final += part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")
        else:
            final += data.get_payload(decode=True).decode(data.get_content_charset() or "utf-8")
        spawn_text(final, "Email")
    except:
        clear()
        input("An error occured\nPress any key to continue...")
        return
def main():
    login()
    clear()
    while True:
        clear()
        decision = int(input("1) View inbox\n2) Send email\n3) View email\n4) Exit\n> "))
        if decision == 1:
            view_emails()
        if decision == 2:
            send_mail()
        if decision == 3:
            view_email()
        if decision == 4:
            clear()
            sys.exit(0)
        clear()
if __name__ == "__main__":
    main()


