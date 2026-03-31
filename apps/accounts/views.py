from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import SignUpForm, LoginForm, ProfileUpdateForm
from .models import Certificate, Notification
from apps.courses.models import Enrollment, Course, LessonProgress
from apps.events.models import EventRegistration


def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Code & Circuits, {user.first_name}!')
            return redirect('accounts:dashboard')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'accounts:dashboard')
            return redirect(next_url)
        messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('core:home')


@login_required
def dashboard(request):
    user = request.user
    enrollments = Enrollment.objects.filter(user=user).select_related('course', 'course__instructor').order_by('-enrolled_at')
    upcoming_registrations = EventRegistration.objects.filter(
        user=user,
        event__date__gte=timezone.now().date()
    ).select_related('event').order_by('event__date')[:5]
    notifications = Notification.objects.filter(user=user, is_read=False)[:5]
    certificates = Certificate.objects.filter(user=user).select_related('course')

    context = {
        'enrollments': enrollments,
        'upcoming_registrations': upcoming_registrations,
        'notifications': notifications,
        'certificates': certificates,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile(request):
    user = request.user
    profile_obj = user.profile

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_obj, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=profile_obj, user=user)

    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def trainer_dashboard(request):
    user = request.user
    if not hasattr(user, 'profile') or not user.profile.is_trainer:
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')

    courses = Course.objects.filter(instructor=user).prefetch_related('enrollments', 'reviews')
    total_students = sum(c.enrollment_count for c in courses)
    context = {
        'courses': courses,
        'total_students': total_students,
    }
    return render(request, 'dashboard/trainer.html', context)


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')

    from django.contrib.auth.models import User as AuthUser
    from apps.events.models import Event

    context = {
        'total_users': AuthUser.objects.count(),
        'total_courses': Course.objects.count(),
        'total_enrollments': Enrollment.objects.count(),
        'total_events': Event.objects.count(),
        'recent_users': AuthUser.objects.order_by('-date_joined')[:10],
        'recent_courses': Course.objects.order_by('-created_at')[:10],
    }
    return render(request, 'dashboard/admin.html', context)


@login_required
def mark_notification_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    if notif.link:
        return redirect(notif.link)
    return redirect('accounts:dashboard')


def verify_certificate(request, pk):
    cert = get_object_or_404(Certificate, pk=pk)
    return render(request, 'accounts/certificate.html', {'cert': cert})
