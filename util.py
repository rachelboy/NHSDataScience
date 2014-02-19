import thinkplot as tp
import thinkstats as ts
import pandas
import numpy as np

def sumBy(df,key):
	return df.groupby(key, as_index=False).aggregate(np.sum)

def printVals(df,key,keyVal,cols):
	for index,row in df.iterrows():
		if row[key] == keyVal:
			print [row[col] for col in cols]

def plotEverything(infile,key):
	data = pandas.read_csv(infile).to_dict(outtype='list')
	pmf = ts.MakePmfFromList(data[key])
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
	xs, ys = ts.NormalProbability(data[key])
	tp.Plot(xs, ys)
	tp.Config(title='normal')

	tp.SubPlot(2, 3, 5)
	scale = tp.Cdf(cdf, transform='pareto')
	tp.Config(title='pareto', **scale)

	tp.SubPlot(2, 3, 6)
	scale = tp.Cdf(cdf, transform='weibull')
	tp.Config(title='weibull', **scale)

	tp.Show()


def selectBNFPrefix(Config,df,prefix):
	 criterion = df[Config.keys['bnf']].map(lambda x: x.startswith(prefix))
	 return df[criterion]