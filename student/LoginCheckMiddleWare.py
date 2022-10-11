from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self , request, view_func, view_args, view_kwargs):
        modul = view_func.__module__
        print(modul)
        user = request.user
        print(user)
        if user.is_authenticated:
            if user.user_type == "1" :
                if modul == "student.HodViews" or modul =="django.views.static" or modul =="import_export.admin" or modul =="django.contrib.admin.options":
                    pass
                elif modul == "student.views" or modul =="django.contrib.admin.sites" or modul =="django.contrib.auth.views" or modul == "debug_toolbar.views":
                    pass
                else :
                    return HttpResponseRedirect(reverse("admin_home"))

            elif user.user_type == "2" :
                if modul == "student.StaffViews" or modul =="django.views.static":
                    pass
                elif modul == "student.views" or modul =="django.contrib.admin.sites" or modul =="django.contrib.auth.views" or modul == "debug_toolbar.views" :
                    pass
                else :
                    return HttpResponseRedirect(reverse("mostachar_home"))

            elif user.user_type == "3" :
                if modul == "student.StudentViews" or modul =="django.views.static":
                    pass
                elif modul == "student.views" or modul =="django.contrib.admin.sites" or modul =="django.contrib.auth.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("student_home"))
            else:
                return HttpResponseRedirect(reverse("show_login"))

        else:
            if request.path == reverse("show_login") or request.path == reverse("do_login") or modul == "django.contrib.auth.views" or modul =="django.contrib.admin.sites":
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))