

from .models import SchoolProfile, Notice

def school_global_context(request):
    """
    Supplies school profile info, latest urgent banner, and global stats across all templates.
    """
    school_info = SchoolProfile.objects.first()
    recent_notices = Notice.objects.filter(is_published=True)[:5]
    
    return {
        'school_info': school_info,
        'global_recent_notices': recent_notices,
    }
