import smtplib

def send_email(email: str, password: str, subject: str, body: str):
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login(email, password)
    message = f"Subject: {subject}\n\n{body}"
    server.sendmail(email, email, message)
    server.quit()