# -*- coding = utf-8 -*-

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q

from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger



from .models import CourseOrg, CityDict, Teacher
from mkonline.settings import PAGE_COUNTS
from .forms import UserAskForm
from apps.operation.models import UserFavorite
from apps.course.models import Course
# Create your views here.


class OrgView(View):
    def get(self, request):


        #取出所有课程机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_num")


        #搜索课程关键词
        keywords  = request.GET.get("keywords", "")
        if keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=keywords)|Q(desc__icontains=keywords)|Q(address__icontains=keywords))

        #取出所有城市
        all_citys = CityDict.objects.all()

        #筛选城市
        city_id = request.GET.get("city", "")
        if city_id:
            all_orgs = all_orgs.filter(city=int(city_id))


        #筛选类别
        category_edu = request.GET.get("category", "")
        if category_edu:
            all_orgs = all_orgs.filter(category=category_edu)


        #机构排序
        sort_type = request.GET.get("sort", "")
        if sort_type == 'students':
            all_orgs =  all_orgs.order_by("-students")

        elif sort_type == 'courses':
            all_orgs =  all_orgs.order_by("-course_num")


        org_nums = all_orgs.count()
        #对课程进行分页
        each = PAGE_COUNTS
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, each, request=request)
        orgs = p.page(page)


        return render(request, 'org-list.html', {
            "all_citys": all_citys,
            "all_orgs": orgs,
            "org_nums": org_nums,
            "city_id": city_id,
            "category_edu": category_edu,
            "hot_orgs": hot_orgs
        })


class UserAskView(View):
    # def post(self,request):
    #     userask_form = UserAskForm(request.POST)
    #     if userask_form.is_valid():
    #         user_ask = userask_form.save(commit=True)
    #         return HttpResponse("{'status':'success'}", content_type="application/json")
    #     else:
    #         return HttpResponse("{'status':'fail','msg':'添加出错'}", content_type="application/json")
    """
     用户添加咨询
     """

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"您的字段有错误,请检查"}', content_type='application/json')



class OrgHomeView(View):
    def get(self, request, org_id):
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=3):
                has_fav = True
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_num += 1
        course_org.save()
        # org = CourseOrg.objects.filter(id=int(org_id))
        all_courses = course_org.course_set.all()[:4]
        all_teachers = course_org.teacher_set.all()[:1]

        return render(request, 'org-detail-homepage.html', {
            'org': course_org,
            'all_courses': all_courses,
            'all_teacher': all_teachers,
            'has_fav': has_fav,
        })


class OrgCourseView(View):
    def get(self, request, org_id):
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=3):
                has_fav = True
        course_org = CourseOrg.objects.get(id=int(org_id))
        # org = CourseOrg.objects.filter(id=int(org_id))
        all_courses = course_org.course_set.all()
        all_teachers = course_org.teacher_set.all()[:1]

        return render(request, 'org-detail-course.html', {
            'org': course_org,
            'all_courses': all_courses,
            'all_teacher': all_teachers,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    def get(self, request, org_id):
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=3):
                has_fav = True
        course_org = CourseOrg.objects.get(id=int(org_id))
        # org = CourseOrg.objects.filter(id=int(org_id))
        all_courses = course_org.course_set.all()
        all_teachers = course_org.teacher_set.all()[:1]

        return render(request, 'org-detail-desc.html', {
            'org': course_org,
            'all_courses': all_courses,
            'all_teacher': all_teachers,
            'has_fav': has_fav,
        })

class OrgTeacherView(View):
    def get(self, request, org_id):
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=3):
                has_fav = True
        course_org = CourseOrg.objects.get(id=int(org_id))
        # org = CourseOrg.objects.filter(id=int(org_id))
        all_courses = course_org.course_set.all()
        all_teachers = course_org.teacher_set.all()

        return render(request, 'org-detail-teachers.html', {
            'org': course_org,
            'all_courses': all_courses,
            'all_teacher': all_teachers,
            'has_fav': has_fav,
        })


class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', '0')
        fav_type = request.POST.get('fav_type', '0')
        if not request.user.is_authenticated:
            #判断用户登陆状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type="application/json")
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))

        if exist_records:
            #存在的情况下，表示用户取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            elif int(fav_type) == 3:
                org = CourseOrg.objects.get(id=int(fav_id))
                org.fav_nums -= 1
                if org.fav_nums < 0:
                    org.fav_nums = 0
                org.save()

            return HttpResponse('{"status":"success", "msg":"取消收藏"}', content_type="application/json")
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                elif int(fav_type) == 3:
                    org = CourseOrg.objects.get(id=int(fav_id))
                    org.fav_nums +=1
                    org.save()

                return HttpResponse('{"status":"success", "msg":"收藏成功"}', content_type="application/json")

            else:
                return HttpResponse('{"status":"fail", "msg":"收藏失败"}', content_type="application/json")


class TeahcerListView(View):
    def get(self, request):

        sort = request.GET.get("sort", "")
        all_teachers = Teacher.objects.all()
        hot_teachers = all_teachers.order_by("-click_nums")[:3]


        #搜索教师关键词
        keywords  = request.GET.get("keywords", "")
        if keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=keywords)|Q(work_company__icontains=keywords)|Q(work_position__icontains=keywords))

        if sort == 'hot':
            all_teachers = all_teachers.order_by("-click_nums")


        #对教师进行分页
        each = 2
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, each, request=request)
        sort_teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'all_teachers': sort_teachers,
            'hot_teachers': hot_teachers,

        })


class TeahcerDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        courses = Course.objects.filter(teacher_id=int(teacher_id))
        all_teachers = Teacher.objects.all()
        hot_teachers = all_teachers.order_by("-click_nums")[:3]

        has_fav_teacher = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(teacher.id), fav_type=2):
                has_fav_teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_id=int(teacher.org.id), fav_type=3):
                has_fav_org = True




        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'courses': courses,
            'hot_teachers': hot_teachers,
            'has_fav_org': has_fav_org,
            'has_fav_teacher': has_fav_teacher,
        })
