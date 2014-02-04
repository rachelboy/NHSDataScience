import os

'''
def config_initial_ingest():
	self.data_directory = ''
	self.infilename = ''
	self.outfilename = 'ingest_10.2013.csv'
'''
class Config():

	def __init__(self):
		#directory containing all the data files
		self.data_directory = "/home/rboy/DataSci/NHS"
		os.chdir(self.data_directory)
		self.keys = {'practice':'PRACTICE','bnf':'BNF CODE',
		                 'items':'ITEMS  ','nic':'NIC        '}

	def config_initial_ingest(self):
		#list of (file of raw data, file to write selected data to)
		self.filenames = [('prescribing.csv','Sep2013Drug.csv')]
