from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import PendingNotifications

urlpatterns = [
	url(r'^v1/pending_notifications/$', csrf_exempt(PendingNotifications.as_view()), name="Notification_pending_action"),
]