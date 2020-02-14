import re
import json

from django.views.generic import View
from django.http import QueryDict

from AccessControl.models import *
from AccessControl.utils import (authenticate_user, gen_password_hash, validate_password,
								send_email_verification_link, send_reset_password_link,
								create_auth_token)
from AccessControl.constants import *
from AccessControl.exceptions import *
from Ippa_v1.responses import *
from Ippa_v1.utils import (copy_content_to_s3, generate_unique_id)
from Ippa_v1.decorators import decorator_4xx, email_decorator_4xx, decorator_4xx_admin
from Ippa_v1.redis_utils import set_token, get_token
from NotificationEngine.models import NotificationMessage

class SignUp(View):
	
	def __init__(self):
		"""Initialize response."""

		self.response = init_response()

	def dispatch(self, *args, **kwargs):

		return super(self.__class__, self).dispatch(*args, **kwargs)

	@email_decorator_4xx([])
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
			email_id = params.get("email_id")
			token = create_auth_token(user.player_id)
			set_token(token, user.player_id)
			send_email_verification_link(EMAIL_VERIFICATION_NOTI, token, user)
			#add notification string.
			NotificationMessage.objects.add_notification_str(NOTIFICATION_STRING_SIGNUP.format(user.name))
			self.response["res_str"] = "Player registered successfully."
			self.response["res_data"] = {"player_id":user.pk}
			return send_201(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

	@email_decorator_4xx([])
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
			if code != SUCCESSFUL_LOGIN:
				raise Exception(res_str)
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
		title = request.POST.get("title")

		try:
			order_no = len(player.achievements) + 1
			file_name = generate_unique_id("ACHIEVE")
			file_s3_url = copy_content_to_s3(achievement_file, "ACHIEVE/"+file_name)
			player.achievements.append({
					"order":order_no,
					"unique_id":title,
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
	def get(self, request, *args, **kwargs):

		user = request.user
		try:
			kyc_details = dict()
			poi_image = user.poi_image.split(",") if user.poi_image else ""
			if poi_image:
				kyc_details["poi_f_url"] = poi_image[0]
				kyc_details["poi_b_url"] = poi_image[1]
				kyc_details["poi_status"] = user.poi_status if user.poi_status else ""
			poa_image = user.poa_image.split(",") if user.poa_image else ""
			if poa_image:
				kyc_details["poa_f_url"] = poa_image[0]
				kyc_details["poa_b_url"] = poa_image[1]
				kyc_details["poa_status"] = user.poi_status if user.poi_status else ""
			self.response["res_str"] = "kyc details fetch successfully."
			self.response["res_data"] = kyc_details
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

	@decorator_4xx([])
	def post(self, request, *args, **kwargs):

		player = request.user
		poi_doc_f = request.FILES.get("poi_f")
		poi_doc_b = request.FILES.get("poi_b")
		poa_doc_f = request.FILES.get("poa_f")
		poa_doc_b = request.FILES.get("poa_b")
		try:
			s3_url_dict = dict()
			poi_doc_f_s3_url, poi_doc_b_s3_url, poa_doc_f_s3_url, poa_doc_b_s3_url = "","","",""
			if poi_doc_f:
				file_name = generate_unique_id("FRONT")
				poi_doc_f_s3_url = copy_content_to_s3(poi_doc_f, "KYC/"+file_name)
				s3_url_dict["poi_doc_f_s3_url"] = poi_doc_f_s3_url
				player.poi_status = IppaUser.KYC_PENDING
				player.poi_image = poi_doc_f_s3_url
			if poi_doc_b:
				file_name = generate_unique_id("BACK")
				poi_doc_b_s3_url = copy_content_to_s3(poi_doc_b, "KYC/"+file_name)
				s3_url_dict["poi_doc_b_s3_url"] = poi_doc_b_s3_url
				player.poi_status = IppaUser.KYC_PENDING
				player.poi_image = player.poi_image + poi_doc_b_s3_url
			if poa_doc_f:
				file_name = generate_unique_id("FRONT")
				poa_doc_f_s3_url = copy_content_to_s3(poa_doc_f, "KYC/"+file_name)
				s3_url_dict["poa_doc_f_s3_url"] = poa_doc_f_s3_url
				player.poa_status = IppaUser.KYC_PENDING
				player.poa_image = poa_doc_f_s3_url
			if poa_doc_b:
				file_name = generate_unique_id("BACK")
				poa_doc_b_s3_url = copy_content_to_s3(poa_doc_b, "KYC/"+file_name)
				s3_url_dict["poa_doc_b_s3_url"] = poa_doc_b_s3_url
				player.poa_status = IppaUser.KYC_PENDING
				player.poa_image = player.poa_image + poa_doc_b_s3_url
			player.save()
			NotificationMessage.objects.add_notification_str(NOTIFICATION_STRING_KYC.format(player.name))
			send_kyc_document_upload_link(user)
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
					elif action.get("doc_type") == "poa":
						if action.get("action_type") == "approved":
							user.poa_status = IppaUser.KYC_APPROVED
						elif action.get("action_type") == "declined":
							user.poa_status = IppaUser.KYC_DECLINED
				user.save()
				#Update Kyc Status
				if user.poi_status == IppaUser.KYC_APPROVED and user.poa_status == IppaUser.KYC_APPROVED:
					user.kyc_status = IppaUser.KYC_APPROVED
					send_kyc_approved_email_to_user(user)
				elif user.poi_status == IppaUser.KYC_DECLINED and user.poa_status == IppaUser.KYC_DECLINED:
					user.kyc_status = IppaUser.KYC_DECLINED
					send_kyc_declined_email_to_user(user)
			else:
				raise ACTION_NOT_ALLOWED(STR_ACTION_NOT_ALLOWED)
			self.response["res_str"] = "KYC documents verified successfully."
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)


class VerifyEmail(View):
	
	def __init__(self):
		"""Initialize response."""

		self.response = init_response()

	def dispatch(self, *args, **kwargs):

		return super(self.__class__, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):

		params = request.POST
		try:
			token = params.get("token")
			player_id = get_token(token)
			user = IppaUser.objects.get(player_id=player_id)
			user.is_email_verified = True
			user.save()
			self.response["res_str"] = "Email verification successfull."
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

class ResetPassword(View):

	def __init__(self):

		self.response = init_response()

	def dispatch(self, *args, **kwargs):

		return super(self.__class__, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):

		params = request.GET
		email_id = params.get("email_id")
		try:
			user = IppaUser.objects.get(email_id=email_id)
			token = create_auth_token(user.player_id)
			set_token(token, user.player_id)
			send_reset_password_link(RESET_PASSWORD_NOTI, token, user)
			self.response["res_str"] = "Reset password link sent to email id."
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

	def post(self, request, *args, **kwargs):
		params = request.POST
		try:
			password = params.get("password")
			repeat_password = params.get("repeat_password")
			if not password == repeat_password:
				raise Exception(PASSWORD_DIDNT_MATCH)
			validate_password(password)
			token = params.get("token")
			player_id = get_token(token)
			user = IppaUser.objects.get(player_id=player_id)
			password_hash = gen_password_hash(params.get("password"))
			user.password = password_hash
			user.save()
			self.response["res_str"] = "Successfully updated the password."
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

class UploadProfilePic(View):

	def __init__(self):

		self.response = init_response()

	def dispatch(self, *args, **kwargs):

		return super(self.__class__, self).dispatch(*args, **kwargs)

	@decorator_4xx([])
	def post(self, request, *args, **kwargs):

		player = request.user
		profile_pic = request.FILES.get("profile_pic")
		try:
			file_s3_url = copy_content_to_s3(profile_pic, "Profile_pic")
			player.profile_image = file_s3_url
			player.save()
			self.response["res_data"] = {"file_url":file_s3_url}
			self.response["res_str"] = "Profile Picture added successfully."
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

