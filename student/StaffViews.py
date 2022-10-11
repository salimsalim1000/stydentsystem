from datetime import datetime
import json


from django.contrib import messages
from django.db.models.functions import Cast
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from student.models import Subjects, SessionYearModel, Students, Attendance, AttendanceReport, LeaveRaportStaff, Staffs, \
    FeedBackStaff, CustomUser, Courses, Primary, DegreyPrem, DegreyPremCompany, Moyen, DegreyMoyen, DegreyMoyenCompany, \
    Secondary, DegreyCompany, Degrey, Spesial, MediaSec, MediaMoy, MediaPre, ListeningCells, Followcommit, MotabaSec, \
    MotabaMoy, MediaSecParnt, MediaMoyParnt, MediaPreParnt, ActiviteName, OtherActiv, TypeFileMedia, FileMediaSec, \
    FileMediaMoy, Mostachar
from django.core import serializers
from django.db.models import Sum, Count, FloatField, ExpressionWrapper, F, Q
from django.db.models import Func


class Round2(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 2)'

#
def mostachar_home(request):
    return render(request, template_name="staff_template/staff_home_template.html")


def add_degreyprem(request):
    companys = Primary.objects.select_related('withuser').filter(withuser=request.user.id)
    company_list = companys.values_list('id', flat=1)
    degray = DegreyPrem.objects.all()
    degrycomanyexist = DegreyPremCompany.objects.filter(company__in=company_list)
    context = {"companys": companys, "degray": degray, "degrycomanyexist": degrycomanyexist}
    return render(request, template_name="staff_template/add_degreypremary_template.html", context=context)


def add_degreyprem_save(request):
    if request.method != "POST":
        messages.error(request, "method not allow")
        return HttpResponseRedirect(reverse("add_degreyprem"))
    else:
        primary = request.POST.get("primary")
        degry = request.POST.get("degry")
        numetud = request.POST.get("numetud")
        numetudex = request.POST.get("numetudex")
        femal = request.POST.get("femal")
        reatrap = request.POST.get("reatrap")
        try:
            degrys = DegreyPrem.objects.get(id=degry)
            prim = Primary.objects.get(id=primary)
        except:
            messages.error(request, "لا يوجد مؤسسة مسندة لك")
            return HttpResponseRedirect(reverse("add_degreyprem"))

        try:
            DegreyPremCompany.objects.get(withdegrey=degrys, company=prim)
            messages.error(request, "موجود بالفعل")
            return HttpResponseRedirect(reverse("add_degreyprem"))
        except:
            try:
                model = DegreyPremCompany.objects.create(withdegrey=degrys, company=prim, name=degrys.name)
                model.nomberetud = numetud
                model.nomberexist = numetudex
                model.femail = femal
                model.reatrap = reatrap
                model.save()
                messages.success(request, "تم اضافة المستوى بنجاح")
                return HttpResponseRedirect(reverse("add_degreyprem"))
            except:
                messages.error(request, "خطأ غير معروف")
                return HttpResponseRedirect(reverse("add_degreyprem"))


def add_degreymoyene(request):
    companys = Moyen.objects.filter(withuser=request.user.id)
    company_list = companys.values_list('id', flat=1)
    degray = DegreyMoyen.objects.all()
    degrycomanyexist = DegreyMoyenCompany.objects.select_related("company").filter(company__in=company_list)
    context = {"companys": companys, "degray": degray, "degrycomanyexist": degrycomanyexist}
    return render(request, template_name="staff_template/add_degreymoyen_template.html", context=context)


def add_degreymoyene_save(request):
    if request.method != "POST":
        messages.error(request, "method not allow")
        return HttpResponseRedirect(reverse("add_degreymoyene"))
    else:
        primary = request.POST.get("primary")
        degry = request.POST.get("degry")
        numetud = request.POST.get("numetud")
        numetudex = request.POST.get("numetudex")
        femal = request.POST.get("femal")
        reatrap = request.POST.get("reatrap")
        try:
            degrys = DegreyMoyen.objects.get(id=degry)
            prim = Moyen.objects.get(id=primary)
        except:
            messages.error(request, "لا يوجد مؤسسة مسندة لك")
            return HttpResponseRedirect(reverse("add_degreymoyene"))
        try:
            DegreyMoyenCompany.objects.get(withdegrey=degrys, company=prim)
            messages.error(request, "موجود بالفعل")
            return HttpResponseRedirect(reverse("add_degreymoyene"))
        except:
            try:
                model = DegreyMoyenCompany.objects.create(withdegrey=degrys, company=prim, name=degrys.name)
                model.nomberetud = numetud
                model.nomberexist = numetudex
                model.femail = femal
                model.reatrap = reatrap
                model.save()
                messages.success(request, "تم اضافة المستوى بنجاح")
                return HttpResponseRedirect(reverse("add_degreymoyene"))
            except:
                messages.error(request, "خطأ غير معروف")
                return HttpResponseRedirect(reverse("add_degreymoyene"))


def add_degresecondarye(request):
    try:
        companys = Secondary.objects.get(withprimary=request.user.id)
    except Secondary.DoesNotExist:
        companys = None

    degray = Degrey.objects.all()
    spesialtes = Spesial.objects.all()
    degrycomanyexistt = DegreyCompany.objects.select_related("spesial").filter(company=companys)
    listdegeryall = list(degrycomanyexistt)

    context = {"companys": companys, "degray": degray, "degrycomanyexistt": degrycomanyexistt, "spesialtes": spesialtes}
    return render(request, template_name="staff_template/add_degresecondry_template.html", context=context)


