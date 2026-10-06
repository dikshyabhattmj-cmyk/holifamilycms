from django import forms
from django.contrib.auth.forms import AuthenticationForm
from school.models import (
    Notice, BlogPost, Event, TeacherStaff, AdmissionApplication,
    SchoolProfile, AcademicResource, Facility, GalleryAlbum
)

class PortalLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Admin Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password'}))


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'category', 'publish_date', 'summary', 'content', 'attachment', 'is_pinned', 'is_urgent', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'publish_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
            'is_pinned': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_urgent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'category', 'author_name', 'author_role', 'published_date', 'excerpt', 'content', 'featured_image', 'is_published', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'author_name': forms.TextInput(attrs={'class': 'form-control'}),
            'author_role': forms.TextInput(attrs={'class': 'form-control'}),
            'published_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'event_date', 'start_time', 'end_time', 'location', 'short_summary', 'description', 'featured_image', 'is_upcoming', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'event_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '09:00 AM'}),
            'end_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '03:00 PM'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'short_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_upcoming': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TeacherStaffForm(forms.ModelForm):
    class Meta:
        model = TeacherStaff
        fields = ['name', 'staff_type', 'designation', 'department', 'qualification', 'experience_years', 'subject_specialization', 'bio', 'photo', 'email', 'phone', 'order', 'is_featured']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'staff_type': forms.Select(attrs={'class': 'form-select'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'subject_specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AdmissionStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = AdmissionApplication
        fields = ['status', 'admin_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'admin_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Internal notes on interview date, entrance exam scores, or fee clearance...'}),
        }


class SchoolProfileEditForm(forms.ModelForm):
    class Meta:
        model = SchoolProfile
        fields = [
            'name', 'tagline', 'short_intro', 'established_year', 'affiliation',
            'phone_primary', 'phone_secondary', 'email_primary', 'email_admissions',
            'address', 'office_hours', 'facebook_url', 'twitter_url', 'instagram_url', 'youtube_url',
            'urgent_announcement_enabled', 'urgent_announcement_text', 'urgent_announcement_link',
            'hero_title', 'hero_subtitle', 'hero_banner_image',
            'principal_name', 'principal_designation', 'principal_message', 'principal_photo',
            'stat_students_count', 'stat_teachers_count', 'stat_pass_rate', 'stat_awards_count',
            'vision', 'mission', 'objectives', 'history', 'core_values'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'tagline': forms.TextInput(attrs={'class': 'form-control'}),
            'short_intro': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'established_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'affiliation': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_primary': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_secondary': forms.TextInput(attrs={'class': 'form-control'}),
            'email_primary': forms.EmailInput(attrs={'class': 'form-control'}),
            'email_admissions': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'office_hours': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook_url': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter_url': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-control'}),
            'youtube_url': forms.URLInput(attrs={'class': 'form-control'}),
            'urgent_announcement_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'urgent_announcement_text': forms.TextInput(attrs={'class': 'form-control'}),
            'urgent_announcement_link': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_title': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_subtitle': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'hero_banner_image': forms.FileInput(attrs={'class': 'form-control'}),
            'principal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'principal_designation': forms.TextInput(attrs={'class': 'form-control'}),
            'principal_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'principal_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'stat_students_count': forms.TextInput(attrs={'class': 'form-control'}),
            'stat_teachers_count': forms.TextInput(attrs={'class': 'form-control'}),
            'stat_pass_rate': forms.TextInput(attrs={'class': 'form-control'}),
            'stat_awards_count': forms.TextInput(attrs={'class': 'form-control'}),
            'vision': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'mission': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'history': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'core_values': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AcademicResourceForm(forms.ModelForm):
    class Meta:
        model = AcademicResource
        fields = ['title', 'resource_type', 'grade_level', 'file', 'description', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'resource_type': forms.Select(attrs={'class': 'form-select'}),
            'grade_level': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['title', 'category', 'icon_class', 'short_description', 'image', 'order']


class AlbumForm(forms.ModelForm):
    class Meta:
        model = GalleryAlbum
        fields = ['title', 'description', 'cover_image', 'event_date']
