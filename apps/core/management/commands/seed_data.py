"""
Management command to seed the database with demo data.
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.courses.models import Category, Course, Lesson
from apps.events.models import Event
from apps.accounts.models import UserProfile
import datetime


class Command(BaseCommand):
    help = 'Seeds the database with demo data for Code & Circuits'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('Seeding Code & Circuits database...'))

        # Categories
        categories_data = [
            {'name': 'IoT & Arduino', 'slug': 'iot', 'icon': 'cpu', 'description': 'Internet of Things and embedded systems'},
            {'name': 'AI & Machine Learning', 'slug': 'ai', 'icon': 'brain', 'description': 'Artificial intelligence and ML algorithms'},
            {'name': 'Programming', 'slug': 'programming', 'icon': 'code-2', 'description': 'Software development and coding'},
            {'name': 'Electronics', 'slug': 'electronics', 'icon': 'zap', 'description': 'Circuit design and electronics'},
            {'name': 'Robotics', 'slug': 'robotics', 'icon': 'bot', 'description': 'Robot design and programming'},
            {'name': 'Networking', 'slug': 'networking', 'icon': 'network', 'description': 'Computer networks and protocols'},
        ]
        categories = {}
        for cat_data in categories_data:
            cat, _ = Category.objects.get_or_create(slug=cat_data['slug'], defaults=cat_data)
            categories[cat_data['slug']] = cat
        self.stdout.write(self.style.SUCCESS(f'  Created {len(categories)} categories'))

        # Create superuser/admin
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@codecircuits.io',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            admin.profile.role = 'admin'
            admin.profile.bio = 'Platform administrator'
            admin.profile.save()

        # Create trainer
        trainer, created = User.objects.get_or_create(
            username='trainer_kemi',
            defaults={
                'email': 'kemi@codecircuits.io',
                'first_name': 'Kemi',
                'last_name': 'Adeyemi',
            }
        )
        if created:
            trainer.set_password('trainer123')
            trainer.save()
            trainer.profile.role = 'trainer'
            trainer.profile.bio = 'PhD in Computer Engineering, 15 years in STEM education.'
            trainer.profile.location = 'Lagos, Nigeria'
            trainer.profile.save()

        # Create second trainer
        trainer2, created = User.objects.get_or_create(
            username='trainer_eze',
            defaults={
                'email': 'eze@codecircuits.io',
                'first_name': 'Chukwuemeka',
                'last_name': 'Eze',
            }
        )
        if created:
            trainer2.set_password('trainer123')
            trainer2.save()
            trainer2.profile.role = 'trainer'
            trainer2.profile.bio = 'Hardware engineer with 10 years building embedded systems.'
            trainer2.profile.save()

        # Demo student
        student, created = User.objects.get_or_create(
            username='student_demo',
            defaults={
                'email': 'student@codecircuits.io',
                'first_name': 'Demo',
                'last_name': 'Student',
            }
        )
        if created:
            student.set_password('student123')
            student.save()

        self.stdout.write(self.style.SUCCESS('  Created demo users'))

        # Courses
        courses_data = [
            {
                'title': 'Arduino Fundamentals: Build Your First IoT Device',
                'short_description': 'Learn Arduino from scratch — sensors, actuators, and wireless communication.',
                'description': 'A complete beginner\'s guide to Arduino programming and circuit design. Build 10 real projects.',
                'instructor': trainer2,
                'category': categories['iot'],
                'price': 0,
                'level': 'beginner',
                'duration_hours': 12,
                'is_published': True,
                'is_free': True,
            },
            {
                'title': 'IoT with ESP32: Connect Everything to the Cloud',
                'short_description': 'Master the ESP32 microcontroller and connect your projects to AWS, Firebase, and MQTT.',
                'description': 'Deep dive into ESP32 development — WiFi, Bluetooth, sensors, and cloud connectivity.',
                'instructor': trainer2,
                'category': categories['iot'],
                'price': 49.99,
                'level': 'intermediate',
                'duration_hours': 20,
                'is_published': True,
                'is_free': False,
            },
            {
                'title': 'Machine Learning for Engineers',
                'short_description': 'Practical ML for people who build things — scikit-learn, TensorFlow, and deployment.',
                'description': 'Skip the math overload. Learn ML through engineering projects you can actually ship.',
                'instructor': trainer,
                'category': categories['ai'],
                'price': 79.99,
                'level': 'intermediate',
                'duration_hours': 25,
                'is_published': True,
                'is_free': False,
            },
            {
                'title': 'Python for Hardware Engineers',
                'short_description': 'Control hardware with Python — Raspberry Pi, serial ports, and automation scripts.',
                'description': 'The essential Python toolkit for engineers who want to automate and control the physical world.',
                'instructor': trainer,
                'category': categories['programming'],
                'price': 39.99,
                'level': 'beginner',
                'duration_hours': 15,
                'is_published': True,
                'is_free': False,
            },
            {
                'title': 'PCB Design with KiCad',
                'short_description': 'Design professional printed circuit boards from schematic to production-ready Gerbers.',
                'description': 'A hands-on PCB design course using the free, open-source KiCad EDA suite.',
                'instructor': trainer2,
                'category': categories['electronics'],
                'price': 59.99,
                'level': 'intermediate',
                'duration_hours': 18,
                'is_published': True,
                'is_free': False,
            },
            {
                'title': 'Introduction to Robotics with ROS',
                'short_description': 'Build and program robots using the Robot Operating System (ROS2).',
                'description': 'Get started with ROS2 — simulation, real robots, and autonomous navigation.',
                'instructor': trainer,
                'category': categories['robotics'],
                'price': 89.99,
                'level': 'advanced',
                'duration_hours': 30,
                'is_published': True,
                'is_free': False,
            },
        ]

        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults=course_data
            )
            if created:
                # Add sample lessons
                lessons = [
                    {'order': 1, 'title': 'Course Introduction & Setup', 'duration_minutes': 8, 'is_preview': True},
                    {'order': 2, 'title': 'Module 1: Foundations', 'duration_minutes': 25},
                    {'order': 3, 'title': 'Module 2: Core Concepts', 'duration_minutes': 32},
                    {'order': 4, 'title': 'Module 3: First Project', 'duration_minutes': 45},
                    {'order': 5, 'title': 'Module 4: Going Deeper', 'duration_minutes': 38},
                    {'order': 6, 'title': 'Final Project & Next Steps', 'duration_minutes': 20},
                ]
                for lesson_data in lessons:
                    Lesson.objects.create(course=course, **lesson_data)

        self.stdout.write(self.style.SUCCESS(f'  Created {len(courses_data)} courses with lessons'))

        # Events
        today = datetime.date.today()
        events_data = [
            {
                'title': 'IoT Hackathon: Smart City Solutions',
                'slug': 'iot-hackathon-smart-city',
                'description': 'A 24-hour hackathon where teams build IoT solutions for urban challenges.',
                'short_description': '24-hour hackathon — build IoT solutions for smart city challenges.',
                'date': today + datetime.timedelta(days=14),
                'time': datetime.time(9, 0),
                'location': 'Lagos Tech Hub, Victoria Island',
                'is_online': False,
                'organizer': trainer2,
                'capacity': 80,
                'price': 0,
                'is_published': True,
            },
            {
                'title': 'Live Workshop: Building Your First Neural Network',
                'slug': 'live-workshop-neural-network',
                'description': 'Join Kemi Adeyemi for a live, interactive session building a neural network from scratch in Python.',
                'short_description': 'Live session: Build a neural network from scratch with expert guidance.',
                'date': today + datetime.timedelta(days=7),
                'time': datetime.time(18, 0),
                'location': 'Online — Zoom',
                'is_online': True,
                'online_link': 'https://zoom.us/j/example',
                'organizer': trainer,
                'capacity': 200,
                'price': 0,
                'is_published': True,
            },
            {
                'title': 'Arduino Masterclass: Advanced Sensor Fusion',
                'slug': 'arduino-masterclass-sensor-fusion',
                'description': 'An advanced workshop on combining multiple sensors for precise measurement and control.',
                'short_description': 'Advanced Arduino: combine multiple sensors for precise control.',
                'date': today + datetime.timedelta(days=21),
                'time': datetime.time(14, 0),
                'location': 'Online — Google Meet',
                'is_online': True,
                'organizer': trainer2,
                'capacity': 100,
                'price': 15.00,
                'is_published': True,
            },
        ]

        for event_data in events_data:
            Event.objects.get_or_create(slug=event_data['slug'], defaults=event_data)

        self.stdout.write(self.style.SUCCESS(f'  Created {len(events_data)} events'))

        self.stdout.write(self.style.SUCCESS('\n✓ Seed complete!'))
        self.stdout.write('')
        self.stdout.write('  Demo accounts:')
        self.stdout.write('  ─────────────────────────────────────')
        self.stdout.write('  Admin:   admin / admin123')
        self.stdout.write('  Trainer: trainer_kemi / trainer123')
        self.stdout.write('  Student: student_demo / student123')
        self.stdout.write('')
