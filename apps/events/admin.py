from django.contrib import admin
from .models import Event, EventRegistration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location', 'is_online', 'is_published', 'registration_count')
    list_filter = ('is_online', 'is_published', 'date')
    search_fields = ('title', 'location', 'description')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('organizer',)

    def registration_count(self, obj):
        return obj.registrations.count()
    registration_count.short_description = 'Registered'


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'registered_at')
    search_fields = ('user__username', 'event__title')
    raw_id_fields = ('user', 'event')
