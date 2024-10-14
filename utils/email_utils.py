"""Email Utility"""

import smtplib
from datetime import date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_exam_email(candidate_details):
    """Sending Email"""

    message = f"""
    Hello {candidate_details.name},<br/><br/>

    You have been shortlisted for the next round of recruitment with us.<br/>
    As part of preliminary round, you need to attend the following exam.<br/><br/>

    <strong>Note:</strong> This link is valid for just <strong>2 days</strong> and will expire on <strong>{date.today() + timedelta(days=2)} 23:59:59</strong><br/><br/>

    We have generated credentils. Please enter these when you are attending.<br/><br/>

    Please find the exam link, credentials abd duration below.<br/><br/>

    <strong>Exam Link:</strong> <a href={candidate_details.exam_link} target='_blank'>SmartHire</a><br/>

    <strong>Username:</strong> {candidate_details.username}<br/>
    <strong>Password:</strong> {candidate_details.password}<br/>
    <strong>Duration:</strong> 60 minutes<br/>
    <strong>Job Title:</strong> {candidate_details.job_title} <br/><br/>

    Wishing you Good luck!<br/><br/><br/><br/>

    Regards,<br/>
    SmartHire HR Team
    """
    mail_message = MIMEMultipart("alternative")
    mail_message["Subject"] = "Your Exam Invitation"
    mail_message["From"] = "admin@smarthire.com"
    mail_message["To"] = candidate_details.email

    content_body = MIMEText(message, "html")
    mail_message.attach(content_body)

    with smtplib.SMTP("localhost", port=25) as server:
        server.send_message(mail_message)
