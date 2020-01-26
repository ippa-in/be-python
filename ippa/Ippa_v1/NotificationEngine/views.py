# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic import View

from Ippa_v1.decorators import decorator_4xx, decorator_4xx_admin
from Ippa_v1.responses import *
from .models import NotificationMessage

class PendingNotifications(View):

	def __init__(self):
		self.response = init_response()

	def dispatch(self, *args, **kwargs):
		return super(self.__class__, self).dispatch(*args, **kwargs)

	@decorator_4xx_admin([])
	def get(self, request, *args, **kwargs):
		
		try:
			notifications = NotificationMessage.objects.filter(has_read=False)
			notifications_list = list()
			for notification in notifications:
				notifications_list.append(notification.serialize())
			self.response["res_str"] = "Notificaitons fetched successfully."
			self.response["res_data"] = notifications_list
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

	@decorator_4xx_admin([])
	def put(self, request, *args, **kwargs):
		
		try:
			notifications = NotificationMessage.objects.all()
			notifications.update(has_read=True)
			self.response["res_str"] = "Notificaitons updated successfully."
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

