#Add search configurations
from Filter.models import SearchConfiguration
from django.contrib.contenttypes.models import ContentType


display_name = "tournament_content"
app_label = "Content"
model = "tournaments"

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
# search_field_detail = {
# 	"search_config_id":15,
# 	"display_name":"Network",
# 	"field_name":"network__name",
# 	"status":True,
# 	"is_user_filter":False,
# 	"filter_type":"dropdown",
# 	"order":2,
# 	"is_sortable":False
# }

#version 3
from Filter.models import SearchField

search_field_detail = {
	"search_config_id":17,
	"display_name":"buy_in_sort",
	"field_name":"buy_in",
	"status":True,
	"is_user_filter":False,
	"is_sortable":True
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

subject = "Offer Redeemed."
notification_name = "offer_redeemed_notification_user"
mail_id  = generate_unique_id("MAIL")
mail_obj = Mail.objects.create(mail_id=mail_id, subject=subject, mail_body="")

noti_id  = generate_unique_id("NOTI")
noti_obj = Notification.objects.create(notification_id=noti_id, mail_id=mail_id, notification_name=notification_name)


#Call mail
def call_mail():
	from NotificationEngine.models import *
	import pdb;pdb.set_trace()
	notification_key = "email_verfication_notification"
	notification_obj = {
		"identifier_dict":{
			"user_name":"testin",
			"link":""
		},
		"to":["sandeepks.6198@gmail.com"]
	}
	not_sent = Notification.objects.send_notification(notification_key, notification_obj)

call_mail()


