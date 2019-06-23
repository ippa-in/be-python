from __future__ import unicode_literals

from django.db import models, transaction
from django.db.models import Q

from AccessControl.constants import *
from AccessControl.utils import get_user_data_dict
from Ippa_v1.constants import *

# Create your models here.
class BaseModel(models.Model):

	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	is_deleted = models.SmallIntegerField(default=0)

	class Meta:
		abstract = True

class IppaUserManager(models.Manager):

	def _init_user_params(self, params):

		self.email_id = params.get("email_id")
		self.password = params.get("password")
		self.referral_code = params.get("referral_code")
		self.user_name = params.get("user_name")

	def _validate_user_data(self):

		from AccessControl.utils import valid_email_id, validate_password

		validate_password(self.password)
		if not valid_email_id(self.email_id):
			raise Exception("{0} is not valid".format(self.email_id))

	def create_user(self, params):

		self._init_user_params(params)
		self._validate_user_data()
		user = IppaUser.objects.filter(Q(email_id=self.email_id)  
									|Q(user_name=self.user_name))
		if user.exists():
			raise Exception(USER_ALREADY_EXISTS_STR)
		user_data_set = get_user_data_dict(params)
		with transaction.atomic():
			ippa_user = IppaUser.objects.create(**user_data_set)
		return ippa_user

class IppaUser(BaseModel):
	"""
		Users can be admin or players.
	"""

	KYC_APPROVED = 0
	KYC_PENDING = 1
	KYC_NOT_INITIATED = 3
	KYC_DECLINED = 2
	KYC_STATUS = ((KYC_NOT_INITIATED, 'Not-initiated'),
				  (KYC_PENDING, 'Pending'),
				  (KYC_APPROVED, 'Approved'),
				  (KYC_DECLINED, 'Declined'),)

	player_id = models.CharField(max_length=255, primary_key=True)
	name = models.CharField(max_length=255, null=True, blank=True)
	user_name = models.CharField(max_length=255, null=True, blank=True)
	mobile_number = models.CharField(max_length=255, null=True, blank=True)
	email_id = models.EmailField(max_length=255, db_index=True)
	dob = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	is_admin = models.BooleanField(default=False)
	password = models.TextField(max_length=255)
	is_email_verified = models.BooleanField(default=False)
	poi_image = models.TextField(null=True, blank=True)
	kyc_status = models.PositiveSmallIntegerField(default=3, choices=KYC_STATUS)
	referral_code = models.CharField(max_length=255, null=True, blank=True)
	city = models.CharField(max_length=255, null=True, blank=True)
	country = models.CharField(max_length=255, default="India")
	profile_image = models.TextField(null=True, blank=True)

	objects = IppaUserManager()

	def __unicode__(self):
		return str(self.player_id) + " " + str(self.name)

	def updated_user_info(self, **kwargs):
		self.name = kwargs.get("name")
		self.dob = kwargs.get("dob")
		self.mobile_number = kwargs.get("mobile_number")
		self.city = kwargs.get("city")
		self.save()