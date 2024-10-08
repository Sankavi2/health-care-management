from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from . models import *

class DoctorRegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField()
    contact_number = forms.CharField(max_length=15)
    specialization = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super(DoctorRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))
        
    class Meta:
        model = CustomUser 
        fields = ['username', 'password1', 'password2', 'date_of_birth', 'contact_number', 'specialization']
        
class PatientRegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField()
    contact_number = forms.CharField(max_length=15)

    def __init__(self, *args, **kwargs):
        super(PatientRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))

    class Meta:
        model = CustomUser 
        fields = ['username', 'password1', 'password2', 'date_of_birth', 'contact_number']
        
        
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Login'))

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = self.authenticate_user(username, password)
            if user is None or not user.is_active:
                raise forms.ValidationError("Invalid username or password. Please try again.")
        
        return cleaned_data

    def authenticate_user(self, username, password):
        try:
            user = CustomUser.objects.get(username=username)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            pass

        return None
        
class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), empty_label="Select a doctor")

    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'reason_for_visit',]
        
class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['amount', 'invoice_date']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'invoice_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        
class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['diagnosis', 'treatment_plan', 'entry_date']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'class': 'form-control'}),
            'treatment_plan': forms.Textarea(attrs={'class': 'form-control'}),
            'entry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }