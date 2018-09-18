# -*- coding = utf-8 -*-
__author__ = 'cannon'
__date__ = '2018/6/20 18:57'

from django import  forms
import re

from apps.operation.models import UserAsk


# class UserAskFrom(forms.Form):
#     name = forms.CharField(required=True, min_length=2, max_length=50)
#     mobile = forms.CharField(required=True, min_length=11, max_length=11)
#     course_name = forms.CharField(required=True, min_length=5, max_length=50)


#ModelForm可以继承，也可以新增
class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

        # def clean_mobile(self):
        #     mobile = self.cleaned_data['mobile']
        #     REGEX_MOBILE = "^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\\d{8}$"
        #     p = re.compile(REGEX_MOBILE)
        #     if p.match(mobile):
        #         return mobile
        #     else:
        #         raise forms.ValidationError(U"手机号码非法",code='mobile_invalid')

    # 手机号的正则表达式验证
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")

