from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from Filter.views import FilterView, SearchFieldView

urlpatterns = [
	url(r'^v1/search_fields/$', csrf_exempt(SearchFieldView.as_view()), name="Filter_search_field"),
	url(r'^v1/filter/$', csrf_exempt(FilterView.as_view()), name="Filter_filter"),
]