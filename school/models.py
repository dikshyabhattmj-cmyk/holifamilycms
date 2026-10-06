from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User

class SchoolProfile(models.Model):
    name = models.CharField(max_length=200, default="Holi Family Secondary School")
    tagline = models.CharField(max_length=255, default="Excellence in Education, Character, & Leadership")
    short_intro = models.TextField(default="Empowering young minds through holistic education, state-of-the-art facilities, and strong moral grounding.")
    established_year = models.PositiveIntegerField(default=1995)
    affiliation = models.CharField(max_length=200, default="National Examination Board (NEB) & Ministry of Education")
    
    # Contact Info
    address = models.CharField(max_length=255, default="Main Academic Avenue, Kathmandu, Nepal")
    phone_primary = models.CharField(max_length=50, default="+977-1-4567890")
    phone_secondary = models.CharField(max_length=50, blank=True, null=True, default="+977-1-4567891")
    email_primary = models.EmailField(default="info@holifamily.edu.np")
    email_admissions = models.EmailField(default="admissions@holifamily.edu.np")
    office_hours = models.CharField(max_length=100, default="Sunday - Friday: 8:00 AM - 4:30 PM")
    google_maps_embed_url = models.TextField(blank=True, default="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d14128.527376883253!2d85.3188!3d27.7172!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMjfCsDQzJzAyLjAiTiA4NcKwMTknMDcuNyJF!5e0!3m2!1sen!2snp!4v1650000000000!5m2!1sen!2snp")
    
    # Social Links
    facebook_url = models.URLField(blank=True, default="https://facebook.com/holifamilyschool")
    twitter_url = models.URLField(blank=True, default="https://twitter.com/holifamily")
    instagram_url = models.URLField(blank=True, default="https://instagram.com/holifamilyschool")
    youtube_url = models.URLField(blank=True, default="https://youtube.com/@holifamily")
    linkedin_url = models.URLField(blank=True, default="https://linkedin.com/school/holifamily")
    
    # Vision, Mission, Journey
    vision = models.TextField(default="To nurture disciplined, curious, and empathetic future leaders who thrive globally while staying deeply rooted in values.")
    mission = models.TextField(default="To deliver rigorous academic standards, foster creative innovation, support physical wellness, and instill unwavering integrity.")
    objectives = models.TextField(default="Cultivate intellectual curiosity; instil moral values and civic responsibility; promote digital and scientific literacy; nurture athletic and cultural talents.")
    history = models.TextField(default="Founded with a modest classroom and a profound dream in 1995, Holi Family Secondary School has grown into a premier institution educating over 2,500 students with a heritage of 100% academic excellence.")
    core_values = models.TextField(default="Integrity, Innovation, Respect, Compassion, Resilience, and Lifelong Learning.")

    # Principal's Desk
    principal_name = models.CharField(max_length=150, default="Dr. Sarah Jenkins, Ph.D.")
    principal_designation = models.CharField(max_length=150, default="Principal & Academic Director")
    principal_message = models.TextField(default="Welcome to Holi Family Secondary School. For nearly three decades, our institution has stood as a beacon of academic rigor and character formation. We believe every child arrives with unique potential waiting to be ignited. Our faculty, modern learning spaces, and comprehensive co-curricular programs ensure our graduates step into the world with confidence and purpose.")
    principal_photo = models.ImageField(upload_to='school/principal/', blank=True, null=True)

    # Hero Banner Assets
    hero_title = models.CharField(max_length=200, default="Inspiring Excellence, Nurturing Character")
    hero_subtitle = models.CharField(max_length=300, default="A world-class co-educational sanctuary shaping thinkers, innovators, and leaders for tomorrow.")
    hero_banner_image = models.ImageField(upload_to='school/hero/', blank=True, null=True)
    
    # Statistics / Counters
    stat_students_count = models.CharField(max_length=50, default="2,500+")
    stat_teachers_count = models.CharField(max_length=50, default="120+")
    stat_pass_rate = models.CharField(max_length=50, default="100%")
    stat_awards_count = models.CharField(max_length=50, default="45+")

    # Notification & Alert Banner Switch
    urgent_announcement_enabled = models.BooleanField(default=True)
    urgent_announcement_text = models.CharField(max_length=300, default="Admissions open for Academic Session 2026-2027 from Playgroup to Grade XI (Science & Management).")
    urgent_announcement_link = models.CharField(max_length=255, blank=True, default="/admissions/")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "School Profile & Settings"
        verbose_name_plural = "School Profile & Settings"

    def __str__(self):
        return self.name


