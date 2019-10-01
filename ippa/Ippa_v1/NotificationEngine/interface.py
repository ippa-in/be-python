from NotificationEngine.models import Notification

def initiate_notification(notification_key, notification_obj):

	try:
		Notification.objects.send_notification(notification_key, notification_obj)
	except Exception as ex:
		pass

