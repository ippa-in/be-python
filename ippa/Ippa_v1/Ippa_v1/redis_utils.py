import redis

from .server_config import HOST

r = redis.Redis(host=HOST)

#set value with 15 min expiry time.
def set_token_exp(key, value, ttl=604800):
	r.setex(key, ttl ,value)

#set token without expiry time
def set_token(key, value):
	r.set(key, value)

#get value of token
def get_token(key):
	return r.get(key)

def is_token_exists(key):
	return r.exists(key)

def set_expire_time(key, ttl=604800):
	r.set(key, ttl)