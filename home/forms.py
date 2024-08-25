from django import forms
from home.models import *
from account.models import *
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

class UserCreationForm(BaseUserCreationForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[validate_password]
    )
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number', 'image', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'true'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
        }

    def __init__(self, *args, **kwargs):
        roles = kwargs.pop('roles', None)
        super().__init__(*args, **kwargs)
        if roles:
            self.fields['role'].choices = roles

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user