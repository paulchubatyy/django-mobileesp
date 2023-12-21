from django.conf import settings
from django.utils.functional import SimpleLazyObject

DETECT_USER_AGENTS = getattr(settings, 'DETECT_USER_AGENTS', {})

def lazy_detection(request, key):
    detector = DETECT_USER_AGENTS[key]
    return SimpleLazyObject( lambda: detector(request) )


class UserAgentDetectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    """
    Middleware to detect request's user agent
    """
    def __call__(self, request):
        for each in DETECT_USER_AGENTS:
            setattr( request, each, lazy_detection(request, each) )
        return self.get_response(request)

