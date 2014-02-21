import util
import config
import pandas
import os


def loadDF(filename):
	print "Loading", filename
	try:
		return pandas.read_csv(filename)
	except:
		print "trouble loading", filename
		return False


def calc_drug_over_time(Config):
	folder = 'SepGeneric'
	infiles = Config.append_dir(folder)

	drugs = {}

	for month in infiles:
		df = loadDF(month)
		month = month[-11:-4]
		grouped = util.sumBy(df,Config.keys['bnf'])

		for index,row in grouped.iterrows():
			item =row[Config.keys['bnf']]
			
			if item in drugs.keys():
				drugs[item][month] = (row[Config.keys['quantity']],row[Config.keys['nic']])
			else:
				drugs[item] = {}
				drugs[item][month] = (row[Config.keys['quantity']],row[Config.keys['nic']])

	print drugs

if __name__ == "__main__":

	Config = config.Config()
	calc_drug_over_time(Config)



