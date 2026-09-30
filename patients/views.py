from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Patient
from doctors.models import Doctor
from appointments.models import Appointment


# =========================================================
# PATIENT DASHBOARD
# =========================================================

@login_required
def patient_dashboard(request):

    if request.user.role != 'patient':
        messages.error(
            request,
            'Access denied.'
        )
        return redirect('patient_login')

    patient, created = Patient.objects.get_or_create(
        user=request.user
    )

    today = timezone.localdate()

    appointments = Appointment.objects.filter(
        patient=patient
    )

    upcoming_appointments = appointments.filter(
        appointment_date__gte=today,
        status__in=['pending', 'accepted']
    ).select_related(
        'doctor',
        'doctor__user'
    ).order_by(
        'appointment_date',
        'appointment_time'
    )

    upcoming_count = upcoming_appointments.count()

    completed_count = appointments.filter(
        status='completed'
    ).count()

    pending_count = appointments.filter(
        status='pending'
    ).count()

    doctors_count = Doctor.objects.filter(
        is_available=True
    ).count()

    context = {
        'patient': patient,
        'user': request.user,
        'upcoming_appointments': upcoming_appointments[:5],
        'upcoming_count': upcoming_count,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'doctors_count': doctors_count,
    }

    return render(
        request,
        'patients/dashboard.html',
        context
    )


# =========================================================
# PATIENT PROFILE
# =========================================================

@login_required
def patient_profile(request):

    if request.user.role != 'patient':
        messages.error(
            request,
            'Only patients can access this page.'
        )
        return redirect('patient_login')

    patient, created = Patient.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        # -------------------------------------------------
        # USER INFORMATION
        # -------------------------------------------------

        request.user.first_name = request.POST.get(
            'first_name',
            ''
        ).strip()

        request.user.last_name = request.POST.get(
            'last_name',
            ''
        ).strip()

        request.user.email = request.POST.get(
            'email',
            ''
        ).strip()

        request.user.phone = request.POST.get(
            'phone',
            ''
        ).strip()

        request.user.save()


        # -------------------------------------------------
        # PATIENT INFORMATION
        # -------------------------------------------------

        age = request.POST.get(
            'age',
            ''
        ).strip()

        gender = request.POST.get(
            'gender',
            ''
        ).strip()

        date_of_birth = request.POST.get(
            'date_of_birth',
            ''
        ).strip()

        address = request.POST.get(
            'address',
            ''
        ).strip()


        # -------------------------------------------------
        # AGE VALIDATION
        # -------------------------------------------------

        if age:

            try:
                patient.age = int(age)

            except ValueError:

                messages.error(
                    request,
                    'Please enter a valid age.'
                )

                return redirect(
                    'patient_profile'
                )

        else:

            patient.age = None


        # -------------------------------------------------
        # OTHER PATIENT DETAILS
        # -------------------------------------------------

        patient.gender = gender

        if date_of_birth:
            patient.date_of_birth = date_of_birth
        else:
            patient.date_of_birth = None

        patient.address = address

        patient.save()


        messages.success(
            request,
            'Profile updated successfully!'
        )

        return redirect(
            'patient_profile'
        )


    context = {
        'patient': patient,
        'user': request.user,
    }

    return render(
        request,
        'patients/profile.html',
        context
    )


# =========================================================
# PATIENT RECORDS
# =========================================================

@login_required
def patient_records(request):

    if request.user.role != 'patient':

        messages.error(
            request,
            'Only patients can access patient records.'
        )

        return redirect(
            'patient_login'
        )


    patient, created = Patient.objects.get_or_create(
        user=request.user
    )


    appointments = Appointment.objects.filter(
        patient=patient
    ).select_related(
        'doctor',
        'doctor__user'
    ).order_by(
        '-appointment_date',
        '-appointment_time'
    )


    context = {
        'patient': patient,
        'user': request.user,
        'appointments': appointments,
    }


    return render(
        request,
        'patients/records.html',
        context
    )