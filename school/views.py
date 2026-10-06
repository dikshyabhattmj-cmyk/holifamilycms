from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import (
    SchoolProfile, Notice, AcademicProgram, AcademicResource,
    TeacherStaff, Facility, Event, GalleryAlbum,
    BlogPost, AdmissionApplication, CareerVacancy, FAQ, SchoolAchievement, Testimonial
)
from .forms import AdmissionForm, ContactForm, JobApplicationForm

def home_view(request):
    profile = SchoolProfile.objects.first()
    urgent_notices = Notice.objects.filter(is_published=True, is_urgent=True)[:3]
    latest_notices = Notice.objects.filter(is_published=True)[:6]
    programs = AcademicProgram.objects.filter(is_featured=True)[:4]
    upcoming_events = Event.objects.filter(is_upcoming=True)[:3]
    featured_staff = TeacherStaff.objects.filter(is_featured=True)[:4]
    featured_blogs = BlogPost.objects.filter(is_published=True, is_featured=True)[:3]
    if not featured_blogs.exists():
        featured_blogs = BlogPost.objects.filter(is_published=True)[:3]
    albums = GalleryAlbum.objects.all()[:4]
    facilities = Facility.objects.all()[:6]
    achievements = SchoolAchievement.objects.all()[:4]
    testimonials = Testimonial.objects.filter(is_featured=True)[:4]
    faqs = FAQ.objects.all()[:5]

    context = {
        'profile': profile,
        'urgent_notices': urgent_notices,
        'latest_notices': latest_notices,
        'programs': programs,
        'upcoming_events': upcoming_events,
        'featured_staff': featured_staff,
        'featured_blogs': featured_blogs,
        'albums': albums,
        'facilities': facilities,
        'achievements': achievements,
        'testimonials': testimonials,
        'faqs': faqs,
    }
    return render(request, 'school/home.html', context)


def about_view(request):
    profile = SchoolProfile.objects.first()
    achievements = SchoolAchievement.objects.all()
    facilities = Facility.objects.all()
    leadership = TeacherStaff.objects.filter(staff_type='management')
    testimonials = Testimonial.objects.all()

    context = {
        'profile': profile,
        'achievements': achievements,
        'facilities': facilities,
        'leadership': leadership,
        'testimonials': testimonials,
    }
    return render(request, 'school/about.html', context)


def principal_message_view(request):
    profile = SchoolProfile.objects.first()
    return render(request, 'school/principal_message.html', {'profile': profile})


def academics_view(request):
    programs = AcademicProgram.objects.all()
    resources = AcademicResource.objects.filter(is_active=True)
    return render(request, 'school/academics.html', {
        'programs': programs,
        'resources': resources,
    })


def program_detail_view(request, slug):
    program = get_object_or_404(AcademicProgram, slug=slug)
    subjects = program.subjects.all()
    other_programs = AcademicProgram.objects.exclude(id=program.id)
    return render(request, 'school/program_detail.html', {
        'program': program,
        'subjects': subjects,
        'other_programs': other_programs,
    })


def admissions_view(request):
    faqs = FAQ.objects.filter(category='admissions')
    if request.method == 'POST':
        form = AdmissionForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save()
            
            # Send push notification for new admission application
            from portal.push_service import broadcast_push_notification
            broadcast_push_notification(
                title=f"🎓 New Admission Application Received",
                body=f"Application #{application.application_reference_no} submitted for {application.first_name} {application.last_name} ({application.applied_grade}).",
                url=f"/admissions/check-status/?ref={application.application_reference_no}",
                tag=f"admission-new-{application.application_reference_no}",
                event_type="new_admission"
            )

            messages.success(
                request,
                f"Application submitted successfully! Your tracking reference number is: {application.application_reference_no}. Please save this for your records."
            )
            return redirect('admission_success', ref=application.application_reference_no)
        else:
            messages.error(request, "There was an error in your submission. Please check all required fields.")
    else:
        form = AdmissionForm()

    return render(request, 'school/admissions.html', {
        'form': form,
        'faqs': faqs,
    })


def admission_success_view(request, ref):
    application = get_object_or_404(AdmissionApplication, application_reference_no=ref)
    return render(request, 'school/admission_success.html', {'application': application})


def admission_status_view(request):
    application = None
    searched = False
    ref = request.GET.get('ref', '').strip()
    if ref:
        searched = True
        try:
            application = AdmissionApplication.objects.get(application_reference_no__iexact=ref)
        except AdmissionApplication.DoesNotExist:
            application = None

    return render(request, 'school/admission_status.html', {
        'application': application,
        'searched': searched,
        'ref': ref,
    })


