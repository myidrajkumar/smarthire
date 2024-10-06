"""Email Utility"""

import smtplib
from email.mime.text import MIMEText


def send_exam_email(to_email: str, exam_link: str, username: str, password: str):
    """Sending Email"""

    message = f"""
    Hello,

    Your exam link is: {exam_link}
    Username: {username}
    Password: {password}

    Good luck!
    """
    msg = MIMEText(message)
    msg["Subject"] = "Your Exam Invitation"
    msg["From"] = "admin@smarthire.com"
    msg["To"] = to_email

    with smtplib.SMTP("localhost", port=25) as server:
        server.send_message(msg)
