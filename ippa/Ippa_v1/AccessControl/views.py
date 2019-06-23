import re

from django.views.generic import View
from django.http import QueryDict

from AccessControl.models import *
from AccessControl.utils import authenticate_user
from Ippa_v1.responses import *

class SignUp(View):
	
	def __init__(self):
		"""Initialize response."""

		self.response = init_response()

	def dispatch(self, *args, **kwargs):

		return super(self.__class__, self).dispatch(*args, **kwargs)

	def _init_user_details(self, params):

		self.name = params.get("name")
		self.dob = params.get("dob")
		self.mobile_number = params.get("mobile_number")
		self.city = params.get("city")

	def _is_info_updated(self):

		self.is_updated_info = False
		for field in EDITABLE_FIELDS:
			updated_value = eval("self."+field)
			if updated_value:
				self.is_updated_info = self.is_updated_info or\
						updated_value != eval("self.edited_user."+field)



	def post(self, request, *args, **kwargs):
		"""
		Register a player after validating email-id and password format.
		"""

		params = request.POST
		try:
			user = IppaUser.objects.create_user(params)
			self.response["res_str"] = "Player registered successfully."
			self.response["res_data"] = {"player_id":user.pk}
			return send_201(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

	def put(self, request, *args, **kwargs):
		"""
		Update player details if any data is being updated.
		"""

		params = QueryDict(request.body)
		self.edited_user = request.user
		try:
			self._init_user_details(params)
			self._is_info_updated()
			if self.is_updated_info:
				with transaction.atomic():
					self.edited_user.updated_user_info(name=self.name,
													   dob=self.dob,
													   mobile_number=self.mobile_number,
													   city=self.city)
			self.response["res_str"] = "Player information successfully updated."
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

class LogIn(View):

	def __init__(self):
		"""Initialize response."""

		self.response = init_response()

	def dispatch(self, *args, **kwargs):

		return super(self.__class__, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):

		import pdb;pdb.set_trace()
		params = request.POST
		email_id = params.get("email_id")
		password = params.get("password")
		try:
			code, res_str, res_data = authenticate_user(email_id, password)
			self.response["res_str"] = res_str
			if code != SUCCESSFUL_LOGIN:
				return send_400(self.response)
			resp = send_200(self.response)
			resp["PLAYER-ID"] = res_data.get("cid")
			resp["PLAYER-TOKEN"] = res_data.get("token")
			resp['Access-Control-Expose-Headers'] = "PLAYER-ID, PLAYER-TOKEN"
			return resp
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)



