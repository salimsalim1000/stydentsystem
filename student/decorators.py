from django.http import HttpResponse
from django.shortcuts import redirect

def unauthen_user(view_func):
    def wrapper_func(request , *args , **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request , *args , **kwargs)
    return wrapper_func


def allowed_user(allow_role=[]):
    def decor (view_func):
        def wrapper_func(request , *args , **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allow_role:
                 return view_func(request , *args , **kwargs)
            else:
                return HttpResponse("u cant be here")
        return wrapper_func
    return decor

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'admin':
            return view_func(request, *args, **kwargs)
        if group == 'customers':
            return redirect('profile')

    return wrapper_func

