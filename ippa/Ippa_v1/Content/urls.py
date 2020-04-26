from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from Content.views import (GetNavigationBar, DashboardImage, UpdateDashboardImage,
							PreviewPoints, ManagePoints, PreviewRewards, ManageRewards,
							GetRewardsNetworks, RedeemReward, GetRewards, AdView)


urlpatterns = [
	url(r'^v1/navigation_bar/$', csrf_exempt(GetNavigationBar.as_view()), name="Content_navigation_bar"),
	url(r'^v1/dashboard_image/$', csrf_exempt(DashboardImage.as_view()), name="Content_dashboard_image"),
	url(r'^v1/update_dashboard_image/$', csrf_exempt(UpdateDashboardImage.as_view()), name="Content_update_dashboard_image"),
	url(r'^v1/preview_points/$', csrf_exempt(PreviewPoints.as_view()), name="Content_preview_points"),
	url(r'^v1/points/$', csrf_exempt(ManagePoints.as_view()), name="Content_points"),
	url(r'^v1/preview_rewards/$', csrf_exempt(PreviewRewards.as_view()), name="Content_preview_rewards"),
	url(r'^v1/rewards/$', csrf_exempt(ManageRewards.as_view()), name="Content_rewards"),
	url(r'^v1/get_rewards_network/$', csrf_exempt(GetRewardsNetworks.as_view()), name="Content_rewards_network"),
	url(r'^v1/get_rewards/$', csrf_exempt(GetRewards.as_view()), name="Content_reward"),
	url(r'^v1/redeem/$', csrf_exempt(RedeemReward.as_view()), name="Content_redeem_reward"),
	url(r'^v1/ads/$', csrf_exempt(AdView.as_view()), name="Content_ads"),


]