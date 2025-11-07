from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(AbstractUser):
    pass

    def __str__(self):
        return f"Profile for {self.user.username}"


# --- RequestLog MODEL ---
class RequestLog(models.Model):
    """
    Model to log details of incoming requests, linked to the User model.
    """
    # RequestLog still links directly to the core User model
    user = models.ForeignKey(Profile,  on_delete=models.CASCADE)
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Request Timestamp",
        help_text="The date and time when the request was made."
    )
    ip_address = models.GenericIPAddressField(verbose_name="IP Address", help_text="The IP address from which the request originated.")
    path = models.CharField(max_length=255, verbose_name="Request Path", help_text="The path of the request (e.g., /home/).")


    class Meta:
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"
        ordering = ['-timestamp']


    def __str__(self):
        user_info = self.user.username if self.user else "Anonymous"
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] User: {user_info}, IP: {self.ip_address}, Path: {self.path}"

    # # --- Signals for automatic Profile creation ---
    # @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)

    # @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    # def save_user_profile(sender, instance, **kwargs):
    #     # This ensures the profile is saved/updated whenever the user is saved/updated
    #     if hasattr(instance, 'profile'):
    #         instance.profile.save()


    # ip_tracking/models.py


class DeviceLocation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # store IMEI hashed if you must keep identifier
    imei_hash = models.CharField(max_length=64, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(default=timezone.now)
    source = models.CharField(max_length=20, default='gps')  # 'gps' or 'ip' etc.

    def __str__(self):
        return f"{self.user} @ {self.latitude},{self.longitude} ({self.timestamp})"



class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return self.ip_address
