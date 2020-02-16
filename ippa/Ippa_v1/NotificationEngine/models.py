# -*- coding: utf-8 -*-
import pytz

from django.db import models
from datetime import datetime
from django.template import Template, Context
from django.core.mail import EmailMultiAlternatives

from .constants import *
from .utils import get_time_diff

# Create your models here.

class BaseModel(models.Model):

	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	is_deleted = models.BooleanField(default=False)

	class Meta:
		abstract = True

class MailManager(models.Manager):

	def send_mail(self, subject, mail_body, from_email, to, cc=[], bcc=[], attachments=[]):
		msg = EmailMultiAlternatives(subject, mail_body, from_email, to, cc, bcc, attachments)
		msg.attach_alternative(mail_body, "text/html")
		msg.send()

class Mail(BaseModel):

	mail_id = models.CharField(max_length=255, primary_key=True)
	subject = models.TextField("Use same variable name in html template and in identifier_dict.")
	mail_body = models.TextField("Use same variable name in html template and in identifier_dict.")
	from_email = models.CharField(max_length=255, default=ADMIN_EMAIL)
	to_emails = models.TextField(null=True, blank=True)
	cc_emails = models.TextField(null=True, blank=True)
	bcc_emails = models.TextField(null=True, blank=True)

	objects = MailManager()

	def __unicode__(self):
		return self.mail_id

class NotificationManager(models.Manager):

	def _render_template(self, mail_content, identifier_dict):

		html_content = Template(mail_content)
		values = Context(identifier_dict, autoescape=False)
		template_content = html_content.render(values)
		return template_content

	def send_notification(self, notification_key, notification_obj):

		notify_obj = Notification.objects.select_related('mail').\
										get(notification_name=notification_key, 
											status="Active")
		mail_obj = notify_obj.mail
		subject_content = mail_obj.subject
		message_content = mail_obj.mail_body
		from_mail = mail_obj.from_email
		to = notification_obj.get("to", [])
		cc = notification_obj.get("cc", [])
		bcc = notification_obj.get("bcc", [])
		attachments = notification_obj.get("attachments", [])
		identifier_dict = notification_obj.get("identifier_dict", {})
		subject = self._render_template(subject_content, identifier_dict)
		mail_body = self._render_template(message_content, identifier_dict)
		Mail.objects.send_mail(subject, mail_body, from_mail, to, cc, bcc, attachments)


class Notification(BaseModel):

	ACTIVE = "Active"
	DELEATED = "Deleated"

	status_choices = ((ACTIVE, "Active"),
						(DELEATED, "Deleated"))
	notification_id = models.CharField(max_length=255, primary_key=True)
	notification_name = models.CharField(max_length=255)
	mail = models.ForeignKey(Mail)
	status = models.CharField(max_length=255, default=ACTIVE, choices=status_choices)

	objects = NotificationManager()

	def __unicode__(self):
		return self.notification_id + " " + self.notification_name

class NotificationMessageManager(models.Manager):

	def add_notification_str(self, notification_str):

		NotificationMessage.objects.create(notification_str=notification_str)

class NotificationMessage(BaseModel):

	notification_str = models.CharField(max_length=255)
	has_read = models.BooleanField(default=False)

	objects = NotificationMessageManager()

	def __unicode__(self):
		return str(self.pk)

	def serialize(self):

		notification_dict = {
			"notification_id":self.pk,
			"notification_str":self.notification_str,
			"time":get_time_diff(self.created_on)
		}
		return 	notification_dict




