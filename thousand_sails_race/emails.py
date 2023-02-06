
from flask import current_app
from thousand_sails_race.extends import mail
from flask_mail import Message
from threading import Thread
import random


def _send_async_mail(_app, _message):
    with _app.app_context():
        mail.send(message=_message)


def send_async_mail(subject, to, body):
    message = Message(subject=subject, recipients=[to], html=body)
    _app = current_app._get_current_object()
    thr = Thread(target=_send_async_mail, args=[_app, message])
    thr.start()
    return thr


def send_captcha(receptions):
    _captcha = ''.join(str(random.randint(0, 9)) for _ in range(4))
    send_async_mail(subject='千帆竞发邮箱验证码', to=receptions, body='<p>千帆竞发邮箱验证码为</p>' + '<h1>' + _captcha + '</h1>')
    return _captcha
