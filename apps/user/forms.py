# -*- coding = utf-8 -*-
__author__ = 'cannon'
__date__ = '2018/6/19 10:03'

from django import forms
from captcha.fields import CaptchaField


from .models import UserProfile


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    # username = forms.CharField(required=True,min_length=5, max_length=20)
    password = forms.CharField(required=True, min_length=5, max_length=20)
    captcha = CaptchaField()


class LoginForm(forms.Form):
    username = forms.CharField(required=True,min_length=5, max_length=20)
    password = forms.CharField(required=True, min_length=5, max_length=20)


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    # username = forms.CharField(required=True,min_length=5, max_length=20)
    # password = forms.CharField(required=True, min_length=5, max_length=20)
    captcha = CaptchaField()


class ResetForm(forms.Form):
    # email = forms.EmailField(required=False)
    password1 = forms.CharField(required=True, min_length=5, max_length=20)
    password2 = forms.CharField(required=True, min_length=5, max_length=20)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']



# 用于个人中心修改个人信息
class UserInfoForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address', 'mobile']