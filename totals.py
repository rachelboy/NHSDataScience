import config
import pandas
import numpy as np
import thinkstats as ts
import thinkplot

def sumBy(df,key):
	return df.groupby(key).aggregate(np.sum)

def testSumBy():
	df = pandas.DataFrame.from_dict(
		{'A':['a','b','a','b','c']
		,'B':['AA','BB','CC','DD','EE']
		,'C':[1.0,2.0,3.0,4.0,5.0]
		,'D':['1.0','2.0','3.0','4.0','5,0']})
	summed = sumBy(df,'A')
	print summed

def makeDrugSums():
	Config = config.Config()
	df = pandas.read_csv("Sep2013Drug.csv")
	summed = sumBy(df,Config.keys['bnf'])
	summed.to_csv('SummedByDrug.csv')

def makeDrugPostalSums():
	Config = config.Config()
	Config.config_join_addresses()
	for infile, adds, outfile in Config.filenames:
		try:
			df = pandas.read_csv(outfile)
		except:
			print "file", infile, "not found in", Config.data_directory
			continue
		df['POST AREA'] = df.apply(lambda row: 
			row[Config.keys['post code']][0:4]
			,axis=1)
		summed = sumBy(df,[Config.keys['bnf'],'POST AREA'])
		summed.to_csv(outfile[0:-4]+'Summed.csv')



	
	


	
