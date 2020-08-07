import requests

from Ippa_v1.server_config import KARIX_BASE_URL, KARIX_ACCESS_KEY, SENDER_ID
from Ippa_v1.err_logger import EMERGENCY, INFO, DEBUG, log_error, ALERT

class SMSProvider(object):

	def __init__(self, mobile_number, otp):

		self.otp = otp
		self.mobile_number = mobile_number
		self.request_url = "https://" + KARIX_BASE_URL

	def _prepare_req_data(self):

		data = {
			"ver":"1.0",
			"key":KARIX_ACCESS_KEY,
			"dest":self.mobile_number,
			"text":str(self.otp) + "is your One Time Password for your Mobile No"+self.mobile_number,
			"send":SENDER_ID
		}
		return data

	def _send_sms(self):
		
		data = self._prepare_req_data()
		response = requests.get(self.request_url, data=data, headers=dict())
		log_error(INFO, "SMS RESPONSE LOGS", "", message=response.text)


