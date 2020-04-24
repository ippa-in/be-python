# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from Ippa_v1.utils import *
from Network.models import Network

# Create your models here.
class BaseModel(models.Model):

	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	is_deleted = models.SmallIntegerField(default=0)

	class Meta:
		abstract = True

class DashBoardImageManager(models.Manager):
	
	def add_dashboard_image(self, title=None, description=None, img_url=None):

		img_order_old = DashBoardImage.objects.all().count()
		img_order_new = img_order_old + 1
		image = DashBoardImage.objects.create(title=title, description=description,
											img_url=img_url, order=img_order_new)
		return image

	def bulk_serializer(self, queryset):

		image_data = []
		for obj in queryset:
			image_data.append(obj.serializer())
		return image_data

class DashBoardImage(BaseModel):

	title = models.TextField(null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	img_url = models.TextField(null=True, blank=True)
	order = models.IntegerField()

	objects = DashBoardImageManager()

	def __unicode__(self):
		return str(self.pk)

	def serializer(self):

		image_dict = {
			"id":self.pk,
			"title":self.title,
			"description":self.description,
			"img_s3_url":self.img_url,
			"order":self.order
		}
		return image_dict

	def update_dashboard_image(self, title=None, description=None, img_url=None):

		if title:
			self.title = title
		if description:
			self.description = description
		if img_url:
			self.img_url = img_url
		self.save()

class PointsManager(models.Manager):

	def add_excel(self, title=None, no_of_rows=None, file_url=None):

		file = Points.objects.create(title=title, total_records=no_of_rows, file_url=file_url)
		return file

	def bulk_serializer(self, queryset):

		points_data = []
		for obj in queryset:
			points_data.append(obj.serialize())
		return points_data

class Points(BaseModel):

	PENDING = "Pending"
	APPROVED = "Approved"
	DECLINED = "Declined"
	FAILED = "Failed"
	status_choices = ((PENDING, "Pending"),
					(APPROVED, "Approved"),
					(DECLINED, "Declined"),
					(FAILED, "Failed"))

	title = models.CharField(max_length=255, blank=True, null=True)
	total_records = models.IntegerField()
	status = models.CharField(max_length=255, default=PENDING, choices=status_choices)
	file_url = models.TextField(null=True, blank=True)

	objects = PointsManager()

	def __unicode__(self):
		return str(self.title)

	def serialize(self):

		file_data = dict()
		file_data["file_id"] = self.pk
		file_data["title"] = self.title
		file_data["total_records"] = self.total_records
		file_data["status"] = self.status
		file_data["created_on"] = convert_datetime_to_string(self.created_on, "%d %b %Y %I:%M %p")
		return file_data

class RewardsManager(models.Manager):

	def bulk_serializer(self, queryset):

		rewards_data = []
		for obj in queryset:
			rewards_data.append(obj.serialize())
		return rewards_data

	def take_action(self, reward_id, action, comments):
		if action == "DELETED":
			reward_obj = Rewards.objects.get(pk=reward_id)
			reward_obj.is_deleted = True
			reward_obj.save()
			return reward_obj

class Rewards(BaseModel):

	PENDING = "Pending"
	ACTIVE = "Active"
	DEACTIVE = "Deactive"
	EXPIRED = "Expired"
	status_choices = ((PENDING, "Pending"),
					(ACTIVE, "Active"),
					(DEACTIVE, "Deactive"),
					(EXPIRED, "Expired"))

	title = models.CharField(max_length=255, blank=True, null=True)
	description = models.TextField(null=True, blank=True)
	from_date = models.DateTimeField()
	to_date = models.DateTimeField()
	deactivate_date = models.DateTimeField()
	network = models.ForeignKey(Network, null=True, blank=True, related_name="network_reward")
	point_name = models.TextField(null=True, blank=True)
	goal_points = models.CharField(max_length=255, blank=True, null=True)
	more_info_link = models.TextField(null=True, blank=True)
	status = models.CharField(max_length=255, default=ACTIVE, choices=status_choices)
	is_redeemed = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	objects = RewardsManager()

	def __unicode__(self):
		return str(self.title)

	def serialize(self):

		reward_data = dict()
		reward_data["reward_id"] = self.pk
		reward_data["title"] = self.title
		reward_data["description"] = self.description
		reward_data["from_date"] = self.from_date
		reward_data["to_date"] = self.to_date
		reward_data["status"] = self.status
		reward_data["network"] = {"name":self.network.name, "id": self.network.pk, "image_url":self.network.image_url}
		reward_data["point_name"] = self.point_name
		reward_data["goal_points"] = self.goal_points
		reward_data["more_info_link"] = self.more_info_link
		reward_data["is_redeemed"] = self.is_redeemed
		reward_data["is_active"] = self.is_active
		return reward_data


