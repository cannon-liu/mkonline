# -*- coding = utf-8 -*-
__author__ = 'cannon'
__date__ = '2018/6/18 10:37'

from extra_apps import xadmin
from .models import Course, Chapter, Video, CourseResource,BannerCourse


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'image', 'click_nums', 'is_banner','add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students','is_banner']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'image', 'click_nums','is_banner', 'add_time']
    model_icon = "fa fa-camera-retro"
    style_fields = {"detail": "ueditor"}
    import_excel = True

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def post(self, request, *args , **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)

class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'image', 'click_nums', 'is_banner','add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students','is_banner']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'image', 'click_nums','is_banner', 'add_time']
    model_icon = "fa fa-clipboard"

    def queryset(self):
        qs = super(BannerCourseAdmin,self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class ChapterAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']





class VideoAdmin(object):
    list_display = ['chapter', 'name', 'add_time']
    search_fields = ['chapter', 'name']
    list_filter = ['chapter__name', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download','add_time']
    search_fields = ['course', 'name''download']
    list_filter = ['course__name', 'name', 'download','add_time']





xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Chapter, ChapterAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
