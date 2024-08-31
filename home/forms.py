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

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['employee_id', 'date_of_birth', 'gender', 'nationality', 'national_id', 'marital_status',
                  'alternative_phone_number', 'address', 'position', 'department', 'employment_status',
                  'date_joined', 'years_of_experience', 'highest_degree', 'major', 'institution',
                  'graduation_year', 'certifications', 'skills', 'subjects_taught', 'classes_assigned',
                  'emergency_contact_name', 'emergency_contact_relationship', 'emergency_contact_phone',
                  'bio', 'achievements']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'true'}),
            'gender': forms.Select(attrs={'class': 'form-control select2', 'required': 'true'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'marital_status': forms.Select(attrs={'class': 'form-control select2', 'required': 'true'}),
            'alternative_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'employment_status': forms.Select(attrs={'class': 'form-control select2', 'required': 'true'}),
            'date_joined': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'true'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'highest_degree': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'major': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'institution': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'graduation_year': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'certifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional'}),
            'subjects_taught': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': 'true'}),
            'classes_assigned': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': 'true'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'emergency_contact_relationship': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional'}),
            'achievements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional'}),
        }

class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ['academic_year', 'name', 'start_date', 'end_date']
        widgets = {
            'academic_year': forms.Select(attrs={'class': 'form-control select2', 'required': 'true'}),
            'name': forms.Select(attrs={'class': 'form-control select2', 'required': 'true'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'true'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'true'}),
        }

class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = ['name', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'true'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'true'}),
        }

class ClassForm(forms.ModelForm):
    # students = forms.ModelMultipleChoiceField(
    #     queryset=Student.objects.filter(delete_status=False),
    #     required=False
    # )

    class Meta:
        model = Class
        fields = ['name', 'grade', 'section', 'head_teacher', 'students', 'capacity', 'academic_year']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'grade': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'section': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
        }

    def __init__(self, *args, **kwargs):
        super(ClassForm, self).__init__(*args, **kwargs)
        self.fields['head_teacher'].queryset = Teacher.objects.filter(delete_status=False)
        self.fields['academic_year'].queryset = AcademicYear.objects.filter(delete_status=False)

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ClassSubjectForm(forms.ModelForm):
    class Meta:
        model = ClassSubject
        fields = ['subject', 'teacher', 'starting_hour', 'ending_hour']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control js-example-basic-single'}),
            'teacher': forms.Select(attrs={'class': 'form-control js-example-basic-single'}),
            'starting_hour': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'ending_hour': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super(ClassSubjectForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.filter(delete_status=False)
        self.fields['teacher'].queryset = Teacher.objects.filter(delete_status=False)