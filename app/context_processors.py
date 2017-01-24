from django.conf import settings


def add_settings(request):
    return {
        'request': request,
        'settings': settings,
    }
