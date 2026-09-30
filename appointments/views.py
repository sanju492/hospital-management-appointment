from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Appointment
from patients.models import Patient
from doctors.models import Doctor


# =========================================================
# BOOK APPOINTMENT
# =========================================================

@login_required
def book_appointment(request):

    # Only patients can book appointments
    if request.user.role != 'patient':
        messages.error(
            request,
            'Only patients can book appointments.'
        )
        return redirect('patient_dashboard')

    # Get patient profile
    patient, created = Patient.objects.get_or_create(
        user=request.user
    )

    # Get available doctors
    doctors = Doctor.objects.filter(
        is_available=True
    ).select_related('user')

    # Doctor selected from doctor detail page
    selected_doctor = request.GET.get('doctor', '')

    if request.method == 'POST':

        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        reason = request.POST.get('reason', '').strip()

        # ---------------------------------------------
        # Validation
        # ---------------------------------------------

        if not doctor_id:
            messages.error(
                request,
                'Please select a doctor.'
            )
            return redirect('book_appointment')

        if not appointment_date:
            messages.error(
                request,
                'Please select an appointment date.'
            )
            return redirect('book_appointment')

        if not appointment_time:
            messages.error(
                request,
                'Please select an appointment time.'
            )
            return redirect('book_appointment')

        # ---------------------------------------------
        # Get selected doctor
        # ---------------------------------------------

        doctor = get_object_or_404(
            Doctor,
            id=doctor_id,
            is_available=True
        )

        # ---------------------------------------------
        # Convert date
        # ---------------------------------------------

        try:
            selected_date = timezone.datetime.strptime(
                appointment_date,
                '%Y-%m-%d'
            ).date()
        except ValueError:

            messages.error(
                request,
                'Invalid appointment date.'
            )

            return redirect(
                f'/appointments/book/?doctor={doctor.id}'
            )

        today = timezone.localdate()

        # ---------------------------------------------
        # Prevent past dates
        # ---------------------------------------------

        if selected_date < today:

            messages.error(
                request,
                'Please select a future date.'
            )

            return redirect(
                f'/appointments/book/?doctor={doctor.id}'
            )

        # ---------------------------------------------
        # Check duplicate booking
        # ---------------------------------------------

        existing_appointment = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=selected_date,
            appointment_time=appointment_time,
            status__in=['pending', 'accepted']
        ).exists()

        if existing_appointment:

            messages.error(
                request,
                'This time slot is already booked.'
            )

            return redirect(
                f'/appointments/book/?doctor={doctor.id}'
            )

        # ---------------------------------------------
        # Create appointment
        # ---------------------------------------------

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=selected_date,
            appointment_time=appointment_time,
            reason=reason,
            status='pending'
        )

        messages.success(
            request,
            'Appointment booked successfully!'
        )

        return redirect('my_appointments')

    # ---------------------------------------------
    # Context
    # ---------------------------------------------

    context = {
        'doctors': doctors,
        'selected_doctor': selected_doctor,
        'today': timezone.localdate().strftime('%Y-%m-%d'),
    }

    return render(
        request,
        'appointments/book.html',
        context
    )


# =========================================================
# PATIENT - MY APPOINTMENTS
# =========================================================

@login_required
def my_appointments(request):

    # Only patients can view their appointments
    if request.user.role != 'patient':

        messages.error(
            request,
            'Only patients can view appointments.'
        )

        return redirect('patient_dashboard')

    # Get patient profile
    patient, created = Patient.objects.get_or_create(
        user=request.user
    )

    # Get patient's appointments
    appointments = Appointment.objects.filter(
        patient=patient
    ).select_related(
        'doctor',
        'doctor__user'
    ).order_by(
        '-appointment_date',
        '-appointment_time'
    )

    return render(
        request,
        'appointments/my_appointments.html',
        {
            'appointments': appointments
        }
    )


# =========================================================
# PATIENT - CANCEL APPOINTMENT
# =========================================================

