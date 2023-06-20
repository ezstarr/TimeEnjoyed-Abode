from django.utils import timezone as tz


def now_and_today(request):
    now = tz.now()
    return {
     'now': now,
     'today': tz.localtime(now).date(),
    }
