from django.db import transaction
from datetime import datetime

from Transaction.models import Transaction
from Network.models import PlayerTag
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
					err_msg = USER_NOT_TAGGED_STR.format(network_user_name, network_name)
					raise UserNotTagged(err_msg)

				taggeg_user = network_tagging_obj.user
				txn_date = datetime.strptime(txn.get("Date"), "%d-%m-%Y")
				txn_detail = {
					"txn_date":txn_date,
					"txn_type":Transaction.DEPOSIT,
					"amount":txn.get("Amount"),
					"user":taggeg_user,
					"network":network_tagging_obj.network,
					"is_bulk_creation":True
				}
				txn_obj = Transaction.objects.create_txn(**txn_detail)
				txn_obj_list.append(txn_obj)
				txn_count = txn_count + 1
				#update user points
				user_points = taggeg_user.points
				user_points["redeemable_points"] += int(txn.get("Amount"))
				taggeg_user.points = user_points
				taggeg_user.save()

				#initiate points notification
				month = txn_date.strftime("%B")
				update_point_notification_to_user(month, taggeg_user)
			Transaction.objects.bulk_create(txn_obj_list)
		return True, txn_count, ""
	except Exception as ex:
		raise TxnCreationFailed(str(ex))
