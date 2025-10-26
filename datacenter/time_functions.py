from django.utils import timezone
from django.utils.timezone import localtime

def format_duration(duration):
    seconds_in_minute = 60
    seconds_in_hour = 3600
    total_seconds = duration.total_seconds()
    hours = int(total_seconds//seconds_in_hour)
    minets = int((total_seconds % seconds_in_hour)//seconds_in_minute)
    seconds = int(total_seconds % seconds_in_minute)
    return f"{hours}:{minets}:{seconds}"

def get_duration(visit):
    entered_local_time = timezone.localtime(visit.entered_at)
    if visit.leaved_at:
        delta_time = localtime(visit.leaved_at) - entered_local_time
    else:
        delta_time = timezone.localtime(timezone.now()) - entered_local_time
    return delta_time


def is_visit_long(deltatime, minutes=60):
    total_seconds = minutes * 60
    long_visit = deltatime.total_seconds() > total_seconds
    return long_visit