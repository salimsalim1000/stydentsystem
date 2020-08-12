from django import forms

from student.models import Courses, SessionYearModel


class DateInput(forms.DateInput):
    input_type = "date"

class AddStudentForm(forms.Form):
    email = forms.EmailField(label="email", max_length=100 ,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off"}))
    password = forms.CharField(label="password", max_length=100,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="first name", max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="last name", max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))  
    username = forms.CharField(label="username", max_length=100,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
    address = forms.CharField(label="address", max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="profile pic", max_length=100,widget=forms.FileInput(attrs={"class":"form-control"}),required=0)
    cours_list = []
    try:
        courses = Courses.objects.all()
        for cours in courses:
            small_cours = (cours.id , cours.course_name)
            cours_list.append(small_cours)
    except:
        cours_list = []

    session_list = []
    try:
        sessions = SessionYearModel.objects.all()

        for ses in sessions:
            small_ses = (ses.id, str(ses.session_stat_year) + "   TO  " + str(ses.session_end_year))
            session_list.append(small_ses)
    except:
        session_list = []


    gender = (("male","male"),("female","female"))
    course = forms.ChoiceField(label="course", choices=cours_list ,widget=forms.Select(attrs={"class":"form-control"}))
    sex = forms.ChoiceField(choices=gender,widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_list,
                                        widget=forms.Select(attrs={"class": "form-control"}))

    
    
class EditStudentForm(forms.Form):
    email = forms.EmailField(label="email", max_length=100 ,widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="password", max_length=100,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="first name", max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="last name", max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))  
    username = forms.CharField(label="username", max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="address", max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="profile pic", max_length=100,widget=forms.FileInput(attrs={"class":"form-control"}), required=0)

    cours_list = []
    try:
        courses = Courses.objects.all()
        for cours in courses:
            small_cours = (cours.id , cours.course_name)
            cours_list.append(small_cours)
    except:
        cours_list = []

    session_list = []
    try:
        sessions = SessionYearModel.objects.all()
        for session in sessions:
            small_session = (session.id , str(session.session_stat_year)+ "-" + str(session.session_end_year))
            session_list.append(small_session)
    except:
        session_list = []
        #  session_list = []
    gender = (("male","male"),("female","female"))
    course = forms.ChoiceField(label="course", choices=cours_list ,widget=forms.Select(attrs={"class":"form-control"}))
    sex = forms.ChoiceField(choices=gender,widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_list,
                                        widget=forms.Select(attrs={"class": "form-control"}))
