"""stydentsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django
from django.conf.urls.static import static
from django.contrib import admin , auth
from django.urls import path, include
from django.contrib.auth import views as auth_views
from student import views, HodViews, StaffViews, StudentViews
from stydentsystem import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('password/', auth_views.PasswordChangeView.as_view()),
    path('accounts/', include('django.contrib.auth.urls')),
    path('demo', views.showDemoPage),

    path('', views.ShowLoginPage, name="show_login"),
    path('show_login/', views.ShowLoginPage, name="show_login"),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user, name="logout"),
    path('doLogin', views.doLogin, name="do_login"),
    path('admin_home', HodViews.admin_home, name="admin_home"),
    path('add_premary', HodViews.add_premary,name="add_premary"),
    path('add_premary_save' , HodViews.add_premary_save ,name="add_premary_save"),
    path('add_moyen', HodViews.add_moyen, name="add_moyen"),
    path('add_moyen_save', HodViews.add_moyen_save, name="add_moyen_save"),
    path('add_secondry', HodViews.add_secondry, name="add_secondry"),
    path('add_secondry_save', HodViews.add_secondry_save, name="add_secondry_save"),
    path('add_degreymoyen', HodViews.add_degreymoyen, name="add_degreymoyen"),
    path('add_degreymoyen_save', HodViews.add_degreymoyen_save, name="add_degreymoyen_save"),
    path('add_degreypremglobal', HodViews.add_degreypremglobal, name="add_degreypremglobal"),
    path('add_degreypremglobal_save', HodViews.add_degreypremglobal_save, name="add_degreypremglobal_save"),
    path('add_degreyseco', HodViews.add_degreyseco, name="add_degreyseco"),
    path('add_degreyseco_save', HodViews.add_degreyseco_save, name="add_degreyseco_save"),
    path('add_speasial', HodViews.add_speasial, name="add_speasial"),
    path('add_speasial_save', HodViews.add_speasial_save, name="add_speasial_save"),
    path('add_classprem', HodViews.add_classprem, name="add_classprem"),
    path('add_classprem_save', HodViews.add_classprem_save, name="add_classprem_save"),
    path('add_classmoyen', HodViews.add_classmoyen, name="add_classmoyen"),
    path('add_classmoyen_save', HodViews.add_classmoyen_save, name="add_classprem_save"),
    path('add_classsecond', HodViews.add_classsecond, name="add_classsecond"),
    path('add_classsecond_save', HodViews.add_classsecond_save, name="add_classsecond_save"),
    path('add_mostachar', HodViews.add_mostachar, name="add_mostachar"),
    path('add_mostachar_save', HodViews.add_mostachar_save),
    path('add_blukuser', HodViews.add_blukuser, name="add_blukuser"),
    path('add_blukuser_save', HodViews.add_blukuser_save),
    path('manage_mostachar', HodViews.manage_mostachar, name="manage_mostachar"),
    path('edit_mostachar/<str:mostachar_id>', HodViews.edit_mostachar, name="edit_mostachar"),
    path('edit_mostachar_save', HodViews.edit_mostachar_save, name="edit_mostachar_save"),
    path('distribit', HodViews.distribit, name="distribit"),
    path('distribit_save', HodViews.distribit_save, name="distribit_save"),
    path('distribitmoyen_save', HodViews.distribitmoyen_save, name="distribitmoyen_save"),
    path('distribitprimer_save', HodViews.distribitprimer_save, name="distribitprimer_save"),
    path('check_email_exist', HodViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist', HodViews.check_username_exist, name="check_username_exist"),
    path('admin_profile', HodViews.admin_profile,name="admin_profile"),
    path('admin_profile_save', HodViews.admin_profile_save,name="admin_profile_save"),
    path('add_activte', HodViews.add_activte, name="add_activte"),
    path('add_activte_save', HodViews.add_activte_save, name="add_activte_save"),
    path('add_typefilemedia', HodViews.add_typefilemedia, name="add_typefilemedia"),
    path('add_typefilemedia_save', HodViews.add_typefilemedia_save, name="add_typefilemedia_save"),
    path('mostachar_info', HodViews.mostachar_info, name="mostachar_info"),
    path('date_all', HodViews.date_all, name="date_all"),
    path('date_all_get', HodViews.date_all_get, name="date_all_get"),
    path('date_range_full', HodViews.date_range_full, name="date_range_full"),
    path('date_range_full_get', HodViews.date_range_full_get, name="date_range_full_get"),




#staff
    path('mostachar_home', StaffViews.mostachar_home, name="mostachar_home"),
    path('add_degreyprem', StaffViews.add_degreyprem, name="add_degreyprem"),
    path('add_degreyprem_save', StaffViews.add_degreyprem_save, name="add_degreyprem_save"),
    path('add_degreymoyene', StaffViews.add_degreymoyene, name="add_degreymoyene"),
    path('add_degreymoyene_save', StaffViews.add_degreymoyene_save, name="add_degreymoyene_save"),
    path('add_degresecondarye', StaffViews.add_degresecondarye, name="add_degresecondarye"),
    path('add_degresecondarye_save', StaffViews.add_degresecondarye_save, name="add_degresecondarye_save"),
    path('get_spesialite', StaffViews.get_spesialite, name="get_spesialite"),
    path('ilam_seconder', StaffViews.ilam_seconder, name="ilam_seconder"),
    path('ilam_seconder_save', StaffViews.ilam_seconder_save, name="ilam_seconder_save"),
    path('ilam_moyen', StaffViews.ilam_moyen, name="ilam_moyen"),
    path('ilam_moyen_save', StaffViews.ilam_moyen_save, name="ilam_moyen_save"),
    path('ilam_prem', StaffViews.ilam_prem, name="ilam_prem"),
    path('ilam_prem_save', StaffViews.ilam_prem_save, name="ilam_prem_save"),
    path('cell_listen', StaffViews.cell_listen, name="cell_listen"),
    path('cell_coumit', StaffViews.cell_coumit, name="cell_coumit"),
    path('save_cell', StaffViews.save_cell, name="save_cell"),
    path('save_cellnoexist', StaffViews.save_cellnoexist, name="save_cellnoexist"),
    path('cell_moyen_save', StaffViews.cell_moyen_save, name="cell_moyen_save"),
    path('nocell_moyen_save', StaffViews.nocell_moyen_save, name="nocell_moyen_save"),
    path('save_motaba', StaffViews.save_motaba, name="save_motaba"),
    path('save_motaba_moy', StaffViews.save_motaba_moy, name="save_motaba_moy"),
    path('ilam_parents', StaffViews.ilam_parents, name="ilam_parents"),
    path('save_ilam_parnts', StaffViews.save_ilam_parnts, name="save_ilam_parnts"),
    path('ilam_parents_moy', StaffViews.ilam_parents_moy, name="ilam_parents_moy"),
    path('save_ilam_parentsmoy', StaffViews.save_ilam_parentsmoy, name="save_ilam_parentsmoy"),
    path('ilam_parents_prem', StaffViews.ilam_parents_prem, name="ilam_parents_prem"),
    path('save_ilam_parntsprem', StaffViews.save_ilam_parntsprem, name="save_ilam_parntsprem"),
    path('other_activite', StaffViews.other_activite, name="other_activite"),
    path('other_activitemoy', StaffViews.other_activitemoy, name="other_activitemoy"),
    path('save_activeite_sec', StaffViews.save_activeite_sec, name="save_activeite_sec"),
    path('save_activeite_any', StaffViews.save_activeite_any, name="save_activeite_any"),
    path('save_activeite_moy', StaffViews.save_activeite_moy, name="save_activeite_moy"),
    path('save_activeite_prem', StaffViews.save_activeite_prem, name="save_activeite_prem"),
    path('add_file_media', StaffViews.add_file_media, name="add_file_media"),
    path('add_file_mediamoy', StaffViews.add_file_mediamoy, name="add_file_mediamoy"),
    path('add_mediasec_save', StaffViews.add_mediasec_save, name="add_mediasec_save"),
    path('add_mediamoyen_save', StaffViews.add_mediamoyen_save, name="add_mediamoyen_save"),
    path('date_range_all', StaffViews.date_range_all, name="date_range_all"),
    path('date_range_all_get', StaffViews.date_range_all_get, name="date_range_all_get"),
    path('date_range_fulle', StaffViews.date_range_fulle, name="date_range_fulle"),
    path('date_range_fulle_get', StaffViews.date_range_fulle_get, name="date_range_fulle_get"),
    path('delete_otheract', StaffViews.delete_otheract, name="delete_otheract"),
    path('delete_mediasec', StaffViews.delete_mediasec, name="delete_mediasec"),
    path('delete_mediamoy', StaffViews.delete_mediamoy, name="delete_mediamoy"),
    path('delete_mediapre', StaffViews.delete_mediapre, name="delete_mediapre"),
    path('delete_motabasec', StaffViews.delete_motabasec, name="delete_motabasec"),
    path('delete_motabamoy', StaffViews.delete_motabamoy, name="delete_motabamoy"),
    path('delete_ilmparnt', StaffViews.delete_ilmparnt, name="delete_ilmparnt"),
    path('delete_ilmparntmoy', StaffViews.delete_ilmparntmoy, name="delete_ilmparntmoy"),
    path('delete_ilmparntpre', StaffViews.delete_ilmparntpre, name="delete_ilmparntpre"),
    path('delete_filemedia', StaffViews.delete_filemedia, name="delete_filemedia"),
    path('delete_filemediamoy', StaffViews.delete_filemediamoy, name="delete_filemediamoy"),



    path('staff_profile', StaffViews.staff_profile, name="staff_profile"),
    path('save_info', StaffViews.save_info, name="save_info"),
    path('student_home', StudentViews.student_home, name="student_home"),
    path('student_view_attendance', StudentViews.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post', StudentViews.student_view_attendance_post, name="student_view_attendance_post"),
    path('student_aplly_leave', StudentViews.student_aplly_leave, name="student_aplly_leave"),
    path('student_aplly_leave_save', StudentViews.student_aplly_leave_save, name="student_aplly_leave_save"),
    path('student_feedback', StudentViews.student_feedback, name="student_feedback"),
    path('student_feedback_save', StudentViews.student_feedback_save, name="student_feedback_save"),
    path('student_profile', StudentViews.student_profile, name="student_profile"),
    path('student_profile_save', StudentViews.student_profile_save, name="student_profile_save"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
