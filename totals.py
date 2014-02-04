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


if __name__ == "__main__":
	Config = config.Config()
	costs = pandas.read_csv("SummedByDrug.csv").to_dict(outtype='list')
	pmf = ts.MakePmfFromList(costs[Config.keys['nic']])
	cdf = pmf.MakeCdf()

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
