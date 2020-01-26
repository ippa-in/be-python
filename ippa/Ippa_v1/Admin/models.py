# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType

from AccessControl.models import IppaUser

# Create your models here.
class BaseModel(models.Model):

	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	is_deleted = models.BooleanField(default=False)

	class Meta:
		abstract = True

class ActionLogManager(models.Manager):

	def add_action_log(self, admin, content_type, action, content_id, comments=None):

		log_details = {
			"admin":admin,
			"content_id":content_id,
			"action":action,
			"comments":comments,
			"content_type":content_type
		}
		log_obj = self.create(**log_details)
		return log_obj

class ActionLog(BaseModel):

	content_id = models.CharField(max_length=255, null=True, blank=True)
	admin = models.ForeignKey(IppaUser, related_name="admin_action_log")
	action = models.CharField(max_length=255, null=True, blank=True)
	comments = models.TextField(default='', null=True, blank=True)
	content_type = models.ForeignKey(ContentType, null=True, blank=True)
	objects = ActionLogManager()

	def __unicode__(self):
		return self.content_id

	def serialize(self):

		log_details = dict()
		log_details["log_id"] = self.log_id
		log_details["name"] = self.name
		return log_details
