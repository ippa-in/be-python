import boto3

from datetime import datetime
from random import randint

from server_config import *

def rand_four_digit():
	return randint(1000, 9999)

def generate_unique_id(key):

	dt = datetime.now()
	return (  key + str(dt.year) + str(dt.month) + str(dt.day)
			+ str(dt.hour) + str(dt.minute) + str(dt.second)
			+ str(dt.microsecond) + str(rand_four_digit())
			+ "IPPA")

def copy_content_to_s3(file, key):

	file_s3_url = S3_URL + "/" + key

	client = boto3.client('s3', aws_access_key_id=AWS_SECRET_KEY_ID,
								aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
	client.put_object(ACL='public-read', Body=file, Bucket=S3_BUCKET_NAME, Key=key)

	return file_s3_url


