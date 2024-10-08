from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from . forms import *
from . models import *
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

def index(request):
    return render(request,'index.html')
def doctor_signup(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
        
            Doctor.objects.create(
                user=user,
                first_name=user.username,
                last_name="",
                specialization=form.cleaned_data.get('specialization'),
                contact_number=form.cleaned_data.get('contact_number')
                # Add more fields as needed
            )

            return redirect('login')  # Customize the success redirect URL
    else:
        form = DoctorRegistrationForm()

    return render(request, 'registration/doctor_signup.html', {'form': form})


def patient_signup(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Patient.objects.create(
                user=user,
                first_name=user.username,
                last_name="",
                date_of_birth=form.cleaned_data.get('date_of_birth'),
                contact_number=form.cleaned_data.get('contact_number')
                # Add more fields as needed
            )
            return redirect('login')  
    else:
        form = PatientRegistrationForm()

    return render(request, 'registration/patient_signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Redirect based on user type
            if user.user_type == 'Doctor':
                return redirect('doctor_dashboard')
            elif user.user_type == 'Patient':
                return redirect('patient_dashboard') 
    else:
        form = UserLoginForm()

    return render(request, 'registration/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect(reverse('index'))


def patient_dashboard(request):
    appointments = Appointment.objects.filter(patient=request.user.patient)
    doctors = Doctor.objects.all()
    billing_records = Billing.objects.filter(patient=request.user.patient)
    medical_records = MedicalRecord.objects.filter(patient=request.user.patient)
    
    return render(request, 'patient_dashboard.html', {
        'appointments': appointments,
        'doctors': doctors,
        'billing_records': billing_records,
        'medical_records': medical_records,
    })

def apply_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.save()
            messages.success(request, 'Appointment request submitted successfully!')
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()

    return render(request, 'apply_appointment.html', {'form': form})


def doctor_dashboard(request):
    appointments = Appointment.objects.filter(doctor=request.user.doctor)
    medical_records = MedicalRecord.objects.filter(doctor=request.user.doctor)

    return render(request, 'doctor_dashboard.html', {'appointments': appointments, 'medical_records': medical_records})

def patient_details(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    appointments = Appointment.objects.filter(patient=patient)
    medical_records = MedicalRecord.objects.filter(patient=patient)

    return render(request, 'patient_details.html', {'patient': patient, 'appointments': appointments, 'medical_records': medical_records})

def accept_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = Appointment.Status.ACCEPTED
    appointment.save()
    return redirect('doctor_dashboard')

def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = Appointment.Status.CANCELED
    appointment.save()
    return redirect('doctor_dashboard')

def generate_bill(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            billing = form.save(commit=False)
            billing.patient = patient
            billing.doctor = request.user.doctor  # Assuming the logged-in user is a doctor
            billing.save()
            return redirect('patient_details', patient_id=patient_id)
    else:
        form = BillingForm()

    return render(request, 'generate_medical_record.html', {'form': form, 'patient': patient})

def generate_medical_record(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.patient = patient
            medical_record.doctor = request.user.doctor  # Assuming the logged-in user is a doctor
            medical_record.save()
            return redirect('patient_details', patient_id=patient_id)
    else:
        form = MedicalRecordForm()

    return render(request, 'generate_medical_record.html', {'form': form, 'patient': patient})