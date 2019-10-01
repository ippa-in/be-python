from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from AccessControl.views import SignUp, LogIn, UploadAchivements

urlpatterns = [
	url(r'^v1/createuser/$', csrf_exempt(SignUp.as_view()), name="AccessControl_createuser"),
	url(r'^v1/login/$', csrf_exempt(LogIn.as_view()), name="AccessControl_login"),
	url(r'^v1/upload_achievements/$', csrf_exempt(UploadAchivements.as_view()), name="AccessControl_achievement")

]