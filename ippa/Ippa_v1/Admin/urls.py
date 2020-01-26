from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import AdminAction

urlpatterns = [
	url(r'^v1/admin_action/$', csrf_exempt(AdminAction.as_view()), name="Admin_action"),
]