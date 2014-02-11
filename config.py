import os


class Config():

	def __init__(self):
		#directory containing all the data files
		self.data_directory = "/home/rboy/DataSci/NHS"
		
		os.chdir(self.data_directory)
		self.keys = {'practice':'PRACTICE','bnf':'BNF CODE',
		                 'items':'ITEMS  ','nic':'NIC        ',
		                 'quantity':'QUANTITY', 'post code':'postal code'}
		self.filenames = [Oct2013.csv, Sep2013.csv, Aug2013.csv, Jul2013.csv, Jun2013.csv, May2013.csv, Apr2013.csv, Mar2013.csv, Feb2013.csv, Jan2013.csv, Dec2012.csv, Nov2012.csv, Oct2012.csv, Sep2012.csv, Aug2012.csv, Jul2012.csv, Jun2012.csv, May2012.csv, Apr2012.csv, Mar2012.csv, Feb2012.csv, Jan2012.csv]
		self.ppis_file = 'Criteria/ppis'
		self.directories ={'Ingest_in': 'RawData', 'Ingest_out': 'CompressedData',
							'Join_ppis_in':'CompressedData', 'Join_ppis_out':'JoinedPpis',
							'Join_post_codes_in': 'JoinedPpis', 'Addresses':'Addresses', 'Join_post_codes_out': 'Grouped',
							'Sep_brand_generic_in': 'Grouped', 'SepBrandOut':'Sep_brand','SepGenericOut':'SepGeneric'
							}
	def addr_to_file(self, directory):
		return [item + '/' + self.directories[directory] for item in self.filenames]
	

