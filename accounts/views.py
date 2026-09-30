from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from patients.models import Patient
from doctors.models import Doctor


User = get_user_model()


# =========================================================
# HOME
# =========================================================

def home(request):
    return render(
        request,
        'home.html'
    )


# =========================================================
# REGISTER CHOICE
# =========================================================

def register_choice(request):
    return render(
        request,
        'register_choice.html'
    )


# =========================================================
# PATIENT REGISTER
# =========================================================

def patient_register(request):

    if request.method == 'POST':

        full_name = request.POST.get(
            'full_name',
            ''
        ).strip()

        username = request.POST.get(
            'username',
            ''
        ).strip()

        email = request.POST.get(
            'email',
            ''
        ).strip()

        phone = request.POST.get(
            'phone',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        confirm_password = request.POST.get(
            'confirm_password',
            ''
        )

        age = request.POST.get(
            'age',
            ''
        )

        gender = request.POST.get(
            'gender',
            ''
        )


        # -------------------------
        # Password check
        # -------------------------

        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return redirect(
                'patient_register'
            )


        # -------------------------
        # Username check
        # -------------------------

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                'Username already exists.'
            )

            return redirect(
                'patient_register'
            )


        # -------------------------
        # Email check
        # -------------------------

        if email and User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                'Email already registered.'
            )

            return redirect(
                'patient_register'
            )


        # -------------------------
        # Split full name
        # -------------------------

        name_parts = full_name.split()

        first_name = (
            name_parts[0]
            if name_parts
            else ''
        )

        last_name = (
            ' '.join(name_parts[1:])
            if len(name_parts) > 1
            else ''
        )


        # -------------------------
        # Create User
        # -------------------------

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role='patient'
        )


        # -------------------------
        # Create Patient Profile
        # -------------------------

        Patient.objects.create(
            user=user,
            age=int(age) if age else None,
            gender=gender
        )


        messages.success(
            request,
            'Patient account created successfully! Please login.'
        )

        return redirect(
            'patient_login'
        )


    return render(
        request,
        'patients/register.html'
    )


# =========================================================
# DOCTOR REGISTER
# =========================================================

def doctor_register(request):

    if request.method == 'POST':

        full_name = request.POST.get(
            'full_name',
            ''
        ).strip()

        username = request.POST.get(
            'username',
            ''
        ).strip()

        email = request.POST.get(
            'email',
            ''
        ).strip()

        phone = request.POST.get(
            'phone',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        confirm_password = request.POST.get(
            'confirm_password',
            ''
        )

        specialization = request.POST.get(
            'specialization',
            ''
        )

        qualification = request.POST.get(
            'qualification',
            ''
        )

        experience = request.POST.get(
            'experience',
            '0'
        )

        consultation_fee = request.POST.get(
            'consultation_fee',
            '0'
        )

        available_days = request.POST.get(
            'available_days',
            ''
        )

        available_time = request.POST.get(
            'available_time',
            ''
        )

        bio = request.POST.get(
            'bio',
            ''
        )


        # -------------------------
        # Password check
        # -------------------------

        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return redirect(
                'doctor_register'
            )


        # -------------------------
        # Username check
        # -------------------------

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                'Username already exists.'
            )

            return redirect(
                'doctor_register'
            )


        # -------------------------
        # Email check
        # -------------------------

        if email and User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                'Email already registered.'
            )

            return redirect(
                'doctor_register'
            )


        # -------------------------
        # Split full name
        # -------------------------

        name_parts = full_name.split()

        first_name = (
            name_parts[0]
            if name_parts
            else ''
        )

        last_name = (
            ' '.join(name_parts[1:])
            if len(name_parts) > 1
            else ''
        )


        # -------------------------
        # Create User
        # -------------------------

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role='doctor'
        )


        # -------------------------
        # Create Doctor Profile
        # -------------------------

        Doctor.objects.create(
            user=user,
            specialization=specialization,
            qualification=qualification,
            experience=int(experience)
            if experience
            else 0,
            consultation_fee=float(consultation_fee)
            if consultation_fee
            else 0,
            available_days=available_days,
            available_time=available_time,
            bio=bio,
            is_available=True
        )


        messages.success(
            request,
            'Doctor account created successfully! Please login.'
        )

        return redirect(
            'doctor_login'
        )


    return render(
        request,
        'doctors/doctors_register.html'
    )


# =========================================================
# PATIENT LOGIN
# =========================================================

