# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View

from Ippa_v1.decorators import decorator_4xx, decorator_4xx_admin
from Ippa_v1.responses import *
from Ippa_v1.utils import generate_unique_id, copy_content_to_s3, get_content_from_s3
from Ippa_v1.redis_utils import is_token_exists
from AccessControl.models import IppaUser
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


class PreviewRewards(View):

	def __init__(self):
		self.response = init_response()

	def dispatch(self, *args, **kwargs):
		return super(self.__class__, self).dispatch(*args, **kwargs)

	@decorator_4xx_admin([])
	def post(self, request, *args, **kwargs):

		user = request.user
		rewards_file = request.FILES.get("file", "")
		title = request.POST.get("title", "")
		
		try:
			data_dict = dict()
			data_dict["title"] = title
			if ".xlsx" in title:
				data_dict["data"] = read_excel_file(rewards_file)
			elif ".csv" in title:
				data_dict["data"] = read_csv_file(rewards_file)
			self.response["res_str"] = "Rewards fetched successfully."
			self.response["res_data"] = data_dict
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

class ManageRewards(View):

	def __init__(self):
		self.response = init_response()

	def dispatch(self, *args, **kwargs):
		return super(self.__class__, self).dispatch(*args, **kwargs)

	@decorator_4xx_admin([])
	def post(self, request, *args, **kwargs):

		"""
		ToDo: Create Rewards
		"""
		user = request.user
		rewards_file = request.FILES.get("file", "")
		title = request.POST.get("title", "")
		try:
			if ".xlsx" in title:
				reward_data = read_excel_file(rewards_file)
			elif ".csv" in title:
				reward_data = read_csv_file(rewards_file)

			reward_obj_list = list()
			for reward in reward_data:

				network = Network.objects.get(name=reward.get("network_name"))
				reward_detail = {
					"title":reward.get("title", ""),
					"description":reward.get("description", ""),
					"from_date":datetime.strptime(reward.get("from_date", ""), "%d-%m-%Y"),
					"to_date":datetime.strptime(reward.get("to_date", ""), "%d-%m-%Y"),
					"deactivate_date":datetime.strptime(reward.get("deactivate_date", ""), "%d-%m-%Y"),
					"status":Rewards.ACTIVE,
					"network":network,
					"point_name":reward.get("point_name", ""),
					"goal_points":reward.get("goal_points", ""),
					"more_info_link":reward.get("more_info_link", ""),
				}
				reward_obj = Rewards(**reward_detail)
				reward_obj_list.append(reward_obj)
			Rewards.objects.bulk_create(reward_obj_list)

			self.response["res_str"] = "Rewards added Successfully."
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

	@decorator_4xx_admin([])
	def get(self, request, *args, **kwargs):

		"""
		return details of reward.
		"""

		data = request.params_dict
		try:
			reward_id = data.get("reward_id", "")
			reward_obj = Rewards.objects.get(pk=reward_id)
			self.response["res_str"] = "Rewards details fetch successfully."
			self.response["res_data"] = reward_obj.serialize()
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

class GetRewards(View):

	def __init__(self):
		self.response = init_response()

	def dispatch(self, *args, **kwargs):
		return super(self.__class__, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):

		"""
		return details of reward group as filter wise.
		"""
		data = request.GET
		network_id = data.get("network_id")
		try:
			rewards = Rewards.objects.filter(
						status__in=[Rewards.ACTIVE, Rewards.EXPIRED], 
						network__network_id=network_id)
			reward_details =  Rewards.objects.bulk_serializer(rewards)
			self.response["res_str"] = "Rewards details fetch successfully."
			self.response["res_data"] = reward_details
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

class GetRewardsNetworks(View):

	def __init__(self):
		self.response = init_response()

	def dispatch(self, *args, **kwargs):
		return super(self.__class__, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):

		"""
		return details of reward network
		"""

		is_logged_in = False
		user_points = dict()
		reward_data = dict()
		login_token = request.META.get("HTTP_PLAYER_TOKEN")
		if login_token and is_token_exists(login_token):
			is_logged_in = True
			player_id = request.META.get("HTTP_PLAYER_ID")
			user = IppaUser.objects.get(player_id=player_id)
			user_points = user.points

		reward_data["is_logged_in"] = is_logged_in
		reward_data["user_points"] = user_points
		reward_data["reward_networks"] = list()
		try:
			reward_networks = Rewards.objects.filter(
						status__in=[Rewards.ACTIVE, Rewards.EXPIRED])\
						.values_list('network__network_id', flat=True)
			network_list = list(set(reward_networks))

			network_objs = Network.objects.filter(network_id__in=reward_networks)
			order_no = 2
			for network in network_objs:
				network_detail = network.serialize()
				if network_detail.get("name") == "IPPA":
					network_detail["order"] = 1
				else:
					network_detail["order"] = order_no
					order_no = order_no + 1
				reward_data["reward_networks"].append(network_detail)

			self.response["res_str"] = "Rewards Networks details fetch successfully."
			self.response["res_data"] = reward_data
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

class RedeemReward(View):

	def __init__(self):
		self.response = init_response()

	def dispatch(self, *args, **kwargs):
		return super(self.__class__, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):

		"""
		Deduct point and redeem reward.
		"""
		try:
			self.response["res_str"] = "Reward redeemed  Successfully."
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

# Create your views here.
class AdView(View):

	def __init__(self):
		self.response = init_response()

	def dispatch(self, *args, **kwargs):
		return super(self.__class__, self).dispatch(*args, **kwargs)

	@decorator_4xx_admin([])
	def post(self, request, *args, **kwargs):

		user = request.user
		ad_img = request.FILES.get("file")
		redirect_url = request.POST.get("redirect_url", "")

		try:
			file_name = generate_unique_id("AD")
			file_s3_url = copy_content_to_s3(ad_img, "AD/"+file_name)
			ad_obj = Ad.objects.add_ad(redirect_url=redirect_url, img_url=file_s3_url)
			self.response["res_str"] = "Ad Added Successfully."
			self.response["res_data"] = {"ad_id":ad_obj.pk}
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)
			return send_400(self.response)

	@decorator_4xx_admin([])
	def get(self, request, *args, **kwargs):

		try:
			ad_list = Ad.objects.filter(is_deleted=0).order_by('order')
			ad_details = list()
			for ad in ad_list:
				ad_details.append(ad.serializer())
			self.response["res_str"] = "Ad fetched Successfully."
			self.response["res_data"] = ad_details
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
				ad_obj = Ad.objects.filter(pk=data.get("ad_id1"))
				ad_obj.update(is_deleted=1)
			elif action == "swap":
				ad_obj1 = Ad.objects.filter(pk=data.get("ad_id1"))
				ad_obj2 = Ad.objects.filter(pk=data.get("ad_id2"))
				ad1_order = ad_obj1[0].order
				ad_obj1.update(order=ad_obj2[0].order)
				ad_obj2.update(order=ad1_order)
			self.response["res_str"] = "Ad updated Successfully."
			return send_200(self.response)
		except Exception as ex:
			self.response["res_str"] = str(ex)


