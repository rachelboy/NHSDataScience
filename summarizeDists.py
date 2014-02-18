import util
import config
import thinkplot as tp
import thinkstats as ts
import pandas
import matplotlib.pyplot as pp
import numpy as np
import csv


def plotEverything(dataList,key,pmf=None,cdf=None,out=None):
	if not pmf:
		pmf = ts.MakePmfFromList(dataList[key])
	if not cdf:
		cdf = pmf.MakeCdf()

	tp.SubPlot(2, 3, 1)
	tp.Pmf(pmf)
	tp.Config(title='pmf')

	tp.SubPlot(2, 3, 2)
	scale = tp.Cdf(cdf, xscale='log')
	tp.Config(title='logx', **scale)

	tp.SubPlot(2, 3, 3)
	scale = tp.Cdf(cdf, transform='exponential')
	tp.Config(title='expo', **scale)

	tp.SubPlot(2, 3, 4)
	xs, ys = ts.NormalProbability(dataList[key])
	tp.Plot(xs, ys)
	tp.Config(title='normal')

	tp.SubPlot(2, 3, 5)
	scale = tp.Cdf(cdf, transform='pareto')
	tp.Config(title='pareto', **scale)

	tp.SubPlot(2, 3, 6)
	scale = tp.Cdf(cdf, transform='weibull')
	tp.Config(title='weibull', **scale)

	tp.Show()

def plotDataFrame(df,key):
	plotEverything(df.to_dict(outtype='list'),key)

def plotFile(infile,key):
	plotDataFrame(pandas.read_csv(infile),key)

def getStats(pmf,cdf=None):
	if not cdf:
		cdf = pmf.MakeCdf()
	return {'Mean':pmf.Mean(), 'Median':cdf.Value(.5), 
			'StdDev': (pmf.Var())**.5}

def examineDist(dataframe,key,visual=True):
	data = dataframe.to_dict(outtype='list')
	pmf = ts.MakePmfFromList(data[key])
	cdf = pmf.MakeCdf()

	stats = getStats(pmf,cdf=cdf)

	if visual:
		print "Mean", stats['Mean']
		print "Median", stats['Median']
		print "Standard Deviation", stats['StdDev']

		try:
			plotEverything(data,key,pmf=pmf,cdf=cdf, out='temp.png')
		except:
			tp.Show()
			print data
			print "something broke in the plotting"

	return stats

def ExpendituresDist(dataframe,Config,visual = True):
	return examineDist(dataframe,Config.keys['nic'],visual=visual)

def CostsDist(dataframe,Config,visual=True):
	dataframe['ITEM COST'] = dataframe[Config.keys['nic']]/dataframe[Config.keys['quantity']]
	return examineDist(dataframe,'ITEM COST',visual=visual)

def QuantityDist(dataframe,Config,visual=True):
	return examineDist(dataframe,Config.keys['quantity'],visual=visual)

def examineBnfDists(datafiles,Config,distFun,outfile=None,visual=True):
	if outfile:
		out = open(outfile,'wb')
		writer = csv.writer(out)
		writer.writerow(['Date','Mean','Median','Std Dev'])
	for datafile in datafiles:
		print datafile

		df = pandas.read_csv(datafile)
		df = util.sumBy(df,Config.keys['bnf'])

		stats = distFun(df,Config,visual=visual)

		if outfile:
			writer.writerow(
				[datafile[-11:-4],stats['Mean'],stats['Median'],stats['StdDev']])
	if outfile:
		out.close()

def generateBnfStats(Config):
	inputs = [Config.append_dir(dirc) for dirc in Config.directories['Summary_stats_in']]
	distFuns = [('Expenditures',ExpendituresDist),('Costs',CostsDist),('Quantity',QuantityDist)]
	for files, dirname in zip(inputs,Config.directories['Summary_stats_in']):
		for distFun in distFuns:
			outfile = Config.directories['Summary_stats_out']+'/'+dirname+'_'+distFun[0]+'_SummaryStats'
			examineBnfDists(files,Config,distFun[1],outfile=outfile,visual=False)

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

	