"""mkonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# -*- coding = utf-8 -*-
from django.contrib import admin
from django.urls import path, include,re_path
from django.views.generic import TemplateView
from django.views.static import serve

from extra_apps import xadmin
from apps.user.views import user_login
from apps.user.views import LoginView, RegisterView, ActiveView, ForgetView, ResetView, ModifyView, LogoutView, IndexView
from apps.organization.views import OrgView
from mkonline.settings import MEDIA_ROOT, STATIC_ROOT
from django.conf.urls import handler404,handler400,handler403,handler500

urlpatterns = [
    # path('admin/', admin.site.urls),
    path(r'xadmin/', xadmin.site.urls),
    #不使用自定义的View
    # path(r'', TemplateView.as_view(template_name='index.html'), name='index'),
    #使用自定义的View
    path('', IndexView.as_view(), name="index"),
    # path(r'login/', TemplateView.as_view(template_name='login.html'), name='login'),
    # path(r'login/', user_login, name='login'),
    #登录
    path(r'login/', LoginView.as_view(), name='login'),
    #登出
    path(r'logout/', LogoutView.as_view(), name='logout'),

    path(r'register/', RegisterView.as_view(), name='register'),
    path(r'captcha/', include('captcha.urls')),
    path(r'active/<active_code>/', ActiveView.as_view(), name='user_active'),
    path(r'reset/<active_code>/', ResetView.as_view(), name='user_reset'),
    path(r'modify_pwd/', ModifyView.as_view(), name='user_modify'),
    path(r'forget/', ForgetView.as_view(), name='forget'),
    # path(r'active/', ActiveView.as_view(), name='user_active')

    #读取上传图片
    # path(r'media/<path>', serve, {"document_root": MEDIA_ROOT}),
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),

    # path('static/<path>', serve, {'document_root': STATIC_ROOT}),
    path('static/<path:path>', serve, {'document_root': STATIC_ROOT}),

    #课程机构配置
    path(r'org/', include(('apps.organization.urls', 'org'), namespace='org')),

    #课程配置
    path(r'course/', include(('apps.course.urls', 'course'), namespace='course')),

    #用户配置
    path(r'user/', include(('apps.user.urls', 'user'), namespace='user')),

    #ueditior第三方插件url
    path(r'ueditor/',  include('DjangoUeditor.urls')),

]

handler404 = 'apps.user.views.page_not_found'
handler500 = 'apps.user.views.page_error'
