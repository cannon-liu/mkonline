# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'城市名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    desc = models.CharField(max_length=150, verbose_name=u'城市描述')

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name
        db_table = 'city'

    def __str__(self):
        return  self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    desc = models.CharField(max_length=150, verbose_name=u'机构描述')
    category = models.CharField(choices=(("company", u"培训机构"),("person", u"个人"),("university", u"高校")),
                                default='universiy',max_length=20,verbose_name=u'机构类别')
    click_num = models.IntegerField(default=0, verbose_name=u'点击人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to="organization/%Y/%m", max_length=100, verbose_name='机构图片')
    address = models.CharField(max_length=150, verbose_name=u'机构地址')
    city = models.ForeignKey(CityDict, verbose_name= u'城市', on_delete=models.CASCADE)
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    course_num = models.IntegerField(default=0, verbose_name=u'课程数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'机构'
        verbose_name_plural = verbose_name
        db_table = 'organization'
    def __str__(self):
        return  self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg,verbose_name= u'机构',on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name=u'教师名称')
    age = fav_nums = models.IntegerField(verbose_name=u'收藏人数', null=True, blank=True)
    work_years = models.IntegerField(default=0, verbose_name=u'工作年限')
    work_company = models.CharField(max_length=50, verbose_name=u'工作单位')
    work_position = models.CharField(max_length=50, verbose_name=u'工作职称')
    points = models.CharField(max_length=50, verbose_name=u'教师特点')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to="teacher/%Y/%m", max_length=100, verbose_name='教师图片')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name
        db_table = 'teacher'

    def __str__(self):
        return  self.name





