import re
import hashlib
import string
import random

from random import randint

from AccessControl.constants import *
from Ippa_v1.constants import REGEX_PASSWORD_POLICY, EMAIL_REGEX, MOBILE_REGEX
from Ippa_v1.redis_utils import set_token, set_token_exp
from Ippa_v1.server_config import HOST_FT_URL, HTTP_PROTOCOL

def valid_email_id(email_id):

	if re.match(EMAIL_REGEX, email_id):
		return True
	return False

def valid_mobile_no(mobile_number):
	if re.match(MOBILE_REGEX, mobile_number):
		return True
	return False

def validate_password(password):
	assert password.strip() != "", INVAILD_PASSWORD_STR

	if not re.match(REGEX_PASSWORD_POLICY, password):
		raise AssertionError(PWD_INVALID_ERR)

def gen_password_hash(password):
	return str(hashlib.sha256(password).hexdigest())

def _get_otp():
	return randint(100000, 999999)

def create_auth_token(player_id):

	chars = string.ascii_uppercase + string.digits
	random_string =  TOKEN_STR_FIRST + ''.join(random.choice(chars) for _ in range(12)) + TOKEN_STR_LAST
	return random_string

def authenticate_user(email_id, password):
	"""
	Authenticate User and return token and player id in response headers.
	"""
	from AccessControl.models import IppaUser

	code, res_str, response = "0", "", dict()

	assert password.strip() != "", INVAILD_PASSWORD_STR
	assert email_id.strip() != "", INVAILD_PASSWORD_STR

	user = IppaUser.objects.filter(email_id=email_id)

	if not user.exists():
		res_str = USER_PROFILE_DOES_NOT_EXISTS_STR
		return "1", res_str, {}
	user = user.first()
	# if not user.is_email_verified:
	# 	res_str = VERIFY_YOUR_EMAIL_ID
	# 	return "2", res_str, {}

	saved_password = gen_password_hash(password)
	if not saved_password == user.password:
		res_str = INVAILD_PASSWORD_STR
		return "3", res_str, {}
	else:
		token = create_auth_token(user.player_id)
		set_token_exp(token, user.player_id)
		response = {
			"token":token,
			"cid": user.player_id
		}
		res_str = LOGIN_SUCCESSFUL
	return code, res_str, response

def send_kyc_approved_email_to_user(user, to=[], cc=[]):
	from NotificationEngine.interface import initiate_notification

	notification_obj = {
		"identifier_dict":{
			"user_name":user.name
		},
		"to":[user.email_id]
	}

	try:
		initiate_notification(KYC_DETAILS_APPROVED, notification_obj)
	except Exception as ex:
		pass

def send_kyc_declined_email_to_user(user, comments, to=[], cc=[]):
	from NotificationEngine.interface import initiate_notification

	notification_obj = {
		"identifier_dict":{
			"user_name":user.name,
			"comments":comments
		},
		"to":[user.email_id]
	}

	try:
		initiate_notification(KYC_DETAILS_DECLINED, notification_obj)
	except Exception as ex:
		pass

def send_email_verification_link(notification_key, token, user, to=[], cc=[]):
	from NotificationEngine.interface import initiate_notification

	link = HTTP_PROTOCOL + HOST_FT_URL + "/profile?token=" + token 
	notification_obj = {
		"identifier_dict":{
			"user_name":user.name,
			"link":link
		},
		"to":[user.email_id]
	}

	try:
		initiate_notification(notification_key, notification_obj)
	except Exception as ex:
		pass

def send_kyc_document_upload_link(user, to=[], cc=[]):
	from NotificationEngine.interface import initiate_notification

	notification_obj = {
		"identifier_dict":{
			"user_name":user.name
		},
		"to":[user.email_id]
	}

	try:
		initiate_notification(KYC_UPLOAD_NOTI, notification_obj)
	except Exception as ex:
		pass

def send_reset_password_link(notification_key, token, user, to=[], cc=[]):
	from NotificationEngine.interface import initiate_notification

	link = HTTP_PROTOCOL + HOST_FT_URL + "/frgt-pass/?q=" + token 
	notification_obj = {
		"identifier_dict":{
			"user_name":user.name,
			"link":link
		},
		"to":[user.email_id]
	}

	try:
		initiate_notification(notification_key, notification_obj)
	except Exception as ex:
		pass





