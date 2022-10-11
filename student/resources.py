from import_export import resources
from student.models import CustomUser,User


class UserResource(resources.ModelResource):

    class Meta:
        model = CustomUser