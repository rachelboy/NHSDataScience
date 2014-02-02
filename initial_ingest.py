import pandas
import os
import config
def initial_ingest(Config):
	Config.config_initial_ingest()
	for infile, outfile in Config.filenames:
		df = pandas.read_csv(infile)
		new_df = df.loc[:,['PRACTICE','BNF CODE','ITEMS  ','NIC        ']]#list columns you want
		new_df.to_csv(outfile)

if __name__ == "__main__":
	Config = config.Config()
	initial_ingest(Config)