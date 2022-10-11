
import json
from builtins import id
from datetime import datetime
from decimal import Decimal
from django.db.models import Q
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum, F, FloatField, Count , ExpressionWrapper
from django.db.models.functions import Cast
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


from student import views
from student.forms import AddStudentForm, EditStudentForm
from student.models import CustomUser, Courses, Students, Staffs, Subjects, SessionYearModel, FeedBackStudent, \
    FeedBackStaff, LeaveRaportStudent, LeaveRaportStaff, Attendance, AttendanceReport, Primary, Moyen, Secondary, \
    DegreyMoyen, Degrey, DegreyPrem, Spesial, ClassPrimary, ClassMoyen, ClassSecondary, Mostachar, ActiviteName, \
    TypeFileMedia, MediaSec, MediaMoy, MediaPre, MotabaSec, MotabaMoy, Followcommit, ListeningCells, MediaSecParnt, \
    DegreyCompany, MediaMoyParnt, DegreyMoyenCompany, MediaPreParnt, DegreyPremCompany, FileMediaSec, FileMediaMoy, \
    OtherActiv
from django.db.models import Func


class Round2(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 2)'

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


def add_premary(request):
    premers = Primary.objects.all()
    context={"premers":premers}
    return render(request, template_name="hod_template/add_premary_template.html",context=context)

def add_premary_save(request):
    if request.method != "POST" :
        messages.error(request,"method not allow")
        return HttpResponseRedirect(reverse("add_premary"))
    else:

        name = request.POST.get("name")
        codeonec = request.POST.get("codeonec")
        codelocal = request.POST.get("codelocal")
        try:
            primary_model = Primary.objects.create(name=name,codeonec=codeonec,codelocal=codelocal)
            primary_model.save()
            messages.success(request, "تم اضافة المؤسسة بنجاح")
            return HttpResponseRedirect(reverse("add_premary"))
        except:
            messages.error(request, "error add cours")
            return HttpResponseRedirect(reverse("add_premary"))

def add_moyen(request):
    premers = Moyen.objects.all()
    context={"premers":premers}
    return render(request, template_name="hod_template/add_moyen_template.html",context=context)

def add_moyen_save(request):
    if request.method != "POST" :
        messages.error(request,"method not allow")
        return HttpResponseRedirect(reverse("add_moyen"))
    else:

        name = request.POST.get("name")
        codeonec = request.POST.get("codeonec")
        codelocal = request.POST.get("codelocal")
        try:
            moyen_model = Moyen.objects.create(name=name,codeonec=codeonec,codelocal=codelocal)
            moyen_model.save()
            messages.success(request, "تم اضافة المؤسسة بنجاح")
            return HttpResponseRedirect(reverse("add_moyen"))
        except:
            messages.error(request, "error add cours")
            return HttpResponseRedirect(reverse("add_moyen"))

def add_secondry(request):
    premers = Secondary.objects.all()
    context={"premers":premers}
    return render(request, template_name="hod_template/add_secondry_template.html",context=context)

def add_secondry_save(request):
    if request.method != "POST" :
        messages.error(request,"method not allow")
        return HttpResponseRedirect(reverse("add_secondry"))
    else:

        name = request.POST.get("name")
        codeonec = request.POST.get("codeonec")
        codelocal = request.POST.get("codelocal")
        try:
            secondary_model = Secondary.objects.create(name=name,codeonec=codeonec,codelocal=codelocal)
            secondary_model.save()
            messages.success(request, "تم اضافة المؤسسة بنجاح")
            return HttpResponseRedirect(reverse("add_secondry"))
        except:
            messages.error(request, "error add cours")
            return HttpResponseRedirect(reverse("add_secondry"))

def add_degreymoyen(request):
    return render(request, template_name="hod_template/add_degreymoyen_template.html")

