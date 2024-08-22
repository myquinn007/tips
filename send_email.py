import smtplib


def send_email(subject, body):
    email = "Sender Email"
    receiver_email = 'receiver_email'


    subject = subject
    message = body

    text = f"Subject: {subject}\n\n{message}"
    stmt = 'smt.gmail.com'
    port = 587
    server = smtplib.SMTP(stmt, port)
    server.starttls()

    server.login(email, "get secret key from gmail")
    server.sendmail(email, receiver_email, message)
    