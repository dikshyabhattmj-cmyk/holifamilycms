from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('about/principal-message/', views.principal_message_view, name='principal_message'),
    
    path('academics/', views.academics_view, name='academics'),
    path('academics/program/<slug:slug>/', views.program_detail_view, name='program_detail'),
    path('academics/downloads/', views.resources_downloads_view, name='downloads'),
    
    path('admissions/', views.admissions_view, name='admissions'),
    path('admissions/success/<str:ref>/', views.admission_success_view, name='admission_success'),
    path('admissions/check-status/', views.admission_status_view, name='admission_status'),
    
    path('faculty-staff/', views.teachers_view, name='teachers'),
    
    path('notices/', views.notices_view, name='notices'),
    path('notices/<slug:slug>/', views.notice_detail_view, name='notice_detail'),
    
    path('events/', views.events_view, name='events'),
    path('events/<slug:slug>/', views.event_detail_view, name='event_detail'),
    
    path('gallery/', views.gallery_view, name='gallery'),
    path('gallery/<slug:slug>/', views.album_detail_view, name='album_detail'),
    
    path('news-blogs/', views.blogs_view, name='blogs'),
    path('news-blogs/<slug:slug>/', views.blog_detail_view, name='blog_detail'),
    
    path('careers/', views.careers_view, name='careers'),
    path('careers/apply/<int:vacancy_id>/', views.career_apply_view, name='career_apply'),
    
    path('contact/', views.contact_view, name='contact'),
    path('faqs/', views.faqs_view, name='faqs'),
    path('search/', views.global_search_view, name='search'),
]
