from flask_mail import Message
from flask import render_template
from app import application, mail


def send_mail(email_ids, sub, message_text, html_file=None, html_payload=None):
    if html_file:
        html_message = render_template(html_file, **html_payload)
        msg = Message(subject=sub,
                      body=message_text,
                      html=html_message,
                      sender=application.config['MAIL_DEFAULT_SENDER'],
                      recipients=email_ids)
    else:
        msg = Message(subject=sub,
                      body=message_text,
                      sender=application.config['MAIL_DEFAULT_SENDER'],
                      recipients=email_ids)
    mail.send(msg)

