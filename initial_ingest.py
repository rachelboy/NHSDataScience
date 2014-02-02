import pandas
import os
def initial_ingest():
	#change directory to data directory config.data_directory
	df = pandas.read_csv(config.infilename)
	new_df = df[]#list columns you want
	pandas.new_df.to_csv(config.outfilename)
