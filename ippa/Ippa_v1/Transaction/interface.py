from django.db import transaction
from datetime import datetime

from Transaction.models import Transaction
from Network.models import PlayerTag, NetworkPoints
from Transaction.exceptions import UserNotTagged, TxnCreationFailed
from Transaction.constants import USER_NOT_TAGGED_STR
from Transaction.utils import *

def bulk_txn_create(txn_data):

	"""
	Assumptions: 
	1. All transaction will be deposit.
	2. Currently network to ippa points conversion rate is 1.
	3. In future it's need to be handled.
	"""
	txn_obj_list = list()
	txn_count = 0
	try:
		with transaction.atomic():
			for txn in txn_data:
				network_name = txn.get("Network")
				network_user_name = txn.get("UserName")
				network_tagging_obj = PlayerTag.objects.filter(network__name=network_name,
														tag_user_name=network_user_name,
														is_deleted=False).first()

				if not network_tagging_obj:
					continue
					# err_msg = USER_NOT_TAGGED_STR.format(network_user_name, network_name)
					# raise UserNotTagged(err_msg)

				network_obj = network_tagging_obj.network
				conversion_exp = network_obj.net_to_ippa_exp
				network_points = txn.get("Amount")
				ippa_points = int(round(float(network_points)*eval(conversion_exp)))
				tagged_user = network_tagging_obj.user
				txn_date = datetime.strptime(txn.get("Date"), "%d-%m-%Y")
				txn_detail = {
					"txn_date":txn_date,
					"txn_type":Transaction.DEPOSIT,
					"amount":network_points,
					"user":tagged_user,
					"network":network_obj,
					"is_bulk_creation":True
				}
				txn_obj = Transaction.objects.create_txn(**txn_detail)
				txn_obj_list.append(txn_obj)
				txn_count = txn_count + 1

				#update user points

				user_points = tagged_user.points
				user_points["current_month_points"] += ippa_points
				user_points["total_points"] += ippa_points
				tagged_user.points = user_points
				tagged_user.save()

				#add network specific points
				NetworkPoints.objects.create_txn(user=tagged_user, 
								network=network_obj,
								points=network_points,
								txn_type=NetworkPoints.DEPOSIT)

				#initiate points notification
				month = txn_date.strftime("%B")
				update_point_notification_to_user(month, tagged_user)
			Transaction.objects.bulk_create(txn_obj_list)
		return True, txn_count, ""
	except Exception as ex:
		raise TxnCreationFailed(str(ex))
