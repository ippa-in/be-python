from NotificationEngine.interface import initiate_notification

def send_take_action_email_to_admin(notification_key, txn_obj, user, to=[], cc=[]):

	notification_obj = {
		"identifier_dict":{
			"txn_id":txn_obj.txn_id,
			"user_name":user.name,
			"link":""
		},
		"to":[user.email_id]
	}

	try:
		initiate_notification(notification_key, notification_obj)
	except Exception as ex:
		pass

def send_txn_info_email_to_user(notification_key, txn_obj, user, to=[], cc=[]):

	notification_obj = {
		"identifier_dict":{
			"txn_id":txn_obj.txn_id
		},
		"to":[user.email_id]
	}

	try:
		initiate_notification(notification_key, notification_obj)
	except Exception as ex:
		pass