from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.exceptions import ValidationError

#Model for forms.ModelForm, usercreation form is subclass
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = CustomUser
        fields = ("email", "full_name", "password1", "password2")
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password2
#individual forms.Form
class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True, label="Enter OTP")