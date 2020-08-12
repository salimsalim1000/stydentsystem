from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from student.models import Students, CustomUser, Staffs


class UserModel(UserAdmin):
    pass
admin.site.register(CustomUser , UserModel)
admin.site.register(Students)
admin.site.register(Staffs)
