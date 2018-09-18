# -*- coding = utf-8 -*-
__author__ = 'cannon'
__date__ = '2018/6/19 15:45'

from random import Random
from apps.user.models import EmailVerifyRecord
from django.core.mail import send_mail

from mkonline.settings import EMAIL_FROM


def generate_random_str(randomlength=8):
    code_str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    random = Random()
    length = len(chars)-1
    for i in range(randomlength):
        code_str += chars[random.randint(0, length)]
    return code_str


def send_mkonlie_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type == 'reset':
        email_record.code = generate_random_str(4)
    else:
        email_record.code = generate_random_str(16)
    email_record.send_type = send_type
    email_record.email = email
    email_record.save()

    if send_type == "register":
        active_url = 'http://127.0.0.1:8000/active/{0}'.format(email_record.code)
        email_title = '注册激活链接'
        email_body = '请点击下面链接激活账号：'+active_url

        send_status = send_mail(subject=email_title, message=email_body,
                                from_email=EMAIL_FROM, recipient_list=[email_record.email])
        if send_status == True:
            pass

    elif send_type == "forget":
        active_url = 'http://127.0.0.1:8000/reset/{0}'.format(email_record.code)
        email_title = '密码重置链接'
        email_body = '请点击下面链接激活账号：' + active_url
        send_status = send_mail(subject=email_title, message=email_body,
                                from_email=EMAIL_FROM, recipient_list=[email_record.email])
        if send_status == True:
            pass

    elif send_type == "reset":
        active_code = '{0}'.format(email_record.code)
        email_title = '用户中心密码重置链接'
        email_body = '邮箱验证码：' + active_code
        send_status = send_mail(subject=email_title, message=email_body,
                                from_email=EMAIL_FROM, recipient_list=[email_record.email])
        if send_status == True:
            pass

    

    else:
        pass








