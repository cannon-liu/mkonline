# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from django.contrib.auth.models import AbstractUser
from DjangoUeditor.models import UEditorField


from apps.organization.models import CourseOrg,Teacher



# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=50,verbose_name= u'课程名')
    desc = models.CharField(max_length=300,verbose_name= u'课程详情')
    detail = UEditorField(verbose_name= u'课程详情', width=600, height=300,imagePath="courses/ueditor/", filePath="courses/ueditor/",default='')
    degree = models.CharField(choices=(('easy', '简单'), ('normal', '一般'), ('hard','困难')),verbose_name=u'课程难度',max_length=15)
    learn_time = models.FloatField(default=0,verbose_name=u'学习时长')
    students = models.IntegerField(default=0,verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to="course/%Y/%m", max_length=100, verbose_name='课程图片')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击人数')
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name=u"课程机构", null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name=u"课程教师", null=True, blank=True)
    category = models.CharField(max_length=50, verbose_name=u'课程类别', null=True, blank=True)
    tag = models.CharField(max_length=30, verbose_name=u'课程标签', null=True, blank=True)
    notice = models.CharField(max_length=100, verbose_name=u'课程公告', null=True, blank=True)
    is_banner = models.BooleanField(verbose_name=u'是否轮播', default=False)
    index = models.IntegerField(default=100, verbose_name=u'轮播顺序')
    need_know = models.CharField(max_length=200, verbose_name=u'课程须知', null=True, blank=True)
    teacher_tell = models.CharField(max_length=200, verbose_name=u'教师讲解', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')




    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name
        db_table = 'course'

class BannerCourse(Course):
    class Meta:
        verbose_name = "轮播课程"
        verbose_name_plural = verbose_name
        proxy = True


    def __str__(self):
        return self.name


class Chapter(models.Model):
    course = models.ForeignKey(Course,  on_delete=models.CASCADE, verbose_name=u'课程')
    name = models.CharField(max_length=50, verbose_name=u'章节名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name
        db_table = 'chapter'

    def __str__(self):
        return self.name


class Video(models.Model):
    chapter = models.ForeignKey(Chapter,  on_delete=models.CASCADE, verbose_name=u'章节')
    name = models.CharField(max_length=50, verbose_name=u'视频名称')
    has_learned = models.BooleanField(default=False, verbose_name=u'是否学习')
    url = models.CharField(max_length=200, default="", verbose_name=u"访问地址")
    play_time = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name
        db_table = 'video'

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程')
    name = models.CharField(max_length=50, verbose_name=u'资料名称')
    download = models.FileField(upload_to="resource/%Y/%m", max_length=100, verbose_name='课程资源')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'资源'
        verbose_name_plural = verbose_name
        db_table = 'resource'

    def __str__(self):
        return self.name
