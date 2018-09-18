# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from apps.user.models import UserProfile
from apps.course.models import Course
from apps.organization.models import Teacher
from apps.organization.models import CourseOrg

# Create your models here.


class UserAsk(models.Model):
    name = models.CharField(max_length=50, verbose_name= u'用户名称')
    mobile = models.CharField(max_length=11, verbose_name= u'手机号码')
    course_name = models.CharField(max_length=50, verbose_name= u'课程名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户咨询'
        verbose_name_plural = verbose_name
        db_table = 'user_ask'


    def __str__(self):
        return '{0} {1}'.format(self.name,'用户咨询')


class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name=u'用户')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程')
    comments = models.TextField(verbose_name=u'课程评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程评论'
        verbose_name_plural = verbose_name
        db_table = 'course_comment'

    def __str__(self):
        return '{0} {1}'.format(self.course.name, '课程评论')


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name=u'用户')
    # course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程')
    # teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE, verbose_name=u'教师')
    # org = models.ForeignKey(CourseOrg,on_delete=models.CASCADE, verbose_name=u'机构')
    fav_id = models.IntegerField(default=0, verbose_name=u'数据id')
    fav_type = models.IntegerField(choices=((1, '课程'), (2, '教师'), (3, '机构')), default=1, verbose_name=u'收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name
        db_table = 'user_fav'

    def __str__(self):
        return '{0} {1}'.format(self.user.username, '用户收藏')


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u'接受用户id')
    message = models.CharField(max_length=11, verbose_name=u'用户信息')
    has_read = models.BooleanField(default=False, verbose_name=u'是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name
        db_table = 'user_message'

    def __str__(self):
        from apps.user.models import UserProfile
        userprofile = UserProfile.objects.get(id=self.user)
        return '{0} {1}'.format(userprofile.username, '用户消息')




class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name=u'用户')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户课程'
        verbose_name_plural = verbose_name
        db_table = 'user_course'

    def __str__(self):
        return '{0} {1}'.format(self.user.username, self.course.name)
