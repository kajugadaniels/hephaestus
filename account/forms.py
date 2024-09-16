from home.models import *
from django import forms
from account.models import User
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=255,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Phone Number'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '**********'})
    )

    academic_year = forms.ModelChoiceField(
        queryset=AcademicYear.objects.filter(delete_status=False).order_by('-start_date'),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get('phone_number')
        password = cleaned_data.get('password')

        if phone_number and password:
            user = authenticate(phone_number=phone_number, password=password)
            if user is None:
                raise forms.ValidationError("Invalid phone number or password")
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False