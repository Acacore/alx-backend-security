# from .models import Widget
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import SuspiciousIP
from .models import RequestLog  # Assuming you have a model that logs requests with `ip_address` and `path`

SENSITIVE_PATHS = ['/admin', '/login']
REQUEST_THRESHOLD = 100  # requests per hour

@shared_task
def flag_suspicious_ips():
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # Aggregate request counts per IP
    recent_requests = RequestLog.objects.filter(timestamp__gte=one_hour_ago)
    
    ip_request_counts = {}
    for req in recent_requests:
        ip_request_counts[req.ip_address] = ip_request_counts.get(req.ip_address, 0) + 1

        # Flag if accessing sensitive path
        if req.path in SENSITIVE_PATHS:
            SuspiciousIP.objects.get_or_create(
                ip_address=req.ip_address,
                defaults={'reason': f'Accessed sensitive path {req.path}'}
            )

    # Flag IPs exceeding request threshold
    for ip, count in ip_request_counts.items():
        if count > REQUEST_THRESHOLD:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                defaults={'reason': f'Made {count} requests in the last hour'}
            )
