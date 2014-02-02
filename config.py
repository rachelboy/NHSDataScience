import os

class Config():

	def __init__(self):
		self.data_directory = "/home/rboy/DataSci/NHS"
		os.chdir(self.data_directory)

	def config_initial_ingest(self):
		self.filenames = [('prescribing.csv','Sep2013Drug.csv')]
