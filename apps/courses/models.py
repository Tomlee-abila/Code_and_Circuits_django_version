from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default='circuit-board', help_text='Lucide icon name')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('courses:list') + f'?category={self.slug}'


class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses_taught')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    thumbnail = models.ImageField(upload_to='courses/thumbnails/', blank=True, null=True)
    intro_video_url = models.URLField(blank=True, help_text='YouTube/Vimeo embed URL')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES, default='beginner')
    duration_hours = models.PositiveIntegerField(default=0, help_text='Total hours')
    is_published = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'slug': self.slug})

    @property
    def enrollment_count(self):
        return self.enrollments.count()

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return round(sum(r.rating for r in reviews) / reviews.count(), 1)

    @property
    def lesson_count(self):
        return self.lessons.count()


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True, help_text='YouTube/Vimeo embed URL')
    duration_minutes = models.PositiveIntegerField(default=0)
    is_preview = models.BooleanField(default=False, help_text='Free preview lesson')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.course.title} — Lesson {self.order}: {self.title}'

    def get_embed_url(self):
        url = self.video_url
        if 'youtube.com/watch?v=' in url:
            video_id = url.split('v=')[1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        if 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1]
            return f'https://www.youtube.com/embed/{video_id}'
        return url


class Resource(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='courses/resources/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user.username} → {self.course.title}'

    @property
    def progress_percent(self):
        total = self.course.lessons.count()
        if total == 0:
            return 0
        completed = LessonProgress.objects.filter(
            user=self.user, lesson__course=self.course, completed=True
        ).count()
        return int((completed / total) * 100)


class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f'{self.user.username} — {self.lesson.title}'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} → {self.course.title} ({self.rating}★)'
