from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
#Model for forms.ModelForm, usercreation form is subclass
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = CustomUser
        fields = ("email", "full_name", "password1", "password2")
#individual forms.Form
class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True, label="Enter OTP")