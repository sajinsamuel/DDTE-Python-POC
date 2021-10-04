import os.path
import smtplib
import yaml
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)


def send_email(email_recipient,
               email_subject,
               email_message,
               attachment_location=''):
    email_sender = data["smtpUsername"]

    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_recipient
    msg['Subject'] = email_subject

    msg.attach(MIMEText(email_message, 'plain'))

    if attachment_location != '':
        filename = os.path.basename(attachment_location)
        attachment = open(attachment_location, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= %s" % filename)
        msg.attach(part)

    try:
        server = smtplib.SMTP(data["smtpServerUrl"], data["smtpServerPort"])
        server.ehlo()
        server.starttls()
        server.login(data["smtpUsername"], data["smtpPassword"])
        text = msg.as_string()
        server.sendmail(email_sender, email_recipient, text)
        print('email sent to destination successfully')
        server.quit()
    except:
        print("SMTP server connection error")
    return True
