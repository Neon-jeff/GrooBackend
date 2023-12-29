from django.conf import settings
import smtplib
from django.template.loader import render_to_string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from rest_framework.response import Response
import cloudinary.uploader

from xhtml2pdf import pisa

def render_to_pdf(context_dict={}):
    template = get_template('agreement.html')
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), result,encoding="UTF-8")
    if pdf.err:
        return Response({"error":"pdf operation failed"}, status_code=400)
    return result.getvalue()
    # return HttpResponse(result.getvalue(), content_type='application/pdf')




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

