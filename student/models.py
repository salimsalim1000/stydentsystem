from datetime import datetime

from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.contrib.auth.models import Group
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    user_type_data = (("1", "HDO"), ("2", "staff"), ("3", "student"))
    user_type = models.CharField(default="1", choices=user_type_data, max_length=20)
    email = models.EmailField(unique=True)

class SessionYearModel(models.Model):
    session_stat_year = models.DateField()
    session_end_year = models.DateField()


class DegreyPrem(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Primary(models.Model):
    withuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    codeonec = models.PositiveSmallIntegerField()
    codelocal = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class DegreyPremCompany(models.Model):
    withdegrey = models.ForeignKey(DegreyPrem, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Primary, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, default=withdegrey.name, null=True, blank=True)
    nomberetud = models.PositiveSmallIntegerField(null=True, blank=True)
    nomberexist = models.PositiveSmallIntegerField(null=True, blank=True)
    femail = models.PositiveSmallIntegerField(null=True, blank=True)
    reatrap = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ('withdegrey', 'company')

    def __str__(self):
        return self.name


class ClassPrimary(models.Model):
    pass


class ClassMoyen(models.Model):
    pass


class ClassSecondary(models.Model):
    pass


class Moyen(models.Model):
    withuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    codeonec = models.PositiveSmallIntegerField()
    codelocal = models.PositiveSmallIntegerField()
    address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class DegreyMoyen(models.Model):
    name = models.CharField(max_length=200)


class DegreyMoyenCompany(models.Model):
    withdegrey = models.ForeignKey(DegreyMoyen, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Moyen, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, default=withdegrey.name, null=True, blank=True)
    nomberetud = models.PositiveSmallIntegerField(null=True, blank=True)
    nomberexist = models.PositiveSmallIntegerField(null=True, blank=True)
    femail = models.PositiveSmallIntegerField(null=True, blank=True)
    reatrap = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ('withdegrey', 'company')

    def __str__(self):
        return self.name


class Secondary(models.Model):
    withprimary = models.OneToOneField(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    codeonec = models.PositiveSmallIntegerField()
    codelocal = models.PositiveSmallIntegerField()
    address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Degrey(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)


class DegreyCompany(models.Model):
    withdegrey = models.ForeignKey(Degrey, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Secondary, on_delete=models.CASCADE, null=True, blank=True)
    spesial = models.ForeignKey('Spesial', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, default=withdegrey.name, null=True, blank=True)
    nomberetud = models.PositiveSmallIntegerField(null=True, blank=True)
    nomberexist = models.PositiveSmallIntegerField(null=True, blank=True)
    femail = models.PositiveSmallIntegerField(null=True, blank=True)
    reatrap = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ('withdegrey', 'company', 'spesial'),

    def __str__(self):
        return self.name


class Spesial(models.Model):
    name = models.CharField(max_length=200)
    degrey = models.ForeignKey(Degrey, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AdminHOD(models.Model):
    withuser = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Mostachar(models.Model):
    withuser = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    datenes = models.DateField(null=True, blank=True)
    stat = models.CharField(max_length=200, null=True, blank=True)
    nomberchild = models.PositiveSmallIntegerField(null=True, blank=True)
    chhada = models.CharField(max_length=200, null=True, blank=True)
    datechhada = models.DateField(null=True, blank=True)
    spesialte = models.CharField(max_length=200, null=True, blank=True)
    universti = models.CharField(max_length=200, null=True, blank=True)
    firstdate = models.DateField(null=True, blank=True)
    firstdateinsector = models.DateField(null=True, blank=True)
    companystay = models.CharField(max_length=200, null=True, blank=True)
    firstdatecomp = models.DateField(null=True, blank=True)
    as1 = models.CharField(max_length=200, null=True, blank=True)
    as2 = models.CharField(max_length=200, null=True, blank=True)
    degry = models.CharField(max_length=200, null=True, blank=True)
    datestart = models.DateField(null=True, blank=True)
    lastdegry = models.PositiveSmallIntegerField(null=True, blank=True)
    dateactive = models.DateField(null=True, blank=True)
    nbrith = models.PositiveSmallIntegerField(null=True, blank=True)
    placebrith = models.CharField(max_length=200, null=True, blank=True)
    ncountccp = models.PositiveSmallIntegerField(null=True, blank=True)
    clee = models.PositiveSmallIntegerField(null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    phone1 = models.CharField(max_length=200, null=True, blank=True)
    phone2 = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.withuser.username)


class MotabaSec(models.Model):
    withcompany = models.ForeignKey(Secondary, on_delete=models.CASCADE)
    study = models.PositiveSmallIntegerField(null=1, blank=1)
    behaviorism = models.PositiveSmallIntegerField(null=1, blank=1)
    familial = models.PositiveSmallIntegerField(null=1, blank=1)
    psychological = models.PositiveSmallIntegerField(null=1, blank=1)
    healthy = models.PositiveSmallIntegerField(null=1, blank=1)
    date = models.DateField(null=1, blank=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.withcompany)


class MotabaMoy(models.Model):
    withcompany = models.ForeignKey(Moyen, on_delete=models.CASCADE)
    study = models.PositiveSmallIntegerField(null=1, blank=1)
    behaviorism = models.PositiveSmallIntegerField(null=1, blank=1)
    familial = models.PositiveSmallIntegerField(null=1, blank=1)
    psychological = models.PositiveSmallIntegerField(null=1, blank=1)
    healthy = models.PositiveSmallIntegerField(null=1, blank=1)
    date = models.DateField(null=1, blank=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class MotabaPre(models.Model):
    withcompany = models.ForeignKey(Primary, on_delete=models.CASCADE)
    study = models.PositiveSmallIntegerField()
    behaviorism = models.PositiveSmallIntegerField()
    familial = models.PositiveSmallIntegerField()
    psychological = models.PositiveSmallIntegerField()
    healthy = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ListeningCells(models.Model):
    withcompany = models.OneToOneField(Secondary, on_delete=models.CASCADE)
    stat_data = (("0", "غير منصبة"), ("1", "منصبة"))
    stat = models.CharField(default="0", choices=stat_data, max_length=20)
    why = models.TextField(max_length=500, null=1, blank=1)
    date = models.DateField(null=1, blank=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Followcommit(models.Model):
    withcompany = models.OneToOneField(Moyen, on_delete=models.CASCADE)
    stat_data = (("0", "غير منصبة"), ("1", "منصبة"))
    stat = models.CharField(default="0", choices=stat_data, max_length=20)
    why = models.TextField(max_length=500, null=1, blank=1)
    date = models.DateField(null=1, blank=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class DirectingSec(models.Model):
    withcompany = models.ForeignKey(Secondary, on_delete=models.CASCADE)
    wafi = models.CharField(max_length=200)
    tawziestbiyan = models.CharField(max_length=200)
    esteglalestbiyan = models.CharField(max_length=200)
    tawzieragbat = models.CharField(max_length=200)
    dirastragbat = models.CharField(max_length=200)
    tawjihtadriji = models.CharField(max_length=200)
    betaktragbat = models.CharField(max_length=200)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class DirectingMoy(models.Model):
    withcompany = models.ForeignKey(Moyen, on_delete=models.CASCADE)
    wafi = models.CharField(max_length=200)
    tawziestbiyan = models.CharField(max_length=200)
    esteglalestbiyan = models.CharField(max_length=200)
    tawzieragbat = models.CharField(max_length=200)
    dirastragbat = models.CharField(max_length=200)
    tawjihtadriji = models.CharField(max_length=200)
    betaktragbat = models.CharField(max_length=200)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class MediaSec(models.Model):
    degraycomany = models.ForeignKey(DegreyCompany, on_delete=models.CASCADE)
    nomberhisas = models.SmallIntegerField()
    date = models.DateField()
    update_at = models.DateTimeField(auto_now_add=True, blank=1, null=1)
    created_at = models.DateTimeField(auto_now_add=True)


class MediaMoy(models.Model):
    withclass = models.ForeignKey(DegreyMoyenCompany, on_delete=models.CASCADE)
    nomberhisas = models.PositiveIntegerField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class MediaPre(models.Model):
    withclass = models.ForeignKey(DegreyPremCompany, on_delete=models.CASCADE)
    nomberhisas = models.PositiveIntegerField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class MediaSecParnt(models.Model):
    withdegrey = models.ForeignKey(Degrey, on_delete=models.CASCADE)
    withsecondray = models.ForeignKey(Secondary, on_delete=models.CASCADE)
    nomberesteda = models.PositiveIntegerField(null=1, blank=1)
    nomberhodor = models.PositiveIntegerField(null=1, blank=1)
    date = models.DateField(null=1, blank=1)
    update_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)


class MediaMoyParnt(models.Model):
    withcompany = models.ForeignKey(Moyen, on_delete=models.CASCADE)
    withdegry = models.ForeignKey(DegreyMoyenCompany, on_delete=models.CASCADE)
    nomberesteda = models.PositiveIntegerField()
    nomberhodor = models.PositiveIntegerField()
    date = models.DateField(null=1, blank=1)
    created_at = models.DateTimeField(auto_now_add=True)


class MediaPreParnt(models.Model):
    withcompany = models.ForeignKey(Primary, on_delete=models.CASCADE)
    withdegry = models.ForeignKey(DegreyPremCompany, on_delete=models.CASCADE)
    nomberesteda = models.PositiveIntegerField()
    nomberhodor = models.PositiveIntegerField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class FileMediaMoy(models.Model):
    withcompany = models.ForeignKey(Moyen, on_delete=models.CASCADE)
    withdegry = models.ForeignKey(DegreyMoyenCompany, on_delete=models.CASCADE)
    type = models.ForeignKey('TypeFileMedia', on_delete=models.CASCADE)
    titel = models.CharField(max_length=2000)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class TypeFileMedia(models.Model):
    name = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FileMediaSec(models.Model):
    withcompany = models.ForeignKey(Secondary, on_delete=models.CASCADE)
    withdegry = models.ForeignKey(Degrey, on_delete=models.CASCADE)
    type = models.ForeignKey(TypeFileMedia, on_delete=models.CASCADE)
    titel = models.CharField(max_length=2000)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class ActiviteName(models.Model):
    name = models.CharField(max_length=2000)
    chouice = (("1", "ثانوي"), ("2", "متوسط"), ("3", "ابتدائي"), ("4", "عام"))
    typee = models.CharField(default="1", choices=chouice, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class OtherActiv(models.Model):
    withuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    withcompany1 = models.ForeignKey(Secondary, on_delete=models.CASCADE, null=True, blank=True)
    withcompany2 = models.ForeignKey(Moyen, on_delete=models.CASCADE, null=True, blank=True)
    withcompany3 = models.ForeignKey(Primary, on_delete=models.CASCADE, null=True, blank=True)
    name = models.ForeignKey(ActiviteName, on_delete=models.CASCADE)
    note = models.TextField(max_length=2000)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class Staffs(models.Model):
    withuser = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.withuser.first_name)


class Courses(models.Model):
    course_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Students(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    profile_pic = models.ImageField(null=1, blank=1)
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING, default=1)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.admin.username


class Subjects(models.Model):
    subject_name = models.CharField(max_length=200)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Attendance(models.Model):
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True)


class AttendanceReport(models.Model):
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class LeaveRaportStudent(models.Model):
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class LeaveRaportStaff(models.Model):
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class FeedBackStudent(models.Model):
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=255)
    feedback_replay = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class FeedBackStaff(models.Model):
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=255)
    feedback_replay = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class NotificationStudent(models.Model):
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class NotificationStaff(models.Model):
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=Secondary)
def create_cells(sender, instance, created, **kwargs):
    if created:
        obk = ListeningCells.objects.create(withcompany=instance, stat="0")
        obk.save()


@receiver(post_save, sender=Moyen)
def create_cell(sender, instance, created, **kwargs):
    if created:
        obk = Followcommit.objects.create(withcompany=instance, stat="0")
        obk.save()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(withuser=instance)
        if instance.user_type == 2:
            Mostachar.objects.create(withuser=instance,email="",phone1="",phone2="",ncountccp=0,nbrith=0,placebrith="",lastdegry=0,degry=0,as1=1,as2=1,companystay="",spesialte="",universti="",stat=1,nomberchild=0,chhada=1,clee=0)
        if instance.user_type == 3:
            Students.objects.create(withuser=instance, course_id=Courses.objects.get(id=1),
                                    session_year_id=SessionYearModel.objects.get(id=1),
                                    address="",
                                    profile_pic="", gender="")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.mostachar.save()




