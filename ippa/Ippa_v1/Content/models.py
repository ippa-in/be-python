# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from Ippa_v1.utils import *
from Network.models import Network
from AccessControl.models import IppaUser
from .constants import DEPOSIT_BONUS, FREE_ENTRY_TOURNAMETS


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

	def bulk_serializer(self, queryset, is_logged_in):

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

class AdManager(models.Manager):
	
	def add_ad(self, redirect_url=None, img_url=None):

		ad_order_old = Ad.objects.filter(is_deleted=False).count()
		ad_order_new = ad_order_old + 1
		ad_obj = Ad.objects.create(redirect_url=redirect_url, img_url=img_url, 
									order=ad_order_new)
		return ad_obj

	def bulk_serializer(self, queryset, is_logged_in):

		ad_data = []
		for obj in queryset:
			ad_data.append(obj.serializer())
		return ad_data

class Ad(BaseModel):

	redirect_url = models.TextField(null=True, blank=True)
	img_url = models.TextField(null=True, blank=True)
	order = models.IntegerField()

	objects = AdManager()

	def __unicode__(self):
		return str(self.pk)

	def serializer(self):

		ad_dict = {
			"id":self.pk,
			"redirect_url":self.redirect_url,
			"img_s3_url":self.img_url,
			"order":self.order
		}
		return ad_dict

class PointsManager(models.Manager):

	def add_excel(self, title=None, no_of_rows=None, file_url=None):

		file = Points.objects.create(title=title, total_records=no_of_rows, file_url=file_url)
		return file

	def bulk_serializer(self, queryset, is_logged_in):

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

	def bulk_serializer(self, queryset, is_logged_in):

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

class RedeemedRewardsManager(models.Manager):

	def add_reward_redeemed(self, reward, user):

		redeemed_obj = RedeemedRewards.objects.create(reward=reward,
							user=user,redeemed_date=datetime.now())
		return redeemed_obj

class RedeemedRewards(models.Model):

	reward = models.ForeignKey(Rewards, null=True, blank=True)
	user = models.ForeignKey(IppaUser, null=True, blank=True)
	redeemed_date = models.DateTimeField(null=True, blank=True)
	objects = RedeemedRewardsManager()

	def __unicode__(self):
		return str(self.pk)

class PromotionsManager(models.Manager):

	def create_promotion(self, params, tournament_s3_file, cover_s3_url, htgt_s3_url=""):

		htgt_dict = {
			"htgt_img":htgt_s3_url,
			"promo_code":params.get("promo_code", ""),
			"redirect_url":params.get("redirect_url", "")
		}

		promotion_obj = Promotions.objects.create(
							tournament_title=params.get("tournament_title"),
							cover_img = cover_s3_url,
							network_name=params.get("network_name"),
							introduction={"title":params.get("title"), "description":params.get("description")},
							pokergenie_carousal = params.get("pokergenie_carousal"),
							tournament_file_url = tournament_s3_file,
							deposit_bonus = params.get("deposit_bonus"),
							free_entry_trn = FREE_ENTRY_TOURNAMETS,
							htgt = htgt_dict
							)
		return promotion_obj

