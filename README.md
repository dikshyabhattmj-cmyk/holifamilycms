# Holi Family Secondary School — Web Portal & CMS

A complete, modern, world-class, fully responsive School Management and Content Management Website built using **Python** and **Django**.

Designed with a deep navy blue, royal blue, white, and gold visual identity tailored for an educational institution.

---

## 🌟 Key Features

1. **Homepage & Branding**:
   - Dynamic Hero Banner with urgent announcement notifications.
   - Heritage statistics counter and quick action CTAs.
   - Latest circulars and pinned urgent notices.
   - Principal's desk highlight and core campus pillars.
   - Academic pathways showcase and upcoming school events.
   - Community testimonials and feedback.
   - Global floating contact widget and SEO-optimized footer.

2. **About Section**:
   - Institutional history, vision, mission, and core values.
   - Principal's message and leadership team directory.
   - Campus facilities and educational infrastructure.
   - Milestones and achievements catalog.

3. **Academics & Curricula**:
   - Detailed levels: Primary, Middle School, Secondary (SEE), Higher Secondary (+2 Science & Management).
   - Subject-wise syllabus and credit breakdowns.
   - Download Center for exam routines, syllabi, handbooks, and term result notices.

4. **Admissions Management & Tracker**:
   - Multi-step online admission registration form with file/marksheet uploads.
   - Unique tracking reference code generation (e.g. `HFSS-XXXXXX`).
   - Public application status tracker for parents to track application review states (Under Review, Interview Scheduled, Accepted).

5. **Faculty & Staff Directory**:
   - Role-based sorting (Leadership, Teaching Faculty, Counseling, Support Staff).
   - Real-time department filtering and keyword search.

6. **Notices & Circulars System**:
   - Category filters (Academic, Admission, Events, General, Holidays).
   - Urgent banner switches, pinned notices, and PDF attachments.

7. **Events, Gallery & Blogs**:
   - Upcoming and past event agendas.
   - Photo albums and responsive gallery views.
   - News, academic insights, and social sharing metadata.

8. **Careers & Vacancy Portal**:
   - Active job listings, qualification requirements, deadlines.
   - Online job application form with resume attachment.

9. **Dedicated Admin CMS Portal (`/portal/`)**:
   - Secure login with audit logging and session security.
   - Full CRUD control for Notices, Admissions, Blog Articles, Faculty Profiles, Messages, and Downloads.
   - Global site settings editor for banner text, contact info, and principal message.
   - Native Django Admin interface available at `/admin/`.

---

## 🚀 Local Development Setup

### 1. Requirements
- Python 3.10+ (Tested with Python 3.14)
- Pip & Virtualenv (optional)

### 2. Installation
Clone or navigate to the project directory:
```bash
pip install -r requirements.txt
```

### 3. Database Migration & Seed Sample Content
```bash
python manage.py migrate
python manage.py seed_data
```

### 4. Run Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 🔐 Default Credentials
- **Admin Portal URL**: `http://127.0.0.1:8000/portal/login/`
- **Django Admin URL**: `http://127.0.0.1:8000/admin/`
- **Username**: `admin`
- **Password**: `admin123`

---

## 🛡️ Production Deployment Notes
- Set `DEBUG = False` and define `ALLOWED_HOSTS` in `holifamily_core/settings.py`.
- Configure `DJANGO_SECRET_KEY` in environment variables.
- Connect to PostgreSQL by updating `DATABASES['default']` in `settings.py`.
- Run `python manage.py collectstatic` to generate production assets.
