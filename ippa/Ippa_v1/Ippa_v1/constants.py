#############################AccessControl############################
EMAIL_REGEX = r"(^[a-zA-Z0-9\'_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
REGEX_PASSWORD_POLICY = r'^(?=\S*[A-Z])(?=\S*\d)(?=\S*[$@$!#%*?&])[A-Za-z\d$@$!#%*?&]{8,}'
MOBILE_REGEX = r"^[1-9]{1}[0-9]{9}$"

LOGIN_NOT_REQUIRED_CONTENT_TYPE = ["tournament_content", "dashboard_videos"]

