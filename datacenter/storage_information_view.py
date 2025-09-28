from datacenter.time_functions import format_duration, get_duration
from datacenter.models import Visit
from django.shortcuts import render
from django.utils import timezone


def storage_information_view(request):
    active_visits = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []
    for visit in active_visits:
        entered_local_time = timezone.localtime(visit.entered_at)
        duration = get_duration(visit)
        time_inside = format_duration(duration)
        person = visit.passcard
        non_closed_visits.append(
            {
                'who_entered': person,
                'entered_at':  entered_local_time,
                'duration': time_inside,
            }
        )
    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
