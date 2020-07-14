from NotificationEngine.interface import initiate_notification
from Ippa_v1.utils import convert_datetime_to_string
from Ippa_v1.server_config import ADMIN_TO_EMAIL
from Transaction.constants import *


def send_take_action_on_txn_email_to_admin(notification_key, txn_obj, user, to=[], cc=[]):

	notification_obj = {
		"identifier_dict":{
			"txn_id":txn_obj.txn_id,
			"user_name":user.name,
			"link":""
		},
		"to":[ADMIN_TO_EMAIL]
	}

	try:
		initiate_notification(notification_key, notification_obj)
	except Exception as ex:
		pass

def send_txn_info_email_to_user(notification_key, txn_obj, user, to=[], cc=[]):

	notification_obj = {
		"identifier_dict":{
			"txn_id":txn_obj.txn_id,
			"date":convert_datetime_to_string(txn_obj.txn_date,  "%d-%m-%Y"),
			"time":convert_datetime_to_string(txn_obj.txn_date,  "%H:%M %p"),
			"amount":txn_obj.amount
		},
		"to":[user.email_id]
	}

	try:
		initiate_notification(notification_key, notification_obj)
	except Exception as ex:
		pass

def send_bank_acc_add_mail_to_admin(notification_key, bank_acc_obj, user, to=[], cc=[]):

	notification_obj = {
		"identifier_dict":{
			"bank_acc_name":bank_acc_obj.acc_name,
			"user_name":user.name,
			"link":""
		},
		"to":[ADMIN_TO_EMAIL],
	}

	try:
		initiate_notification(notification_key, notification_obj)
	except Exception as ex:
		pass

def send_bank_acc_add_mail_to_user(notification_key, bank_acc_obj, user, to=[], cc=[]):

	notification_obj = {
		"identifier_dict":{
			"bank_acc_name":bank_acc_obj.acc_name
		},
		"to":[user.email_id]
	}

	try:
		initiate_notification(notification_key, notification_obj)
	except Exception as ex:
		pass


def bank_acc_action_taken_mail_to_user(notification_key, action, bank_acc_obj, user, to=[], cc=[]):

	notification_obj = {
		"identifier_dict":{
			"bank_acc_name":bank_acc_obj.acc_name,
			"user_name":user.name,
			"action":action
		},
		"to":[user.email_id]
	}

	try:
		initiate_notification(notification_key, notification_obj)
	except Exception as ex:
		pass

def txn_action_taken_mail_to_user(notification_key, action, txn_obj, user, to=[], cc=[]):

	notification_obj = {
		"identifier_dict":{
			"txn_id":txn_obj.txn_id,
			"user_name":user.name,
			"action":action
		},
		"to":[user.email_id]
	}

	try:
		initiate_notification(notification_key, notification_obj)
	except Exception as ex:
		pass

def txn_approved_notification_to_user(txn_obj, user, to=[], cc=[]):

	notification_obj = {
		"identifier_dict":{
			"amount":txn_obj.amount,
			"user_name":user.name
		},
		"to":[user.email_id]
	}

	try:
		initiate_notification(WITHDRAWL_REQUEST_APPROVED, notification_obj)
	except Exception as ex:
		pass

def txn_declined_notification_to_user(txn_obj, user, comments, to=[], cc=[]):

	notification_obj = {
		"identifier_dict":{
			"amount":txn_obj.amount,
			"user_name":user.name,
			"comments":comments
		},
		"to":[user.email_id]
	}

	try:
		initiate_notification(WITHDRAWL_REQUEST_DECLINED, notification_obj)
	except Exception as ex:
		pass
def update_point_notification_to_user(month, user, to=[], cc=[]):
	link = ""
	notification_obj = {
		"identifier_dict":{
			"month":month,
			"user_name":user.name,
			"link":link
		},
		"to":[user.email_id]
	}

	try:
		initiate_notification(POINT_UPDATED_NOTIFICATION, notification_obj)
	except Exception as ex:
		pass

