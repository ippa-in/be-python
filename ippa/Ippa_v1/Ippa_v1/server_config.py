import os

# Database configurations
SERVER_DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],
    },

}

#Path configurations
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname( __name__ ), '..'))+'/'

#AWS CONFIGURATIONS
AWS_SECRET_KEY_ID = os.environ.get("AWS_SECRET_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

#S3 Bucket configurations.
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
S3_BUCKET_URL = os.environ.get("S3_BUCKET_URL")
S3_URL = S3_BUCKET_URL + "/" + S3_BUCKET_NAME

#Email password
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

#Host detail
HOST_FT_URL = os.environ.get("HOST_FT_URL")
HTTP_PROTOCOL = os.environ.get("HTTP_PROTOCOL")

#Redis detail
HOST = os.environ.get("HOST")