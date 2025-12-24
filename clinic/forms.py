# clinic/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# ✅ User Registration Form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']

# ✅ Contact Form for the Contact Us page
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=150)
    message = forms.CharField(widget=forms.Textarea)
