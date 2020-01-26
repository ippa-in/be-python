# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View

from Ippa_v1.decorators import decorator_4xx_admin
from Ippa_v1.responses import *
from Filter.models import SearchConfiguration
from .models import ActionLog

# Create your views here.
class AdminAction(View):

	def __init__(self):

		self.response = init_response()

	def dispatch(self, *args, **kwargs):

		return super(self.__class__, self).dispatch(*args, **kwargs)

	@decorator_4xx_admin([])
	def post(self, request, *args, **kwargs):

		user = request.user
		params = request.params_dict
		content_id = params.get("content_id")
		display_name = params.get("content_type")
		action = params.get("action")
		comments = params.get("comments" , "")

		try:
			search_config = SearchConfiguration.objects.get(display_name=display_name)
			content_type = search_config.content_type
			model = content_type.model_class()

			#log which admin is going to take which action on what model.
			action_log = ActionLog.objects.add_action_log(admin=user, content_type=content_type,
										action=action, content_id=content_id, comments=comments)

			#take action on that content
			model_obj = model.objects.take_action(content_id, action=action, comments=comments)

			self.response["res_data"] = {"model_pk":model_obj.pk}
			self.response["res_str"] = "Action is taken successfully."
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)
