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

def plotEverything(pmf,cdf):
	thinkplot.SubPlot(2, 3, 1)
	thinkplot.Pmf(pmf)
	thinkplot.Config(title='pmf')

	thinkplot.SubPlot(2, 3, 2)
	scale = thinkplot.Cdf(cdf, xscale='log')
	thinkplot.Config(title='logx', **scale)

	thinkplot.SubPlot(2, 3, 3)
	scale = thinkplot.Cdf(cdf, transform='exponential')
	thinkplot.Config(title='expo', **scale)

	thinkplot.SubPlot(2, 3, 4)
	xs, ys = ts.NormalProbability(costs[Config.keys['nic']])
	thinkplot.Plot(xs, ys)
	thinkplot.Config(title='normal')

	thinkplot.SubPlot(2, 3, 5)
	scale = thinkplot.Cdf(cdf, transform='pareto')
	thinkplot.Config(title='pareto', **scale)

	thinkplot.SubPlot(2, 3, 6)
	scale = thinkplot.Cdf(cdf, transform='weibull')
	thinkplot.Config(title='weibull', **scale)

	thinkplot.Show()

def makeDists(infile,key):
	data = pandas.read_csv(infile).to_dict(outtype='list')
	pmf = ts.MakePmfFromList(data[key])
	cdf = pmf.MakeCdf()
	return pmf,cdf



	
	


	
