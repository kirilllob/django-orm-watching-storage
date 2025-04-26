from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404


def get_duration(visit):
    entered_local_time = timezone.localtime(visit.entered_at)
    if visit.leaved_at:
        delta_time = localtime(visit.leaved_at) - entered_local_time
    else:
        delta_time = timezone.localtime(timezone.utc)
    return delta_time


def is_visit_long(deltatime, minutes=60):
    total_seconds = minutes * 60
    long_visit = deltatime.total_seconds() > total_seconds
    return long_visit


def format_duration(duration):
    total_seconds = duration.total_seconds()
    hours = int(total_seconds//3600)
    minets = int((total_seconds % 3600)//60)
    seconds = int(total_seconds % 60)
    return f"{hours}:{minets}:{seconds}"


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    active_visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []
    for visit in active_visits:
        entered_local_time = timezone.localtime(visit.entered_at)
        duration = get_duration(visit)
        time_inside = format_duration(duration)
        is_strange = is_visit_long(duration)
        this_passcard_visits.append(
            {
                'entered_at': entered_local_time,
                'duration': time_inside,
                'is_strange': is_strange
            },
        )
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)


