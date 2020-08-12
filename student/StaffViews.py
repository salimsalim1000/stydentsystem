import json
from builtins import id

from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from student.models import Subjects, SessionYearModel, Students, Attendance, AttendanceReport, LeaveRaportStaff, Staffs, \
    FeedBackStaff, CustomUser, Courses
from django.core import serializers

def staff_home(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    course_id_list = []
    for subject in subjects:
        course=Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)
    final_course = []
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)
    student_count =Students.objects.filter(course_id__in=final_course).count()
    attenance_count = Attendance.objects.filter(subject_id__in=subjects).count()
    staff_obj = Staffs.objects.get(admin=request.user.id)
    leave_staff = LeaveRaportStaff.objects.filter(staff_id=staff_obj,leave_status=1).count()
    subject_count=subjects.count()

    subject_list = []
    attendace_list = []
    for subject in subjects:
        attendancecount1 = Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendace_list.append(attendancecount1)

    student_attendance = Students.objects.filter(course_id__in=final_course)
    student_list=[]
    student_list_present = []
    student_list_absent = []
    for stud in student_attendance:
        attendance_present_count = AttendanceReport.objects.filter(status=True,student_id=stud.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(status=False,student_id=stud.id).count()
        student_list_present.append(attendance_present_count)
        student_list_absent.append(attendance_absent_count)
        student_list.append(stud.admin.username)
    context={'student_list_present':student_list_present,'student_list_absent':student_list_absent,'student_list':student_list,'subject_list':subject_list,'attendace_list':attendace_list,'student_count':student_count,'attenance_count':attenance_count,'leave_staff':leave_staff,'subject_count':subject_count}
    return render(request, template_name="staff_template/staff_home_template.html",context=context)

def staff_take_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYearModel.objects.all()

    context={"subjects":subjects , "session_years":session_years }
    return render(request , template_name='staff_template/staff_take_attendance.html', context=context)



@csrf_exempt
def get_student(request):
    subject_id = request.POST.get("subject")
    session_year_id = request.POST.get("session_year")
    subject = Subjects.objects.get(id=subject_id)
    session_year = SessionYearModel.objects.get(id=session_year_id)
    students = Students.objects.filter(course_id=subject.course_id,session_year_id=session_year)
    #student_data = serializers.serialize("python", students)

    list_data=[]
    for student in students:
        data_small = {'id':student.id , 'name':student.admin.first_name+" "+student.admin.last_name }
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def save_attendance_data(request):
    student_ids=request.POST.get("student_ids")
    subject_id=request.POST.get("subject_id")
    attendance_date=request.POST.get("attendance_date")
    session_year_id=request.POST.get("session_year_id")

    subject_model=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.objects.get(id=session_year_id)
    json_sstudent=json.loads(student_ids)
    print(student_ids)
    print(subject_id)
    print(attendance_date)
    print(session_year_id)

    print(json_sstudent)


    try:
        attendance=Attendance(subject_id=subject_model,attendance_date=attendance_date,session_year_id=session_model)
        attendance.save()
        print(attendance)
        for stud in json_sstudent:
            print(stud)
            student=Students.objects.get(id=stud['id'])
            attendance_report=AttendanceReport(student_id=student,attendance_id=attendance,status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")
@csrf_exempt
def staff_update_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_year_id = SessionYearModel.objects.all()
    attendance = Attendance.objects.all()
    context = {"subjects": subjects, "session_year_id": session_year_id}
    return render(request,template_name="staff_template/staff_update_attendance.html", context=context)
@csrf_exempt
def get_attendance_dates(request):
    subject = request.POST.get("subject")
    session_year_id = request.POST.get("session_year_id")

    subject_obj = Subjects.objects.get(id=subject)
    session_year_obj = SessionYearModel.objects.get(id=session_year_id)
    attendance = Attendance.objects.filter(subject_id=subject_obj , session_year_id=session_year_obj)
    attendance_obj = []
    for attendance_single in attendance:
        data = {"id":attendance_single.id , "attendance_date":str(attendance_single.attendance_date) , "session_year_id":attendance_single.session_year_id.id }
        attendance_obj.append(data)
    print(attendance_obj)

    return JsonResponse(json.dumps(attendance_obj),safe=False)
@csrf_exempt
def get_attendance_student(request):

    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)
    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    #students = Students.objects.filter(course_id=subject.course_id, session_year_id=session_year)
    # student_data = serializers.serialize("python", students)

    list_data = []
    for student in attendance_data:
        data_small = {'id': student.student_id.admin.id,'status': student.status , 'name': student.student_id.admin.first_name + " " + student.student_id.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

@csrf_exempt
def save_updateattendance_data(request):
    student_ids=request.POST.get("student_ids")
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    json_sstudent=json.loads(student_ids)
    print(json_sstudent)

    try:
        for stud in json_sstudent:

            print(stud)
            student=Students.objects.get(admin=stud['id'])
            attendance_report=AttendanceReport.objects.get(student_id=student,attendance_id=attendance)
            attendance_report.status=stud['status']
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

def staff_aplly_leave(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    leave_data = LeaveRaportStaff.objects.filter(staff_id=staff_obj)
    context = {"leave_data": leave_data}
    return render(request , template_name="staff_template/staff_apply_leave.html",context=context)
@csrf_exempt
def staff_aplly_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_aplly_leave"))
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_reason")
        staff_obj = Staffs.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveRaportStaff(staff_id=staff_obj , leave_date=leave_date , leave_message=leave_msg , leave_status=0)
            leave_report.save()
            messages.success(request, "success add aplly_leave")
            return HttpResponseRedirect(reverse("staff_aplly_leave"))
        except:
            messages.error(request, "error add aplly_leave")
            return HttpResponseRedirect(reverse("staff_aplly_leave"))

def staff_feedback(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaff.objects.filter(staff_id=staff_obj)
    context = {"feedback_data": feedback_data}
    return render(request , template_name="staff_template/staff_feedback.html",context=context)
@csrf_exempt
def staff_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_feedback"))
    else:
        feedback_msg = request.POST.get("feedback_msg")

        staff_obj = Staffs.objects.get(admin=request.user.id)
        try:
            feedback = FeedBackStaff(staff_id=staff_obj , feedback=feedback_msg , feedback_replay="")
            feedback.save()
            messages.success(request, "success sent Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))
        except:
            messages.error(request, "failed sent Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))

def staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs.objects.get(admin=user)
    context={'user':user , 'staff':staff}
    return render(request, template_name="staff_template/staff_profile.html", context=context)
@csrf_exempt
def staff_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        address = request.POST.get("address")
        try:
            userobj = CustomUser.objects.get(id=request.user.id)
            staff_addres = Staffs.objects.get(admin=userobj)
            staff_addres.address = address
            staff_addres.save()
            userobj.first_name = first_name
            userobj.last_name= last_name
            if password != "" and password != None:
                userobj.set_password(password)
            userobj.save()
            messages.success(request, "Successfully update Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request , "Fail to update Profile")
            return HttpResponseRedirect(reverse("staff_profile"))