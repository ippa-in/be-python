# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q

from Network.models import Network, PlayerTag
from Ippa_v1.decorators import decorator_4xx, decorator_4xx_admin
from .exceptions import USERNAME_ALREADY_TAKEN
from .constants import USER_NAME_ALREADY_EXISTS
from Ippa_v1.responses import *
from Ippa_v1.redis_utils import is_token_exists
from AccessControl.models import IppaUser
from Content.constants import EDITABLE_FIELDS

# Create your views here.
class ManageNetwork(View):

	def __init__(self):
		self.response = init_response()

	def dispatch(self, *args, **kwargs):

		return super(self.__class__, self).dispatch(*args, **kwargs)

	@decorator_4xx([])
	def get(self, request, *args, **kwargs):

		try:
			tagged_user_networks_ids = PlayerTag.objects.filter(user=request.user)\
							.values_list('network_id', flat=True)
			networks = Network.objects.filter(status="Active").exclude(network_id__in=tagged_user_networks_ids)
			networks_list = list()
			for network in networks:
				networks_list.append(network.serialize())
			self.response["res_str"] = "Network details fetch successfully."
			self.response["res_data"] = networks_list
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

	@decorator_4xx_admin([])
	def post(self, request, *args, **kwargs):
		"""
		Adding a network.
		"""
		params = request.POST
		try:
			network = Network.objects.create_network(params)
			self.response["res_str"] = "Network added successfully."
			self.response["res_data"] = {"network_id":network.pk}
			return send_201(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

class NetworkTagging(View):

	def __init__(self):
		self.response = init_response()

	def dispatch(self, *args, **kwargs):

		return super(self.__class__, self).dispatch(*args, **kwargs)

	@decorator_4xx([])
	def get(self, request, *args, **kwargs):

		try:
			tagging_list = PlayerTag.objects.filter((Q(status="Pending") 
													|Q(status="Verified")),
													user=request.user)
			tagging_res = list()
			for tagging in tagging_list:
				tagging_res.append(tagging.serialize())
			self.response["res_str"] = "Tagging details fetch successfully."
			self.response["res_data"] = tagging_res
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

	@decorator_4xx([])
	def post(self, request, *args, **kwargs):
		"""
		Register a player after validating email-id and password format.
		"""

		params = request.POST
		network_id = params.get("network_id")
		tag_user_name = params.get("tag_user_name")
		user = request.user
		try:
			tagged_user = PlayerTag.objects.filter(network_id=network_id, 
													tag_user_name=tag_user_name)
			if tagged_user.exists():
				raise USERNAME_ALREADY_TAKEN(USER_NAME_ALREADY_EXISTS)

			tagging = PlayerTag.objects.create_tagging(network_id,
												tag_user_name, user)
			self.response["res_str"] = "User tagged successfully."
			self.response["res_data"] = {"network_id":tagging.pk}
			return send_201(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

class NetworkNames(View):

	def __init__(self):
		self.response = init_response()

	def dispatch(self, *args, **kwargs):

		return super(self.__class__, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):

		is_logged_in = False
		is_admin = False
		login_token = request.META.get("HTTP_PLAYER_TOKEN")
		if login_token and is_token_exists(login_token):
			is_logged_in = True
			player_id = request.META.get("HTTP_PLAYER_ID")
			user = IppaUser.objects.get(player_id=player_id)
			is_admin = user.is_admin
		try:
			networks = Network.objects.filter(status="Active").values_list('name', flat=True)
			networks = list(networks)
			self.response["res_str"] = "Network names fetch successfully."
			self.response["res_data"] = {
											"network_names":networks,
											"editable_fields":EDITABLE_FIELDS
										}
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)