from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from school.models import (
    SchoolProfile, Notice, AcademicProgram, AcademicSubject, AcademicResource,
    TeacherStaff, Facility, Event, GalleryAlbum, GalleryPhoto,
    BlogPost, CareerVacancy, FAQ, SchoolAchievement, Testimonial
)

class Command(BaseCommand):
    help = 'Populates the database with rich sample data for Holi Family Secondary School'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating database with sample data...")

        # 1. Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@holifamily.edu.np', 'admin123')
            self.stdout.write("Created superuser 'admin' with password 'admin123'")

        # 2. School Profile
        profile, created = SchoolProfile.objects.get_or_create(
            id=1,
            defaults={
                'name': "Holi Family Secondary School",
                'tagline': "Excellence in Education, Character, & Leadership",
                'short_intro': "Founded with a sacred commitment to holistic student development, Holi Family Secondary School inspires intellectual curiosity, fosters creative innovation, and builds disciplined character in every learner.",
                'established_year': 1995,
                'affiliation': "National Examination Board (NEB) & Ministry of Education, Nepal",
                'address': "Main Academic Avenue, Kathmandu, Nepal",
                'phone_primary': "+977-1-4567890",
                'phone_secondary': "+977-1-4567891",
                'email_primary': "info@holifamily.edu.np",
                'email_admissions': "admissions@holifamily.edu.np",
                'office_hours': "Sunday - Friday: 8:00 AM - 4:30 PM",
                'urgent_announcement_enabled': True,
                'urgent_announcement_text': "Admissions Open for Academic Session 2026-2027: Playgroup to Grade XI (Science & Management). Early entrance scholarship applications now active!",
                'urgent_announcement_link': "/admissions/",
                'principal_name': "Dr. Sarah Jenkins, Ph.D.",
                'principal_designation': "Principal & Academic Director",
                'principal_message': "Welcome to Holi Family Secondary School. For nearly three decades, our institution has stood as a beacon of academic rigor, character formation, and inclusive leadership. We believe every child arrives with unique potential waiting to be ignited. Our dedicated faculty, innovative STEM laboratories, and value-based pedagogy prepare students to excel globally while remaining humble and grounded.",
                'stat_students_count': "2,500+",
                'stat_teachers_count': "120+",
                'stat_pass_rate': "100%",
                'stat_awards_count': "48+",
                'vision': "To nurture disciplined, empathetic, and visionary global citizens who lead with wisdom, moral integrity, and intellectual excellence.",
                'mission': "To provide world-class, learner-centered education combining rigorous academic standards with dynamic co-curricular exploration, cutting-edge technology, and strong ethical values.",
                'core_values': "Integrity, Innovation, Inclusivity, Compassion, Resilience, and Lifelong Intellectual Growth.",
                'history': "Founded in 1995 with just a modest classroom and twenty students, Holi Family Secondary School has grown into one of Nepal's most respected secondary institutions, having educated over 15,000 alumni across medical, engineering, governance, and business sectors.",
            }
        )

        # 3. Notices
        notices_data = [
            {
                'title': "Admissions Open for Academic Session 2026-2027",
                'category': 'admission',
                'summary': "Online applications are now open for Early Childhood Development (ECD) through Grade 11 (Science & Management).",
                'content': "Holi Family Secondary School invites prospective parents and students to apply for the upcoming academic session 2026-2027. Application forms are available online and at the school reception. Entrance assessment tests and parent counseling will take place in rolling cohorts. Merit scholarships are available for deserving candidates.",
                'is_pinned': True,
                'is_urgent': True,
                'publish_date': timezone.now().date(),
            },
            {
                'title': "Annual Science, Robotics & Innovation Exhibition 2026",
                'category': 'event',
                'summary': "Inter-school STEM expo scheduled for next month showcasing robotics, AI models, and green energy prototypes.",
                'content': "Students from Grades 6 through 12 will be displaying innovative projects spanning artificial intelligence, renewable energy solutions, biotechnology, and robotics. Parents, alumni, and educational delegates are warmly invited.",
                'is_pinned': True,
                'is_urgent': False,
                'publish_date': timezone.now().date() - timedelta(days=2),
            },
            {
                'title': "First Term Examination Routine & Syllabus Published",
                'category': 'academic',
                'summary': "Terminal assessment routine for Grades 1 to 10 has been published. Download from the resources portal.",
                'content': "All students, teachers, and parents are notified that the Terminal Examination will commence according to the official timetable. Detailed subject-wise syllabus guidelines and revision worksheets are available for download.",
                'is_pinned': False,
                'is_urgent': False,
                'publish_date': timezone.now().date() - timedelta(days=5),
            },
            {
                'title': "Parent-Teacher Conference (PTC) for Secondary Level",
                'category': 'general',
                'summary': "Interactive dialogue between teachers and parents regarding academic progress and behavioral development.",
                'content': "The quarterly Parent-Teacher Conference provides an opportunity to evaluate holistic student development. Individual meeting slots are designated between 9:00 AM and 2:00 PM.",
                'is_pinned': False,
                'is_urgent': False,
                'publish_date': timezone.now().date() - timedelta(days=8),
            }
        ]
        for nd in notices_data:
            Notice.objects.get_or_create(title=nd['title'], defaults=nd)

        # 4. Academic Programs & Subjects
        programs_data = [
            {
                'name': "Primary & Foundational Wing (Playgroup - Grade 5)",
                'level_code': 'primary',
                'tagline': "Inspiring curiosity, literacy, and joyful foundational learning",
                'description': "Our primary curriculum focuses on experiential learning, language development, basic mathematics, artistic expression, and social-emotional growth in a nurturing environment.",
                'curriculum_details': "Montessori-inspired child-centered methodology combined with national foundational guidelines. Emphasizes phonetic reading, hands-on numeracy, sports, music, and moral science.",
                'order': 1,
                'subjects': ["English Language & Literature", "Mathematics & Logic", "Integrated Science", "Social Studies", "Nepali", "Visual Arts & Music", "Physical Health & Ethics"]
            },
            {
                'name': "Middle School (Grade 6 - Grade 8)",
                'level_code': 'middle',
                'tagline': "Deepening analytical inquiry, scientific understanding, and collaborative problem solving",
                'description': "Students transition into structured disciplines, laboratory investigations, structured computer science coding, and leadership clubs.",
                'curriculum_details': "Rigorous alignment with national curricula enhanced with STEM projects, debate workshops, and environmental science field trips.",
                'order': 2,
                'subjects': ["Advanced Mathematics", "General Science (Physics/Chem/Bio)", "English & Creative Writing", "Computer Science & Python", "Social Studies & Civics", "Nepali Literature", "Moral & Environmental Studies"]
            },
            {
                'name': "Secondary School (Grade 9 - Grade 10 SEE)",
                'level_code': 'secondary',
                'tagline': "Mastery of core disciplines in preparation for the National Secondary Education Examination (SEE)",
                'description': "Comprehensive academic rigor, mock testing regimes, intensive lab practicals, and personalized academic counseling.",
                'curriculum_details': "Complete NEB SEE curriculum, with optional additional math, computer science, and accountancy tracks.",
                'order': 3,
                'subjects': ["Compulsory English", "Compulsory Nepali", "Compulsory Mathematics", "Opt. Mathematics / Accountancy", "Science & Laboratory Practical", "Social Studies", "Computer Applications & Informatics"]
            },
            {
                'name': "Higher Secondary (+2 Science & Management)",
                'level_code': 'higher_secondary',
                'tagline': "Pre-university excellence preparing students for top engineering, medical, and business colleges worldwide",
                'description': "Advanced physics, chemistry, biology, mathematics, computer science, management, and economics taught by distinguished senior professors.",
                'curriculum_details': "NEB +2 affiliated syllabus with integrated medical/engineering entrance coaching and business leadership internships.",
                'order': 4,
                'subjects': ["Physics & Lab", "Chemistry & Lab", "Biology / Computer Science", "Higher Mathematics", "Principles of Accounting", "Business Economics", "English & Nepali"]
            },
        ]

        for p_data in programs_data:
            subjects_list = p_data.pop('subjects')
            prog, _ = AcademicProgram.objects.get_or_create(name=p_data['name'], defaults=p_data)
            for sub_name in subjects_list:
                AcademicSubject.objects.get_or_create(program=prog, name=sub_name)

        # 5. Faculty & Staff
        staff_data = [
            {
                'name': "Dr. Sarah Jenkins, Ph.D.",
                'staff_type': 'management',
                'designation': "Principal & Academic Director",
                'department': "Executive Leadership",
                'qualification': "Ph.D. in Educational Leadership (Edinburgh), M.Ed.",
                'experience_years': 22,
                'subject_specialization': "Educational Strategy, Institutional Ethics",
                'bio': "Dr. Jenkins has guided over two decades of transformative pedagogical leadership across international and national academic councils.",
                'order': 1,
                'is_featured': True
            },
            {
                'name': "Prof. Rajeshwar Sharma",
                'staff_type': 'management',
                'designation': "Vice Principal & Head of Academics",
                'department': "Academic Affairs",
                'qualification': "M.Sc. Mathematics (Gold Medalist), B.Ed.",
                'experience_years': 18,
                'subject_specialization': "Pure Mathematics, Curriculum Design",
                'bio': "Oversees curriculum implementation, teacher development, and standardized examination benchmarking.",
                'order': 2,
                'is_featured': True
            },
            {
                'name': "Dr. Alisha Shrestha",
                'staff_type': 'teacher',
                'designation': "Senior Faculty & Head of Science Department",
                'department': "Natural Sciences & STEM",
                'qualification': "Ph.D. in Applied Chemistry, M.Sc.",
                'experience_years': 12,
                'subject_specialization': "Advanced Organic Chemistry, STEM Projects",
                'bio': "Passionate about green chemistry, laboratory safety, and mentoring students in international science olympiads.",
                'order': 3,
                'is_featured': True
            },
            {
                'name': "Mr. David Miller",
                'staff_type': 'teacher',
                'designation': "Head of Languages & Literature",
                'department': "Humanities & Languages",
                'qualification': "M.A. English Literature (Cambridge), CELTA",
                'experience_years': 10,
                'subject_specialization': "World Literature, Debate & Rhetoric",
                'bio': "Directs the school debating society, annual literary magazine, and creative writing workshops.",
                'order': 4,
                'is_featured': True
            },
            {
                'name': "Ms. Sunita Adhikari",
                'staff_type': 'counselor',
                'designation': "Lead Student Welfare Counselor",
                'department': "Counseling & Career Guidance",
                'qualification': "M.A. Clinical & Child Psychology",
                'experience_years': 8,
                'subject_specialization': "Adolescent Psychology, Career Guidance",
                'bio': "Dedicated to providing confidential psychological guidance, mindfulness workshops, and university admissions coaching.",
                'order': 5,
                'is_featured': False
            },
        ]
        for sd in staff_data:
            TeacherStaff.objects.get_or_create(name=sd['name'], defaults=sd)

        # 6. Campus Facilities
        facilities_data = [
            {'title': "Advanced STEM & Robotics Labs", 'short_description': "State-of-the-art physics, chemistry, biology, and robotics laboratories with modern safety gear and sensors.", 'icon_class': "fa-solid fa-flask-vial", 'order': 1},
            {'title': "Digital Multimedia Library", 'short_description': "Over 25,000 physical titles, digital research repositories, quiet study carrels, and e-learning terminals.", 'icon_class': "fa-solid fa-book-open", 'order': 2},
            {'title': "Multi-Sport Complex & Arena", 'short_description': "Full-sized football pitch, regulation basketball courts, badminton arena, and indoor table tennis halls.", 'icon_class': "fa-solid fa-volleyball", 'order': 3},
            {'title': "Auditorium & Performing Arts Studio", 'short_description': "Acoustically treated 800-seat amphitheater for dramas, musical concerts, seminars, and debates.", 'icon_class': "fa-solid fa-masks-theater", 'order': 4},
            {'title': "Hygienic Cafeteria & Nutrition Bar", 'short_description': "Certified hygienic kitchen offering nutritious, freshly cooked meals and balanced diets for growing students.", 'icon_class': "fa-solid fa-utensils", 'order': 5},
            {'title': "Safe GPS-Tracked Transportation", 'short_description': "Fleet of well-maintained school buses covering major city routes with certified drivers and speed governors.", 'icon_class': "fa-solid fa-bus", 'order': 6},
        ]
        for fd in facilities_data:
            Facility.objects.get_or_create(title=fd['title'], defaults=fd)

        # 7. Events
        events_data = [
            {
                'title': "Annual Sports & Athletics Meet 2026",
                'event_date': timezone.now().date() + timedelta(days=20),
                'start_time': "08:30 AM",
                'end_time': "04:30 PM",
                'location': "School Main Sports Complex",
                'short_summary': "A multi-day athletics extravaganza celebrating track events, relay races, football finals, and house championships.",
                'description': "The Annual Sports Meet brings together four school houses competing in track and field, gymnastics, basketball, and tug-of-war. Medals, trophies, and the prestigious House Rolling Trophy will be presented by chief guests.",
                'is_upcoming': True,
                'is_featured': True
            },
            {
                'title': "Inter-School Model United Nations (HFSS-MUN 2026)",
                'event_date': timezone.now().date() + timedelta(days=45),
                'start_time': "09:00 AM",
                'end_time': "05:00 PM",
                'location': "Main Auditorium & Conference Chambers",
                'short_summary': "Three days of intense diplomatic debate simulating UN General Assembly, Security Council, and Climate summits.",
                'description': "HFSS-MUN gathers over 300 student delegates across Nepal to deliberate on geopolitics, international peace, sustainability, and technological governance.",
                'is_upcoming': True,
                'is_featured': True
            }
        ]
        for ed in events_data:
            Event.objects.get_or_create(title=ed['title'], defaults=ed)

        # 8. Blogs
        blogs_data = [
            {
                'title': "Nurturing 21st Century Skills: Beyond Traditional Rote Learning",
                'category': 'academics',
                'author_name': "Dr. Sarah Jenkins",
                'author_role': "Principal",
                'excerpt': "How experiential education, inquiry-based STEM projects, and critical thinking frameworks shape resilient problem-solvers.",
                'content': "In a rapidly evolving digital world, the value of education lies not merely in what students memorize, but in how effectively they can synthesize information, collaborate across disciplines, and solve complex real-world problems. At Holi Family Secondary School, we integrate design thinking, robotics, and rhetoric into daily classroom experiences.",
                'published_date': timezone.now().date() - timedelta(days=3),
                'is_published': True,
                'is_featured': True,
                'views_count': 142
            },
            {
                'title': "The Role of Sports & Physical Fitness in Cognitive Development",
                'category': 'sports',
                'author_name': "Sports Dept Editorial",
                'author_role': "Physical Education Board",
                'excerpt': "Scientific research highlights how cardiovascular wellness directly amplifies academic focus, memory, and emotional regulation.",
                'content': "Regular physical exercise is scientifically linked to enhanced neuroplasticity, lower stress levels, and improved academic test scores. Our mandatory physical education curriculum ensures every student discovers a sport they love.",
                'published_date': timezone.now().date() - timedelta(days=10),
                'is_published': True,
                'is_featured': False,
                'views_count': 98
            }
        ]
        for bd in blogs_data:
            BlogPost.objects.get_or_create(title=bd['title'], defaults=bd)

        # 9. FAQs
        faqs_data = [
            {'question': "What is the admission procedure for the new academic session?", 'answer': "Parents must submit the online application form with the child's birth certificate and previous academic reports. The admissions committee schedules a friendly aptitude interaction and parent dialogue before confirming the seat.", 'category': 'admissions', 'order': 1},
            {'question': "Does the school provide dedicated transportation services?", 'answer': "Yes, Holi Family operates a comprehensive fleet of modern, GPS-enabled school buses covering all major metropolitan neighborhoods with trained female attendants.", 'category': 'facilities', 'order': 2},
            {'question': "Are scholarships available for meritorious and needy students?", 'answer': "We offer comprehensive merit-based academic scholarships for top scorers in our entrance tests, as well as sports and socioeconomic financial aid grants.", 'category': 'admissions', 'order': 3},
            {'question': "What are the school operating hours?", 'answer': "Administrative offices are open Sunday to Friday from 8:00 AM to 4:30 PM. Regular academic classes operate from 8:45 AM to 3:30 PM.", 'category': 'general', 'order': 4},
        ]
        for fq in faqs_data:
            FAQ.objects.get_or_create(question=fq['question'], defaults=fq)

        # 10. Testimonials
        testimonials_data = [
            {'author_name': "Mr. Bikram Thapa", 'role': 'parent', 'relation_or_batch': "Parent of Grade 10 Scholar", 'content': "Sending our son to Holi Family was the best decision of our lives. The teachers are exceptionally dedicated and nurture both academic discipline and warm human values.", 'rating': 5},
            {'author_name': "Pooja Gurung", 'role': 'alumni', 'relation_or_batch': "Batch of 2021 & Harvard Medical Scholar", 'content': "The foundational science laboratories and mentorship at Holi Family gave me the confidence to compete and excel at the highest international university levels.", 'rating': 5},
            {'author_name': "Dr. Rameshwor Poudel", 'role': 'parent', 'relation_or_batch': "Parent of Grade 5 & Grade 9 Students", 'content': "The balance of sports, robotics, music, and academic rigor is unmatched. The administrative portal makes staying updated seamless.", 'rating': 5},
        ]
        for td in testimonials_data:
            Testimonial.objects.get_or_create(author_name=td['author_name'], defaults=td)

        # 11. Careers Vacancies
        CareerVacancy.objects.get_or_create(
            title="Senior Secondary Physics Lecturer (+2 Level)",
            defaults={
                'department': "Department of Physics & Sciences",
                'job_type': 'full_time',
                'open_positions': 2,
                'min_qualification': "Master's Degree in Physics (M.Sc.) with first division",
                'experience_required': "Minimum 3 years teaching Higher Secondary / +2 curricula",
                'salary_range': "Attractive package with provident fund and medical insurance",
                'description': "We are seeking an inspiring, enthusiastic Physics educator capable of guiding students through conceptual physics, laboratory experiments, and competitive entrance coaching.",
                'responsibilities': "Deliver engaging lectures; supervise practical laboratory experiments; conduct regular assessments; mentor students for olympiads.",
                'requirements': "Master's degree in Physics; excellent English communication skills; demonstrated proficiency in digital classroom smartboards.",
                'deadline': timezone.now().date() + timedelta(days=30),
                'is_active': True,
            }
        )

        # 12. Gallery Album
        album, _ = GalleryAlbum.objects.get_or_create(
            title="Annual Science Fair & Tech Fest",
            defaults={'description': "Exhibition of student robotics models, chemical reactions, and renewable energy inventions.", 'event_date': timezone.now().date() - timedelta(days=15)}
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded rich initial data for Holi Family Secondary School!"))
