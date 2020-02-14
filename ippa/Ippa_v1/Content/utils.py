import os
import csv
import pandas as pd

def read_excel_file(file):

	"""
	File format should be below.
	col1	col2	col3
	1		2		3
	4		5		6
	"""

	#save file locally.
	with open('temp_file.xlsx', 'w') as f:
		f.write(file.read())

	#read from temp file.
	data_frame = pd.read_excel('temp_file.xlsx')
	data_dict = data_frame.to_dict('records')
	return data_dict

def read_csv_file(file):

	"""
	File format should be below.
	col1,col2,col3
	1,2,3
	4,5,6
	"""

	points_data = list()
	#read from temp file.
	with open('temp_file.txt', 'w') as f:
		f.write(file.read())
	with open('temp_file.txt') as f:
		data_dict = csv.DictReader(f, delimiter=',')
		for data in data_dict:
			points_data.append(data)
	return points_data