def add_degresecondarye_save(request):
    if request.method != "POST":
        messages.error(request, "method not allow")
        return HttpResponseRedirect(reverse("add_degresecondarye"))
    else:
        degry = request.POST.get("degry")
        spesial = request.POST.get("spesialte")
        numetud = request.POST.get("numetud")
        numetudex = request.POST.get("numetudex")
        femal = request.POST.get("femal")
        reatrap = request.POST.get("reatrap")
        try:
            degrys = Degrey.objects.get(id=degry)
            prim = Secondary.objects.get(withprimary=request.user.id)
            spesials = Spesial.objects.get(id=spesial)
        except:
            messages.error(request, "لا يوجد مؤسسة مسندة لك")
            return HttpResponseRedirect(reverse("add_degresecondarye"))

        try:
            DegreyCompany.objects.get(withdegrey=degrys, company=prim, spesial=spesials)
            messages.error(request, "موجود بالفعل")
            return HttpResponseRedirect(reverse("add_degresecondarye"))
        except:
            try:
                model = DegreyCompany.objects.create(withdegrey=degrys, company=prim, spesial=spesials,
                                                     name=degrys.name)
                model.nomberetud = numetud
                model.nomberexist = numetudex
                model.femail = femal
                model.reatrap = reatrap
                model.save()
                messages.success(request, "تم اضافة المستوى بنجاح")
                return HttpResponseRedirect(reverse("add_degresecondarye"))
            except:
                messages.error(request, "خطأ غير معروف")
                return HttpResponseRedirect(reverse("add_degresecondarye"))


@csrf_exempt
def get_spesialite(request):
    degryid = request.POST.get("degryid")
    spesialobj = Spesial.objects.filter(degrey=degryid)
    list_degray = []
    for spes in spesialobj:
        data_small = {'id': spes.id, 'name': spes.name}
        list_degray.append(data_small)
    return JsonResponse(json.dumps(list_degray), content_type="application/json", safe=False)


def ilam_seconder(request):
    try:
        companys = Secondary.objects.get(withprimary=request.user.id)
    except Secondary.DoesNotExist:
        companys = None

    degray = Degrey.objects.all()
    spesialtes = Spesial.objects.all()
    degrycomanyexistt = DegreyCompany.objects.select_related("spesial").filter(company=companys)

    context = {"companys": companys, "degray": degray, "degrycomanyexistt": degrycomanyexistt, "spesialtes": spesialtes}
    return render(request, template_name="staff_template/add_ilamsecond_template.html", context=context)


@csrf_exempt
def ilam_seconder_save(request):
    id = request.POST.get("id")
    nomber = request.POST.get("nomber")
    date = request.POST.get("date")
    the_date = datetime.strptime(date, "%Y-%m-%d")
    try:
        degrycomp = DegreyCompany.objects.get(id=id)
        model = MediaSec.objects.create(degraycomany=degrycomp, nomberhisas=nomber, date=the_date)
        model.save()
        data = ""
    except:
        data = ""
    return JsonResponse(data, content_type="application/json", safe=False)


def ilam_moyen(request):
    try:
        companys = Moyen.objects.filter(withuser=request.user.id)
    except Moyen.DoesNotExist:
        companys = None

    degray = DegreyMoyen.objects.all()
    degrycomanyexistt = DegreyMoyenCompany.objects.select_related("company").filter(company__in=companys)

    context = {"companys": companys, "degray": degray, "degrycomanyexistt": degrycomanyexistt}
    return render(request, template_name="staff_template/add_ilammoyen_template.html", context=context)


@csrf_exempt
def ilam_moyen_save(request):
    id = request.POST.get("id")
    nomber = request.POST.get("nomber")
    date = request.POST.get("date")
    the_date = datetime.strptime(date, "%Y-%m-%d")
    try:
        degrycomp = DegreyMoyenCompany.objects.get(id=id)
        model = MediaMoy.objects.create(withclass=degrycomp, nomberhisas=nomber, date=the_date)
        model.save()
        data = ""
    except:
        data = ""
    return JsonResponse(data, content_type="application/json", safe=False)


def ilam_prem(request):
    try:
        companys = Primary.objects.filter(withuser=request.user.id)
    except Moyen.DoesNotExist:
        companys = None
    degray = DegreyPrem.objects.all()
    degrycomanyexistt = DegreyPremCompany.objects.filter(company__in=companys)

    context = {"companys": companys, "degray": degray, "degrycomanyexistt": degrycomanyexistt}
    return render(request, template_name="staff_template/add_ilamprem_template.html", context=context)


@csrf_exempt
def ilam_prem_save(request):
    id = request.POST.get("id")
    nomber = request.POST.get("nomber")
    date = request.POST.get("date")
    the_date = datetime.strptime(date, "%Y-%m-%d")
    try:
        degrycomp = DegreyPremCompany.objects.get(id=id)
        model = MediaPre.objects.create(withclass=degrycomp, nomberhisas=nomber, date=the_date)
        model.save()
        data = ""
    except:
        data = ""
    return JsonResponse(data, content_type="application/json", safe=False)


def cell_listen(request):
    try:
        companys= Moyen.objects.filter(withuser=request.user.id)
        print(companys)
    except:
        companys=""
    try:
        secondarys = Secondary.objects.get(withprimary=request.user.id)
        print(secondarys)
    except:
        secondarys = 0
    try:
        listeningcells = ListeningCells.objects.get(withcompany=secondarys)
        print(listeningcells)
    except:
        listeningcells = ""
    try:
        followcommit = Followcommit.objects.filter(withcompany__in=companys)
        print(followcommit)

    except:
        followcommit = ""


    context={"companys": companys, "secondarys": secondarys, "listeningcells":listeningcells, "followcommit":followcommit}
    return render(request, template_name="staff_template/add_celllistenand_template.html",context=context)


