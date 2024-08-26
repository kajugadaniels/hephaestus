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

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'image', 'dob', 'gender', 'current_status', 'nationality',
                  'cell', 'village', 'sector', 'district', 'emergency_contact_name',
                  'emergency_contact_relation', 'emergency_contact_phone',
                  'medical_conditions', 'allergies', 'special_needs', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'true'}),
            'gender': forms.Select(attrs={'class': 'form-control select2', 'required': 'true'}),
            'current_status': forms.Select(attrs={'class': 'form-control select2', 'required': 'true'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'cell': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'village': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'sector': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'emergency_contact_relation': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'medical_conditions': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
            'special_needs': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super(StudentForm, self).__init__(*args, **kwargs)
    #     self.fields['image'].required = False

    # def clean_image(self):
    #     image = self.cleaned_data.get('image')
    #     if image:
    #         if image.size > 5 * 1024 * 1024:  # 5MB limit
    #             raise forms.ValidationError("Image file too large ( > 5MB )")
    #         if image.content_type not in ['image/jpeg', 'image/png', 'image/webp']:
    #             raise forms.ValidationError("Please upload a JPEG, PNG or WebP image.")
    #     return image