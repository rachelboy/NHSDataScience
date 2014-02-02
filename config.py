import os

class Config():

	def __init__(self):
		#directory containing all the data files
		self.data_directory = "/home/rboy/DataSci/NHS"
		os.chdir(self.data_directory)

	def config_initial_ingest(self):
		#list of (file of raw data, file to write selected data to)
		self.filenames = [('prescribing.csv','Sep2013Drug.csv')]
