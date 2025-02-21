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

smtp_server = '0.0.0.0'
smtp_port = 1025

def send_email(to: list[str], events: list[Event]):
    msg = MIMEMultipart()
    msg['Subject'] = 'Eventos de musica a ciegas este mes'
    me = TEST_EMAIL
    msg['From'] = me
    msg['To'] = ', '.join(to)
    msg['Content-Type'] = 'text/html'
    html = generate_html_for_events(events)
    msg.attach(MIMEText(html, 'html'))
    with open('mocks/generated.html', 'w') as file:
        file.write(html)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.sendmail(me, to, msg.as_string())
        server.quit()
