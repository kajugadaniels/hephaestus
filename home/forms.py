from django import forms
from home.models import *
from account.models import *
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'true'}))
    password_confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'true'}), label="Password Confirmation")

    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number', 'image', 'role', 'password']

    def __init__(self, *args, **kwargs):
        roles = kwargs.pop('roles', [])
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['role'].choices = [(role, role) for role in roles]
        self.fields['role'].widget.attrs.update({'class': 'form-control', 'required': 'true'})

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data