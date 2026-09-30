from django.urls import path
from . import views


urlpatterns = [

    path(
        'dashboard/',
        views.patient_dashboard,
        name='patient_dashboard'
    ),

    path(
        'profile/',
        views.patient_profile,
        name='patient_profile'
    ),

    path(
        'records/',
        views.patient_records,
        name='patient_records'
    ),

]