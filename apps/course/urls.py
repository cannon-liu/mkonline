# -*- coding = utf-8 -*-
__author__ = 'cannon'
__date__ = '2018/6/21 20:15'

from django.urls import path, include,re_path
from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentView, CoursePlayView
from apps.organization.views import AddFavView


app_name = 'course'

urlpatterns = [
    path(r'list/', CourseListView.as_view(), name='course_list'),
    path(r'detail/<course_id>', CourseDetailView.as_view(), name='course_detail'),
    path(r'add_fav/', AddFavView.as_view(), name='add_fav'),
    path(r'info/<course_id>', CourseInfoView.as_view(), name='course_info'),
    path(r'comment/<course_id>', CourseCommentView.as_view(), name='course_comment'),
    path(r'add_comment/', AddCommentView.as_view(), name='add_comment'),
    path(r'video/<video_id>', CoursePlayView.as_view(), name='course_play'),


]

