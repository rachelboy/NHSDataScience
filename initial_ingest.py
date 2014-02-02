import pandas
from os.path import expanduser
import os
from config.py import config_initial_ingest

def initial_ingest():
	home = expanduser("~")
	os.chdir(config.data_directory)
	df = pandas.read_csv(config.infilename)
	new_df = df[2,3,5,6]#list columns you want
	pandas.new_df.to_csv(config.outfilename)
