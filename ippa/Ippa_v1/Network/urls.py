from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from Network.views import ManageNetwork, NetworkTagging, NetworkNames

urlpatterns = [
	url(r'^v1/network/$', csrf_exempt(ManageNetwork.as_view()), name="Network_network"),
	url(r'^v1/tagging/$', csrf_exempt(NetworkTagging.as_view()), name="Network_tagging"),
	url(r'^v1/network_names/$', csrf_exempt(NetworkNames.as_view()), name="Network_network_names"),

]