def teachers_view(request):
    staff_type = request.GET.get('type', '')
    department = request.GET.get('dept', '')
    query = request.GET.get('q', '')

    staff_list = TeacherStaff.objects.all()

    if staff_type:
        staff_list = staff_list.filter(staff_type=staff_type)
    if department:
        staff_list = staff_list.filter(department__icontains=department)
    if query:
        staff_list = staff_list.filter(
            Q(name__icontains=query) |
            Q(designation__icontains=query) |
            Q(subject_specialization__icontains=query)
        )

    paginator = Paginator(staff_list, 12)
    page_number = request.GET.get('page')
    staff = paginator.get_page(page_number)

    departments = TeacherStaff.objects.values_list('department', flat=True).distinct()

    return render(request, 'school/teachers.html', {
        'staff': staff,
        'departments': departments,
        'selected_type': staff_type,
        'selected_dept': department,
        'query': query,
    })


def notices_view(request):
    category = request.GET.get('category', '')
    query = request.GET.get('q', '')

    notice_list = Notice.objects.filter(is_published=True)

    if category:
        notice_list = notice_list.filter(category=category)
    if query:
        notice_list = notice_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(summary__icontains=query)
        )

    paginator = Paginator(notice_list, 10)
    page_number = request.GET.get('page')
    notices = paginator.get_page(page_number)

    return render(request, 'school/notices.html', {
        'notices': notices,
        'selected_category': category,
        'query': query,
    })


def notice_detail_view(request, slug):
    notice = get_object_or_404(Notice, slug=slug, is_published=True)
    recent_notices = Notice.objects.filter(is_published=True).exclude(id=notice.id)[:5]
    return render(request, 'school/notice_detail.html', {
        'notice': notice,
        'recent_notices': recent_notices,
    })


def events_view(request):
    upcoming_events = Event.objects.filter(is_upcoming=True)
    past_events = Event.objects.filter(is_upcoming=False)
    return render(request, 'school/events.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    })


def event_detail_view(request, slug):
    event = get_object_or_404(Event, slug=slug)
    other_events = Event.objects.exclude(id=event.id)[:3]
    return render(request, 'school/event_detail.html', {
        'event': event,
        'other_events': other_events,
    })


def gallery_view(request):
    albums = GalleryAlbum.objects.all()
    return render(request, 'school/gallery.html', {'albums': albums})


def album_detail_view(request, slug):
    album = get_object_or_404(GalleryAlbum, slug=slug)
    photos = album.photos.all()
    return render(request, 'school/album_detail.html', {
        'album': album,
        'photos': photos,
    })


def blogs_view(request):
    category = request.GET.get('cat', '')
    query = request.GET.get('q', '')

    blog_list = BlogPost.objects.filter(is_published=True)

    if category:
        blog_list = blog_list.filter(category=category)
    if query:
        blog_list = blog_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        )

    paginator = Paginator(blog_list, 6)
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)

    featured_post = BlogPost.objects.filter(is_published=True, is_featured=True).first()

    return render(request, 'school/blogs.html', {
        'blogs': blogs,
        'featured_post': featured_post,
        'selected_cat': category,
        'query': query,
    })


def blog_detail_view(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug, is_published=True)
    blog.views_count += 1
    blog.save(update_fields=['views_count'])
    
    recent_blogs = BlogPost.objects.filter(is_published=True).exclude(id=blog.id)[:3]
    return render(request, 'school/blog_detail.html', {
        'blog': blog,
        'recent_blogs': recent_blogs,
    })


def careers_view(request):
    vacancies = CareerVacancy.objects.filter(is_active=True)
    return render(request, 'school/careers.html', {'vacancies': vacancies})


def career_apply_view(request, vacancy_id):
    vacancy = get_object_or_404(CareerVacancy, id=vacancy_id, is_active=True)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.vacancy = vacancy
            app.save()
            messages.success(request, f"Your application for '{vacancy.title}' has been successfully recorded. Thank you!")
            return redirect('careers')
    else:
        form = JobApplicationForm()

    return render(request, 'school/career_apply.html', {
        'vacancy': vacancy,
        'form': form,
    })


def contact_view(request):
    profile = SchoolProfile.objects.first()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been sent to school administration. We will reply promptly.")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'school/contact.html', {
        'profile': profile,
        'form': form,
    })


def global_search_view(request):
    query = request.GET.get('q', '').strip()
    results = {}
    if query:
        results['notices'] = Notice.objects.filter(is_published=True).filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )[:5]
        results['programs'] = AcademicProgram.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )[:5]
        results['blogs'] = BlogPost.objects.filter(is_published=True).filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )[:5]
        results['events'] = Event.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )[:5]
        results['staff'] = TeacherStaff.objects.filter(
            Q(name__icontains=query) | Q(designation__icontains=query) | Q(subject_specialization__icontains=query)
        )[:5]

    return render(request, 'school/search_results.html', {
        'query': query,
        'results': results,
    })


def faqs_view(request):
    faqs = FAQ.objects.all()
    return render(request, 'school/faqs.html', {'faqs': faqs})


def resources_downloads_view(request):
    resources = AcademicResource.objects.filter(is_active=True)
    return render(request, 'school/resources.html', {'resources': resources})
