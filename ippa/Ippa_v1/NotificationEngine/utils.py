import pytz
from datetime import datetime

def get_time_diff(created_on):
	notification_creation_date = created_on
	today_date = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
	time_diff = today_date - notification_creation_date
	seconds = time_diff.seconds
	minutes = seconds/60
	days = minutes/1440
	months = days/30
	year = months/12

	if year:
		return str(year) + " years"
	if months:
		return str(months) + " months"
	if days:
		return str(days) + " days"
	if minutes:
		return str(minutes) + " minutes"
	if seconds:
		return str(seconds) + " seconds"