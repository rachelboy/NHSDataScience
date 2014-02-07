import config
import pandas
from os.path import expanduser
import os
import config

def initial_ingest(Config):
	'''Pull out only the columns we want from the data files
	   specified in Config'''
	Config.config_initial_ingest()
	for infile, outfile in Config.filenames:
		try:
			df = pandas.read_csv(infile)
		except:
			print "file", infile, "not found in", Config.data_directory
			continue
		new_df = df.loc[:,[Config.keys['practice'],Config.keys['bnf']
		                  ,Config.keys['items'],Config.keys['quantity']
		                  ,Config.keys['nic']]]
		new_df.to_csv(outfile,index=False)

def isGeneric(bnf):
	'''Check if a drug's bnf is in the right format for a generic'''
	end_bnf = bnf[-4:] 
	return end_bnf[0:2] == end_bnf[2:4]

def sep_brand_generic(Config):
	'''put branded and generic drugs in separate files'''
	Config.config_sep_brand_generic()
	for infile, outfile_brand, outfile_gen in Config.filenames:
		try:
			df = pandas.read_csv(infile)
		except:
			print "file", infile, "not found in", Config.data_directory
			continue

		df['DRUG TYPE'] = df.apply(lambda row: 
			'Generic' if isGeneric(row[Config.keys['bnf']]) else 'Brand'
			,axis=1)

		grouped = df.groupby('DRUG TYPE')
		grouped.get_group('Brand').to_csv(outfile_brand,index=False)
		grouped.get_group('Generic').to_csv(outfile_gen,index=False)

def joinPostCodes(Config):
	'''attach post codes for each practice'''
	Config.config_join_addresses()
	for datafile, addsfile, outfile in Config.filenames:
		try:
			rxs = pandas.read_csv(datafile)
		except:
			print "file", infile, "not found in", Config.data_directory
			continue
		try:
			addresses = pandas.read_csv("addresses.csv",
				header=None, 
				names=["practice","name","parent org","street",
				"town","county",Config.keys['post code']])
		except:
			print "file", infile, "not found in", Config.data_directory
			continue
		postCodes = addresses.loc[:,["practice",Config.keys['post code']]]
		joined = pandas.merge(rxs,postCodes,
			left_on=Config.keys["practice"],
			right_on="practice",
			how="left",
			sort=False)
		joined = joined.drop("practice",1)
		joined.to_csv(outfile,index=False)

if __name__ == "__main__":
	Config = config.Config() #changes directory to data_directory in config
	initial_ingest(Config)
	sep_brand_generic(Config)
	joinPostCodes(Config)