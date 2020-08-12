from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self , request, view_func, view_args, view_kwargs):
        modul = view_func.__module__
        user = request.user
        if user.is_authenticated:
            if user.user_type == "1" :
                if modul == "student.HodViews" or modul =="django.views.static":
                    pass
                elif modul == "student.views" or modul =="django.views.static":
                    pass
                else :
                    return HttpResponseRedirect(reverse("admin_home"))

            elif user.user_type == "2" :
                if modul == "student.StaffViews" or modul =="django.views.static":
                    pass
                elif modul == "student.views" or modul =="django.views.static":
                    pass
                else :
                    return HttpResponseRedirect(reverse("staff_home"))

            elif user.user_type == "3" :
                if modul == "student.StudentViews" or modul =="django.views.static":
                    pass
                elif modul == "student.views" or modul =="django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("student_home"))
            else:
                return HttpResponseRedirect(reverse("show_login"))

        else:
            if request.path == reverse("show_login") or request.path == reverse("do_login") or modul == "django.contrib.auth.views" :
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))