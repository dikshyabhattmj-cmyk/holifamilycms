import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from school.models import (
    SchoolProfile, Notice, AcademicProgram, TeacherStaff, Event,
    GalleryAlbum, GalleryPhoto, BlogPost, AdmissionApplication,
    CareerVacancy, JobApplication, ContactMessage, AcademicResource, FAQ
)
from .models import AdminAuditLog, PushSubscription, NotificationLog
from .forms import (
    PortalLoginForm, NoticeForm, BlogPostForm, EventForm,
    TeacherStaffForm, AdmissionStatusUpdateForm, SchoolProfileEditForm,
    AcademicResourceForm, FacilityForm, AlbumForm
)
from .push_service import broadcast_push_notification

def portal_login_view(request):
    if request.user.is_authenticated:
        return redirect('portal:dashboard')
        
    if request.method == 'POST':
        form = PortalLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Log successful login
            AdminAuditLog.objects.create(
                user=user,
                action="User logged into Admin Portal",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            return redirect('portal:dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = PortalLoginForm()

    return render(request, 'portal/login.html', {'form': form})


def portal_logout_view(request):
    if request.user.is_authenticated:
        AdminAuditLog.objects.create(
            user=request.user,
            action="User logged out of Admin Portal",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        logout(request)
        messages.info(request, "You have been logged out securely.")
    return redirect('portal:login')


@login_required
def dashboard_view(request):
    total_applications = AdmissionApplication.objects.count()
    pending_applications = AdmissionApplication.objects.filter(status='pending').count()
    total_notices = Notice.objects.count()
    total_messages = ContactMessage.objects.filter(is_read=False).count()
    total_vacancies = CareerVacancy.objects.filter(is_active=True).count()
    total_blogs = BlogPost.objects.count()
    total_events = Event.objects.count()
    total_teachers = TeacherStaff.objects.count()
    active_subscriptions = PushSubscription.objects.filter(is_active=True).count()

    recent_applications = AdmissionApplication.objects.all()[:6]
    recent_messages = ContactMessage.objects.all()[:5]
    audit_logs = AdminAuditLog.objects.all()[:8]
    recent_notifications = NotificationLog.objects.all()[:5]

    context = {
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'total_notices': total_notices,
        'total_messages': total_messages,
        'total_vacancies': total_vacancies,
        'total_blogs': total_blogs,
        'total_events': total_events,
        'total_teachers': total_teachers,
        'active_subscriptions': active_subscriptions,
        'recent_applications': recent_applications,
        'recent_messages': recent_messages,
        'audit_logs': audit_logs,
        'recent_notifications': recent_notifications,
    }
    return render(request, 'portal/dashboard.html', context)


# --- Notices Management ---
@login_required
def manage_notices(request):
    notices = Notice.objects.all()
    return render(request, 'portal/notices_list.html', {'notices': notices})

@login_required
def create_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save()
            AdminAuditLog.objects.create(
                user=request.user,
                action=f"Created Notice: {notice.title}",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            # Broadcast Push Notification if published
            if notice.is_published:
                prefix = "[URGENT] " if notice.is_urgent else ""
                broadcast_push_notification(
                    title=f"📢 {prefix}{notice.title}",
                    body=notice.summary or notice.content[:140],
                    url=notice.get_absolute_url() if hasattr(notice, 'get_absolute_url') else f"/notices/{notice.slug}/",
                    tag=f"notice-{notice.id}",
                    event_type='notice'
                )

            messages.success(request, "Notice created and push notification broadcasted successfully!")
            return redirect('portal:manage_notices')
    else:
        form = NoticeForm()
    return render(request, 'portal/notice_form.html', {'form': form, 'title': 'Publish New Notice'})

@login_required
def edit_notice(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            saved_notice = form.save()
            AdminAuditLog.objects.create(
                user=request.user,
                action=f"Updated Notice: {saved_notice.title}",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, "Notice updated successfully!")
            return redirect('portal:manage_notices')
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'portal/notice_form.html', {'form': form, 'title': 'Edit Notice'})

@login_required
def delete_notice(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    title = notice.title
    notice.delete()
    AdminAuditLog.objects.create(
        user=request.user,
        action=f"Deleted Notice: {title}",
        ip_address=request.META.get('REMOTE_ADDR')
    )
    messages.success(request, f"Notice '{title}' deleted successfully.")
    return redirect('portal:manage_notices')


# --- Admissions Management ---
@login_required
def manage_admissions(request):
    status_filter = request.GET.get('status', '')
    apps = AdmissionApplication.objects.all()
    if status_filter:
        apps = apps.filter(status=status_filter)
    return render(request, 'portal/admissions_list.html', {'applications': apps, 'status_filter': status_filter})

@login_required
def view_admission_detail(request, pk):
    app = get_object_or_404(AdmissionApplication, pk=pk)
    if request.method == 'POST':
        old_status = app.status
        form = AdmissionStatusUpdateForm(request.POST, instance=app)
        if form.is_valid():
            updated_app = form.save()
            AdminAuditLog.objects.create(
                user=request.user,
                action=f"Updated Admission Status for {updated_app.first_name} ({updated_app.application_reference_no}) to {updated_app.status}",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            # Send Push Notification if status changed
            if old_status != updated_app.status:
                broadcast_push_notification(
                    title=f"🎓 Admission Status Update: {updated_app.get_status_display()}",
                    body=f"Application {updated_app.application_reference_no} for {updated_app.first_name} is now '{updated_app.get_status_display()}'.",
                    url=f"/admissions/check-status/?ref={updated_app.application_reference_no}",
                    tag=f"admission-{updated_app.application_reference_no}",
                    event_type='admission_update'
                )

            messages.success(request, "Application status updated and notification triggered.")
            return redirect('portal:view_admission', pk=pk)
    else:
        form = AdmissionStatusUpdateForm(instance=app)
    return render(request, 'portal/admission_detail.html', {'application': app, 'form': form})


# --- Blogs Management ---
@login_required
def manage_blogs(request):
    blogs = BlogPost.objects.all()
    return render(request, 'portal/blogs_list.html', {'blogs': blogs})

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save()
            AdminAuditLog.objects.create(
                user=request.user,
                action=f"Created Blog Post: {blog.title}",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            if blog.is_published:
                broadcast_push_notification(
                    title=f"📰 New Article: {blog.title}",
                    body=blog.excerpt or blog.content[:140],
                    url=blog.get_absolute_url() if hasattr(blog, 'get_absolute_url') else f"/news-blogs/{blog.slug}/",
                    tag=f"blog-{blog.id}",
                    event_type='blog'
                )

            messages.success(request, "Blog post published and subscribers notified!")
            return redirect('portal:manage_blogs')
    else:
        form = BlogPostForm()
    return render(request, 'portal/blog_form.html', {'form': form, 'title': 'Create New Article'})

@login_required
def edit_blog(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            AdminAuditLog.objects.create(
                user=request.user,
                action=f"Updated Blog Post: {blog.title}",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, "Blog post updated successfully!")
            return redirect('portal:manage_blogs')
    else:
        form = BlogPostForm(instance=blog)
    return render(request, 'portal/blog_form.html', {'form': form, 'title': 'Edit Article'})

@login_required
def delete_blog(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    blog.delete()
    messages.success(request, "Blog post deleted.")
    return redirect('portal:manage_blogs')


# --- Teachers Management ---
@login_required
def manage_teachers(request):
    staff_list = TeacherStaff.objects.all()
    return render(request, 'portal/teachers_list.html', {'staff_list': staff_list})

@login_required
def create_teacher(request):
    if request.method == 'POST':
        form = TeacherStaffForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, f"Faculty profile for {teacher.name} created successfully.")
            return redirect('portal:manage_teachers')
    else:
        form = TeacherStaffForm()
    return render(request, 'portal/teacher_form.html', {'form': form, 'title': 'Add Faculty / Staff Member'})

@login_required
def edit_teacher(request, pk):
    teacher = get_object_or_404(TeacherStaff, pk=pk)
    if request.method == 'POST':
        form = TeacherStaffForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, f"Faculty profile for {teacher.name} updated.")
            return redirect('portal:manage_teachers')
    else:
        form = TeacherStaffForm(instance=teacher)
    return render(request, 'portal/teacher_form.html', {'form': form, 'title': 'Edit Faculty Profile'})

@login_required
def delete_teacher(request, pk):
    teacher = get_object_or_404(TeacherStaff, pk=pk)
    teacher.delete()
    messages.success(request, "Faculty profile removed.")
    return redirect('portal:manage_teachers')


# --- Contact Inquiries Management ---
@login_required
def manage_messages(request):
    msgs = ContactMessage.objects.all()
    return render(request, 'portal/messages_list.html', {'messages_list': msgs})

@login_required
def view_message_detail(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if not msg.is_read:
        msg.is_read = True
        msg.save(update_fields=['is_read'])
    return render(request, 'portal/message_detail.html', {'msg': msg})

@login_required
def delete_message(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.delete()
    messages.success(request, "Message deleted.")
    return redirect('portal:manage_messages')


# --- School Profile & Global Settings ---
@login_required
def edit_school_settings(request):
    profile = SchoolProfile.objects.first()
    old_announcement_enabled = profile.urgent_announcement_enabled if profile else False
    old_announcement_text = profile.urgent_announcement_text if profile else ""

    if request.method == 'POST':
        form = SchoolProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            saved_profile = form.save()
            AdminAuditLog.objects.create(
                user=request.user,
                action="Updated School Profile, Banner & Contact Settings",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            # Broadcast push if urgent banner was newly enabled or changed
            if saved_profile.urgent_announcement_enabled and (
                not old_announcement_enabled or saved_profile.urgent_announcement_text != old_announcement_text
            ):
                broadcast_push_notification(
                    title="⚠️ Important School Announcement",
                    body=saved_profile.urgent_announcement_text,
                    url=saved_profile.urgent_announcement_link or "/",
                    tag="urgent-announcement",
                    event_type="urgent_banner"
                )

            messages.success(request, "School settings saved and push notification updated.")
            return redirect('portal:school_settings')
    else:
        form = SchoolProfileEditForm(instance=profile)
    return render(request, 'portal/school_settings.html', {'form': form, 'profile': profile})


# --- Academic Downloads Management ---
@login_required
def manage_resources(request):
    resources = AcademicResource.objects.all()
    if request.method == 'POST':
        form = AcademicResourceForm(request.POST, request.FILES)
        if form.is_valid():
            res = form.save()
            
            # Broadcast new academic resource (e.g. routine, result, syllabus)
            broadcast_push_notification(
                title=f"📚 New Download Available: {res.title}",
                body=f"[{res.get_resource_type_display()}] Grade: {res.grade_level}. Tap to access now.",
                url="/academics/downloads/",
                tag=f"resource-{res.id}",
                event_type="resource"
            )

            messages.success(request, "Document uploaded and published.")
            return redirect('portal:manage_resources')
    else:
        form = AcademicResourceForm()
    return render(request, 'portal/resources_list.html', {'resources': resources, 'form': form})

@login_required
def delete_resource(request, pk):
    res = get_object_or_404(AcademicResource, pk=pk)
    res.delete()
    messages.success(request, "Resource deleted.")
    return redirect('portal:manage_resources')


# ==========================================
# --- Web Push & PWA API Endpoints ---
# ==========================================

def get_vapid_public_key(request):
    """
    Returns the VAPID public key so client browsers can generate push subscriptions.
    """
    public_key = getattr(settings, 'WEBPUSH_VAPID_PUBLIC_KEY', '')
    return JsonResponse({'publicKey': public_key})


@csrf_exempt
def save_push_subscription(request):
    """
    Registers or updates a browser PushSubscription endpoint.
    Accepts JSON payload: { endpoint, keys: { p256dh, auth }, userAgent }
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        endpoint = data.get('endpoint', '').strip()
        keys = data.get('keys', {})
        p256dh = keys.get('p256dh', '').strip()
        auth = keys.get('auth', '').strip()
        user_agent = data.get('userAgent', request.META.get('HTTP_USER_AGENT', ''))

        if not endpoint or not p256dh or not auth:
            return JsonResponse({'error': 'Missing endpoint or encryption keys'}, status=400)

        user = request.user if request.user.is_authenticated else None

        sub, created = PushSubscription.objects.update_or_create(
            endpoint=endpoint,
            defaults={
                'user': user,
                'p256dh': p256dh,
                'auth': auth,
                'user_agent': user_agent,
                'is_active': True
            }
        )

        return JsonResponse({'status': 'success', 'created': created, 'id': sub.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def unsubscribe_push(request):
    """
    Deactivates or removes a push subscription endpoint.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        endpoint = data.get('endpoint', '').strip()
        if endpoint:
            PushSubscription.objects.filter(endpoint=endpoint).delete()
        return JsonResponse({'status': 'unsubscribed'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def push_notifications_manager(request):
    """
    Admin control center to monitor subscriptions, view delivery logs, and send custom broadcasts.
    """
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        body = request.POST.get('body', '').strip()
        url = request.POST.get('url', '/').strip() or '/'
        tag = request.POST.get('tag', 'hf-admin-broadcast').strip() or 'hf-admin-broadcast'

        if title and body:
            broadcast_push_notification(
                title=title,
                body=body,
                url=url,
                tag=tag,
                event_type='custom_broadcast'
            )
            AdminAuditLog.objects.create(
                user=request.user,
                action=f"Sent Custom Push Broadcast: {title}",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, f"Push notification '{title}' queued for instant real-time broadcast!")
            return redirect('portal:push_manager')
        else:
            messages.error(request, "Please provide both title and body for the push notification.")

    subscriptions = PushSubscription.objects.filter(is_active=True)
    logs = NotificationLog.objects.all()[:30]

    return render(request, 'portal/push_manager.html', {
        'subscriptions': subscriptions,
        'logs': logs,
        'total_subscribers': subscriptions.count(),
    })

