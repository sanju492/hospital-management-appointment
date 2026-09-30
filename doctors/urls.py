from django.urls import path

from . import views


urlpatterns = [

    # =========================================
    # DOCTOR LOGIN
    # =========================================

    path(
        'login/',
        views.doctor_login,
        name='doctor_login'
    ),


    # =========================================
    # DOCTOR DASHBOARD
    # =========================================

    path(
        'dashboard/',
        views.doctor_dashboard,
        name='doctor_dashboard'
    ),


    # =========================================
    # DOCTOR MY PROFILE
    # =========================================

    path(
        'profile/',
        views.doctor_profile,
        name='doctor_profile'
    ),


    # =========================================
    # DOCTOR LOGOUT
    # =========================================

    path(
        'logout/',
        views.doctor_logout,
        name='doctor_logout'
    ),


    # =========================================
    # PATIENT - VIEW AVAILABLE DOCTORS
    # =========================================

    path(
        'list/',
        views.doctor_list,
        name='doctor_list'
    ),


    # =========================================
    # DOCTOR - VIEW THEIR PATIENTS
    # =========================================

    path(
        'patients/',
        views.doctor_patients,
        name='doctor_patients'
    ),


    # =========================================
    # PATIENT - VIEW DOCTOR DETAILS
    # =========================================

    path(
        '<int:doctor_id>/',
        views.doctor_detail,
        name='doctor_detail'
    ),
    path(
    'availability/',
    views.doctor_availability,
    name='doctor_availability'
),

]