import re
import json

from django.views.generic import View
from django.http import QueryDict

from AccessControl.models import *
from AccessControl.utils import authenticate_user, send_kyc_verified_email_to_user
from Ippa_v1.responses import *
from Ippa_v1.utils import copy_content_to_s3, generate_unique_id
from Ippa_v1.decorators import decorator_4xx

class SignUp(View):
	
	def __init__(self):
		"""Initialize response."""

		self.response = init_response()

	def dispatch(self, *args, **kwargs):

		return super(self.__class__, self).dispatch(*args, **kwargs)

	@decorator_4xx([])
	def get(self, request, *args, **kwargs):

		try:
			self.response["res_str"] = "Player details fetch successfully."
			self.response["res_data"] = request.user.serialize()
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

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

	@decorator_4xx([])
	def put(self, request, *args, **kwargs):
		"""
		Update player details if any data is being updated.
		"""
		player = request.user
		try:
			player.update_user_info(request.params_dict)
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

class UploadAchivements(View):

	def __init__(self):

		self.response = init_response()

	def dispatch(self, *args, **kwargs):

		return super(self.__class__, self).dispatch(*args, **kwargs)

	@decorator_4xx([])
	def post(self, request, *args, **kwargs):

		player = request.user
		achievement_file = request.FILES.get("achievement")
		file_name = request.POST.get("file_name")

		try:
			order_no = len(player.achievements) + 1
			file_s3_url = copy_content_to_s3(achievement_file, "KYC/"+file_name)
			player.achievements.append({
					"order":order_no,
					"unique_id":file_name,
					"s3_url":file_s3_url
				})
			player.save()
			self.response["res_data"] = {"file_url":file_s3_url}
			self.response["res_str"] = "Achievement added successfully."
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)


class UploadKYC(View):

	def __init__(self):

		self.response = init_response()

	def dispatch(self, *args, **kwargs):

		return super(self.__class__, self).dispatch(*args, **kwargs)

	@decorator_4xx([])
	def post(self, request, *args, **kwargs):

		player = request.user
		poi_doc = request.FILES.get("poi")
		poa_doc = request.FILES.get("poa")
		try:
			s3_url_dict = dict()
			if poi_doc:
				file_name = generate_unique_id("FILE")
				file_s3_url = copy_content_to_s3(poi_doc, "KYC/"+file_name)
				player.poi_image = file_s3_url
				s3_url_dict["poi_s3_url"] = file_s3_url
			if poa_doc:
				file_name = generate_unique_id("FILE")
				file_s3_url = copy_content_to_s3(poa_doc, "KYC/"+file_name)
				player.poa_image = file_s3_url
				s3_url_dict["poa_s3_url"] = file_s3_url
			player.save()
			self.response["res_data"] = s3_url_dict
			self.response["res_str"] = "KYC documents added successfully."
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

	@decorator_4xx([])
	def put(self, request, *args, **kwargs):
		player = request.user
		params = request.params_dict
		user_id = params.get("user_id")
		action_list = json.loads(params.get("action_list"))
		try:
			if player.is_admin:
				user = IppaUser.objects.get(player_id=user_id)
				for action in action_list:
					if action.get("doc_type") == "poi":
						if action.get("action_type") == "approved":
							user.poi_status = IppaUser.KYC_APPROVED
						elif action.get("action_type") == "declined":
							user.poi_status = IppaUser.KYC_DECLINED
						send_kyc_verified_email_to_user(KYC_DETAILS_APPROVED, 
										"proof of identity", action, user)
					elif action.get("doc_type") == "poa":
						if action.get("action_type") == "approved":
							user.poa_status = IppaUser.KYC_APPROVED
						elif action.get("action_type") == "declined":
							user.poa_status = IppaUser.KYC_DECLINED
						send_kyc_verified_email_to_user(KYC_DETAILS_APPROVED, 
										"proof of address", action, user)
				user.save()
			else:
				raise ACTION_NOT_ALLOWED(STR_ACTION_NOT_ALLOWED)
			self.response["res_str"] = "KYC documents verified successfully."
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)