class Promotions(BaseModel):

	PENDING = "Pending"
	PREVIEW = "Preview"
	LIVE = "Live"
	status_choices = ((PENDING, "Pending"),(PREVIEW, "Preview"),(LIVE, "Live"))

	tournament_title =  models.TextField(null=True, blank=True)
	tournament_file_url =  models.TextField(null=True, blank=True)
	htgt = JSONField(help_text="How to get Tagged", default=dict(), null=True, blank=True)
	network_logo = models.TextField(null=True, blank=True)
	cover_img = models.TextField(null=True, blank=True)
	term_and_con = models.TextField(null=True, blank=True)
	network_name = models.CharField(max_length=255, blank=True, null=True)
	introduction = JSONField(default=dict(), null=True, blank=True)
	pokergenie_carousal = JSONField(default=list(), null=True, blank=True)
	deposit_bonus = JSONField(default=DEPOSIT_BONUS, null=True, blank=True)
	free_entry_trn = JSONField(default=list(), null=True, blank=True)
	status = models.CharField(max_length=255, default=PENDING, choices=status_choices)
	objects = PromotionsManager()

	def __unicode__(self):
		return str(self.pk)

	def serializer(self):

		promotion_data = dict()
		promotion_data["promo_id"] = self.pk
		promotion_data["tournament_title"] = self.tournament_title
		promotion_data["how_to_get_tagged"] = self.htgt
		promotion_data["network_logo"] = self.network_logo if self.network_logo else ""
		promotion_data["cover_img"] = self.cover_img if self.cover_img else ""
		promotion_data["term_and_con"] = self.term_and_con if self.term_and_con else ""
		promotion_data["network_name"] = self.network_name
		promotion_data["introduction"] = self.introduction
		promotion_data["pokergenie_carousal"] = json.loads(self.pokergenie_carousal)
		promotion_data["deposit_bonus"] = json.loads(self.deposit_bonus)
		promotion_data["free_entry_trn"] = self.free_entry_trn
		promotion_data["status"] = self.status
		promotion_data["htgt_dict"] = self.htgt
		return promotion_data

	def update_promotion(self, data=None, action=None, file_upload=None):

		if action == "update":
			if file_upload == "TOURNAMENT":
				self.tournament_file_url = data
			if file_upload == "COVER":
				self.cover_img = data
			if file_upload == "HTGT":
				self.htgt["htgt_img"] = data
		elif action == "preview":
			self.status = "Preview"
		elif action == "live":
			self.status = "Live"
		else:
			for key, value in data.iteritems():
				if key == "title" and value:
					self.introduction["title"] = value
				if key == "description" and value:
					self.introduction["description"] = value
				if key == "pokergenie_carousal" and value:
					self.pokergenie_carousal = value
				if key == "deposit_bonus" and value:
					self.deposit_bonus = value
				if key == "tournament_title" and value:
					self.tournament_title = value
				if key == "redirect_url" and value:
					self.htgt["redirect_url"] = value
				if key == "promo_code" and value:
					self.htgt["promo_code"] = value
		self.save()

class TournamentsManager(models.Manager):

	def create_tournament(self, tournament_date=None, event_name=None, buy_in=None,
							guaranteed=None, network_name=None):
		tournament_detail = {
			"tournament_date":tournament_date,
			"event_name":event_name,
			"buy_in":buy_in,
			"guaranteed":guaranteed,
			"network_name":network_name
		}
		tournament_obj = Tournaments(**tournament_detail)
		return tournament_obj

	def bulk_serializer(self, queryset, is_logged_in):

		tournament_data = []
		for obj in queryset:
			tournament_data.append(obj.serializer())
		return tournament_data

class Tournaments(BaseModel):

	tournament_date = models.DateTimeField(null=True, blank=True)
	event_name = models.CharField(max_length=255, null=True, blank=True)
	buy_in = models.CharField(max_length=255, null=True, blank=True)
	guaranteed = models.CharField(max_length=255, null=True, blank=True)
	network_name = models.CharField(max_length=255, blank=True, null=True)
	objects = TournamentsManager()

	def __unicode__(self):
		return str(self.pk)

	def serializer(self):

		tournament_data = dict()
		tournament_data["date"] = self.tournament_date
		tournament_data["event_name"] = self.event_name
		tournament_data["buy_in"] = self.buy_in
		tournament_data["guaranteed"] = self.guaranteed
		tournament_data["network_name"] = self.network_name
		return tournament_data

class ActivityManager(models.Manager):

	def add_activity(self, user, content_obj):

		activity_obj = Activity.objects.create(activity="U", posted_by=user,
												content_object=content_obj)

class Activity(BaseModel):

	UPVOTE = 'U'
	activity_choices = ((UPVOTE, 'Upvote'),)

	posted_by = models.ForeignKey(IppaUser, null=True, blank=True)
	activity = models.CharField(max_length=1, choices=activity_choices)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.CharField(max_length=255)
	content_object = GenericForeignKey()

	objects = ActivityManager()