def cell_coumit(request):
    try:
        companys= Moyen.objects.filter(withuser=request.user.id)
        print(companys)
    except:
        companys=""


    try:
        followcommit = Followcommit.objects.filter(withcompany__in=companys)
        print(followcommit)

    except:
        followcommit = ""


    context={"companys": companys, "followcommit":followcommit}
    return render(request, template_name="staff_template/add_coumit_template.html",context=context)

@csrf_exempt
def save_cell(request):
    idcompany = request.POST.get("idcompany")
    date = request.POST.get("date")
    the_date = datetime.strptime(date, "%Y-%m-%d")
    try:
        idobj= Secondary.objects.get(id=idcompany)
        listeningcells= ListeningCells.objects.get(withcompany=idobj)
        listeningcells.date= the_date
        listeningcells.why = ""
        listeningcells.stat= "1"
        listeningcells.save()
        data = ""
    except:
        data = ""
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def save_cellnoexist(request):
    try:
        idcompany = request.POST.get("idcompany")
        why = request.POST.get("why")
        idobj= Secondary.objects.get(id=idcompany)
        listeningcells = ListeningCells.objects.get(withcompany=idobj)
        listeningcells.why = why
        listeningcells.stat= "0"
        listeningcells.save()
        data = ""
    except:
        data = ""
    return JsonResponse(data, content_type="application/json", safe=False)

@csrf_exempt
def cell_moyen_save(request):
    try:
        id = request.POST.get("id")
        date = request.POST.get("date")
        the_date = datetime.strptime(date, "%Y-%m-%d")
        idobj = Moyen.objects.get(id=id)
        followcommit = Followcommit.objects.get(withcompany=idobj)
        followcommit.stat = "1"
        followcommit.date = the_date
        followcommit.save()
        data = ""
    except:
        data = ""
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def nocell_moyen_save(request):
    try:
        id = request.POST.get("id")
        way = request.POST.get("way")
        idobj = Moyen.objects.get(id=id)
        followcommit = Followcommit.objects.get(withcompany=idobj)
        followcommit.way = way
        followcommit.stat = "0"
        followcommit.save()
        data = ""
    except:
        data = ""
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def save_motaba(request):
    try:
        idcompany = request.POST.get("idcompany")
        helth = request.POST.get("helth")
        behaviorism = request.POST.get("behaviorism")
        study = request.POST.get("study")
        familial = request.POST.get("familial")
        psychological = request.POST.get("psychological")
        date = request.POST.get("date")
        the_date = datetime.strptime(date, "%Y-%m-%d").date()
        idobj = Secondary.objects.get(id=idcompany)
        motabasec = MotabaSec.objects.create(withcompany=idobj)
        motabasec.withcompany = idobj
        if helth:
            motabasec.healthy = helth
        if behaviorism:
            motabasec.behaviorism = behaviorism
        if study:
            motabasec.study = study
        if familial:
            motabasec.familial = familial
        if psychological:
            motabasec.psychological = psychological
        motabasec.date = the_date
        motabasec.save()
        data = ""
    except:
        data = ""
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def save_motaba_moy(request):
    try:
        idcompany = request.POST.get("id")
        helth = request.POST.get("helth")
        behaviorism = request.POST.get("behaviorism")
        study = request.POST.get("study")
        familial = request.POST.get("familial")
        psychological = request.POST.get("psychological")
        date = request.POST.get("date")
        the_date = datetime.strptime(date, "%Y-%m-%d").date()
        idobj = Moyen.objects.get(id=idcompany)
        motabamoy = MotabaMoy.objects.create(withcompany=idobj)
        motabamoy.withcompany = idobj
        if helth:
            motabamoy.healthy = helth
        if behaviorism:
            motabamoy.behaviorism = behaviorism
        if study:
            motabamoy.study = study
        if familial:
            motabamoy.familial = familial
        if psychological:
            motabamoy.psychological = psychological
        motabamoy.date = the_date
        motabamoy.save()
        data = ""
    except:
        data = ""
    return JsonResponse(data, content_type="application/json", safe=False)


def ilam_parents(request):
    try:
        companys = Secondary.objects.get(withprimary=request.user.id)
    except Secondary.DoesNotExist:
        companys = None
    degray = Degrey.objects.all()
    degraylist = degray.values("id","name")
    degraylist = list(degraylist)
    data_list = []
    mydict = {}
    for key in degraylist:
        degrycomanyexistt = DegreyCompany.objects.filter(withdegrey=key["id"], company=companys).aggregate(Sum('nomberetud'))
        data_list.append(degrycomanyexistt)
        mydict= degrycomanyexistt.update(key)

    print(data_list)
    degrycomanyexistt = DegreyCompany.objects.filter(withdegrey__in=degray)
    context = {"companys": companys, "degray": degray, "degrycomanyexistt": degrycomanyexistt,"degraylist":degraylist, "data_list":data_list}
    return render(request, template_name="staff_template/add_ilamsecondparnts_template.html",  context=context)


@csrf_exempt
def save_ilam_parnts(request):
    try:
        iddegry = request.POST.get("id")
        ist = request.POST.get("ist")
        come = request.POST.get("come")
        date = request.POST.get("date")
        the_date = datetime.strptime(date, "%Y-%m-%d").date()
        idobj = Secondary.objects.get(withprimary=request.user.id)
        degryobj = Degrey.objects.get(id=iddegry)
        mediasecparnt = MediaSecParnt.objects.create(withdegrey=degryobj, withsecondray=idobj)
        if ist:
            mediasecparnt.nomberesteda = ist
        if come:
            mediasecparnt.nomberhodor = come

        mediasecparnt.date = the_date
        mediasecparnt.save()
        data = ""
    except:
        data = ""
    return JsonResponse(data, content_type="application/json", safe=False)


