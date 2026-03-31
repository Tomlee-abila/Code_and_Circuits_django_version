from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    is_online = models.BooleanField(default=False)
    online_link = models.URLField(blank=True)
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='organized_events')
    capacity = models.PositiveIntegerField(default=100)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'slug': self.slug})

    @property
    def registration_count(self):
        return self.registrations.count()

    @property
    def spots_left(self):
        return max(0, self.capacity - self.registration_count)

    @property
    def is_free(self):
        return self.price == 0


class EventRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f'{self.user.username} → {self.event.title}'
