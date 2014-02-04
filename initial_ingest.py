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

if __name__ == "__main__":
	Config = config.Config() #changes directory to data_directory in config
	initial_ingest(Config)
