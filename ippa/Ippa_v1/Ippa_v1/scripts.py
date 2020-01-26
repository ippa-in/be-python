#Add search configurations
from Filter.models import SearchConfiguration
from django.contrib.contenttypes.models import ContentType


display_name = "transaction_content"
app_label = "Transaction"
model = "transaction"

ct = ContentType.objects.get(app_label=app_label, model=model)
sc = SearchConfiguration.objects.create(display_name=display_name, content_type=ct)
print sc

#Add Search fields
from Filter.models import SearchField

# #version 1
# search_field_detail = {
# 	"search_config_id":11,
# 	"display_name":"Date",
# 	"field_name":"txn_date",
# 	"status":True,
# 	"is_user_filter":False
# }

#version 2
search_field_detail = {
	"search_config_id":11,
	"display_name":"Date",
	"field_name":"txn_date",
	"status":True,
	"is_user_filter":False,
	"filter_type":"date",
	"order":3
}

sf = SearchField.objects.create(**search_field_detail)
print sf

#Add Bank
from Transaction.models import Bank

data = {
	"name":"YES"
}
bank_obj = Bank.objects.create_bank(data)
print bank_obj

#Add new notification key and mail
from Ippa_v1.utils import generate_unique_id
from NotificationEngine.models import *

subject = "Reset passwork IPPA."
notification_name = "reset_password_notification"
mail_id  = generate_unique_id("MAIL")
mail_obj = Mail.objects.create(mail_id=mail_id, subject=subject, mail_body="")

noti_id  = generate_unique_id("NOTI")
noti_obj = Notification.objects.create(notification_id=noti_id, mail_id=mail_id, notification_name=notification_name)