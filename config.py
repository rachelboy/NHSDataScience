import os


class Config(object):

	def __init__(self, changeDir=True):
		#directory containing all the data files
		self.data_directory = "/media/rboy/22A7-AB54"
		if changeDir:
			os.chdir(self.data_directory)
		self.keys = {'practice':'PRACTICE','pct': 'PCT','bnf':'BNF CODE',
		                 'items':'ITEMS  ','nic':'NIC        ',
		                 'quantity':'QUANTITY', 'post code':'postal code',
		                 'gen':'GENERIC', 'ccg':'CCG'}
		self.filenames = ['Oct2013.csv', 'Sep2013.csv', 'Aug2013.csv', 
					'Jul2013.csv', 'Jun2013.csv', 'May2013.csv', 'Apr2013.csv', 
					'Mar2013.csv', 'Feb2013.csv', 'Jan2013.csv', 'Dec2012.csv', 
					'Nov2012.csv', 'Oct2012.csv', 'Sep2012.csv', 'Aug2012.csv', 
					'Jul2012.csv','Jun2012.csv', 'May2012.csv', 'Apr2012.csv', 
					'Mar2012.csv', 'Feb2012.csv', 'Jan2012.csv']
		self.before_ccgs = ['Mar2013.csv', 'Feb2013.csv', 'Jan2013.csv', 'Dec2012.csv', 
					'Nov2012.csv', 'Oct2012.csv', 'Sep2012.csv', 'Aug2012.csv', 
					'Jul2012.csv','Jun2012.csv', 'May2012.csv', 'Apr2012.csv', 
					'Mar2012.csv', 'Feb2012.csv', 'Jan2012.csv']
		self.ppis_file = 'Criteria/ppis.csv'
		self.naproxen_file = 'NSAID/naproxen.csv'
		self.diclofenac_file = 'NSAID/diclofenac.csv'
		self.psych_file = 'Criteria/antipsychotics.csv'
		self.CCGfile = 'Criteria/practiceToCCG.csv'
		self.directories = {'PCT_to_CCG_in':'RawData', 'PCT_to_CCG_out':'CCGConverted',
							'Ingest_in': 'CCGConverted', 'Ingest_out': 'CompressedData',
							'Join_ppis_in':'CompressedData', 'Join_ppis_out':'JoinedPpis',
							'Join_post_codes_in': 'JoinedPpis', 'Addresses':'Addresses', 'Join_post_codes_out': 'JoinedAdds',
							'Sep_brand_generic_in': 'JoinedAdds', 'Sep_brand_out':'SepBrand','Sep_generic_out':'SepGeneric',
							'Summary_stats_in': ['CompressedData','JoinedPpis','SepBrand','SepGeneric'], 'Summary_stats_out': 'Results',
							'WriteRatioDatasetBrand': 'SepBrand', 'WriteRatioDatasetGeneric': 'SepGeneric', 'WriteRatioDatasetOut':'RatioDataset',
							'OutCodeRatiosIn': 'RatioDataset', 'OutCodeRatiosOut': 'OutCodeRatios',
							'MakeDrugPairsIn': 'JoinedAdds', 'MakeDrugPairsOut': 'PracticePpiDrugPairings',
							'OutCodeDrugsIn': 'PracticePpiDrugPairings', 'OutCodeDrugsOut': 'OutCodePpiPairings',
							'CorrsIn': ['JoinedPpis','SepBrand','SepGeneric'],
							'AllDrugsIn': 'PracticePpiDrugPairings', 'AllDrugsOut': 'PpiDrugPairings'}
		self.nsaid_directories = {'Ingest_in' : 'CCGConverted', 'Ingest_out_nap' : 'NapCompressedData', 'Ingest_out_dic' : 'DicCompressedData',
									'Sum_by_practice_in_nap': 'NapCompressedData', 'Sum_by_practice_in_dic':'DicCompressedData', 'Sum_by_practice_out':'NSAIDSummed'}
		self.psych_directories = {'Ingest_in' : 'CCGConverted', 'Ingest_out' : 'JoinedPsych'}
	def append_dir(self, directory, group = 'PPIS'):
		if group == 'PPIS':
			return [self.directories.get(directory,directory) + '/' +  item for item in self.filenames]
		if group == 'NSAID':
			return [self.nsaid_directories.get(directory,directory) + '/' +  item for item in self.filenames]
		if group == 'psych':
			return [self.psych_directories.get(directory,directory) + '/' +  item for item in self.filenames]

class TestConfig(Config):

	def __init__(self):
		#directory containing all the data files
		super(TestConfig,self).__init__(changeDir = False)
		
		#self.data_directory = "/home/jgorson/DataScience/NHS/test_environment"
		self.data_directory = "/home/rboy/DataSci/NHS"
		os.chdir(self.data_directory)
		self.filenames=['tiny.csv']


