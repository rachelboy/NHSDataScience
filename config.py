import os


class Config():

	def __init__(self):
		#directory containing all the data files
		self.data_directory = "/home/rboy/DataSci/NHS"
		
		os.chdir(self.data_directory)
		self.keys = {'practice':'PRACTICE','bnf':'BNF CODE',
		                 'items':'ITEMS  ','nic':'NIC        ',
		                 'quantity':'QUANTITY', 'post code':'postal code'}

	def config_initial_ingest(self):
		#list of (file of raw data, file to write selected data to)
		self.filenames = [('prescribing.csv','Sep2013Drug.csv')]
	def config_sep_brand_generic(self):
		self.filenames = [('SummedByDrug.csv', 'Sep2013BrandSummed.csv', 'Sep2013GenericSummed.csv'),
						  ('Sep2013Drug.csv','Sep2013Brand.csv','Sep2013Generic.csv')]
	def config_join_addresses(self):
		self.filenames = [('Sep2013Brand.csv', 'addresses.csv', 'Sep2013BrandPC.csv'),
						  ('Sep2013Generic.csv', 'addresses.csv','Sep2013GenericPC.csv')]