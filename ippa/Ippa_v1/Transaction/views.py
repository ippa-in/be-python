# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render
from django.views.generic import View
from django.db import transaction

from .models import *
from Ippa_v1.responses import *
from Ippa_v1.decorators import decorator_4xx
from .utils import (send_take_action_on_txn_email_to_admin, send_txn_info_email_to_user,
					send_bank_acc_add_mail_to_admin, send_bank_acc_add_mail_to_user,
					bank_acc_action_taken_mail_to_user, txn_action_taken_mail_to_user)
from .constants import *
from .exceptions import BANK_ACC_NOT_EXIST, LESS_POINTS, ACCOUNT_ALREADY_EXISTS
from NotificationEngine.models import NotificationMessage

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
	def get(self, request, *args, **kwargs):

		user = request.user
		params = request.params_dict
		try:
			txn_list = list()
			if user.is_admin:
				txn_status = params.get("status")
				txns = Transaction.objects.select_related('user', 'network').filter(status=txn_status)
			else:
				txns = Transaction.objects.select_related('user', 'network').filter(user=user)
			for txn in txns:
				txn_list.append(txn.serialize())
			self.response["res_str"] = "Transaction details fetch successfully."
			self.response["res_data"] = txn_list
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

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
				#add notification string
				NotificationMessage.objects.add_notification_str(NOTIFICATION_STR_TXN.format(user.name))
				#Send mail to admin to take action.
				send_take_action_on_txn_email_to_admin(ADMIN_TXN_ACTION_MAIL, txn_obj, user)

				#Send email to user for the trasaction creation.
				send_txn_info_email_to_user(USER_TXN_INFO_MAIL, txn_obj, user)

			self.response["res_str"] = "Successfully redeemed points and created transaction."
			self.response["res_data"] = {"txn_id":txn_obj.txn_id}
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

	@decorator_4xx([])
	def put(self, request, *args, **kwargs):

		params = request.params_dict
		user = request.user
		action = params.get("action")
		try:
			if user.is_admin:
				txn_ids = json.loads(params.get("txn_ids"))
				txn_objs = Transaction.objects.filter(pk__in=txn_ids, status=Transaction.PENDING)
				for txn_obj in txn_objs:
					if action == "approved":
						txn_obj.status = Transaction.APPROVED
					elif action == "declined":
						txn_obj.status = Transaction.DECLINED
					txn_obj.save()
					txn_action_taken_mail_to_user(USER_TXN_ACTION_TAKEN_MAIL, 
												action, txn_obj, txn_obj.user)
				self.response["res_str"] = "Action taken successfully."
				return send_200(self.response)
			else:
				raise ACTION_NOT_ALLOWED(STR_ACTION_NOT_ALLOWED)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

class BankView(View):

	def __init__(self):
		self.response = init_response()

	def dispatch(self, *args, **kwargs):

		return super(self.__class__, self).dispatch(*args, **kwargs)

	@decorator_4xx([])
	def get(self, request, *args, **kwargs):

		try:
			banks = Bank.objects.all()
			bank_list = list()
			for bank in banks:
				bank_list.append(bank.serialize())
			self.response["res_str"] = "Bank details fetch successfully."
			self.response["res_data"] = bank_list
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

	@decorator_4xx([])
	def post(self, request, *args, **kwargs):
		"""
		Adding a bank.
		"""
		params = request.POST
		try:
			bank = Bank.objects.create_bank(params)
			self.response["res_str"] = "Bank added successfully."
			self.response["res_data"] = {"bank_id":bank.pk}
			return send_201(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

class BankAccountView(View):

	def __init__(self):
		self.response = init_response()

	def dispatch(self, *args, **kwargs):

		return super(self.__class__, self).dispatch(*args, **kwargs)

	@decorator_4xx([])
	def get(self, request, *args, **kwargs):

		try:
			bank_account = BankAccount.objects.get(user=request.user)
			self.response["res_str"] = "Bank details fetch successfully."
			self.response["res_data"] = bank_account.serialize()
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

	@decorator_4xx([])
	def post(self, request, *args, **kwargs):
		"""
		Adding a bank account.
		"""
		params = request.POST
		user = request.user
		try:
			with transaction.atomic():
				bank_acc = BankAccount.objects.filter(user=request.user)
				if bank_acc:
					raise ACCOUNT_ALREADY_EXISTS(ACCOUNT_EXISTS_STR)
				bank = Bank.objects.get(bank_id=params.get("bank_id"))
				bank_account = BankAccount.objects.create_bank_account(params, bank, user)
				#add notification string
				NotificationMessage.objects.add_notification_str(NOTIFICATION_STR_BANK_ACC.format(user.name))
				#Send mail to admin to approve bank account.
				send_bank_acc_add_mail_to_admin(ADMIN_BANK_ACC_ACTION_MAIL, bank_account, user)

				#Send email to user for the addition of bank account.
				send_bank_acc_add_mail_to_user(USER_BANK_ACC_INFO_MAIL, bank_account, user)
			self.response["res_str"] = "Bank account added successfully."
			self.response["res_data"] = {"bank_account_id":bank_account.pk}
			return send_201(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

	@decorator_4xx([])
	def put(self, request, *args, **kwargs):
		"""
		1. Admin can verify or decline the account.
		2. user can edit bank account details untill it's in pending state.
		"""
		params = request.params_dict
		user = request.user
		try:
			if user.is_admin:
				bank_acc = BankAccount.objects.get(pk=params.get("bank_acc_id"),
													status=BankAccount.PENDING)
				action = params.get("action")
				if action == "approved":
					bank_acc.status = BankAccount.VERIFIED
				elif action == "declined":
					bank_acc.status = BankAccount.DECLINED
				bank_acc_action_taken_mail_to_user(USER_BANK_ACC_ACTION_TAKEN_MAIL, 
													action, bank_acc, user)
			else:
				if params.get("bank_id"):
					bank = Bank.objects.get(bank_id=params.get("bank_id"))
				bank_acc = BankAccount.objects.get(pk=params.get("bank_acc_id"), user=user)
				if not bank_acc.status == BankAccount.PENDING:
					raise BANK_ACC_UPDATION_FAILED(BANK_ACCOUNT_EDIT_FAILED)
				bank_acc.update_bank_acc(params, bank)
			self.response["res_str"] = "Bank account updated successfully."
			self.response["res_data"] = {"bank_account_id":bank_acc.pk}
			return send_201(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)


