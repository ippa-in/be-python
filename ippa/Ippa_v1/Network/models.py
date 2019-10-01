# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from AccessControl.models import IppaUser
from Ippa_v1.utils import generate_unique_id


# Create your models here.
class BaseModel(models.Model):

	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	is_deleted = models.SmallIntegerField(default=0)

	class Meta:
		abstract = True

class NetworkManager(models.Manager):
	
	def create_network(self, data):
		
		network_dict = {
			"network_id":generate_unique_id("NTWRK"),
			"name": data.get("name"),
			"network_url": data.get("network_url"),
			"image_url":data.get("image_url"),
		}
		network = Network.objects.create(**network_dict)
		return network
	
class Network(BaseModel):

	ACTIVE = "Active"
	DELEATED = "Deleted"

	status_choices = ((ACTIVE, 'Active'),
						(DELEATED, 'Deleted'))

	network_id = models.CharField(max_length=255, primary_key=True)
	name = models.CharField(max_length=255, null=True, blank=True)
	network_url = models.URLField(max_length=200, null=True, blank=True)
	image_url =  models.URLField(max_length=200, null=True, blank=True)
	net_to_ippa_exp = models.CharField(max_length=255, null=True, blank=True)
	status = models.CharField(max_length=255, default=ACTIVE, choices=status_choices)
	objects = NetworkManager()

	def __unicode__(self):
		return self.network_id + " " + self.name

	def serialize(self):

		network_details = {}
		network_details["network_id"] = self.network_id
		network_details["name"] = self.name
		network_details["image_url"] = self.image_url
		return network_details

class PlayerTagManager(models.Manager):
	
	def create_tagging(self, network_id, tag_user_name, user):

		tagging_dict = {
			"tag_id":generate_unique_id("TAGG"),
			"user": user,
			"network_id": network_id,
			"tag_user_name":tag_user_name,
		}
		tagging = PlayerTag.objects.create(**tagging_dict)
		return tagging

class PlayerTag(BaseModel):

	PENDING = "Pending"
	VERIFIED = "Verified"
	DECLINED = "Declined"

	status_choices = ((PENDING, "Pending"),
						(VERIFIED, "Verified"),
						(DECLINED, "Declined")
					)

	tag_id = models.CharField(max_length=255, primary_key=True)
	user = models.ForeignKey(IppaUser, null=True, blank=True, related_name="user_network")
	network = models.ForeignKey(Network, null=True, blank=True, related_name="network_users")
	status = models.CharField(max_length=255, default=PENDING, choices=status_choices)
	tag_user_name = models.CharField(max_length=255, null=True, blank=True)
	points_earned = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

	objects = PlayerTagManager()

	def __unicode__(self):
		return self.user_id + " " + self.network_id + " " + self.tag_name

	def serialize(self):

		tagging_dict = dict()
		tagging_dict["tag_id"] = self.tag_id
		tagging_dict["network"] = self.network.serialize()
		tagging_dict["user_name"] = self.tag_user_name
		tagging_dict["status"] = self.status
		return tagging_dict
		




