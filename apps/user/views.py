# -*- coding = utf-8 -*-
import json
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse,HttpResponseRedirect
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import UserProfile,EmailVerifyRecord,Banner
from .forms import LoginForm, RegisterForm, ForgetForm, ResetForm
from apps.utils.email_send import send_mkonlie_email
# Create your views here.
from apps.utils.mixin_utils import LoginRequiredMixin
from .forms import UploadImageForm, UserInfoForm
from apps.utils.email_send import send_mkonlie_email
from .models import EmailVerifyRecord
from apps.operation.models import UserCourse, UserFavorite,  UserMessage
from apps.course.models import Course
from apps.organization.models import CourseOrg,Teacher



class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=email_name):
                return render(request, "register.html", {"register_form": register_form, "message": "用户已经存在"})
            pass_word = request.POST.get("password", "")
            # captcha_code = request.POST.get("captcha","")
            user_profile = UserProfile()
            user_profile.username = email_name
            user_profile.email = email_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_mkonlie_email(email_name, send_type="register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class ActiveView(View):
    def get(self, request, active_code = 0):
        all_records =  EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return render(request, "login.html", {})
        else:
            return render(request, "active_fail.html", {"message": "激活有误"})


class ResetView(View):
    def get(self, request, active_code = 0):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                if user:
                    return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "reset_fail.html", {"message": "重置失败"})


class ModifyView(View):
    def post(self, request):
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            email_address = request.POST.get("email", "")
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            reset_user = UserProfile.objects.get(email=email_address)
            if pwd1 != pwd2:
                return render(request, 'password_reset.html',{"message":"密码不一致"})
            else:
                if reset_user:
                    reset_user.password = make_password(pwd1)
                    reset_user.save()
                    return render(request, 'login.html')
        else:
            return render(request, 'password_reset.html', {"message": "输入有误"})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "请激活账户! "})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误! "})
        else:
            return render(request, "login.html", {"login_form": login_form})


class ForgetView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=email_name):
                send_mkonlie_email(email_name, send_type="forget")
                return render(request, 'send_success.html', {})
            else:
                return render(request, 'forgetpwd.html', {"forget_form": forget_form, "message": "用户不存在"})
        else:
            return render(request, 'forgetpwd.html', {"forget_form": forget_form, "message": "输入有误"})






def user_login(request):
    # 前端向后端发送的请求方式: get 或post

    # 登录提交表单为post
    if request.method == "POST":
        # 取不到时为空，username，password为前端页面name值
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")

        # 成功返回user对象,失败返回null
        user = authenticate(username=user_name, password=pass_word)

        # 如果不是null说明验证成功
        if user is not None:
            login(request, user)
            # 跳转到首页 user request会被带回到首页
            return render(request, "index.html")
        # 没有成功说明里面的值是None，并再次跳转回主页面
        else:
            return render(request, "login.html", {"msg": "用户名或密码错误! "})

    # 获取登录页面为get
    elif request.method == "GET":
        # render就是渲染html返回用户
        # render三变量: request 模板名称 一个字典写明传给前端的值
        return render(request, "login.html", {})


class UserInfo(LoginRequiredMixin,View):
    def get(self, request):
        return  render(request, 'usercenter-info.html', {})


class UploadUserImage(LoginRequiredMixin,View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail"}', content_type="application/json")


class UsercenterModifyPwdView(LoginRequiredMixin, View):
    def post(self, request):
        usercenter_modify_form = ResetForm(request.POST)
        if usercenter_modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","message": "密码不一致"}', content_type="application/json")
            else:
               request.user.password = make_password(pwd1)
               request.user.save()
               return HttpResponse('{"status":"success","message": "密码修改成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail","message": json.dumps(usercenter_modify_form)}', content_type="application/json")


class SendEmail_CodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get("email", "")
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"status":"fail","message": "邮箱已存在"}', content_type="application/json")
        else:
            send_mkonlie_email(email, send_type="reset")






class Update_EmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")
        if EmailVerifyRecord.objects.filter(email=email,code=code,send_type='reset'):
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail"}', content_type="application/json")


class Update_PersonalInfoView(LoginRequiredMixin, View):
    def post(self, request):
        userinfo_form = UserInfoForm(request.POST,instance=request.user)
        if userinfo_form.is_valid():
            # nick_name = request.POST.get("nick_name", "")
            # birth_day = request.POST.get("birday", "")
            # address = request.POST.get("address", "")
            # gender
            # user = request.user
            # user.nick_name = nick_name
            # user.birthday = birth_day
            # user.address = address
            # user.save()
            userinfo_form.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse(json.dumps(userinfo_form.errors), content_type="application/json")



class UserMyCourse(LoginRequiredMixin,View):
    def get(self, request):
        all_courses = UserCourse.objects.filter(user=request.user)
        return  render(request, 'usercenter-mycourse.html', {
            'all_courses':all_courses
        })


class UserFavCourse(LoginRequiredMixin, View):
    def get(self, request):
        userfav_courses = UserFavorite.objects.filter(fav_type=1, user=request.user)
        fav_ids = [userfav_course.fav_id for userfav_course in userfav_courses]
        all_course = Course.objects.filter(id__in=fav_ids)
        return render(request,'usercenter-fav-course.html', {
            'fav_courses': all_course
        })


class UserFavOrg(LoginRequiredMixin, View):
    def get(self,request):
        userfav_orgs = UserFavorite.objects.filter(fav_type=3, user=request.user)
        fav_ids = [userfav_org.fav_id for userfav_org in userfav_orgs]
        all_orgs = CourseOrg.objects.filter(id__in=fav_ids)
        return render(request, 'usercenter-fav-org.html', {
            "fav_orgs": all_orgs
        })


class UserFavTeacher(LoginRequiredMixin,View):
    def get(self, request):
        userfav_teachers = UserFavorite.objects.filter(fav_type=2, user=request.user)
        fav_ids = [userfav_teacher.fav_id for userfav_teacher in userfav_teachers]
        all_teachers = Teacher.objects.filter(id__in=fav_ids)

        return render(request, 'usercenter-fav-teacher.html', {
            'fav_teachers': all_teachers
        })


class UserMessageView(LoginRequiredMixin, View):
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)

        #对教师进行分页
        each = 2
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, each, request=request)
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'user_messages': messages
        })


class IndexView(View):
    def get(self, request):
        all_banner = Banner.objects.all()
        banner_courses = Course.objects.filter(is_banner=True).order_by("index")
        normal_courses = Course.objects.filter(is_banner=False)[:6]
        orgs = CourseOrg.objects.all()[:15]

        return render(request, 'index.html', {
            "all_banner": all_banner,
            "banner_courses": banner_courses,
            "normal_courses": normal_courses,
            "orgs": orgs,

        })


#全局404 错误处理函数
def page_not_found(request):
    from  django.shortcuts import render_to_response
    # response = render_to_response('404.html', {})
    return render(request, '404.html', {})
    response.status_code = 404
    return response

#全局500 错误处理函数
def page_error(request):
    from  django.shortcuts import render_to_response
    # response = render_to_response('500.html', {})
    return render(request, '500.html', {})
    response.status_code = 500
    return response


