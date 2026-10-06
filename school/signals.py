import time
import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import (
    Notice, BlogPost, Event, AcademicResource, TeacherStaff,
    SchoolProfile, AdmissionApplication, Facility, GalleryAlbum, SchoolAchievement, CareerVacancy,
    AcademicProgram, FAQ, Testimonial
)
from portal.push_service import broadcast_push_notification

logger = logging.getLogger(__name__)

# Track recent notifications in-memory to prevent duplicate pushes (deduplication window: 5 seconds)
_recent_push_dispatches = {}

def should_dispatch_push(dedup_key, window_seconds=5):
    now = time.time()
    last_time = _recent_push_dispatches.get(dedup_key, 0)
    if now - last_time < window_seconds:
        return False
    _recent_push_dispatches[dedup_key] = now
    # Clean up old keys
    if len(_recent_push_dispatches) > 200:
        keys_to_del = [k for k, v in _recent_push_dispatches.items() if now - v > 60]
        for k in keys_to_del:
            _recent_push_dispatches.pop(k, None)
    return True


# 1. Notice Creation / Updates / Deletions
@receiver(post_save, sender=Notice)
def notice_saved_signal(sender, instance, created, **kwargs):
    if not instance.is_published:
        return
    
    action = "New Notice" if created else "Notice Update"
    prefix = "[URGENT] " if instance.is_urgent else ""
    dedup_key = f"notice_save_{instance.id}"
    
    if should_dispatch_push(dedup_key):
        broadcast_push_notification(
            title=f"📢 {prefix}{instance.title}",
            body=instance.summary or instance.content[:140] or f"Official notice has been {'published' if created else 'updated'}.",
            url=instance.get_absolute_url() if hasattr(instance, 'get_absolute_url') else f"/notices/{instance.slug}/",
            tag=f"notice-{instance.id}",
            event_type='notice'
        )

@receiver(post_delete, sender=Notice)
def notice_deleted_signal(sender, instance, **kwargs):
    dedup_key = f"notice_del_{instance.id}"
    if should_dispatch_push(dedup_key):
        broadcast_push_notification(
            title="📢 Notice Removed",
            body=f"Notice '{instance.title}' was archived or removed.",
            url="/notices/",
            tag=f"notice-{instance.id}",
            event_type='notice_delete'
        )


# 2. Blog Post Creation / Updates / Deletions
@receiver(post_save, sender=BlogPost)
def blog_saved_signal(sender, instance, created, **kwargs):
    if not instance.is_published:
        return
    
    dedup_key = f"blog_save_{instance.id}"
    if should_dispatch_push(dedup_key):
        broadcast_push_notification(
            title=f"📰 {'New Article' if created else 'Updated Story'}: {instance.title}",
            body=instance.excerpt or instance.content[:140] or "Read the latest update from Holy Family School.",
            url=instance.get_absolute_url() if hasattr(instance, 'get_absolute_url') else f"/news-blogs/{instance.slug}/",
            tag=f"blog-{instance.id}",
            event_type='blog'
        )

@receiver(post_delete, sender=BlogPost)
def blog_deleted_signal(sender, instance, **kwargs):
    dedup_key = f"blog_del_{instance.id}"
    if should_dispatch_push(dedup_key):
        broadcast_push_notification(
            title="📰 Article Removed",
            body=f"Article '{instance.title}' was removed.",
            url="/news-blogs/",
            tag=f"blog-{instance.id}",
            event_type='blog_delete'
        )


# 3. Events Creation / Updates / Deletions
@receiver(post_save, sender=Event)
def event_saved_signal(sender, instance, created, **kwargs):
    dedup_key = f"event_save_{instance.id}"
    if should_dispatch_push(dedup_key):
        broadcast_push_notification(
            title=f"🎉 {'New School Event' if created else 'Event Update'}: {instance.title}",
            body=f"Date: {instance.event_date.strftime('%b %d, %Y')}. {instance.short_summary[:120] if instance.short_summary else ''}",
            url=instance.get_absolute_url() if hasattr(instance, 'get_absolute_url') else f"/events/{instance.slug}/",
            tag=f"event-{instance.id}",
            event_type='event'
        )

@receiver(post_delete, sender=Event)
def event_deleted_signal(sender, instance, **kwargs):
    dedup_key = f"event_del_{instance.id}"
    if should_dispatch_push(dedup_key):
        broadcast_push_notification(
            title="🎉 Event Cancelled / Removed",
            body=f"Event '{instance.title}' has been removed from the school calendar.",
            url="/events/",
            tag=f"event-{instance.id}",
            event_type='event_delete'
        )


# 4. Academic Resources (Downloads, Routines, Results, Syllabi)
@receiver(post_save, sender=AcademicResource)
def resource_saved_signal(sender, instance, created, **kwargs):
    if not instance.is_active:
        return
    
    dedup_key = f"resource_save_{instance.id}"
    if should_dispatch_push(dedup_key):
        broadcast_push_notification(
            title=f"📚 {'New Download' if created else 'Updated Resource'}: {instance.title}",
            body=f"[{instance.get_resource_type_display()}] Grade: {instance.grade_level}. Tap to download.",
            url="/academics/downloads/",
            tag=f"resource-{instance.id}",
            event_type='resource'
        )

