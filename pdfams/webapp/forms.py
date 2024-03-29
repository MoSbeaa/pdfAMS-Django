from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Record

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from django.forms.widgets import PasswordInput, TextInput, EmailInput, DateInput, NumberInput

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


# Create Record Form
class CreateRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('Full_name', 'Date_of_birth', 'SIN', 'Date_of_hire', 'Address', 'City', 'Zip', 'State', 'Home_phone', 'Cell_phone', 'Spouse_name', 'Em_name', 'Em_relationship', 'Date')
        widgets = {
        'Date_of_birth': forms.DateInput(
            
            attrs={'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                    }),
        'Date_of_hire': forms.DateInput(
            
            attrs={'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                    }),
        'Date': forms.DateInput(
            
            attrs={'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                    }),
        'SIN': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'SIN'}),
        }

# Update Record Form
class UpdateRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        Date_of_birth = forms.DateField(widget=DateInput())
        fields = ('Full_name', 'Date_of_birth', 'SIN', 'Date_of_hire', 'Address', 'City', 'Zip', 'State', 'Home_phone', 'Cell_phone', 'Spouse_name', 'Em_name', 'Em_relationship', 'Date')
        widgets = {
        'Date_of_birth': forms.DateInput(
            
            attrs={'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                    }),
        'Date_of_hire': forms.DateInput(
            
            attrs={'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                    }),
        'Date': forms.DateInput(
            
            attrs={'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                    }),
        'SIN': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'SIN'}),    
        }