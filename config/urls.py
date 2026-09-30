from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    # =========================================
    # DJANGO ADMIN
    # =========================================

    path(
        'admin/',
        admin.site.urls
    ),


    # =========================================
    # ACCOUNTS
    # Home
    # Patient Register
    # Doctor Register
    # Patient Login
    # Doctor Login
    # Logout
    # =========================================

    path(
        '',
        include('accounts.urls')
    ),


    # =========================================
    # PATIENTS
    # Patient Dashboard
    # =========================================

    path(
        'patient/',
        include('patients.urls')
    ),


    # =========================================
    # DOCTORS
    # Doctor Dashboard
    # Doctor Login
    # Doctor Logout
    # Doctor List
    # Doctor Details
    # =========================================

    path(
        'doctor/',
        include('doctors.urls')
    ),


    # =========================================
    # APPOINTMENTS
    # Book Appointment
    # My Appointments
    # Cancel Appointment
    # Doctor Appointments
    # Accept / Reject / Complete
    # =========================================

    path(
        'appointments/',
        include('appointments.urls')
    ),

]