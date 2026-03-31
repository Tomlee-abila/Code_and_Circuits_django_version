from django.contrib import admin
from .models import Category, Course, Lesson, Resource, Enrollment, LessonProgress, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('order', 'title', 'video_url', 'duration_minutes', 'is_preview')


class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'level', 'price', 'is_published', 'enrollment_count', 'created_at')
    list_filter = ('is_published', 'level', 'category', 'is_free')
    search_fields = ('title', 'instructor__username', 'description')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('instructor',)
    inlines = [LessonInline]

    def enrollment_count(self, obj):
        return obj.enrollments.count()
    enrollment_count.short_description = 'Enrolled'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'duration_minutes', 'is_preview')
    list_filter = ('is_preview', 'course')
    search_fields = ('title', 'course__title')
    inlines = [ResourceInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at', 'completed')
    list_filter = ('completed', 'enrolled_at')
    search_fields = ('user__username', 'course__title')
    raw_id_fields = ('user', 'course')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('user__username', 'course__title')
