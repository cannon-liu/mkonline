# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u'昵称', default='')
    birthday = models.DateField(verbose_name=u'生日', null=True, blank=True)
    gender = models.CharField(choices=(('male', u'男'), ('female', u'女')), default='male', max_length=6, verbose_name=u'性别')
    address = models.CharField(max_length=100, verbose_name=u'地址', null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name=u"电话")
    image = models.ImageField(upload_to="user/%Y/%m", default='static/image/default.png', max_length=100, verbose_name='头像')

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name
        db_table = 'user'

    def __str__(self):
        return self.username

    def unread_nums(self):
        num = 0
        from apps.operation.models import UserMessage
        messages = UserMessage.objects.filter(user=self.id)
        for message in messages:
            if message.has_read == False:
                num = num + 1
        return num



class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name=u'验证码')
    email = models.CharField(max_length=20,verbose_name=u'邮箱')
    send_type = models.CharField(choices=(('register', u'注册'), ('forget', u'忘记密码'), ('reset', u'密码重置')), max_length=15)
    send_time = models.DateField(default=datetime.now)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name
        db_table = 'EmailVerifyRecord'

    # def __unicode__(self):
    #     return '{0}({1})'.format(self.code, self.email)
    #
    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'标题')
    image = models.ImageField(upload_to='banner/%Y/%m', verbose_name=u'轮播图片',max_length=100)
    url = models.URLField(max_length=200, verbose_name=u'访问地址')
    index = models.IntegerField(default=100, verbose_name=u'顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name
        db_table = 'banner'


    def __str__(self):
        return self.title
