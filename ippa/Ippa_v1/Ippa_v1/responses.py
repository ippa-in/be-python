from django.http.response import JsonResponse

def init_response(res_str=None, res_data=None):
	"""Initialize the resposne structure."""
	
	response = {
		"res_str":"", 
		"res_data":dict()
	}
	response["res_str"] = res_str if res_str else ""
	response["res_data"] = res_data if res_data else dict()
	return response

def _send(data, status_code):
	return JsonResponse(data=data, status=status_code)

def send_200(data):
	return _send(data, 200)

def send_201(data):
	return _send(data, 201)

def send_400(data):
	return _send(data, 400)