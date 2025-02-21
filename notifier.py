import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from models.Event import Event
from utils.utils import generate_html_for_events
from dotenv import load_dotenv

load_dotenv('.env.development')

TEST_EMAIL = os.getenv('TEST_EMAIL')
RECIPIENTS = [
    TEST_EMAIL
]

if not os.getenv('SMTP_SERVER') or not os.getenv('SMTP_PORT'):
    raise Exception('SMTP_SERVER and SMTP_PORT are required')

smtp_server = os.getenv('SMTP_SERVER')
smtp_port = os.getenv('SMTP_PORT')

def send_email(to: list[str], events: list[Event]):
    msg = MIMEMultipart()
    msg['Subject'] = 'Eventos de musica a ciegas este mes'
    me = TEST_EMAIL
    msg['From'] = me
    msg['To'] = ', '.join(to)
    msg['Content-Type'] = 'text/html'
    html = generate_html_for_events(events)
    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.sendmail(me, to, msg.as_string())
        server.quit()
