from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from Network.views import ManageNetwork, NetworkTagging

urlpatterns = [
	url(r'^v1/network/$', csrf_exempt(ManageNetwork.as_view()), name="Network_network"),
	url(r'^v1/tagging/$', csrf_exempt(NetworkTagging.as_view()), name="Network_tagging"),
]