@receiver(post_delete, sender=AcademicResource)
def resource_deleted_signal(sender, instance, **kwargs):
    dedup_key = f"resource_del_{instance.id}"
    if should_dispatch_push(dedup_key):
        broadcast_push_notification(
            title="📚 Academic Resource Removed",
            body=f"File '{instance.title}' is no longer active for download.",
            url="/academics/downloads/",
            tag=f"resource-{instance.id}",
            event_type='resource_delete'
        )


# 5. Teacher / Faculty Updates
@receiver(post_save, sender=TeacherStaff)
def teacher_saved_signal(sender, instance, created, **kwargs):
    dedup_key = f"teacher_save_{instance.id}"
    if should_dispatch_push(dedup_key):
        broadcast_push_notification(
            title=f"👨‍🏫 Faculty Update: {instance.name}",
            body=f"{instance.designation} - {instance.department}. View our faculty profile.",
            url="/faculty-staff/",
            tag=f"teacher-{instance.id}",
            event_type='teacher'
        )

@receiver(post_delete, sender=TeacherStaff)
def teacher_deleted_signal(sender, instance, **kwargs):
    dedup_key = f"teacher_del_{instance.id}"
    if should_dispatch_push(dedup_key):
        broadcast_push_notification(
            title="👨‍🏫 Faculty Member Directory Updated",
            body=f"Faculty directory updated.",
            url="/faculty-staff/",
            tag=f"teacher-{instance.id}",
            event_type='teacher_delete'
        )


# 6. Global School Profile & Urgent Announcement Banner
@receiver(post_save, sender=SchoolProfile)
def profile_saved_signal(sender, instance, created, **kwargs):
    dedup_key = f"profile_save_{instance.id}"
    if should_dispatch_push(dedup_key):
        if instance.urgent_announcement_enabled and instance.urgent_announcement_text:
            broadcast_push_notification(
                title="⚠️ Important School Announcement",
                body=instance.urgent_announcement_text,
                url=instance.urgent_announcement_link or "/",
                tag="urgent-announcement",
                event_type="urgent_banner"
            )
        else:
            broadcast_push_notification(
                title="🏫 School Profile & Information Updated",
                body=f"{instance.name}: Official school information and contacts updated.",
                url="/",
                tag="school-profile-update",
                event_type="profile_update"
            )


# 7. Admissions Applications Status Updates
@receiver(post_save, sender=AdmissionApplication)
def admission_saved_signal(sender, instance, created, **kwargs):
    dedup_key = f"admission_save_{instance.id}_{instance.status}"
    if should_dispatch_push(dedup_key):
        if created:
            logger.info(f"Admission application received: {instance.application_reference_no}")
        else:
            broadcast_push_notification(
                title=f"🎓 Admission Status Update: {instance.get_status_display()}",
                body=f"Application {instance.application_reference_no} for {instance.first_name} is now '{instance.get_status_display()}'.",
                url=f"/admissions/check-status/?ref={instance.application_reference_no}",
                tag=f"admission-{instance.application_reference_no}",
                event_type='admission_update'
            )


# 8. Academic Programs
@receiver(post_save, sender=AcademicProgram)
def program_saved_signal(sender, instance, created, **kwargs):
    dedup_key = f"program_save_{instance.id}"
    if should_dispatch_push(dedup_key):
        broadcast_push_notification(
            title=f"📖 Academic Program: {instance.name}",
            body=f"{instance.name} ({instance.code or ''}) information updated.",
            url=f"/academics/program/{instance.slug}/",
            tag=f"program-{instance.id}",
            event_type='program'
        )


# 9. Career Vacancies
@receiver(post_save, sender=CareerVacancy)
def career_saved_signal(sender, instance, created, **kwargs):
    if not instance.is_active:
        return
    dedup_key = f"career_save_{instance.id}"
    if should_dispatch_push(dedup_key):
        broadcast_push_notification(
            title=f"💼 Career Opportunity: {instance.title}",
            body=f"Department: {instance.department}. Applications open now.",
            url="/careers/",
            tag=f"career-{instance.id}",
            event_type='career'
        )


# 10. Campus Facilities & Infrastructure
@receiver(post_save, sender=Facility)
def facility_saved_signal(sender, instance, created, **kwargs):
    dedup_key = f"facility_save_{instance.id}"
    if should_dispatch_push(dedup_key):
        broadcast_push_notification(
            title=f"🏛️ Campus Infrastructure: {instance.title}",
            body=f"Explore our newly added campus facility: {instance.title}.",
            url="/about/",
            tag=f"facility-{instance.id}",
            event_type='facility'
        )


# 11. Gallery Albums & Events
@receiver(post_save, sender=GalleryAlbum)
def album_saved_signal(sender, instance, created, **kwargs):
    dedup_key = f"album_save_{instance.id}"
    if should_dispatch_push(dedup_key):
        broadcast_push_notification(
            title=f"📸 New Photo Album: {instance.title}",
            body=f"Explore new campus event photos: {instance.title}.",
            url=f"/gallery/{instance.slug}/",
            tag=f"album-{instance.id}",
            event_type='gallery'
        )


# 12. School Achievements
@receiver(post_save, sender=SchoolAchievement)
def achievement_saved_signal(sender, instance, created, **kwargs):
    dedup_key = f"achievement_save_{instance.id}"
    if should_dispatch_push(dedup_key):
        broadcast_push_notification(
            title=f"🏆 School Achievement: {instance.title}",
            body=f"{instance.description[:120] if instance.description else 'Holi Family School celebrated a new milestone!'}",
            url="/about/",
            tag=f"achievement-{instance.id}",
            event_type='achievement'
        )
