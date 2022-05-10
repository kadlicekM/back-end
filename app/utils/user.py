import smtplib
import yaml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime as dt


def send_confirmation_mail(reciever_mail: str, is_activated: bool=False):
    with open('config/mail.yaml') as file:
        config = yaml.safe_load(file)
    port = config.get('port', 587)
    host = config.get('host', '')
    sender_email = config.get('sender', '')
    password = config.get('password', '')
    subject = config.get('subject', '')
    message = config.get('confirm' if is_activated else 'cancel', {}).get('message', '')
    
    today = dt.today().strftime('%Y-%m-%d_%H-30-00')
    mail = MIMEMultipart('mixed')
    mail['From'] = sender_email
    mail['To'] = reciever_mail
    mail['Date'] = today
    mail['Subject'] = subject
    mail.attach(MIMEText(message, 'html'))

    try:
        smtp = smtplib.SMTP(host, port)
        # smtp.connect(host, port)
        smtp.starttls()
        smtp.login(sender_email, password)
        smtp.sendmail(sender_email, reciever_mail, mail.as_string())
        smtp.close()
        return True
    except Exception as e:
        print(e)
        return False