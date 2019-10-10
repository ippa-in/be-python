#Add search configurations
from Filter.models import SearchConfiguration
from django.contrib.contenttypes.models import ContentType


display_name = "transaction_filter"
app_label = "Transaction"
model = "transaction"

ct = ContentType.objects.get(app_label=app_label, model=model)
sc = SearchConfiguration.objects.create(display_name=display_name, content_type=ct)
print sc

#Add Search fields
from Filter.models import SearchField

search_field_detail = {
	"search_config_id":1,
	"display_name":"user",
	"field_name":"transaction__user",
	"status":True,
	"is_user_filter":True
}

sf = SearchField.objects.create(**search_field_detail)
print sf