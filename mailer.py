import smtplib

def send_email(email: str, password: str, subject: str, body: str):
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    try:
        server.login(email, password)
    except smtplib.SMTPAuthenticationError:
        print("Invalid credentials")
        return
    message = f"Subject: {subject}\n\n{body}"
    server.sendmail(email, email, message)
    server.quit()