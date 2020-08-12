import datetime
import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from student import views
from student.forms import AddStudentForm, EditStudentForm
from student.models import CustomUser, Courses, Students, Staffs, Subjects, SessionYearModel, FeedBackStudent, \
    FeedBackStaff, LeaveRaportStudent, LeaveRaportStaff, Attendance, AttendanceReport


def admin_home(request):
    subjects_count = Subjects.objects.all().count()
    student_count = Students.objects.all().count()
    course_count = Courses.objects.all().count()
    staff_count = Staffs.objects.all().count()
    subjects_list=[]
    cours_list = []
    student_list=[]
    course_all = Courses.objects.all()
    for cour in course_all:
        subjec = Subjects.objects.filter(course_id=cour.id).count()
        studentevery = Students.objects.filter(course_id=cour.id).count()
        subjects_list.append(subjec)
        cours_list.append(cour.course_name)
        student_list.append(studentevery)

    context={'student_list':student_list,'subjects_list':subjects_list,'cours_list':cours_list,'subjects_count':subjects_count,'student_count':student_count,'course_count':course_count,'staff_count':staff_count}
    return render (request,template_name="hod_template/home_content.html",context=context)

def add_staff(request):
    return render(request,template_name="hod_template/add_staff_template.html")

def add_staff_save(request):
    if request.method != "POST":
        return HttpResponse("method not valid")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        try:
            user = CustomUser.objects.create_user(first_name= first_name ,last_name=last_name , username=username , email=email , password=password , user_type= 2 )
            user.staffs.address = address
            user.save()
            messages.success(request,"success add staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request, "error add staff")
            return HttpResponseRedirect(reverse("add_staff"))


def add_course(request):
    return render(request, template_name="hod_template/add_course_template.html")

def add_course_save(request):
    if request.method != "POST" :
        messages.error(request,"method not allow")
        return HttpResponseRedirect(reverse("add_course"))
    else:
        course = request.POST.get("course")
        try:
            course_model = Courses.objects.create(course_name=course)
            course_model.save()
            messages.success(request, "success add cours")
            return HttpResponseRedirect(reverse("add_course"))
        except:
            messages.error(request, "error add cours")
            return HttpResponseRedirect(reverse("add_course"))


def add_student(request):
    courses = Courses.objects.all()
    sessions = SessionYearModel.objects.all()
    form = AddStudentForm()
    return render(request, template_name="hod_template/add_student_template.html",context={'courses':courses , 'sessions':sessions ,'form':form})


def add_student_save(request ):

    if request.method != "POST":
        messages.error(request, "method not allow")
        return HttpResponseRedirect(reverse("add_student_save"))
    else:
        form = AddStudentForm(request.POST , request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            address = form.cleaned_data["address"]
            course_id = form.cleaned_data["course"]
            sex = form.cleaned_data["sex"]
            session_year_id = form.cleaned_data["session_year_id"]

            if request.FILES.get('profile_pic', False):
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename = fs.save(profile_pic.name,profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None


            try:
                user = CustomUser.objects.create_user(first_name= first_name ,last_name=last_name , username=username , email=email , password=password , user_type= 3 )
                user.students.address = address
                user.students.gender = sex
                course_obj = Courses.objects.get(id=course_id)
                user.students.course_id = course_obj

                user.students.profile_pic = profile_pic_url
                session = SessionYearModel.objects.get(id=session_year_id)
                user.students.session_year_id = session

                #user.students.profile_pic = ""
                user.save()
                messages.success(request,"success reistertion studernt")
                return HttpResponseRedirect(reverse("add_student"))
            except:
                messages.error(request, "field reistertion studernt")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form = AddStudentForm(request.POST )
        return render(request, template_name="hod_template/add_student_template.html",context={ 'form':form})

def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, template_name="hod_template/add_subject_template.html",context={'courses':courses , 'staffs':staffs})

def add_subject_save(request):
    if request.method != "POST":
        messages.error(request, "method not allow")
        return HttpResponseRedirect(reverse("add_subject"))
    else:
        subject_name = request.POST.get("subject_name")
      #  course_id = request.POST.get("course")
        course = Courses.objects.get(id=request.POST.get("course"))

        staff_id = request.POST.get("staff")
        staff = CustomUser.objects.get(id=staff_id)
    try:

        subject = Subjects.objects.create(subject_name=subject_name , course_id_id=course.id , staff_id_id=staff.id)
        subject.save()
        messages.success(request, "success add subject")
        return HttpResponseRedirect(reverse("add_subject"))
    except:
        messages.error(request, "field  add subject")
        return HttpResponseRedirect(reverse("add_subject"))


def manage_staff(request):
    staffs = Staffs.objects.all()
    context={'staffs':staffs}
    return render(request, template_name="hod_template/manage_staff_template.html",context=context)


def manage_student(request):
    students = Students.objects.all()
    context={'students':students}
    return render(request, template_name="hod_template/manage_student_template.html",context=context)


def manage_course(request):
    courses = Courses.objects.all()
    context={'courses':courses}
    return render(request, template_name="hod_template/manage_course_template.html",context=context)

def manage_subject(request):
    subjects = Subjects.objects.all()
    context={'subjects':subjects}
    return render(request, template_name="hod_template/manage_subject_template.html",context=context)

def edit_staff(request , staff_id ):
    staff = Staffs.objects.get(admin=staff_id)
    context = {'staff': staff , 'staff_idd':staff_id}
    return render(request, template_name="hod_template/edit_staff_template.html",context=context)

def edit_staff_save(request):
    if request.method != "POST" :
        messages.error(request, "method not allow")

    else:
        staff_id = request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")

        address = request.POST.get("address")
        try:

            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email

            user.save()

            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()
            messages.success(request, "success update staff")
            return HttpResponseRedirect(reverse("edit_staff", args=[staff_id]))
        except:

            messages.error(request, "field  update staff")
            return HttpResponseRedirect(reverse("edit_staff",args=[staff_id]))


def edit_student(request , student_id ):
    request.session['student_id']= student_id
    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()

    form.fields['email'].initial = student.admin.email
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['username'].initial = student.admin.username
    form.fields['address'].initial = student.address
    form.fields['course'].initial = student.course_id.id
    form.fields['sex'].initial = student.gender
#   form.fields['profile_pic'].initial = student.profile_pic

    form.fields['session_year_id'].initial = student.session_year_id.id



    context = {'form': form  , 'id':student_id , 'username':student.admin.username}
    return render(request, template_name="hod_template/edit_student_template.html",context=context)

def edit_student_save(request):
    if request.method != "POST" :
        messages.error(request, "method not allow")

    else:
        student_id = request.session.get('student_id')
        if student_id == None:
            return HttpResponseRedirect(reverse("manage_student"))
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")

        address = request.POST.get("address")
        course_id = request.POST.get("course")
        sex = request.POST.get("sex")
        session_year_id = request.POST.get("session_year_id")
        sess = SessionYearModel.objects.get(id= session_year_id)
        session_year_idd = sess

        if request.FILES.get('profile_pic' , False) :
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None
        try:


            user = CustomUser.objects.get(id=student_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email


            user.save()

            student_model = Students.objects.get(admin=student_id)
            student_model.address = address
            student_model.gender = sex
            student_model.session_year_id = session_year_idd

            if profile_pic_url != None:
                student_model.profile_pic = profile_pic_url

            course = Courses.objects.get(id=course_id)
            student_model.course_id = course
            student_model.save()
            del request.session['student_id']
            messages.success(request, "success update student")
            return HttpResponseRedirect(reverse("edit_student" , args=[student_id]))
        except:

            messages.error(request, "field  update student")
            return HttpResponseRedirect(reverse("edit_student" , args=[student_id]))


def edit_course(request , cours_id ):
    course = Courses.objects.get(id=cours_id)

    context = {'course':course , 'id':cours_id}
    return render(request, template_name="hod_template/edit_course_template.html",context=context)

def edit_course_save(request):
    if request.method != "POST":
        messages.error(request, "method not allow")
    else:
        cours_name = request.POST.get("course")
        course_id = request.POST.get("course_id")

        try:
            cours = Courses.objects.get(id=course_id)
            cours.course_name = cours_name
            cours.save()
            return HttpResponseRedirect(reverse('edit_course' , args=[course_id]))
        except:
            messages.error(request, "field  update cours")
            return HttpResponseRedirect(reverse('edit_course' , args=[course_id]))

def edit_subject(request , subject_id ):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    context = {'subject':subject , 'courses':courses , 'staffs':staffs , 'id':subject_id}
    return render(request, template_name="hod_template/edit_subject_template.html",context=context)

def edit_subject_save(request):
    if request.method != "POST":
        messages.error(request, "method not allow")
        return HttpResponse("not allow to be here")
    else:
        try:
            subject_name = request.POST.get("subject_name")
            subject_id = request.POST.get("subject_id")
            course = request.POST.get("course")
            staffs = request.POST.get("staff")

            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name

            staff = CustomUser.objects.get(id=staffs)
            subject.staff_id = staff
      
            cours = Courses.objects.get(id=course)
            subject.course_id = cours

            subject.save()
            return HttpResponseRedirect(reverse('edit_subject',args=[subject_id]))
        except:
            messages.error(request, "field  update cours")
            return HttpResponseRedirect(reverse('edit_subject',args=[subject_id]))


def manage_session(request):
    return render(request , template_name='hod_template/manage_session_template.html')

def manage_session_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_start_year = request.POST.get("session_start")
        session_end_year = request.POST.get("session_end")
        try:
            sessionyear = SessionYearModel(session_stat_year=session_start_year , session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request , "success add session")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request, "field  add session")
            return HttpResponseRedirect(reverse("manage_session"))

@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

def student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.all()
    context={
        'feedbacks':feedbacks
    }
    return render(request,template_name="hod_template/student_feedback_template.html",context=context)
@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_msg = request.POST.get("message")
    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_replay=feedback_msg
        feedback.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Eroor")
def staff_feedback_message(request):
    feedbacks = FeedBackStaff.objects.all()
    context={
        'feedbacks':feedbacks
    }
    return render(request,template_name="hod_template/staff_feedback_template.html",context=context)
@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_msg = request.POST.get("message")
    try:
        feedback = FeedBackStaff.objects.get(id=feedback_id)
        feedback.feedback_replay = feedback_msg
        feedback.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Eroor")

def student_leave_view(request):
    leaves=LeaveRaportStudent.objects.all()
    context = {
        'leaves': leaves
    }
    return render(request,template_name="hod_template/student_leave_view.html",context=context)


def staff_leave_view(request):
    leaves=LeaveRaportStaff.objects.all()
    context = {
        'leaves': leaves
    }
    return render(request,template_name="hod_template/staff_leave_view.html",context=context)

def student_approve_leave(request , leave_id):
    leavereport = LeaveRaportStudent.objects.get(id=leave_id)
    leavereport.leave_status = "1"
    leavereport.save()
    return HttpResponseRedirect(reverse("student_leave_view"))
def staff_disapprove_leave(request,leave_id):
    leavereport = LeaveRaportStudent.objects.get(id=leave_id)
    leavereport.leave_status = "2"
    leavereport.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def student_disapprove_leave(request, leave_id):
    leavereport = LeaveRaportStudent.objects.get(id=leave_id)
    leavereport.leave_status = "2"
    leavereport.save()
    return HttpResponseRedirect(reverse("student_leave_view"))

def staff_approve_leave(request , leave_id):
    leavereport = LeaveRaportStudent.objects.get(id=leave_id)
    leavereport.leave_status = "1"
    leavereport.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_year_id = SessionYearModel.objects.all()
    context = {"subjects": subjects, "session_year_id": session_year_id}
    return render(request, template_name="hod_template/admin_view_attendance.html",context=context)
@csrf_exempt
def admin_get_attendance_dates(request):
    subject = request.POST.get("subject")
    session_year_id = request.POST.get("session_year_id")
    subject_obj = Subjects.objects.get(id=subject)
    session_year_obj = SessionYearModel.objects.get(id=session_year_id)
    attendance = Attendance.objects.filter(subject_id=subject_obj, session_year_id=session_year_obj)
    attendance_obj = []
    for attendance_single in attendance:
        data = {"id": attendance_single.id, "attendance_date": str(attendance_single.attendance_date),
                "session_year_id": attendance_single.session_year_id.id}
        attendance_obj.append(data)
    print(attendance_obj)

    return JsonResponse(json.dumps(attendance_obj), safe=False)
@csrf_exempt
def admin_get_attendance_student(request):
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)
    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # students = Students.objects.filter(course_id=subject.course_id, session_year_id=session_year)
    # student_data = serializers.serialize("python", students)

    list_data = []
    for student in attendance_data:
        data_small = {'id': student.student_id.admin.id, 'status': student.status,
                      'name': student.student_id.admin.first_name + " " + student.student_id.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    context={'user':user}
    return render(request, template_name="hod_template/admin_profile.html", context=context)
@csrf_exempt
def admin_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        try:
            userobj = CustomUser.objects.get(id=request.user.id)
            userobj.first_name = first_name
            userobj.last_name= last_name
            if password != "" and password != None:
                userobj.set_password(password)
            userobj.save()
            messages.success(request, "Successfully update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request , "Fail to update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))

