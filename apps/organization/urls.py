# -*- coding = utf-8 -*-
__author__ = 'cannon'
__date__ = '2018/6/20 19:13'


from django.urls import path, include,re_path
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf.urls.static import static

from .views import OrgView, UserAskView,  OrgHomeView, OrgCourseView, \
    OrgDescView, OrgTeacherView, AddFavView, TeahcerListView, TeahcerDetailView

from mkonline.settings import MEDIA_ROOT,MEDIA_URL

app_name = 'org'
urlpatterns = [
    # 课程机构首页
    path(r'list/', OrgView.as_view(), name='org_list'),
    path(r'ask/', UserAskView.as_view(), name='org_ask'),
    path(r'home/<org_id>', OrgHomeView.as_view(), name='org_home'),
    path(r'course/<org_id>', OrgCourseView.as_view(), name='org_course'),
    path(r'desc/<org_id>', OrgDescView.as_view(), name='org_desc'),
    path(r'org_teacher/<org_id>', OrgTeacherView.as_view(), name='org_teacher'),

    path(r'add_fav/', AddFavView.as_view(), name='add_fav'),
    path(r'teacher/list/', TeahcerListView.as_view(), name='teacher_list'),
    path(r'teacher/detail/<teacher_id>', TeahcerDetailView.as_view(), name='teacher_detail'),


]

