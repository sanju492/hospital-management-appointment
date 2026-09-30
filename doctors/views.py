from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Doctor
from appointments.models import Appointment


# =========================================
# DOCTOR LOGIN
# =========================================

def doctor_login(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if user.role == 'doctor':

                login(request, user)

                return redirect(
                    'doctor_dashboard'
                )

            else:

                messages.error(
                    request,
                    'This account is not registered as a doctor.'
                )

        else:

            messages.error(
                request,
                'Invalid username or password.'
            )

    return render(
        request,
        'doctors/login.html'
    )


# =========================================
# DOCTOR DASHBOARD
# =========================================

@login_required
def doctor_dashboard(request):

    if request.user.role != 'doctor':

        messages.error(
            request,
            'Access denied. Doctor login required.'
        )

        return redirect(
            'doctor_login'
        )

    doctor, created = Doctor.objects.get_or_create(
        user=request.user
    )

    context = {
        'doctor': doctor,
    }

    return render(
        request,
        'doctors/dashboard.html',
        context
    )


# =========================================
# DOCTOR PROFILE
# =========================================

@login_required
def doctor_profile(request):

    if request.user.role != 'doctor':

        messages.error(
            request,
            'Only doctors can access this page.'
        )

        return redirect(
            'doctor_login'
        )

    doctor, created = Doctor.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

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

        specialization = request.POST.get(
            'specialization',
            ''
        ).strip()

        qualification = request.POST.get(
            'qualification',
            ''
        ).strip()

        experience = request.POST.get(
            'experience',
            '0'
        ).strip()

        consultation_fee = request.POST.get(
            'consultation_fee',
            '0'
        ).strip()

        available_days = request.POST.get(
            'available_days',
            ''
        ).strip()

        available_time = request.POST.get(
            'available_time',
            ''
        ).strip()

        bio = request.POST.get(
            'bio',
            ''
        ).strip()

        doctor.specialization = specialization

        doctor.qualification = qualification

        doctor.experience = (
            int(experience)
            if experience
            else 0
        )

        doctor.consultation_fee = (
            consultation_fee
            if consultation_fee
            else 0
        )

        doctor.available_days = available_days

        doctor.available_time = available_time

        doctor.bio = bio

        doctor.is_available = (
            request.POST.get(
                'is_available'
            ) == 'on'
        )

        doctor.save()

        messages.success(
            request,
            'Doctor profile updated successfully!'
        )

        return redirect(
            'doctor_profile'
        )

    context = {
        'doctor': doctor,
        'user': request.user,
        'specializations': Doctor.SPECIALIZATION_CHOICES,
    }

    return render(
        request,
        'doctors/profile.html',
        context
    )


# =========================================
# DOCTOR LOGOUT
# =========================================

@login_required
def doctor_logout(request):

    logout(request)

    messages.success(
        request,
        'You have been logged out successfully.'
    )

    return redirect(
        'doctor_login'
    )


# =========================================
# VIEW AVAILABLE DOCTORS
# =========================================
# IMPORTANT:
# This page is accessible through the
# Home -> Service -> Password flow.
# Login is NOT required here.
# =========================================

def doctor_list(request):

    doctors = Doctor.objects.filter(
        is_available=True
    ).select_related(
        'user'
    )

    specialization = request.GET.get(
        'specialization',
        ''
    ).strip()

    search = request.GET.get(
        'search',
        ''
    ).strip()

    if specialization:

        doctors = doctors.filter(
            specialization=specialization
        )

    if search:

        doctors = doctors.filter(
            user__first_name__icontains=search
        ) | doctors.filter(
            user__last_name__icontains=search
        )

    context = {
        'doctors': doctors,
        'specializations': Doctor.SPECIALIZATION_CHOICES,
        'selected_specialization': specialization,
        'search': search,
    }

    return render(
        request,
        'doctors/doctor_list.html',
        context
    )


# =========================================
# DOCTOR DETAILS
# =========================================
# Login is NOT required here.
# =========================================

def doctor_detail(request, doctor_id):

    doctor = get_object_or_404(
        Doctor.objects.select_related(
            'user'
        ),
        id=doctor_id,
        is_available=True
    )

    return render(
        request,
        'doctors/doctor_detail.html',
        {
            'doctor': doctor
        }
    )


# =========================================
# DOCTOR PATIENTS
# =========================================

@login_required
def doctor_patients(request):

    if request.user.role != 'doctor':

        messages.error(
            request,
            'Only doctors can view patients.'
        )

        return redirect(
            'doctor_login'
        )

    doctor, created = Doctor.objects.get_or_create(
        user=request.user
    )

    appointments = Appointment.objects.filter(
        doctor=doctor
    ).select_related(
        'patient',
        'patient__user'
    ).order_by(
        '-appointment_date',
        '-appointment_time'
    )

    patients = {}

    for appointment in appointments:

        patient = appointment.patient

        if patient.id not in patients:

            patients[patient.id] = {
                'patient': patient,
                'last_appointment': appointment,
            }

    context = {
        'doctor': doctor,
        'patients': patients.values(),
    }

    return render(
        request,
        'doctors/patients.html',
        context
    )


# =========================================
# DOCTOR AVAILABILITY
# =========================================

@login_required
def doctor_availability(request):

    if request.user.role != 'doctor':

        messages.error(
            request,
            'Only doctors can access availability settings.'
        )

        return redirect(
            'doctor_login'
        )

    doctor, created = Doctor.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        available_days = request.POST.get(
            'available_days',
            ''
        ).strip()

        available_time = request.POST.get(
            'available_time',
            ''
        ).strip()

        is_available = request.POST.get(
            'is_available'
        ) == 'on'

        doctor.available_days = available_days

        doctor.available_time = available_time

        doctor.is_available = is_available

        doctor.save()

        messages.success(
            request,
            'Availability updated successfully!'
        )

        return redirect(
            'doctor_availability'
        )

    context = {
        'doctor': doctor,
        'user': request.user,
    }

    return render(
        request,
        'doctors/availability.html',
        context
    )