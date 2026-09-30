from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # HOME
    # =====================================================

    path(
        '',
        views.home,
        name='home'
    ),


    # =====================================================
    # REGISTRATION
    # =====================================================

    path(
        'register/',
        views.register_choice,
        name='register_choice'
    ),

    path(
        'register/patient/',
        views.patient_register,
        name='patient_register'
    ),

    path(
        'register/doctor/',
        views.doctor_register,
        name='doctor_register'
    ),


    # =====================================================
    # LOGIN
    # =====================================================

    path(
        'login/',
        views.patient_login,
        name='patient_login'
    ),

    path(
        'doctor-login/',
        views.doctor_login,
        name='doctor_login'
    ),


    # =====================================================
    # LOGOUT
    # =====================================================

    path(
        'logout/',
        views.patient_logout,
        name='patient_logout'
    ),

    path(
        'doctor-logout/',
        views.doctor_logout,
        name='doctor_logout'
    ),


    # =====================================================
    # SERVICE PASSWORD
    # =====================================================

    path(
        'service/<str:service>/',
        views.service_password,
        name='service_password'
    ),


    # =====================================================
    # DEPARTMENTS
    # =====================================================

    path(
        'departments/',
        views.department_list,
        name='department_list'
    ),

]