@login_required
def cancel_appointment(request, appointment_id):

    # Only patients can cancel
    if request.user.role != 'patient':

        messages.error(
            request,
            'Access denied.'
        )

        return redirect('patient_dashboard')

    # Get patient profile
    patient, created = Patient.objects.get_or_create(
        user=request.user
    )

    # Get appointment belonging to this patient
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=patient
    )

    # ---------------------------------------------
    # Cancel pending or accepted appointment
    # ---------------------------------------------

    if appointment.status in ['pending', 'accepted']:

        appointment.status = 'cancelled'

        appointment.save()

        messages.success(
            request,
            'Appointment cancelled successfully.'
        )

    else:

        messages.error(
            request,
            'This appointment cannot be cancelled.'
        )

    return redirect('my_appointments')


# =========================================================
# DOCTOR - VIEW PATIENT APPOINTMENTS
# =========================================================

@login_required
def doctor_appointments(request):

    # Only doctors can access
    if request.user.role != 'doctor':

        messages.error(
            request,
            'Only doctors can view patient appointments.'
        )

        return redirect('doctor_login')

    # Get current doctor profile
    doctor, created = Doctor.objects.get_or_create(
        user=request.user
    )

    # Get appointments for this doctor
    appointments = Appointment.objects.filter(
        doctor=doctor
    ).select_related(
        'patient',
        'patient__user'
    ).order_by(
        'appointment_date',
        'appointment_time'
    )

    context = {
        'doctor': doctor,
        'appointments': appointments,
    }

    return render(
        request,
        'appointments/doctor_appointments.html',
        context
    )


# =========================================================
# DOCTOR - UPDATE APPOINTMENT STATUS
# =========================================================

@login_required
def update_appointment_status(request, appointment_id):

    # Only doctors can update appointment status
    if request.user.role != 'doctor':

        messages.error(
            request,
            'Only doctors can update appointments.'
        )

        return redirect('doctor_login')

    # Get current doctor
    doctor, created = Doctor.objects.get_or_create(
        user=request.user
    )

    # Get appointment belonging to this doctor
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=doctor
    )

    # Only POST request allowed
    if request.method != 'POST':

        messages.error(
            request,
            'Invalid request.'
        )

        return redirect('doctor_appointments')

    # Get status from form
    new_status = request.POST.get('status')

    # Allowed statuses
    allowed_statuses = [
        'accepted',
        'rejected',
        'completed',
        'cancelled'
    ]

    # Validate status
    if new_status not in allowed_statuses:

        messages.error(
            request,
            'Invalid appointment status.'
        )

        return redirect('doctor_appointments')

    # ---------------------------------------------
    # Status update rules
    # ---------------------------------------------

    if new_status == 'accepted':

        if appointment.status != 'pending':

            messages.error(
                request,
                'Only pending appointments can be accepted.'
            )

            return redirect('doctor_appointments')

    elif new_status == 'rejected':

        if appointment.status != 'pending':

            messages.error(
                request,
                'Only pending appointments can be rejected.'
            )

            return redirect('doctor_appointments')

    elif new_status == 'completed':

        if appointment.status != 'accepted':

            messages.error(
                request,
                'Only accepted appointments can be completed.'
            )

            return redirect('doctor_appointments')

    elif new_status == 'cancelled':

        if appointment.status not in ['pending', 'accepted']:

            messages.error(
                request,
                'This appointment cannot be cancelled.'
            )

            return redirect('doctor_appointments')

    # ---------------------------------------------
    # Save new status
    # ---------------------------------------------

    appointment.status = new_status

    appointment.save()

    # ---------------------------------------------
    # Success message
    # ---------------------------------------------

    status_message = {
        'accepted': 'Appointment accepted successfully.',
        'rejected': 'Appointment rejected successfully.',
        'completed': 'Appointment marked as completed.',
        'cancelled': 'Appointment cancelled successfully.',
    }

    messages.success(
        request,
        status_message.get(
            new_status,
            'Appointment status updated.'
        )
    )

    return redirect('doctor_appointments')