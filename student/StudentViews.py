import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from student.models import Subjects, Students, Courses, CustomUser, Attendance, AttendanceReport, LeaveRaportStudent, \
    FeedBackStudent


def student_home(request):
    student_obj = Students.objects.get(admin=request.user.id)
    attendance_total = AttendanceReport.objects.filter(student_id=student_obj).count()
    attendance_present = AttendanceReport.objects.filter(student_id=student_obj,status=True).count()
    attendance_absent = AttendanceReport.objects.filter(student_id=student_obj,status=False).count()
    cours_obj = Courses.objects.get(id=student_obj.course_id.id)
    subjects = Subjects.objects.filter(course_id=cours_obj).count()
    subject_name=[]
    data_present=[]
    data_absent=[]
    subject_data = Subjects.objects.filter(course_id=student_obj.course_id)
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance,status=True,student_id=student_obj.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=False,student_id=student_obj.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)
    context={'attendance_total':attendance_total,'attendance_present':attendance_present,'attendance_absent':attendance_absent,'subjects':subjects,'subject_name':subject_name,'data_present':data_present,'data_absent':data_absent}
    return render(request , template_name="student_template/student_home_template.html",context=context)

def student_view_attendance(request):
    students = Students.objects.get(admin=request.user.id)
    courses = Courses.objects.get(id=students.course_id.id)
    subjects = Subjects.objects.filter(course_id=courses)
    context ={
        "subjects":subjects
    }
    return render(request , template_name="student_template/student_view_attendance.html",context=context)
@csrf_exempt
def student_view_attendance_post(request):
    subject_id = request.POST.get("subject")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    start_data_parse = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_data_parse = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    subject_obj = Subjects.objects.get(id=subject_id)
    user_object = CustomUser.objects.get(id = request.user.id)
    stud_obj = Students.objects.get(admin=user_object)
    attendance=Attendance.objects.filter(attendance_date__range=(start_data_parse,end_data_parse),subject_id=subject_obj)
    attendance_reports=AttendanceReport.objects.filter(attendance_id__in=attendance,student_id=stud_obj)
    for attendance_report in attendance_reports:
        print("Date : "+str(attendance_report.attendance_id.attendance_date),"status :"+str(attendance_report.status))

    return render(request,"student_template/student_attendance_data.html",{"attendance_reports":attendance_reports})

def student_aplly_leave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    leave_data = LeaveRaportStudent.objects.filter(student_id=student_obj)
    context = {"leave_data": leave_data}
    return render(request , template_name="student_template/student_apply_leave.html",context=context)
@csrf_exempt
def student_aplly_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_aplly_leave"))
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_reason")
        students_obj = Students.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveRaportStudent(student_id=students_obj , leave_date=leave_date , leave_message=leave_msg , leave_status=0)
            leave_report.save()
            messages.success(request, "success add aplly_leave")
            return HttpResponseRedirect(reverse("student_aplly_leave"))
        except:
            messages.error(request, "error add aplly_leave")
            return HttpResponseRedirect(reverse("student_aplly_leave"))

def student_feedback(request):
    students_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=students_obj)
    context = {"feedback_data": feedback_data}
    return render(request , template_name="student_template/student_feedback.html",context=context)

@csrf_exempt
def student_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_feedback"))
    else:
        feedback_msg = request.POST.get("feedback_msg")
        students_obj = Students.objects.get(admin=request.user.id)
        try:
            feedback = FeedBackStudent(student_id=students_obj , feedback=feedback_msg , feedback_replay="")
            feedback.save()
            messages.success(request, "success sent Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
        except:
            messages.error(request, "failed sent Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))

def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)
    context={'user':user , 'student':student}
    return render(request, template_name="student_template/student_profile.html", context=context)
@csrf_exempt
def student_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        address = request.POST.get("address")
        try:
            userobj = CustomUser.objects.get(id=request.user.id)
            student_addres = Students.objects.get(admin=userobj)
            student_addres.address = address
            student_addres.save()
            userobj.first_name = first_name
            userobj.last_name= last_name
            if password != "" and password != None:
                userobj.set_password(password)
            userobj.save()
            messages.success(request, "Successfully update Profile")
            return HttpResponseRedirect(reverse("student_profile"))
        except:
            messages.error(request , "Fail to update Profile")
            return HttpResponseRedirect(reverse("student_profile"))