# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from AccessControl.models import IppaUser
from Network.models import Network

# Create your models here.
class BaseModel(models.Model):

	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	is_deleted = models.BooleanField(default=False)

	class Meta:
		abstract = True

class BankAccountManager(models.Manager):
	pass

class BankAccount(BaseModel):

	PENDING = "Pending"
	VERIFIED = "Verified"
	DECLINED = "Declined"


	status_choices = ((PENDING, "Pending"),
						(VERIFIED, "Verified"),
						(DECLINED, "Declined")
					)
	name = models.CharField(max_length=255)
	ifsc = models.CharField(max_length=11, null=True, blank=True)
	acc_name = models.CharField(max_length=255, null=True, blank=True)
	acc_number = models.CharField(max_length=255, db_index=True)
	user = models.ForeignKey(IppaUser, related_name="user_bank_account")
	status = models.CharField(max_length=255, default=PENDING, choices=status_choices)

	objects = BankAccountManager()

	def __unicode__(self):
		return self.acc_number + " " + self.acc_name

class TransactionManager(models.Manager):

	def create_txn(self, txn_date=None, txn_type=None, status=None, 
					amount=None, description=None, network=None, user=None):
	
		from Ippa_v1.utils import generate_unique_id
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




