from django.utils import timezone
from .models import *


class VisitorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request
        response = self.get_response(request)

        # If the request is not from a bot, track the visitor
        if not request.user_agent.is_bot:
            ip_address = request.META.get("REMOTE_ADDR")
            timestamp = timezone.now()
            Visitor.objects.create(ip_address=ip_address, timestamp=timestamp)

        return response
