from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import Widget, ForeignKeyWidget

from student.models import Students, CustomUser, Staffs, Secondary, Moyen, Primary, Mostachar , User
from import_export import resources , fields
from django.contrib.auth.hashers import make_password




class UserModel(UserAdmin):
    pass
class UserModel2(ImportExportModelAdmin):
    pass

admin.site.register(Students , UserModel2)
admin.site.register(Staffs , UserModel2)
admin.site.register(Primary , UserModel2)
admin.site.register(Moyen , UserModel2)
admin.site.register(Secondary , UserModel2)
admin.site.register(Mostachar , UserModel2)




admin.site.register(CustomUser , UserModel2)