def ilam_parents_moy(request):
    try:
        companys = Moyen.objects.filter(withuser=request.user.id)
    except Moyen.DoesNotExist:
        companys = None
    degraycomp = DegreyMoyenCompany.objects.filter(company__in=companys)
    degraylist = degraycomp.values()
    degraylist = list(degraylist)
    context = {"companys": companys, "degraylist": degraylist}
    return render(request, template_name="staff_template/add_ilammoyenparnts_template.html", context=context)


@csrf_exempt
def save_ilam_parentsmoy(request):
    try:
        iddegrycomp = request.POST.get("iddegrycomp")
        ist = request.POST.get("ist")
        come = request.POST.get("come")
        date = request.POST.get("date")
        the_date = datetime.strptime(date, "%Y-%m-%d")
        degryobj = DegreyMoyenCompany.objects.get(id=iddegrycomp)
        idobj = Moyen.objects.get(id=degryobj.company.id)
        mediamoyparnt = MediaMoyParnt.objects.create(withdegry=degryobj, withcompany=idobj, nomberesteda=ist, nomberhodor=come, date=the_date)
        mediamoyparnt.save()
        data = ""
    except:
        data = ""

    return JsonResponse(data, content_type="application/json", safe=False)


def ilam_parents_prem(request):
    try:
        companys = Primary.objects.filter(withuser=request.user.id)
    except Primary.DoesNotExist:
        companys = None
    degraycomp = DegreyPremCompany.objects.all()
    degraylist = degraycomp.values()
    degraylist = list(degraylist)
    context = {"companys": companys, "degraylist": degraylist}
    return render(request, template_name="staff_template/add_ilampremparnts_template.html", context=context)


@csrf_exempt
def save_ilam_parntsprem(request):
    try:
        iddegrycomp = request.POST.get("iddegrycomp")
        ist = request.POST.get("ist")
        come = request.POST.get("come")
        date = request.POST.get("date")
        the_date = datetime.strptime(date, "%Y-%m-%d")
        degryobj = DegreyPremCompany.objects.get(id=iddegrycomp)
        idobj = Primary.objects.get(id=degryobj.company.id)
        mediamoyparnt = MediaPreParnt.objects.create(withdegry=degryobj, withcompany=idobj, nomberesteda=ist,
                                                         nomberhodor=come, date=the_date)
        mediamoyparnt.save()
        data = ""
    except:
        data = ""

    return JsonResponse(data, content_type="application/json", safe=False)


def other_activite(request):
    try:
        prymerys = Primary.objects.filter(withuser=request.user.id)
    except:
        prymerys = ""

    try:
        companys= Moyen.objects.filter(withuser=request.user.id)
    except:
        companys=""
    try:
        secondarys = Secondary.objects.get(withprimary=request.user.id)
    except:
        secondarys = ""
    allactivite = ActiviteName.objects.all()
    context = {"prymerys": prymerys, "companys":companys, "secondarys":secondarys, "allactivite":allactivite}
    return render(request, template_name="staff_template/add_otheractivite_template.html", context=context)

def other_activitemoy(request):
    try:
        prymerys = Primary.objects.filter(withuser=request.user.id)
    except:
        prymerys = ""

    try:
        companys= Moyen.objects.filter(withuser=request.user.id)
    except:
        companys=""

    allactivite = ActiviteName.objects.all()
    context = {"prymerys": prymerys, "companys":companys, "allactivite":allactivite}
    return render(request, template_name="staff_template/add_otheractivitemoy_template.html", context=context)
@csrf_exempt
def save_activeite_sec(request):
    try:
        idcompany = request.POST.get("idcompany")
        why = request.POST.get("why")
        options = request.POST.get("options")
        date = request.POST.get("date")
        the_date = datetime.strptime(date, "%Y-%m-%d")
        secondarys = Secondary.objects.get(id=idcompany)
        active = ActiviteName.objects.get(id=options)
        userobj = CustomUser.objects.get(id=request.user.id)
        activaite = OtherActiv.objects.create(withuser=userobj, withcompany1=secondarys, name=active, note=why, date=the_date)
        activaite.save()
        data = ""
    except:
        data = ""
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def save_activeite_moy(request):
    try:
        idcompany = request.POST.get("idmoy")
        textmoy = request.POST.get("textmoy")
        optionmoy = request.POST.get("optionmoy")
        date = request.POST.get("date")
        the_date = datetime.strptime(date, "%Y-%m-%d")
        moyens = Moyen.objects.get(id=idcompany)
        active = ActiviteName.objects.get(id=optionmoy)
        userobj = CustomUser.objects.get(id=request.user.id)
        activaite = OtherActiv.objects.create(withuser=userobj, withcompany2=moyens, name=active, note=textmoy, date=the_date)
        activaite.save()
        data = ""
    except:
        data = ""
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def save_activeite_prem(request):
    try:
        idcompany = request.POST.get("id")
        way = request.POST.get("way")
        optionprem = request.POST.get("optionprem")
        date = request.POST.get("date")
        the_date = datetime.strptime(date, "%Y-%m-%d")
        pream = Primary.objects.get(id=idcompany)
        active = ActiviteName.objects.get(id=optionprem)
        userobj = CustomUser.objects.get(id=request.user.id)
        activaite = OtherActiv.objects.create(withuser=userobj, withcompany3=pream, name=active, note=way, date=the_date)
        activaite.save()
        data = ""
    except:
        data = ""
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def save_activeite_any(request):
    try:
        why = request.POST.get("why")
        options = request.POST.get("options")
        date = request.POST.get("date")
        the_date = datetime.strptime(date, "%Y-%m-%d")
        active = ActiviteName.objects.get(id=options)
        userobj = CustomUser.objects.get(id=request.user.id)
        activaite = OtherActiv.objects.create(withuser=userobj, name=active, note=why, date=the_date)
        activaite.save()
        data = ""
    except:
        data = ""
    return JsonResponse(data, content_type="application/json", safe=False)