def add_degreymoyen_save(request):
    if request.method != "POST" :
        messages.error(request,"method not allow")
        return HttpResponseRedirect(reverse("add_degreymoyen"))
    else:
        name = request.POST.get("name")
        try:
            model = DegreyMoyen.objects.create(name=name)
            model.save()
            messages.success(request, "تم اضافة المستوى بنجاح")
            return HttpResponseRedirect(reverse("add_degreymoyen"))
        except:
            messages.error(request, "error add cours")
            return HttpResponseRedirect(reverse("add_degreymoyen"))


def add_speasial(request):
    degry = Degrey.objects.all()
    context={'degry':degry}
    return render(request, template_name="hod_template/add_spesial_template.html",context=context)

def add_speasial_save(request):
    if request.method != "POST" :
        messages.error(request,"method not allow")
        return HttpResponseRedirect(reverse("add_speasial"))
    else:
        name = request.POST.get("name")
        degryid = request.POST.get("degry")
        try:
            degry = Degrey.objects.get(id=degryid)
            model = Spesial.objects.create(name=name,degrey=degry)
            model.save()
            messages.success(request, "تم اضافة المستوى بنجاح")
            return HttpResponseRedirect(reverse("add_speasial"))
        except:
            messages.error(request, "خطافي الاضافة")
            return HttpResponseRedirect(reverse("add_speasial"))


def add_degreypremglobal(request):
    return render(request, template_name="hod_template/add_degrypremary_template.html")


def add_degreypremglobal_save(request):
    if request.method != "POST" :
        messages.error(request,"method not allow")
        return HttpResponseRedirect(reverse("add_degreypremglobal"))
    else:
        name = request.POST.get("name")
        try:
            model = DegreyPrem.objects.create(name=name)
            model.save()
            messages.success(request, "تم اضافة المستوى بنجاح")
            return HttpResponseRedirect(reverse("add_degreypremglobal"))
        except:
            messages.error(request, "error add cours")
            return HttpResponseRedirect(reverse("add_degreypremglobal"))

def add_degreyseco(request):
    return render(request, template_name="hod_template/add_degryseconder_template.html")

def add_degreyseco_save(request):
    if request.method != "POST" :
        messages.error(request,"method not allow")
        return HttpResponseRedirect(reverse("add_degreyseco"))
    else:
        name = request.POST.get("name")
        try:
            model = Degrey.objects.create(name=name)
            model.save()
            messages.success(request, "تم اضافة المستوى بنجاح")
            return HttpResponseRedirect(reverse("add_degreyseco"))
        except:
            messages.error(request, "error add cours")
            return HttpResponseRedirect(reverse("add_degreyseco"))

def add_classprem(request):
    degry = DegreyPrem.objects.all()
    Primarys= Primary.objects.all()
    context={"degry":degry,"Primarys":Primarys}
    return render(request, template_name="hod_template/add_classpremary_template.html",context=context)

def add_classprem_save(request):
    if request.method != "POST" :
        messages.error(request,"method not allow")
        return HttpResponseRedirect(reverse("add_classprem"))
    else:
        primary = request.POST.get("primary")
        idd = request.POST.get("degry")
        name = request.POST.get("name")
        numetud = request.POST.get("numetud")
        numetudex = request.POST.get("numetudex")
        femal = request.POST.get("femal")
        reatrap = request.POST.get("reatrap")

        try:
            primarys = Primary.objects.get(id=primary)
            degreyid = DegreyPrem.objects.get(id=idd)
            modele = ClassPrimary.objects.create(withprimary=primarys,degrey=degreyid,name=name,nomberstudent=numetud,nomberstudexist=numetudex,nomberfemale=femal,repeater=reatrap)
            modele.save()
            messages.success(request, "تم اضافة القسم بنجاح")
            return HttpResponseRedirect(reverse("add_classprem"))
        except:
            messages.error(request, "error add cours")
            return HttpResponseRedirect(reverse("add_classprem"))



def add_classmoyen(request):
    degry = DegreyMoyen.objects.all()
    primarys = Moyen.objects.all()
    context={"degry":degry,"primarys":primarys}
    return render(request, template_name="hod_template/add_classmoyen_template.html",context=context)

