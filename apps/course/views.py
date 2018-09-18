from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q

from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course, Video
from apps.organization.views import AddFavView
from apps.operation.models import UserFavorite, CourseComments, UserCourse
from apps.utils.mixin_utils import LoginRequiredMixin

# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all()
        hot_courses = all_courses.order_by("-click_nums")[:3]

        #搜索课程关键词
        keywords  = request.GET.get("keywords", "")
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords)|Q(desc__icontains=keywords)|Q(detail__icontains=keywords))

        sort = request.GET.get("sort", "")
        if sort == "hot" :
            all_courses = all_courses.order_by("-click_nums")
        elif sort == "students":
            all_courses = all_courses.order_by("-students")



        #对课程进行分页
        each = 6
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, each, request=request)
        sort_courses = p.page(page)

        return render(request, 'course-list.html', {
            "all_courses": sort_courses,
            'all_hot_courses': hot_courses,
            "sort_type": sort,
        })


class CourseDetailView(View):
    def get(self, request, course_id):

        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        has_org_fav = False
        has_course_fav = False
        org_id = course.course_org.id
        cour_id = course.id
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_org_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_id=int(cour_id), fav_type=1):
                has_course_fav = True

        #tag存在问题，相关课程会重复到自身
        tag = course.tag
        if tag:
            related_courses = Course.objects.filter(tag=tag)[1:2]
            if not related_courses:
                related_courses = []
        else:
            related_courses = []

        return render(request, 'course-detail.html', {
            "course": course,
            'related_courses': related_courses,
            'has_course_fav': has_course_fav,
            'has_org_fav': has_org_fav,
        })


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request,course_id):
        course = Course.objects.get(id=int(course_id))
        #先通过课程id取出所有的user_coursr
        user_courses = UserCourse.objects.filter(course_id=course.id)
        #通过每个user_coursr取出共上一门课的用户
        user_ids = [user_course.user_id for user_course in user_courses]
        #通过所有用户id得到关联的user_course，继而得到课程id，获取所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course_id for user_course in all_user_courses]
        #依然存在会本身重复的问题，待解决
        relatd_coourses = Course.objects.filter(id__in = course_ids).order_by("click_nums")[1:4]



        return render(request, 'course-video.html', {
            "course": course,
            "related_courses": relatd_coourses,
        })


class CourseCommentView(LoginRequiredMixin, View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        return render(request, 'course-comment.html', {
            "course": course,

        })


class AddCommentView(View):
    def post(self, request):
        course_id = request.POST.get('course_id', '0')
        comments = request.POST.get('comments', '')
        if not request.user.is_authenticated:
            #判断用户登陆状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type="application/json")
        else:
            user_comment = CourseComments()
            #需要解决的是评论时间先后的问题
            if int(course_id) > 0:
                user_comment.user = request.user
                user_comment.comments = comments
                user_comment.course = Course.objects.get(id=int(course_id))
                user_comment.save()
                return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type="application/json")

            else:
                return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type="application/json")


class CoursePlayView(LoginRequiredMixin, View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.chapter.course

        return render(request, 'course_play.html', {
            "course": course,
            'video': video,

        })
