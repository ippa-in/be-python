# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class BaseModel(models.Model):

	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	is_deleted = models.SmallIntegerField(default=0)

	class Meta:
		abstract = True

class SearchConfigurationManager(models.Manager):
	pass

class SearchConfiguration(BaseModel):

	display_name = models.CharField(max_length=255)
	content_type = models.ForeignKey(ContentType, null=True, blank=True)

	objects = SearchConfigurationManager()

	def __unicode__(self):
		return self.display_name

class SearchFieldManager(models.Manager):
	pass

class SearchField(BaseModel):

	filter_choices = (
						("daterange", "daterange"),
						("dropdown", "dropdown"),
						("date", "date")
					)

	search_config = models.ForeignKey(SearchConfiguration, null=True, blank=True)
	display_name = models.CharField(max_length=255, null=True, blank=True)
	field_name = models.CharField(max_length=255, null=True, blank=True)
	filter_type = models.CharField(max_length=255, null=True, blank=True, choices=filter_choices)
	values = models.TextField(null=True, blank=True)
	order = models.IntegerField(null=True, blank=True)
	status = models.BooleanField(default=False)
	is_sortable = models.BooleanField(default=False)
	is_user_filter = models.BooleanField(default=False)

	objects = SearchFieldManager()

	def __unicode__(self):
		return str(self.pk) + " " + self.display_name

	def serialize(self):

		field_data = dict()
		field_data["id"] = self.pk
		field_data["display_name"] = self.display_name
		field_data["filter_type"] = self.filter_type
		field_data["field_name"] = self.field_name
		if self.filter_type == "dropdown":
			field_data["values"] = self.values.split(',')
		else:
			field_data["values"] = list()
		field_data["order"] = self.order
		field_data["is_sortable"] = self.is_sortable
		return field_data