def add_file_media(request):
    try:
        companys= Moyen.objects.filter(withuser=request.user.id)
    except:
        companys=""
    degraycomp = DegreyMoyenCompany.objects.all()
    degraylistmoy = degraycomp.values()
    degraylistmoy = list(degraylistmoy)
    try:
        secondarys = Secondary.objects.get(withprimary=request.user.id)
    except Secondary.DoesNotExist:
        secondarys = None
    degray = Degrey.objects.all()
    degraylist = degray.values("id", "name")
    degraylist = list(degraylist)
    data_list = []

    for key in degraylist:
        degrycomanyexistt = DegreyCompany.objects.filter(withdegrey=key["id"]).aggregate(Sum('nomberetud'))
        data_list.append(degrycomanyexistt)
        degrycomanyexistt.update(key)


    typefile = TypeFileMedia.objects.all()
    context = {"companys":companys, "secondarys":secondarys, "typefile":typefile, "degray": degray, "data_list":data_list, "degraylistmoy": degraylistmoy}
    return render(request, template_name="staff_template/add_mediafile_template.html", context=context)

def add_file_mediamoy(request):
    try:
        companys= Moyen.objects.filter(withuser=request.user.id)
    except:
        companys=""
    degraycomp = DegreyMoyenCompany.objects.all()
    degraylistmoy = degraycomp.values()
    degraylistmoy = list(degraylistmoy)


    typefile = TypeFileMedia.objects.all()
    context = {"companys":companys, "typefile":typefile, "degraylistmoy": degraylistmoy}
    return render(request, template_name="staff_template/add_mediafilemoy_template.html", context=context)
@csrf_exempt
def add_mediasec_save(request):
    try:
        idcompany = request.POST.get("idcompany")
        iddegry = request.POST.get("iddegry")
        why = request.POST.get("why")
        options = request.POST.get("options")
        date = request.POST.get("date")
        the_date = datetime.strptime(date, "%Y-%m-%d")
        typefile = TypeFileMedia.objects.get(id=options)
        iddegry = Degrey.objects.get(id=iddegry)
        secobj = Secondary.objects.get(withprimary=request.user.id)
        activaite = FileMediaSec.objects.create(withcompany= secobj, withdegry= iddegry, type= typefile, titel= why, date= the_date)
        activaite.save()
        data = ""
    except:
        data = ""
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def add_mediamoyen_save(request):
    try:
        iddegrycomp = request.POST.get("iddegrycomp")
        idcomp = request.POST.get("idcomp")
        why = request.POST.get("why")
        options = request.POST.get("options")
        date = request.POST.get("date")
        the_date = datetime.strptime(date, "%Y-%m-%d")
        typefile = TypeFileMedia.objects.get(id=options)
        iddegrycomp = DegreyMoyenCompany.objects.get(id=iddegrycomp)
        moyobj = Moyen.objects.get(id=idcomp)
        activaite = FileMediaMoy.objects.create(withcompany=moyobj, withdegry=iddegrycomp, type=typefile, titel=why, date=the_date)
        activaite.save()
        data = ""
    except:
        data = ""
    return JsonResponse(data, content_type="application/json", safe=False)


def date_range_all(request):
    return render(request, template_name="staff_template/date_range_template.html")