class Notice(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General Notice'),
        ('academic', 'Academic & Exams'),
        ('admission', 'Admission Notice'),
        ('event', 'Events & Sports'),
        ('holiday', 'Holidays & Vacations'),
        ('urgent', 'Urgent Announcement'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    summary = models.TextField(blank=True, help_text="Short summary for homepage and cards")
    content = models.TextField(help_text="Detailed content of the notice")
    attachment = models.FileField(upload_to='notices/files/', blank=True, null=True)
    is_pinned = models.BooleanField(default=False, help_text="Pin to top of notices list")
    is_published = models.BooleanField(default=True)
    is_urgent = models.BooleanField(default=False)
    publish_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-publish_date', '-created_at']
        verbose_name = "Notice & Announcement"
        verbose_name_plural = "Notices & Announcements"

    def save(self, *args, **kwargs):
        if not self.publish_date:
            from django.utils import timezone
            self.publish_date = timezone.now().date()
        if not self.slug:
            self.slug = slugify(self.title) + '-' + str(self.publish_date)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{'[PINNED] ' if self.is_pinned else ''}{self.title}"

    def get_absolute_url(self):
        return reverse('notice_detail', kwargs={'slug': self.slug})


class AcademicProgram(models.Model):
    LEVEL_CHOICES = [
        ('primary', 'Primary Level (Playgroup - Grade 5)'),
        ('middle', 'Middle School (Grade 6 - Grade 8)'),
        ('secondary', 'Secondary School (Grade 9 - Grade 10)'),
        ('higher_secondary', 'Higher Secondary (+2 Science, Management, Humanities)'),
    ]

    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    level_code = models.CharField(max_length=50, choices=LEVEL_CHOICES, default='primary')
    tagline = models.CharField(max_length=255, default="Empowering discovery and foundational excellence")
    description = models.TextField()
    curriculum_details = models.TextField(blank=True)
    eligibility = models.TextField(blank=True)
    teaching_methodology = models.TextField(blank=True)
    image = models.ImageField(upload_to='academics/programs/', blank=True, null=True)
    order = models.PositiveIntegerField(default=1)
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AcademicSubject(models.Model):
    program = models.ForeignKey(AcademicProgram, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    credits_or_hours = models.CharField(max_length=50, default="4 Hours/Week")

    def __str__(self):
        return f"{self.name} ({self.program.name})"


class AcademicResource(models.Model):
    RESOURCE_TYPES = [
        ('syllabus', 'Syllabus & Curriculum'),
        ('calendar', 'Academic Calendar'),
        ('routine', 'Exam Routine / Schedule'),
        ('result', 'Result Notice / Sheet'),
        ('worksheet', 'Study Material & Worksheet'),
        ('policy', 'Academic Rules & Handbook'),
    ]

    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES, default='syllabus')
    grade_level = models.CharField(max_length=100, default="All Grades")
    file = models.FileField(upload_to='academics/resources/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"[{self.get_resource_type_display()}] {self.title}"


class TeacherStaff(models.Model):
    STAFF_TYPE_CHOICES = [
        ('management', 'School Leadership & Administration'),
        ('teacher', 'Teaching Faculty'),
        ('counselor', 'Counselor & Student Welfare'),
        ('support', 'Administrative & Support Staff'),
    ]

    name = models.CharField(max_length=150)
    staff_type = models.CharField(max_length=50, choices=STAFF_TYPE_CHOICES, default='teacher')
    designation = models.CharField(max_length=150)
    department = models.CharField(max_length=100, default="General Science & Tech")
    qualification = models.CharField(max_length=200, default="M.Sc. / M.Ed.")
    experience_years = models.PositiveIntegerField(default=5)
    subject_specialization = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='staff/photos/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    order = models.PositiveIntegerField(default=1)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Teacher & Staff Member"
        verbose_name_plural = "Teachers & Staff"

    def __str__(self):
        return f"{self.name} - {self.designation}"


class Facility(models.Model):
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=100, default="Campus Life")
    short_description = models.TextField()
    icon_class = models.CharField(max_length=50, default="fa-solid fa-flask-vial", help_text="FontAwesome icon class")
    image = models.ImageField(upload_to='facilities/', blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'title']
        verbose_name_plural = "Facilities"

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    event_date = models.DateField()
    start_time = models.CharField(max_length=50, default="09:00 AM")
    end_time = models.CharField(max_length=50, default="03:00 PM")
    location = models.CharField(max_length=200, default="School Main Auditorium / Sports Ground")
    short_summary = models.TextField()
    description = models.TextField()
    featured_image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_upcoming = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-event_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + '-' + str(self.event_date)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.event_date})"

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'slug': self.slug})


