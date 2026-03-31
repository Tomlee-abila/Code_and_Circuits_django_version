from django.shortcuts import render
from apps.courses.models import Course, Category
from apps.events.models import Event


def home(request):
    featured_courses = Course.objects.filter(is_published=True).select_related(
        'instructor', 'category'
    ).order_by('-created_at')[:6]

    upcoming_events = Event.objects.filter(
        is_published=True
    ).order_by('date')[:4]

    categories = Category.objects.all()[:6]

    stats = {
        'students': '10,000+',
        'courses': '150+',
        'instructors': '50+',
        'countries': '30+',
    }

    testimonials = [
        {
            'name': 'Amara Nwosu',
            'role': 'IoT Engineer',
            'text': 'Code & Circuits transformed my career. The Arduino and IoT courses gave me hands-on skills I use every single day.',
            'avatar': None,
        },
        {
            'name': 'James Okafor',
            'role': 'AI Developer',
            'text': 'The AI curriculum here is genuinely world-class. Structured, practical, and taught by real practitioners.',
            'avatar': None,
        },
        {
            'name': 'Fatima Al-Rashid',
            'role': 'Software Engineer',
            'text': 'The community aspect is what sets Code & Circuits apart. You are never learning alone.',
            'avatar': None,
        },
    ]

    context = {
        'featured_courses': featured_courses,
        'upcoming_events': upcoming_events,
        'categories': categories,
        'stats': stats,
        'testimonials': testimonials,
    }
    return render(request, 'core/home.html', context)


def about(request):
    team = [
        {'name': 'Dr. Kemi Adeyemi', 'role': 'Founder & CEO', 'bio': 'PhD in Computer Engineering, 15 years in STEM education.', 'avatar': None},
        {'name': 'Chukwuemeka Eze', 'role': 'Lead Instructor — IoT', 'bio': 'Hardware engineer with 10 years building embedded systems for industrial applications.', 'avatar': None},
        {'name': 'Blessing Okonkwo', 'role': 'AI & ML Lead', 'bio': 'Former ML engineer at a top tech company, passionate about democratizing AI education.', 'avatar': None},
        {'name': 'Taiwo Adeniyi', 'role': 'Head of Community', 'bio': 'Community builder with a background in developer relations and open-source projects.', 'avatar': None},
    ]
    return render(request, 'core/about.html', {'team': team})
