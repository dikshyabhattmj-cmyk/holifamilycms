from django.contrib import admin
from .models import (
    SchoolProfile, Notice, AcademicProgram, AcademicSubject, AcademicResource,
    TeacherStaff, Facility, Event, GalleryAlbum, GalleryPhoto,
    BlogPost, AdmissionApplication, CareerVacancy, JobApplication,
    ContactMessage, FAQ, SchoolAchievement, Testimonial
)

@admin.register(SchoolProfile)
class SchoolProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'established_year', 'phone_primary', 'email_primary', 'urgent_announcement_enabled')

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'publish_date', 'is_pinned', 'is_urgent', 'is_published')
    list_filter = ('category', 'is_pinned', 'is_urgent', 'is_published', 'publish_date')
    search_fields = ('title', 'content', 'summary')
    prepopulated_fields = {'slug': ('title',)}

class SubjectInline(admin.TabularInline):
    model = AcademicSubject
    extra = 2

@admin.register(AcademicProgram)
class AcademicProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'level_code', 'order', 'is_featured')
    list_editable = ('order', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubjectInline]

@admin.register(AcademicResource)
class AcademicResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'grade_level', 'uploaded_at', 'is_active')
    list_filter = ('resource_type', 'grade_level', 'is_active')
    search_fields = ('title', 'description')

@admin.register(TeacherStaff)
class TeacherStaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'staff_type', 'department', 'experience_years', 'order', 'is_featured')
    list_filter = ('staff_type', 'department', 'is_featured')
    search_fields = ('name', 'designation', 'subject_specialization')
    list_editable = ('order', 'is_featured')

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'icon_class', 'order')
    list_editable = ('order',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'start_time', 'location', 'is_upcoming', 'is_featured')
    list_filter = ('is_upcoming', 'is_featured', 'event_date')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

class PhotoInline(admin.TabularInline):
    model = GalleryPhoto
    extra = 3

@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PhotoInline]

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author_name', 'published_date', 'is_published', 'is_featured', 'views_count')
    list_filter = ('category', 'is_published', 'is_featured', 'published_date')
    search_fields = ('title', 'content', 'author_name')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = ('application_reference_no', 'first_name', 'last_name', 'applied_grade', 'guardian_phone', 'status', 'created_at')
    list_filter = ('status', 'applied_grade', 'gender', 'created_at')
    search_fields = ('application_reference_no', 'first_name', 'last_name', 'guardian_name', 'guardian_phone', 'guardian_email')
    readonly_fields = ('application_reference_no', 'created_at')

@admin.register(CareerVacancy)
class CareerVacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'job_type', 'open_positions', 'deadline', 'is_active')
    list_filter = ('job_type', 'department', 'is_active')
    search_fields = ('title', 'description', 'requirements')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'vacancy', 'phone', 'email', 'years_of_experience', 'created_at')
    list_filter = ('vacancy', 'created_at')
    search_fields = ('full_name', 'email', 'phone')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('full_name', 'email', 'subject', 'message')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order')
    list_filter = ('category',)
    list_editable = ('order',)

@admin.register(SchoolAchievement)
class SchoolAchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'category', 'order')
    list_filter = ('year', 'category')
    list_editable = ('order',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'role', 'relation_or_batch', 'rating', 'is_featured')
    list_filter = ('role', 'is_featured')
