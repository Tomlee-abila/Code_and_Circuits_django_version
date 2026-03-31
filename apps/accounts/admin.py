from django.contrib import admin
from .models import UserProfile, Certificate, Notification


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'location', 'created_at')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email', 'location')
    raw_id_fields = ('user',)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'issued_at')
    list_filter = ('issued_at',)
    search_fields = ('user__username', 'course__title')
    raw_id_fields = ('user', 'course')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read')
    search_fields = ('user__username', 'title')
