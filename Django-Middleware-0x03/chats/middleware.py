import logging
from pathlib import Path
from datetime import datetime

class RequestLoggingMiddleware:
    """
    logs each request to a file including timestamp, user and path
    Implements __init__ and __call__
    """

    def __init__(self, get_response):
        #middleware initialization
        self.get_response = get_response

        project_root = Path(__file__).resolve().parent.parent
        self.log_path = project_root / "requests.log"

        #logger
        logging.basicConfig(
            filename=str(self.log_path),
            level=logging.INFO,
            format="%(message)s"
        )
        self.logger = logging.getLogger("request_logger")

    def __call__(self, request):
        user = request.user if hasattr(request, "user") and request.user.is_authenticated else "Anonymous"

        self.logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware restricts access during certain hours
    Denies access (403) if the current time is not between 6PM and 9PM
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #current server time
        current_hour = datetime.now().hour

        #allowed range
        if not (18 <= current_hour < 21):
            return HttpResponseForbidden("Access to this app is restricted at this time")

        return self.get_response(request)