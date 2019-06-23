from datetime import datetime
from random import randint

def rand_four_digit():
	return randint(1000, 9999)

def generate_unique_id(key):

	dt = datetime.now()
	return (  key + str(dt.year) + str(dt.month) + str(dt.day)
			+ str(dt.hour) + str(dt.minute) + str(dt.second)
			+ str(dt.microsecond) + str(rand_four_digit())
			+ "IPPA")