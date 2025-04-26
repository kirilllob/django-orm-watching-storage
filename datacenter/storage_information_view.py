from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime
from django.utils import timezone


def get_duration(visit):
    entered_local_time = timezone.localtime(visit.entered_at)
    date_now = timezone.localtime(timezone.now())
    delta_time = date_now-entered_local_time
    return delta_time


def format_duration(duration):
    total_seconds = duration.total_seconds()
    hours = int(total_seconds//3600)
    minets = int((total_seconds % 3600)//60)
    seconds = int(total_seconds % 60)
    return f"{hours}:{minets}:{seconds}"


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
if __name__ == '__main__':
    main()