import os


class Config(object):

	def __init__(self, changeDir=True):
		#directory containing all the data files
		self.data_directory = "/media/rboy/22A7-AB54"
		if changeDir:
			os.chdir(self.data_directory)
		self.keys = {'practice':'PRACTICE','bnf':'BNF CODE',
		                 'items':'ITEMS  ','nic':'NIC        ',
		                 'quantity':'QUANTITY', 'post code':'postal code'}
		self.filenames = ['Oct2013.csv', 'Sep2013.csv', 'Aug2013.csv', 
					'Jul2013.csv', 'Jun2013.csv', 'May2013.csv', 'Apr2013.csv', 
					'Mar2013.csv', 'Feb2013.csv', 'Jan2013.csv', 'Dec2012.csv', 
					'Nov2012.csv', 'Oct2012.csv', 'Sep2012.csv', 'Aug2012.csv', 
					'Jul2012.csv', 'Jun2012.csv', 'May2012.csv', 'Apr2012.csv', 
					'Mar2012.csv', 'Feb2012.csv', 'Jan2012.csv']
		self.ppis_file = 'Criteria/ppis.csv'
		self.directories ={'Ingest_in': 'RawData', 'Ingest_out': 'CompressedData',
							'Join_ppis_in':'CompressedData', 'Join_ppis_out':'JoinedPpis',
							'Join_post_codes_in': 'JoinedPpis', 'Addresses':'Addresses', 'Join_post_codes_out': 'JoinedAdds',
							'Sep_brand_generic_in': 'JoinedAdds', 'Sep_brand_out':'SepBrand','Sep_generic_out':'SepGeneric',
							'Summary_stats_in': ['CompressedData','JoinedPpis','SepBrand','SepGeneric'], 'Summary_stats_out': 'Results'
							'WriteRatioDatasetBrand': 'SepBrand', 'WriteRatioDatasetGeneric': 'SepGeneric'
							}
	def append_dir(self, directory):
		return [self.directories.get(directory,directory) + '/' +  item for item in self.filenames]
	

class TestConfig(Config):

	def __init__(self):
		#directory containing all the data files
		super(TestConfig,self).__init__(changeDir = False)
		
		self.data_directory = "/home/rboy/DataSci/NHS"
		os.chdir(self.data_directory)
		self.filenames=['tiny.csv']


