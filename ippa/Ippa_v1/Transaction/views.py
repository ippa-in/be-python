# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render
from django.views.generic import View
from django.db import transaction

from .models import *
from Ippa_v1.responses import *
from Ippa_v1.decorators import decorator_4xx
from .utils import send_take_action_email_to_admin, send_txn_info_email_to_user
from .constants import *
from .exceptions import BANK_ACC_NOT_EXIST, LESS_POINTS

# Create your views here.
class PointsTransactionView(View):

	"""This view does three actions.
	1. get: Get all transaction if admin. Get user transactions if normal user.
	2. post: this will work as redeem points as user will create a transaction.
	3. put: This will work as admin approve or decline transaction.
	"""

	def __init__(self):
		self.response = init_response()

	def dispatch(self, *args, **kwargs):
		return super(self.__class__, self).dispatch(*args, **kwargs)

	@decorator_4xx([])
	def post(self, request, *args, **kwargs):

		try:
			user = request.user
			bank_acc = BankAccount.objects.filter(user=request.user, 
												status=BankAccount.VERIFIED,
												is_deleted=False)
			if not bank_acc:
				raise BANK_ACC_NOT_EXIST(BANK_ACCOUNT_NOT_EXIST)

			user_points = user.points
			redeemable_points = user_points.get("redeemable_points")
			if not redeemable_points:
				raise LESS_POINTS(REDEEMABLE_POINTS_IS_ZERO)
			with transaction.atomic():
				user_points["redeemed_points"] += redeemable_points
				user_points["redeemable_points"] = 0
				user.points = user_points
				user.save()

				#Add transaction
				txn_obj = Transaction.objects.create_txn(txn_type=Transaction.WITHDRAW,
														amount=redeemable_points,
														user=user)
				#Send mail to admin to take action.
				send_take_action_email_to_admin(ADMIN_TXN_ACTION_MAIL, txn_obj, user)

				#Send email to user for the trasaction creation.
				send_txn_info_email_to_user(USER_TXN_INFO_MAIL, txn_obj, user)

			self.response["res_str"] = "Successfully redeemed points and created transaction."
			self.response["res_data"] = {"txn_id":txn_obj.txn_id}
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)