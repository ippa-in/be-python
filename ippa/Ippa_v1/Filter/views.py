# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render
from django.views.generic import View

from Ippa_v1.responses import *
from .models import SearchConfiguration, SearchField
from .utils import get_foreign_keys
from Ippa_v1.redis_utils import is_token_exists
from Ippa_v1.decorators import decorator_4xx
from Content.constants import CONTENT_COLUMN_MAPPING

# Create your views here.
class SearchFieldView(View):

	def __init__(self):
		self.response = init_response()

	def dispatch(self, *args, **kwargs):

		return super(self.__class__, self).dispatch(*args, **kwargs)

	@decorator_4xx([])
	def get(self, request, *args, **kwargs):

		params = request.params_dict
		content_name = params.get("display_name")
		try:
			search_config = SearchConfiguration.objects.get(display_name=content_name)
			search_fields = SearchField.objects.filter(search_config=search_config, 
														status=True).\
														order_by('order')
			filter_field_data = list()
			sort_field_data = list()
			for field in search_fields:
				serialized_data = field.serialize()
				if serialized_data.get("is_sortable"):
					sort_field_data.append(serialized_data)
				else:
					filter_field_data.append(serialized_data)
			self.response["res_str"] = "Filter config fetch successfully."
			self.response["res_data"] = {
				"filters":filter_field_data,	
				"sort":sort_field_data,
				"colums":CONTENT_COLUMN_MAPPING.get(content_name, list())
			}
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

class FilterView(View):

	def __init__(self):
		self.response = init_response()

	def dispatch(self, *args, **kwargs):

		return super(self.__class__, self).dispatch(*args, **kwargs)

	@decorator_4xx([])
	def get(self, request, *args, **kwargs):
		"""Filter and sort data based on display name.
		data_type = all: don't apply any filter and return paginated data.
		"""
		params = request.params_dict
		filters = json.loads(params.get("filters", str(dict())))
		sortable = json.loads(params.get("sortable", str(dict())))
		limit = params.get("limit")
		offset = params.get("offset")
		data_type = params.get("data_type")
		pre_query = json.loads(params.get("query", str(dict())))
		pre_sort = json.loads(params.get("sort_query", str(list())))
		is_logged_in = False
		login_token = request.META.get("HTTP_PLAYER_TOKEN")
		if login_token and is_token_exists(login_token):
			is_logged_in = True
		try:
			search_config = SearchConfiguration.objects.get(display_name=params.get("display_name"))
			content_type = search_config.content_type
			model = content_type.model_class()
			select_related_fields = get_foreign_keys(model)

			search_id_value_map = dict()
			if data_type == "all":
				filter_query_set = model.objects.filter(is_deleted=False, **pre_query)
			else:
				#apply filters
				filter_search_field_ids = filters.keys()
				search_fields = SearchField.objects.filter(pk__in=filter_search_field_ids, status=True,
														search_config=search_config)
				for search_field in search_fields:
					search_id_value_map[str(search_field.pk)] = search_field.serialize()
				filter_dict = dict()
				for key, value in search_id_value_map.iteritems():
					filter_values = filters.get(key)
					filter_type = value.get("filter_type")
					field_name = value.get("field_name")
					if filter_type == "daterange":
						filter_dict[field_name+"__gte"] = filter_values.get("min_range")
						filter_dict[field_name+"__lte"] = filter_values.get("max_range")
					if filter_type == "dropdown":
						filter_dict[field_name+"__in"] = filter_values.get("dropdown_values")
					if filter_type == "date":
						filter_dict[field_name] = filter_values.get("date")
					if filter_type == "multiselectdropdown":
						filter_dict[field_name+"__overlap"] = filter_values.get("dropdown_values")
					if filter_type == "look_ahead":
						filter_dict[field_name+"__icontains"] = filter_values.get("look_text", "")
				#Apply User Filter
				user_search_field = SearchField.objects.filter(is_user_filter=True, status=True, search_config=search_config)
				if user_search_field and is_logged_in:
					filter_dict["user"] = request.user
				filter_dict["is_deleted"] = False
				filter_query_set = model.objects.select_related(*select_related_fields).filter(**filter_dict)

			#paginated response.
			if limit:
				filter_query_set_ids = list(filter_query_set.values_list("pk", flat=True))
				paginated_ids = filter_query_set_ids[int(offset):int(limit)]
				filter_query_set = model.objects.select_related(*select_related_fields)\
												.filter(pk__in=paginated_ids, is_deleted=False)

			#apply sort
			sort_search_fields_ids = sortable.keys()
			search_fields =SearchField.objects.filter(pk__in=sort_search_fields_ids, 
													  status=True, is_sortable=True,
													  search_config=search_config)
			for search_field in search_fields:
				search_id_value_map[str(search_field.pk)] = search_field.serialize()
			sort_field_list = list()
			for key, value in search_id_value_map.iteritems():
				sort_order = sortable.get(key)
				field_name = value.get("field_name")
				if sort_order == "ASC":
					sort_field_list.append(field_name)
				if sort_order == "DESC":
					sort_field_list.append("-"+field_name)
			filter_sorted_query_set = filter_query_set.order_by(*sort_field_list)

			if data_type == "all":
				filter_sorted_query_set = filter_sorted_query_set.order_by(*pre_sort)
			#Return serialized response.
			filter_sorted_query_data = model.objects.bulk_serializer(filter_sorted_query_set, is_logged_in)
			self.response["res_str"] = "Data fetched successfully."
			self.response["res_data"] = filter_sorted_query_data
			return send_201(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

