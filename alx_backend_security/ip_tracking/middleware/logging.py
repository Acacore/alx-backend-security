import logging
import time
from django.http import HttpResponseForbidden
from ip_tracking.models import BlockedIP


logger = logging.getLogger('ip_tracking')
# logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s; %(message)s")
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class LoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
       
       start_time = time.time()

       request_data = {
          'method': request.method,
          'ip_address': request.META.get('REMOTE_ADDR'),
          'path': request.path
       }
       # Log the request details
       logger.info(request_data)

       response = self.get_response(request)
       duration = time.time() - start_time

       restponse_dict = {
           'status_code': response.status_code,
           'duration':duration
       }
       logger.info(restponse_dict)

       return response


class BlockedIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Access denied: Your IP is blocked.")

        response = self.get_response(request)
        return response

