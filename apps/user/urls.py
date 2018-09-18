# -*- coding = utf-8 -*-
__author__ = 'cannon'
__date__ = '2018/6/27 10:46'


from django.urls import path


from .views import UserInfo, UserMessageView, UserMyCourse, UserFavCourse, UserFavOrg, UserFavTeacher, UploadUserImage,\
    UsercenterModifyPwdView, SendEmail_CodeView, Update_EmailView, Update_PersonalInfoView

app_name = 'user'
urlpatterns = [
    # 个人中心首页
    path(r'info/', UserInfo.as_view(), name='user_info'),
    path(r'message/', UserMessageView.as_view(), name='user_message'),
    path(r'course/', UserMyCourse.as_view(), name='user_course'),
    path(r'fav/', UserFavCourse.as_view(), name='user_fav_course'),
    path(r'fav_course/', UserFavCourse.as_view(), name='user_fav_course'),
    path(r'fav_org/', UserFavOrg.as_view(), name='user_fav_org'),
    path(r'fav_teacher/', UserFavTeacher.as_view(), name='user_fav_teacher'),
    path(r'upload_image/', UploadUserImage.as_view(), name='user_upload_image'),
    path(r'center_modify_pwd/', UsercenterModifyPwdView.as_view(), name='user_modify_pwd'),
    #发送邮箱验证码
    path(r'sendemail_code/', SendEmail_CodeView.as_view(), name='user_sendemail_code'),
    #修改邮箱
    path(r'update_email/', Update_EmailView.as_view(), name='update_email'),
    # 修改个人信息
    path(r'update_info/', Update_PersonalInfoView.as_view(), name='update_info'),




]