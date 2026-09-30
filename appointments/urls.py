from django.urls import path
from . import views


urlpatterns = [

    # =========================================
    # PATIENT - BOOK APPOINTMENT
    # =========================================

    path(
        'book/',
        views.book_appointment,
        name='book_appointment'
    ),


    # =========================================
    # PATIENT - MY APPOINTMENTS
    # =========================================

    path(
        'my-appointments/',
        views.my_appointments,
        name='my_appointments'
    ),


    # =========================================
    # PATIENT - CANCEL APPOINTMENT
    # =========================================

    path(
        'cancel/<int:appointment_id>/',
        views.cancel_appointment,
        name='cancel_appointment'
    ),


    # =========================================
    # DOCTOR - VIEW PATIENT APPOINTMENTS
    # =========================================

    path(
        'doctor/',
        views.doctor_appointments,
        name='doctor_appointments'
    ),


    # =========================================
    # DOCTOR - UPDATE APPOINTMENT STATUS
    # =========================================

    path(
        'doctor/update/<int:appointment_id>/',
        views.update_appointment_status,
        name='update_appointment_status'
    ),

]