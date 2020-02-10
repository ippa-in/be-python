# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View

from Ippa_v1.decorators import decorator_4xx, decorator_4xx_admin
from Ippa_v1.responses import *
from Ippa_v1.utils import generate_unique_id, copy_content_to_s3, get_content_from_s3
from AccessControl.constants import STR_ACTION_NOT_ALLOWED
from AccessControl.exceptions import ACTION_NOT_ALLOWED
from Content.models import *
from Content.utils import read_excel_file, read_csv_file
from Content.constants import *
from Transaction.interface import bulk_txn_create

# Create your views here.
class DashboardImage(View):

	def __init__(self):
		self.response = init_response()

	def dispatch(self, *args, **kwargs):
		return super(self.__class__, self).dispatch(*args, **kwargs)

	@decorator_4xx_admin([])
	def post(self, request, *args, **kwargs):

		user = request.user
		db_img = request.FILES.get("file")
		title = request.POST.get("title", "")
		description = request.POST.get("desc", "")

		try:
			file_name = generate_unique_id("DIMG")
			file_s3_url = copy_content_to_s3(db_img, "DIMG/"+file_name)
			image = DashBoardImage.objects.add_dashboard_image(title=title,
									description=description, img_url=file_s3_url)
			self.response["res_str"] = "Dashboard Image Added Successfully."
			self.response["res_data"] = {"img_id":image.pk}
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

	@decorator_4xx_admin([])
	def get(self, request, *args, **kwargs):

		try:
			dashboard_images = DashBoardImage.objects.filter(is_deleted=0).order_by('order')
			db_images = list()
			for images in dashboard_images:
				db_images.append(images.serializer())
			self.response["res_str"] = "Images fetched Successfully."
			self.response["res_data"] = db_images
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)

	@decorator_4xx_admin([])
	def put(self, request, *args, **kwargs):
		"""Todo: Test for image order swapping."""

		data = request.params_dict
		action = data.get("action")
		try:
			if action == "delete":
				image = DashBoardImage.objects.filter(pk=data.get("img_id1"))
				image.update(is_deleted=1)
			elif action == "swap":
				img_obj1 = DashBoardImage.objects.filter(pk=data.get("img_id1"))
				img_obj2 = DashBoardImage.objects.filter(pk=data.get("img_id2"))
				img1_order = img_obj1[0].order
				img_obj1.update(order=img_obj2[0].order)
				img_obj2.update(order=img1_order)
			self.response["res_str"] = "Image updated Successfully."
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)

class UpdateDashboardImage(View):

	def __init__(self):
		self.response = init_response()

	def dispatch(self, *args, **kwargs):
		return super(self.__class__, self).dispatch(*args, **kwargs)

	@decorator_4xx_admin([])
	def post(self, request, *args, **kwargs):

		user = request.user
		data = request.params_dict
		db_img = request.FILES.get("file", "")
		title = data.get("title", "")
		description = data.get("desc", "")
		file_s3_url = ""
		try:
			image = DashBoardImage.objects.get(pk=data.get("img_id"))
			if db_img:
				file_name = generate_unique_id("DIMG")
				file_s3_url = copy_content_to_s3(db_img, "DIMG/"+file_name)
			image.update_dashboard_image(title=title, description=description, 
												img_url=file_s3_url)
			self.response["res_str"] = "Dashboard Image Updated Successfully."
			self.response["res_data"] = image.serializer()
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

class PreviewPoints(View):

	def __init__(self):
		self.response = init_response()

	def dispatch(self, *args, **kwargs):
		return super(self.__class__, self).dispatch(*args, **kwargs)

	@decorator_4xx_admin([])
	def post(self, request, *args, **kwargs):

		user = request.user
		points_file = request.FILES.get("file", "")
		title = request.POST.get("title", "")
		
		try:
			data_dict = dict()
			data_dict["title"] = title
			if ".xlsx" in title:
				data_dict["data"] = read_excel_file(points_file)
			elif ".csv" in title:
				data_dict["data"] = read_csv_file(points_file)
			self.response["res_str"] = "Points fetched successfully."
			self.response["res_data"] = data_dict
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

class ManagePoints(View):

	def __init__(self):
		self.response = init_response()

	def dispatch(self, *args, **kwargs):
		return super(self.__class__, self).dispatch(*args, **kwargs)

	@decorator_4xx_admin([])
	def post(self, request, *args, **kwargs):

		"""
		ToDo: If two times click submit transaction should be created only once.
		"""
		user = request.user
		points_file = request.FILES.get("file", "")
		title = request.POST.get("title", "")
		
		try:
			if ".xlsx" in title:
				txn_data = read_excel_file(points_file)
			elif ".csv" in title:
				txn_data = read_csv_file(points_file)

			bulk_txn_created, no_of_rows, err_msg = bulk_txn_create(txn_data)

			#Upload file to s3
			points_file.seek(0)			#after reading file need to set file pointer at starting of file.
			file_name = generate_unique_id("POIXL")
			file_s3_url = copy_content_to_s3(points_file, "POINTS_FILE/"+file_name)

			#Save file URL
			file = Points.objects.add_excel(title=title, 
											no_of_rows=no_of_rows,
											file_url=file_s3_url)

			self.response["res_str"] = "Transactions created Successfully."
			self.response["res_data"] = {"file_id":file.pk}
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

	@decorator_4xx_admin([])
	def get(self, request, *args, **kwargs):

		"""
		if excel id comes return detail of excel else return all data.
		"""

		data = request.params_dict
		try:
			points_file_id = data.get("point_file_id", "")
			if points_file_id:
				file = Points.objects.get(pk=points_file_id)
				title = file.title
				s3_url = file.file_url

				s3_url_list = s3_url.split("/")
				file_key = s3_url_list[-2] + "/" + s3_url_list[-1]

				point_file = get_content_from_s3(file_key)
				file_content = point_file.get("Body")
				if ".xlsx" in title:
					file_data = read_excel_file(file_content)
				elif ".csv" in title:
					file_data = read_csv_file(file_content)
			else:
				files = Points.objects.all().order_by('-created_on')
				file_data = list()
				for file in files:
					file_data.append(file.serialize())

			self.response["res_str"] = "Points details fetch successfully."
			self.response["res_data"] = file_data
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

class GetNavigationBar(View):

	def __init__(self):
		self.response = init_response()

	def dispatch(self, *args, **kwargs):
		return super(self.__class__, self).dispatch(*args, **kwargs)

	@decorator_4xx_admin([])
	def get(self, request, *args, **kwargs):

		try:
			self.response["res_data"] = NAVIGATION_BAR
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)
