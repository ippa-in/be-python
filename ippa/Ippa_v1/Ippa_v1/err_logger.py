import json
import socket
import logging

from django.core.mail import send_mail

from .server_config import ERROR_LOG_FILE

# create logger
logger = logging.getLogger('ippa')
logger.setLevel(logging.ERROR)

# create console handler and set level to error
ch = logging.FileHandler(ERROR_LOG_FILE)
ch.setLevel(logging.ERROR)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -  %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


# EMERGENCY - Any error that is forcing a shutdown of the service or application to
# prevent data loss (or further data loss).
EMERGENCY = 'EMERGENCY'

# Error - Any error which is fatal to the operation, but not the service or
# application (can't open a required file, missing data, etc.)
CRITICAL = 'CRITICAL'

# ALERT - Anything that can potentially cause application oddities
ALERT = 'ALERT'

# Info - Generally useful information to log (service start/stop, configuration assumptions, etc).
INFO = 'INFO'

# Debug - Information that is diagnostically helpful to people more than just
# developers (IT, sysadmins, etc.).
DEBUG = 'DEBUG'

# Trace - Only when you would be "tracing" the code and trying to find one part
# of a function specifically.
TRACE = 'TRACE'

HOSTNAME = socket.gethostname()

def log_error(severity, api_name, user_id, **kwargs):
		logger.log(logging.ERROR,
							 str(HOSTNAME) + ' - ' +
							 str(severity) + ' - ' +
							 str(api_name) + ' - ' +
							 str(user_id) + ' - ' +
							 str(json.dumps(kwargs)))