class GalleryAlbum(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='gallery/covers/', blank=True, null=True)
    event_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class GalleryPhoto(models.Model):
    album = models.ForeignKey(GalleryAlbum, on_delete=models.CASCADE, related_name='photos')
    caption = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='gallery/photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"Photo #{self.id} in {self.album.title}"


class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('academics', 'Academic Insight'),
        ('campus_life', 'Campus Life'),
        ('achievements', 'Student Achievements'),
        ('pedagogy', 'Educational Insights'),
        ('sports', 'Sports & Activities'),
        ('stem', 'Science, Tech & Arts'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='academics')
    author_name = models.CharField(max_length=150, default="Academic Editorial Board")
    author_role = models.CharField(max_length=150, default="Faculty Member")
    featured_image = models.ImageField(upload_to='blog/images/', blank=True, null=True)
    excerpt = models.TextField(help_text="Short teaser for cards and meta descriptions")
    content = models.TextField()
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    published_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date', '-created_at']

    def save(self, *args, **kwargs):
        if not self.published_date:
            from django.utils import timezone
            self.published_date = timezone.now().date()
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})


class AdmissionApplication(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Under Review'),
        ('shortlisted', 'Shortlisted for Interview'),
        ('accepted', 'Accepted / Offered Seat'),
        ('rejected', 'Not Accepted'),
    ]

    # Student Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    applied_grade = models.CharField(max_length=100, help_text="e.g. Grade 1, Grade 8, +2 Science, etc.")
    previous_school = models.CharField(max_length=200, blank=True)
    previous_gpa_or_grade = models.CharField(max_length=50, blank=True)

    # Guardian Info
    guardian_name = models.CharField(max_length=150)
    guardian_relationship = models.CharField(max_length=50, default="Parent")
    guardian_phone = models.CharField(max_length=50)
    guardian_email = models.EmailField()
    guardian_occupation = models.CharField(max_length=150, blank=True)
    residential_address = models.TextField()

    # Document Uploads
    birth_certificate = models.FileField(upload_to='admissions/birth_cert/', blank=True, null=True)
    previous_marksheet = models.FileField(upload_to='admissions/marksheets/', blank=True, null=True)
    student_photo = models.ImageField(upload_to='admissions/photos/', blank=True, null=True)

    # Additional
    statement_or_notes = models.TextField(blank=True, help_text="Any special medical/educational notes")
    application_reference_no = models.CharField(max_length=30, unique=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.application_reference_no:
            import random
            self.application_reference_no = f"HFSS-{random.randint(100000, 999999)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.application_reference_no}] {self.first_name} {self.last_name} ({self.applied_grade})"


class CareerVacancy(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contractual'),
    ]

    title = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, default='full_time')
    open_positions = models.PositiveIntegerField(default=1)
    min_qualification = models.CharField(max_length=200, default="Master's Degree / Bachelor's in relevant discipline")
    experience_required = models.CharField(max_length=100, default="Minimum 2-3 years teaching experience")
    salary_range = models.CharField(max_length=100, default="Competitive & Commensurate with Experience")
    description = models.TextField()
    responsibilities = models.TextField()
    requirements = models.TextField()
    deadline = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Career Vacancies"

    def __str__(self):
        return f"{self.title} ({self.department})"


class JobApplication(models.Model):
    vacancy = models.ForeignKey(CareerVacancy, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    qualification = models.CharField(max_length=200)
    years_of_experience = models.CharField(max_length=50)
    resume = models.FileField(upload_to='careers/resumes/')
    cover_letter = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.vacancy.title}"


class ContactMessage(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name}: {self.subject}"


class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('admissions', 'Admissions & Enrollment'),
        ('academics', 'Academics & Examinations'),
        ('facilities', 'Campus & Transportation'),
        ('general', 'General Queries'),
    ]

    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'question']

    def __str__(self):
        return self.question


class SchoolAchievement(models.Model):
    title = models.CharField(max_length=200)
    year = models.PositiveIntegerField(default=2025)
    category = models.CharField(max_length=100, default="Academic Excellence")
    description = models.TextField()
    image = models.ImageField(upload_to='achievements/', blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['-year', 'order']

    def __str__(self):
        return f"{self.year} - {self.title}"


class Testimonial(models.Model):
    ROLE_CHOICES = [
        ('parent', 'Parent of Student'),
        ('alumni', 'Alumni / Graduate'),
        ('student', 'Current Student'),
    ]

    author_name = models.CharField(max_length=150)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='parent')
    relation_or_batch = models.CharField(max_length=150, default="Parent of Grade 9 Scholar")
    content = models.TextField()
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.PositiveIntegerField(default=5)
    is_featured = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.author_name} ({self.get_role_display()})"
