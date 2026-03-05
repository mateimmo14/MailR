import imaplib,os,platform,sys
from email.header import decode_header, make_header
import email,threading,tkinter as tk
def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
def login():
    global mail
    clear()
    address = input("Please enter your email address:\n> ")
    password = input("Please enter your password:\n> ")
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(address,password)
    except imaplib.IMAP4.error as e:
        print(e)
        return login()
global mail
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
                    body = part.get_payload(decode=True).decode(part.get_content_charset())
                    break
        else:
            body = msg.get_payload(decode=True).decode(msg.get_content_charset())
       #----- de reparat (nu merge decodingu) --------

        emails.append({
            "Id" : int(email_id),
            "Subject": str(make_header(decode_header(msg["Subject"]))),
            "From":str(make_header(decode_header(msg["From"]))),
            "To": str(make_header(decode_header(msg["To"])))  ,
            "Content": body

        })
        i += 1
    return emails
def spawn_text(text, title="popup"):
    max = 0
    for lines in text.split("\n"):
        if max < len(lines):
            max = len(lines)
    root = tk.Tk()
    root.title(title)
    lable = tk.Text(root, width=max)
    lable.insert("1.0", text)
    lable.configure(state="disabled")

    lable.pack()
    root.mainloop()
def view_emails():
    clear()
    amount = int(input("Please enter the amount of emails you wish to see:\n> "))
    emails = collect(amount)
    clear()
    final = ""
    for message in emails:
        final += f"Id: {message["Id"]}\nSubject: {message['Subject']}\nFrom: {message['From']}\n\n"
    threading.Thread(target=spawn_text, args=(final, "emails")).start()
    clear()
def main():
    login()
    clear()
    while True:
        clear()
        decision = int(input("1) View inbox\n2) Send email\n3) View email\n4) Exit\n> "))
        if decision == 1:
            view_emails()
        if decision == 4:
            clear()
            sys.exit(0)
        clear()
if __name__ == "__main__":
    main()


