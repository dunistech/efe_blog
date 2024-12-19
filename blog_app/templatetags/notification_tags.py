# blog_app/templatetags/__init__.py
# Leave this file empty

# blog_app/templatetags/notification_tags.py
from django import template
from blog_app.models import Notification

register = template.Library()

@register.simple_tag
def get_unread_notifications_count(user):
    return Notification.objects.filter(recipient=user, is_read=False).count()