# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from Ippa_v1.utils import generate_unique_id
from AccessControl.models import IppaUser
from Network.models import Network

# Create your models here.
class BaseModel(models.Model):

	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	is_deleted = models.BooleanField(default=False)

	class Meta:
		abstract = True

class BankManager(models.Manager):

	def create_bank(self, data):

		bank_dict = {
			"bank_id":generate_unique_id("BANK"),
			"name": data.get("name")
		}
		bank_obj = self.create(**bank_dict)
		return bank_obj

class Bank(BaseModel):

	bank_id = models.CharField(max_length=255)
	name = models.CharField(max_length=255, null=True, blank=True)

	objects = BankManager()

	def __unicode__(self):
		return self.bank_id + " " + self.name

	def serialize(self):

		bank_details = dict()
		bank_details["bank_id"] = self.bank_id
		bank_details["name"] = self.name
		return bank_details

class BankAccountManager(models.Manager):
	
	def create_bank_account(self, params, bank, user):

		bank_acc_details = {
			"ifsc":params.get("ifsc"),
			"acc_name":params.get("acc_name"),
			"acc_number":params.get("acc_num"),
			"bank":bank,
			"user":user
		}
		bank_acc = self.create(**bank_acc_details)
		return bank_acc

class BankAccount(BaseModel):

	PENDING = "Pending"
	VERIFIED = "Verified"
	DECLINED = "Declined"


	status_choices = ((PENDING, "Pending"),
						(VERIFIED, "Verified"),
						(DECLINED, "Declined")
					)
	ifsc = models.CharField(max_length=11, null=True, blank=True)
	acc_name = models.CharField(max_length=255, null=True, blank=True)
	acc_number = models.CharField(max_length=255, db_index=True)
	user = models.ForeignKey(IppaUser, related_name="user_bank_account")
	bank = models.ForeignKey(Bank, null=True, blank=True, related_name="bank_account")
	status = models.CharField(max_length=255, default=PENDING, choices=status_choices)

	objects = BankAccountManager()

	def __unicode__(self):
		return self.acc_number + " " + self.acc_name

	def serialize(self):

		bank_acc_dict = {
			"acc_id":self.pk,
			"acc_name":self.acc_name,
			"acc_number":self.acc_number,
			"bank":self.bank.serialize(),
			"ifsc_code":self.ifsc,
			"status":self.status
		}
		return bank_acc_dict

	def update_bank_acc(self, params, bank=None):

		if params.get("acc_name"):
			self.acc_name = params.get("acc_name")
		elif params.get("acc_number"):
			self.acc_number = params.get("acc_number")
		if bank:
			self.bank = bank
		if params.get("ifsc_code"):
			self.ifsc_code = params.get("ifsc_code")
		self.save()

class TransactionManager(models.Manager):

	def create_txn(self, txn_date=None, txn_type=None, status=None, 
					amount=None, description=None, network=None, user=None):
	
		txn_id = generate_unique_id("TXN")
		txn_details = {
			"txn_id":txn_id,
			"amount":amount,
			"user":user
		}
		if txn_type:
			txn_details["txn_type"] = txn_type
		if status:
			txn_details["status"] = status
		if description:
			txn_details["description"] = description
		if network:
			txn_details["network"] = network
		if txn_date:
			txn_details["txn_date"] = txn_date
		else:
			txn_details["txn_date"] = datetime.now()
		txn_obj = self.create(**txn_details)
		return txn_obj

	def bulk_serializer(self, queryset):

		txn_data = []
		for obj in queryset:
			txn_data.append(obj.serialize())
		return txn_data

class Transaction(BaseModel):

	PENDING = "Pending"
	APPROVED = "Approved"
	DECLINED = "Declined"
	FAILED = "Failed"
	status_choices = ((PENDING, "Pending"),
					(APPROVED, "Approved"),
					(DECLINED, "Declined"),
					(FAILED, "Failed"))

	WITHDRAW = "Withdraw"
	DEPOSIT = "Deposit"
	txn_type_choices = ((WITHDRAW, "Withdraw"),
						(DEPOSIT, "Deposit"))

	txn_id = models.CharField(max_length=255, primary_key=True)
	txn_date = models.DateTimeField(null=True, blank=True)
	txn_type = models.CharField(max_length=255, default=DEPOSIT, choices=txn_type_choices)
	status = models.CharField(max_length=255, default=PENDING, choices=status_choices)
	amount = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
	description = models.TextField(default='', null=True, blank=True)
	user = models.ForeignKey(IppaUser, null=True, blank=True, related_name="user_txn")
	network = models.ForeignKey(Network, null=True, blank=True, related_name="network_txn")

	objects = TransactionManager()

	def __unicode__(self):
		return self.txn_id

	def serialize(self):

		txn_data = dict()
		txn_data["txn_id"] = self.txn_id
		txn_data["txn_date"] = self.txn_date
		txn_data["txn_type"] = self.txn_type
		txn_data["status"] = self.status
		txn_data["amount"] = self.amount
		txn_data["description"] = self.description
		txn_data["user"] = {"player_id":self.user.player_id, "user_name":self.user.name} if self.user else {}
		txn_data["network"] = {"network_id":self.network.network_id, "name":self.network.name} if self.network else {}
		return txn_data