def add_classmoyen_save(request):
    if request.method != "POST" :
        messages.error(request,"method not allow")
        return HttpResponseRedirect(reverse("add_classprem"))
    else:
        primary = request.POST.get("primary")
        idd = request.POST.get("degry")
        name = request.POST.get("name")
        numetud = request.POST.get("numetud")
        numetudex = request.POST.get("numetudex")
        femal = request.POST.get("femal")
        reatrap = request.POST.get("reatrap")

        try:
            moyen = Moyen.objects.get(id=primary)
            degreyid = DegreyMoyen.objects.get(id=idd)
            modele = ClassMoyen.objects.create(withprimary=moyen,degrey=degreyid,name=name,nomberstudent=numetud,nomberstudexist=numetudex,nomberfemale=femal,repeater=reatrap)
            modele.save()
            messages.success(request, "تم اضافة القسم بنجاح")
            return HttpResponseRedirect(reverse("add_classprem"))
        except:
            messages.error(request, "error add cours")
            return HttpResponseRedirect(reverse("add_classprem"))

def add_classsecond(request):
    name = Secondary.objects.all()
    degry = Degrey.objects.all()
    spisialte = Spesial.objects.all()

    context={"name":name,"degry":degry,"spisialte":spisialte}
    return render(request, template_name="hod_template/add_classsecond_template.html",context=context)

def add_classsecond_save(request):
    if request.method != "POST" :
        messages.error(request,"method not allow")
        return HttpResponseRedirect(reverse("add_classsecond"))
    else:
        primary = request.POST.get("primary")
        degry = request.POST.get("degry")
        speisal = request.POST.get("speisal")
        name = request.POST.get("name")
        numetud = request.POST.get("numetud")
        numetudex = request.POST.get("numetudex")
        femal = request.POST.get("femal")
        reatrap = request.POST.get("reatrap")
        try:
            degreyid = Degrey.objects.get(id=degry)
            companyid = Secondary.objects.get(id=primary)
            speisalid = Spesial.objects.get(id=speisal)
            modele = ClassSecondary.objects.create(withprimary=companyid,degreye=degreyid,specialite=speisalid,name=name,nomberstudent=numetud,nomberstudexist=numetudex,nomberfemale=femal,repeater=reatrap)
            modele.save()
            messages.success(request, "تم اضافة القسم بنجاح")
            return HttpResponseRedirect(reverse("add_classsecond"))
        except:
            messages.error(request, "error add cours")
            return HttpResponseRedirect(reverse("add_classsecond"))


def add_mostachar(request):
    return render(request,template_name="hod_template/add_mostachar_template.html")

def add_mostachar_save(request):
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
            user.mostachar.address = address
            user.save()
            messages.success(request,"تم اضافة المستشار")
            return HttpResponseRedirect(reverse("add_mostachar"))
        except:
            messages.error(request, "اسم المستخدم او البريد الالكتروني موجود بالفعل")
            return HttpResponseRedirect(reverse("add_mostachar"))

def manage_mostachar(request):
    mostachars = Mostachar.objects.all()
    context={'mostachars':mostachars}
    return render(request, template_name="hod_template/manage_mostachar_template.html",context=context)

def edit_mostachar(request , mostachar_id ):
    mostachar = Mostachar.objects.get(withuser=mostachar_id)
    context = {'mostachar': mostachar , 'staff_idd':mostachar_id}
    return render(request, template_name="hod_template/edit_mostachar_template.html",context=context)

