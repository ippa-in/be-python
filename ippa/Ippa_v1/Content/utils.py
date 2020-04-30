import os
import csv
import pandas as pd

from NotificationEngine.interface import initiate_notification

def read_excel_file(file):

	"""
	File format should be below.
	col1	col2	col3
	1		2		3
	4		5		6
	"""

	#save file locally.
	with open('temp_file.xlsx', 'w') as f:
		f.write(file.read())

	#read from temp file.
	data_frame = pd.read_excel('temp_file.xlsx')
	data_dict = data_frame.to_dict('records')
	os.remove('temp_file.xlsx')
	return data_dict

def read_csv_file(file):

	"""
	File format should be below.
	col1,col2,col3
	1,2,3
	4,5,6
	"""

	points_data = list()
	#read from temp file.
	with open('temp_file.txt', 'w') as f:
		f.write(file.read())
	with open('temp_file.txt') as f:
		data_dict = csv.DictReader(f, delimiter=',')
		for data in data_dict:
			points_data.append(data)
	os.remove('temp_file.txt')
	return points_data


def send_offer_redeemed_email_to_admin(notification_key, reward, user, to=[], cc=[]):

	notification_obj = {
		"identifier_dict":{
			"network_name":reward.network.name,
			"title":reward.title,
			"points":reward.goal_points
		},
		"to":["noreply@ippa.in"]
	}

	try:
		initiate_notification(notification_key, notification_obj)
	except Exception as ex:
		pass

def send_offer_redeemed_email_to_user(notification_key, reward, user, to=[], cc=[]):

	notification_obj = {
		"identifier_dict":{
			"user_name":user.user_name,
			"title":reward.title,
			"link":""
		},
		"to":[user.email_id]
	}

	try:
		initiate_notification(notification_key, notification_obj)
	except Exception as ex:
		pass
		




