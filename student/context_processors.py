from student.models import Moyen, Primary, Secondary


def get_current_year_to_context(request):
    moyenexiste = Moyen.objects.filter(withuser=request.user.id).exists()
    moyenexiste=bool(moyenexiste)
    preexiste = Primary.objects.filter(withuser=request.user.id).exists()
    preexiste = bool(preexiste)
    seconderexisttt = Secondary.objects.filter(withprimary=request.user.id).exists()
    seconderexisttt = bool(seconderexisttt)
    return {
        'moyenexiste': moyenexiste,
        'preexiste': preexiste,
        'seconderexisttt': seconderexisttt
    }