class VideosManger(models.Manager):

	def add_video(self, params, user):

		video_obj = Videos.objects.create(
							video_id=generate_unique_id("VID"),
							title=params.get("title"),
							description = params.get("description"),
							is_featured=True if params.get("is_featured") == "true" else False,
							permission=params.get("permission"),
							video_url=params.get("video_url"),
							posted_by=user,
							thumbnail_img_link= params.get("thumbnail_img_link"),
							game_type=params.get("game_type", list()).split(","),
							skill_level=params.get("skill_level", list()).split(","),
							tags=params.get("tags", list()).split(",")
							)
		return video_obj

	def bulk_serializer(self, queryset, is_logged_in):

		video_data = []
		for obj in queryset:
			video_dict = obj.serialize()
			if is_logged_in and video_dict.get("permission") != Videos.ALL_USERS:
				video_dict.pop("video_url")
			video_data.append(video_dict)
		return video_data

class Videos(BaseModel):

	ALL_USERS = 0
	LOGGED_IN_USERS = 1
	PREMIUM_USERS = 2
	permission_choices = ((ALL_USERS, "ALL USERS"),
					(LOGGED_IN_USERS, "LOGGED IN USERS"),
					(PREMIUM_USERS, "PREMIUM USERS"))

	video_id = models.CharField(max_length=255, primary_key=True)
	title = models.CharField(max_length=255, blank=True, null=True)
	description = models.TextField(null=True, blank=True)
	video_url = models.TextField(null=True, blank=True)
	thumbnail_img_link = models.TextField(null=True, blank=True)
	posted_by = models.ForeignKey(IppaUser, null=True, blank=True)
	game_type = ArrayField(models.CharField(blank=True, max_length=255), blank=True, null=True, default=list())
	skill_level = ArrayField(models.CharField(blank=True, max_length=255), blank=True, null=True, default=list())
	tags = ArrayField(models.CharField(blank=True, max_length=255), blank=True, null=True, default=list())
	views_count = models.IntegerField(default=0)
	is_featured = models.BooleanField(default=False)
	permission = models.IntegerField(default=ALL_USERS, choices=permission_choices)
	upvote_count = models.IntegerField(default=0)
	upvotes = GenericRelation(Activity, related_query_name='video')
	objects = VideosManger()

	def __unicode__(self):
		return str(self.video_id)

	def serialize(self):
		video_data = dict()
		video_data["video_id"] = self.video_id
		video_data["title"] = self.title
		video_data["description"] = self.description
		video_data["video_url"] = self.video_url
		video_data["thumbnail_img_link"] = self.thumbnail_img_link
		video_data["game_type"] = self.game_type
		video_data["skill_level"] = self.skill_level
		video_data["tags"] = self.tags
		video_data["views_count"] = self.views_count
		video_data["is_featured"] = self.is_featured
		video_data["permission"] = self.permission
		video_data["upvote_count"] = self.upvote_count
		video_data["posted_on"] = self.created_on.strftime("%d.%m.%Y")
		video_data["posted_by"] = {"name":self.posted_by.name, "profile_pic_link":self.posted_by.profile_image}
		return video_data

	def update_video(self, data):
		for key, value in data.iteritems():
			if key == "title" and value:
				self.title = value
			if key == "description" and value:
				self.description = value
			if key == "video_url" and value:
				self.video_url = value
			if key == "game_type" and value:
				self.game_type = json.loads(value)
			if key == "skill_level" and value:
				self.skill_level = json.loads(value)
			if key == "tags" and value:
				self.tags = json.loads(value)
			if key == "is_featured" and value:
				self.is_featured = value
			if key == "permission" and value:
				self.permission = value
		self.save()

class CommentsManager(models.Manager):

	def add_comments(self, user, comment, content_obj):

		comment_obj = Comments.objects.create(posted_by=user, 
											comment=comment,
											content_object=content_obj)

class Comments(BaseModel):

	comment = models.TextField(blank=True)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.CharField(max_length=255)
	posted_by = models.ForeignKey(IppaUser, null=True, blank=True) 
	content_object = GenericForeignKey()
	upvotes = GenericRelation(Activity, related_query_name='comments')

	objects = CommentsManager()

	def __unicode__(self):
		return str(self.pk)

	def serialize(self):

		comment_data = dict()
		comment_data["comment_id"] = self.pk
		comment_data["comment"] = self.comment
		comment_data["upvotes"] = self.upvotes.count()
		comment_data["posted_on"] = self.created_on.strftime("%-M") + " min"
		comment_data["posted_by"] = {"name":self.posted_by.name, "profile_pic_link":self.posted_by.profile_image}
		return comment_data





