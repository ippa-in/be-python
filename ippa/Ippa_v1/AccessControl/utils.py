import re
import hashlib
import string
import random

from AccessControl.constants import *
from Ippa_v1.constants import REGEX_PASSWORD_POLICY, EMAIL_REGEX

def valid_email_id(email_id):

	if re.match(EMAIL_REGEX, email_id):
		return True
	return False

def validate_password(password):
	assert password.strip() != "", INVAILD_PASSWORD_STR

	if not re.match(REGEX_PASSWORD_POLICY, password):
		raise AssertionError(PWD_INVALID_ERR)

def gen_password_hash(password):
	return str(hashlib.sha256(password).hexdigest())

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
	if not user.is_email_verified:
		res_str = VERIFY_YOUR_EMAIL_ID
		return "2", res_str, {}

	saved_password = gen_password_hash(password)
	if not saved_password == user.password:
		res_str = INVAILD_PASSWORD_STR
		return "3", res_str, {}
	else:
		token = create_auth_token(user.player_id)
		response = {
			"token":token,
			"cid": user.player_id
		}
		res_str = LOGIN_SUCCESSFUL
	return code, res_str, response

def send_kyc_verified_email_to_user(notification_key, doc_type, action, user, to=[], cc=[]):
	from NotificationEngine.interface import initiate_notification

	notification_obj = {
		"identifier_dict":{
			"user_name":user.name,
			"action":action,
			"doc_type":doc_type
		},
		"to":[user.email_id]
	}

	try:
		initiate_notification(notification_key, notification_obj)
	except Exception as ex:
		pass







