from django.http import JsonResponse


def health_check(request):
    """Simplest healthcheck ever"""
    return JsonResponse({"status": "ok"})
