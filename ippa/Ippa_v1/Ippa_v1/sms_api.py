import requests
import base64
import json

def send_sms_uat():

	import pdb;pdb.set_trace()
	# request_url = "https://japi.instaalerts.zone/httpapi/JsonReceiver"
	request_url = "https://japi.instaalerts.zone/httpapi/QueryStringReceiver"

	# user_name = "PGENIE"
	AccessKey = "V8ESZuXyciS5lEWN3iXuTA=="
	# auth_value = base64.b64encode(user_name+":"+AccessKey)
	# headers = {
	# 	"Authorization":auth_value
	# }
	headers = dict()
	# data = {
	# 	"ver":"1.0",
	# 	"key":AccessKey,
	# 	"encrypt":0,
	# 	"messages":[
	# 	{
	# 		"dest":["8318629982"],
	# 		"text":["Hello this is for testing."],
	# 		"send":"Alerts",
	# 		"tag":"CAMPAIGN",
	# 		"tag1": "16",
	# 		"tag2": "1809",
	# 		"tag3": "1076",
	# 		"tag4": "1"
	# 	}
	# 	]
	# }
	# data = {
	# 	"ver":"1.0",
	# 	"key":AccessKey,
	# 	"encrypt":0,
	# 	"messages":[
	# 	{
	# 		"dest":["8318629982"],
	# 		"text":["Hello this is for testing."],
	# 		"send":"Alerts",
	# 		"tag":"CAMPAIGN",
	# 		"tag1": "16",
	# 		"tag2": "1809",
	# 		"tag3": "1076",
	# 		"tag4": "1",
	# 		"sch_at": "2020-06-20 14:57:00"
	# 	}
	# 	]
	# }
	# data = {
	# 	"ver":"1.0",
	# 	"key":AccessKey,
	# 	"encrypt":0,
	# 	"messages":[
	# 	{
	# 		"dest":["8318629982"],
	# 		"text":["23454 is your One Time Password for your Mobile No 8318629982"],
	# 		"send":"PGENIE",
	# 		"tag":"CAMPAIGN",
	# 		"tag1": "16",
	# 		"tag2": "1809",
	# 		"tag3": "1076",
	# 		"tag4": "1",
	# 	}
	# 	]
	# }
	data = {
		"ver":"1.0",
		"key":AccessKey,
		"dest":"+918318629982",
		"text":"324323is your One Time Password for your Mobile No8318629982",
		"send":"MPGNIE"
	}
	response = requests.get(request_url, data=data, headers=headers)
	print response.text

send_sms_uat()

