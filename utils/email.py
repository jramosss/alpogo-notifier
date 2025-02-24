import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from models.Event import Event
from utils.utils import generate_html_for_events

TEST_EMAIL = os.getenv("TEST_EMAIL")
RECIPIENTS = [TEST_EMAIL]

if not os.getenv("SMTP_SERVER") or not os.getenv("SMTP_PORT"):
    raise Exception("SMTP_SERVER and SMTP_PORT are required")

smtp_server = os.getenv("SMTP_SERVER")
smtp_port = os.getenv("SMTP_PORT")


class EmailUtils:
    def send_email(self, to: list[str], events: list[Event]):
        print("Hi im send email", to, events)
        msg = MIMEMultipart()
        msg["Subject"] = "Eventos de musica a ciegas este mes"
        me = TEST_EMAIL
        msg["From"] = me
        msg["To"] = ", ".join(to)
        msg["Content-Type"] = "text/html"
        html = generate_html_for_events(events)
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.sendmail(me, to, msg.as_string())
            server.quit()
