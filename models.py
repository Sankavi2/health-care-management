from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('Patient', 'Patient'),
        ('Doctor', 'Doctor'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='Patient')

class Patient(models.Model):
    user = models.OneToOneField(CustomUser(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=15)
    # Add more fields for patient information

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Doctor(models.Model):
    user = models.OneToOneField(CustomUser(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    # Add more fields for doctor information

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"
    
    def get_upcoming_appointments(self):
        return Appointment.objects.filter(doctor=self, appointment_date__gte=timezone.now()).order_by('appointment_date')[:5]
    
class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        ACCEPTED = 'Accepted', 'Accepted'
        CANCELED = 'Canceled', 'Canceled'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    reason_for_visit = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    # Add more fields for appointment details

    def __str__(self):
        return f"Appointment for {self.patient} with Dr. {self.doctor} on {self.appointment_date} - Status: {self.status}"
    
class Billing(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_date = models.DateField()
    # Add more fields for billing details

    def __str__(self):
        return f"Billing for {self.patient} from Dr. {self.doctor} - Amount: {self.amount}"
    
class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    entry_date = models.DateField()
    # Add more fields for medical record details

    def __str__(self):
        return f"Medical Record for {self.patient} by Dr. {self.doctor} - Date: {self.entry_date}"