def edit_mostachar_save(request):
    if request.method != "POST" :
        messages.error(request, "method not allow")

    else:
        mostachar_id = request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        address = request.POST.get("address")
        try:

            user = CustomUser.objects.get(id=mostachar_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email

            user.save()

            mostachar_model = Mostachar.objects.get(withuser=mostachar_id)
            mostachar_model.address = address
            mostachar_model.save()
            messages.success(request, "تم تعديل معلومات المستشار")
            return HttpResponseRedirect(reverse("edit_mostachar", args=[mostachar_id]))
        except:

            messages.error(request, "خطأ في تعديل المعلومات قد يكون اسم المستخدم او البريد محجوزين بالفعل")
            return HttpResponseRedirect(reverse("edit_mostachar",args=[mostachar_id]))


def distribit(request):
    mostachars = Mostachar.objects.all()
    seconrays = Secondary.objects.all()
    moyens = Moyen.objects.all()
    primary = Primary.objects.all()
    context = {"mostachars":mostachars, "seconrays":seconrays, "moyens":moyens, "primarys":primary}
    return render(request, template_name="hod_template/distrebit_mostachar_template.html",context =context )


def distribit_save(request):
    if request.method != "POST" :
        messages.error(request, "method not allow")
    else:
        mostachar_id = request.POST.get("mostacharid")
        checkcompany = request.POST.getlist("checkcompany")

        #  try:
        mostacharobj = Mostachar.objects.get(id=mostachar_id)
        user = CustomUser.objects.get(id=mostacharobj.withuser.id)
        secondry = Secondary.objects.get(id__in=checkcompany)
        secondry.withprimary = user
        print(secondry)
        secondry.save()
        messages.success(request, "success update staff")
        return HttpResponseRedirect(reverse("distribit"))
            # except:


def distribitmoyen_save(request):
    if request.method != "POST":
        messages.error(request, "method not allow")
    else:
        mostachar_id = request.POST.get("mostacharmoyenid")
        checkcompany = request.POST.getlist("checkcompanymoyen")
        print(mostachar_id)
        print(checkcompany)
            #  try:
        mostacharobj = Mostachar.objects.get(id=mostachar_id)
        print(mostacharobj)
        user = CustomUser.objects.get(id=mostacharobj.withuser.id)
        moyen = Moyen.objects.filter(id__in=checkcompany)
        print(moyen)
        for company in moyen:
            company.withuser = user
            print(company)
            company.save()
        messages.success(request, "success update staff")
        return HttpResponseRedirect(reverse("distribit"))


def distribitprimer_save(request):
    if request.method != "POST":
        messages.error(request, "method not allow")
    else:
        mostachar_id = request.POST.get("mostacharprimerid")
        checkcompany = request.POST.getlist("checkcompanyprem")
        print(mostachar_id)
        print(checkcompany)
            #  try:
        mostacharobj = Mostachar.objects.get(id=mostachar_id)
        print(mostacharobj)
        user = CustomUser.objects.get(id=mostacharobj.withuser.id)
        premer = Primary.objects.filter(id__in=checkcompany)
        print(premer)
        for company in premer:
            company.withuser = user
            print(company)
            company.save()
        messages.success(request, "success update staff")
        return HttpResponseRedirect(reverse("distribit"))

    #   messages.error(request, "field  update staff")
            #return HttpResponseRedirect(reverse("distribit"))

def add_activte(request):
    activeobj = ActiviteName.objects.all()
    context={'activeobj':activeobj}
    return render(request, template_name="hod_template/add_actvite_template.html", context=context)


def add_activte_save(request):
    if request.method != "POST" :
        messages.error(request, "method not allow")
    else:
        name = request.POST.get("name")
        typee = request.POST.get("typee")
        active = ActiviteName.objects.create(name=name, typee=typee)
        active.save()
        messages.success(request, "تم الاضافة")
        return HttpResponseRedirect(reverse("add_activte"))


def add_typefilemedia(request):
    try:
        filemedia = TypeFileMedia.objects.all()
    except:
        filemedia=""
    context = {'filemedia': filemedia}
    return render(request, template_name="hod_template/add_typefilemedia_template.html", context=context)


def add_typefilemedia_save(request):
    if request.method != "POST" :
        messages.error(request, "method not allow")
    else:
        name = request.POST.get("name")
        typemediafile = TypeFileMedia.objects.create(name=name)
        typemediafile.save()
        messages.success(request, "تم الاضافة")
        return HttpResponseRedirect(reverse("add_typefilemedia"))


def mostachar_info(request):
    mostachars = Mostachar.objects.select_related('withuser').all()
    context={'mostachars':mostachars}
    return render(request, template_name="hod_template/mostachar_info.html",context=context)


def date_all(request):
    mostachars = Mostachar.objects.select_related('withuser').all()
    context={'mostachars':mostachars}
    return render(request, template_name="hod_template/date_range_template.html",context=context)


def date_all_get(request):



    primary1 = request.GET.get("primary1")
    primary2 = request.GET.get("primary2")


    # الاعلام#
    try:
        primary1 = datetime.strptime(primary1, "%Y-%m-%d")
        primary2 = datetime.strptime(primary2, "%Y-%m-%d")
    except:
        pass


    try:
        mediasec = MediaSec.objects.select_related('degraycomany__company','degraycomany__spesial').filter(date__range=[primary1, primary2])
    except:
        mediasec=""
    try:
        mediamoy = MediaMoy.objects.select_related('withclass__company').filter(date__range=[primary1, primary2])
    except:
        mediamoy=""
    try:
        mediapre = MediaPre.objects.select_related('withclass__company').filter(date__range=[primary1, primary2])
    except:
        mediapre=""

    #المتابعة

    try:
        motabasec = MotabaSec.objects.select_related('withcompany').filter(date__range=[primary1, primary2])
    except:
        motabasec = ""



    try:
        motabamoy = MotabaMoy.objects.select_related('withcompany').filter(date__range=[primary1, primary2])
    except:
        motabamoy = ""


    #خلية الاصغاء

    try:
        listingcell = ListeningCells.objects.select_related('withcompany').filter(date__range=[primary1, primary2])
    except:
        listingcell = ""



    #لجان المتابعة

    try:
        followcomit = Followcommit.objects.select_related('withcompany').filter(date__range=[primary1, primary2])
    except:
        followcomit = ""


    #اعلام الاولياء

    try:
        mediasecparnt = MediaSecParnt.objects.select_related('withsecondray','withdegrey').filter(date__range=[primary1, primary2]).values('id', 'withdegrey__name', 'withdegrey__id', 'withsecondray__id', 'withsecondray__name', 'date','nomberesteda','nomberhodor').annotate(persontage=Round2(ExpressionWrapper(Cast(F('nomberhodor')*100, FloatField())/F('nomberesteda'),
        output_field=FloatField())))
        listmedsec=list(mediasecparnt)
        liste = mediasecparnt.values_list('withdegrey_id', 'withsecondray_id')
        thelist = list(liste)
        q_filter = Q(*[Q(withdegrey=x, company=y) for x, y in (thelist)], _connector=Q.OR)
        ddegrycomp = DegreyCompany.objects.filter(q_filter).values('withdegrey_id', 'company_id').annotate(
            nomberetude=Sum('nomberetud'))
        ddegrycompe = list(ddegrycomp)
        data = []
        dictt = {}
        i = 0
        while i < len(listmedsec):
            j = 0
            while j < len(ddegrycompe):
                if listmedsec[i]['withsecondray__id'] == ddegrycompe[j]['company_id'] and listmedsec[i]['withdegrey__id'] == ddegrycompe[j]['withdegrey_id']:
                    dictt.update(listmedsec[i])
                    dictt.update(ddegrycompe[j])
                    newdict = dict(dictt)
                    data.append(newdict)
                j += 1
            i += 1
        print(data)
    except:
        data= []

    #اعلا الاولياء متوسط

    try:
        mediamoyparnt =MediaMoyParnt.objects.filter(date__range=[primary1, primary2]).values('id','date','withdegry__name','withcompany__name','nomberesteda','nomberhodor','withdegry__nomberetud')
        data_listmediamoy = list(mediamoyparnt)
        datamoy = []
        for l in data_listmediamoy:
            persontage = ((l["nomberhodor"] * 100) / l["nomberesteda"]).__round__(2)
            l.update({"percontage": persontage})
            datamoy.append(l)
    except:
        datamoy = []


    #اعلا الاولياء ابتدائي

    try:
        mediapremparnt = MediaPreParnt.objects.select_related('withcompany','withdegry').filter(date__range=[primary1, primary2]).values('id','date','withdegry__name','withcompany__name','nomberesteda','nomberhodor','withdegry__nomberetud').annotate(persontage=Round2(ExpressionWrapper(Cast(F('nomberhodor')*100, FloatField())/F('nomberesteda'),
        output_field=FloatField())))
        dataprem = list(mediapremparnt)
    except:
        dataprem = []


    # ثانوي الوثائق الاعلامية

    try:
        filemediasec = FileMediaSec.objects.select_related('withcompany','withdegry','type').filter(date__range=[primary1, primary2])

    except:
        filemediasec = ""


    # متوسط الوثائق الاعلامية

    try:
        filemediamoy = FileMediaMoy.objects.select_related('withcompany','withdegry','type').filter(date__range=[primary1, primary2])
    except:
        filemediamoy = ""


    # نشاطات اخرى ثانوي
    try:
        otheractivesec = OtherActiv.objects.select_related('withcompany1','name').filter(withcompany1__isnull=False,date__range=[primary1, primary2])
    except:
        otheractivesec = ""


    # نشاطات اخرى متوسط
    try:
        otheractivemoy = OtherActiv.objects.select_related('withcompany2','name').filter(withcompany2__isnull=False,date__range=[primary1, primary2])
    except:
        otheractivemoy = ""


    # نشاطات اخرى ابتدائي
    try:
        otheractiveprem = OtherActiv.objects.select_related('withcompany3','name').filter(withcompany3__isnull=False, date__range=[primary1, primary2])
    except:
        otheractiveprem = ""
    test = OtherActiv.objects.filter(
        withcompany3__isnull=False, date__range=[primary1, primary2])

    print(test)
    # نشاطات اخرى عامة
    try:
        otheract = OtherActiv.objects.select_related('name').filter(withcompany1=None, withcompany2=None, withcompany3=None, date__range=[primary1, primary2])
    except:
        otheract = ""
    context = {"data":data, "otheract":otheract, "otheractiveprem":otheractiveprem,"otheractivesec":otheractivesec, "otheractivemoy":otheractivemoy, "filemediasec":filemediasec,"filemediamoy":filemediamoy ,"dataprem":dataprem ,"datamoy":datamoy ,"mediasec":mediasec, "mediamoy":mediamoy, "mediapre":mediapre, "primary1":primary1, "primary2":primary2, "motabasec":motabasec, "motabamoy":motabamoy, "listingcell":listingcell, "followcomit":followcomit}
    return render(request, template_name="hod_template/date_range_template.html",context=context)

 #--------------------------------------------#

#hالجميع الكلي
def date_range_full(request):
    return render(request, template_name="hod_template/date_rangeall_template.html")

#hالجميع الكلي
def date_range_full_get(request):
    primary1 = request.GET.get("primary1")
    primary2 = request.GET.get("primary2")

    try:
        objsecondery = Secondary.objects.get(withprimary=request.user.id)
        degraycompsec = DegreyCompany.objects.filter(company=objsecondery)
    except:
        objsecondery = ""
        degraycompsec = ""
    try:
        objmoyen = Moyen.objects.filter(withuser=request.user.id)
        degraycompmoy = DegreyMoyenCompany.objects.filter(company__in=objmoyen)
    except:
        objmoyen = ""
        degraycompmoy = ""

    try:
        objprem = Primary.objects.filter(withuser=request.user.id)
        degraycompprem = DegreyPremCompany.objects.filter(company__in=objprem)
    except:
        objprem = ""
        degraycompprem = ""
    # الاعلام#
    try:
        primary1 = datetime.strptime(primary1, "%Y-%m-%d")
        primary2 = datetime.strptime(primary2, "%Y-%m-%d")
    except:
        pass

    # الاعلام ثانوي#
    try:
        # mediasec = MediaSec.objects.filter(date__range=[primary1, primary2]).select_related()
        test1ok = MediaSec.objects.select_related('degraycomany_id').filter(date__range=[primary1, primary2]).values('degraycomany_id','degraycomany__company__name','degraycomany__company__withprimary__username','degraycomany__nomberexist','degraycomany__spesial__name','degraycomany__name').annotate(total=Sum('nomberhisas'))
    except:
        test1ok =""

    # الاعلام متوسط#
    try:
        mediamoy = MediaMoy.objects.filter(date__range=[primary1, primary2]).values(
            'withclass_id','withclass__company__withuser__username','withclass__company__name','withclass__withdegrey__name','withclass__nomberexist').annotate(total=Sum('nomberhisas'))
    except:
        mediamoy=""


    # الاعلام ابتدائي#
    try:
        #mediapre = MediaPre.objects.filter(date__range=[primary1, primary2], withclass__in=degraycompprem)
        mediapre = MediaPre.objects.filter(date__range=[primary1, primary2]).values(
            'withclass_id','withclass__company__name','withclass__company__withuser__username','withclass__withdegrey__name','withclass__nomberexist').annotate(total=Sum('nomberhisas'))
    except:
        mediapre = ""


    #المتابعة

    try:
        motabasec = MotabaSec.objects.filter(date__range=[primary1, primary2]).values(
                'withcompany__name').annotate(study=Sum('study'), behaviorism=Sum('behaviorism'), familial=Sum('familial'), psychological=Sum('psychological'), healthy=Sum('healthy'))

    except:
        motabasec = ""

    # المتابعة متوسط

    try:
        listmota = MotabaMoy.objects.filter(date__range=[primary1, primary2]).values(
                'withcompany__name').annotate(study=Sum('study'), behaviorism=Sum('behaviorism'), familial=Sum('familial'), psychological=Sum('psychological'), healthy=Sum('healthy'))
    except:
        listmota = ""

    #خلية الاصغاء

    try:
        listingcell = ListeningCells.objects.filter(date__range=[primary1, primary2]).values('withcompany__name','date','stat','why')
    except:
        listingcell = ""



    #لجان المتابعة
    if objmoyen != "":
        try:
            followcomit = Followcommit.objects.select_related('withcompany').filter(date__range=[primary1, primary2])
        except:
            followcomit = ""
    else:
        followcomit = ""

    #اعلام الاولياء

    try:
        listilam = MediaSecParnt.objects.filter(date__range=[primary1, primary2]).values(
                'withsecondray__name','withdegrey__name','withsecondray_id','withdegrey_id').annotate(nomberhodor=Sum('nomberhodor'), nomberesteda=Sum('nomberesteda'), percent=Round2(ExpressionWrapper(Cast(F('nomberhodor')*100, FloatField())/F('nomberesteda'),
        output_field=FloatField())))
        listilame = list(listilam)
        liste = listilam.values_list('withdegrey_id', 'withsecondray_id')
        thelist = list(liste)
        q_filter = Q(*[Q(withdegrey=x, company=y) for x, y in (thelist)], _connector=Q.OR)
        ddegrycomp = DegreyCompany.objects.filter(q_filter).values('withdegrey_id', 'company_id').annotate(
            nomberetude=Sum('nomberetud'))
        ddegrycompe = list(ddegrycomp)
        listilamsec = []
        dictt = {}
        i=0
        while i < len(listilam):
            j=0
            while j < len(listilame):
                if listilame[i]['withsecondray_id'] == ddegrycompe[j]['company_id'] and listilame[i]['withdegrey_id'] == ddegrycompe[j]['withdegrey_id']:
                    dictt.update(listilame[i])
                    dictt.update(ddegrycompe[j])
                    newdict = dict(dictt)
                    listilamsec.append(newdict)
                j+=1
            i+=1
    except:
        listilamsec = ""



    #اعلا الاولياء متوسط

    try:
        medmoypar = MediaMoyParnt.objects.filter(date__range=[primary1, primary2]).values(
                'withdegry_id', 'withdegry__name', 'withcompany_id','withcompany__name','withdegry__nomberetud').annotate(nomberesteda=Sum('nomberesteda'), nomberhodor=Sum('nomberhodor'), persontage=Round2(ExpressionWrapper(Cast(F('nomberhodor')*100, FloatField())/F('nomberesteda'),
        output_field=FloatField())))
        listmedmoypar = list(medmoypar)
    except:
        listmedmoypar = []





    #اعلا الاولياء ابتدائي

    try:
        mediapremparnt = MediaPreParnt.objects.filter(date__range=[primary1, primary2]).values(
                'withdegry_id', 'withcompany_id','withcompany__name','withdegry__name','withdegry__nomberetud').annotate(nomberesteda=Sum('nomberesteda'), nomberhodor=Sum('nomberhodor'), persontage=Round2(ExpressionWrapper(Cast(F('nomberhodor')*100, FloatField())/F('nomberesteda'),
        output_field=FloatField())))
        dataprem = list(mediapremparnt)
    except:
        dataprem = []


    # ثانوي الوثائق الاعلامية
    try:
        filemediasec = FileMediaSec.objects.filter(date__range=[primary1, primary2]).values(
                'withcompany__id', 'withdegry__id', 'type_id','withdegry__name', 'withcompany__name', 'type__name').annotate(count=Count('type_id'))
    except:
        filemediasec = ""


    # متوسط الوثائق الاعلامية

    try:
        filemediamoy = FileMediaMoy.objects.filter(date__range=[primary1, primary2]).values(
                'withcompany_id', 'withdegry_id', 'type_id','withdegry__name', 'withcompany__name', 'type__name').annotate(count=Count('type_id'))
    except:
        filemediamoy = ""


    # نشاطات اخرى ثانوي
    try:
        otheractivesec = OtherActiv.objects.filter(withcompany1__isnull=False,date__range=[primary1, primary2]).values(
                'name__name','withcompany1__name').annotate(count =Count('name'))
    except:
        otheractivesec = ""


    # نشاطات اخرى متوسط
    try:
        otheractivemoy = OtherActiv.objects.filter(withcompany2__isnull=False,date__range=[primary1, primary2]).values(
                'name__name','withcompany2__name').annotate(count =Count('name'))
    except:
        otheractivemoy = ""

    # نشاطات اخرى ابتدائي
    try:
        otheractiveprem = OtherActiv.objects.filter(withcompany3__isnull=False,date__range=[primary1, primary2]).values(
                'name__name','withcompany3__name').annotate(count =Count('name'))
    except:
        otheractiveprem = ""

    # نشاطات اخرى عامة
    try:
        otheract = OtherActiv.objects.filter(withcompany1= None, withcompany2= None, withcompany3= None, date__range=[primary1, primary2]).values(
                'name__name','withuser__username').annotate(count =Count('name'))
    except:
        otheract = ""

    context = {"listmediasec":test1ok, "listilamsec":listilamsec, "otheract":otheract, "otheractiveprem":otheractiveprem,"otheractivesec":otheractivesec, "otheractivemoy":otheractivemoy, "listmedfilesec":filemediasec,"listmedfilemoy":filemediamoy ,"dataprem":dataprem ,"datamoypar":listmedmoypar, "listmediamoy":mediamoy, "listmediapre":mediapre, "primary2":primary2, "primary1":primary1, "motabasec":motabasec, "listmota":listmota, "listingcell":listingcell, "followcomit":followcomit}
    return render(request, template_name="hod_template/date_rangeall_template.html",context=context)


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

