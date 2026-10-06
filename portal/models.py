from django.db import models
from django.contrib.auth.models import User

class AdminAuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} - {self.action} ({self.timestamp:%Y-%m-%d %H:%M})"


class PushSubscription(models.Model):
    """
    Stores browser Push Subscriptions across devices for public visitors and logged-in staff.
    Supports desktop, mobile (Android/iOS PWA), and tablet browsers.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='push_subscriptions')
    endpoint = models.TextField(unique=True, help_text="Push service endpoint URL")
    p256dh = models.CharField(max_length=255, help_text="Client public encryption key")
    auth = models.CharField(max_length=255, help_text="Client authentication secret")
    user_agent = models.TextField(blank=True, default='', help_text="Device / browser info")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Push Subscription"
        verbose_name_plural = "Push Subscriptions"

    def __str__(self):
        owner = self.user.username if self.user else "Public Guest"
        return f"[{owner}] {self.endpoint[:45]}..."


class NotificationLog(models.Model):
    """
    Tracks sent push notifications for auditing, analytics, and duplicate prevention.
    """
    STATUS_CHOICES = [
        ('sent', 'Successfully Delivered'),
        ('failed', 'Failed'),
        ('partial', 'Partially Delivered'),
    ]

    title = models.CharField(max_length=255)
    body = models.TextField()
    url = models.CharField(max_length=500, default='/')
    icon = models.CharField(max_length=500, blank=True, default='/static/icons/icon-192x192.png')
    tag = models.CharField(max_length=100, blank=True, default='hf-announcement')
    event_type = models.CharField(max_length=100, default='general')
    success_count = models.PositiveIntegerField(default=0)
    failure_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notification Log"
        verbose_name_plural = "Notification Logs"

    def __str__(self):
        return f"{self.title} ({self.success_count} delivered) - {self.created_at:%Y-%m-%d %H:%M}"
