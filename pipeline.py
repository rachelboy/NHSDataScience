import config
import pandas
from os.path import expanduser
import os
import config

class Pipeline:
	def __init__(self,Config):
		self.Config = Config


	def loadDF(self,filename):
		try:
			return pandas.read_csv(filename)
		except:
			print "file", filename, "not found in", self.Config.data_directory
			return False

class Initial_ingest(Pipeline):

	def run(self):
		'''Pull out only the columns we want from the data files
		   specified in Config'''

		for (infile, outfile) in zip(self.Config.append_dir("Ingest_in"),self.Config.append_dir("Ingest_out")):
			df = self.loadDF(infile)
			if not df:
				continue
			new_df = df.loc[:,[self.Config.keys['practice'],self.Config.keys['bnf']
			                  ,self.Config.keys['items'],self.Config.keys['quantity']
			                  ,self.Config.keys['nic']]]
			new_df.to_csv(outfile,index=False)

class Join_ppis(Pipeline):

	def run(self):
		'''attach post codes for each practice'''

		try:
			ppisfile = pandas.read_csv(self.Config.ppis_file, header=None)
		except:
			print "file", infile, "not found in", self.Config.data_directory
			return
		for (datafile, outfile) in zip(self.Config.append_dir("Join_ppis_in"),self.Config.append_dir("Join_ppis_out")):
			rxs = self.loadDF(datafile)
			if not rxs:
				continue
		
			include = ppis.loc[:,["BNFCODE","INCLUDE","GENERIC"]]
			joined = pandas.merge(rxs,postCodes,
				left_on=self.Config.keys["bnf"],
				right_on="BNFCODE",
				how="left",
				sort=False)
			joined = joined.drop("BNFCODE",1)
			grouped = joined.groupby('INCLUDE')
			grouped.get_group('1').to_csv(outfile,index=False)

			# df['DRUG TYPE'] = df.apply(lambda row: 
			# 	'Generic' if self.isGeneric(row[self.Config.keys['bnf']]) else 'Brand'
			# 	,axis=1)

			# grouped = df.groupby('DRUG TYPE')
			# grouped.get_group('Brand').to_csv(outfile_brand,index=False)
			# grouped.get_group('Generic').to_csv(outfile_gen,index=False)

class Join_post_codes(Pipeline):

	def run(self):
		'''attach post codes for each practice'''
		try:
			addresses = pandas.read_csv(addsfile,
				header=None, 
				names=["practice","name","parent org","street",
				"town","county",self.Config.keys['post code']])
		except:
			print "address file not found in", self.Config.data_directory
			return

		for (datafile,outfile,addsfile) in zip(self.Config.append_dir("Join_post_codes_in"), self.Config.append_dir("Join_post_codes_out"),self.Config.append_dir("Join_post_codes_out")):
			rxs = self.loadDF(datafile)
			if not rxs:
				continue
			postCodes = addresses.loc[:,["practice",self.Config.keys['post code']]]
			joined = pandas.merge(rxs,postCodes,
				left_on=self.Config.keys["practice"],
				right_on="practice",
				how="left",
				sort=False)
			joined = joined.drop("practice",1)
			joined.to_csv(outfile,index=False)
class Sep_brand_generic(Pipeline):

	def isGeneric(self,bnf):
		'''Check if a drug's bnf is in the right format for a generic'''
		end_bnf = bnf[-4:] 
		return end_bnf[0:2] == end_bnf[2:4]

	def run(self):
		'''put branded and generic drugs in separate files'''
		for (infile, outfile_brand, outfile_gen) in zip(self.Config.append_dir('Sep_brand_generic_in'),self.Config.append_dir('Sep_brand_out'),self.Config.append_dir('Addresses')):
			df = self.loadDF(infile)
			if not df:
				continue

			# df['DRUG TYPE'] = df.apply(lambda row: 
			# 	'Generic' if self.isGeneric(row[self.Config.keys['bnf']]) else 'Brand'
			# 	,axis=1)

			grouped = df.groupby('GENERIC')
			grouped.get_group('0').to_csv(outfile_brand,index=False)
			grouped.get_group('1').to_csv(outfile_gen,index=False)



if __name__ == "__main__":
	Config = config.Config() #changes directory to data_directory in config
	next = Initial_ingest(Config)
	next.run()
	next = Join_post_codes(Config)
	next.run()
	next = Join_ppis(Config)
	next.run()
	next = Sep_brand_generic(Config)
	next.run()