def patient_login(request):

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

            # -------------------------
            # Patient
            # -------------------------

            if user.role == 'patient':

                login(
                    request,
                    user
                )

                return redirect(
                    'patient_dashboard'
                )


            # -------------------------
            # Doctor
            # -------------------------

            elif user.role == 'doctor':

                messages.error(
                    request,
                    'This is a doctor account. Please use Doctor Login.'
                )


            # -------------------------
            # Admin
            # -------------------------

            elif user.role == 'admin':

                messages.error(
                    request,
                    'This is an admin account. Please use Admin Login.'
                )


        else:

            messages.error(
                request,
                'Invalid username or password.'
            )


    return render(
        request,
        'patients/login.html'
    )


# =========================================================
# DOCTOR LOGIN
# =========================================================

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

            # -------------------------
            # Doctor
            # -------------------------

            if user.role == 'doctor':

                login(
                    request,
                    user
                )

                return redirect(
                    'doctor_dashboard'
                )


            # -------------------------
            # Patient
            # -------------------------

            elif user.role == 'patient':

                messages.error(
                    request,
                    'This is a patient account. Please use Patient Login.'
                )


            # -------------------------
            # Admin
            # -------------------------

            elif user.role == 'admin':

                messages.error(
                    request,
                    'This is an admin account.'
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


# =========================================================
# PATIENT LOGOUT
# =========================================================

@login_required
def patient_logout(request):

    logout(request)

    messages.success(
        request,
        'You have been logged out successfully.'
    )

    return redirect(
        'patient_login'
    )


# =========================================================
# DOCTOR LOGOUT
# =========================================================

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


# =========================================================
# SERVICE PASSWORD PROTECTION
# =========================================================

SERVICE_PASSWORD = "password123"


def service_password(request, service):

    # -------------------------
    # Allowed services
    # -------------------------

    allowed_services = [

        'doctors',

        'appointment',

        'departments',

        'records',

    ]


    # -------------------------
    # Check invalid service
    # -------------------------

    if service not in allowed_services:

        messages.error(
            request,
            'Invalid service.'
        )

        return redirect(
            'home'
        )


    # -------------------------
    # Service names
    # -------------------------

    service_names = {

        'doctors':
            'Find Doctors',

        'appointment':
            'Book Appointment',

        'departments':
            'Departments',

        'records':
            'Patient Records',

    }


    # -------------------------
    # Password submission
    # -------------------------

    if request.method == 'POST':

        password = request.POST.get(
            'password',
            ''
        )


        # -------------------------
        # Correct password
        # -------------------------

        if password == SERVICE_PASSWORD:

            request.session[
                f'{service}_access'
            ] = True


            # -------------------------
            # Find Doctors
            # -------------------------

            if service == 'doctors':

                return redirect(
                    'doctor_list'
                )


            # -------------------------
            # Book Appointment
            # -------------------------

            elif service == 'appointment':

                return redirect(
                    'book_appointment'
                )


            # -------------------------
            # Departments
            # -------------------------

            elif service == 'departments':

                return redirect(
                    'department_list'
                )


            # -------------------------
            # Patient Records
            # -------------------------

            elif service == 'records':

                return redirect(
                    'patient_records'
                )


        # -------------------------
        # Wrong password
        # -------------------------

        else:

            messages.error(
                request,
                'Incorrect service password.'
            )


    return render(
        request,
        'service_password.html',
        {
            'service': service,
            'service_name': service_names[service],
        }
    )


# =========================================================
# DEPARTMENT LIST
# =========================================================

def department_list(request):

    departments = [

        {
            'name':
                'Cardiology',

            'icon':
                '❤️',

            'description':
                'Heart and cardiovascular care.'
        },

        {
            'name':
                'Neurology',

            'icon':
                '🧠',

            'description':
                'Diagnosis and treatment of nervous system disorders.'
        },

        {
            'name':
                'Orthopedics',

            'icon':
                '🦴',

            'description':
                'Bone, joint and muscle treatment.'
        },

        {
            'name':
                'Pediatrics',

            'icon':
                '👶',

            'description':
                'Medical care for infants, children and adolescents.'
        },

        {
            'name':
                'Dermatology',

            'icon':
                '🧴',

            'description':
                'Skin, hair and nail care.'
        },

        {
            'name':
                'General Medicine',

            'icon':
                '🩺',

            'description':
                'General medical consultation and primary healthcare.'
        },

    ]


    return render(
        request,
        'departments.html',
        {
            'departments': departments
        }
    )