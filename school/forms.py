from django import forms
from .models import AdmissionApplication, ContactMessage, JobApplication

class AdmissionForm(forms.ModelForm):
    class Meta:
        model = AdmissionApplication
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender', 'applied_grade',
            'previous_school', 'previous_gpa_or_grade',
            'guardian_name', 'guardian_relationship', 'guardian_phone', 'guardian_email',
            'guardian_occupation', 'residential_address',
            'birth_certificate', 'previous_marksheet', 'student_photo', 'statement_or_notes'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'applied_grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Grade 1, Grade 9, +2 Science'}),
            'previous_school': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Previous School Name'}),
            'previous_gpa_or_grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., GPA 3.8 / 85%'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name of Parent/Guardian'}),
            'guardian_relationship': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Father, Mother, Local Guardian'}),
            'guardian_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+977-98XXXXXXXX'}),
            'guardian_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'parent@example.com'}),
            'guardian_occupation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Occupation'}),
            'residential_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Full residential street address'}),
            'statement_or_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special health, dietary, or learning needs'}),
            'birth_certificate': forms.FileInput(attrs={'class': 'form-control'}),
            'previous_marksheet': forms.FileInput(attrs={'class': 'form-control'}),
            'student_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['full_name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Phone Number'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject / Inquiry topic'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your message or inquiry here...'}),
        }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['full_name', 'email', 'phone', 'qualification', 'years_of_experience', 'resume', 'cover_letter']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Legal Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Highest Qualification (e.g. M.Sc. Physics)'}),
            'years_of_experience': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 4 Years'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'cover_letter': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Introduce yourself and state your teaching philosophy...'}),
        }
