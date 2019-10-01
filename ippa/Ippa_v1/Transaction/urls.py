from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from Transaction.views import PointsTransactionView

urlpatterns = [
	url(r'^v1/redeem_points/$', csrf_exempt(PointsTransactionView.as_view()), name="Transaction_redeempoints"),
]