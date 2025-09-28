from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datacenter.time_functions import get_duration, format_duration, is_visit_long


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


