from __future__ import unicode_literals

from django.db import models, transaction
from django.contrib.postgres.fields import ArrayField, JSONField

from AccessControl.constants import *
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

	def _validate_user_data(self):

		from AccessControl.utils import valid_email_id, validate_password

		validate_password(self.password)
		if not valid_email_id(self.email_id):
			raise Exception("{0} is not valid".format(self.email_id))

	def _get_user_data_dict(self, params):

		from Ippa_v1.utils import generate_unique_id
		from AccessControl.utils import gen_password_hash

		user_data = {
			"player_id":generate_unique_id("IPPA"),
			"email_id":params.get("email_id"),
			"password":gen_password_hash(params.get("password"))
		}
		return user_data

	def create_user(self, params):

		self._init_user_params(params)
		self._validate_user_data()
		user = IppaUser.objects.filter(email_id=self.email_id)
		if user.exists():
			raise Exception(USER_ALREADY_EXISTS_STR)
		user_data_set = self._get_user_data_dict(params)
		with transaction.atomic():
			ippa_user = IppaUser.objects.create(**user_data_set)
		return ippa_user

class IppaUser(BaseModel):
	"""
		Users can be admin or players.
	"""

	KYC_APPROVED = 0
	KYC_PENDING = 1
	KYC_DECLINED = 2
	KYC_STATUS = ((KYC_PENDING, 'Pending'),
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
	is_mobile_number_verified = models.BooleanField(default=False)
	poi_image = models.TextField(null=True, blank=True, help_text="Proof of identity.(Kyc currently)")
	poa_image = models.TextField(null=True, blank=True, help_text="Proof of address.")
	kyc_status = models.PositiveSmallIntegerField(default=3, choices=KYC_STATUS)
	referral_code = models.CharField(max_length=255, null=True, blank=True)
	city = models.CharField(max_length=255, null=True, blank=True)
	country = models.CharField(max_length=255, default="India")
	profile_image = models.TextField(null=True, blank=True)
	favourite_hands = ArrayField(models.CharField(blank=True, max_length=10), blank=True, null=True, default=list())
	achievements = JSONField(default=list(), null=True, blank=True)
	points = JSONField(default=POINTS_DICT, null=True, blank=True)

	objects = IppaUserManager()

	def __unicode__(self):
		return str(self.player_id) + " " + str(self.name)

	def serialize(self):

		user_details = dict()
		user_details["player_id"] = self.player_id
		user_details["email_id"] = self.email_id
		user_details["referral_code"] = self.referral_code
		user_details["name"] = self.name
		user_details["user_name"] = self.user_name
		user_details["dob"]	= self.dob
		user_details["mobile_number"] = self.mobile_number
		user_details["email_id"] = self.email_id
		user_details["points"] = self.points
		user_details["favourite_hands"] = self.favourite_hands
		user_details["achievements"] = sorted(self.achievements, key=lambda achi: achi["order"])
		return user_details

	def update_user_info(self, params_dict):

		for key, value in params_dict.iteritems():
			if key == "name" and value:
				self.name = value
			if key == "dob" and value:
				self.dob = value
			if key == "city" and value:
				self.city = value
			if key == "favourite_hands" and value:
				self.favourite_hands.append(value)
		self.save()
