from django.conf import settings
import smtplib
from django.template.loader import render_to_string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings



sender=settings.EMAIL_USER
auth=settings.EMAIL_AUTH

def SendEmail(user):
    recipient = f'{user.email}'
# Create message
    msg = MIMEMultipart("alternative")
    email_template=render_to_string('transactional.html',{'user':user})
    # text="Hi, welcome to nello"
    msg['Subject'] = f"Welcome STEMs"
    msg['From'] = sender
    msg['To'] = recipient
    part2 = MIMEText(email_template, 'html')
    msg.attach(part2)
# Create server object with SSL option
    server = smtplib.SMTP_SSL("smtp.zoho.com", 465)

# Perform operations via server
    server.login(sender, auth)
    server.sendmail(sender, [recipient], msg.as_string())
    server.quit()
