from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from Transaction.views import PointsTransactionView, BankView, BankAccountView

urlpatterns = [
	url(r'^v1/redeem_points/$', csrf_exempt(PointsTransactionView.as_view()), name="Transaction_redeempoints"),
	url(r'^v1/bank/$', csrf_exempt(BankView.as_view()), name="Transaction_bank"),
	url(r'^v1/bank_account/$', csrf_exempt(BankAccountView.as_view()), name="Transaction_bankaccount")

]