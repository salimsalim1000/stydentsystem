import datetime
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.http import HttpResponse , HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
# Create your views here.
from student.EmailBackEnd import EmailBackEnd
from django.contrib.auth.decorators import user_passes_test, login_required


def showDemoPage(request):
    return render(request,template_name="demo.html")


def ShowLoginPage(request):
    user = request.user
    if request.user.is_authenticated:
        if user.user_type == "1":
            return redirect('admin_home')
        else:
            return redirect('mostachar_home')
    else:
        return render(request,template_name='login_page.html')


def doLogin(request):
    if request.method != "POST" :
        return HttpResponse("<h2> not allow to be here </h2>")
    else:
        user = EmailBackEnd.authenticate(request , username=request.POST.get("email") , password=request.POST.get("password"))
        if user != None:
            login(request,user)
            if user.user_type =="1" :
                return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("mostachar_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request,"خطأ في البريد الالكتروني او كلمة المرور")
            return HttpResponseRedirect(reverse("show_login"))


def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("user : " + request.user.email + "usertype" + request.user.user_type)
    else:
        return HttpResponse("pls login first")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")