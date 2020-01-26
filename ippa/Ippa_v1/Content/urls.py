from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from Content.views import (GetNavigationBar, DashboardImage, UpdateDashboardImage,
							PreviewPoints, ManagePoints)


urlpatterns = [
	url(r'^v1/navigation_bar/$', csrf_exempt(GetNavigationBar.as_view()), name="Content_navigation_bar"),
	url(r'^v1/dashboard_image/$', csrf_exempt(DashboardImage.as_view()), name="Content_dashboard_image"),
	url(r'^v1/update_dashboard_image/$', csrf_exempt(UpdateDashboardImage.as_view()), name="Content_update_dashboard_image"),
	url(r'^v1/preview_points/$', csrf_exempt(PreviewPoints.as_view()), name="Content_preview_points"),
	url(r'^v1/points/$', csrf_exempt(ManagePoints.as_view()), name="Content_points"),
]