def date_range_all_get(request):
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


    try:
        mediasec = MediaSec.objects.select_related('degraycomany','degraycomany__company','degraycomany__spesial').filter(date__range=[primary1, primary2], degraycomany__in=degraycompsec)
    except:
        mediasec=""
    try:
        mediamoy = MediaMoy.objects.select_related('withclass','withclass__company').filter(date__range=[primary1, primary2], withclass__in=degraycompmoy)
    except:
        mediamoy=""
    try:
        mediapre = MediaPre.objects.select_related('withclass','withclass__company').filter(date__range=[primary1, primary2], withclass__in=degraycompprem)
    except:
        mediapre=""

    #المتابعة
    if objsecondery != "":
        try:
            motabasec = MotabaSec.objects.select_related('withcompany').filter(withcompany=objsecondery, date__range=[primary1, primary2])
        except:
            motabasec = ""
    else:
        motabasec = ""

    if objmoyen != "":
        try:
            motabamoy = MotabaMoy.objects.select_related('withcompany').filter(withcompany__in=objmoyen, date__range=[primary1, primary2])
        except:
            motabamoy = ""
    else:
        motabamoy = ""

    #خلية الاصغاء
    if objsecondery != "":
        try:
            listingcell = ListeningCells.objects.get(withcompany=objsecondery, date__range=[primary1, primary2])
        except:
            listingcell = ""
    else:
        listingcell = ""


    #لجان المتابعة
    if objmoyen != "":
        try:
            followcomit = Followcommit.objects.select_related('withcompany').filter(withcompany__in=objmoyen, date__range=[primary1, primary2])
        except:
            followcomit = ""
    else:
        followcomit = ""

    #اعلام الاولياء
    if objsecondery != "":
        try:
            mediasecparnt = MediaSecParnt.objects.filter(withsecondray=objsecondery, date__range=[primary1, primary2]).values('id', 'withdegrey__name', 'withdegrey__id', 'withsecondray__id', 'withsecondray__name', 'date','nomberesteda','nomberhodor').annotate(persontage=Round2(ExpressionWrapper(Cast(F('nomberhodor')*100, FloatField())/F('nomberesteda'),
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

        except:
            data = ""
    else:
        data = ""

    #اعلا الاولياء متوسط
    if objmoyen != "":
        try:
            mediamoyparnt = MediaMoyParnt.objects.select_related('withdegry','withcompany').order_by('withcompany_id','withdegry_id').filter(withcompany__in=objmoyen,
                                                                                                   date__range=[primary1, primary2]).annotate(persontage=Round2(ExpressionWrapper(Cast(F('nomberhodor')*100, FloatField())/F('nomberesteda'),
        output_field=FloatField())))
        except:
            mediamoyparnt = ""
    else:
        mediamoyparnt = ""


    #اعلا الاولياء ابتدائي
    if objprem != "":
        try:
            dataprem = MediaPreParnt.objects.select_related('withdegry','withcompany').order_by('withcompany_id','withdegry_id').filter(withcompany__in=objprem,
                                                                                                    date__range=[primary1, primary2]).annotate(persontage=Round2(ExpressionWrapper(Cast(F('nomberhodor')*100, FloatField())/F('nomberesteda'),
        output_field=FloatField())))
        except:
            dataprem = ""
    else:
        dataprem = ""

    # ثانوي الوثائق الاعلامية
    if objsecondery != "":
        try:
            filemediasec = FileMediaSec.objects.select_related('type','withdegry').filter(withcompany=objsecondery, date__range=[primary1, primary2])

        except:
            filemediasec = ""
    else:
        filemediasec = ""

    # متوسط الوثائق الاعلامية
    if objmoyen != "":
        try:
            filemediamoy = FileMediaMoy.objects.select_related('type','withdegry','withcompany').filter(withcompany__in=objmoyen, date__range=[primary1, primary2])
        except:
            filemediamoy = ""
    else:
        filemediamoy = ""

    # نشاطات اخرى ثانوي
    try:
        otheractivesec = OtherActiv.objects.select_related('name').filter(withcompany1=objsecondery, date__range=[primary1, primary2])
    except:
        otheractivesec = ""


    # نشاطات اخرى متوسط
    try:
        otheractivemoy = OtherActiv.objects.select_related('withcompany2','name').filter(withcompany2__in=objmoyen, date__range=[primary1, primary2])
    except:
        otheractivemoy = ""

    # نشاطات اخرى ابتدائي
    try:
        otheractiveprem = OtherActiv.objects.select_related('withcompany3','name').filter(withcompany3__in=objprem, date__range=[primary1, primary2])
    except:
        otheractiveprem = ""

    # نشاطات اخرى عامة
    try:
        otheract = OtherActiv.objects.select_related('name').filter(withcompany1= None, withcompany2= None, withcompany3= None, date__range=[primary1, primary2])
    except:
        otheract = ""

    context = {"mediamoyparnt":mediamoyparnt,"data":data, "otheract":otheract, "otheractiveprem":otheractiveprem,"otheractivesec":otheractivesec, "otheractivemoy":otheractivemoy, "filemediasec":filemediasec,"filemediamoy":filemediamoy,"dataprem":dataprem, "mediasec":mediasec, "mediamoy":mediamoy, "mediapre":mediapre, "primary1":primary1, "primary2":primary2, "motabasec":motabasec, "motabamoy":motabamoy, "listingcell":listingcell, "followcomit":followcomit}
    return render(request, template_name="staff_template/date_range_template.html",context=context)

#hالجميع الكلي
def date_range_fulle(request):
    return render(request, template_name="staff_template/date_rangeall_template.html")

#hالجميع الكلي
def date_range_fulle_get(request):
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
        mediasec = MediaSec.objects.filter(date__range=[primary1, primary2], degraycomany__in=degraycompsec).values('degraycomany_id','degraycomany__company__name','degraycomany__nomberexist','degraycomany__spesial__name','degraycomany__name').annotate(total=Sum('nomberhisas'))
        mediasec=list(mediasec)
    except:
        mediasec=""

    #print(listmediasec)

    # الاعلام متوسط#
    try:
        mediamoy = MediaMoy.objects.select_related().filter(date__range=[primary1, primary2], withclass__in=degraycompmoy).values(
            'withclass_id','withclass__company__name','withclass__withdegrey__name','withclass__nomberexist').annotate(total=Sum('nomberhisas'))
        listmediamoy=list(mediamoy)
    except:
        listmediamoy=""
    # print(listmediamoy)

    # الاعلام ابتدائي#
    try:
        mediapre = MediaPre.objects.filter(date__range=[primary1, primary2], withclass__in=degraycompprem).values(
            'withclass_id','withclass__company__name','withclass__withdegrey__name','withclass__nomberexist').annotate(total=Sum('nomberhisas'))
        listmediapre=list(mediapre)
    except:
        listmediapre = ""


    #المتابعة
    if objsecondery != "":
        try:
            motasec = MotabaSec.objects.filter(date__range=[primary1, primary2], withcompany=objsecondery).values(
                'withcompany_id','withcompany__name').annotate(study=Sum('study'), behaviorism=Sum('behaviorism'), familial=Sum('familial'), psychological=Sum('psychological'), healthy=Sum('healthy'))
        except:
            motasec = ''
    else:
        motasec = ''
    # المتابعة متوسط
    if objmoyen != "":
        try:
            listmota = MotabaMoy.objects.filter(date__range=[primary1, primary2], withcompany__in=objmoyen).values(
                'withcompany_id','withcompany__name').annotate(study=Sum('study'), behaviorism=Sum('behaviorism'), familial=Sum('familial'), psychological=Sum('psychological'), healthy=Sum('healthy'))
            listmota = list(listmota)
        except:
            listmota = ""
    else:
        listmota = ""

    #خلية الاصغاء
    if objsecondery != "":
        try:
            listingcell = ListeningCells.objects.get(withcompany=objsecondery, date__range=[primary1, primary2])
        except:
            listingcell = ""
    else:
        listingcell = ""


    #لجان المتابعة
    if objmoyen != "":
        try:
            followcomit = Followcommit.objects.filter(withcompany__in=objmoyen, date__range=[primary1, primary2])
        except:
            followcomit = ""
    else:
        followcomit = ""

    #اعلام الاولياء
    if objsecondery != "":
        try:
            listilam = MediaSecParnt.objects.select_related().filter(withsecondray=objsecondery, date__range=[primary1, primary2]).values(
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
    else:
        listilamsec = ""




    #اعلا الاولياء متوسط
    if objmoyen != "":
        try:

            medmoypar = MediaMoyParnt.objects.select_related().filter(withcompany__in=objmoyen, date__range=[primary1, primary2]).values(
                'withdegry_id', 'withdegry__name', 'withcompany_id','withcompany__name','withdegry__nomberetud').annotate(nomberesteda=Sum('nomberesteda'), nomberhodor=Sum('nomberhodor'), persontage=Round2(ExpressionWrapper(Cast(F('nomberhodor')*100, FloatField())/F('nomberesteda'),
        output_field=FloatField())))
            datamoypar = list(medmoypar)
        except:

            datamoypar = []
    else:

        datamoypar = []




    #اعلا الاولياء ابتدائي
    if objprem != "":
        try:
            mediapremparnt = MediaPreParnt.objects.select_related().filter(withcompany__in=objprem, date__range=[primary1, primary2]).values(
                'withdegry_id', 'withcompany_id','withcompany__name','withdegry__name','withdegry__nomberetud').annotate(nomberesteda=Sum('nomberesteda'), nomberhodor=Sum('nomberhodor'), persontage=Round2(ExpressionWrapper(Cast(F('nomberhodor')*100, FloatField())/F('nomberesteda'),
        output_field=FloatField())))
            dataprem = list(mediapremparnt)
        except:
            dataprem = []
    else:
        dataprem = []

    # ثانوي الوثائق الاعلامية
    if objsecondery != "":
        try:
            filemediasec = FileMediaSec.objects.select_related('titel').filter(withcompany=objsecondery, date__range=[primary1, primary2]).values(
                'withcompany__id', 'withdegry__id', 'type_id','withdegry__name', 'withcompany__name', 'type__name').annotate(count=Count('type_id'))
            listmedfilesec = list(filemediasec)
        except:
            listmedfilesec = ""
    else:
        listmedfilesec = ""

    # متوسط الوثائق الاعلامية
    if objmoyen != "":
        try:
            filemediamoy = FileMediaMoy.objects.filter(withcompany__in=objmoyen, date__range=[primary1, primary2]).values(
                'withcompany__id', 'withdegry__id', 'type_id','withdegry__name', 'withcompany__name', 'type__name').annotate(count=Count('type_id'))
            listmedfilemoy = list(filemediamoy)
        except:
            listmedfilemoy = ""
    else:
        listmedfilemoy = ""

    # نشاطات اخرى ثانوي
    try:
        otheractivesec = OtherActiv.objects.filter(withcompany1=objsecondery, date__range=[primary1, primary2]).values(
                'withcompany1_id','name__name').annotate(count=Count('name'))
        otheractivesec = list(otheractivesec)
    except:
        otheractivesec = ""


    # نشاطات اخرى متوسط
    try:
        otheractivemoy = OtherActiv.objects.filter(withcompany2__in=objmoyen, date__range=[primary1, primary2]).values(
                'name__name','withcompany2__name').annotate(count =Count('name'))
    except:
        otheractivemoy = ""

    # نشاطات اخرى ابتدائي
    try:
        otheractiveprem = OtherActiv.objects.filter(withcompany3__in=objprem, date__range=[primary1, primary2]).values(
                'name__name','withcompany3__name').annotate(count =Count('name'))
    except:
        otheractiveprem = ""

    # نشاطات اخرى عامة
    try:
        otheract = OtherActiv.objects.filter(withcompany1= None, withcompany2= None, withcompany3= None, date__range=[primary1, primary2]).values(
                'name__name').annotate(count =Count('name'))
    except:
        otheract = ""

    context = {"listmediasec":mediasec, "listilamsec":listilamsec, "otheract":otheract, "otheractiveprem":otheractiveprem,"otheractivesec":otheractivesec, "otheractivemoy":otheractivemoy, "listmedfilesec":listmedfilesec,"listmedfilemoy":listmedfilemoy ,"dataprem":dataprem ,"datamoypar":datamoypar, "listmediamoy":listmediamoy, "listmediapre":listmediapre, "primary2":primary2, "primary1":primary1, "motasec":motasec, "listmota":listmota, "listingcell":listingcell, "followcomit":followcomit}
    return render(request, template_name="staff_template/date_rangeall_template.html",context=context)


@csrf_exempt
def delete_otheract(request):
    try:
        id = request.POST.get("id")
        otheract = OtherActiv.objects.get(id=id)
        otheract.delete()
        data = ""
    except:
        data = "خطأ في الحذف"
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def delete_mediasec(request):
    try:
        id = request.POST.get("id")
        mediasec = MediaSec.objects.get(id=id)
        mediasec.delete()
        data = ""
    except:
        data = "خطأ في الحذف"
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def delete_mediamoy(request):
    try:
        id = request.POST.get("id")
        mediamoy = MediaMoy.objects.get(id=id)
        mediamoy.delete()
        data = ""
    except:
        data = "خطأ في الحذف"
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def delete_mediapre(request):
    try:
        id = request.POST.get("id")
        mediapre = MediaPre.objects.get(id=id)
        mediapre.delete()
        data = ""
    except:
        data = "خطأ في الحذف"
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def delete_motabasec(request):
    try:
        id = request.POST.get("id")
        motasec = MotabaSec.objects.get(id=id)
        motasec.delete()
        data = ""
    except:
        data = "خطأ في الحذف"
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def delete_motabamoy(request):
    try:
        id = request.POST.get("id")
        motamoy = MotabaMoy.objects.get(id=id)
        motamoy.delete()
        data = ""
    except:
        data = "خطأ في الحذف"
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def delete_ilmparnt(request):
    try:
        id = request.POST.get("id")
        ilmparnt = MediaSecParnt.objects.get(id=id)
        ilmparnt.delete()
        data = ""
    except:
        data = "خطأ في الحذف"
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def delete_ilmparntmoy(request):
    try:
        id = request.POST.get("id")
        ilmparntmoy = MediaMoyParnt.objects.get(id=id)
        ilmparntmoy.delete()
        data = ""
    except:
        data = "خطأ في الحذف"
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def delete_ilmparntpre(request):
    try:
        id = request.POST.get("id")
        ilmparntpre = MediaPreParnt.objects.get(id=id)
        ilmparntpre.delete()
        data = ""
    except:
        data = "خطأ في الحذف"
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def delete_filemedia(request):
    try:
        id = request.POST.get("id")
        filemedia = FileMediaSec.objects.get(id=id)
        filemedia.delete()
        data = ""
    except:
        data = "خطأ في الحذف"
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def delete_filemediamoy(request):
    try:
        id = request.POST.get("id")
        filemediamoy = FileMediaMoy.objects.get(id=id)
        filemediamoy.delete()
        data = ""
    except:
        data = "خطأ في الحذف"
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def save_info(request):
    try:
        dateness = request.POST.get("dateness")
        if dateness:
            dateness = datetime.strptime(dateness, "%d/%m/%Y").date()
        status = request.POST.get("status")
        child = request.POST.get("child")
        certificate = request.POST.get("certificate")
        datemask1 = request.POST.get("datemask1")
        if datemask1:
            datemask1 = datetime.strptime(datemask1, "%d/%m/%Y").date()
        speacial = request.POST.get("speacial")
        compan = request.POST.get("compan")
        datemask2 = request.POST.get("datemask2")
        if datemask2:
            datemask2 = datetime.strptime(datemask2, "%d/%m/%Y").date()
        datemask3 = request.POST.get("datemask3")
        if datemask3:
            datemask3 = datetime.strptime(datemask3, "%d/%m/%Y").date()
        companystay = request.POST.get("companystay")
        datemask4 = request.POST.get("datemask4")
        if datemask4:
            datemask4 = datetime.strptime(datemask4, "%d/%m/%Y").date()
        ases = request.POST.get("as")
        morasamono = request.POST.get("morasamono")
        raisono = request.POST.get("raisono")
        datemask5 = request.POST.get("datemask5")
        if datemask5:
            datemask5 = datetime.strptime(datemask5, "%d/%m/%Y").date()
        degry = request.POST.get("degry")
        datemask6 = request.POST.get("datemask6")
        if datemask6:
            datemask6 = datetime.strptime(datemask6, "%d/%m/%Y").date()
        nemdateness = request.POST.get("nemdateness")
        placeness = request.POST.get("placeness")
        nccp = request.POST.get("nccp")
        cle = request.POST.get("cle")
        phone = request.POST.get("phone")
        phone2 = request.POST.get("phone2")
        email = request.POST.get("email")
        mostachar = Mostachar.objects.get(withuser=request.user.id)
        if dateness != '':
            mostachar.datenes = dateness
        mostachar.stat = status
        mostachar.nomberchild = child
        mostachar.chhada = certificate
        if datemask1 != '':
            mostachar.datechhada = datemask1
        else:
            mostachar.datechhada = None
        mostachar.spesialte = speacial
        mostachar.universti = compan
        if datemask2 != '':
            mostachar.firstdate = datemask2
        else:
            mostachar.firstdate = None
        if datemask3 != '':
            mostachar.firstdateinsector = datemask3
        else:
            mostachar.firstdateinsector = None
        mostachar.companystay = companystay
        if datemask4 != '':
            mostachar.firstdatecomp = datemask4
        else:
            mostachar.firstdatecomp = None
        mostachar.as1 = ases
        mostachar.as2 = morasamono
        mostachar.degry = raisono
        if datemask5 != '':
            mostachar.datestart = datemask5
        else:
            mostachar.datestart = None
        mostachar.lastdegry = degry
        if datemask6 != '':
            mostachar.dateactive = datemask6
        else:
            mostachar.dateactive = None
        mostachar.nbrith = nemdateness
        mostachar.placebrith = placeness
        mostachar.ncountccp = nccp
        mostachar.clee = cle
        mostachar.phone1 = phone
        mostachar.phone2 = phone2
        mostachar.email = email
        mostachar.save()
        data = "تم اضافة المعلومات الشخصية بنجاح"
    except:
        data = "هناك خطأ ما في اضافة المعلومات الشخصية"
        #print("lol")
    return JsonResponse(data, content_type="application/json", safe=False)


def staff_profile(request):
    staff = Mostachar.objects.get(withuser=request.user)
    context = {'user': request.user, 'staff': staff}
    return render(request, template_name="staff_template/staff_profile.html", context=context)

