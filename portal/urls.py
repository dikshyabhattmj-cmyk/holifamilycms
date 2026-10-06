from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('login/', views.portal_login_view, name='login'),
    path('logout/', views.portal_logout_view, name='logout'),
    path('', views.dashboard_view, name='dashboard'),
    
    # Notices
    path('notices/', views.manage_notices, name='manage_notices'),
    path('notices/create/', views.create_notice, name='create_notice'),
    path('notices/edit/<int:pk>/', views.edit_notice, name='edit_notice'),
    path('notices/delete/<int:pk>/', views.delete_notice, name='delete_notice'),
    
    # Admissions
    path('admissions/', views.manage_admissions, name='manage_admissions'),
    path('admissions/view/<int:pk>/', views.view_admission_detail, name='view_admission'),
    
    # News & Blogs
    path('blogs/', views.manage_blogs, name='manage_blogs'),
    path('blogs/create/', views.create_blog, name='create_blog'),
    path('blogs/edit/<int:pk>/', views.edit_blog, name='edit_blog'),
    path('blogs/delete/<int:pk>/', views.delete_blog, name='delete_blog'),
    
    # Faculty & Staff
    path('teachers/', views.manage_teachers, name='manage_teachers'),
    path('teachers/create/', views.create_teacher, name='create_teacher'),
    path('teachers/edit/<int:pk>/', views.edit_teacher, name='edit_teacher'),
    path('teachers/delete/<int:pk>/', views.delete_teacher, name='delete_teacher'),
    
    # Messages
    path('messages/', views.manage_messages, name='manage_messages'),
    path('messages/view/<int:pk>/', views.view_message_detail, name='view_message'),
    path('messages/delete/<int:pk>/', views.delete_message, name='delete_message'),
    
    # Downloads & Resources
    path('resources/', views.manage_resources, name='manage_resources'),
    path('resources/delete/<int:pk>/', views.delete_resource, name='delete_resource'),
    
    # School Site Settings
    path('settings/', views.edit_school_settings, name='school_settings'),

    # Push Notification Control & Web Push APIs
    path('push/vapid-public-key/', views.get_vapid_public_key, name='vapid_public_key'),
    path('push/subscribe/', views.save_push_subscription, name='push_subscribe'),
    path('push/unsubscribe/', views.unsubscribe_push, name='push_unsubscribe'),
    path('push/manager/', views.push_notifications_manager, name='push_manager'),
]
