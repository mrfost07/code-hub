from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone


class NotificationManager(models.Manager):
    def for_user(self, user):
        return self.filter(receipient=user)
    
    def unread(self, user):
        return self.for_user(user).filter(read=False)
    
    def read(self, user):
        return self.for_user(user).filter(read=True)


class Notification(models.Model):  # Fixed typo in class name
    receipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="actions")
    verb = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)  # Set automatically
    read = models.BooleanField(default=False)

    objects = NotificationManager()

    def __str__(self):
        return f'{self.actor} {self.verb} {self.content_object}'
    
    class Meta:
        ordering = ['-created_at']

    @property
    def notification_time_formatted(self):
        """Return a human-readable time format"""
        now = timezone.now()
        diff = now - self.created_at
        
        if diff.days == 0:
            if diff.seconds < 60:
                return "just now"
            elif diff.seconds < 3600:
                minutes = diff.seconds // 60
                return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
            else:
                hours = diff.seconds // 3600
                return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.days == 1:
            return "yesterday"
        elif diff.days < 7:
            return f"{diff.days} days ago"
        else:
            return self.created_at.strftime('%b %d, %Y')

