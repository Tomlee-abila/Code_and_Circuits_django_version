from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Event, EventRegistration


def event_list(request):
    events = Event.objects.filter(is_published=True)

    q = request.GET.get('q', '')
    date_filter = request.GET.get('date', '')
    event_type = request.GET.get('type', '')

    if q:
        events = events.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if date_filter == 'upcoming':
        events = events.filter(date__gte=timezone.now().date())
    elif date_filter == 'past':
        events = events.filter(date__lt=timezone.now().date())
    if event_type == 'online':
        events = events.filter(is_online=True)
    elif event_type == 'physical':
        events = events.filter(is_online=False)

    context = {
        'events': events,
        'q': q,
        'date_filter': date_filter,
        'event_type': event_type,
    }
    return render(request, 'events/list.html', context)


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug, is_published=True)
    is_registered = False
    if request.user.is_authenticated:
        is_registered = EventRegistration.objects.filter(user=request.user, event=event).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        if not is_registered and event.spots_left > 0:
            EventRegistration.objects.create(user=request.user, event=event)
            messages.success(request, f'You have registered for {event.title}!')
            return redirect('events:detail', slug=slug)
        elif is_registered:
            messages.info(request, 'You are already registered for this event.')

    context = {
        'event': event,
        'is_registered': is_registered,
    }
    return render(request, 'events/detail.html', context)
