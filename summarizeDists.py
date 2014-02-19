import util
import config
import thinkplot as tp
import thinkstats as ts
import pandas
import matplotlib.pyplot as pp
import numpy as np
import csv



def plotDataFrame(df,key):
	plotEverything(df.to_dict(outtype='list'),key)

def plotFile(infile,key):
	plotDataFrame(pandas.read_csv(infile),key)







def plotTransform(dataframe,xLabel,yLabel,transform=(lambda x: x),transformName = ""):
	pp.scatter(transform(dataframe[xLabel]),transform(dataframe[yLabel]))
	pp.ylabel(transformName+" "+yLabel)
	pp.xlabel(transformName+" "+xLabel)

def findCorr(dataframe,xLabel,yLabel,transform):
	return ts.LeastSquares(transform(dataframe[xLabel]),transform(dataframe[yLabel]))

def plotCostVQuantity(filenames,Config):
	for datafile in datafiles:
		print datafile

		df = pandas.read_csv(datafile)
		df = util.sumBy(df,Config.keys['bnf'])

		df['ITEM COST'] = df[Config.keys['nic']]/df[Config.keys['quantity']]

		plotTransform(df,'ITEM COST',Config.keys['quantity'],np.log,"Log")
		inter,slope = findCorr(df,'ITEM COST',Config.keys['quantity'],np.log)
		ys = [inter+slope*x for x in np.log(df['ITEM COST'])]
		pp.scatter(np.log(df['ITEM COST']),ys,color='red')
		pp.show()



if __name__ == "__main__":
	Config = config.TestConfig()
	datafiles = ["CompressedData/tiny.csv"]

	generateBnfStats(Config)

	'''plotCostVQuantity(datafiles,Config)'''

	