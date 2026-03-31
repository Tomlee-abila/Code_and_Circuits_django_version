from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Course, Category, Lesson, Enrollment, LessonProgress, Review, Resource
from .forms import CourseForm, LessonForm, ReviewForm


def course_list(request):
    courses = Course.objects.filter(is_published=True).select_related('instructor', 'category')

    q = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    level = request.GET.get('level', '')
    price_filter = request.GET.get('price', '')

    if q:
        courses = courses.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if category_slug:
        courses = courses.filter(category__slug=category_slug)
    if level:
        courses = courses.filter(level=level)
    if price_filter == 'free':
        courses = courses.filter(is_free=True)
    elif price_filter == 'paid':
        courses = courses.filter(is_free=False)

    paginator = Paginator(courses, 9)
    page = request.GET.get('page', 1)
    courses_page = paginator.get_page(page)

    categories = Category.objects.all()

    context = {
        'courses': courses_page,
        'categories': categories,
        'q': q,
        'selected_category': category_slug,
        'selected_level': level,
        'selected_price': price_filter,
        'total_count': paginator.count,
    }
    return render(request, 'courses/list.html', context)


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    lessons = course.lessons.all()
    reviews = course.reviews.select_related('user').all()

    is_enrolled = False
    enrollment = None
    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        is_enrolled = enrollment is not None

    review_form = None
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        if not user_review:
            review_form = ReviewForm()

    if request.method == 'POST' and request.user.is_authenticated:
        if 'enroll' in request.POST:
            if not is_enrolled:
                Enrollment.objects.create(user=request.user, course=course)
                messages.success(request, f'You are now enrolled in {course.title}!')
                return redirect('courses:inner_dashboard', slug=slug)
        elif 'review' in request.POST and not user_review:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                r = review_form.save(commit=False)
                r.user = request.user
                r.course = course
                r.save()
                messages.success(request, 'Review submitted!')
                return redirect('courses:detail', slug=slug)

    context = {
        'course': course,
        'lessons': lessons,
        'reviews': reviews,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
        'review_form': review_form,
        'user_review': user_review,
        'related_courses': Course.objects.filter(
            category=course.category, is_published=True
        ).exclude(pk=course.pk)[:3],
    }
    return render(request, 'courses/detail.html', context)


@login_required
def course_inner_dashboard(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)

    lessons = course.lessons.prefetch_related('resources', 'quiz').all()
    completed_lesson_ids = set(
        LessonProgress.objects.filter(
            user=request.user, lesson__course=course, completed=True
        ).values_list('lesson_id', flat=True)
    )

    lesson_id = request.GET.get('lesson')
    current_lesson = None
    if lesson_id:
        current_lesson = get_object_or_404(Lesson, pk=lesson_id, course=course)
    elif lessons:
        current_lesson = lessons.first()

    if request.method == 'POST' and 'mark_complete' in request.POST:
        lesson_to_mark = get_object_or_404(Lesson, pk=request.POST['mark_complete'], course=course)
        progress, created = LessonProgress.objects.get_or_create(
            user=request.user, lesson=lesson_to_mark
        )
        if not progress.completed:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save()
        return redirect(f'{request.path}?lesson={lesson_to_mark.pk}')

    context = {
        'course': course,
        'enrollment': enrollment,
        'lessons': lessons,
        'current_lesson': current_lesson,
        'completed_lesson_ids': completed_lesson_ids,
        'progress': enrollment.progress_percent,
    }
    return render(request, 'courses/inner_dashboard.html', context)


@login_required
def create_course(request):
    if not hasattr(request.user, 'profile') or not request.user.profile.is_trainer:
        messages.error(request, 'Only trainers can create courses.')
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, 'Course created!')
            return redirect('courses:edit_course', slug=course.slug)
    else:
        form = CourseForm()

    return render(request, 'courses/create.html', {'form': form})


@login_required
def edit_course(request, slug):
    course = get_object_or_404(Course, slug=slug, instructor=request.user)
    lessons = course.lessons.all()

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated!')
            return redirect('courses:edit_course', slug=course.slug)
    else:
        form = CourseForm(instance=course)

    lesson_form = LessonForm()
    context = {
        'form': form,
        'course': course,
        'lessons': lessons,
        'lesson_form': lesson_form,
    }
    return render(request, 'courses/edit.html', context)


@login_required
def add_lesson(request, slug):
    course = get_object_or_404(Course, slug=slug, instructor=request.user)
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request, 'Lesson added!')
    return redirect('courses:edit_course', slug=slug)
