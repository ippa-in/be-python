from NotificationEngine.interface import initiate_notification

def send_take_action_on_txn_email_to_admin(notification_key, txn_obj, user, to=[], cc=[]):

	notification_obj = {
		"identifier_dict":{
			"txn_id":txn_obj.txn_id,
			"user_name":user.name,
			"link":""
		},
		"to":["sandeepks.6198@gmail.com"]
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

def send_bank_acc_add_mail_to_admin(notification_key, bank_acc_obj, user, to=[], cc=[]):

	notification_obj = {
		"identifier_dict":{
			"bank_acc_name":bank_acc_obj.acc_name,
			"user_name":user.name,
			"link":""
		},
		"to":["sandeepks.6198@gmail.com"],
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