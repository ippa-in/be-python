from functools import wraps

from django.http import HttpResponseBadRequest, HttpResponse
from django.utils.decorators import available_attrs
from django.http import QueryDict

from AccessControl.models import IppaUser

class decorator_4xx(object):

	"""
	1. It will check for all mandatory fields.
	2. Add user in request
	3. Validate token.
	"""

	def __init__(self, mand_params):
		self.mand_params = mand_params

	def _get_all_params(self, request):

		params_dict = dict()
		if request.method == "GET":
			params_dict = request.GET
		elif request.method == "POST":
			params_dict = request.POST
		elif request.method == "PUT":
			params_dict = QueryDict(request.body)
		return params_dict

	def __call__(self, func, *args, **kwargs):

		@wraps(func, assigned=available_attrs(func))
		def inner(*args, **kwargs):

			request = args[1]
			params = self._get_all_params(request)
			request.params_dict = params
			#check for mandatory params.
			params_list = params.keys()
			missing_params = [params for params in self.mand_params if params not in params_list]
			if missing_params:
				msg_str = ', '.join(missing_params) + " are mandatory parameters."
				return HttpResponseBadRequest(msg_str)

			#validate token if valid add user to request object(todo)
			player_id = request.META.get("HTTP_PLAYER_ID")
			try:
				user = IppaUser.objects.get(player_id=player_id, is_deleted=0)
			except IppaUser.DoesNotExist:
				return HttpResponse("Invalid User", status=401)

			request.user = user

			return func(*args, **kwargs)
		return inner
